use crate::board::{Board, RAM_BASE, RAM_SIZE};
use crate::exception::InvalidControlCause;
use crate::loader::{ElfLoadError, ElfLoadOptions, ElfLoadResult, load_elf};
use crate::trap::{DivideErrorCause, IllegalInstructionCause};
use crate::{
    AccessDomain, AccessFaultContext, AccessFaultReason, AccessKind, CpuRegister, CpuState, Flags,
    PageFaultContext, PageFaultReason, SegmentRegister, SegmentSelector, Status, StepResult, Trap,
    VectorRangeErrorCause,
};
use bedrock_bus::BusResult;
use bedrock_sail_core::{
    SailBusExecutionError, SailCore, SailCoreCreateError, SailCoreRequest, SailCoreState,
    SailCoreStatus,
};

pub const DEFAULT_STACK_POINTER: u64 = RAM_BASE + RAM_SIZE;

pub struct Machine {
    core: SailCore,
    state: CpuState,
    board: Board,
}

impl std::fmt::Debug for Machine {
    fn fmt(&self, formatter: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        formatter
            .debug_struct("Machine")
            .field("core", &self.core)
            .field("state", &self.state)
            .field("board", &self.board)
            .finish()
    }
}

impl Clone for Machine {
    fn clone(&self) -> Self {
        let core = self
            .core
            .try_clone()
            .expect("Sail core could not clone architectural state");
        Self {
            core,
            state: self.state.clone(),
            board: self.board.clone(),
        }
    }
}

impl PartialEq for Machine {
    fn eq(&self, other: &Self) -> bool {
        self.core.state() == other.core.state()
            && self.core.environment_state() == other.core.environment_state()
            && self.state == other.state
            && self.board == other.board
    }
}

impl Eq for Machine {}

impl Default for Machine {
    fn default() -> Self {
        Self::new()
    }
}

impl Machine {
    pub fn new() -> Self {
        let core = new_core();
        let state = snapshot_state(
            &core
                .state()
                .expect("new Sail core did not expose its initial state"),
        );
        Self {
            core,
            state,
            board: Board::new(),
        }
    }

    pub fn state(&self) -> &CpuState {
        &self.state
    }

    /// Replace the observer-facing state cache without mutating the Sail core.
    ///
    /// Frontends may use this while another `Machine` owns execution. The
    /// cached state must not be used to resume this machine; a complete
    /// executing machine must be transferred back first.
    pub fn set_observer_state(&mut self, state: CpuState) {
        self.state = state;
    }

    pub fn set_state(&mut self, state: CpuState) -> Result<(), SailCoreStatus> {
        let mut raw = self.core.state()?;
        write_state(&mut raw, &state);
        match self.core.set_state(raw) {
            SailCoreStatus::Ok => {
                self.refresh_state()?;
                Ok(())
            }
            status => Err(status),
        }
    }

    pub fn set_pc(&mut self, pc: u64) -> Result<(), SailCoreStatus> {
        let mut state = self.state.clone();
        state.pc = pc;
        self.set_state(state)
    }

    pub fn write_register(
        &mut self,
        register: CpuRegister,
        value: u64,
    ) -> Result<(), SailCoreStatus> {
        let mut state = self.state.clone();
        state.write_register(register, value);
        self.set_state(state)
    }

    pub fn post_interrupt(&mut self, identity: u32) -> Result<(), SailCoreStatus> {
        match self.core.post_interrupt(identity) {
            SailCoreStatus::Ok => {
                self.refresh_state()?;
                Ok(())
            }
            status => Err(status),
        }
    }

    pub fn advance_time(&mut self, ticks: u64) -> Result<(), SailCoreStatus> {
        match self.core.advance_time(ticks) {
            SailCoreStatus::Ok => {
                self.refresh_state()?;
                Ok(())
            }
            status => Err(status),
        }
    }

    pub fn board(&self) -> &Board {
        &self.board
    }

    pub fn board_mut(&mut self) -> &mut Board {
        &mut self.board
    }

    pub fn processor_reset(&mut self, pc: u64) {
        assert_eq!(self.core.reset(), SailCoreStatus::Ok);
        assert_eq!(self.core.set_pc(pc), SailCoreStatus::Ok);
        assert_eq!(self.core.set_sp(DEFAULT_STACK_POINTER), SailCoreStatus::Ok);
        self.refresh_state()
            .expect("Sail core did not expose reset state");
    }

    pub fn system_reset(&mut self, pc: u64) {
        self.board = Board::new();
        self.processor_reset(pc);
    }

    pub fn load_program(&mut self, addr: u64, bytes: &[u8]) -> BusResult<()> {
        self.board.load_ram(addr, bytes)
    }

    pub fn load_elf(
        &mut self,
        bytes: &[u8],
        options: ElfLoadOptions,
    ) -> Result<ElfLoadResult, ElfLoadError> {
        let result = load_elf(&mut self.board, bytes, options)?;
        self.processor_reset(result.entry);
        Ok(result)
    }

    pub fn step(&mut self) -> StepResult {
        let pc = self.state.pc;
        let result = self.core.step_on_bus(&mut self.board);
        let raw = self.core.state();
        if let Ok(raw) = &raw {
            self.state = snapshot_state(raw);
        }
        match result {
            Ok(()) => match raw {
                Ok(raw) if raw.halted != 0 || raw.run_state != 0 => StepResult::Halted,
                Ok(_) => StepResult::Running,
                Err(status) => core_status_trap(pc, status),
            },
            Err(error) => execution_error(pc, error, &self.state),
        }
    }

    fn refresh_state(&mut self) -> Result<(), SailCoreStatus> {
        self.state = snapshot_state(&self.core.state()?);
        Ok(())
    }
}

fn new_core() -> SailCore {
    SailCore::new().unwrap_or_else(|SailCoreCreateError::Status(status)| {
        panic!("failed to create Sail core: {status:?}")
    })
}

fn snapshot_state(raw: &SailCoreState) -> CpuState {
    let mut segments = crate::SegmentRegisters::default();
    for selector in SEGMENT_SELECTORS {
        segments.set(
            selector,
            SegmentRegister::from_raw(raw.segments[selector as usize]),
        );
    }
    CpuState {
        r: raw.registers,
        f: raw.floating_registers,
        v: raw.vector_registers,
        p: raw.predicate_registers,
        sp: raw.sp,
        pc: raw.pc,
        flags: Flags::from_bits_truncate(raw.flags as u16),
        status: Status::from_bits_truncate(raw.status as u16),
        segments,
        ptcr: crate::PageTableControl::from_raw(raw.controls.base_ptcr),
        ascr: crate::AddressSpaceControl::from_raw(raw.controls.base_ascr),
        ecr: crate::EventControl::from_raw(raw.controls.base_ecr),
        upc: raw.controls.base_upc,
        usp: raw.controls.base_usp,
        ucs: SegmentRegister::from_raw(raw.controls.base_ucs),
        uds: SegmentRegister::from_raw(raw.controls.base_uds),
        uss: SegmentRegister::from_raw(raw.controls.base_uss),
        uctl: raw.controls.base_uctl,
        uinfo: raw.controls.base_uinfo,
        epc: raw.controls.base_epc,
        ecs: SegmentRegister::from_raw(raw.controls.base_ecs),
        eds: SegmentRegister::from_raw(raw.controls.base_eds),
        sss: SegmentRegister::from_raw(raw.controls.base_sss),
        ssp: raw.controls.base_ssp,
        iss: SegmentRegister::from_raw(raw.controls.base_iss),
        isp: raw.controls.base_isp,
        fss: SegmentRegister::from_raw(raw.controls.base_fss),
        fsp: raw.controls.base_fsp,
        dss: SegmentRegister::from_raw(raw.controls.base_dss),
        dsp: raw.controls.base_dsp,
        bootpc: raw.controls.base_bootpc,
        bootcfg: raw.controls.base_bootcfg,
        pmc: raw.controls.base_pmc,
        fstatus: raw.fstatus as u16,
        fflags: raw.fflags as u16,
        hidden_current_dfa: raw.current_dfa != 0,
    }
}

fn write_state(raw: &mut SailCoreState, state: &CpuState) {
    raw.registers = state.r;
    raw.floating_registers = state.f;
    raw.vector_registers = state.v;
    raw.predicate_registers = state.p;
    raw.sp = state.sp;
    raw.pc = state.pc;
    raw.flags = u64::from(state.flags.bits());
    raw.status = u64::from(state.status.bits());
    for selector in SEGMENT_SELECTORS {
        raw.segments[selector as usize] = state.segments.get(selector).raw();
    }
    raw.controls.base_ptcr = state.ptcr.raw();
    raw.controls.base_ascr = state.ascr.raw();
    raw.controls.base_ecr = state.ecr.raw();
    raw.controls.base_upc = state.upc;
    raw.controls.base_usp = state.usp;
    raw.controls.base_ucs = state.ucs.raw();
    raw.controls.base_uds = state.uds.raw();
    raw.controls.base_uss = state.uss.raw();
    raw.controls.base_uctl = state.uctl;
    raw.controls.base_uinfo = state.uinfo;
    raw.controls.base_epc = state.epc;
    raw.controls.base_ecs = state.ecs.raw();
    raw.controls.base_eds = state.eds.raw();
    raw.controls.base_sss = state.sss.raw();
    raw.controls.base_ssp = state.ssp;
    raw.controls.base_iss = state.iss.raw();
    raw.controls.base_isp = state.isp;
    raw.controls.base_fss = state.fss.raw();
    raw.controls.base_fsp = state.fsp;
    raw.controls.base_dss = state.dss.raw();
    raw.controls.base_dsp = state.dsp;
    raw.controls.base_bootpc = state.bootpc;
    raw.controls.base_bootcfg = state.bootcfg;
    raw.controls.base_pmc = state.pmc;
    raw.fstatus = u64::from(state.fstatus);
    raw.fflags = u64::from(state.fflags);
    raw.current_dfa = u8::from(state.hidden_current_dfa);
    raw.supervisor = u8::from(state.status.contains(Status::PM));
}

fn execution_error(pc: u64, error: SailBusExecutionError, state: &CpuState) -> StepResult {
    match error {
        SailBusExecutionError::Bus(error) => StepResult::Trap(Trap::Bus { pc, error }),
        SailBusExecutionError::Core(status) => core_status_trap(pc, status),
        SailBusExecutionError::Fault { fault, request } => {
            fault_trap(pc, fault.kind, fault.error_code, request.as_deref(), state)
        }
        SailBusExecutionError::InvalidFraming { .. } => {
            illegal_trap(pc, IllegalInstructionCause::InsufficientLength)
        }
        SailBusExecutionError::UnsupportedRequest(_)
        | SailBusExecutionError::UnsupportedNumericOperation(_) => {
            StepResult::Trap(Trap::InvalidControlState {
                pc,
                cause: InvalidControlCause::InvalidSelector,
            })
        }
    }
}

fn core_status_trap(pc: u64, status: SailCoreStatus) -> StepResult {
    let cause = match status {
        SailCoreStatus::InvalidInstruction => IllegalInstructionCause::InvalidOpcode,
        _ => IllegalInstructionCause::ExplicitIllegal,
    };
    illegal_trap(pc, cause)
}

fn fault_trap(
    pc: u64,
    kind: i32,
    error_code: u64,
    request: Option<&SailCoreRequest>,
    state: &CpuState,
) -> StepResult {
    match kind {
        2 => StepResult::Trap(Trap::PrivilegeFault { pc }),
        3 => illegal_trap(pc, IllegalInstructionCause::UnavailableExtension),
        4 => StepResult::Trap(Trap::InvalidControlState {
            pc,
            cause: InvalidControlCause::ReservedBits,
        }),
        5 => StepResult::Trap(Trap::InvalidControlState {
            pc,
            cause: InvalidControlCause::InvalidSelector,
        }),
        6 => StepResult::Trap(Trap::InvalidControlState {
            pc,
            cause: InvalidControlCause::ReservedBits,
        }),
        7 => StepResult::Trap(Trap::InvalidControlState {
            pc,
            cause: InvalidControlCause::InvalidImage,
        }),
        8 => StepResult::Trap(Trap::InvalidControlState {
            pc,
            cause: InvalidControlCause::InvalidTransition,
        }),
        9 => StepResult::Trap(Trap::DivideError {
            pc,
            cause: DivideErrorCause::ZeroDivisor,
        }),
        10 => StepResult::Trap(Trap::DivideError {
            pc,
            cause: DivideErrorCause::SignedOverflow,
        }),
        13 => request.map_or_else(
            || illegal_trap(pc, IllegalInstructionCause::ExplicitIllegal),
            |request| page_fault_trap(pc, error_code, request, state),
        ),
        14 => request.map_or_else(
            || illegal_trap(pc, IllegalInstructionCause::ExplicitIllegal),
            |request| access_fault_trap(pc, error_code, request, state),
        ),
        16 => StepResult::Trap(Trap::FloatingPointFault {
            pc,
            causes: crate::FpCauses::from_bits_truncate(error_code as u8),
        }),
        17 => StepResult::Trap(Trap::VectorRangeError {
            pc,
            cause: VectorRangeErrorCause::LaneIndex,
        }),
        _ => illegal_trap(pc, IllegalInstructionCause::ExplicitIllegal),
    }
}

fn page_fault_trap(
    pc: u64,
    error_code: u64,
    request: &SailCoreRequest,
    state: &CpuState,
) -> StepResult {
    let access_kind = request_access_kind(request.access);
    let reason = match error_code as u8 {
        0 => PageFaultReason::NotPresent,
        1 if access_kind == AccessKind::InstructionFetch => PageFaultReason::Execute,
        1 => PageFaultReason::ReadOnly,
        2 => PageFaultReason::InvalidEntry,
        3 => PageFaultReason::NonCanonical,
        4 => PageFaultReason::SegmentBounds,
        5 => PageFaultReason::AtomicAlignment,
        6 => PageFaultReason::MemoryType,
        _ => PageFaultReason::PagingFormatUnavailable,
    };
    StepResult::Trap(Trap::PageFault {
        pc,
        context: PageFaultContext {
            effective_address: request.effective_address,
            linear_address: (reason != PageFaultReason::SegmentBounds)
                .then_some(request.linear_address),
            reason,
            access_kind,
            access_domain: request_access_domain(request.domain),
            segment: request_segment(request.segment),
            asid: state.ascr.asid(),
            access_size: u8::try_from(request.width).ok(),
            operand: (access_kind == AccessKind::InstructionFetch).then_some(0xff),
            atomic: request.access == 3,
        },
    })
}

fn access_fault_trap(
    pc: u64,
    error_code: u64,
    request: &SailCoreRequest,
    state: &CpuState,
) -> StepResult {
    let access_kind = request_access_kind(request.access);
    let reason = match error_code as u8 {
        1 => AccessFaultReason::MmioAlignment,
        2 => AccessFaultReason::MmioOperation,
        _ => AccessFaultReason::PhysicalAddress,
    };
    StepResult::Trap(Trap::AccessFault {
        pc,
        context: AccessFaultContext {
            effective_address: request.effective_address,
            linear_address: Some(request.linear_address),
            reason,
            access_kind,
            access_domain: request_access_domain(request.domain),
            segment: request_segment(request.segment),
            asid: state.ascr.asid(),
            access_size: u8::try_from(request.width).ok(),
            operand: (access_kind == AccessKind::InstructionFetch).then_some(0xff),
            atomic: request.access == 3,
        },
    })
}

fn request_access_kind(access: i32) -> AccessKind {
    match access {
        2 | 3 | 6 => AccessKind::Write,
        4 => AccessKind::InstructionFetch,
        _ => AccessKind::Read,
    }
}

fn request_access_domain(domain: i32) -> AccessDomain {
    if domain == 1 {
        AccessDomain::User
    } else {
        AccessDomain::Current
    }
}

fn request_segment(segment: i64) -> Option<SegmentSelector> {
    match segment {
        0 => Some(SegmentSelector::Cs),
        1 => Some(SegmentSelector::Ds),
        2 => Some(SegmentSelector::Ss),
        3 => Some(SegmentSelector::Gs0),
        4 => Some(SegmentSelector::Gs1),
        5 => Some(SegmentSelector::Gs2),
        6 => Some(SegmentSelector::Gs3),
        7 => Some(SegmentSelector::Gs4),
        8 => Some(SegmentSelector::Gs5),
        _ => None,
    }
}

fn illegal_trap(pc: u64, cause: IllegalInstructionCause) -> StepResult {
    StepResult::Trap(Trap::IllegalInstruction { pc, cause })
}

const SEGMENT_SELECTORS: [SegmentSelector; 9] = [
    SegmentSelector::Cs,
    SegmentSelector::Ds,
    SegmentSelector::Ss,
    SegmentSelector::Gs0,
    SegmentSelector::Gs1,
    SegmentSelector::Gs2,
    SegmentSelector::Gs3,
    SegmentSelector::Gs4,
    SegmentSelector::Gs5,
];

#[cfg(test)]
mod tests {
    use super::Machine;
    use crate::{PageFaultReason, PageTableControl, Status, StepResult, Trap};
    use bedrock_bus::Bus;

    #[test]
    fn processor_reset_preserves_board_state() {
        let mut machine = Machine::new();
        machine
            .board_mut()
            .framebuffer_mut()
            .write_vram_u8(0, 0xaa)
            .unwrap();
        machine.board_mut().keyboard_mut().push_event(0x0001_0041);
        let mut state = machine.state().clone();
        state.r[0] = 0xfeed;
        machine.set_state(state).unwrap();

        machine.processor_reset(0x1234);

        assert_eq!(machine.state().pc, 0x1234);
        assert_eq!(machine.state().sp, super::DEFAULT_STACK_POINTER);
        assert_eq!(machine.state().status, Status::PM);
        assert_eq!(machine.state().r[0], 0);
        assert_eq!(machine.board().framebuffer().vram()[0], 0xaa);
        assert_eq!(machine.board().keyboard().queued_len(), 1);
    }

    #[test]
    fn system_reset_clears_board_state() {
        let mut machine = Machine::new();
        machine
            .board_mut()
            .framebuffer_mut()
            .write_vram_u8(0, 0xaa)
            .unwrap();
        machine.board_mut().keyboard_mut().push_event(0x0001_0041);
        let mut state = machine.state().clone();
        state.r[0] = 0xfeed;
        machine.set_state(state).unwrap();

        machine.system_reset(0x5678);

        assert_eq!(machine.state().pc, 0x5678);
        assert_eq!(machine.state().sp, super::DEFAULT_STACK_POINTER);
        assert_eq!(machine.state().status, Status::PM);
        assert_eq!(machine.state().r[0], 0);
        assert_eq!(machine.board().framebuffer().vram()[0], 0);
        assert_eq!(machine.board().keyboard().queued_len(), 0);
    }

    #[test]
    fn step_executes_through_sail_core() {
        let mut machine = Machine::new();
        machine.load_program(0, &[0x01]).unwrap();
        machine.processor_reset(0);

        assert_eq!(machine.step(), crate::StepResult::Running);
        assert_eq!(machine.state().pc, 1);
    }

    #[test]
    fn observer_state_does_not_mutate_sail_core() {
        let mut machine = Machine::new();
        machine.load_program(0, &[0x01]).unwrap();
        machine.processor_reset(0);
        let mut observed = machine.state().clone();
        observed.pc = 0x100;

        machine.set_observer_state(observed);

        assert_eq!(machine.state().pc, 0x100);
        assert_eq!(machine.step(), StepResult::Running);
        assert_eq!(machine.state().pc, 1);
    }

    #[test]
    fn step_fetches_instruction_through_page_tables() {
        const TABLE: u64 = 0x1f;
        const LEAF_RX: u64 = 0x11;
        let mut machine = Machine::new();
        machine.processor_reset(0);
        machine
            .board_mut()
            .write_u64(0x1000, 0x2000 | TABLE)
            .unwrap();
        machine
            .board_mut()
            .write_u64(0x2000, 0x3000 | TABLE)
            .unwrap();
        machine
            .board_mut()
            .write_u64(0x3000, 0x4000 | TABLE)
            .unwrap();
        machine
            .board_mut()
            .write_u64(0x4000, 0x9000 | LEAF_RX)
            .unwrap();
        machine.load_program(0x9000, &[0x01]).unwrap();
        let mut state = machine.state().clone();
        state.ptcr = PageTableControl::from_raw(0x1001);
        machine.set_state(state).unwrap();

        assert_eq!(machine.step(), StepResult::Running);
        assert_eq!(machine.state().pc, 1);
    }

    #[test]
    fn missing_fetch_page_becomes_page_fault_trap() {
        let mut machine = Machine::new();
        machine.processor_reset(0);
        let mut state = machine.state().clone();
        state.ptcr = PageTableControl::from_raw(0x1001);
        machine.set_state(state).unwrap();

        let StepResult::Trap(Trap::PageFault { pc, context }) = machine.step() else {
            panic!("expected page fault");
        };
        assert_eq!(pc, 0);
        assert_eq!(context.reason, PageFaultReason::NotPresent);
        assert_eq!(context.effective_address, 0);
        assert_eq!(context.linear_address, Some(0));
    }
}
