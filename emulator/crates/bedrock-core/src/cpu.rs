use crate::exception::{
    BaseException, EventClass, EventCode, EventFrameMetadata, EventInfo, ExceptionFrameType,
    FrameControl, InvalidControlCause, RepeatContinuation, RepeatKind,
};
use crate::trap::{DivideErrorCause, IllegalInstructionCause};
use crate::{AccessDomain, AccessKind, Flags, SegmentSelector, Status, StepResult, Trap};
use bedrock_bus::{
    AcknowledgedBusFailure, Bus, BusError, BusFailureCause, RetrySafety, SlotData, SlotOutcome,
    SlotProtocolError, SlotRequest, SlotTransactionError, SlotWidth,
};
use bedrock_isa::{
    AutoUpdate, CompactEa, DecodedInstruction, DestinationOverlapRule, DisplacementWidth,
    Ext0Descriptor, FieldKind, FormId, InstructionSet, MAX_INSTRUCTION_BYTES, Opcode,
    RepeatObservation, RepeatObservedOperand, RepeatOperandLocation, Size, decode, decode_header,
    generated::GENERATED_FORMS,
};
use std::cell::Cell;

const DOUBLE_FAULT_ENTRY_STATE: u64 = 0;
const DOUBLE_FAULT_STACK_STATE: u64 = 1;
const DOUBLE_FAULT_FRAME_ADDRESS: u64 = 2;
const DOUBLE_FAULT_FRAME_STORE: u64 = 3;
const URCTL_VALID: u64 = 1 << 32;
const URCTL_ALLOWED: u64 = (1 << 33) - 1;

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
struct EventRequest {
    code: EventCode,
    saved_pc: u64,
    error_code: u64,
    fault_ea: u64,
    fault_linear: u64,
    event_aux: u64,
}

impl EventRequest {
    const fn exception(exception: BaseException, saved_pc: u64, error_code: u64) -> Self {
        Self {
            code: EventCode::exception(exception),
            saved_pc,
            error_code,
            fault_ea: 0,
            fault_linear: 0,
            event_aux: 0,
        }
    }

    #[allow(dead_code)]
    const fn floating_point_fault(saved_pc: u64, causes: crate::fpu::env::FpCauses) -> Self {
        Self::exception(
            BaseException::FloatingPointFault,
            saved_pc,
            causes.bits() as u64,
        )
    }

    fn nmi(saved_pc: u64) -> Self {
        Self {
            code: EventCode::new(EventClass::Nmi, 0).expect("NMI source zero is representable"),
            saved_pc,
            error_code: 0,
            fault_ea: 0,
            fault_linear: 0,
            event_aux: 0,
        }
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
enum TransactionOutcome {
    Complete(StepResult),
    PostCommit(EventRequest),
}

#[derive(Debug)]
struct DeliveryFailure {
    _trap: Trap,
    stage: u64,
    fault_ea: u64,
    fault_linear: u64,
}

#[derive(Debug, Clone, PartialEq, Eq, Default)]
pub struct Cpu {
    state: crate::CpuState,
    halted: bool,
    repeat: Option<RepeatState>,
    cycle_counter: Cell<u64>,
    instret_counter: Cell<u64>,
    ptwalk_counter: Cell<u64>,
    repeat_ea_result: Cell<Option<u64>>,
    successful_slot_transaction: Cell<bool>,
}

#[derive(Debug, Clone, PartialEq, Eq)]
struct RepeatState {
    counter: u8,
    // Used only by scalar REP/REPcc. Grouped REPG reads its live register.
    remaining: u64,
    condition: u8,
    bodies: Vec<(u64, DecodedInstruction)>,
    index: usize,
    after_pc: u64,
    grouped: bool,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
struct ResolvedAddress {
    linear: u64,
    target: crate::TranslatedTarget,
}

impl Cpu {
    pub fn new() -> Self {
        Self::default()
    }
    pub fn state(&self) -> &crate::CpuState {
        &self.state
    }
    pub fn state_mut(&mut self) -> &mut crate::CpuState {
        &mut self.state
    }
    pub fn is_halted(&self) -> bool {
        self.halted
    }

    /// Latches an architecturally coalesced non-maskable interrupt request.
    /// Admission occurs at the next instruction boundary where ECR.V is set
    /// and STATUS.NI is clear.
    pub fn request_nmi(&mut self) {
        self.state.ecr = self.state.ecr.with_nmi_pending(true);
    }

    pub fn reset(&mut self, pc: u64) {
        self.state.reset(pc);
        self.halted = false;
        self.repeat = None;
        self.cycle_counter.set(0);
        self.instret_counter.set(0);
        self.ptwalk_counter.set(0);
        self.repeat_ea_result.set(None);
        self.successful_slot_transaction.set(false);
    }

    fn performance_monitoring_enabled(&self) -> bool {
        self.state.pmc & 1 != 0
    }

    fn increment_cycle(&self) {
        if self.performance_monitoring_enabled() {
            self.cycle_counter
                .set(self.cycle_counter.get().wrapping_add(1));
        }
    }

    fn increment_instret(&self) {
        if self.performance_monitoring_enabled() {
            self.instret_counter
                .set(self.instret_counter.get().wrapping_add(1));
        }
    }

    fn increment_page_walk(&self, ptcr: crate::PageTableControl) {
        if ptcr.paging_enabled() {
            self.increment_page_walk_counter();
        }
    }

    fn increment_page_walk_counter(&self) {
        if self.performance_monitoring_enabled() {
            self.ptwalk_counter
                .set(self.ptwalk_counter.get().wrapping_add(1));
        }
    }

    pub fn step<B: Bus>(&mut self, bus: &mut B) -> StepResult {
        if self.state.ecr.valid()
            && self.state.ecr.nmi_pending()
            && !self.state.status.contains(Status::NI)
        {
            self.increment_cycle();
            return self.deliver_required_event(bus, EventRequest::nmi(self.state.pc));
        }
        if self.halted {
            return StepResult::Halted;
        }
        self.increment_cycle();
        let pc = self.state.pc;
        self.successful_slot_transaction.set(false);
        if let Err(error) = bus.begin_transaction() {
            return StepResult::Trap(Trap::Bus { pc, error });
        }
        let saved_state = self.state.clone();
        let saved_halted = self.halted;
        let saved_repeat = self.repeat.clone();
        match self.step_transaction(bus, pc) {
            Ok(TransactionOutcome::Complete(result)) => {
                bus.commit_transaction();
                self.increment_instret();
                result
            }
            Ok(TransactionOutcome::PostCommit(request)) => {
                bus.commit_transaction();
                self.increment_instret();
                self.deliver_required_event(bus, request)
            }
            Err(trap) => {
                bus.rollback_transaction();
                self.state = saved_state;
                self.halted = saved_halted;
                self.repeat = saved_repeat;
                let trap = self.normalize_architectural_bus_trap(trap);
                match event_request_from_trap(&trap) {
                    Some(request) => self.deliver_required_event(bus, request),
                    None => StepResult::Trap(trap),
                }
            }
        }
    }

    fn step_transaction<B: Bus>(
        &mut self,
        bus: &mut B,
        pc: u64,
    ) -> Result<TransactionOutcome, Trap> {
        let trace_selected = self.state.status.contains(Status::TF);
        let trace_suppressed = self.state.status.contains(Status::RF);
        if self.repeat.is_some() {
            let active = self.repeat.clone().expect("checked repeat state");
            let result = self.step_repeat(bus, pc)?;
            if active.grouped && self.repeat.as_ref().is_some_and(|next| next.index != 0) {
                return Ok(TransactionOutcome::Complete(result));
            }
            return self.finish_trace_unit(
                bus,
                pc,
                result,
                trace_selected,
                trace_suppressed,
                false,
            );
        }
        let decoded = self.fetch_decode(bus, pc)?;
        if !matches!(
            decoded.attributes.instruction_set,
            InstructionSet::Base | InstructionSet::Fpu | InstructionSet::FpuTranscendental
        ) {
            return Err(Trap::IllegalInstruction {
                pc,
                cause: IllegalInstructionCause::UnavailableExtension,
            });
        }
        if decoded.opcode == Opcode::Ptquery && !(1..=5).contains(&field(&decoded, 'i')) {
            return Err(Trap::IllegalInstruction {
                pc,
                cause: IllegalInstructionCause::ReservedEncoding,
            });
        }
        if decoded.attributes.privileged
            && !self.state.status.contains(Status::PM)
            && decoded.opcode != Opcode::Eret
        {
            return Err(Trap::PrivilegeFault { pc });
        }
        let result = self.execute(bus, pc, &decoded)?;
        if decoded.opcode == Opcode::Bkpt {
            if trace_suppressed {
                self.state.status.remove(Status::RF);
            }
            return Ok(TransactionOutcome::PostCommit(EventRequest::exception(
                BaseException::Breakpoint,
                self.state.pc,
                0,
            )));
        }
        if matches!(decoded.opcode, Opcode::Repcc | Opcode::Repg) && self.repeat.is_some() {
            return Ok(TransactionOutcome::Complete(result));
        }
        self.finish_trace_unit(bus, pc, result, trace_selected, trace_suppressed, false)
    }

    fn finish_trace_unit<B: Bus>(
        &mut self,
        bus: &mut B,
        pc: u64,
        result: StepResult,
        trace_selected: bool,
        trace_suppressed: bool,
        suppress_self_trace: bool,
    ) -> Result<TransactionOutcome, Trap> {
        if result != StepResult::Running {
            return Ok(TransactionOutcome::Complete(result));
        }
        if trace_suppressed {
            self.state.status.remove(Status::RF);
            return Ok(TransactionOutcome::Complete(result));
        }
        if trace_selected && !suppress_self_trace {
            return Ok(TransactionOutcome::PostCommit(EventRequest::exception(
                BaseException::DebugTrace,
                self.state.pc,
                0,
            )));
        }
        let _ = (bus, pc);
        Ok(TransactionOutcome::Complete(result))
    }

    fn fetch_decode<B: Bus>(&self, bus: &mut B, pc: u64) -> Result<DecodedInstruction, Trap> {
        let mut bytes = [0u8; MAX_INSTRUCTION_BYTES];
        let first_address = self.translate_fetch(bus, pc, pc)?;
        bytes[0] = bus
            .read_u8(first_address)
            .map_err(|error| self.fetch_bus_trap(pc, pc, error))?;
        let header_prefix = if bytes[0] & 0xc0 == 0xc0 {
            let logical = self.checked_fetch_offset(pc, 1)?;
            let physical = self.translate_fetch(bus, logical, pc)?;
            bytes[1] = bus
                .read_u8(physical)
                .map_err(|error| self.fetch_bus_trap(pc, logical, error))?;
            &bytes[..2]
        } else {
            &bytes[..1]
        };
        let header = decode_header(header_prefix).map_err(|error| Trap::Decode {
            pc,
            error: error.into(),
        })?;
        self.checked_fetch_offset(pc, u64::from(header.length_bytes) - 1)?;
        let prefix_len = header_prefix.len();
        for (index, byte) in bytes
            .iter_mut()
            .enumerate()
            .take(usize::from(header.length_bytes))
            .skip(prefix_len)
        {
            let logical = self.checked_fetch_offset(pc, index as u64)?;
            let physical = self.translate_fetch(bus, logical, pc)?;
            *byte = bus
                .read_u8(physical)
                .map_err(|error| self.fetch_bus_trap(pc, logical, error))?;
        }
        decode(&bytes[..usize::from(header.length_bytes)])
            .map_err(|error| Trap::Decode { pc, error })
    }

    fn execute<B: Bus>(
        &mut self,
        bus: &mut B,
        pc: u64,
        instruction: &DecodedInstruction,
    ) -> Result<StepResult, Trap> {
        let next_pc = pc.wrapping_add(u64::from(instruction.length_bytes));
        self.validate_dynamic_operand_relations(pc, instruction)?;
        match instruction.opcode {
            Opcode::Illegal => Err(Trap::IllegalInstruction {
                pc,
                cause: IllegalInstructionCause::ExplicitIllegal,
            }),
            Opcode::Nop
            | Opcode::Yield
            | Opcode::Wait
            | Opcode::Rfence
            | Opcode::Wfence
            | Opcode::Afence
            | Opcode::Trace => {
                self.state.pc = next_pc;
                Ok(StepResult::Running)
            }
            Opcode::Halt => {
                self.state.pc = next_pc;
                self.halted = true;
                Ok(StepResult::Halted)
            }
            Opcode::Bkpt => {
                self.state.pc = next_pc;
                Ok(StepResult::Breakpoint)
            }
            Opcode::Reset => {
                let bootpc = self.state.bootpc;
                let bootcfg = self.state.bootcfg;
                self.reset(bootpc);
                self.state.bootpc = bootpc;
                self.state.bootcfg = bootcfg;
                Ok(StepResult::Running)
            }
            Opcode::Mov => self.execute_move(bus, pc, next_pc, instruction),
            Opcode::Movcu | Opcode::Movuc | Opcode::Movuu | Opcode::Movnt => {
                self.execute_move(bus, pc, next_pc, instruction)
            }
            Opcode::Movcc => {
                if self.state.flags.condition(field(instruction, 'c') as u8) {
                    self.execute_move(bus, pc, next_pc, instruction)
                } else {
                    self.state.pc = next_pc;
                    Ok(StepResult::Running)
                }
            }
            Opcode::Clr => self.execute_clear(bus, pc, next_pc, instruction),
            Opcode::Set | Opcode::Setcc => self.execute_set(bus, pc, next_pc, instruction),
            Opcode::Add | Opcode::Sub | Opcode::And | Opcode::Or | Opcode::Xor => {
                self.execute_binary(bus, pc, next_pc, instruction, false)
            }
            Opcode::Adc | Opcode::Sbb => self.execute_carry_binary(bus, pc, next_pc, instruction),
            Opcode::Cmp | Opcode::Test => self.execute_binary(bus, pc, next_pc, instruction, true),
            Opcode::Inc
            | Opcode::Dec
            | Opcode::Neg
            | Opcode::Abs
            | Opcode::Not
            | Opcode::Incf
            | Opcode::Decf => self.execute_unary(bus, pc, next_pc, instruction),
            Opcode::Xchg => self.execute_exchange(bus, pc, next_pc, instruction),
            Opcode::Shl | Opcode::Shr | Opcode::Sar | Opcode::Rol | Opcode::Ror => {
                self.execute_shift(bus, pc, next_pc, instruction)
            }
            Opcode::Btest | Opcode::Bset | Opcode::Bclr | Opcode::Bchg => {
                self.execute_bit(bus, pc, next_pc, instruction)
            }
            Opcode::Clz | Opcode::Cls | Opcode::Ctz | Opcode::Cts | Opcode::Popcnt => {
                self.execute_count(bus, pc, next_pc, instruction)
            }
            Opcode::Revbyte => self.execute_revbyte(bus, pc, next_pc, instruction),
            Opcode::Parity => self.execute_parity(bus, pc, next_pc, instruction),
            Opcode::Mul
            | Opcode::Mulhu
            | Opcode::Mulhs
            | Opcode::Mulhsu
            | Opcode::Clmul
            | Opcode::Clmulh
            | Opcode::Mins
            | Opcode::Minu
            | Opcode::Maxs
            | Opcode::Maxu => self.execute_math(bus, pc, next_pc, instruction),
            Opcode::Divs | Opcode::Divu | Opcode::Mods | Opcode::Modu => {
                self.execute_divide(bus, pc, next_pc, instruction)
            }
            Opcode::Extzl
            | Opcode::Extzq
            | Opcode::Extzw
            | Opcode::Extsl
            | Opcode::Extsq
            | Opcode::Extsw => self.execute_extend(bus, pc, next_pc, instruction),
            Opcode::Jmp | Opcode::Jcc => self.execute_jump(bus, pc, next_pc, instruction),
            Opcode::Push | Opcode::Pushp => self.execute_push(bus, pc, next_pc, instruction),
            Opcode::Pop | Opcode::Popp => self.execute_pop(bus, pc, next_pc, instruction),
            Opcode::Call | Opcode::Callcc => self.execute_call(bus, pc, next_pc, instruction),
            Opcode::Ret => self.execute_return(bus, pc),
            Opcode::Repcc => self.enter_scalar_repeat(bus, pc, next_pc, instruction),
            Opcode::Repg => self.enter_group_repeat(bus, pc, next_pc, instruction),
            Opcode::Lea | Opcode::Seglea => self.execute_lea(pc, next_pc, instruction),
            Opcode::Setf
            | Opcode::Clrf
            | Opcode::Rdflags
            | Opcode::Wrflags
            | Opcode::Rdstatus
            | Opcode::Wrstatus
            | Opcode::Rdfflags
            | Opcode::Wrfflags
            | Opcode::Rdfstatus
            | Opcode::Wrfstatus => self.execute_state_register(next_pc, instruction),
            Opcode::Rdseg | Opcode::Wrseg => self.execute_segment_register(next_pc, instruction),
            Opcode::Rdcr | Opcode::Wrcr | Opcode::Rdpmc | Opcode::Cpuid => {
                self.execute_control_register(bus, pc, next_pc, instruction)
            }
            Opcode::Prefetch | Opcode::Prefetchnt => {
                if let Some(ea) = first_ea(instruction) {
                    self.touch_prefetch_address(bus, pc, instruction, ea)?;
                }
                self.state.pc = next_pc;
                Ok(StepResult::Running)
            }
            Opcode::Invpage => {
                if let Some(ea) = first_ea(instruction) {
                    let (segment, offset) = self.address_operand_location(pc, instruction, ea)?;
                    self.effective_linear_address(segment, offset, pc)?;
                }
                self.state.pc = next_pc;
                Ok(StepResult::Running)
            }
            Opcode::Flshdcache
            | Opcode::Invdcache
            | Opcode::Invicache
            | Opcode::Invtlb
            | Opcode::Invasid
            | Opcode::Synccache
            | Opcode::Wrbkdcache => {
                if let Some(ea) = first_ea(instruction) {
                    self.touch_address_operand(bus, pc, instruction, ea)?;
                }
                self.state.pc = next_pc;
                Ok(StepResult::Running)
            }
            Opcode::Cmpjcc | Opcode::Testjcc => {
                self.execute_compare_jump(bus, pc, next_pc, instruction)
            }
            Opcode::Djcc | Opcode::Ijcc => self.execute_count_jump(bus, pc, next_pc, instruction),
            Opcode::Fetchadd
            | Opcode::Fetchand
            | Opcode::Fetchor
            | Opcode::Fetchsub
            | Opcode::Fetchxor
            | Opcode::Cmpxchg => self.execute_atomic(bus, pc, next_pc, instruction),
            Opcode::Bndsii
            | Opcode::Bndsix
            | Opcode::Bndsxi
            | Opcode::Bndsxx
            | Opcode::Bnduii
            | Opcode::Bnduix
            | Opcode::Bnduxi
            | Opcode::Bnduxx => self.execute_bounds(bus, pc, next_pc, instruction),
            Opcode::Divmods | Opcode::Divmodu => self.execute_divmod(bus, pc, next_pc, instruction),
            Opcode::Swpt | Opcode::Swpta | Opcode::Ptquery | Opcode::Vtop => {
                self.execute_translation_control(bus, pc, next_pc, instruction)
            }
            Opcode::Lcall | Opcode::Ljmp | Opcode::Lret => {
                self.execute_long_control(bus, pc, next_pc, instruction)
            }
            Opcode::Extract => self.execute_extract(bus, pc, next_pc, instruction),
            Opcode::Save | Opcode::Restore => {
                self.execute_save_restore(bus, pc, next_pc, instruction)
            }
            Opcode::Syscall => self.execute_syscall(bus, pc, next_pc),
            Opcode::Sysret => self.execute_system_return(bus, pc),
            Opcode::Eret => self.execute_event_return(bus, pc),
            Opcode::Fabs
            | Opcode::Facosa
            | Opcode::Fadd
            | Opcode::Fasina
            | Opcode::Fatana
            | Opcode::Fatanha
            | Opcode::Fbndii
            | Opcode::Fbndix
            | Opcode::Fbndxi
            | Opcode::Fbndxx
            | Opcode::Fceil
            | Opcode::Fclass
            | Opcode::Fclr
            | Opcode::Fcmp
            | Opcode::Fcopysign
            | Opcode::Fcosa
            | Opcode::Fcosha
            | Opcode::Fcvt
            | Opcode::Fcvtu
            | Opcode::Fdiv
            | Opcode::Fetoxa
            | Opcode::Fetoxm1a
            | Opcode::Ffloor
            | Opcode::Fgetexp
            | Opcode::Fgetman
            | Opcode::Fint
            | Opcode::Fintrz
            | Opcode::Flog10a
            | Opcode::Flog2a
            | Opcode::Flogna
            | Opcode::Flognp1a
            | Opcode::Fmax
            | Opcode::Fmin
            | Opcode::Fmod
            | Opcode::Fmov
            | Opcode::Fmovcc
            | Opcode::Fmovcr
            | Opcode::Fmadd
            | Opcode::Fmsub
            | Opcode::Fmul
            | Opcode::Fneg
            | Opcode::Fnmadd
            | Opcode::Fnmsub
            | Opcode::Fpopp
            | Opcode::Fpushp
            | Opcode::Frem
            | Opcode::Fround
            | Opcode::Fscale
            | Opcode::Fsina
            | Opcode::Fsincosa
            | Opcode::Fsinha
            | Opcode::Fsqrt
            | Opcode::Fsub
            | Opcode::Ftana
            | Opcode::Ftanha
            | Opcode::Ftentoxa
            | Opcode::Ftest
            | Opcode::Ftrunc
            | Opcode::Ftwotoxa
            | Opcode::Fxchg => self.execute_fpu(bus, pc, next_pc, instruction),
        }
    }

    fn validate_dynamic_operand_relations(
        &self,
        pc: u64,
        instruction: &DecodedInstruction,
    ) -> Result<(), Trap> {
        let form = GENERATED_FORMS
            .iter()
            .find(|form| form.form == instruction.form)
            .expect("decoded form must have generated metadata");
        for relation in form.destination_overlap {
            if relation.rule != DestinationOverlapRule::IllegalInstruction {
                continue;
            }
            let [left, right] = relation.operand_fields;
            if field(instruction, left) == field(instruction, right) {
                return Err(Trap::IllegalInstruction {
                    pc,
                    cause: IllegalInstructionCause::InvalidOperandRelation,
                });
            }
        }
        Ok(())
    }

    fn enter_scalar_repeat<B: Bus>(
        &mut self,
        bus: &mut B,
        _pc: u64,
        body_pc: u64,
        instruction: &DecodedInstruction,
    ) -> Result<StepResult, Trap> {
        let body = self.fetch_decode(bus, body_pc)?;
        let condition = field(instruction, 'c') as u8;
        let eligible = if condition == 0 {
            body.attributes.repeat_rep
        } else {
            body.attributes.repeat_repcc
        };
        if !eligible || is_repeat_forbidden(&body) {
            return Err(Trap::IllegalInstruction {
                pc: body_pc,
                cause: IllegalInstructionCause::ReservedEncoding,
            });
        }
        let counter = field(instruction, 'r') as u8;
        let after_pc = body_pc.wrapping_add(u64::from(body.length_bytes));
        let remaining = self.state.r[counter as usize];
        if remaining == 0 {
            self.state.pc = after_pc;
        } else {
            self.state.pc = body_pc;
            self.repeat = Some(RepeatState {
                counter,
                remaining,
                condition,
                bodies: vec![(body_pc, body)],
                index: 0,
                after_pc,
                grouped: false,
            });
        }
        Ok(StepResult::Running)
    }

    fn enter_group_repeat<B: Bus>(
        &mut self,
        bus: &mut B,
        pc: u64,
        body_pc: u64,
        instruction: &DecodedInstruction,
    ) -> Result<StepResult, Trap> {
        let body_bytes = read_unsigned(trailing_bytes(instruction), 2);
        if body_bytes == 0 {
            return Err(illegal_instruction(pc));
        }
        let after_pc = body_pc
            .checked_add(body_bytes)
            .ok_or(illegal_instruction(pc))?;
        let mut cursor = body_pc;
        let mut bodies = Vec::new();
        while cursor < after_pc {
            let body = self.fetch_decode(bus, cursor)?;
            if !body.attributes.repeat_repg || is_repeat_forbidden(&body) {
                return Err(Trap::IllegalInstruction {
                    pc: cursor,
                    cause: IllegalInstructionCause::ReservedEncoding,
                });
            }
            let next = cursor.wrapping_add(u64::from(body.length_bytes));
            if next > after_pc {
                return Err(illegal_instruction(pc));
            }
            bodies.push((cursor, body));
            cursor = next;
        }
        if cursor != after_pc || bodies.is_empty() {
            return Err(illegal_instruction(pc));
        }
        let counter = field(instruction, 'r') as u8;
        self.state.pc = body_pc;
        self.repeat = Some(RepeatState {
            counter,
            remaining: 0,
            condition: 0,
            bodies,
            index: 0,
            after_pc,
            grouped: true,
        });
        Ok(StepResult::Running)
    }

    fn step_repeat<B: Bus>(&mut self, bus: &mut B, pc: u64) -> Result<StepResult, Trap> {
        let active = self.repeat.clone().expect("checked repeat state");
        let (body_pc, body) = active.bodies[active.index].clone();
        if pc != body_pc {
            return Err(illegal_instruction(pc));
        }
        self.repeat_ea_result.set(None);
        let source_observation = match body.attributes.repeat_observed {
            Some(RepeatObservation::Source { operand }) => {
                self.repeat_observed_operand(&body, operand)
            }
            _ => None,
        };
        let result = self.execute(bus, body_pc, &body)?;
        if result != StepResult::Running {
            return Ok(result);
        }

        if active.grouped && active.index + 1 < active.bodies.len() {
            let mut next = active;
            next.index += 1;
            self.state.pc = next.bodies[next.index].0;
            self.repeat = Some(next);
            return Ok(StepResult::Running);
        }

        if active.grouped {
            let loop_control = self.state.r[active.counter as usize];
            let repeat_group = if loop_control == 0 {
                false
            } else {
                let decremented = loop_control - 1;
                self.state.r[active.counter as usize] = decremented;
                decremented != 0
            };
            if repeat_group {
                let mut next = active;
                next.index = 0;
                self.state.pc = next.bodies[0].0;
                self.repeat = Some(next);
            } else {
                self.state.pc = active.after_pc;
                self.repeat = None;
            }
            return Ok(StepResult::Running);
        }

        let observed_flags = if active.condition == 0 {
            None
        } else {
            Some(match body.attributes.repeat_observed {
                Some(RepeatObservation::Flags) => self.state.flags,
                Some(RepeatObservation::Result { operand }) => logical_repeat_flags(
                    self.repeat_observed_operand(&body, operand)
                        .ok_or(illegal_instruction(body_pc))?,
                    instruction_size(&body),
                ),
                Some(RepeatObservation::Source { .. }) => logical_repeat_flags(
                    source_observation.ok_or(illegal_instruction(body_pc))?,
                    instruction_size(&body),
                ),
                None => return Err(illegal_instruction(body_pc)),
            })
        };
        let remaining = active.remaining - 1;
        self.state.r[active.counter as usize] = remaining;
        let condition_holds = observed_flags.is_none_or(|flags| flags.condition(active.condition));
        if remaining != 0 && condition_holds {
            let mut next = active;
            next.remaining = remaining;
            next.index = 0;
            self.state.pc = next.bodies[0].0;
            self.repeat = Some(next);
        } else {
            self.state.pc = active.after_pc;
            self.repeat = None;
        }
        Ok(StepResult::Running)
    }

    fn repeat_observed_operand(
        &self,
        instruction: &DecodedInstruction,
        operand: RepeatObservedOperand,
    ) -> Option<u64> {
        match operand.location {
            RepeatOperandLocation::Rn => {
                let symbol = operand.field?;
                Some(self.state.r[field(instruction, symbol) as usize])
            }
            RepeatOperandLocation::EffectiveAddress => self.repeat_ea_result.get(),
            RepeatOperandLocation::StackPointer => Some(self.state.sp),
            RepeatOperandLocation::SegmentRegister => {
                let symbol = operand.field?;
                let selector = segment_selector(field(instruction, symbol) as u8);
                Some(self.state.segments.get(selector).raw())
            }
            RepeatOperandLocation::CodeSegment => Some(self.state.segments.cs().raw()),
        }
    }

    fn capture_repeat_ea_result(
        &self,
        instruction: &DecodedInstruction,
        symbol: Option<char>,
        ea: CompactEa,
        value: u64,
    ) {
        let Some(RepeatObservation::Result { operand }) = instruction.attributes.repeat_observed
        else {
            return;
        };
        if operand.location != RepeatOperandLocation::EffectiveAddress {
            return;
        }
        let matches = match (operand.field, symbol) {
            (Some(expected), Some(actual)) => expected == actual,
            (Some(expected), None) => ea_field(instruction, expected) == Some(ea),
            (None, _) => true,
        };
        if matches {
            self.repeat_ea_result.set(Some(value));
        }
    }

    fn execute_carry_binary<B: Bus>(
        &mut self,
        bus: &mut B,
        pc: u64,
        next_pc: u64,
        instruction: &DecodedInstruction,
    ) -> Result<StepResult, Trap> {
        let size = instruction_size(instruction);
        let (src, dst, destination) = self.binary_operands(bus, pc, instruction, size)?;
        let carry = u64::from(self.state.flags.contains(Flags::C));
        let mask = size_mask(size);
        let lhs = dst & mask;
        let rhs = src & mask;
        let (result, carry_or_borrow, signed_result) = if instruction.opcode == Opcode::Adc {
            let complete = u128::from(lhs) + u128::from(rhs) + u128::from(carry);
            (
                complete as u64 & mask,
                complete > u128::from(mask),
                i128::from(sign_extend(lhs, size))
                    + i128::from(sign_extend(rhs, size))
                    + i128::from(carry),
            )
        } else {
            (
                lhs.wrapping_sub(rhs).wrapping_sub(carry) & mask,
                u128::from(lhs) < u128::from(rhs) + u128::from(carry),
                i128::from(sign_extend(lhs, size))
                    - i128::from(sign_extend(rhs, size))
                    - i128::from(carry),
            )
        };
        self.write_destination(bus, pc, instruction, destination, size, result)?;
        self.set_logic_flags(size, result);
        self.state.flags.set(Flags::C, carry_or_borrow);
        let signed_limit = 1_i128 << (size.bytes() * 8 - 1);
        self.state.flags.set(
            Flags::V,
            signed_result < -signed_limit || signed_result >= signed_limit,
        );
        self.state.pc = next_pc;
        Ok(StepResult::Running)
    }

    fn execute_shift<B: Bus>(
        &mut self,
        bus: &mut B,
        pc: u64,
        next_pc: u64,
        instruction: &DecodedInstruction,
    ) -> Result<StepResult, Trap> {
        let size = instruction_size(instruction);
        let count = if instruction.allocation_id.contains("rn_s") {
            self.state.r[field(instruction, 's') as usize]
        } else {
            optional_field(instruction, 'i').unwrap_or(0)
        };
        let width = (size.bytes() * 8) as u32;
        let count = (count % u64::from(width)) as u32;
        let destination = if instruction.allocation_id.contains("rn_s_rn_d") {
            Destination::Register(field(instruction, 'd') as u8)
        } else {
            let ea = first_ea(instruction).ok_or(illegal_instruction(pc))?;
            Destination::Ea(self.resolve_ea(pc, instruction, ea, size)?)
        };
        let old = self.read_destination(bus, pc, destination, size)? & size_mask(size);
        let result = if count == 0 {
            old
        } else {
            (match instruction.opcode {
                Opcode::Shl => old.wrapping_shl(count),
                Opcode::Shr => old.wrapping_shr(count),
                Opcode::Sar => (sign_extend(old, size) >> count) as u64,
                Opcode::Rol => rotate_left_width(old, count, width),
                Opcode::Ror => rotate_right_width(old, count, width),
                _ => unreachable!(),
            }) & size_mask(size)
        };
        self.write_destination(bus, pc, instruction, destination, size, result)?;
        self.state.pc = next_pc;
        Ok(StepResult::Running)
    }

    fn execute_bit<B: Bus>(
        &mut self,
        bus: &mut B,
        pc: u64,
        next_pc: u64,
        instruction: &DecodedInstruction,
    ) -> Result<StepResult, Trap> {
        let size = instruction_size(instruction);
        let bit = if let Some(index) = optional_field(instruction, 'b') {
            self.state.r[index as usize]
        } else if let Some(index) = optional_field(instruction, 's') {
            self.state.r[index as usize]
        } else {
            optional_field(instruction, 'i').unwrap_or(0)
        } % (size.bytes() * 8) as u64;
        let destination = if instruction.allocation_id.contains("rn_d") {
            Destination::Register(field(instruction, 'd') as u8)
        } else {
            let ea = first_ea(instruction).ok_or(illegal_instruction(pc))?;
            Destination::Ea(self.resolve_ea(pc, instruction, ea, size)?)
        };
        let old = self.read_destination(bus, pc, destination, size)?;
        let mask = 1u64 << bit;
        self.state.flags.set(Flags::Z, old & mask == 0);
        let result = match instruction.opcode {
            Opcode::Bset => Some(old | mask),
            Opcode::Bclr => Some(old & !mask),
            Opcode::Bchg => Some(old ^ mask),
            Opcode::Btest => None,
            _ => unreachable!(),
        };
        if let Some(result) = result {
            self.write_destination(bus, pc, instruction, destination, size, result)?;
        }
        self.state.pc = next_pc;
        Ok(StepResult::Running)
    }

    fn execute_count<B: Bus>(
        &mut self,
        bus: &mut B,
        pc: u64,
        next_pc: u64,
        instruction: &DecodedInstruction,
    ) -> Result<StepResult, Trap> {
        let size = instruction_size(instruction);
        let source = if let Some(ea) = first_ea(instruction) {
            self.read_ea(bus, pc, instruction, ea, size)?
        } else {
            self.read_r(field(instruction, 's') as usize, size)
        };
        let bits = (size.bytes() * 8) as u32;
        let value = source & size_mask(size);
        let result = match instruction.opcode {
            Opcode::Clz => value.leading_zeros().saturating_sub(64 - bits),
            Opcode::Cls => (!value & size_mask(size))
                .leading_zeros()
                .saturating_sub(64 - bits),
            Opcode::Ctz => value.trailing_zeros().min(bits),
            Opcode::Cts => (!value & size_mask(size)).trailing_zeros().min(bits),
            Opcode::Popcnt => value.count_ones(),
            _ => unreachable!(),
        } as u64;
        let dst = optional_field(instruction, 'd').unwrap_or(0) as usize;
        self.write_r(dst, size, result);
        self.state.pc = next_pc;
        Ok(StepResult::Running)
    }

    fn execute_revbyte<B: Bus>(
        &mut self,
        bus: &mut B,
        pc: u64,
        next_pc: u64,
        instruction: &DecodedInstruction,
    ) -> Result<StepResult, Trap> {
        let size = instruction_size(instruction);
        let destination = if let Some(r) = optional_field(instruction, 'r') {
            Destination::Register(r as u8)
        } else {
            let ea = first_ea(instruction).ok_or(illegal_instruction(pc))?;
            Destination::Ea(self.resolve_ea(pc, instruction, ea, size)?)
        };
        let value = self.read_destination(bus, pc, destination, size)?;
        let result = match size {
            Size::Byte => value,
            Size::Word => (value as u16).swap_bytes() as u64,
            Size::Long => (value as u32).swap_bytes() as u64,
            Size::Quad => value.swap_bytes(),
        };
        self.write_destination(bus, pc, instruction, destination, size, result)?;
        self.state.pc = next_pc;
        Ok(StepResult::Running)
    }

    fn execute_parity<B: Bus>(
        &mut self,
        bus: &mut B,
        pc: u64,
        next_pc: u64,
        instruction: &DecodedInstruction,
    ) -> Result<StepResult, Trap> {
        let size = instruction_size(instruction);
        let value = if let Some(ea) = first_ea(instruction) {
            self.read_ea(bus, pc, instruction, ea, size)?
        } else {
            self.read_r(field(instruction, 's') as usize, size)
        };
        let result = u64::from((value & size_mask(size)).count_ones() & 1);
        self.write_r(field(instruction, 'd') as usize, size, result);
        self.state.pc = next_pc;
        Ok(StepResult::Running)
    }

    fn execute_math<B: Bus>(
        &mut self,
        bus: &mut B,
        pc: u64,
        next_pc: u64,
        instruction: &DecodedInstruction,
    ) -> Result<StepResult, Trap> {
        let size = instruction_size(instruction);
        let (src, dst, destination) = self.binary_operands(bus, pc, instruction, size)?;
        let width = size.bytes() * 8;
        let result = match instruction.opcode {
            Opcode::Mul => dst.wrapping_mul(src),
            Opcode::Mulhu => high_product_unsigned(dst, src, width),
            Opcode::Mulhs => high_product_signed(dst, src, width),
            Opcode::Mulhsu => high_product_signed_unsigned(dst, src, width),
            Opcode::Clmul => carryless_product(dst, src).0,
            Opcode::Clmulh => carryless_product_high(dst, src, width),
            Opcode::Minu => (dst & size_mask(size)).min(src & size_mask(size)),
            Opcode::Maxu => (dst & size_mask(size)).max(src & size_mask(size)),
            Opcode::Mins => (sign_extend(dst, size).min(sign_extend(src, size))) as u64,
            Opcode::Maxs => (sign_extend(dst, size).max(sign_extend(src, size))) as u64,
            _ => unreachable!(),
        } & size_mask(size);
        self.write_destination(bus, pc, instruction, destination, size, result)?;
        self.state.pc = next_pc;
        Ok(StepResult::Running)
    }

    fn execute_divide<B: Bus>(
        &mut self,
        bus: &mut B,
        pc: u64,
        next_pc: u64,
        instruction: &DecodedInstruction,
    ) -> Result<StepResult, Trap> {
        let size = instruction_size(instruction);
        let (src, dst, destination) = self.binary_operands(bus, pc, instruction, size)?;
        if src & size_mask(size) == 0 {
            return Err(Trap::DivideError {
                pc,
                cause: DivideErrorCause::ZeroDivisor,
            });
        }
        let signed = matches!(instruction.opcode, Opcode::Divs | Opcode::Mods);
        let modulo = matches!(instruction.opcode, Opcode::Mods | Opcode::Modu);
        let result = if signed {
            let lhs = sign_extend(dst, size);
            let rhs = sign_extend(src, size);
            if lhs == signed_min(size) && rhs == -1 {
                return Err(Trap::DivideError {
                    pc,
                    cause: DivideErrorCause::SignedOverflow,
                });
            }
            (if modulo { lhs % rhs } else { lhs / rhs }) as u64
        } else if modulo {
            (dst & size_mask(size)) % (src & size_mask(size))
        } else {
            (dst & size_mask(size)) / (src & size_mask(size))
        };
        self.write_destination(bus, pc, instruction, destination, size, result)?;
        self.state.pc = next_pc;
        Ok(StepResult::Running)
    }

    fn execute_extend<B: Bus>(
        &mut self,
        bus: &mut B,
        pc: u64,
        next_pc: u64,
        instruction: &DecodedInstruction,
    ) -> Result<StepResult, Trap> {
        let dst_size = match instruction.opcode {
            Opcode::Extzw | Opcode::Extsw => Size::Word,
            Opcode::Extzl | Opcode::Extsl => Size::Long,
            Opcode::Extzq | Opcode::Extsq => Size::Quad,
            _ => unreachable!(),
        };
        let src_size = instruction_size(instruction);
        let id = instruction.allocation_id;
        let src = if id.contains("rn_s_rn_d") || id.contains("rn_s_ea_e") {
            self.read_r(field(instruction, 's') as usize, src_size)
        } else if id.contains("ea_s_ea_d") {
            self.read_ea_field(bus, pc, instruction, 's', src_size)?
        } else if id.contains("ea_e_rn_d") {
            self.read_ea_field(bus, pc, instruction, 'e', src_size)?
        } else {
            return Err(illegal_instruction(pc));
        };
        let result = if matches!(
            instruction.opcode,
            Opcode::Extsw | Opcode::Extsl | Opcode::Extsq
        ) {
            sign_extend(src, src_size) as u64
        } else {
            src
        };
        if let Some(dst) = general_field(instruction, 'd') {
            self.write_r(dst, dst_size, result);
        } else if id.contains("ea_s_ea_d") {
            self.write_ea_field(bus, pc, instruction, 'd', dst_size, result)?;
        } else if id.contains("rn_s_ea_e") {
            self.write_ea_field(bus, pc, instruction, 'e', dst_size, result)?;
        } else {
            return Err(illegal_instruction(pc));
        }
        self.state.pc = next_pc;
        Ok(StepResult::Running)
    }

    fn execute_lea(
        &mut self,
        pc: u64,
        next_pc: u64,
        instruction: &DecodedInstruction,
    ) -> Result<StepResult, Trap> {
        let size = instruction_size(instruction);
        let ea = first_ea(instruction).ok_or(illegal_instruction(pc))?;
        let (segment, address) = match ea {
            CompactEa::Register(r) => (SegmentSelector::Ds, self.state.r[r as usize]),
            CompactEa::StackPointer => (SegmentSelector::Ss, self.state.sp),
            CompactEa::Immediate(width) => (
                SegmentSelector::Ds,
                read_signed(ea_payload(instruction, ea), width) as u64,
            ),
            _ => self.effective_location_with_payload(pc, ea, ea_payload(instruction, ea), size)?,
        };
        let dst = field(instruction, 'd') as usize;
        if instruction.opcode == Opcode::Seglea {
            let descriptor = self.state.segments.get(segment);
            let translated = if !descriptor.enabled() {
                Some(address)
            } else {
                let base = u128::from(descriptor.base());
                let span = (u128::from(descriptor.mantissa()) << descriptor.exponent()) * 4096;
                let candidate = u128::from(address);
                let in_bounds = if descriptor.bounds_only() {
                    base <= candidate && candidate < base + span
                } else {
                    candidate < span
                };
                in_bounds.then(|| {
                    if descriptor.bounds_only() {
                        address
                    } else {
                        descriptor.base().wrapping_add(address)
                    }
                })
            };
            self.state.flags.set(Flags::V, translated.is_none());
            if let Some(value) = translated {
                self.write_r(dst, size, value);
            }
        } else {
            self.write_r(dst, size, address);
        }
        self.state.pc = next_pc;
        Ok(StepResult::Running)
    }

    fn execute_state_register(
        &mut self,
        next_pc: u64,
        instruction: &DecodedInstruction,
    ) -> Result<StepResult, Trap> {
        let src = optional_field(instruction, 's')
            .or_else(|| optional_field(instruction, 'r'))
            .unwrap_or(0) as usize;
        let dst = optional_field(instruction, 'd')
            .or_else(|| optional_field(instruction, 'r'))
            .unwrap_or(0) as usize;
        match instruction.opcode {
            Opcode::Setf => {
                self.state
                    .flags
                    .insert(Flags::from_bits_truncate(field(instruction, 'm') as u16))
            }
            Opcode::Clrf => {
                self.state
                    .flags
                    .remove(Flags::from_bits_truncate(field(instruction, 'm') as u16))
            }
            Opcode::Rdflags => self.state.r[dst] = u64::from(self.state.flags.bits()),
            Opcode::Wrflags => {
                let value = self.state.r[src] as u16;
                if value & !Flags::all().bits() != 0 {
                    return Err(Trap::IllegalInstruction {
                        pc: next_pc.wrapping_sub(u64::from(instruction.length_bytes)),
                        cause: IllegalInstructionCause::ReservedEncoding,
                    });
                }
                self.state.flags = Flags::from_bits_retain(value)
            }
            Opcode::Rdstatus => self.state.r[dst] = u64::from(self.state.status.bits()),
            Opcode::Wrstatus => {
                let value = self.state.r[src] as u16;
                let immutable = Status::EA | Status::PM;
                if value & !Status::all().bits() != 0
                    || (value & immutable.bits()) != (self.state.status.bits() & immutable.bits())
                {
                    return Err(Trap::InvalidControlState {
                        pc: next_pc.wrapping_sub(u64::from(instruction.length_bytes)),
                        cause: InvalidControlCause::ReservedBits,
                    });
                }
                self.state.status = Status::from_bits_retain(value)
            }
            Opcode::Rdfflags => self.state.r[dst] = u64::from(self.state.fflags),
            Opcode::Wrfflags => {
                let value = self.state.r[src] as u16;
                crate::fpu::env::FpCauses::from_bits(value).map_err(|_| {
                    Trap::InvalidControlState {
                        pc: next_pc.wrapping_sub(u64::from(instruction.length_bytes)),
                        cause: InvalidControlCause::ReservedBits,
                    }
                })?;
                self.state.fflags = value;
            }
            Opcode::Rdfstatus => self.state.r[dst] = u64::from(self.state.fstatus),
            Opcode::Wrfstatus => {
                let value = self.state.r[src] as u16;
                crate::fpu::env::FpStatus::decode(value).map_err(|_| {
                    Trap::InvalidControlState {
                        pc: next_pc.wrapping_sub(u64::from(instruction.length_bytes)),
                        cause: InvalidControlCause::ReservedBits,
                    }
                })?;
                self.state.fstatus = value;
            }
            _ => unreachable!(),
        }
        self.state.pc = next_pc;
        Ok(StepResult::Running)
    }

    fn execute_segment_register(
        &mut self,
        next_pc: u64,
        instruction: &DecodedInstruction,
    ) -> Result<StepResult, Trap> {
        let selector = if instruction.allocation_id.contains("rdseg_cs") {
            SegmentSelector::Cs
        } else {
            segment_selector(field(instruction, 's') as u8)
        };
        let register = field(instruction, 'd') as usize;
        if instruction.opcode == Opcode::Rdseg {
            self.state.r[register] = self.state.segments.get(selector).raw();
        } else {
            let image = crate::SegmentRegister::from_raw(self.state.r[register]);
            if !image.valid() {
                return Err(Trap::InvalidControlState {
                    pc: next_pc.wrapping_sub(u64::from(instruction.length_bytes)),
                    cause: InvalidControlCause::InvalidImage,
                });
            }
            self.state.segments.set(selector, image);
        }
        self.state.pc = next_pc;
        Ok(StepResult::Running)
    }

    fn execute_control_register<B: Bus>(
        &mut self,
        bus: &mut B,
        pc: u64,
        next_pc: u64,
        instruction: &DecodedInstruction,
    ) -> Result<StepResult, Trap> {
        if instruction.opcode == Opcode::Cpuid {
            let register = field(instruction, 'r') as usize;
            self.state.r[register] = crate::cpuid::query(self.state.r[register]);
        } else if instruction.opcode == Opcode::Rdpmc {
            let counter_id = read_unsigned(trailing_bytes(instruction), 2);
            self.state.r[field(instruction, 'd') as usize] = match counter_id {
                1 => self.cycle_counter.get(),
                2 => self.instret_counter.get(),
                3 => self.ptwalk_counter.get(),
                _ => {
                    return Err(Trap::InvalidControlState {
                        pc,
                        cause: InvalidControlCause::InvalidSelector,
                    });
                }
            };
        } else {
            let selector = read_unsigned(trailing_bytes(instruction), 2);
            if instruction.opcode == Opcode::Rdcr {
                let value = match selector {
                    0 => self.state.ptcr.raw(),
                    1 => self.state.ascr.raw(),
                    2 => self.state.ecr.raw(),
                    0x0100 => self.state.spc,
                    0x0101 => self.state.scs.raw(),
                    0x0102 => self.state.sds.raw(),
                    0x0108 => self.state.urpc,
                    0x0109 => self.state.ursp,
                    0x010a => self.state.urcs.raw(),
                    0x010b => self.state.urds.raw(),
                    0x010c => self.state.urss.raw(),
                    0x010d => self.state.urctl,
                    0x0110 => self.state.epc,
                    0x0111 => self.state.ecs.raw(),
                    0x0112 => self.state.eds.raw(),
                    0x0200 => self.state.sss.raw(),
                    0x0201 => self.state.ssp,
                    0x0210 => self.state.iss.raw(),
                    0x0211 => self.state.isp,
                    0x0220 => self.state.fss.raw(),
                    0x0221 => self.state.fsp,
                    0x0230 => self.state.dss.raw(),
                    0x0231 => self.state.dsp,
                    0x1000 => self.state.bootpc,
                    0x1001 => self.state.bootcfg,
                    0x1100 => self.state.pmc,
                    _ => {
                        return Err(Trap::InvalidControlState {
                            pc,
                            cause: InvalidControlCause::InvalidSelector,
                        });
                    }
                };
                self.state.r[field(instruction, 'd') as usize] = value;
            } else {
                let value = self.state.r[field(instruction, 's') as usize];
                match selector {
                    0 => self.state.ptcr = Self::validate_ptcr_image(pc, value)?,
                    1 => self.state.ascr = Self::validate_ascr_image(pc, value)?,
                    2 => {
                        let candidate = self
                            .state
                            .ecr
                            .validate_software_image(value)
                            .map_err(|cause| Trap::InvalidControlState { pc, cause })?;
                        if candidate.valid() {
                            self.validate_event_configuration(bus, pc)?;
                        }
                        self.state.ecr = candidate;
                    }
                    0x0100 => {
                        if value & 0x0f != 0 || !self.state.scs.valid() {
                            return Err(Trap::InvalidControlState {
                                pc,
                                cause: InvalidControlCause::InvalidImage,
                            });
                        }
                        self.validate_return_target_in_cs(bus, pc, value, self.state.scs, true)?;
                        self.state.spc = value;
                    }
                    0x0101 => self.state.scs = Self::validate_segment_image(pc, value)?,
                    0x0102 => self.state.sds = Self::validate_segment_image(pc, value)?,
                    0x0108 => self.state.urpc = value,
                    0x0109 => self.state.ursp = value,
                    0x010a => self.state.urcs = crate::SegmentRegister::from_raw(value),
                    0x010b => self.state.urds = crate::SegmentRegister::from_raw(value),
                    0x010c => self.state.urss = crate::SegmentRegister::from_raw(value),
                    0x010d => {
                        let decoded = Self::decode_urctl(pc, value)?;
                        if value & URCTL_VALID != 0 {
                            self.validate_user_return_image(pc, value, decoded)?;
                        }
                        self.state.urctl = value;
                    }
                    0x0110 => {
                        if value & 0x0f != 0 {
                            return Err(Trap::InvalidControlState {
                                pc,
                                cause: InvalidControlCause::InvalidImage,
                            });
                        }
                        let mut candidate = self.clone();
                        candidate.state.epc = value;
                        let before_walks = candidate.ptwalk_counter.get();
                        let validation = candidate.validate_event_entry_target(bus, pc);
                        self.ptwalk_counter
                            .set(self.ptwalk_counter.get().wrapping_add(
                                candidate.ptwalk_counter.get().wrapping_sub(before_walks),
                            ));
                        validation.map_err(|_| Trap::InvalidControlState {
                            pc,
                            cause: InvalidControlCause::InvalidImage,
                        })?;
                        self.state.epc = value;
                    }
                    0x0111 => self.state.ecs = Self::validate_segment_image(pc, value)?,
                    0x0112 => self.state.eds = Self::validate_segment_image(pc, value)?,
                    0x0200 => self.state.sss = Self::validate_segment_image(pc, value)?,
                    0x0201 => {
                        Self::validate_stack_top(pc, value)?;
                        self.state.ssp = value;
                    }
                    0x0210 | 0x0220 | 0x0230 => {
                        let image = Self::validate_segment_image(pc, value)?;
                        match selector {
                            0x0210 => self.state.iss = image,
                            0x0220 => self.state.fss = image,
                            _ => self.state.dss = image,
                        }
                    }
                    0x0211 | 0x0221 | 0x0231 => {
                        Self::validate_stack_top(pc, value)?;
                        match selector {
                            0x0211 => self.state.isp = value,
                            0x0221 => self.state.fsp = value,
                            _ => self.state.dsp = value,
                        }
                    }
                    0x1000 => self.state.bootpc = value,
                    0x1001 => self.state.bootcfg = value,
                    0x1100 => {
                        if value & !1 != 0 {
                            return Err(Trap::InvalidControlState {
                                pc,
                                cause: InvalidControlCause::ReservedBits,
                            });
                        }
                        self.state.pmc = value;
                    }
                    _ => {
                        return Err(Trap::InvalidControlState {
                            pc,
                            cause: InvalidControlCause::InvalidSelector,
                        });
                    }
                }
            }
        }
        self.state.pc = next_pc;
        Ok(StepResult::Running)
    }

    fn execute_compare_jump<B: Bus>(
        &mut self,
        bus: &mut B,
        pc: u64,
        next_pc: u64,
        instruction: &DecodedInstruction,
    ) -> Result<StepResult, Trap> {
        let size = instruction_size(instruction);
        let src = self.read_r(field(instruction, 's') as usize, size);
        let dst = self.read_r(field(instruction, 'd') as usize, size);
        let result = if instruction.opcode == Opcode::Cmpjcc {
            dst.wrapping_sub(src) & size_mask(size)
        } else {
            dst & src
        };
        let flags = if instruction.opcode == Opcode::Cmpjcc {
            sub_flags(size, dst, src, result)
        } else {
            logic_flags(size, result)
        };
        let condition = field(instruction, 'c') as u8;
        if flags.condition(condition) {
            let target = next_pc.wrapping_add(signed_immediate(instruction) as u64);
            self.validate_control_target(bus, pc, target)?;
            self.state.pc = target;
        } else {
            self.state.pc = next_pc;
        }
        Ok(StepResult::Running)
    }

    fn execute_count_jump<B: Bus>(
        &mut self,
        bus: &mut B,
        pc: u64,
        next_pc: u64,
        instruction: &DecodedInstruction,
    ) -> Result<StepResult, Trap> {
        let condition = field(instruction, 'c') as u8;
        if instruction.opcode == Opcode::Djcc {
            let register = field(instruction, 'r') as usize;
            let value = self.state.r[register].wrapping_sub(1);
            let take = value != 0 && self.state.flags.condition(condition);
            let target = take
                .then(|| self.count_jump_target(bus, pc, instruction))
                .transpose()?;
            self.state.r[register] = value;
            self.state.pc = target.unwrap_or(next_pc);
        } else {
            let index = field(instruction, 'i') as usize;
            let bound = field(instruction, 'b') as usize;
            let value = self.state.r[index].wrapping_add(1);
            let take = value != self.state.r[bound] && self.state.flags.condition(condition);
            let target = take
                .then(|| self.count_jump_target(bus, pc, instruction))
                .transpose()?;
            self.state.r[index] = value;
            self.state.pc = target.unwrap_or(next_pc);
        }
        Ok(StepResult::Running)
    }

    fn count_jump_target<B: Bus>(
        &mut self,
        bus: &mut B,
        pc: u64,
        instruction: &DecodedInstruction,
    ) -> Result<u64, Trap> {
        let ea = first_ea(instruction).ok_or(illegal_instruction(pc))?;
        let target = self.read_ea(bus, pc, instruction, ea, Size::Quad)?;
        self.validate_control_target(bus, pc, target)?;
        Ok(target)
    }

    fn execute_atomic<B: Bus>(
        &mut self,
        bus: &mut B,
        pc: u64,
        next_pc: u64,
        instruction: &DecodedInstruction,
    ) -> Result<StepResult, Trap> {
        if optional_field(instruction, 'o').is_some_and(|order| order > 4) {
            return Err(illegal_instruction(pc));
        }
        let size = instruction_size(instruction);
        enum RegisterOperands {
            CompareExchange {
                expected: usize,
                expected_value: u64,
                desired_value: u64,
            },
            Fetch {
                source: usize,
                source_value: u64,
            },
        }
        let operands = if instruction.opcode == Opcode::Cmpxchg {
            let expected = field(instruction, 'x') as usize;
            let expected_value = self.read_r(expected, size);
            let desired = field(instruction, 'd') as usize;
            let desired_value = self.read_r(desired, size);
            RegisterOperands::CompareExchange {
                expected,
                expected_value,
                desired_value,
            }
        } else {
            let source = field(instruction, 's') as usize;
            RegisterOperands::Fetch {
                source,
                source_value: self.read_r(source, size),
            }
        };
        let ea = first_ea(instruction).ok_or(illegal_instruction(pc))?;
        let payload = ea_payload(instruction, ea);
        let (segment, offset) = self.effective_location_with_payload(pc, ea, payload, size)?;
        let linear = self.effective_linear_address(segment, offset, pc)?;
        let translation = crate::MemoryTranslation {
            segments: self.state.segments,
            ptcr: self.state.ptcr,
            ascr: self.state.ascr,
        };
        self.increment_page_walk(translation.ptcr);
        let walk = translation
            .page_address(
                bus,
                linear,
                AccessDomain::Current,
                AccessKind::Write,
                self.state.status.contains(Status::PM),
                false,
            )
            .map_err(|error| {
                atomic_walk_trap(pc, error, offset, segment, size, self.state.ascr.asid())
            })?;
        let address = match walk.target {
            crate::TranslatedTarget::Byte(address) => address,
            crate::TranslatedTarget::Slot(_) => {
                return Err(atomic_page_fault(
                    pc,
                    offset,
                    Some(linear),
                    crate::PageFaultReason::AddressType,
                    size,
                    segment,
                    self.state.ascr.asid(),
                ));
            }
        };
        if linear % size.bytes() as u64 != 0 {
            return Err(atomic_page_fault(
                pc,
                offset,
                Some(linear),
                crate::PageFaultReason::AtomicAlignment,
                size,
                segment,
                self.state.ascr.asid(),
            ));
        }
        let old = read_bus(bus, address, size).map_err(|error| Trap::Bus { pc, error })?;
        let value_to_store = match operands {
            RegisterOperands::CompareExchange {
                expected,
                expected_value,
                desired_value,
            } => {
                let succeeded = old == expected_value;
                self.state.flags = if succeeded { Flags::Z } else { Flags::empty() };
                self.write_r(expected, size, old);
                succeeded.then_some(desired_value)
            }
            RegisterOperands::Fetch {
                source,
                source_value,
            } => {
                let result = match instruction.opcode {
                    Opcode::Fetchadd => old.wrapping_add(source_value),
                    Opcode::Fetchsub => old.wrapping_sub(source_value),
                    Opcode::Fetchand => old & source_value,
                    Opcode::Fetchor => old | source_value,
                    Opcode::Fetchxor => old ^ source_value,
                    _ => unreachable!(),
                } & size_mask(size);
                self.write_r(source, size, old);
                Some(result)
            }
        };
        if let Some(value) = value_to_store {
            // D is exact: validate the write first, but update A/D only once the
            // atomic operation is known to commit a memory update.
            self.increment_page_walk(translation.ptcr);
            let commit_walk = translation
                .page_address(
                    bus,
                    linear,
                    AccessDomain::Current,
                    AccessKind::Write,
                    self.state.status.contains(Status::PM),
                    true,
                )
                .map_err(|error| {
                    atomic_walk_trap(pc, error, offset, segment, size, self.state.ascr.asid())
                })?;
            let commit_address = match commit_walk.target {
                crate::TranslatedTarget::Byte(address) => address,
                crate::TranslatedTarget::Slot(_) => {
                    return Err(atomic_page_fault(
                        pc,
                        offset,
                        Some(linear),
                        crate::PageFaultReason::AddressType,
                        size,
                        segment,
                        self.state.ascr.asid(),
                    ));
                }
            };
            if commit_address != address {
                return Err(atomic_page_fault(
                    pc,
                    offset,
                    Some(linear),
                    crate::PageFaultReason::InvalidEntry,
                    size,
                    segment,
                    self.state.ascr.asid(),
                ));
            }
            write_bus(bus, address, size, value).map_err(|error| Trap::Bus { pc, error })?;
        }
        self.state.pc = next_pc;
        Ok(StepResult::Running)
    }

    fn execute_bounds<B: Bus>(
        &mut self,
        bus: &mut B,
        pc: u64,
        next_pc: u64,
        instruction: &DecodedInstruction,
    ) -> Result<StepResult, Trap> {
        let size = instruction_size(instruction);
        let low = self.read_r(field(instruction, 'l') as usize, size);
        let value = self.read_ea(
            bus,
            pc,
            instruction,
            first_ea(instruction).ok_or(illegal_instruction(pc))?,
            size,
        )?;
        let high = self.read_r(field(instruction, 'h') as usize, size);
        let inclusive_low = matches!(
            instruction.opcode,
            Opcode::Bndsii | Opcode::Bndsix | Opcode::Bnduii | Opcode::Bnduix
        );
        let inclusive_high = matches!(
            instruction.opcode,
            Opcode::Bndsii | Opcode::Bndsxi | Opcode::Bnduii | Opcode::Bnduxi
        );
        let signed = matches!(
            instruction.opcode,
            Opcode::Bndsii | Opcode::Bndsix | Opcode::Bndsxi | Opcode::Bndsxx
        );
        let outside = if signed {
            let (l, v, h) = (
                sign_extend(low, size),
                sign_extend(value, size),
                sign_extend(high, size),
            );
            (if inclusive_low { v < l } else { v <= l })
                || (if inclusive_high { v > h } else { v >= h })
        } else {
            (if inclusive_low {
                value < low
            } else {
                value <= low
            }) || (if inclusive_high {
                value > high
            } else {
                value >= high
            })
        };
        self.state.flags.set(Flags::V, outside);
        self.state.pc = next_pc;
        Ok(StepResult::Running)
    }

    fn execute_divmod<B: Bus>(
        &mut self,
        bus: &mut B,
        pc: u64,
        next_pc: u64,
        instruction: &DecodedInstruction,
    ) -> Result<StepResult, Trap> {
        let size = instruction_size(instruction);
        let divisor = self.read_ea(
            bus,
            pc,
            instruction,
            first_ea(instruction).ok_or(illegal_instruction(pc))?,
            size,
        )?;
        if divisor == 0 {
            return Err(Trap::DivideError {
                pc,
                cause: DivideErrorCause::ZeroDivisor,
            });
        }
        let q = field(instruction, 'q') as usize;
        let r = field(instruction, 'r') as usize;
        let dividend = self.read_r(q, size);
        let (quotient, remainder) = if instruction.opcode == Opcode::Divmods {
            let a = sign_extend(dividend, size);
            let b = sign_extend(divisor, size);
            if a == signed_min(size) && b == -1 {
                return Err(Trap::DivideError {
                    pc,
                    cause: DivideErrorCause::SignedOverflow,
                });
            }
            ((a / b) as u64, (a % b) as u64)
        } else {
            (dividend / divisor, dividend % divisor)
        };
        self.write_r(q, size, quotient);
        self.write_r(r, size, remainder);
        self.state.pc = next_pc;
        Ok(StepResult::Running)
    }

    fn execute_translation_control<B: Bus>(
        &mut self,
        bus: &mut B,
        pc: u64,
        next_pc: u64,
        instruction: &DecodedInstruction,
    ) -> Result<StepResult, Trap> {
        match instruction.opcode {
            Opcode::Swpt => {
                let ptcr =
                    Self::validate_ptcr_image(pc, self.state.r[field(instruction, 'p') as usize])?;
                self.state.ptcr = ptcr;
                self.state.ascr = crate::AddressSpaceControl::from_raw(0);
            }
            Opcode::Swpta => {
                let ptcr =
                    Self::validate_ptcr_image(pc, self.state.r[field(instruction, 'p') as usize])?;
                let asid = self.state.r[field(instruction, 'a') as usize] & 0xffff;
                self.state.ptcr = ptcr;
                self.state.ascr = crate::AddressSpaceControl::from_raw((asid << 16) | 1);
            }
            Opcode::Vtop => {
                let v = self.state.r[field(instruction, 'v') as usize];
                let translation = crate::MemoryTranslation {
                    segments: self.state.segments,
                    ptcr: self.state.ptcr,
                    ascr: self.state.ascr,
                };
                if translation.translation_query_starts_walk(v) {
                    self.increment_page_walk(translation.ptcr);
                }
                let result =
                    translation
                        .query_translation(bus, v)
                        .map_err(|error| match error {
                            crate::translation::PageWalkError::Translation(fault) => {
                                translation_trap_with_context(
                                    pc,
                                    fault,
                                    v,
                                    AccessKind::Read,
                                    AccessDomain::Current,
                                    None,
                                    self.state.ascr.asid(),
                                )
                            }
                            crate::translation::PageWalkError::Bus { error, level } => self
                                .bus_access_trap(
                                    pc,
                                    error,
                                    v,
                                    Some(v),
                                    AccessKind::Read,
                                    AccessDomain::Current,
                                    None,
                                    None,
                                    Some(0),
                                    false,
                                    level,
                                ),
                        })?;
                self.write_page_query_result(field(instruction, 'p') as usize, result);
            }
            Opcode::Ptquery => {
                let ea = first_ea(instruction).ok_or(illegal_instruction(pc))?;
                let translation = crate::MemoryTranslation {
                    segments: self.state.segments,
                    ptcr: self.state.ptcr,
                    ascr: self.state.ascr,
                };
                let (query_ea, query_segment, linear) = match ea {
                    CompactEa::Register(register) => {
                        let address = self.state.r[register as usize];
                        (address, None, address)
                    }
                    CompactEa::StackPointer => (self.state.sp, None, self.state.sp),
                    CompactEa::Immediate(width) => {
                        let address = read_signed(ea_payload(instruction, ea), width) as u64;
                        (address, None, address)
                    }
                    _ => {
                        let payload = ea_payload(instruction, ea);
                        let (segment, offset) =
                            self.effective_location_with_payload(pc, ea, payload, Size::Quad)?;
                        let linear = translation
                            .segment_linear_address(segment, offset)
                            .map_err(|fault| translation_trap(pc, fault))?;
                        (offset, Some(segment), linear)
                    }
                };
                let level = field(instruction, 'i') as u8;
                if translation.page_query_starts_walk(linear, level) {
                    self.increment_page_walk(translation.ptcr);
                }
                let result = translation
                    .query_page_entry(bus, linear, level)
                    .map_err(|error| match error {
                        crate::translation::PageWalkError::Translation(fault) => {
                            translation_trap_with_context(
                                pc,
                                fault,
                                query_ea,
                                AccessKind::Read,
                                AccessDomain::Current,
                                query_segment,
                                self.state.ascr.asid(),
                            )
                        }
                        crate::translation::PageWalkError::Bus {
                            error,
                            level: walk_level,
                        } => self.bus_access_trap(
                            pc,
                            error,
                            query_ea,
                            Some(linear),
                            AccessKind::Read,
                            AccessDomain::Current,
                            query_segment,
                            None,
                            Some(1),
                            false,
                            walk_level,
                        ),
                    })?;
                self.write_page_query_result(field(instruction, 'd') as usize, result);
            }
            _ => unreachable!(),
        };
        self.state.pc = next_pc;
        Ok(StepResult::Running)
    }

    fn write_page_query_result(&mut self, register: usize, result: crate::PageQueryResult) {
        self.state.r[register] = result.value;
        self.state.flags.set(Flags::Z, result.valid);
        self.state.flags.set(Flags::N, result.valid && result.user);
        self.state
            .flags
            .set(Flags::C, result.valid && result.writable);
        self.state
            .flags
            .set(Flags::V, result.valid && result.executable);
    }

    fn execute_syscall<B: Bus>(
        &mut self,
        bus: &mut B,
        pc: u64,
        next_pc: u64,
    ) -> Result<StepResult, Trap> {
        if self.state.status.intersects(Status::PM | Status::EA)
            || self.state.urctl & URCTL_VALID != 0
        {
            return Err(Trap::InvalidControlState {
                pc,
                cause: InvalidControlCause::InvalidTransition,
            });
        }
        if !self.state.scs.valid() || !self.state.sds.valid() || !self.state.sss.valid() {
            return Err(Trap::InvalidControlState {
                pc,
                cause: InvalidControlCause::InvalidImage,
            });
        }
        if self.state.spc & 0x0f != 0 || self.state.ssp & 0x3f != 0 {
            return Err(Trap::InvalidControlState {
                pc,
                cause: InvalidControlCause::InvalidImage,
            });
        }
        self.validate_return_target_in_cs(bus, pc, self.state.spc, self.state.scs, true)?;
        self.validate_saved_stack_pointer(pc, self.state.ssp, self.state.sss)?;

        let saved_urctl = u64::from(self.state.flags.bits())
            | (u64::from(self.state.status.bits()) << 16)
            | URCTL_VALID;
        self.state.urpc = next_pc;
        self.state.ursp = self.state.sp;
        self.state.urcs = self.state.segments.cs();
        self.state.urds = self.state.segments.ds();
        self.state.urss = self.state.segments.ss();
        self.state.urctl = saved_urctl;
        self.state.segments.set(SegmentSelector::Cs, self.state.scs);
        self.state.segments.set(SegmentSelector::Ds, self.state.sds);
        self.state.segments.set(SegmentSelector::Ss, self.state.sss);
        self.state.sp = self.state.ssp;
        self.state.status.insert(Status::PM);
        self.state.pc = self.state.spc;
        self.repeat = None;
        Ok(StepResult::Running)
    }

    fn execute_system_return<B: Bus>(&mut self, bus: &mut B, pc: u64) -> Result<StepResult, Trap> {
        if self.state.status.contains(Status::EA) || self.state.urctl & URCTL_VALID == 0 {
            return Err(Trap::InvalidControlState {
                pc,
                cause: InvalidControlCause::InvalidTransition,
            });
        }
        let control = self.state.urctl;
        let decoded = Self::decode_urctl(pc, control)?;
        self.validate_user_return_bank(bus, pc, control, decoded)?;

        self.state.flags = decoded.0;
        self.state.status = decoded.1;
        self.state
            .segments
            .set(SegmentSelector::Cs, self.state.urcs);
        self.state
            .segments
            .set(SegmentSelector::Ds, self.state.urds);
        self.state
            .segments
            .set(SegmentSelector::Ss, self.state.urss);
        self.state.sp = self.state.ursp;
        self.state.pc = self.state.urpc;
        self.state.urctl &= !URCTL_VALID;
        Ok(StepResult::Running)
    }

    fn execute_fpu<B: Bus>(
        &mut self,
        bus: &mut B,
        pc: u64,
        next_pc: u64,
        instruction: &DecodedInstruction,
    ) -> Result<StepResult, Trap> {
        match instruction.opcode {
            Opcode::Fmov | Opcode::Fmovcc => self.execute_fpu_move(bus, pc, next_pc, instruction),
            Opcode::Fclr => self.execute_fpu_clear(pc, next_pc, instruction),
            Opcode::Fmovcr => self.execute_fpu_constant(pc, next_pc, instruction),
            Opcode::Fpushp | Opcode::Fpopp => {
                self.execute_fpu_pair_stack(bus, pc, next_pc, instruction)
            }
            Opcode::Fabs | Opcode::Fneg | Opcode::Fcopysign | Opcode::Fxchg => {
                self.execute_fpu_bitwise(bus, pc, next_pc, instruction)
            }
            Opcode::Fadd
            | Opcode::Fsub
            | Opcode::Fmul
            | Opcode::Fdiv
            | Opcode::Fmin
            | Opcode::Fmax
            | Opcode::Fmod
            | Opcode::Frem
            | Opcode::Fscale => self.execute_fpu_binary(bus, pc, next_pc, instruction),
            Opcode::Fmadd | Opcode::Fmsub | Opcode::Fnmadd | Opcode::Fnmsub => {
                self.execute_fpu_fused(bus, pc, next_pc, instruction)
            }
            Opcode::Fsqrt
            | Opcode::Fint
            | Opcode::Fintrz
            | Opcode::Fround
            | Opcode::Ftrunc
            | Opcode::Fceil
            | Opcode::Ffloor
            | Opcode::Fgetexp
            | Opcode::Fgetman => self.execute_fpu_unary(bus, pc, next_pc, instruction),
            Opcode::Fclass | Opcode::Fcvt | Opcode::Fcvtu => {
                self.execute_fpu_convert(bus, pc, next_pc, instruction)
            }
            Opcode::Fcmp | Opcode::Ftest => self.execute_fpu_compare(bus, pc, next_pc, instruction),
            Opcode::Fbndii | Opcode::Fbndix | Opcode::Fbndxi | Opcode::Fbndxx => {
                self.execute_fpu_bounds(bus, pc, next_pc, instruction)
            }
            Opcode::Facosa
            | Opcode::Fasina
            | Opcode::Fatana
            | Opcode::Fatanha
            | Opcode::Fcosa
            | Opcode::Fcosha
            | Opcode::Fetoxa
            | Opcode::Fetoxm1a
            | Opcode::Flog10a
            | Opcode::Flog2a
            | Opcode::Flogna
            | Opcode::Flognp1a
            | Opcode::Fsina
            | Opcode::Fsincosa
            | Opcode::Fsinha
            | Opcode::Ftana
            | Opcode::Ftanha
            | Opcode::Ftentoxa
            | Opcode::Ftwotoxa => self.execute_fpu_trans(bus, pc, next_pc, instruction),
            _ => unreachable!(),
        }
    }

    fn execute_fpu_move<B: Bus>(
        &mut self,
        bus: &mut B,
        pc: u64,
        next_pc: u64,
        instruction: &DecodedInstruction,
    ) -> Result<StepResult, Trap> {
        if instruction.opcode == Opcode::Fmovcc
            && !self.state.flags.condition(field(instruction, 'c') as u8)
        {
            self.state.pc = next_pc;
            return Ok(StepResult::Running);
        }
        let size = fpu_size(instruction);
        let source = if let Some(source) = fpu_field(instruction, 's') {
            self.state.f[source] & size_mask(size)
        } else {
            self.read_ea_field(bus, pc, instruction, 'e', size)?
        };
        self.write_fpu_destination(bus, pc, instruction, size, source)?;
        self.state.pc = next_pc;
        Ok(StepResult::Running)
    }

    fn execute_fpu_binary<B: Bus>(
        &mut self,
        bus: &mut B,
        pc: u64,
        next_pc: u64,
        instruction: &DecodedInstruction,
    ) -> Result<StepResult, Trap> {
        let (status, accrued) = self.fpu_environment(pc)?;
        let size = fpu_size(instruction);
        let format = fp_format(size);
        let destination = fpu_field(instruction, 'd').ok_or(illegal_instruction(pc))?;
        let source = self.read_fpu_operand(bus, pc, instruction, 's', size)?;
        let operands = [source, self.state.f[destination] & size_mask(size)];
        let request = crate::fpu::effect::FpRequest {
            format,
            status,
            operands: &operands,
        };
        let effect = match instruction.opcode {
            Opcode::Fadd => crate::fpu::base_arithmetic::add(request),
            Opcode::Fsub => crate::fpu::base_arithmetic::subtract(request),
            Opcode::Fmul => crate::fpu::base_arithmetic::multiply(request),
            Opcode::Fdiv => crate::fpu::base_arithmetic::divide(request),
            Opcode::Fmin => crate::fpu::base_arithmetic::minimum(request),
            Opcode::Fmax => crate::fpu::base_arithmetic::maximum(request),
            Opcode::Fmod => crate::fpu::base_arithmetic::modulo(request),
            Opcode::Frem => crate::fpu::base_arithmetic::ieee_remainder(request),
            Opcode::Fscale => crate::fpu::base_arithmetic::scale(request),
            _ => unreachable!(),
        };
        self.apply_fpu_effect(
            bus,
            pc,
            next_pc,
            Some(instruction),
            size,
            effect,
            FpuDestination::Floating(destination),
            None,
            accrued,
        )
    }

    fn execute_fpu_convert<B: Bus>(
        &mut self,
        bus: &mut B,
        pc: u64,
        next_pc: u64,
        instruction: &DecodedInstruction,
    ) -> Result<StepResult, Trap> {
        let (status, accrued) = self.fpu_environment(pc)?;
        let size = fpu_size(instruction);
        let format = fp_format(size);
        let (effect, destination) = if instruction.opcode == Opcode::Fclass {
            let source = fpu_field(instruction, 's').ok_or(illegal_instruction(pc))?;
            let destination = general_field(instruction, 'd').ok_or(illegal_instruction(pc))?;
            (
                crate::fpu::base_convert_compare::classify(format, status, self.state.f[source]),
                FpuDestination::General(destination),
            )
        } else {
            match (
                general_field(instruction, 's'),
                fpu_field(instruction, 's'),
                general_field(instruction, 'd'),
                fpu_field(instruction, 'd'),
            ) {
                (Some(source), None, None, Some(destination)) => {
                    let effect = if instruction.opcode == Opcode::Fcvt {
                        crate::fpu::base_convert_compare::signed_integer_to_float(
                            format,
                            status,
                            self.state.r[source],
                        )
                    } else {
                        crate::fpu::base_convert_compare::unsigned_integer_to_float(
                            format,
                            status,
                            self.state.r[source],
                        )
                    };
                    (effect, FpuDestination::Floating(destination))
                }
                (None, Some(source), Some(destination), None) => {
                    let effect = if instruction.opcode == Opcode::Fcvt {
                        crate::fpu::base_convert_compare::float_to_signed_integer(
                            format,
                            status,
                            self.state.f[source],
                        )
                    } else {
                        crate::fpu::base_convert_compare::float_to_unsigned_integer(
                            format,
                            status,
                            self.state.f[source],
                        )
                    };
                    (effect, FpuDestination::General(destination))
                }
                (None, Some(source), None, Some(destination)) => (
                    crate::fpu::base_convert_compare::convert_format(
                        format,
                        status,
                        self.state.f[source],
                    ),
                    FpuDestination::Floating(destination),
                ),
                _ => return Err(illegal_instruction(pc)),
            }
        };
        self.apply_fpu_effect(
            bus,
            pc,
            next_pc,
            None,
            size,
            effect,
            destination,
            None,
            accrued,
        )
    }

    fn execute_fpu_clear(
        &mut self,
        pc: u64,
        next_pc: u64,
        instruction: &DecodedInstruction,
    ) -> Result<StepResult, Trap> {
        let destination = fpu_field(instruction, 'd').ok_or(illegal_instruction(pc))?;
        self.state.f[destination] = 0;
        self.state.pc = next_pc;
        Ok(StepResult::Running)
    }

    fn execute_fpu_constant(
        &mut self,
        pc: u64,
        next_pc: u64,
        instruction: &DecodedInstruction,
    ) -> Result<StepResult, Trap> {
        let destination = fpu_field(instruction, 'd').ok_or(illegal_instruction(pc))?;
        self.state.f[destination] = match read_unsigned(trailing_bytes(instruction), 2) {
            0x0000 => 0x0000_0000_0000_0000,
            0x0001 => 0x8000_0000_0000_0000,
            0x0002 => 0x3ff0_0000_0000_0000,
            0x0003 => 0xbff0_0000_0000_0000,
            0x0004 => 0x3fe0_0000_0000_0000,
            0x0005 => 0xbfe0_0000_0000_0000,
            0x0006 => 0x4000_0000_0000_0000,
            0x0007 => 0xc000_0000_0000_0000,
            0x0008 => 0x4024_0000_0000_0000,
            0x0009 => 0xc024_0000_0000_0000,
            0x0010 => 0x4009_21fb_5444_2d18,
            0x0011 => 0x3ff9_21fb_5444_2d18,
            0x0012 => 0x3fe9_21fb_5444_2d18,
            0x0013 => 0x4019_21fb_5444_2d18,
            0x0014 => 0x3fd4_5f30_6dc9_c883,
            0x0015 => 0x3fe4_5f30_6dc9_c883,
            0x0016 => 0x3ff6_a09e_667f_3bcd,
            0x0017 => 0x3fe6_a09e_667f_3bcc,
            0x0020 => 0x4005_bf0a_8b14_5769,
            0x0021 => 0x3ff7_1547_652b_82fe,
            0x0022 => 0x3fdb_cb7b_1526_e50e,
            0x0023 => 0x3fe6_2e42_fefa_39ef,
            0x0024 => 0x4002_6bb1_bbb5_5516,
            0x0025 => 0x400a_934f_0979_a371,
            0x0026 => 0x3fd3_4413_509f_79ff,
            0x0100 => 0x7ff0_0000_0000_0000,
            0x0101 => 0xfff0_0000_0000_0000,
            0x0102 => 0x7ff8_0000_0000_0000,
            0x0103 => 0xfff8_0000_0000_0000,
            0x0104 => 0x7ff0_0000_0000_0001,
            0x0105 => 0xfff0_0000_0000_0001,
            0x0110 => 0x7fef_ffff_ffff_ffff,
            0x0111 => 0xffef_ffff_ffff_ffff,
            0x0112 => 0x0010_0000_0000_0000,
            0x0113 => 0x8010_0000_0000_0000,
            0x0114 => 0x0000_0000_0000_0001,
            0x0115 => 0x8000_0000_0000_0001,
            0x0116 => 0x3cb0_0000_0000_0000,
            0x0117 => 0x000f_ffff_ffff_ffff,
            0x0118 => 0x800f_ffff_ffff_ffff,
            _ => return Err(illegal_instruction(pc)),
        };
        self.state.pc = next_pc;
        Ok(StepResult::Running)
    }

    fn execute_fpu_bitwise<B: Bus>(
        &mut self,
        bus: &mut B,
        pc: u64,
        next_pc: u64,
        instruction: &DecodedInstruction,
    ) -> Result<StepResult, Trap> {
        if instruction.opcode == Opcode::Fxchg {
            let lhs = fpu_field(instruction, 'l').ok_or(illegal_instruction(pc))?;
            let rhs = fpu_field(instruction, 'r').ok_or(illegal_instruction(pc))?;
            let (new_lhs, new_rhs) = crate::fpu::base_convert_compare::exchange_bits(
                self.state.f[lhs],
                self.state.f[rhs],
            );
            self.state.f[lhs] = new_lhs;
            self.state.f[rhs] = new_rhs;
            self.state.pc = next_pc;
            return Ok(StepResult::Running);
        }

        let size = fpu_size(instruction);
        let format = fp_format(size);
        let value = match instruction.opcode {
            Opcode::Fabs => crate::fpu::base_convert_compare::abs_bits(
                format,
                self.read_fpu_operand(bus, pc, instruction, 's', size)?,
            ),
            Opcode::Fneg => crate::fpu::base_convert_compare::negate_bits(
                format,
                self.read_fpu_operand(bus, pc, instruction, 's', size)?,
            ),
            Opcode::Fcopysign => {
                let sign = self.read_fpu_operand(bus, pc, instruction, 's', size)?;
                let magnitude = self.read_fpu_operand(bus, pc, instruction, 'm', size)?;
                crate::fpu::base_convert_compare::copy_sign_bits(format, sign, magnitude)
            }
            _ => unreachable!(),
        };
        self.write_fpu_destination(bus, pc, instruction, size, value)?;
        self.state.pc = next_pc;
        Ok(StepResult::Running)
    }

    fn execute_fpu_fused<B: Bus>(
        &mut self,
        bus: &mut B,
        pc: u64,
        next_pc: u64,
        instruction: &DecodedInstruction,
    ) -> Result<StepResult, Trap> {
        let (status, accrued) = self.fpu_environment(pc)?;
        let size = fpu_size(instruction);
        let destination = fpu_field(instruction, 'd').ok_or(illegal_instruction(pc))?;
        let lhs = self.read_fpu_operand(bus, pc, instruction, 'l', size)?;
        let rhs = self.read_fpu_operand(bus, pc, instruction, 'r', size)?;
        let operands = [lhs, rhs, self.state.f[destination] & size_mask(size)];
        let request = crate::fpu::effect::FpRequest {
            format: fp_format(size),
            status,
            operands: &operands,
        };
        let effect = match instruction.opcode {
            Opcode::Fmadd => crate::fpu::base_arithmetic::fused_multiply_add(request),
            Opcode::Fmsub => crate::fpu::base_arithmetic::fused_multiply_subtract(request),
            Opcode::Fnmadd => crate::fpu::base_arithmetic::fused_negated_multiply_add(request),
            Opcode::Fnmsub => crate::fpu::base_arithmetic::fused_negated_multiply_subtract(request),
            _ => unreachable!(),
        };
        self.apply_fpu_effect(
            bus,
            pc,
            next_pc,
            Some(instruction),
            size,
            effect,
            FpuDestination::Floating(destination),
            None,
            accrued,
        )
    }

    fn execute_fpu_unary<B: Bus>(
        &mut self,
        bus: &mut B,
        pc: u64,
        next_pc: u64,
        instruction: &DecodedInstruction,
    ) -> Result<StepResult, Trap> {
        let (status, accrued) = self.fpu_environment(pc)?;
        let size = fpu_size(instruction);
        let format = fp_format(size);
        let source = self.read_fpu_operand(bus, pc, instruction, 's', size)?;
        let operands = [source];
        let request = crate::fpu::effect::FpRequest {
            format,
            status,
            operands: &operands,
        };
        let destination = if let Some(destination) = fpu_field(instruction, 'd') {
            FpuDestination::Floating(destination)
        } else {
            FpuDestination::Memory(self.preflight_fpu_memory_destination(
                bus,
                pc,
                instruction,
                'e',
                size,
            )?)
        };
        use crate::fpu::base_convert_compare::IntegralRounding;
        let effect = match instruction.opcode {
            Opcode::Fsqrt => crate::fpu::base_arithmetic::square_root(request),
            Opcode::Fint => crate::fpu::base_convert_compare::round_integral(
                format,
                status,
                source,
                IntegralRounding::Dynamic,
            ),
            Opcode::Fintrz => crate::fpu::base_convert_compare::round_integral(
                format,
                status,
                source,
                IntegralRounding::TowardZero,
            ),
            Opcode::Fround => crate::fpu::base_convert_compare::round_integral(
                format,
                status,
                source,
                IntegralRounding::NearestEven,
            ),
            Opcode::Ftrunc => crate::fpu::base_convert_compare::round_integral(
                format,
                status,
                source,
                IntegralRounding::TowardZero,
            ),
            Opcode::Fceil => crate::fpu::base_convert_compare::round_integral(
                format,
                status,
                source,
                IntegralRounding::TowardPositive,
            ),
            Opcode::Ffloor => crate::fpu::base_convert_compare::round_integral(
                format,
                status,
                source,
                IntegralRounding::TowardNegative,
            ),
            Opcode::Fgetexp => {
                crate::fpu::base_convert_compare::get_exponent(format, status, source)
            }
            Opcode::Fgetman => {
                crate::fpu::base_convert_compare::get_mantissa(format, status, source)
            }
            _ => unreachable!(),
        };
        self.apply_fpu_effect(
            bus,
            pc,
            next_pc,
            Some(instruction),
            size,
            effect,
            destination,
            None,
            accrued,
        )
    }

    fn execute_fpu_compare<B: Bus>(
        &mut self,
        bus: &mut B,
        pc: u64,
        next_pc: u64,
        instruction: &DecodedInstruction,
    ) -> Result<StepResult, Trap> {
        let (status, accrued) = self.fpu_environment(pc)?;
        let size = fpu_size(instruction);
        let format = fp_format(size);
        let flags_effect = if instruction.opcode == Opcode::Fcmp {
            let source = self.read_fpu_operand(bus, pc, instruction, 's', size)?;
            let destination = fpu_field(instruction, 'd').ok_or(illegal_instruction(pc))?;
            crate::fpu::base_convert_compare::compare(
                format,
                status,
                source,
                self.state.f[destination],
            )
        } else {
            let source = self.read_fpu_operand(bus, pc, instruction, 's', size)?;
            crate::fpu::base_convert_compare::test(format, status, source)
        };
        self.apply_fpu_effect(
            bus,
            pc,
            next_pc,
            Some(instruction),
            size,
            flags_effect.effect,
            FpuDestination::None,
            Some((flags_effect.mask, flags_effect.value)),
            accrued,
        )
    }

    fn execute_fpu_bounds<B: Bus>(
        &mut self,
        bus: &mut B,
        pc: u64,
        next_pc: u64,
        instruction: &DecodedInstruction,
    ) -> Result<StepResult, Trap> {
        let (status, accrued) = self.fpu_environment(pc)?;
        let size = fpu_size(instruction);
        let low = self.read_fpu_operand(bus, pc, instruction, 'l', size)?;
        let value = self.read_fpu_operand(bus, pc, instruction, 'v', size)?;
        let high = self.read_fpu_operand(bus, pc, instruction, 'h', size)?;
        use crate::fpu::base_convert_compare::BoundsMode;
        let mode = match instruction.opcode {
            Opcode::Fbndii => BoundsMode::InclusiveInclusive,
            Opcode::Fbndix => BoundsMode::InclusiveExclusive,
            Opcode::Fbndxi => BoundsMode::ExclusiveInclusive,
            Opcode::Fbndxx => BoundsMode::ExclusiveExclusive,
            _ => unreachable!(),
        };
        let flags_effect = crate::fpu::base_convert_compare::bounds(
            fp_format(size),
            status,
            low,
            value,
            high,
            mode,
        );
        self.apply_fpu_effect(
            bus,
            pc,
            next_pc,
            Some(instruction),
            size,
            flags_effect.effect,
            FpuDestination::None,
            Some((flags_effect.mask, flags_effect.value)),
            accrued,
        )
    }

    fn execute_fpu_trans<B: Bus>(
        &mut self,
        bus: &mut B,
        pc: u64,
        next_pc: u64,
        instruction: &DecodedInstruction,
    ) -> Result<StepResult, Trap> {
        let (status, accrued) = self.fpu_environment(pc)?;
        let size = fpu_size(instruction);
        let source = fpu_field(instruction, 's').ok_or(illegal_instruction(pc))?;
        let operands = [self.state.f[source] & size_mask(size)];
        let request = crate::fpu::effect::FpRequest {
            format: fp_format(size),
            status,
            operands: &operands,
        };
        use crate::fpu::trans::contracts::TransOperation;
        let operation = match instruction.opcode {
            Opcode::Fsina => TransOperation::Sine,
            Opcode::Fcosa => TransOperation::Cosine,
            Opcode::Ftana => TransOperation::Tangent,
            Opcode::Fsincosa => TransOperation::SineCosine,
            Opcode::Fasina => TransOperation::ArcSine,
            Opcode::Facosa => TransOperation::ArcCosine,
            Opcode::Fatana => TransOperation::ArcTangent,
            Opcode::Fsinha => TransOperation::HyperbolicSine,
            Opcode::Fcosha => TransOperation::HyperbolicCosine,
            Opcode::Ftanha => TransOperation::HyperbolicTangent,
            Opcode::Fatanha => TransOperation::HyperbolicArcTangent,
            Opcode::Fetoxa => TransOperation::Exponential,
            Opcode::Fetoxm1a => TransOperation::ExponentialMinusOne,
            Opcode::Ftwotoxa => TransOperation::ExponentialBaseTwo,
            Opcode::Ftentoxa => TransOperation::ExponentialBaseTen,
            Opcode::Flogna => TransOperation::NaturalLogarithm,
            Opcode::Flognp1a => TransOperation::NaturalLogarithmPlusOne,
            Opcode::Flog2a => TransOperation::LogarithmBaseTwo,
            Opcode::Flog10a => TransOperation::LogarithmBaseTen,
            _ => unreachable!(),
        };
        let destination = if instruction.opcode == Opcode::Fsincosa {
            FpuDestination::FloatingPair(
                fpu_field(instruction, 'd').ok_or(illegal_instruction(pc))?,
                fpu_field(instruction, 'c').ok_or(illegal_instruction(pc))?,
            )
        } else {
            FpuDestination::Floating(fpu_field(instruction, 'd').ok_or(illegal_instruction(pc))?)
        };
        self.apply_fpu_effect(
            bus,
            pc,
            next_pc,
            Some(instruction),
            size,
            crate::fpu::execute_trans(operation, request),
            destination,
            None,
            accrued,
        )
    }

    fn execute_fpu_pair_stack<B: Bus>(
        &mut self,
        bus: &mut B,
        pc: u64,
        next_pc: u64,
        instruction: &DecodedInstruction,
    ) -> Result<StepResult, Trap> {
        let first = field(instruction, 'i') as usize * 2;
        if instruction.opcode == Opcode::Fpushp {
            let final_sp = self.stack_pair_start(pc, AccessKind::Write, true)?;
            self.validate_stack_pair(bus, pc, final_sp, AccessKind::Write)?;
            self.write_virtual(
                bus,
                pc,
                SegmentSelector::Ss,
                final_sp + 8,
                AccessDomain::Current,
                Size::Quad,
                self.state.f[first],
            )
            .map_err(|trap| page_fault_metadata(trap, Size::Quad, Some(0xff), false))?;
            self.write_virtual(
                bus,
                pc,
                SegmentSelector::Ss,
                final_sp,
                AccessDomain::Current,
                Size::Quad,
                self.state.f[first + 1],
            )
            .map_err(|trap| page_fault_metadata(trap, Size::Quad, Some(0xff), false))?;
            self.state.sp = final_sp;
        } else {
            let start = self.stack_pair_start(pc, AccessKind::Read, false)?;
            self.validate_stack_pair(bus, pc, start, AccessKind::Read)?;
            let second = self
                .read_virtual(
                    bus,
                    pc,
                    SegmentSelector::Ss,
                    start,
                    AccessDomain::Current,
                    Size::Quad,
                )
                .map_err(|trap| page_fault_metadata(trap, Size::Quad, Some(0xff), false))?;
            let first_value = self
                .read_virtual(
                    bus,
                    pc,
                    SegmentSelector::Ss,
                    start + 8,
                    AccessDomain::Current,
                    Size::Quad,
                )
                .map_err(|trap| page_fault_metadata(trap, Size::Quad, Some(0xff), false))?;
            self.state.f[first + 1] = second;
            self.state.f[first] = first_value;
            self.state.sp = start + 16;
        }
        self.state.pc = next_pc;
        Ok(StepResult::Running)
    }

    fn fpu_environment(
        &self,
        pc: u64,
    ) -> Result<(crate::fpu::env::FpStatus, crate::fpu::env::FpCauses), Trap> {
        let status = crate::fpu::env::FpStatus::decode(self.state.fstatus).map_err(|_| {
            Trap::InvalidControlState {
                pc,
                cause: InvalidControlCause::ReservedBits,
            }
        })?;
        let accrued = crate::fpu::env::FpCauses::from_bits(self.state.fflags).map_err(|_| {
            Trap::InvalidControlState {
                pc,
                cause: InvalidControlCause::ReservedBits,
            }
        })?;
        Ok((status, accrued))
    }

    #[allow(clippy::too_many_arguments)]
    fn apply_fpu_effect<B: Bus>(
        &mut self,
        bus: &mut B,
        pc: u64,
        next_pc: u64,
        _instruction: Option<&DecodedInstruction>,
        size: Size,
        effect: crate::fpu::effect::FpEffect,
        destination: FpuDestination,
        flags: Option<(Flags, Flags)>,
        accrued: crate::fpu::env::FpCauses,
    ) -> Result<StepResult, Trap> {
        let crate::fpu::effect::FpEffect::Commit { result, causes } = effect else {
            return Err(Trap::FloatingPointFault {
                pc,
                causes: effect.causes(),
            });
        };
        match (result, destination) {
            (crate::fpu::effect::FpResult::None, FpuDestination::None) => {}
            (crate::fpu::effect::FpResult::Float(value), FpuDestination::Floating(register)) => {
                self.state.f[register] = value & size_mask(size);
            }
            (crate::fpu::effect::FpResult::Float(value), FpuDestination::Memory(destination)) => {
                self.write_virtual(
                    bus,
                    pc,
                    destination.segment,
                    destination.offset,
                    AccessDomain::Current,
                    size,
                    value,
                )
                .map_err(|trap| {
                    page_fault_metadata(trap, size, Some(destination.operand), false)
                })?;
            }
            (
                crate::fpu::effect::FpResult::FloatPair(first, second),
                FpuDestination::FloatingPair(a, b),
            ) => {
                self.state.f[a] = first & size_mask(size);
                self.state.f[b] = second & size_mask(size);
            }
            (crate::fpu::effect::FpResult::Integer(value), FpuDestination::General(register)) => {
                self.state.r[register] = value;
            }
            _ => return Err(illegal_instruction(pc)),
        }
        if let Some((mask, value)) = flags {
            self.state.flags = (self.state.flags & !mask) | (value & mask);
        }
        self.state.fflags = accrued.union(causes).bits();
        self.state.pc = next_pc;
        Ok(StepResult::Running)
    }

    fn preflight_fpu_memory_destination<B: Bus>(
        &mut self,
        bus: &mut B,
        pc: u64,
        instruction: &DecodedInstruction,
        symbol: char,
        size: Size,
    ) -> Result<ResolvedMemoryDestination, Trap> {
        let ea = ea_field(instruction, symbol).ok_or(illegal_instruction(pc))?;
        if matches!(
            ea,
            CompactEa::Register(_) | CompactEa::StackPointer | CompactEa::Immediate(_)
        ) {
            return Err(illegal_instruction(pc));
        }
        let (segment, offset) = self.effective_location_with_payload(
            pc,
            ea,
            ea_payload_for_symbol(instruction, symbol),
            size,
        )?;
        let operand = ea_field_ordinal(instruction, symbol);
        self.validate_virtual_access(
            bus,
            pc,
            segment,
            offset,
            AccessDomain::Current,
            size,
            AccessKind::Write,
        )
        .map_err(|trap| page_fault_metadata(trap, size, Some(operand), false))?;
        Ok(ResolvedMemoryDestination {
            segment,
            offset,
            operand,
        })
    }

    fn write_fpu_destination<B: Bus>(
        &mut self,
        bus: &mut B,
        pc: u64,
        instruction: &DecodedInstruction,
        size: Size,
        value: u64,
    ) -> Result<(), Trap> {
        if let Some(destination) = fpu_field(instruction, 'd') {
            self.state.f[destination] = value & size_mask(size);
            Ok(())
        } else {
            self.write_ea_field(bus, pc, instruction, 'e', size, value)
        }
    }

    fn read_fpu_operand<B: Bus>(
        &mut self,
        bus: &mut B,
        pc: u64,
        instruction: &DecodedInstruction,
        symbol: char,
        size: Size,
    ) -> Result<u64, Trap> {
        if let Some(register) = fpu_field(instruction, symbol) {
            return Ok(self.state.f[register] & size_mask(size));
        }
        let memory_symbol = if ea_field(instruction, symbol).is_some() {
            symbol
        } else {
            'e'
        };
        self.read_ea_field(bus, pc, instruction, memory_symbol, size)
    }

    fn deliver_required_event<B: Bus>(&mut self, bus: &mut B, request: EventRequest) -> StepResult {
        if !self.state.ecr.valid() || self.state.hidden_current_edepth >= 15 {
            self.halted = true;
            return StepResult::Halted;
        }
        match self.try_deliver_event(bus, request) {
            Ok(()) => StepResult::Running,
            Err(failure) => {
                if request.code.base_exception() == Some(BaseException::DoubleFault)
                    || self.state.hidden_current_edepth >= 15
                {
                    self.halted = true;
                    return StepResult::Halted;
                }
                let mut error_code = failure.stage | (1 << 26);
                if failure.stage != DOUBLE_FAULT_ENTRY_STATE {
                    error_code |= 1 << 24;
                }
                if failure.fault_linear != 0 {
                    error_code |= 1 << 25;
                }
                let double_fault = EventRequest {
                    code: EventCode::exception(BaseException::DoubleFault),
                    saved_pc: request.saved_pc,
                    error_code,
                    fault_ea: failure.fault_ea,
                    fault_linear: failure.fault_linear,
                    event_aux: u64::from(request.code.raw()),
                };
                if self.try_deliver_event(bus, double_fault).is_ok() {
                    StepResult::Running
                } else {
                    self.halted = true;
                    StepResult::Halted
                }
            }
        }
    }

    fn try_deliver_event<B: Bus>(
        &mut self,
        bus: &mut B,
        request: EventRequest,
    ) -> Result<(), DeliveryFailure> {
        let pc = request.saved_pc;
        bus.begin_transaction().map_err(|error| DeliveryFailure {
            _trap: Trap::Bus { pc, error },
            stage: DOUBLE_FAULT_FRAME_STORE,
            fault_ea: 0,
            fault_linear: 0,
        })?;
        let saved_state = self.state.clone();
        let saved_halted = self.halted;
        let saved_repeat = self.repeat.clone();
        match self.enter_event_transaction(bus, pc, request) {
            Ok(()) => {
                bus.commit_transaction();
                Ok(())
            }
            Err(failure) => {
                bus.rollback_transaction();
                self.state = saved_state;
                self.halted = saved_halted;
                self.repeat = saved_repeat;
                Err(failure)
            }
        }
    }

    fn enter_event_transaction<B: Bus>(
        &mut self,
        bus: &mut B,
        pc: u64,
        request: EventRequest,
    ) -> Result<(), DeliveryFailure> {
        let descriptor = request.code.frame_descriptor().ok_or(DeliveryFailure {
            _trap: Trap::InvalidControlState {
                pc,
                cause: InvalidControlCause::InvalidImage,
            },
            stage: DOUBLE_FAULT_ENTRY_STATE,
            fault_ea: 0,
            fault_linear: 0,
        })?;
        if !self.state.ecs.valid() || !self.state.eds.valid() || self.state.epc & 0x0f != 0 {
            return Err(DeliveryFailure {
                _trap: Trap::InvalidControlState {
                    pc,
                    cause: InvalidControlCause::InvalidImage,
                },
                stage: DOUBLE_FAULT_ENTRY_STATE,
                fault_ea: 0,
                fault_linear: 0,
            });
        }
        self.validate_event_entry_target(bus, pc)
            .map_err(|trap| DeliveryFailure {
                _trap: trap,
                stage: DOUBLE_FAULT_ENTRY_STATE,
                fault_ea: 0,
                fault_linear: 0,
            })?;

        let requested_esl = if request.code.base_exception() == Some(BaseException::DoubleFault) {
            3
        } else {
            2
        };
        let current_ea = self.state.status.contains(Status::EA);
        let selected_esl = if !current_ea || requested_esl > self.state.hidden_current_esl {
            requested_esl
        } else {
            self.state.hidden_current_esl
        };
        let switch_stack = !current_ea || selected_esl > self.state.hidden_current_esl;
        let (event_ss, stack_top) = if switch_stack {
            self.event_stack_pair(selected_esl)
        } else {
            (self.state.segments.ss(), self.state.sp)
        };
        if !event_ss.valid() || (switch_stack && stack_top & 0x3f != 0) {
            return Err(DeliveryFailure {
                _trap: Trap::InvalidControlState {
                    pc,
                    cause: InvalidControlCause::InvalidImage,
                },
                stage: DOUBLE_FAULT_STACK_STATE,
                fault_ea: stack_top,
                fault_linear: 0,
            });
        }

        let repeat = self
            .repeat_continuation(pc)
            .map_err(|cause| DeliveryFailure {
                _trap: Trap::InvalidControlState { pc, cause },
                stage: DOUBLE_FAULT_ENTRY_STATE,
                fault_ea: 0,
                fault_linear: 0,
            })?;
        let control = FrameControl::new(
            descriptor.frame_type,
            if current_ea {
                self.state.hidden_current_edepth
            } else {
                0
            },
            if current_ea {
                self.state.hidden_current_esl
            } else {
                0
            },
            repeat.is_some(),
            self.state.flags.bits(),
            self.state.status.bits(),
        )
        .map_err(|cause| DeliveryFailure {
            _trap: Trap::InvalidControlState { pc, cause },
            stage: DOUBLE_FAULT_ENTRY_STATE,
            fault_ea: 0,
            fault_linear: 0,
        })?;
        let frame_base = stack_top
            .checked_sub(u64::from(descriptor.slots) * 8)
            .ok_or(DeliveryFailure {
                _trap: Trap::InvalidControlState {
                    pc,
                    cause: InvalidControlCause::InvalidImage,
                },
                stage: DOUBLE_FAULT_FRAME_ADDRESS,
                fault_ea: stack_top,
                fault_linear: 0,
            })?;
        let addresses = self
            .event_frame_addresses(bus, pc, event_ss, frame_base, descriptor.slots)
            .map_err(|trap| DeliveryFailure {
                _trap: trap,
                stage: DOUBLE_FAULT_FRAME_ADDRESS,
                fault_ea: frame_base,
                fault_linear: 0,
            })?;
        let frame = [
            control.encode(),
            EventInfo::new(request.code).encode(),
            repeat.map_or(0, RepeatContinuation::encode),
            request.saved_pc,
            self.state.sp,
            self.state.segments.cs().raw(),
            self.state.segments.ds().raw(),
            self.state.segments.ss().raw(),
            request.error_code,
            request.fault_ea,
            request.fault_linear,
            if descriptor.frame_type == ExceptionFrameType::Auxiliary {
                request.event_aux
            } else {
                0
            },
        ];
        for (address, value) in addresses.into_iter().zip(frame) {
            write_bus(bus, address, Size::Quad, value).map_err(|error| DeliveryFailure {
                _trap: Trap::Bus { pc, error },
                stage: DOUBLE_FAULT_FRAME_STORE,
                fault_ea: frame_base,
                fault_linear: 0,
            })?;
        }

        self.state.segments.set(SegmentSelector::Cs, self.state.ecs);
        self.state.segments.set(SegmentSelector::Ds, self.state.eds);
        self.state.segments.set(SegmentSelector::Ss, event_ss);
        self.state.sp = frame_base;
        self.state.pc = self.state.epc;
        self.state.status.insert(Status::PM | Status::EA);
        self.state
            .status
            .remove(Status::IE | Status::TF | Status::RF);
        if request.code.class() == Some(EventClass::Nmi) {
            self.state.status.insert(Status::NI);
            self.state.ecr = self.state.ecr.with_nmi_pending(false);
            self.halted = false;
        }
        self.state.hidden_current_edepth = control.saved_edepth + 1;
        self.state.hidden_current_esl = selected_esl;
        self.repeat = None;
        Ok(())
    }

    fn execute_event_return<B: Bus>(&mut self, bus: &mut B, pc: u64) -> Result<StepResult, Trap> {
        if !self.state.status.contains(Status::EA) || self.state.hidden_current_edepth == 0 {
            return Err(Trap::InvalidControlState {
                pc,
                cause: InvalidControlCause::InvalidTransition,
            });
        }
        let frame_base = self.state.sp;
        let raw_control = self.read_virtual(
            bus,
            pc,
            SegmentSelector::Ss,
            frame_base,
            AccessDomain::Current,
            Size::Quad,
        )?;
        let control = FrameControl::decode(raw_control)
            .map_err(|cause| Trap::InvalidControlState { pc, cause })?;
        let mut frame = vec![0u64; usize::from(control.frame_size())];
        frame[0] = raw_control;
        for (offset, value) in frame.iter_mut().enumerate().skip(1) {
            let logical = frame_base.wrapping_add(offset as u64 * 8);
            *value = self.read_virtual(
                bus,
                pc,
                SegmentSelector::Ss,
                logical,
                AccessDomain::Current,
                Size::Quad,
            )?;
        }
        let metadata = EventFrameMetadata::decode_return_frame(frame[0], frame[1], frame[2])
            .map_err(|cause| Trap::InvalidControlState { pc, cause })?;
        metadata
            .validate_for_eret(
                self.state.hidden_current_edepth,
                self.state.hidden_current_esl,
            )
            .map_err(|cause| Trap::InvalidControlState { pc, cause })?;
        match metadata.control.frame_type {
            ExceptionFrameType::Error if frame[9] != 0 => {
                return Err(Trap::InvalidControlState {
                    pc,
                    cause: InvalidControlCause::InvalidImage,
                });
            }
            ExceptionFrameType::PageFault if frame[11] != 0 => {
                return Err(Trap::InvalidControlState {
                    pc,
                    cause: InvalidControlCause::InvalidImage,
                });
            }
            _ => {}
        }
        let cs = crate::SegmentRegister::from_raw(frame[5]);
        let ds = crate::SegmentRegister::from_raw(frame[6]);
        let ss = crate::SegmentRegister::from_raw(frame[7]);
        if !cs.valid() || !ds.valid() || !ss.valid() {
            return Err(Trap::InvalidControlState {
                pc,
                cause: InvalidControlCause::InvalidImage,
            });
        }
        let saved_privileged = metadata.control.status & Status::PM.bits() != 0;
        self.validate_return_target_in_cs(bus, pc, frame[3], cs, saved_privileged)?;
        self.validate_saved_stack_pointer(pc, frame[4], ss)?;
        let restored_repeat = self.restore_repeat_continuation(
            bus,
            pc,
            frame[3],
            metadata.repeat,
            cs,
            saved_privileged,
        )?;
        self.state.flags = Flags::from_bits_retain(metadata.control.flags);
        self.state.status = Status::from_bits_retain(metadata.control.status);
        self.state.segments.set(SegmentSelector::Cs, cs);
        self.state.segments.set(SegmentSelector::Ds, ds);
        self.state.segments.set(SegmentSelector::Ss, ss);
        self.state.sp = frame[4];
        self.state.pc = frame[3];
        self.state.hidden_current_edepth = metadata.control.saved_edepth;
        self.state.hidden_current_esl = metadata.control.saved_esl;
        self.repeat = restored_repeat;
        Ok(StepResult::Running)
    }

    fn event_stack_pair(&self, level: u8) -> (crate::SegmentRegister, u64) {
        match level {
            1 => (self.state.iss, self.state.isp),
            2 => (self.state.fss, self.state.fsp),
            _ => (self.state.dss, self.state.dsp),
        }
    }

    fn repeat_continuation(
        &self,
        saved_pc: u64,
    ) -> Result<Option<RepeatContinuation>, InvalidControlCause> {
        let Some(active) = &self.repeat else {
            return Ok(None);
        };
        if active.grouped {
            let group_start = active
                .bodies
                .first()
                .map(|(pc, _)| *pc)
                .ok_or(InvalidControlCause::InvalidImage)?;
            let group_start_delta = saved_pc
                .checked_sub(group_start)
                .and_then(|value| u16::try_from(value).ok())
                .ok_or(InvalidControlCause::InvalidImage)?;
            let body_bytes = active
                .after_pc
                .checked_sub(group_start)
                .and_then(|value| u16::try_from(value).ok())
                .ok_or(InvalidControlCause::InvalidImage)?;
            RepeatContinuation::new(
                active.counter,
                0,
                RepeatKind::Group,
                group_start_delta,
                body_bytes,
            )
            .map(Some)
        } else {
            RepeatContinuation::new(active.counter, active.condition, RepeatKind::Scalar, 0, 0)
                .map(Some)
        }
    }

    fn restore_repeat_continuation<B: Bus>(
        &self,
        bus: &mut B,
        pc: u64,
        saved_pc: u64,
        continuation: Option<RepeatContinuation>,
        saved_cs: crate::SegmentRegister,
        saved_privileged: bool,
    ) -> Result<Option<RepeatState>, Trap> {
        let Some(continuation) = continuation else {
            return Ok(None);
        };
        match continuation.kind {
            RepeatKind::Scalar => {
                let body =
                    self.fetch_decode_in_context(bus, pc, saved_pc, saved_cs, saved_privileged)?;
                let eligible = if continuation.condition == 0 {
                    body.attributes.repeat_rep
                } else {
                    body.attributes.repeat_repcc
                };
                if !eligible || is_repeat_forbidden(&body) {
                    return Err(Trap::InvalidControlState {
                        pc,
                        cause: InvalidControlCause::InvalidImage,
                    });
                }
                let remaining = self.state.r[continuation.register as usize];
                if remaining == 0 {
                    return Err(Trap::InvalidControlState {
                        pc,
                        cause: InvalidControlCause::InvalidImage,
                    });
                }
                Ok(Some(RepeatState {
                    counter: continuation.register,
                    remaining,
                    condition: continuation.condition,
                    after_pc: saved_pc.wrapping_add(u64::from(body.length_bytes)),
                    bodies: vec![(saved_pc, body)],
                    index: 0,
                    grouped: false,
                }))
            }
            RepeatKind::Group => {
                let group_start = saved_pc
                    .checked_sub(u64::from(continuation.group_start_delta))
                    .ok_or(Trap::InvalidControlState {
                        pc,
                        cause: InvalidControlCause::InvalidImage,
                    })?;
                let after_pc = group_start
                    .checked_add(u64::from(continuation.body_bytes))
                    .ok_or(Trap::InvalidControlState {
                        pc,
                        cause: InvalidControlCause::InvalidImage,
                    })?;
                let mut cursor = group_start;
                let mut bodies = Vec::new();
                let mut index = None;
                while cursor < after_pc {
                    if cursor == saved_pc {
                        index = Some(bodies.len());
                    }
                    let body =
                        self.fetch_decode_in_context(bus, pc, cursor, saved_cs, saved_privileged)?;
                    if !body.attributes.repeat_repg || is_repeat_forbidden(&body) {
                        return Err(Trap::InvalidControlState {
                            pc,
                            cause: InvalidControlCause::InvalidImage,
                        });
                    }
                    let next = cursor.checked_add(u64::from(body.length_bytes)).ok_or(
                        Trap::InvalidControlState {
                            pc,
                            cause: InvalidControlCause::InvalidImage,
                        },
                    )?;
                    if next > after_pc {
                        return Err(Trap::InvalidControlState {
                            pc,
                            cause: InvalidControlCause::InvalidImage,
                        });
                    }
                    bodies.push((cursor, body));
                    cursor = next;
                }
                let index = index.ok_or(Trap::InvalidControlState {
                    pc,
                    cause: InvalidControlCause::InvalidImage,
                })?;
                Ok(Some(RepeatState {
                    counter: continuation.register,
                    remaining: 0,
                    condition: 0,
                    bodies,
                    index,
                    after_pc,
                    grouped: true,
                }))
            }
        }
    }

    fn execute_long_control<B: Bus>(
        &mut self,
        bus: &mut B,
        pc: u64,
        next_pc: u64,
        instruction: &DecodedInstruction,
    ) -> Result<StepResult, Trap> {
        if instruction.opcode == Opcode::Lret {
            let start = self.stack_pair_start(pc, AccessKind::Read, false)?;
            self.validate_stack_pair(bus, pc, start, AccessKind::Read)?;
            let target = self
                .read_virtual(
                    bus,
                    pc,
                    SegmentSelector::Ss,
                    start,
                    AccessDomain::Current,
                    Size::Quad,
                )
                .map_err(|trap| page_fault_metadata(trap, Size::Quad, Some(0xff), false))?;
            let cs = self
                .read_virtual(
                    bus,
                    pc,
                    SegmentSelector::Ss,
                    start + 8,
                    AccessDomain::Current,
                    Size::Quad,
                )
                .map_err(|trap| page_fault_metadata(trap, Size::Quad, Some(0xff), false))?;
            let cs = crate::SegmentRegister::from_raw(cs);
            if !cs.valid() {
                return Err(Trap::InvalidControlState {
                    pc,
                    cause: InvalidControlCause::InvalidImage,
                });
            }
            self.validate_control_target_in_cs(bus, pc, target, cs)?;
            self.state.sp = start + 16;
            self.state.segments.set(SegmentSelector::Cs, cs);
            self.state.pc = target;
            return Ok(StepResult::Running);
        }
        let segment = self.state.r[field(instruction, 'r') as usize];
        let ea = first_ea(instruction).ok_or(illegal_instruction(pc))?;
        let target = self.read_ea(bus, pc, instruction, ea, Size::Quad)?;
        let segment = crate::SegmentRegister::from_raw(segment);
        if !segment.valid() {
            return Err(Trap::InvalidControlState {
                pc,
                cause: InvalidControlCause::InvalidImage,
            });
        }
        self.validate_control_target_in_cs(bus, pc, target, segment)?;
        if instruction.opcode == Opcode::Lcall {
            let final_sp = self.stack_pair_start(pc, AccessKind::Write, true)?;
            self.validate_stack_pair(bus, pc, final_sp, AccessKind::Write)?;
            let return_cs = self.state.segments.cs().raw();
            self.write_virtual(
                bus,
                pc,
                SegmentSelector::Ss,
                final_sp,
                AccessDomain::Current,
                Size::Quad,
                next_pc,
            )
            .map_err(|trap| page_fault_metadata(trap, Size::Quad, Some(0xff), false))?;
            self.write_virtual(
                bus,
                pc,
                SegmentSelector::Ss,
                final_sp + 8,
                AccessDomain::Current,
                Size::Quad,
                return_cs,
            )
            .map_err(|trap| page_fault_metadata(trap, Size::Quad, Some(0xff), false))?;
            self.state.sp = final_sp;
        }
        self.state.segments.set(SegmentSelector::Cs, segment);
        self.state.pc = target;
        Ok(StepResult::Running)
    }

    fn execute_extract<B: Bus>(
        &mut self,
        _bus: &mut B,
        _pc: u64,
        next_pc: u64,
        instruction: &DecodedInstruction,
    ) -> Result<StepResult, Trap> {
        let size = instruction_size(instruction);
        let width = (size.bytes() * 8) as u32;
        let offset = field(instruction, 'i') as u32;
        let high = self.read_r(field(instruction, 'h') as usize, size);
        let low = self.read_r(field(instruction, 'l') as usize, size);
        let result = if offset >= width * 2 {
            0
        } else {
            let concatenated = (u128::from(high) << width) | u128::from(low);
            (concatenated >> offset) as u64 & size_mask(size)
        };
        self.write_r(field(instruction, 'l') as usize, size, result);
        self.state.pc = next_pc;
        Ok(StepResult::Running)
    }

    fn execute_save_restore<B: Bus>(
        &mut self,
        bus: &mut B,
        pc: u64,
        next_pc: u64,
        instruction: &DecodedInstruction,
    ) -> Result<StepResult, Trap> {
        let ea = first_ea(instruction).ok_or(illegal_instruction(pc))?;
        let (segment, base) = self.address_operand_location(pc, instruction, ea)?;
        if base & 0xfff != 0 {
            return Err(Trap::InvalidControlState {
                pc,
                cause: InvalidControlCause::InvalidImage,
            });
        }
        const IMAGE_WORDS: usize = (crate::cpuid::SAVE_AREA_SIZE_BYTES / 8) as usize;
        const FIXED_WORDS: usize = (crate::cpuid::SAVE_FIXED_SIZE_BYTES / 8) as usize;
        const FP_START_WORD: usize = (crate::cpuid::SAVE_FP_OFFSET_BYTES / 8) as usize;
        const HEADER_ALLOWED: u64 = 0x000f_ffff_fff0_03ff;
        if instruction.opcode == Opcode::Save {
            self.validate_virtual_range(
                bus,
                pc,
                segment,
                base,
                crate::cpuid::SAVE_AREA_SIZE_BYTES,
                AccessKind::Write,
            )?;
            let mut image = [0_u64; IMAGE_WORDS];
            let fp_clean = self.state.f.iter().all(|&value| value == 0)
                && self.state.fflags == 0
                && self.state.fstatus == 0;
            image[0] = (u64::from(self.state.status.bits()) << 36)
                | (u64::from(self.state.flags.bits()) << 20)
                | (0x3f << 4);
            if !fp_clean {
                image[1] = 1 << crate::cpuid::SAVE_FP_BITMAP_BIT;
            }
            image[2..18].copy_from_slice(&self.state.r);
            for (index, selector) in [
                SegmentSelector::Gs0,
                SegmentSelector::Gs1,
                SegmentSelector::Gs2,
                SegmentSelector::Gs3,
                SegmentSelector::Gs4,
                SegmentSelector::Gs5,
            ]
            .into_iter()
            .enumerate()
            {
                image[18 + index] = self.state.segments.get(selector).raw();
            }
            for (index, value) in image[..FIXED_WORDS].iter().copied().enumerate() {
                self.write_virtual(
                    bus,
                    pc,
                    segment,
                    base + index as u64 * 8,
                    AccessDomain::Current,
                    Size::Quad,
                    value,
                )?;
            }
            if !fp_clean {
                image[FP_START_WORD..FP_START_WORD + 16].copy_from_slice(&self.state.f);
                image[FP_START_WORD + 16] = u64::from(self.state.fflags);
                image[FP_START_WORD + 17] = u64::from(self.state.fstatus);
                for (index, value) in image[FP_START_WORD..].iter().copied().enumerate() {
                    self.write_virtual(
                        bus,
                        pc,
                        segment,
                        base + crate::cpuid::SAVE_FP_OFFSET_BYTES as u64 + index as u64 * 8,
                        AccessDomain::Current,
                        Size::Quad,
                        value,
                    )?;
                }
            }
        } else {
            self.validate_virtual_range(
                bus,
                pc,
                segment,
                base,
                crate::cpuid::SAVE_AREA_SIZE_BYTES,
                AccessKind::Read,
            )?;
            let header =
                self.read_virtual(bus, pc, segment, base, AccessDomain::Current, Size::Quad)?;
            let bitmap = self.read_virtual(
                bus,
                pc,
                segment,
                base + 8,
                AccessDomain::Current,
                Size::Quad,
            )?;

            if header & !HEADER_ALLOWED != 0
                || bitmap & !(1 << crate::cpuid::SAVE_FP_BITMAP_BIT) != 0
            {
                return Err(Trap::InvalidControlState {
                    pc,
                    cause: InvalidControlCause::ReservedBits,
                });
            }
            if header & 0xf != u64::from(crate::cpuid::SAVE_FORMAT) {
                return Err(Trap::InvalidControlState {
                    pc,
                    cause: InvalidControlCause::InvalidImage,
                });
            }
            let flags_raw = ((header >> 20) & 0xffff) as u16;
            let Some(flags) = Flags::from_bits(flags_raw) else {
                return Err(Trap::InvalidControlState {
                    pc,
                    cause: InvalidControlCause::ReservedBits,
                });
            };
            let status_raw = ((header >> 36) & 0xffff) as u16;
            let supervisor = self.state.status.contains(Status::PM);
            if supervisor {
                let immutable = Status::EA | Status::PM;
                if status_raw & !Status::all().bits() != 0
                    || (status_raw & immutable.bits())
                        != (self.state.status.bits() & immutable.bits())
                {
                    return Err(Trap::InvalidControlState {
                        pc,
                        cause: InvalidControlCause::ReservedBits,
                    });
                }
            }

            let mut restored_r = [0_u64; 16];
            for (index, slot) in restored_r.iter_mut().enumerate() {
                *slot = self.read_virtual(
                    bus,
                    pc,
                    segment,
                    base + 0x10 + index as u64 * 8,
                    AccessDomain::Current,
                    Size::Quad,
                )?;
            }
            let gs_valid = ((header >> 4) & 0x3f) as u8;
            let selectors = [
                SegmentSelector::Gs0,
                SegmentSelector::Gs1,
                SegmentSelector::Gs2,
                SegmentSelector::Gs3,
                SegmentSelector::Gs4,
                SegmentSelector::Gs5,
            ];
            let mut gs_images = [crate::SegmentRegister::disabled(); 6];
            for (index, slot) in gs_images.iter_mut().enumerate() {
                if gs_valid & (1 << index) == 0 {
                    continue;
                }
                *slot = crate::SegmentRegister::from_raw(self.read_virtual(
                    bus,
                    pc,
                    segment,
                    base + 0x90 + index as u64 * 8,
                    AccessDomain::Current,
                    Size::Quad,
                )?);
                if !slot.valid() {
                    return Err(Trap::InvalidControlState {
                        pc,
                        cause: InvalidControlCause::InvalidImage,
                    });
                }
            }

            let fp_present = bitmap & (1 << crate::cpuid::SAVE_FP_BITMAP_BIT) != 0;
            let mut restored_f = [0_u64; 16];
            let mut restored_fflags = 0_u16;
            let mut restored_fstatus = 0_u16;
            if fp_present {
                let mut fp_image = [0_u64; IMAGE_WORDS - FP_START_WORD];
                for (index, slot) in fp_image.iter_mut().enumerate() {
                    *slot = self.read_virtual(
                        bus,
                        pc,
                        segment,
                        base + crate::cpuid::SAVE_FP_OFFSET_BYTES as u64 + index as u64 * 8,
                        AccessDomain::Current,
                        Size::Quad,
                    )?;
                }
                if fp_image[18..].iter().any(|&value| value != 0) {
                    return Err(Trap::InvalidControlState {
                        pc,
                        cause: InvalidControlCause::ReservedBits,
                    });
                }
                crate::fpu::env::FpCauses::from_bits(fp_image[16] as u16).map_err(|_| {
                    Trap::InvalidControlState {
                        pc,
                        cause: InvalidControlCause::ReservedBits,
                    }
                })?;
                crate::fpu::env::FpStatus::decode(fp_image[17] as u16).map_err(|_| {
                    Trap::InvalidControlState {
                        pc,
                        cause: InvalidControlCause::ReservedBits,
                    }
                })?;
                if fp_image[16] >> 16 != 0 || fp_image[17] >> 16 != 0 {
                    return Err(Trap::InvalidControlState {
                        pc,
                        cause: InvalidControlCause::ReservedBits,
                    });
                }
                restored_f.copy_from_slice(&fp_image[..16]);
                restored_fflags = fp_image[16] as u16;
                restored_fstatus = fp_image[17] as u16;
            }

            let mut candidate = self.state.clone();
            candidate.r = restored_r;
            candidate.flags = flags;
            if supervisor {
                candidate.status = Status::from_bits_retain(status_raw);
            }
            for (index, selector) in selectors.into_iter().enumerate() {
                if gs_valid & (1 << index) != 0 {
                    candidate.segments.set(selector, gs_images[index]);
                }
            }
            candidate.f = restored_f;
            candidate.fflags = restored_fflags;
            candidate.fstatus = restored_fstatus;
            candidate.pc = next_pc;
            self.state = candidate;
        }
        self.state.pc = next_pc;
        Ok(StepResult::Running)
    }

    fn execute_move<B: Bus>(
        &mut self,
        bus: &mut B,
        pc: u64,
        next_pc: u64,
        instruction: &DecodedInstruction,
    ) -> Result<StepResult, Trap> {
        let size = instruction_size(instruction);
        let id = instruction.allocation_id;
        if id.contains("rn_r_sp") {
            self.state.sp = self.state.r[field(instruction, 'r') as usize];
        } else if id.contains("sp_rn_r") {
            let register = field(instruction, 'r') as usize;
            self.write_r(register, size, self.state.sp);
        } else if instruction.allocation_id.contains("ea_s_ea_d") {
            let (source_domain, destination_domain) = match instruction.opcode {
                Opcode::Movuc => (AccessDomain::User, AccessDomain::Current),
                Opcode::Movcu => (AccessDomain::Current, AccessDomain::User),
                Opcode::Movuu => (AccessDomain::User, AccessDomain::User),
                _ => (AccessDomain::Current, AccessDomain::Current),
            };
            let value =
                self.read_ea_field_in_domain(bus, pc, instruction, 's', size, source_domain)?;
            self.write_ea_field_in_domain(
                bus,
                pc,
                instruction,
                'd',
                size,
                value,
                destination_domain,
            )?;
        } else if instruction.allocation_id.contains("rn_s_ea") {
            let src = field(instruction, 's') as usize;
            let dst = first_ea(instruction).ok_or(illegal_instruction(pc))?;
            let value = self.read_r(src, size);
            self.write_ea(bus, pc, instruction, dst, size, value)?;
        } else if instruction.allocation_id.contains("ea")
            && instruction.allocation_id.contains("rn_d")
        {
            let dst = field(instruction, 'd') as usize;
            let src = first_ea(instruction).ok_or(illegal_instruction(pc))?;
            let value = self.read_ea(bus, pc, instruction, src, size)?;
            self.write_r(dst, size, value);
        } else if let (Some(src), Some(dst)) = (
            optional_field(instruction, 's'),
            optional_field(instruction, 'd'),
        ) {
            if id.contains("rn_s_rn_d") {
                let value = self.read_r(src as usize, size);
                self.write_r(dst as usize, size, value);
            } else if id.contains("rn_s_ea") {
                let value = self.read_r(src as usize, size);
                let ea = ea_field(instruction, 'e')
                    .or_else(|| ea_field(instruction, 'd'))
                    .ok_or(illegal_instruction(pc))?;
                self.write_ea(bus, pc, instruction, ea, size, value)?;
            } else if id.contains("ea") && id.contains("rn_d") {
                let ea = ea_field(instruction, 'e')
                    .or_else(|| ea_field(instruction, 's'))
                    .ok_or(illegal_instruction(pc))?;
                let value = self.read_ea(bus, pc, instruction, ea, size)?;
                self.write_r(dst as usize, size, value);
            } else {
                return Err(illegal_instruction(pc));
            }
        } else {
            return Err(illegal_instruction(pc));
        }
        self.state.pc = next_pc;
        Ok(StepResult::Running)
    }

    fn execute_clear<B: Bus>(
        &mut self,
        bus: &mut B,
        pc: u64,
        next_pc: u64,
        instruction: &DecodedInstruction,
    ) -> Result<StepResult, Trap> {
        let size = instruction_size(instruction);
        if let Some(register) = optional_field(instruction, 'r') {
            self.write_r(register as usize, size, 0);
        } else if let Some(ea) = first_ea(instruction) {
            self.write_ea(bus, pc, instruction, ea, size, 0)?;
        } else {
            return Err(illegal_instruction(pc));
        }
        self.state.pc = next_pc;
        Ok(StepResult::Running)
    }

    fn execute_set<B: Bus>(
        &mut self,
        bus: &mut B,
        pc: u64,
        next_pc: u64,
        instruction: &DecodedInstruction,
    ) -> Result<StepResult, Trap> {
        let condition = optional_field(instruction, 'c').unwrap_or(0);
        let value = u64::from(self.state.flags.condition(condition as u8));
        let size = instruction_size(instruction);
        if let Some(register) = optional_field(instruction, 'r') {
            self.write_r(register as usize, size, value);
        } else if let Some(ea) = first_ea(instruction) {
            self.write_ea(bus, pc, instruction, ea, size, value)?;
        } else {
            return Err(illegal_instruction(pc));
        }
        self.state.pc = next_pc;
        Ok(StepResult::Running)
    }

    fn execute_binary<B: Bus>(
        &mut self,
        bus: &mut B,
        pc: u64,
        next_pc: u64,
        instruction: &DecodedInstruction,
        compare_only: bool,
    ) -> Result<StepResult, Trap> {
        let size = instruction_size(instruction);
        if instruction.allocation_id.ends_with("_sp")
            || matches!(
                instruction.form,
                FormId::MediumAddQEaSpN2 | FormId::MediumSubQEaSpN2
            )
        {
            let source = if instruction.allocation_id.contains("_8_sp") {
                8
            } else {
                optional_field(instruction, 'i')
                    .unwrap_or_else(|| signed_immediate(instruction) as u64)
            };
            let old = self.state.sp;
            self.state.sp = match instruction.opcode {
                Opcode::Add => old.wrapping_add(source),
                Opcode::Sub => old.wrapping_sub(source),
                _ => return Err(illegal_instruction(pc)),
            };
            self.state.pc = next_pc;
            return Ok(StepResult::Running);
        }
        let (src, dst, destination) = self.binary_operands(bus, pc, instruction, size)?;
        let result = match instruction.opcode {
            Opcode::Add => dst.wrapping_add(src),
            Opcode::Sub | Opcode::Cmp => dst.wrapping_sub(src),
            Opcode::And | Opcode::Test => dst & src,
            Opcode::Or => dst | src,
            Opcode::Xor => dst ^ src,
            _ => unreachable!(),
        } & size_mask(size);
        if compare_only {
            if instruction.opcode == Opcode::Cmp {
                self.set_sub_flags(size, dst, src, result);
            } else {
                self.set_logic_flags(size, result);
            }
        } else {
            self.write_destination(bus, pc, instruction, destination, size, result)?;
        }
        self.state.pc = next_pc;
        Ok(StepResult::Running)
    }

    fn execute_unary<B: Bus>(
        &mut self,
        bus: &mut B,
        pc: u64,
        next_pc: u64,
        instruction: &DecodedInstruction,
    ) -> Result<StepResult, Trap> {
        let size = instruction_size(instruction);
        let destination = if let Some(register) = optional_field(instruction, 'r') {
            Destination::Register(register as u8)
        } else if let Some(ea) = first_ea(instruction) {
            Destination::Ea(self.resolve_ea(pc, instruction, ea, size)?)
        } else {
            return Err(illegal_instruction(pc));
        };
        let old = self.read_destination(bus, pc, destination, size)?;
        let result = match instruction.opcode {
            Opcode::Inc | Opcode::Incf => old.wrapping_add(1),
            Opcode::Dec | Opcode::Decf => old.wrapping_sub(1),
            Opcode::Neg => 0u64.wrapping_sub(old),
            Opcode::Abs => {
                if old & sign_bit(size) != 0 {
                    0u64.wrapping_sub(old)
                } else {
                    old
                }
            }
            Opcode::Not => !old,
            _ => unreachable!(),
        } & size_mask(size);
        self.write_destination(bus, pc, instruction, destination, size, result)?;
        if matches!(instruction.opcode, Opcode::Incf | Opcode::Decf) {
            if instruction.opcode == Opcode::Incf {
                self.set_add_flags(size, old, 1, result);
            } else {
                self.set_sub_flags(size, old, 1, result);
            }
        }
        self.state.pc = next_pc;
        Ok(StepResult::Running)
    }

    fn execute_exchange<B: Bus>(
        &mut self,
        bus: &mut B,
        pc: u64,
        next_pc: u64,
        instruction: &DecodedInstruction,
    ) -> Result<StepResult, Trap> {
        let size = instruction_size(instruction);
        match (
            general_field(instruction, 's'),
            general_field(instruction, 'd'),
        ) {
            (Some(src_register), Some(dst_register)) => {
                let src_value = self.read_r(src_register, size);
                let dst_value = self.read_r(dst_register, size);
                self.write_r(src_register, size, dst_value);
                self.write_r(dst_register, size, src_value);
            }
            (Some(src_register), None) => {
                let src_value = self.read_r(src_register, size);
                let ea = first_ea(instruction).ok_or(illegal_instruction(pc))?;
                let destination = self.resolve_ea(pc, instruction, ea, size)?;
                let dst_value = self.read_resolved_ea(bus, pc, destination, size)?;
                self.write_r(src_register, size, dst_value);
                self.write_resolved_ea(bus, pc, instruction, destination, size, src_value)?;
            }
            (None, Some(dst_register)) => {
                let ea = first_ea(instruction).ok_or(illegal_instruction(pc))?;
                let source = self.resolve_ea(pc, instruction, ea, size)?;
                let src_value = self.read_resolved_ea(bus, pc, source, size)?;
                let dst_value = self.read_r(dst_register, size);
                self.write_resolved_ea(bus, pc, instruction, source, size, dst_value)?;
                self.write_r(dst_register, size, src_value);
            }
            (None, None) => return Err(illegal_instruction(pc)),
        }
        self.state.pc = next_pc;
        Ok(StepResult::Running)
    }

    fn execute_jump<B: Bus>(
        &mut self,
        bus: &mut B,
        pc: u64,
        next_pc: u64,
        instruction: &DecodedInstruction,
    ) -> Result<StepResult, Trap> {
        let condition = optional_field(instruction, 'c').unwrap_or(0) as u8;
        if self.state.flags.condition(condition) {
            let target = self.control_target(bus, pc, next_pc, instruction)?;
            self.validate_control_target(bus, pc, target)?;
            self.state.pc = target;
        } else {
            self.state.pc = next_pc;
        }
        Ok(StepResult::Running)
    }

    fn execute_push<B: Bus>(
        &mut self,
        bus: &mut B,
        pc: u64,
        next_pc: u64,
        instruction: &DecodedInstruction,
    ) -> Result<StepResult, Trap> {
        if instruction.opcode == Opcode::Pushp {
            let pair = optional_field(instruction, 'i').unwrap_or(0) as usize;
            let first = pair * 2;
            let final_sp = self.stack_pair_start(pc, AccessKind::Write, true)?;
            self.validate_stack_pair(bus, pc, final_sp, AccessKind::Write)?;
            let first_value = self.state.r[first];
            let second_value = self.state.r[first + 1];
            self.write_virtual(
                bus,
                pc,
                SegmentSelector::Ss,
                final_sp + 8,
                AccessDomain::Current,
                Size::Quad,
                first_value,
            )
            .map_err(|trap| page_fault_metadata(trap, Size::Quad, Some(0xff), false))?;
            self.write_virtual(
                bus,
                pc,
                SegmentSelector::Ss,
                final_sp,
                AccessDomain::Current,
                Size::Quad,
                second_value,
            )
            .map_err(|trap| page_fault_metadata(trap, Size::Quad, Some(0xff), false))?;
            self.state.sp = final_sp;
        } else if instruction.allocation_id.contains("push_cs") {
            self.push_quad(bus, pc, self.state.segments.cs().raw())?;
        } else if instruction.allocation_id.contains("push_sreg") {
            self.push_quad(
                bus,
                pc,
                self.state
                    .segments
                    .get(segment_selector(field(instruction, 's') as u8))
                    .raw(),
            )?;
        } else {
            let register =
                optional_field(instruction, 'r').ok_or(illegal_instruction(pc))? as usize;
            self.push_quad(bus, pc, self.state.r[register])?;
        }
        self.state.pc = next_pc;
        Ok(StepResult::Running)
    }

    fn execute_pop<B: Bus>(
        &mut self,
        bus: &mut B,
        pc: u64,
        next_pc: u64,
        instruction: &DecodedInstruction,
    ) -> Result<StepResult, Trap> {
        if instruction.opcode == Opcode::Popp {
            let pair = optional_field(instruction, 'i').unwrap_or(0) as usize;
            let first = pair * 2;
            let start = self.stack_pair_start(pc, AccessKind::Read, false)?;
            self.validate_stack_pair(bus, pc, start, AccessKind::Read)?;
            let second_value = self
                .read_virtual(
                    bus,
                    pc,
                    SegmentSelector::Ss,
                    start,
                    AccessDomain::Current,
                    Size::Quad,
                )
                .map_err(|trap| page_fault_metadata(trap, Size::Quad, Some(0xff), false))?;
            let first_value = self
                .read_virtual(
                    bus,
                    pc,
                    SegmentSelector::Ss,
                    start + 8,
                    AccessDomain::Current,
                    Size::Quad,
                )
                .map_err(|trap| page_fault_metadata(trap, Size::Quad, Some(0xff), false))?;
            self.state.r[first + 1] = second_value;
            self.state.r[first] = first_value;
            self.state.sp = start + 16;
        } else if instruction.allocation_id.contains("pop_sreg") {
            let value = self.pop_quad(bus, pc)?;
            let image = crate::SegmentRegister::from_raw(value);
            if !image.valid() {
                return Err(Trap::InvalidControlState {
                    pc,
                    cause: InvalidControlCause::InvalidImage,
                });
            }
            self.state
                .segments
                .set(segment_selector(field(instruction, 's') as u8), image);
        } else {
            let register =
                optional_field(instruction, 'r').ok_or(illegal_instruction(pc))? as usize;
            self.state.r[register] = self.pop_quad(bus, pc)?;
        }
        self.state.pc = next_pc;
        Ok(StepResult::Running)
    }

    fn execute_call<B: Bus>(
        &mut self,
        bus: &mut B,
        pc: u64,
        next_pc: u64,
        instruction: &DecodedInstruction,
    ) -> Result<StepResult, Trap> {
        let condition = optional_field(instruction, 'c').unwrap_or(0) as u8;
        if self.state.flags.condition(condition) {
            let target = self.control_target(bus, pc, next_pc, instruction)?;
            self.validate_control_target(bus, pc, target)?;
            self.push_quad(bus, pc, next_pc)?;
            self.state.pc = target;
        } else {
            self.state.pc = next_pc;
        }
        Ok(StepResult::Running)
    }

    fn execute_return<B: Bus>(&mut self, bus: &mut B, pc: u64) -> Result<StepResult, Trap> {
        let target = self.pop_quad(bus, pc)?;
        self.validate_control_target(bus, pc, target)?;
        self.state.pc = target;
        Ok(StepResult::Running)
    }

    fn control_target<B: Bus>(
        &mut self,
        bus: &mut B,
        pc: u64,
        next_pc: u64,
        instruction: &DecodedInstruction,
    ) -> Result<u64, Trap> {
        if let Some(ea) = first_ea(instruction) {
            let size = if matches!(instruction.opcode, Opcode::Jmp | Opcode::Jcc) {
                instruction_size(instruction)
            } else {
                Size::Quad
            };
            return Ok(self.read_ea(bus, pc, instruction, ea, size)? & size_mask(size));
        }
        Ok(next_pc.wrapping_add(signed_immediate(instruction) as u64))
    }

    fn validate_control_target<B: Bus>(
        &self,
        bus: &mut B,
        pc: u64,
        target: u64,
    ) -> Result<(), Trap> {
        self.translate_fetch(bus, target, pc).map(|_| ())
    }

    fn validate_control_target_in_cs<B: Bus>(
        &self,
        bus: &mut B,
        pc: u64,
        target: u64,
        cs: crate::SegmentRegister,
    ) -> Result<(), Trap> {
        let mut segments = self.state.segments;
        segments.set(SegmentSelector::Cs, cs);
        let translation = crate::MemoryTranslation {
            segments,
            ptcr: self.state.ptcr,
            ascr: self.state.ascr,
        };
        let linear = translation
            .segment_address(SegmentSelector::Cs, target)
            .map_err(|fault| {
                translation_trap_with_context(
                    pc,
                    fault,
                    target,
                    AccessKind::InstructionFetch,
                    AccessDomain::Current,
                    Some(SegmentSelector::Cs),
                    self.state.ascr.asid(),
                )
            })?;
        self.increment_page_walk(translation.ptcr);
        translation
            .page_address(
                bus,
                linear,
                AccessDomain::Current,
                AccessKind::InstructionFetch,
                self.state.status.contains(Status::PM),
                true,
            )
            .map(|_| ())
            .map_err(|error| match error {
                crate::translation::PageWalkError::Translation(fault) => {
                    translation_trap_with_context(
                        pc,
                        fault,
                        target,
                        AccessKind::InstructionFetch,
                        AccessDomain::Current,
                        Some(SegmentSelector::Cs),
                        self.state.ascr.asid(),
                    )
                }
                crate::translation::PageWalkError::Bus { error, level } => self.bus_access_trap(
                    pc,
                    error,
                    target,
                    Some(linear),
                    AccessKind::InstructionFetch,
                    AccessDomain::Current,
                    Some(SegmentSelector::Cs),
                    None,
                    Some(0xff),
                    false,
                    level,
                ),
            })
    }

    fn validate_ptcr_image(pc: u64, raw: u64) -> Result<crate::PageTableControl, Trap> {
        let image = crate::PageTableControl::from_raw(raw);
        if !image.reserved_bits_clear() {
            return Err(Trap::InvalidControlState {
                pc,
                cause: InvalidControlCause::ReservedBits,
            });
        }
        let Some(physical_address_bits) = image.physical_address_bits() else {
            return Err(Trap::InvalidControlState {
                pc,
                cause: InvalidControlCause::InvalidImage,
            });
        };
        if image.root_table_addr() >> physical_address_bits != 0 {
            return Err(Trap::InvalidControlState {
                pc,
                cause: InvalidControlCause::InvalidImage,
            });
        }
        Ok(image)
    }

    fn validate_ascr_image(pc: u64, raw: u64) -> Result<crate::AddressSpaceControl, Trap> {
        const ALLOWED: u64 = (0xffff << 16) | 1;
        if raw & !ALLOWED != 0 {
            return Err(Trap::InvalidControlState {
                pc,
                cause: InvalidControlCause::ReservedBits,
            });
        }
        Ok(crate::AddressSpaceControl::from_raw(raw))
    }

    fn validate_segment_image(pc: u64, raw: u64) -> Result<crate::SegmentRegister, Trap> {
        let image = crate::SegmentRegister::from_raw(raw);
        if !image.valid() {
            return Err(Trap::InvalidControlState {
                pc,
                cause: InvalidControlCause::InvalidImage,
            });
        }
        Ok(image)
    }

    fn validate_stack_top(pc: u64, value: u64) -> Result<(), Trap> {
        if value & 0x3f != 0 {
            return Err(Trap::InvalidControlState {
                pc,
                cause: InvalidControlCause::InvalidImage,
            });
        }
        Ok(())
    }

    fn decode_urctl(pc: u64, control: u64) -> Result<(Flags, Status), Trap> {
        if control & !URCTL_ALLOWED != 0 {
            return Err(Trap::InvalidControlState {
                pc,
                cause: InvalidControlCause::ReservedBits,
            });
        }
        let Some(flags) = Flags::from_bits(control as u16) else {
            return Err(Trap::InvalidControlState {
                pc,
                cause: InvalidControlCause::ReservedBits,
            });
        };
        let Some(status) = Status::from_bits((control >> 16) as u16) else {
            return Err(Trap::InvalidControlState {
                pc,
                cause: InvalidControlCause::ReservedBits,
            });
        };
        Ok((flags, status))
    }

    fn validate_user_return_bank<B: Bus>(
        &self,
        bus: &mut B,
        pc: u64,
        control: u64,
        decoded: (Flags, Status),
    ) -> Result<(), Trap> {
        self.validate_user_return_image(pc, control, decoded)?;
        self.validate_return_target_in_cs(bus, pc, self.state.urpc, self.state.urcs, false)?;
        self.validate_saved_stack_pointer(pc, self.state.ursp, self.state.urss)
    }

    fn validate_user_return_image(
        &self,
        pc: u64,
        control: u64,
        decoded: (Flags, Status),
    ) -> Result<(), Trap> {
        if control & URCTL_VALID == 0 {
            return Err(Trap::InvalidControlState {
                pc,
                cause: InvalidControlCause::InvalidTransition,
            });
        }
        if decoded.1.intersects(Status::PM | Status::EA)
            || !self.state.urcs.valid()
            || !self.state.urds.valid()
            || !self.state.urss.valid()
        {
            return Err(Trap::InvalidControlState {
                pc,
                cause: InvalidControlCause::InvalidImage,
            });
        }
        Ok(())
    }

    fn validate_return_target_in_cs<B: Bus>(
        &self,
        bus: &mut B,
        pc: u64,
        target: u64,
        cs: crate::SegmentRegister,
        privileged: bool,
    ) -> Result<(), Trap> {
        let mut candidate = self.clone();
        candidate.state.segments.set(SegmentSelector::Cs, cs);
        candidate.state.status.set(Status::PM, privileged);
        let before_walks = candidate.ptwalk_counter.get();
        let validation = candidate.translate_fetch(bus, target, pc);
        self.ptwalk_counter.set(
            self.ptwalk_counter
                .get()
                .wrapping_add(candidate.ptwalk_counter.get().wrapping_sub(before_walks)),
        );
        validation
            .map(|_| ())
            .map_err(|_| Trap::InvalidControlState {
                pc,
                cause: InvalidControlCause::InvalidImage,
            })
    }

    fn validate_saved_stack_pointer(
        &self,
        pc: u64,
        saved_sp: u64,
        saved_ss: crate::SegmentRegister,
    ) -> Result<(), Trap> {
        let mut segments = self.state.segments;
        segments.set(SegmentSelector::Ss, saved_ss);
        let translation = crate::MemoryTranslation {
            segments,
            ptcr: self.state.ptcr,
            ascr: self.state.ascr,
        };
        let linear = translation
            .segment_address(SegmentSelector::Ss, saved_sp)
            .map_err(|_| Trap::InvalidControlState {
                pc,
                cause: InvalidControlCause::InvalidImage,
            })?;
        translation
            .validate_linear_address(linear)
            .map_err(|_| Trap::InvalidControlState {
                pc,
                cause: InvalidControlCause::InvalidImage,
            })
    }

    fn fetch_decode_in_context<B: Bus>(
        &self,
        bus: &mut B,
        event_pc: u64,
        body_pc: u64,
        cs: crate::SegmentRegister,
        privileged: bool,
    ) -> Result<DecodedInstruction, Trap> {
        let mut candidate = self.clone();
        candidate.state.segments.set(SegmentSelector::Cs, cs);
        candidate.state.status.set(Status::PM, privileged);
        let before_walks = candidate.ptwalk_counter.get();
        let decoded = candidate.fetch_decode(bus, body_pc);
        self.ptwalk_counter.set(
            self.ptwalk_counter
                .get()
                .wrapping_add(candidate.ptwalk_counter.get().wrapping_sub(before_walks)),
        );
        decoded.map_err(|_| Trap::InvalidControlState {
            pc: event_pc,
            cause: InvalidControlCause::InvalidImage,
        })
    }

    fn validate_event_entry_target<B: Bus>(&self, bus: &mut B, pc: u64) -> Result<(), Trap> {
        let mut segments = self.state.segments;
        segments.set(SegmentSelector::Cs, self.state.ecs);
        let translation = crate::MemoryTranslation {
            segments,
            ptcr: self.state.ptcr,
            ascr: self.state.ascr,
        };
        let linear = translation
            .segment_address(SegmentSelector::Cs, self.state.epc)
            .map_err(|fault| translation_trap(pc, fault))?;
        self.increment_page_walk(translation.ptcr);
        translation
            .page_address(
                bus,
                linear,
                AccessDomain::Current,
                AccessKind::InstructionFetch,
                true,
                true,
            )
            .map(|_| ())
            .map_err(|error| page_walk_trap(pc, error))
    }

    fn validate_event_configuration<B: Bus>(&self, bus: &mut B, pc: u64) -> Result<(), Trap> {
        if !self.state.ecs.valid()
            || !self.state.eds.valid()
            || self.state.epc & 0x0f != 0
            || [
                (self.state.iss, self.state.isp),
                (self.state.fss, self.state.fsp),
                (self.state.dss, self.state.dsp),
            ]
            .into_iter()
            .any(|(segment, top)| !segment.valid() || top & 0x3f != 0)
        {
            return Err(Trap::InvalidControlState {
                pc,
                cause: InvalidControlCause::InvalidImage,
            });
        }
        self.validate_event_entry_target(bus, pc)
            .map_err(|_| Trap::InvalidControlState {
                pc,
                cause: InvalidControlCause::InvalidImage,
            })
    }

    fn event_frame_addresses<B: Bus>(
        &self,
        bus: &mut B,
        pc: u64,
        event_ss: crate::SegmentRegister,
        frame_base: u64,
        slots: u8,
    ) -> Result<Vec<u64>, Trap> {
        let mut segments = self.state.segments;
        segments.set(SegmentSelector::Ss, event_ss);
        let translation = crate::MemoryTranslation {
            segments,
            ptcr: self.state.ptcr,
            ascr: self.state.ascr,
        };
        let mut addresses = Vec::with_capacity(usize::from(slots));
        for slot in 0..slots {
            let offset =
                frame_base
                    .checked_add(u64::from(slot) * 8)
                    .ok_or(Trap::InvalidControlState {
                        pc,
                        cause: InvalidControlCause::InvalidImage,
                    })?;
            let linear = translation
                .segment_address(SegmentSelector::Ss, offset)
                .map_err(|fault| {
                    translation_trap_with_context(
                        pc,
                        fault,
                        offset,
                        AccessKind::Write,
                        AccessDomain::Current,
                        Some(SegmentSelector::Ss),
                        self.state.ascr.asid(),
                    )
                })?;
            self.increment_page_walk(translation.ptcr);
            let target = translation
                .page_address(
                    bus,
                    linear,
                    AccessDomain::Current,
                    AccessKind::Write,
                    true,
                    true,
                )
                .map_err(|error| match error {
                    crate::translation::PageWalkError::Translation(fault) => {
                        translation_trap_with_context(
                            pc,
                            fault,
                            offset,
                            AccessKind::Write,
                            AccessDomain::Current,
                            Some(SegmentSelector::Ss),
                            self.state.ascr.asid(),
                        )
                    }
                    crate::translation::PageWalkError::Bus { error, level } => self
                        .bus_access_trap(
                            pc,
                            error,
                            offset,
                            Some(linear),
                            AccessKind::Write,
                            AccessDomain::Current,
                            Some(SegmentSelector::Ss),
                            Some(size_code(Size::Quad)),
                            Some(0xff),
                            false,
                            level,
                        ),
                })?
                .target;
            let address = match target {
                crate::translation::TranslatedTarget::Byte(address) => address,
                crate::translation::TranslatedTarget::Slot(_) => {
                    return Err(translation_trap_with_context(
                        pc,
                        crate::TranslationFault::Page {
                            address: linear,
                            reason: crate::PageFaultReason::AddressType,
                        },
                        offset,
                        AccessKind::Write,
                        AccessDomain::Current,
                        Some(SegmentSelector::Ss),
                        self.state.ascr.asid(),
                    ));
                }
            };
            addresses.push(address);
        }
        Ok(addresses)
    }

    fn touch_address_operand<B: Bus>(
        &mut self,
        bus: &mut B,
        pc: u64,
        instruction: &DecodedInstruction,
        ea: CompactEa,
    ) -> Result<(), Trap> {
        let (segment, offset) = match ea {
            CompactEa::Register(register) => (SegmentSelector::Ds, self.state.r[register as usize]),
            CompactEa::StackPointer => (SegmentSelector::Ss, self.state.sp),
            CompactEa::Immediate(width) => (
                SegmentSelector::Ds,
                read_signed(ea_payload(instruction, ea), width) as u64,
            ),
            _ => self.effective_location_with_payload(
                pc,
                ea,
                ea_payload(instruction, ea),
                Size::Quad,
            )?,
        };
        self.translate(
            bus,
            offset,
            segment,
            AccessDomain::Current,
            AccessKind::Read,
            pc,
            true,
        )
        .map(|_| ())
    }

    fn touch_prefetch_address<B: Bus>(
        &mut self,
        bus: &mut B,
        pc: u64,
        instruction: &DecodedInstruction,
        ea: CompactEa,
    ) -> Result<(), Trap> {
        let (segment, offset) = self.address_operand_location(pc, instruction, ea)?;
        // Hints compute their address and apply EA auto-update, but disabled
        // prefetch faults are architecturally suppressed in this machine model.
        let _ = self.translate(
            bus,
            offset,
            segment,
            AccessDomain::Current,
            AccessKind::Read,
            pc,
            true,
        );
        Ok(())
    }

    fn address_operand_location(
        &mut self,
        pc: u64,
        instruction: &DecodedInstruction,
        ea: CompactEa,
    ) -> Result<(SegmentSelector, u64), Trap> {
        match ea {
            CompactEa::Register(register) => {
                Ok((SegmentSelector::Ds, self.state.r[register as usize]))
            }
            CompactEa::StackPointer => Ok((SegmentSelector::Ss, self.state.sp)),
            CompactEa::Immediate(width) => Ok((
                SegmentSelector::Ds,
                read_signed(ea_payload(instruction, ea), width) as u64,
            )),
            _ => self.effective_location_with_payload(
                pc,
                ea,
                ea_payload(instruction, ea),
                Size::Quad,
            ),
        }
    }

    fn binary_operands<B: Bus>(
        &mut self,
        bus: &mut B,
        pc: u64,
        instruction: &DecodedInstruction,
        size: Size,
    ) -> Result<(u64, u64, Destination), Trap> {
        let id = instruction.allocation_id;
        if id.contains("ea_s_ea_d") {
            let src = self.read_ea_field(bus, pc, instruction, 's', size)?;
            let destination = self.resolve_ea_field(pc, instruction, 'd', size)?;
            let dst = self.read_resolved_ea(bus, pc, destination, size)?;
            return Ok((src, dst, Destination::Ea(destination)));
        }
        if id.contains("rn_s_rn_d") {
            let src = field(instruction, 's') as usize;
            let dst = field(instruction, 'd') as usize;
            return Ok((
                self.read_r(src, size),
                self.read_r(dst, size),
                Destination::Register(dst as u8),
            ));
        }
        if instruction.form == FormId::LongAdcXEaERnS {
            let dst = general_field(instruction, 's').ok_or(illegal_instruction(pc))?;
            return Ok((
                self.read_ea_field(bus, pc, instruction, 'e', size)?,
                self.read_r(dst, size),
                Destination::Register(dst as u8),
            ));
        }
        if id.contains("rn_s_ea") {
            let src = field(instruction, 's') as usize;
            let ea = first_ea(instruction).ok_or(illegal_instruction(pc))?;
            let src = self.read_r(src, size);
            let destination = self.resolve_ea(pc, instruction, ea, size)?;
            let dst = self.read_resolved_ea(bus, pc, destination, size)?;
            return Ok((src, dst, Destination::Ea(destination)));
        }
        if id.contains("ea") && id.contains("rn_d") {
            let dst = field(instruction, 'd') as usize;
            let ea = first_ea(instruction).ok_or(illegal_instruction(pc))?;
            return Ok((
                self.read_ea(bus, pc, instruction, ea, size)?,
                self.read_r(dst, size),
                Destination::Register(dst as u8),
            ));
        }
        if id.contains("imm") {
            if let Some(ea) = first_ea(instruction) {
                let immediate = binary_immediate(instruction);
                let destination = self.resolve_ea(pc, instruction, ea, size)?;
                let dst = self.read_resolved_ea(bus, pc, destination, size)?;
                return Ok((immediate, dst, Destination::Ea(destination)));
            }
            let dst = optional_field(instruction, 'd')
                .or_else(|| optional_field(instruction, 'r'))
                .ok_or(illegal_instruction(pc))? as usize;
            let immediate =
                optional_field(instruction, 'i').unwrap_or_else(|| binary_immediate(instruction));
            return Ok((
                immediate,
                self.read_r(dst, size),
                Destination::Register(dst as u8),
            ));
        }
        Err(illegal_instruction(pc))
    }

    fn read_destination<B: Bus>(
        &self,
        bus: &mut B,
        pc: u64,
        destination: Destination,
        size: Size,
    ) -> Result<u64, Trap> {
        match destination {
            Destination::Register(r) => Ok(self.read_r(r as usize, size)),
            Destination::Ea(ea) => self.read_resolved_ea(bus, pc, ea, size),
        }
    }

    fn write_destination<B: Bus>(
        &mut self,
        bus: &mut B,
        pc: u64,
        instruction: &DecodedInstruction,
        destination: Destination,
        size: Size,
        value: u64,
    ) -> Result<(), Trap> {
        match destination {
            Destination::Register(r) => {
                self.write_r(r as usize, size, value);
                Ok(())
            }
            Destination::Ea(ea) => self.write_resolved_ea(bus, pc, instruction, ea, size, value),
        }
    }

    fn resolve_ea(
        &mut self,
        pc: u64,
        instruction: &DecodedInstruction,
        ea: CompactEa,
        size: Size,
    ) -> Result<ResolvedEa, Trap> {
        self.resolve_ea_with_payload(
            pc,
            instruction,
            ea,
            ea_payload(instruction, ea),
            None,
            ea_operand_ordinal(instruction, ea),
            size,
        )
    }

    fn resolve_ea_field(
        &mut self,
        pc: u64,
        instruction: &DecodedInstruction,
        symbol: char,
        size: Size,
    ) -> Result<ResolvedEa, Trap> {
        let ea = ea_field(instruction, symbol).ok_or(illegal_instruction(pc))?;
        self.resolve_ea_with_payload(
            pc,
            instruction,
            ea,
            ea_payload_for_symbol(instruction, symbol),
            Some(symbol),
            ea_field_ordinal(instruction, symbol),
            size,
        )
    }

    #[allow(clippy::too_many_arguments)]
    fn resolve_ea_with_payload(
        &mut self,
        pc: u64,
        _instruction: &DecodedInstruction,
        ea: CompactEa,
        payload: &[u8],
        symbol: Option<char>,
        operand: u8,
        size: Size,
    ) -> Result<ResolvedEa, Trap> {
        let target = match ea {
            CompactEa::Register(register) => ResolvedEaTarget::Register(register),
            CompactEa::StackPointer => ResolvedEaTarget::StackPointer,
            CompactEa::Immediate(width) => {
                ResolvedEaTarget::Immediate((read_signed(payload, width) as u64) & size_mask(size))
            }
            _ => {
                let (segment, offset) = self
                    .effective_location_with_payload(pc, ea, payload, size)
                    .map_err(|trap| page_fault_metadata(trap, size, Some(operand), false))?;
                ResolvedEaTarget::Memory { segment, offset }
            }
        };
        Ok(ResolvedEa {
            ea,
            symbol,
            operand,
            target,
        })
    }

    fn read_resolved_ea<B: Bus>(
        &self,
        bus: &mut B,
        pc: u64,
        resolved: ResolvedEa,
        size: Size,
    ) -> Result<u64, Trap> {
        match resolved.target {
            ResolvedEaTarget::Register(register) => Ok(self.read_r(register as usize, size)),
            ResolvedEaTarget::StackPointer => Ok(self.state.sp & size_mask(size)),
            ResolvedEaTarget::Immediate(value) => Ok(value),
            ResolvedEaTarget::Memory { segment, offset } => self
                .read_virtual(bus, pc, segment, offset, AccessDomain::Current, size)
                .map_err(|trap| page_fault_metadata(trap, size, Some(resolved.operand), false)),
        }
    }

    fn write_resolved_ea<B: Bus>(
        &mut self,
        bus: &mut B,
        pc: u64,
        instruction: &DecodedInstruction,
        resolved: ResolvedEa,
        size: Size,
        value: u64,
    ) -> Result<(), Trap> {
        match resolved.target {
            ResolvedEaTarget::Register(register) => {
                self.write_r(register as usize, size, value);
            }
            ResolvedEaTarget::StackPointer => write_subfield(&mut self.state.sp, size, value),
            ResolvedEaTarget::Immediate(_) => return Err(illegal_instruction(pc)),
            ResolvedEaTarget::Memory { segment, offset } => self
                .write_virtual(bus, pc, segment, offset, AccessDomain::Current, size, value)
                .map_err(|trap| page_fault_metadata(trap, size, Some(resolved.operand), false))?,
        }
        self.capture_repeat_ea_result(instruction, resolved.symbol, resolved.ea, value);
        Ok(())
    }

    fn read_ea_field<B: Bus>(
        &mut self,
        bus: &mut B,
        pc: u64,
        instruction: &DecodedInstruction,
        symbol: char,
        size: Size,
    ) -> Result<u64, Trap> {
        self.read_ea_field_in_domain(bus, pc, instruction, symbol, size, AccessDomain::Current)
    }

    fn read_ea_field_in_domain<B: Bus>(
        &mut self,
        bus: &mut B,
        pc: u64,
        instruction: &DecodedInstruction,
        symbol: char,
        size: Size,
        domain: AccessDomain,
    ) -> Result<u64, Trap> {
        let ea = ea_field(instruction, symbol).ok_or(illegal_instruction(pc))?;
        self.read_ea_with_payload_in_domain(
            bus,
            pc,
            instruction,
            ea,
            ea_payload_for_symbol(instruction, symbol),
            size,
            domain,
        )
        .map_err(|trap| {
            page_fault_metadata(
                trap,
                size,
                Some(ea_field_ordinal(instruction, symbol)),
                false,
            )
        })
    }

    fn write_ea_field<B: Bus>(
        &mut self,
        bus: &mut B,
        pc: u64,
        instruction: &DecodedInstruction,
        symbol: char,
        size: Size,
        value: u64,
    ) -> Result<(), Trap> {
        self.write_ea_field_in_domain(
            bus,
            pc,
            instruction,
            symbol,
            size,
            value,
            AccessDomain::Current,
        )
    }

    #[allow(clippy::too_many_arguments)]
    fn write_ea_field_in_domain<B: Bus>(
        &mut self,
        bus: &mut B,
        pc: u64,
        instruction: &DecodedInstruction,
        symbol: char,
        size: Size,
        value: u64,
        domain: AccessDomain,
    ) -> Result<(), Trap> {
        let ea = ea_field(instruction, symbol).ok_or(illegal_instruction(pc))?;
        self.write_ea_with_payload_in_domain(
            bus,
            pc,
            instruction,
            ea,
            ea_payload_for_symbol(instruction, symbol),
            size,
            value,
            domain,
        )
        .map_err(|trap| {
            page_fault_metadata(
                trap,
                size,
                Some(ea_field_ordinal(instruction, symbol)),
                false,
            )
        })?;
        self.capture_repeat_ea_result(instruction, Some(symbol), ea, value);
        Ok(())
    }

    fn read_ea<B: Bus>(
        &mut self,
        bus: &mut B,
        pc: u64,
        instruction: &DecodedInstruction,
        ea: CompactEa,
        size: Size,
    ) -> Result<u64, Trap> {
        let operand = ea_operand_ordinal(instruction, ea);
        self.read_ea_with_payload_in_domain(
            bus,
            pc,
            instruction,
            ea,
            ea_payload(instruction, ea),
            size,
            AccessDomain::Current,
        )
        .map_err(|trap| page_fault_metadata(trap, size, Some(operand), false))
    }

    #[allow(clippy::too_many_arguments)]
    fn read_ea_with_payload_in_domain<B: Bus>(
        &mut self,
        bus: &mut B,
        pc: u64,
        _instruction: &DecodedInstruction,
        ea: CompactEa,
        payload: &[u8],
        size: Size,
        domain: AccessDomain,
    ) -> Result<u64, Trap> {
        match ea {
            CompactEa::Register(register) => Ok(self.read_r(register as usize, size)),
            CompactEa::StackPointer => Ok(self.state.sp & size_mask(size)),
            CompactEa::Immediate(width) => {
                Ok((read_signed(payload, width) as u64) & size_mask(size))
            }
            _ => {
                let (segment, offset) =
                    self.effective_location_with_payload(pc, ea, payload, size)?;
                self.read_virtual(bus, pc, segment, offset, domain, size)
            }
        }
    }
    fn write_ea<B: Bus>(
        &mut self,
        bus: &mut B,
        pc: u64,
        instruction: &DecodedInstruction,
        ea: CompactEa,
        size: Size,
        value: u64,
    ) -> Result<(), Trap> {
        let operand = ea_operand_ordinal(instruction, ea);
        self.write_ea_with_payload_in_domain(
            bus,
            pc,
            instruction,
            ea,
            ea_payload(instruction, ea),
            size,
            value,
            AccessDomain::Current,
        )
        .map_err(|trap| page_fault_metadata(trap, size, Some(operand), false))?;
        self.capture_repeat_ea_result(instruction, None, ea, value);
        Ok(())
    }

    #[allow(clippy::too_many_arguments)]
    fn write_ea_with_payload_in_domain<B: Bus>(
        &mut self,
        bus: &mut B,
        pc: u64,
        _instruction: &DecodedInstruction,
        ea: CompactEa,
        payload: &[u8],
        size: Size,
        value: u64,
        domain: AccessDomain,
    ) -> Result<(), Trap> {
        match ea {
            CompactEa::Register(register) => {
                self.write_r(register as usize, size, value);
                Ok(())
            }
            CompactEa::StackPointer => {
                write_subfield(&mut self.state.sp, size, value);
                Ok(())
            }
            CompactEa::Immediate(_) => Err(illegal_instruction(pc)),
            _ => {
                let (segment, offset) =
                    self.effective_location_with_payload(pc, ea, payload, size)?;
                self.write_virtual(bus, pc, segment, offset, domain, size, value)
            }
        }
    }

    fn effective_linear_address(
        &self,
        segment: SegmentSelector,
        offset: u64,
        pc: u64,
    ) -> Result<u64, Trap> {
        let translation = crate::MemoryTranslation {
            segments: self.state.segments,
            ptcr: self.state.ptcr,
            ascr: self.state.ascr,
        };
        translation
            .segment_address(segment, offset)
            .map_err(|fault| translation_trap(pc, fault))
    }

    fn effective_location_with_payload(
        &mut self,
        pc: u64,
        ea: CompactEa,
        payload: &[u8],
        interpretation_size: Size,
    ) -> Result<(SegmentSelector, u64), Trap> {
        let (segment, offset) = match ea {
            CompactEa::RegisterIndirect(r) => (SegmentSelector::Ds, self.state.r[r as usize]),
            CompactEa::RegisterDisplacement { register, width } => (
                SegmentSelector::Ds,
                self.state.r[register as usize].wrapping_add(read_signed(payload, width) as u64),
            ),
            CompactEa::StackDisplacement(width) => (
                SegmentSelector::Ss,
                self.state
                    .sp
                    .wrapping_add(read_signed(payload, width) as u64),
            ),
            CompactEa::ProgramCounterDisplacement(width) => (
                SegmentSelector::Cs,
                pc.wrapping_add(read_signed(payload, width) as u64),
            ),
            CompactEa::StackIndirect => (SegmentSelector::Ss, self.state.sp),
            CompactEa::Absolute32 => (
                SegmentSelector::Ds,
                (read_unsigned(payload, 4) as u32 as i32 as i64) as u64,
            ),
            CompactEa::Absolute64 => (SegmentSelector::Ds, read_unsigned(payload, 8)),
            CompactEa::Ext0 { displacement } => {
                let (descriptor, descriptor_bytes) =
                    Ext0Descriptor::decode(payload).ok_or(illegal_instruction(pc))?;
                let first = if descriptor_bytes == 1 {
                    descriptor.raw as u8
                } else {
                    (descriptor.raw >> 8) as u8
                };
                let access_size = interpretation_size.bytes() as u64;

                let segment = if let Some(segment) = descriptor.segment {
                    segment_selector(segment)
                } else if first == 0x8a {
                    SegmentSelector::Ss
                } else if first == 0x8b {
                    SegmentSelector::Cs
                } else {
                    SegmentSelector::Ds
                };

                let mut base = if first == 0x8a {
                    self.state.sp
                } else if first == 0x8b {
                    pc
                } else {
                    descriptor
                        .base
                        .map_or(0, |register| self.state.r[register as usize])
                };
                if descriptor.base_update == AutoUpdate::PreDecrement {
                    base = base.wrapping_sub(access_size);
                    if let Some(register) = descriptor.base {
                        self.state.r[register as usize] = base;
                    }
                } else if descriptor.base_update == AutoUpdate::PostIncrement
                    && let Some(register) = descriptor.base
                {
                    self.state.r[register as usize] = base.wrapping_add(access_size);
                }

                let mut index = descriptor
                    .index
                    .map_or(0, |register| self.state.r[register as usize]);
                if descriptor.index_update == AutoUpdate::PreDecrement {
                    index = index.wrapping_sub(1);
                    if let Some(register) = descriptor.index {
                        self.state.r[register as usize] = index;
                    }
                } else if descriptor.index_update == AutoUpdate::PostIncrement
                    && let Some(register) = descriptor.index
                {
                    self.state.r[register as usize] = index.wrapping_add(1);
                }

                let displacement = displacement.map_or(0, |width| {
                    read_signed(&payload[descriptor_bytes..], width) as u64
                });
                let offset = base
                    .wrapping_add(index.wrapping_mul(access_size))
                    .wrapping_add(displacement);

                (segment, offset)
            }
            _ => return Err(illegal_instruction(pc)),
        };
        Ok((segment, offset))
    }

    fn read_r(&self, register: usize, size: Size) -> u64 {
        self.state.r[register] & size_mask(size)
    }
    fn write_r(&mut self, register: usize, size: Size, value: u64) {
        write_subfield(&mut self.state.r[register], size, value);
    }
    fn push_quad<B: Bus>(&mut self, bus: &mut B, pc: u64, value: u64) -> Result<(), Trap> {
        let new_sp = self.state.sp.checked_sub(8).ok_or_else(|| {
            page_fault_metadata(
                range_overflow_trap(
                    pc,
                    self.state.sp,
                    SegmentSelector::Ss,
                    AccessDomain::Current,
                    AccessKind::Write,
                    self.state.ascr.asid(),
                ),
                Size::Quad,
                Some(0xff),
                false,
            )
        })?;
        self.write_virtual(
            bus,
            pc,
            SegmentSelector::Ss,
            new_sp,
            AccessDomain::Current,
            Size::Quad,
            value,
        )
        .map_err(|trap| page_fault_metadata(trap, Size::Quad, Some(0xff), false))?;
        self.state.sp = new_sp;
        Ok(())
    }
    fn pop_quad<B: Bus>(&mut self, bus: &mut B, pc: u64) -> Result<u64, Trap> {
        let value = self
            .read_virtual(
                bus,
                pc,
                SegmentSelector::Ss,
                self.state.sp,
                AccessDomain::Current,
                Size::Quad,
            )
            .map_err(|trap| page_fault_metadata(trap, Size::Quad, Some(0xff), false))?;
        self.state.sp = self.state.sp.wrapping_add(8);
        Ok(value)
    }

    fn stack_pair_start(&self, pc: u64, kind: AccessKind, descending: bool) -> Result<u64, Trap> {
        let start = if descending {
            self.state.sp.checked_sub(16)
        } else {
            self.state.sp.checked_add(16).map(|_| self.state.sp)
        };
        start.ok_or_else(|| {
            page_fault_metadata(
                range_overflow_trap(
                    pc,
                    self.state.sp,
                    SegmentSelector::Ss,
                    AccessDomain::Current,
                    kind,
                    self.state.ascr.asid(),
                ),
                Size::Quad,
                Some(0xff),
                false,
            )
        })
    }

    fn validate_stack_pair<B: Bus>(
        &self,
        bus: &mut B,
        pc: u64,
        start: u64,
        kind: AccessKind,
    ) -> Result<(), Trap> {
        for offset in [start, start + 8] {
            self.validate_virtual_access(
                bus,
                pc,
                SegmentSelector::Ss,
                offset,
                AccessDomain::Current,
                Size::Quad,
                kind,
            )
            .map_err(|trap| page_fault_metadata(trap, Size::Quad, Some(0xff), false))?;
        }
        Ok(())
    }

    #[allow(clippy::too_many_arguments)]
    fn validate_virtual_access<B: Bus>(
        &self,
        bus: &mut B,
        pc: u64,
        segment: SegmentSelector,
        offset: u64,
        domain: AccessDomain,
        size: Size,
        kind: AccessKind,
    ) -> Result<(), Trap> {
        let byte_count = size.bytes() as u64;
        let first = self.translate(bus, offset, segment, domain, kind, pc, true)?;
        if matches!(first.target, crate::TranslatedTarget::Slot(_)) {
            return Ok(());
        }
        if byte_count == 1 {
            return Ok(());
        }
        let last_offset = offset.checked_add(byte_count - 1).ok_or_else(|| {
            range_overflow_trap(pc, offset, segment, domain, kind, self.state.ascr.asid())
        })?;
        let last = self.translate(bus, last_offset, segment, domain, kind, pc, true)?;
        self.require_byte_target(last, pc, offset, segment, domain, kind)?;
        Ok(())
    }

    fn validate_virtual_range<B: Bus>(
        &self,
        bus: &mut B,
        pc: u64,
        segment: SegmentSelector,
        offset: u64,
        byte_count: u64,
        kind: AccessKind,
    ) -> Result<(), Trap> {
        if byte_count == 0 {
            return Ok(());
        }
        let first = self.translate(bus, offset, segment, AccessDomain::Current, kind, pc, true)?;
        self.require_byte_target(first, pc, offset, segment, AccessDomain::Current, kind)?;
        let last_offset = offset.checked_add(byte_count - 1).ok_or_else(|| {
            range_overflow_trap(
                pc,
                offset,
                segment,
                AccessDomain::Current,
                kind,
                self.state.ascr.asid(),
            )
        })?;
        let last = self.translate(
            bus,
            last_offset,
            segment,
            AccessDomain::Current,
            kind,
            pc,
            true,
        )?;
        self.require_byte_target(last, pc, offset, segment, AccessDomain::Current, kind)?;
        Ok(())
    }

    fn aggregate_retry_safety(
        &self,
        mut failure: AcknowledgedBusFailure,
    ) -> AcknowledgedBusFailure {
        if self.successful_slot_transaction.get() && failure.retry_safety == RetrySafety::RetrySafe
        {
            failure.retry_safety = RetrySafety::EffectMayHaveOccurred;
        }
        failure
    }

    fn normalize_architectural_bus_trap(&self, trap: Trap) -> Trap {
        match trap {
            Trap::AcknowledgedBusFailure { pc, mut context } => {
                context.failure = self.aggregate_retry_safety(context.failure);
                Trap::AcknowledgedBusFailure { pc, context }
            }
            Trap::Bus { pc, error } => {
                let Some(failure) = raw_bus_failure(&error) else {
                    return Trap::Bus { pc, error };
                };
                let failure = self.aggregate_retry_safety(failure);
                Trap::AcknowledgedBusFailure {
                    pc,
                    context: crate::BusFaultContext {
                        failure,
                        // Callers that know the architectural operand replace
                        // this fallback with `bus_access_trap`. The remaining
                        // legacy paths still retain the final bus address.
                        effective_address: failure.final_address,
                        linear_address: None,
                        access_kind: AccessKind::Read,
                        access_domain: AccessDomain::Current,
                        segment: None,
                        asid: self.state.ascr.asid(),
                        access_size: None,
                        operand: None,
                        atomic: false,
                        walk_level: 0,
                    },
                }
            }
            trap => trap,
        }
    }

    #[allow(clippy::too_many_arguments)]
    fn bus_access_trap(
        &self,
        pc: u64,
        error: BusError,
        effective_address: u64,
        linear_address: Option<u64>,
        access_kind: AccessKind,
        access_domain: AccessDomain,
        segment: Option<SegmentSelector>,
        access_size: Option<u8>,
        operand: Option<u8>,
        atomic: bool,
        walk_level: u8,
    ) -> Trap {
        let Some(failure) = raw_bus_failure(&error) else {
            return Trap::Bus { pc, error };
        };
        Trap::AcknowledgedBusFailure {
            pc,
            context: crate::BusFaultContext {
                failure: self.aggregate_retry_safety(failure),
                effective_address,
                linear_address,
                access_kind,
                access_domain,
                segment,
                asid: self.state.ascr.asid(),
                access_size,
                operand,
                atomic,
                walk_level,
            },
        }
    }

    #[allow(clippy::too_many_arguments)]
    fn slot_access_transaction_trap(
        &self,
        pc: u64,
        error: SlotTransactionError,
        effective_address: u64,
        linear_address: u64,
        access_kind: AccessKind,
        access_domain: AccessDomain,
        segment: SegmentSelector,
        access_size: u8,
    ) -> Trap {
        match error {
            SlotTransactionError::Bus(error) => self.bus_access_trap(
                pc,
                error,
                effective_address,
                Some(linear_address),
                access_kind,
                access_domain,
                Some(segment),
                Some(access_size),
                None,
                false,
                0,
            ),
            error => Trap::SlotTransaction { pc, error },
        }
    }

    fn read_virtual<B: Bus>(
        &self,
        bus: &mut B,
        pc: u64,
        segment: SegmentSelector,
        offset: u64,
        domain: AccessDomain,
        size: Size,
    ) -> Result<u64, Trap> {
        let byte_count = size.bytes() as u64;
        let first = self.translate(bus, offset, segment, domain, AccessKind::Read, pc, true)?;
        let first_linear = first.linear;
        let first_address = match first.target {
            crate::TranslatedTarget::Slot(address) => {
                return self.read_slot(
                    bus,
                    pc,
                    segment,
                    offset,
                    first.linear,
                    domain,
                    size,
                    address,
                );
            }
            crate::TranslatedTarget::Byte(address) => address,
        };
        if byte_count == 1 {
            return bus.read_u8(first_address).map(u64::from).map_err(|error| {
                self.bus_access_trap(
                    pc,
                    error,
                    offset,
                    Some(first_linear),
                    AccessKind::Read,
                    domain,
                    Some(segment),
                    Some(size_code(size)),
                    None,
                    false,
                    0,
                )
            });
        }
        let last_offset = offset.checked_add(byte_count - 1).ok_or_else(|| {
            range_overflow_trap(
                pc,
                offset,
                segment,
                domain,
                AccessKind::Read,
                self.state.ascr.asid(),
            )
        })?;
        let last = self.translate(
            bus,
            last_offset,
            segment,
            domain,
            AccessKind::Read,
            pc,
            true,
        )?;
        let last_address =
            self.require_byte_target(last, pc, offset, segment, domain, AccessKind::Read)?;
        if first_address.checked_add(byte_count - 1) == Some(last_address) {
            return read_bus(bus, first_address, size).map_err(|error| {
                self.bus_access_trap(
                    pc,
                    error,
                    offset,
                    Some(first_linear),
                    AccessKind::Read,
                    domain,
                    Some(segment),
                    Some(size_code(size)),
                    None,
                    false,
                    0,
                )
            });
        }
        let mut value = 0u64;
        for index in 0..byte_count {
            let resolved = self.translate(
                bus,
                offset
                    .checked_add(index)
                    .expect("validated virtual read range"),
                segment,
                domain,
                AccessKind::Read,
                pc,
                true,
            )?;
            let physical =
                self.require_byte_target(resolved, pc, offset, segment, domain, AccessKind::Read)?;
            value |= u64::from(bus.read_u8(physical).map_err(|error| {
                self.bus_access_trap(
                    pc,
                    error,
                    offset,
                    Some(first_linear),
                    AccessKind::Read,
                    domain,
                    Some(segment),
                    Some(size_code(size)),
                    None,
                    false,
                    0,
                )
            })?) << (index * 8);
        }
        Ok(value)
    }
    #[allow(clippy::too_many_arguments)]
    fn write_virtual<B: Bus>(
        &self,
        bus: &mut B,
        pc: u64,
        segment: SegmentSelector,
        offset: u64,
        domain: AccessDomain,
        size: Size,
        value: u64,
    ) -> Result<(), Trap> {
        let byte_count = size.bytes() as u64;
        let first = self.translate(bus, offset, segment, domain, AccessKind::Write, pc, true)?;
        let first_linear = first.linear;
        let first_address = match first.target {
            crate::TranslatedTarget::Slot(address) => {
                return self.write_slot(
                    bus,
                    pc,
                    segment,
                    offset,
                    first.linear,
                    domain,
                    size,
                    address,
                    value,
                );
            }
            crate::TranslatedTarget::Byte(address) => address,
        };
        if byte_count == 1 {
            return bus.write_u8(first_address, value as u8).map_err(|error| {
                self.bus_access_trap(
                    pc,
                    error,
                    offset,
                    Some(first_linear),
                    AccessKind::Write,
                    domain,
                    Some(segment),
                    Some(size_code(size)),
                    None,
                    false,
                    0,
                )
            });
        }
        let last_offset = offset.checked_add(byte_count - 1).ok_or_else(|| {
            range_overflow_trap(
                pc,
                offset,
                segment,
                domain,
                AccessKind::Write,
                self.state.ascr.asid(),
            )
        })?;
        let last = self.translate(
            bus,
            last_offset,
            segment,
            domain,
            AccessKind::Write,
            pc,
            true,
        )?;
        let last_address =
            self.require_byte_target(last, pc, offset, segment, domain, AccessKind::Write)?;
        if first_address.checked_add(byte_count - 1) == Some(last_address) {
            return write_bus(bus, first_address, size, value).map_err(|error| {
                self.bus_access_trap(
                    pc,
                    error,
                    offset,
                    Some(first_linear),
                    AccessKind::Write,
                    domain,
                    Some(segment),
                    Some(size_code(size)),
                    None,
                    false,
                    0,
                )
            });
        }
        for index in 0..byte_count {
            let resolved = self.translate(
                bus,
                offset
                    .checked_add(index)
                    .expect("validated virtual write range"),
                segment,
                domain,
                AccessKind::Write,
                pc,
                true,
            )?;
            let physical =
                self.require_byte_target(resolved, pc, offset, segment, domain, AccessKind::Write)?;
            bus.write_u8(physical, (value >> (index * 8)) as u8)
                .map_err(|error| {
                    self.bus_access_trap(
                        pc,
                        error,
                        offset,
                        Some(first_linear),
                        AccessKind::Write,
                        domain,
                        Some(segment),
                        Some(size_code(size)),
                        None,
                        false,
                        0,
                    )
                })?;
        }
        Ok(())
    }

    #[allow(clippy::too_many_arguments)]
    fn read_slot<B: Bus>(
        &self,
        bus: &mut B,
        pc: u64,
        segment: SegmentSelector,
        effective_address: u64,
        linear_address: u64,
        domain: AccessDomain,
        size: Size,
        slot_address: u64,
    ) -> Result<u64, Trap> {
        let request = SlotRequest::read(slot_address, slot_width(size));
        let acknowledgement = bus
            .slot_transaction(request)
            .map_err(|error| {
                self.slot_access_transaction_trap(
                    pc,
                    error,
                    effective_address,
                    linear_address,
                    AccessKind::Read,
                    domain,
                    segment,
                    size_code(size),
                )
            })?
            .validate_for(request)
            .map_err(|error| {
                self.slot_access_transaction_trap(
                    pc,
                    error,
                    effective_address,
                    linear_address,
                    AccessKind::Read,
                    domain,
                    segment,
                    size_code(size),
                )
            })?;
        match acknowledgement.outcome() {
            SlotOutcome::Read(data) => {
                self.successful_slot_transaction.set(true);
                Ok(data.as_u64())
            }
            SlotOutcome::Failed(failure) => Err(Trap::AcknowledgedBusFailure {
                pc,
                context: crate::BusFaultContext {
                    failure: self.aggregate_retry_safety(failure),
                    effective_address,
                    linear_address: Some(linear_address),
                    access_kind: AccessKind::Read,
                    access_domain: domain,
                    segment: Some(segment),
                    asid: self.state.ascr.asid(),
                    access_size: Some(size_code(size)),
                    operand: None,
                    atomic: false,
                    walk_level: 0,
                },
            }),
            SlotOutcome::Write => Err(slot_transaction_trap(
                pc,
                SlotTransactionError::Protocol {
                    addr: slot_address,
                    error: SlotProtocolError::DirectionMismatch,
                },
            )),
        }
    }

    #[allow(clippy::too_many_arguments)]
    fn write_slot<B: Bus>(
        &self,
        bus: &mut B,
        pc: u64,
        segment: SegmentSelector,
        effective_address: u64,
        linear_address: u64,
        domain: AccessDomain,
        size: Size,
        slot_address: u64,
        value: u64,
    ) -> Result<(), Trap> {
        let request = SlotRequest::write(slot_address, slot_data(size, value));
        let acknowledgement = bus
            .slot_transaction(request)
            .map_err(|error| {
                self.slot_access_transaction_trap(
                    pc,
                    error,
                    effective_address,
                    linear_address,
                    AccessKind::Write,
                    domain,
                    segment,
                    size_code(size),
                )
            })?
            .validate_for(request)
            .map_err(|error| {
                self.slot_access_transaction_trap(
                    pc,
                    error,
                    effective_address,
                    linear_address,
                    AccessKind::Write,
                    domain,
                    segment,
                    size_code(size),
                )
            })?;
        match acknowledgement.outcome() {
            SlotOutcome::Write => {
                self.successful_slot_transaction.set(true);
                Ok(())
            }
            SlotOutcome::Failed(failure) => Err(Trap::AcknowledgedBusFailure {
                pc,
                context: crate::BusFaultContext {
                    failure: self.aggregate_retry_safety(failure),
                    effective_address,
                    linear_address: Some(linear_address),
                    access_kind: AccessKind::Write,
                    access_domain: domain,
                    segment: Some(segment),
                    asid: self.state.ascr.asid(),
                    access_size: Some(size_code(size)),
                    operand: None,
                    atomic: false,
                    walk_level: 0,
                },
            }),
            SlotOutcome::Read(_) => Err(slot_transaction_trap(
                pc,
                SlotTransactionError::Protocol {
                    addr: slot_address,
                    error: SlotProtocolError::DirectionMismatch,
                },
            )),
        }
    }

    #[allow(clippy::too_many_arguments)]
    fn require_byte_target(
        &self,
        resolved: ResolvedAddress,
        pc: u64,
        effective_address: u64,
        segment: SegmentSelector,
        domain: AccessDomain,
        kind: AccessKind,
    ) -> Result<u64, Trap> {
        match resolved.target {
            crate::TranslatedTarget::Byte(address) => Ok(address),
            crate::TranslatedTarget::Slot(_) => Err(translation_trap_with_context(
                pc,
                crate::TranslationFault::Page {
                    address: resolved.linear,
                    reason: crate::PageFaultReason::AddressType,
                },
                effective_address,
                kind,
                domain,
                Some(segment),
                self.state.ascr.asid(),
            )),
        }
    }
    #[allow(clippy::too_many_arguments)]
    fn translate<B: Bus>(
        &self,
        bus: &mut B,
        offset: u64,
        segment: SegmentSelector,
        domain: AccessDomain,
        kind: AccessKind,
        pc: u64,
        update_accessed_dirty: bool,
    ) -> Result<ResolvedAddress, Trap> {
        let translation = crate::MemoryTranslation {
            segments: self.state.segments,
            ptcr: self.state.ptcr,
            ascr: self.state.ascr,
        };
        let linear = translation
            .segment_address(segment, offset)
            .map_err(|fault| {
                translation_trap_with_context(
                    pc,
                    fault,
                    offset,
                    kind,
                    domain,
                    Some(segment),
                    self.state.ascr.asid(),
                )
            })?;
        self.increment_page_walk(translation.ptcr);
        let target = translation
            .page_address(
                bus,
                linear,
                domain,
                kind,
                self.state.status.contains(Status::PM),
                update_accessed_dirty,
            )
            .map_err(|error| match error {
                crate::translation::PageWalkError::Translation(fault) => {
                    translation_trap_with_context(
                        pc,
                        fault,
                        offset,
                        kind,
                        domain,
                        Some(segment),
                        self.state.ascr.asid(),
                    )
                }
                crate::translation::PageWalkError::Bus { error, level } => self.bus_access_trap(
                    pc,
                    error,
                    offset,
                    Some(linear),
                    kind,
                    domain,
                    Some(segment),
                    None,
                    (kind == AccessKind::InstructionFetch).then_some(0xff),
                    false,
                    level,
                ),
            })?
            .target;
        Ok(ResolvedAddress { linear, target })
    }
    fn translate_fetch<B: Bus>(&self, bus: &mut B, offset: u64, pc: u64) -> Result<u64, Trap> {
        let resolved = self.translate(
            bus,
            offset,
            SegmentSelector::Cs,
            AccessDomain::Current,
            AccessKind::InstructionFetch,
            pc,
            true,
        )?;
        self.require_byte_target(
            resolved,
            pc,
            offset,
            SegmentSelector::Cs,
            AccessDomain::Current,
            AccessKind::InstructionFetch,
        )
    }

    fn fetch_bus_trap(&self, pc: u64, effective_address: u64, error: BusError) -> Trap {
        let translation = crate::MemoryTranslation {
            segments: self.state.segments,
            ptcr: self.state.ptcr,
            ascr: self.state.ascr,
        };
        let linear_address = translation
            .segment_address(SegmentSelector::Cs, effective_address)
            .ok();
        self.bus_access_trap(
            pc,
            error,
            effective_address,
            linear_address,
            AccessKind::InstructionFetch,
            AccessDomain::Current,
            Some(SegmentSelector::Cs),
            None,
            Some(0xff),
            false,
            0,
        )
    }
    fn checked_fetch_offset(&self, pc: u64, delta: u64) -> Result<u64, Trap> {
        pc.checked_add(delta).ok_or_else(|| {
            range_overflow_trap(
                pc,
                pc,
                SegmentSelector::Cs,
                AccessDomain::Current,
                AccessKind::InstructionFetch,
                self.state.ascr.asid(),
            )
        })
    }
    fn set_logic_flags(&mut self, size: Size, result: u64) {
        self.state
            .flags
            .set(Flags::Z, result & size_mask(size) == 0);
        self.state.flags.set(Flags::N, result & sign_bit(size) != 0);
        self.state.flags.remove(Flags::C | Flags::V);
    }
    fn set_add_flags(&mut self, size: Size, lhs: u64, rhs: u64, result: u64) {
        self.set_logic_flags(size, result);
        let mask = size_mask(size);
        self.state
            .flags
            .set(Flags::C, (lhs & mask) > mask.wrapping_sub(rhs & mask));
        self.state.flags.set(
            Flags::V,
            (!(lhs ^ rhs) & (lhs ^ result) & sign_bit(size)) != 0,
        );
    }
    fn set_sub_flags(&mut self, size: Size, lhs: u64, rhs: u64, result: u64) {
        self.set_logic_flags(size, result);
        self.state
            .flags
            .set(Flags::C, (lhs & size_mask(size)) < (rhs & size_mask(size)));
        self.state.flags.set(
            Flags::V,
            ((lhs ^ rhs) & (lhs ^ result) & sign_bit(size)) != 0,
        );
    }
}

#[derive(Debug, Clone, Copy)]
enum Destination {
    Register(u8),
    Ea(ResolvedEa),
}

#[derive(Debug, Clone, Copy)]
struct ResolvedEa {
    ea: CompactEa,
    symbol: Option<char>,
    operand: u8,
    target: ResolvedEaTarget,
}

#[derive(Debug, Clone, Copy)]
enum ResolvedEaTarget {
    Register(u8),
    StackPointer,
    Immediate(u64),
    Memory {
        segment: SegmentSelector,
        offset: u64,
    },
}

#[derive(Debug, Clone, Copy)]
struct ResolvedMemoryDestination {
    segment: SegmentSelector,
    offset: u64,
    operand: u8,
}

#[derive(Debug, Clone, Copy)]
enum FpuDestination {
    None,
    General(usize),
    Floating(usize),
    FloatingPair(usize, usize),
    Memory(ResolvedMemoryDestination),
}

fn illegal_instruction(pc: u64) -> Trap {
    Trap::IllegalInstruction {
        pc,
        cause: IllegalInstructionCause::ReservedEncoding,
    }
}

fn event_request_from_trap(trap: &Trap) -> Option<EventRequest> {
    match trap {
        Trap::Decode { pc, error } => {
            let cause = match error {
                bedrock_isa::DecodeError::Reserved => 0,
                bedrock_isa::DecodeError::ReservedEffectiveAddress(_) => 1,
                bedrock_isa::DecodeError::Header(_)
                | bedrock_isa::DecodeError::Truncated { .. }
                | bedrock_isa::DecodeError::OperandPayload { .. } => 5,
            };
            Some(EventRequest::exception(
                BaseException::IllegalInstruction,
                *pc,
                cause,
            ))
        }
        Trap::IllegalInstruction { pc, cause } => Some(EventRequest::exception(
            BaseException::IllegalInstruction,
            *pc,
            *cause as u64,
        )),
        Trap::PrivilegeFault { pc } => Some(EventRequest::exception(
            BaseException::PrivilegeFault,
            *pc,
            0,
        )),
        Trap::DivideError { pc, cause } => Some(EventRequest::exception(
            BaseException::DivideError,
            *pc,
            *cause as u64,
        )),
        Trap::InvalidControlState { pc, cause } => Some(EventRequest::exception(
            BaseException::InvalidControlState,
            *pc,
            *cause as u64,
        )),
        Trap::FloatingPointFault { pc, causes } => {
            Some(EventRequest::floating_point_fault(*pc, *causes))
        }
        Trap::PageFault { pc, context } => Some(EventRequest {
            code: EventCode::exception(BaseException::PageFault),
            saved_pc: *pc,
            error_code: page_fault_error_code(*context),
            fault_ea: context.effective_address,
            fault_linear: context.linear_address.unwrap_or(0),
            event_aux: 0,
        }),
        Trap::AcknowledgedBusFailure { pc, context } => Some(EventRequest {
            code: EventCode::exception(BaseException::BusError),
            saved_pc: *pc,
            error_code: bus_fault_error_code(*context),
            fault_ea: context.effective_address,
            fault_linear: context.linear_address.unwrap_or(0),
            event_aux: context.failure.final_address,
        }),
        Trap::Bus { .. } | Trap::SlotTransaction { .. } => None,
    }
}

fn translation_trap(pc: u64, fault: crate::TranslationFault) -> Trap {
    let effective_address = match fault {
        crate::TranslationFault::NonCanonical { address }
        | crate::TranslationFault::Page { address, .. } => address,
    };
    translation_trap_with_context(
        pc,
        fault,
        effective_address,
        AccessKind::Read,
        AccessDomain::Current,
        None,
        0,
    )
}

#[allow(clippy::too_many_arguments)]
fn translation_trap_with_context(
    pc: u64,
    fault: crate::TranslationFault,
    effective_address: u64,
    access_kind: AccessKind,
    access_domain: AccessDomain,
    segment: Option<SegmentSelector>,
    asid: u16,
) -> Trap {
    match fault {
        crate::TranslationFault::NonCanonical { address } => Trap::PageFault {
            pc,
            context: crate::PageFaultContext {
                effective_address,
                linear_address: Some(address),
                reason: crate::PageFaultReason::NonCanonical,
                access_kind,
                access_domain,
                segment,
                asid,
                access_size: None,
                operand: (access_kind == AccessKind::InstructionFetch).then_some(0xff),
                atomic: false,
            },
        },
        crate::TranslationFault::Page { address, reason } => Trap::PageFault {
            pc,
            context: crate::PageFaultContext {
                effective_address,
                linear_address: (reason != crate::PageFaultReason::SegmentBounds)
                    .then_some(address),
                reason,
                access_kind,
                access_domain,
                segment,
                asid,
                access_size: None,
                operand: (access_kind == AccessKind::InstructionFetch).then_some(0xff),
                atomic: false,
            },
        },
    }
}

fn page_fault_error_code(context: crate::PageFaultContext) -> u64 {
    let mut code = u64::from(context.reason.code());
    code |= match context.access_kind {
        AccessKind::Read => 1 << 8,
        AccessKind::Write => 2 << 8,
        AccessKind::InstructionFetch => 3 << 8,
    };
    if context.access_domain == AccessDomain::User {
        code |= 1 << 10;
    }
    if context.atomic {
        code |= 1 << 11;
    }
    if let Some(operand) = context.operand {
        code |= u64::from(operand) << 16;
    }
    code |= 1 << 24;
    if context.linear_address.is_some() {
        code |= 1 << 25;
    }
    if let Some(size) = context.access_size {
        code |= u64::from(size) << 27;
    }
    code
}

fn bus_fault_error_code(context: crate::BusFaultContext) -> u64 {
    let mut code = context.failure.cause as u64;
    code |= match context.access_kind {
        AccessKind::Read => 1 << 8,
        AccessKind::Write => 2 << 8,
        AccessKind::InstructionFetch => 3 << 8,
    };
    if context.access_domain == AccessDomain::User {
        code |= 1 << 10;
    }
    if context.atomic {
        code |= 1 << 11;
    }
    code |= u64::from(context.walk_level) << 12;
    code |= u64::from(context.operand.unwrap_or(0xff)) << 16;
    code |= 1 << 24;
    if context.linear_address.is_some() {
        code |= 1 << 25;
    }
    code |= 1 << 26;
    if let Some(size) = context.access_size {
        code |= u64::from(size) << 27;
    }
    if context.failure.retry_safety == bedrock_bus::RetrySafety::RetrySafe {
        code |= 1 << 30;
    }
    code
}

fn range_overflow_trap(
    pc: u64,
    effective_address: u64,
    segment: SegmentSelector,
    domain: AccessDomain,
    kind: AccessKind,
    asid: u16,
) -> Trap {
    translation_trap_with_context(
        pc,
        crate::TranslationFault::Page {
            address: effective_address,
            reason: crate::PageFaultReason::SegmentBounds,
        },
        effective_address,
        kind,
        domain,
        Some(segment),
        asid,
    )
}

fn atomic_page_fault(
    pc: u64,
    effective_address: u64,
    linear_address: Option<u64>,
    reason: crate::PageFaultReason,
    size: Size,
    segment: SegmentSelector,
    asid: u16,
) -> Trap {
    Trap::PageFault {
        pc,
        context: crate::PageFaultContext {
            effective_address,
            linear_address,
            reason,
            access_kind: AccessKind::Write,
            access_domain: AccessDomain::Current,
            segment: Some(segment),
            asid,
            access_size: Some(match size {
                Size::Byte => 1,
                Size::Word => 2,
                Size::Long => 3,
                Size::Quad => 4,
            }),
            operand: Some(0),
            atomic: true,
        },
    }
}

fn atomic_walk_trap(
    pc: u64,
    error: crate::translation::PageWalkError,
    effective_address: u64,
    segment: SegmentSelector,
    size: Size,
    asid: u16,
) -> Trap {
    match error {
        crate::translation::PageWalkError::Bus { error, level } => {
            let Some(failure) = raw_bus_failure(&error) else {
                return Trap::Bus { pc, error };
            };
            Trap::AcknowledgedBusFailure {
                pc,
                context: crate::BusFaultContext {
                    failure,
                    effective_address,
                    linear_address: None,
                    access_kind: AccessKind::Write,
                    access_domain: AccessDomain::Current,
                    segment: Some(segment),
                    asid,
                    access_size: Some(size_code(size)),
                    operand: Some(0),
                    atomic: true,
                    walk_level: level,
                },
            }
        }
        crate::translation::PageWalkError::Translation(fault) => {
            let mut trap = translation_trap_with_context(
                pc,
                fault,
                effective_address,
                AccessKind::Write,
                AccessDomain::Current,
                Some(segment),
                asid,
            );
            if let Trap::PageFault { context, .. } = &mut trap {
                context.atomic = true;
                context.operand = Some(0);
                context.access_size = Some(match size {
                    Size::Byte => 1,
                    Size::Word => 2,
                    Size::Long => 3,
                    Size::Quad => 4,
                });
            }
            trap
        }
    }
}

fn page_fault_metadata(mut trap: Trap, size: Size, operand: Option<u8>, atomic: bool) -> Trap {
    match &mut trap {
        Trap::PageFault { context, .. } => {
            context.access_size = Some(size_code(size));
            context.operand = operand;
            context.atomic |= atomic;
        }
        Trap::AcknowledgedBusFailure { context, .. } => {
            context.access_size = Some(size_code(size));
            context.operand = operand;
            context.atomic |= atomic;
        }
        _ => {}
    }
    trap
}

fn ea_field_ordinal(instruction: &DecodedInstruction, symbol: char) -> u8 {
    GENERATED_FORMS
        .iter()
        .find(|form| form.form == instruction.form)
        .and_then(|form| form.ea_fields.iter().find(|field| field.symbol == symbol))
        .map(|field| field.syntax_operand_ordinal)
        .unwrap_or(0)
}

fn ea_operand_ordinal(instruction: &DecodedInstruction, ea: CompactEa) -> u8 {
    instruction
        .fields
        .iter()
        .find(|field| field.kind == FieldKind::Ea7 && CompactEa::decode(field.value as u8) == ea)
        .map(|field| ea_field_ordinal(instruction, field.symbol))
        .unwrap_or(0)
}

fn page_walk_trap(pc: u64, error: crate::translation::PageWalkError) -> Trap {
    match error {
        crate::translation::PageWalkError::Translation(fault) => translation_trap(pc, fault),
        crate::translation::PageWalkError::Bus { error, .. } => Trap::Bus { pc, error },
    }
}

fn optional_field(instruction: &DecodedInstruction, symbol: char) -> Option<u64> {
    instruction
        .fields
        .iter()
        .find(|field| field.symbol == symbol)
        .map(|field| field.value)
}
fn segment_selector(value: u8) -> SegmentSelector {
    match value & 7 {
        0 => SegmentSelector::Ds,
        1 => SegmentSelector::Ss,
        2 => SegmentSelector::Gs0,
        3 => SegmentSelector::Gs1,
        4 => SegmentSelector::Gs2,
        5 => SegmentSelector::Gs3,
        6 => SegmentSelector::Gs4,
        _ => SegmentSelector::Gs5,
    }
}
fn is_repeat_forbidden(instruction: &DecodedInstruction) -> bool {
    matches!(
        instruction.opcode,
        Opcode::Repcc
            | Opcode::Repg
            | Opcode::Jmp
            | Opcode::Jcc
            | Opcode::Call
            | Opcode::Callcc
            | Opcode::Ret
            | Opcode::Lret
            | Opcode::Eret
            | Opcode::Syscall
            | Opcode::Sysret
            | Opcode::Halt
            | Opcode::Bkpt
    )
}
fn field(instruction: &DecodedInstruction, symbol: char) -> u64 {
    optional_field(instruction, symbol).expect("allocated form field")
}
fn ea_field(instruction: &DecodedInstruction, symbol: char) -> Option<CompactEa> {
    instruction
        .fields
        .iter()
        .find(|field| field.symbol == symbol && field.kind == FieldKind::Ea7)
        .map(|field| CompactEa::decode(field.value as u8))
}
fn general_field(instruction: &DecodedInstruction, symbol: char) -> Option<usize> {
    instruction
        .fields
        .iter()
        .find(|field| field.symbol == symbol && field.kind == FieldKind::Rn)
        .map(|field| field.value as usize)
}
fn fpu_field(instruction: &DecodedInstruction, symbol: char) -> Option<usize> {
    instruction
        .fields
        .iter()
        .find(|field| field.symbol == symbol && field.kind == FieldKind::Freg)
        .map(|field| field.value as usize)
}
fn first_ea(instruction: &DecodedInstruction) -> Option<CompactEa> {
    instruction
        .fields
        .iter()
        .find(|field| field.kind == FieldKind::Ea7)
        .map(|field| CompactEa::decode(field.value as u8))
}

fn instruction_size(instruction: &DecodedInstruction) -> Size {
    let selector = optional_field(instruction, 'z')
        .or_else(|| {
            optional_field(instruction, 's').filter(|_| {
                instruction
                    .fields
                    .iter()
                    .any(|field| field.symbol == 's' && field.kind == FieldKind::Size)
            })
        })
        .unwrap_or(0) as u8;
    let text = instruction.form_text;
    if text.contains("BWLQ(z)") || text.contains("z:B/W/L/Q") {
        return [Size::Byte, Size::Word, Size::Long, Size::Quad][selector as usize & 3];
    }
    if text.contains("LQ(z)") || text.contains("z:L/Q") {
        return if selector & 1 == 0 {
            Size::Long
        } else {
            Size::Quad
        };
    }
    if text.contains("BW(z)") || text.contains("z:B/W") {
        return if selector & 1 == 0 {
            Size::Byte
        } else {
            Size::Word
        };
    }
    if text.contains("WL(z)") || text.contains("z:W/L") {
        return if selector & 1 == 0 {
            Size::Word
        } else {
            Size::Long
        };
    }
    if text.contains(".B") {
        Size::Byte
    } else if text.contains(".W") {
        Size::Word
    } else if text.contains(".L") {
        Size::Long
    } else {
        Size::Quad
    }
}
fn fpu_size(instruction: &DecodedInstruction) -> Size {
    if optional_field(instruction, 'z').unwrap_or(1) & 1 == 0 {
        Size::Long
    } else {
        Size::Quad
    }
}
fn fp_format(size: Size) -> crate::fpu::format::FpFormat {
    match size {
        Size::Long => crate::fpu::format::FpFormat::S,
        Size::Quad => crate::fpu::format::FpFormat::D,
        _ => unreachable!("floating-point operations use only S or D"),
    }
}
fn size_mask(size: Size) -> u64 {
    match size {
        Size::Byte => 0xff,
        Size::Word => 0xffff,
        Size::Long => 0xffff_ffff,
        Size::Quad => u64::MAX,
    }
}
fn logical_repeat_flags(value: u64, size: Size) -> Flags {
    let value = value & size_mask(size);
    let mut flags = Flags::empty();
    flags.set(Flags::Z, value == 0);
    flags.set(Flags::N, value & (1_u64 << (size.bytes() * 8 - 1)) != 0);
    flags
}
const fn size_code(size: Size) -> u8 {
    match size {
        Size::Byte => 1,
        Size::Word => 2,
        Size::Long => 3,
        Size::Quad => 4,
    }
}
const fn slot_width(size: Size) -> SlotWidth {
    match size {
        Size::Byte => SlotWidth::B,
        Size::Word => SlotWidth::W,
        Size::Long => SlotWidth::L,
        Size::Quad => SlotWidth::Q,
    }
}
const fn slot_data(size: Size, value: u64) -> SlotData {
    match size {
        Size::Byte => SlotData::B(value as u8),
        Size::Word => SlotData::W(value as u16),
        Size::Long => SlotData::L(value as u32),
        Size::Quad => SlotData::Q(value),
    }
}

fn raw_bus_failure(error: &BusError) -> Option<AcknowledgedBusFailure> {
    let (cause, final_address) = match error {
        BusError::OutOfRange { addr } | BusError::Unmapped { addr } => {
            (BusFailureCause::NoResponder, *addr)
        }
        BusError::ReadOnly { addr } => (BusFailureCause::AccessDenied, *addr),
        BusError::InvalidRange { start, .. } => (BusFailureCause::Other, *start),
        BusError::Device { addr, .. } => (BusFailureCause::Other, *addr),
        BusError::TransactionActive | BusError::NoTransaction => return None,
    };
    Some(AcknowledgedBusFailure::new(
        cause,
        final_address,
        RetrySafety::RetrySafe,
    ))
}

fn slot_transaction_trap(pc: u64, error: SlotTransactionError) -> Trap {
    match error {
        SlotTransactionError::Bus(error) => Trap::Bus { pc, error },
        error => Trap::SlotTransaction { pc, error },
    }
}
fn sign_bit(size: Size) -> u64 {
    1 << (size.bytes() * 8 - 1)
}
fn logic_flags(size: Size, result: u64) -> Flags {
    let mut flags = Flags::empty();
    flags.set(Flags::Z, result & size_mask(size) == 0);
    flags.set(Flags::N, result & sign_bit(size) != 0);
    flags
}
fn sub_flags(size: Size, lhs: u64, rhs: u64, result: u64) -> Flags {
    let mut flags = logic_flags(size, result);
    flags.set(Flags::C, (lhs & size_mask(size)) < (rhs & size_mask(size)));
    flags.set(
        Flags::V,
        ((lhs ^ rhs) & (lhs ^ result) & sign_bit(size)) != 0,
    );
    flags
}
fn sign_extend(value: u64, size: Size) -> i64 {
    let shift = 64 - size.bytes() * 8;
    ((value << shift) as i64) >> shift
}
fn signed_min(size: Size) -> i64 {
    match size {
        Size::Byte => i8::MIN as i64,
        Size::Word => i16::MIN as i64,
        Size::Long => i32::MIN as i64,
        Size::Quad => i64::MIN,
    }
}
fn rotate_left_width(value: u64, count: u32, width: u32) -> u64 {
    if width == 64 {
        value.rotate_left(count)
    } else {
        ((value << count) | (value >> (width - count))) & ((1u64 << width) - 1)
    }
}
fn rotate_right_width(value: u64, count: u32, width: u32) -> u64 {
    if width == 64 {
        value.rotate_right(count)
    } else {
        ((value >> count) | (value << (width - count))) & ((1u64 << width) - 1)
    }
}
fn high_product_unsigned(lhs: u64, rhs: u64, width: usize) -> u64 {
    let mask = if width == 64 {
        u64::MAX
    } else {
        (1u64 << width) - 1
    };
    (((u128::from(lhs & mask) * u128::from(rhs & mask)) >> width) as u64) & mask
}
fn high_product_signed(lhs: u64, rhs: u64, width: usize) -> u64 {
    let size = match width {
        8 => Size::Byte,
        16 => Size::Word,
        32 => Size::Long,
        _ => Size::Quad,
    };
    ((i128::from(sign_extend(lhs, size)) * i128::from(sign_extend(rhs, size))) >> width) as u64
}
fn high_product_signed_unsigned(lhs: u64, rhs: u64, width: usize) -> u64 {
    let size = match width {
        8 => Size::Byte,
        16 => Size::Word,
        32 => Size::Long,
        _ => Size::Quad,
    };
    ((i128::from(sign_extend(lhs, size)) * i128::from(rhs & size_mask(size))) >> width) as u64
}
fn carryless_product(lhs: u64, rhs: u64) -> (u64, u64) {
    let mut result = 0u128;
    for bit in 0..64 {
        if rhs & (1u64 << bit) != 0 {
            result ^= u128::from(lhs) << bit;
        }
    }
    (result as u64, (result >> 64) as u64)
}
fn carryless_product_high(lhs: u64, rhs: u64, width: usize) -> u64 {
    let mask = if width == 64 {
        u64::MAX
    } else {
        (1_u64 << width) - 1
    };
    let lhs = lhs & mask;
    let rhs = rhs & mask;
    let mut result = 0_u128;
    for bit in 0..width {
        if rhs & (1_u64 << bit) != 0 {
            result ^= u128::from(lhs) << bit;
        }
    }
    ((result >> width) as u64) & mask
}
fn write_subfield(target: &mut u64, size: Size, value: u64) {
    let mask = size_mask(size);
    *target = (*target & !mask) | (value & mask);
}
fn trailing_bytes(instruction: &DecodedInstruction) -> &[u8] {
    &instruction.bytes[usize::from(instruction.header.opcode_bytes)..]
}
fn ea_payload(instruction: &DecodedInstruction, target: CompactEa) -> &[u8] {
    let payload = trailing_bytes(instruction);
    let mut cursor = 0;
    for field in instruction
        .fields
        .iter()
        .filter(|field| field.kind == FieldKind::Ea7)
    {
        let ea = CompactEa::decode(field.value as u8);
        if ea == target {
            return payload.get(cursor..).unwrap_or_default();
        }
        cursor += ea_payload_len(ea, payload.get(cursor..).unwrap_or_default());
    }
    payload
}
fn ea_payload_for_symbol(instruction: &DecodedInstruction, target: char) -> &[u8] {
    let payload = trailing_bytes(instruction);
    let mut cursor = 0;
    for field in instruction
        .fields
        .iter()
        .filter(|field| field.kind == FieldKind::Ea7)
    {
        if field.symbol == target {
            return payload.get(cursor..).unwrap_or_default();
        }
        let ea = CompactEa::decode(field.value as u8);
        cursor += ea_payload_len(ea, payload.get(cursor..).unwrap_or_default());
    }
    payload
}
fn ea_payload_len(ea: CompactEa, payload: &[u8]) -> usize {
    match ea {
        CompactEa::Ext0 { displacement } => Ext0Descriptor::decode(payload)
            .map(|(_, descriptor_bytes)| {
                descriptor_bytes + displacement.map_or(0, DisplacementWidth::bytes)
            })
            .unwrap_or(0),
        _ => ea.appended_bytes(),
    }
}
fn payload_after_eas(instruction: &DecodedInstruction) -> &[u8] {
    let payload = trailing_bytes(instruction);
    let mut cursor = 0;
    for field in instruction
        .fields
        .iter()
        .filter(|field| field.kind == FieldKind::Ea7)
    {
        let ea = CompactEa::decode(field.value as u8);
        cursor += ea_payload_len(ea, payload.get(cursor..).unwrap_or_default());
    }
    payload.get(cursor..).unwrap_or_default()
}
fn read_unsigned(bytes: &[u8], count: usize) -> u64 {
    bytes
        .iter()
        .take(count)
        .enumerate()
        .fold(0, |value, (index, byte)| {
            value | (u64::from(*byte) << (index * 8))
        })
}
fn read_signed(bytes: &[u8], width: DisplacementWidth) -> i64 {
    let raw = read_unsigned(bytes, width.bytes());
    let shift = 64 - width.bytes() * 8;
    ((raw << shift) as i64) >> shift
}
fn signed_immediate(instruction: &DecodedInstruction) -> i64 {
    if let Some(value) = optional_field(instruction, 'i') {
        return value as u8 as i8 as i64;
    }
    let width = if instruction.allocation_id.contains("imm8s") {
        DisplacementWidth::Bits8
    } else if instruction.allocation_id.contains("imm16s")
        || matches!(
            instruction.form,
            FormId::MediumAddQEaSp
                | FormId::MediumSubQEaSp
                | FormId::MediumCallEa
                | FormId::MediumCallccEa
                | FormId::MediumJmpEa
                | FormId::MediumJccEa
        )
    {
        DisplacementWidth::Bits16
    } else if instruction.allocation_id.contains("imm32s")
        || matches!(
            instruction.form,
            FormId::MediumAddQEaSpN2
                | FormId::MediumSubQEaSpN2
                | FormId::MediumCallEaN2
                | FormId::MediumCallccEaN2
                | FormId::MediumJmpEaN2
                | FormId::MediumJccEaN2
        )
    {
        DisplacementWidth::Bits32
    } else {
        return 0;
    };
    read_signed(payload_after_eas(instruction), width)
}
fn binary_immediate(instruction: &DecodedInstruction) -> u64 {
    let bytes = payload_after_eas(instruction);
    if instruction.allocation_id.contains("imm8s") {
        return read_signed(bytes, DisplacementWidth::Bits8) as u64;
    }
    if instruction.allocation_id.contains("imm16s") {
        return read_signed(bytes, DisplacementWidth::Bits16) as u64;
    }
    if instruction.allocation_id.contains("imm32s") {
        return read_signed(bytes, DisplacementWidth::Bits32) as u64;
    }
    if instruction.allocation_id.contains("imm64") {
        return read_unsigned(bytes, 8);
    }
    signed_immediate(instruction) as u64
}
fn read_bus<B: Bus>(bus: &mut B, address: u64, size: Size) -> bedrock_bus::BusResult<u64> {
    match size {
        Size::Byte => bus.read_u8(address).map(u64::from),
        Size::Word => bus.read_u16(address).map(u64::from),
        Size::Long => bus.read_u32(address).map(u64::from),
        Size::Quad => bus.read_u64(address),
    }
}
fn write_bus<B: Bus>(
    bus: &mut B,
    address: u64,
    size: Size,
    value: u64,
) -> bedrock_bus::BusResult<()> {
    match size {
        Size::Byte => bus.write_u8(address, value as u8),
        Size::Word => bus.write_u16(address, value as u16),
        Size::Long => bus.write_u32(address, value as u32),
        Size::Quad => bus.write_u64(address, value),
    }
}

#[cfg(test)]
mod tests {
    use super::Cpu;
    use crate::exception::{InvalidControlCause, RepeatContinuation, RepeatKind};
    use crate::{
        AccessDomain, AccessKind, AddressSpaceControl, Flags, PageFaultReason, PageTableControl,
        SegmentRegister, SegmentSelector, Status, StepResult, Trap,
    };
    use bedrock_bus::{
        AcknowledgedBusFailure, Bus, BusError, BusFailureCause, BusResult, Ram, RetrySafety,
        SlotAcknowledgement, SlotData, SlotDirection, SlotProtocolError, SlotRequest, SlotResult,
        SlotTransactionError, SlotWidth,
    };
    use bedrock_isa::{EncodingClass, Size, generated::GENERATED_FORMS};

    const PTE_P: u64 = 1 << 0;
    const PTE_W: u64 = 1 << 1;
    const PTE_X: u64 = 1 << 2;
    const PTE_U: u64 = 1 << 3;
    const PTE_CP: u64 = 1 << 8;
    const PTE_A: u64 = 1 << 5;
    const PTE_D: u64 = 1 << 6;
    const PTE_AT: u64 = 1 << 7;
    const PTE_T: u64 = 1 << 11;

    struct SlotProbeBus {
        ram: Ram,
        slot_requests: Vec<SlotRequest>,
        byte_reads: Vec<u64>,
        byte_writes: Vec<u64>,
        slot_failure: Option<AcknowledgedBusFailure>,
        slot_failure_request: Option<usize>,
        read_only_from: Option<u64>,
    }

    impl SlotProbeBus {
        fn new(byte_len: usize) -> Self {
            Self {
                ram: Ram::new(byte_len),
                slot_requests: Vec::new(),
                byte_reads: Vec::new(),
                byte_writes: Vec::new(),
                slot_failure: None,
                slot_failure_request: None,
                read_only_from: None,
            }
        }

        fn clear_log(&mut self) {
            self.slot_requests.clear();
            self.byte_reads.clear();
            self.byte_writes.clear();
        }
    }

    impl Bus for SlotProbeBus {
        fn begin_transaction(&mut self) -> BusResult<()> {
            Bus::begin_transaction(&mut self.ram)
        }

        fn commit_transaction(&mut self) {
            Bus::commit_transaction(&mut self.ram);
        }

        fn rollback_transaction(&mut self) {
            Bus::rollback_transaction(&mut self.ram);
        }

        fn read_u8(&mut self, address: u64) -> BusResult<u8> {
            self.byte_reads.push(address);
            Bus::read_u8(&mut self.ram, address)
        }

        fn write_u8(&mut self, address: u64, value: u8) -> BusResult<()> {
            self.byte_writes.push(address);
            if self.read_only_from.is_some_and(|start| address >= start) {
                return Err(bedrock_bus::BusError::ReadOnly { addr: address });
            }
            Bus::write_u8(&mut self.ram, address, value)
        }

        fn slot_transaction(&mut self, request: SlotRequest) -> SlotResult<SlotAcknowledgement> {
            self.slot_requests.push(request);
            if let Some(failure) = self.slot_failure
                && self
                    .slot_failure_request
                    .is_none_or(|index| index == self.slot_requests.len())
            {
                return Ok(SlotAcknowledgement::failed(failure));
            }
            match request.direction() {
                SlotDirection::Read => {
                    SlotAcknowledgement::read(request, slot_test_data(request.width()))
                }
                SlotDirection::Write => SlotAcknowledgement::write(request),
            }
        }
    }

    const fn slot_test_data(width: SlotWidth) -> SlotData {
        match width {
            SlotWidth::B => SlotData::B(0xa5),
            SlotWidth::W => SlotData::W(0xb6a5),
            SlotWidth::L => SlotData::L(0xd8c7_b6a5),
            SlotWidth::Q => SlotData::Q(0x1020_3040_d8c7_b6a5),
        }
    }

    fn install_four_level_root(ram: &mut Ram) {
        let table_flags = PTE_P | PTE_W | PTE_X | PTE_U | PTE_T;
        ram.write_u64(0x1000, 0x2000 | table_flags).unwrap();
        ram.write_u64(0x2000, 0x3000 | table_flags).unwrap();
        ram.write_u64(0x3000, 0x4000 | table_flags).unwrap();
    }

    fn map_low_page(ram: &mut Ram, virtual_page: u64, physical_page: u64, flags: u64) {
        ram.write_u64(0x4000 + virtual_page * 8, physical_page | PTE_P | flags)
            .unwrap();
    }

    fn install_slot_leaf(bus: &mut SlotProbeBus, virtual_page: u64, physical_page: u64) {
        install_four_level_root(&mut bus.ram);
        map_low_page(
            &mut bus.ram,
            virtual_page,
            physical_page,
            PTE_W | PTE_CP | PTE_A | PTE_D | PTE_AT,
        );
    }

    fn encoded_form(id: &str, fields: &[(char, u64)], appended: &[u8]) -> Vec<u8> {
        let form = GENERATED_FORMS
            .iter()
            .find(|form| form.id == id)
            .unwrap_or_else(|| panic!("missing generated form {id}"));
        let mut payload = form.value;
        for &(symbol, value) in fields {
            let width = form
                .pattern
                .chars()
                .filter(|&field| field == symbol)
                .count();
            assert!(width != 0, "field {symbol} is absent from {id}");
            let mut field_index = 0;
            for (pattern_index, field) in form.pattern.chars().enumerate() {
                if field != symbol {
                    continue;
                }
                let payload_bit = form.pattern.len() - pattern_index - 1;
                let value_bit = width - field_index - 1;
                payload &= !(1_u64 << payload_bit);
                payload |= ((value >> value_bit) & 1) << payload_bit;
                field_index += 1;
            }
        }

        let opcode_bytes = form.class.opcode_bytes();
        let length = opcode_bytes + appended.len();
        let mut bytes = Vec::with_capacity(length);
        match form.class {
            EncodingClass::ExtraShort => bytes.push(payload as u8),
            EncodingClass::Short => {
                bytes.push(0x80 | ((payload >> 8) as u8 & 0x3f));
                bytes.push(payload as u8);
            }
            EncodingClass::Medium | EncodingClass::Long | EncodingClass::ExtraLong => {
                bytes.push(
                    0xc0 | (((length - 3) as u8) << 2)
                        | ((payload >> ((opcode_bytes - 1) * 8)) as u8 & 3),
                );
                for index in (0..opcode_bytes - 1).rev() {
                    bytes.push((payload >> (index * 8)) as u8);
                }
            }
        }
        bytes.extend_from_slice(appended);
        assert_eq!(bedrock_isa::decode(&bytes).unwrap().allocation_id, id);
        bytes
    }

    fn decoded_form(
        id: &str,
        fields: &[(char, u64)],
        appended: &[u8],
    ) -> bedrock_isa::DecodedInstruction {
        bedrock_isa::decode(&encoded_form(id, fields, appended)).unwrap()
    }

    #[test]
    fn executes_new_extrashort_nop_and_halt() {
        let mut ram = Ram::new(4);
        ram.write_u8(0, 0x01).unwrap();
        ram.write_u8(1, 0x00).unwrap();
        let mut cpu = Cpu::new();
        cpu.reset(0);
        assert_eq!(cpu.step(&mut ram), StepResult::Running);
        assert_eq!(cpu.state().pc, 1);
        assert_eq!(cpu.step(&mut ram), StepResult::Halted);
        assert!(cpu.is_halted());
    }

    #[test]
    fn illegal_instruction_delivers_typed_error_frame_with_zero_padding() {
        let mut ram = Ram::new(0x2000);
        ram.write_u8(0, 0x00).unwrap();
        let mut cpu = Cpu::new();
        cpu.reset(0);
        cpu.state_mut().ecr = crate::EventControl::from_raw(1);
        cpu.state_mut().epc = 0x100;
        cpu.state_mut().fsp = 0x1000;

        assert_eq!(cpu.step(&mut ram), StepResult::Running);
        assert_eq!(cpu.state().pc, 0x100);
        assert_eq!(cpu.state().sp, 0xfb0);
        assert_eq!(ram.read_u64(0xfb8).unwrap(), 0x03);
        assert_eq!(ram.read_u64(0xff0).unwrap(), 4);
        assert_eq!(ram.read_u64(0xff8).unwrap(), 0);
    }

    #[test]
    fn debug_trace_commits_the_unit_then_saves_the_next_boundary() {
        let mut ram = Ram::new(0x2000);
        ram.write_u8(0, 0x01).unwrap();
        let mut cpu = Cpu::new();
        cpu.reset(0);
        cpu.state_mut().status.insert(crate::Status::TF);
        cpu.state_mut().ecr = crate::EventControl::from_raw(1);
        cpu.state_mut().epc = 0x100;
        cpu.state_mut().fsp = 0x1000;

        assert_eq!(cpu.step(&mut ram), StepResult::Running);
        assert_eq!(cpu.state().pc, 0x100);
        assert_eq!(cpu.state().sp, 0xfc0);
        assert_eq!(ram.read_u64(0xfc8).unwrap(), 0);
        assert_eq!(ram.read_u64(0xfd8).unwrap(), 1);
        assert_ne!(ram.read_u64(0xfc0).unwrap() >> 48 & 4, 0);
        assert!(!cpu.state().status.contains(crate::Status::TF));
    }

    #[test]
    fn pending_nmi_coalesces_wakes_halt_and_reenters_only_after_ni_clears() {
        let halt = encoded_form("short.halt", &[], &[]);
        let mut ram = Ram::new(0x2000);
        ram.load(0, &halt).unwrap();
        ram.write_u8(0x100, 0x04).unwrap(); // ERET
        let mut cpu = Cpu::new();
        cpu.reset(0);

        cpu.request_nmi();
        cpu.request_nmi();
        assert!(cpu.state().ecr.nmi_pending());
        assert_eq!(cpu.step(&mut ram), StepResult::Halted);
        assert!(cpu.is_halted());
        assert_eq!(cpu.state().pc, halt.len() as u64);
        assert!(cpu.state().ecr.nmi_pending());

        cpu.state_mut().ecr = crate::EventControl::from_raw(0x81);
        cpu.state_mut().epc = 0x100;
        cpu.state_mut().fsp = 0x1000;
        assert_eq!(cpu.step(&mut ram), StepResult::Running);
        assert!(!cpu.is_halted());
        assert_eq!(cpu.state().pc, 0x100);
        assert_eq!(cpu.state().sp, 0xfc0);
        assert_eq!(ram.read_u64(0xfc8).unwrap(), 2 << 24);
        assert_eq!(ram.read_u64(0xfd8).unwrap(), halt.len() as u64);
        assert!(
            cpu.state()
                .status
                .contains(Status::PM | Status::EA | Status::NI)
        );
        assert!(!cpu.state().ecr.nmi_pending());

        cpu.request_nmi();
        cpu.request_nmi();
        assert_eq!(cpu.step(&mut ram), StepResult::Running); // ERET while NI blocks nesting
        assert_eq!(cpu.state().pc, halt.len() as u64);
        assert!(!cpu.state().status.contains(Status::NI | Status::EA));
        assert!(cpu.state().ecr.nmi_pending());

        assert_eq!(cpu.step(&mut ram), StepResult::Running);
        assert_eq!(cpu.state().pc, 0x100);
        assert!(cpu.state().status.contains(Status::NI | Status::EA));
        assert!(!cpu.state().ecr.nmi_pending());
    }

    #[test]
    fn malformed_eret_frame_delivers_invalid_control_without_consuming_it() {
        let mut ram = Ram::new(0x3000);
        ram.write_u8(0, 0x04).unwrap();
        let mut cpu = Cpu::new();
        cpu.reset(0);
        cpu.state_mut().status = crate::Status::PM | crate::Status::EA;
        cpu.state_mut().hidden_current_edepth = 1;
        cpu.state_mut().hidden_current_esl = 2;
        cpu.state_mut().sp = 0x1000;
        cpu.state_mut().ecr = crate::EventControl::from_raw(1);
        cpu.state_mut().epc = 0x200;

        assert_eq!(cpu.step(&mut ram), StepResult::Running);
        assert_eq!(cpu.state().pc, 0x200);
        assert_eq!(cpu.state().sp, 0xfb0);
        assert_eq!(ram.read_u64(0xfb8).unwrap(), 0x0d);
        assert_eq!(ram.read_u64(0xff0).unwrap(), 2);
        assert_eq!(ram.read_u64(0x1000).unwrap(), 0);
    }

    #[test]
    fn floating_clear_zeros_the_complete_register() {
        let mut ram = Ram::new(3);
        ram.load(0, &[0xc2, 0x40, 0x80]).unwrap(); // FCLR F0
        let mut cpu = Cpu::new();
        cpu.reset(0);
        cpu.state_mut().f[0] = u64::MAX;

        assert_eq!(cpu.step(&mut ram), StepResult::Running);
        assert_eq!(cpu.state().f[0], 0);
        assert_eq!(cpu.state().pc, 3);
    }

    #[test]
    fn floating_constant_and_fused_multiply_add_follow_the_fpu_encoding() {
        let mut ram = Ram::new(10);
        ram.load(
            0,
            &[
                0xcf, 0xd6, 0xb1, 0x02, 0x08, 0x00, // FMOVCR.D 8, F2
                0xc7, 0xd0, 0x89, 0x40, // FMADD.D F1, F2, F0
            ],
        )
        .unwrap();
        let mut cpu = Cpu::new();
        cpu.reset(0);
        cpu.state_mut().f[0] = 2.0f64.to_bits();
        cpu.state_mut().f[1] = 3.0f64.to_bits();

        assert_eq!(cpu.step(&mut ram), StepResult::Running);
        assert_eq!(cpu.state().f[2], 10.0f64.to_bits());
        assert_eq!(cpu.step(&mut ram), StepResult::Running);
        assert_eq!(cpu.state().f[0], 32.0f64.to_bits());
        assert_eq!(cpu.state().pc, 10);
    }

    #[test]
    fn stack_underflow_faults_without_committing_sp() {
        let mut ram = Ram::new(2);
        ram.write_u8(0, 0x20).unwrap();
        let mut cpu = Cpu::new();
        cpu.reset(0);
        cpu.state_mut().sp = 1;
        assert_eq!(cpu.step(&mut ram), StepResult::Halted);
        assert_eq!(cpu.state().sp, 1);
    }

    #[test]
    fn movuc_reads_through_the_user_domain() {
        let mut ram = Ram::new(0x10_000);
        install_four_level_root(&mut ram);
        map_low_page(&mut ram, 0, 0x8000, PTE_W | PTE_X);
        map_low_page(&mut ram, 1, 0x9000, PTE_W | PTE_U);
        ram.load(0x8000, &[0xc7, 0xe2, 0xc8, 0x01]).unwrap(); // MOVUC.Q [R0], R1
        ram.write_u64(0x9000, 0x1122_3344_5566_7788).unwrap();

        let mut cpu = Cpu::new();
        cpu.reset(0);
        cpu.state_mut().ptcr = PageTableControl::from_raw(0x1001);
        cpu.state_mut().r[0] = 0x1000;
        assert_eq!(cpu.step(&mut ram), StepResult::Running);
        assert_eq!(cpu.state().r[1], 0x1122_3344_5566_7788);

        map_low_page(&mut ram, 1, 0x9000, PTE_W);
        cpu.reset(0);
        cpu.state_mut().ptcr = PageTableControl::from_raw(0x1001);
        cpu.state_mut().r[0] = 0x1000;
        assert_eq!(cpu.step(&mut ram), StepResult::Halted);
    }

    #[test]
    fn page_fault_enters_common_event_handler_and_populates_fault_frame() {
        let mut ram = Ram::new(0x20_000);
        install_four_level_root(&mut ram);
        map_low_page(&mut ram, 0, 0x8000, PTE_X | PTE_U);
        map_low_page(&mut ram, 5, 0xd000, PTE_X);
        map_low_page(&mut ram, 6, 0xe000, PTE_W);
        ram.load(0x8000, &[0xc0, 0x38, 0x90]).unwrap(); // MOV.Q [R0], R1
        ram.write_u8(0xd000, 0x04).unwrap(); // ERET

        let mut cpu = Cpu::new();
        cpu.reset(0);
        cpu.state_mut().status = crate::Status::empty();
        cpu.state_mut().ptcr = PageTableControl::from_raw(0x1001);
        cpu.state_mut().ascr = crate::AddressSpaceControl::from_raw(0x1234_0001);
        cpu.state_mut().ecr = crate::EventControl::from_raw(1);
        cpu.state_mut().epc = 0x5000;
        cpu.state_mut().fsp = 0x7000;
        cpu.state_mut().r[0] = 0x1000;
        cpu.state_mut().r[1] = 0xfeed_face;

        assert_eq!(cpu.step(&mut ram), StepResult::Running);
        assert_eq!(cpu.state().pc, 0x5000);
        assert_eq!(cpu.state().sp, 0x6fa0);
        assert!(
            cpu.state()
                .status
                .contains(crate::Status::PM | crate::Status::EA)
        );
        assert_eq!(cpu.state().r[1], 0xfeed_face);

        let frame = 0xefa0;
        assert_eq!(ram.read_u64(frame).unwrap() & 0xfff, (2 << 8) | 12);
        assert_eq!(ram.read_u64(frame + 8).unwrap(), 9);
        assert_eq!(ram.read_u64(frame + 24).unwrap(), 0);
        assert_eq!(
            ram.read_u64(frame + 64).unwrap(),
            u64::from(PageFaultReason::NotPresent.code()) | 0x2300_0100
        );
        assert_eq!(ram.read_u64(frame + 72).unwrap(), 0x1000);
        assert_eq!(ram.read_u64(frame + 80).unwrap(), 0x1000);
        assert_eq!(ram.read_u64(frame + 88).unwrap(), 0);

        assert_eq!(cpu.step(&mut ram), StepResult::Running);
        assert_eq!(cpu.state().pc, 0);
        assert_eq!(cpu.state().status, crate::Status::empty());
    }

    #[test]
    fn page_fault_and_double_fault_delivery_failure_enters_shutdown() {
        let mut ram = Ram::new(0x20_000);
        install_four_level_root(&mut ram);
        map_low_page(&mut ram, 0, 0x8000, PTE_X | PTE_U);
        ram.load(0x8000, &[0xc0, 0x38, 0x90]).unwrap(); // MOV.Q [R0], R1

        let mut cpu = Cpu::new();
        cpu.reset(0);
        cpu.state_mut().status = crate::Status::empty();
        cpu.state_mut().ptcr = PageTableControl::from_raw(0x1001);
        cpu.state_mut().ecr = crate::EventControl::from_raw(1);
        cpu.state_mut().epc = 0x5000;
        cpu.state_mut().fsp = 0x7000;
        cpu.state_mut().r[0] = 0x1000;

        assert_eq!(cpu.step(&mut ram), StepResult::Halted);
        assert!(cpu.is_halted());
        assert_eq!(cpu.state().pc, 0);
        assert_eq!(cpu.state().status, crate::Status::empty());
    }

    #[test]
    fn movcu_and_movuu_use_the_user_domain_for_their_memory_sides() {
        let mut ram = Ram::new(0x10_000);
        install_four_level_root(&mut ram);
        map_low_page(&mut ram, 0, 0x8000, PTE_W | PTE_X);
        map_low_page(&mut ram, 1, 0x9000, PTE_W | PTE_U);
        map_low_page(&mut ram, 2, 0xa000, PTE_W | PTE_U);
        ram.load(
            0x8000,
            &[
                0xc7, 0xe3, 0xc1, 0x11, // MOVCU.Q R2, [R1]
                0xc7, 0xe4, 0xc8, 0x11, // MOVUU.Q [R0], [R1]
            ],
        )
        .unwrap();

        let mut cpu = Cpu::new();
        cpu.reset(0);
        cpu.state_mut().ptcr = PageTableControl::from_raw(0x1001);
        cpu.state_mut().r[1] = 0x1000;
        cpu.state_mut().r[2] = 0xaabb_ccdd_eeff_0011;
        assert_eq!(cpu.step(&mut ram), StepResult::Running);
        assert_eq!(ram.read_u64(0x9000).unwrap(), 0xaabb_ccdd_eeff_0011);

        cpu.state_mut().r[0] = 0x2000;
        cpu.state_mut().r[1] = 0x1000;
        ram.write_u64(0xa000, 0x8877_6655_4433_2211).unwrap();
        assert_eq!(cpu.step(&mut ram), StepResult::Running);
        assert_eq!(ram.read_u64(0x9000).unwrap(), 0x8877_6655_4433_2211);
    }

    #[test]
    fn swpta_encodes_the_asid_and_vtop_walks_the_active_page_table() {
        let mut control_ram = Ram::new(8);
        control_ram.load(0, &[0xc7, 0xef, 0x48, 0x90]).unwrap(); // SWPTA R0, R1
        let mut cpu = Cpu::new();
        cpu.reset(0);
        cpu.state_mut().r[0] = 0;
        cpu.state_mut().r[1] = 0xfeed_1234;
        assert_eq!(cpu.step(&mut control_ram), StepResult::Running);
        assert_eq!(cpu.state().ascr.raw(), 0x1234_0001);

        let mut ram = Ram::new(0x10_000);
        install_four_level_root(&mut ram);
        map_low_page(&mut ram, 0, 0x8000, PTE_W | PTE_X);
        map_low_page(&mut ram, 1, 0x9000, PTE_W | PTE_U);
        ram.load(0x8000, &[0xc7, 0xef, 0x48, 0x82]).unwrap(); // VTOP R1, R2
        cpu.reset(0);
        cpu.state_mut().ptcr = PageTableControl::from_raw(0x1001);
        cpu.state_mut().r[1] = 0x1234;
        assert_eq!(cpu.step(&mut ram), StepResult::Running);
        assert_eq!(cpu.state().r[2], 0x9234);
        assert_eq!(cpu.state().flags, Flags::Z | Flags::N | Flags::C);
        assert_eq!(ram.read_u64(0x4008).unwrap() & (PTE_A | PTE_D), 0);
    }

    #[test]
    fn vtop_with_paging_disabled_is_identity_and_sets_all_query_flags() {
        let instruction = encoded_form("long.vtop_rn_v_rn_p", &[('v', 1), ('p', 2)], &[]);
        let mut ram = Ram::new(instruction.len());
        ram.load(0, &instruction).unwrap();
        let mut cpu = Cpu::new();
        cpu.reset(0);
        cpu.state_mut().r[1] = u64::MAX;

        assert_eq!(cpu.step(&mut ram), StepResult::Running);
        assert_eq!(cpu.state().r[2], u64::MAX);
        assert_eq!(cpu.state().flags, Flags::Z | Flags::N | Flags::C | Flags::V);
    }

    #[test]
    fn vtop_failure_retires_with_zero_and_cleared_flags() {
        let mut ram = Ram::new(0x10_000);
        install_four_level_root(&mut ram);
        map_low_page(&mut ram, 0, 0x8000, PTE_W | PTE_X);
        ram.load(
            0x8000,
            &encoded_form("long.vtop_rn_v_rn_p", &[('v', 1), ('p', 2)], &[]),
        )
        .unwrap();
        let mut cpu = Cpu::new();
        cpu.reset(0);
        cpu.state_mut().ptcr = PageTableControl::from_raw(0x1001);
        cpu.state_mut().r[1] = 1 << 48;
        cpu.state_mut().r[2] = u64::MAX;
        cpu.state_mut().flags = Flags::all();

        assert_eq!(cpu.step(&mut ram), StepResult::Running);
        assert_eq!(cpu.state().r[2], 0);
        assert!(cpu.state().flags.is_empty());
    }

    #[test]
    fn fetch_through_a_slot_leaf_obeys_privilege_then_address_type_priority() {
        let mut ram = Ram::new(0x10_000);
        install_four_level_root(&mut ram);
        map_low_page(
            &mut ram,
            0,
            0x10_000,
            PTE_W | PTE_CP | PTE_A | PTE_D | PTE_AT,
        );
        let mut cpu = Cpu::new();
        cpu.reset(0);
        cpu.state_mut().ptcr = PageTableControl::from_raw(0x1001);
        cpu.state_mut().status.remove(crate::Status::PM);

        assert!(matches!(
            cpu.translate_fetch(&mut ram, 0, 0),
            Err(Trap::PageFault {
                context: crate::PageFaultContext {
                    reason: PageFaultReason::Privilege,
                    ..
                },
                ..
            })
        ));

        let leaf = ram.read_u64(0x4000).unwrap();
        ram.write_u64(0x4000, leaf | PTE_U).unwrap();

        assert!(matches!(
            cpu.translate_fetch(&mut ram, 0, 0),
            Err(Trap::PageFault {
                context: crate::PageFaultContext {
                    reason: PageFaultReason::AddressType,
                    ..
                },
                ..
            })
        ));
    }

    #[test]
    fn slot_loads_and_stores_issue_exactly_one_typed_transaction_for_every_width() {
        let mut bus = SlotProbeBus::new(0x6000);
        install_slot_leaf(&mut bus, 0, 0x8000);
        let mut cpu = Cpu::new();
        cpu.reset(0);
        cpu.state_mut().ptcr = PageTableControl::from_raw(0x1001);
        let cases = [
            (Size::Byte, SlotData::B(0x5a)),
            (Size::Word, SlotData::W(0x1234)),
            (Size::Long, SlotData::L(0x89ab_cdef)),
            (Size::Quad, SlotData::Q(0x0123_4567_89ab_cdef)),
        ];

        for (size, write_data) in cases {
            bus.clear_log();
            let value = cpu
                .read_virtual(
                    &mut bus,
                    0,
                    SegmentSelector::Ds,
                    0x123,
                    AccessDomain::Current,
                    size,
                )
                .unwrap();
            assert_eq!(value, slot_test_data(write_data.width()).as_u64());
            assert_eq!(
                bus.slot_requests,
                [SlotRequest::read(0x8123, write_data.width())]
            );
            assert!(bus.byte_reads.iter().all(|&address| address < 0x8000));

            bus.clear_log();
            cpu.write_virtual(
                &mut bus,
                0,
                SegmentSelector::Ds,
                0x123,
                AccessDomain::Current,
                size,
                write_data.as_u64(),
            )
            .unwrap();
            assert_eq!(bus.slot_requests, [SlotRequest::write(0x8123, write_data)]);
            assert!(bus.byte_writes.iter().all(|&address| address < 0x8000));
        }
    }

    #[test]
    fn quad_slot_at_leaf_end_does_not_translate_or_touch_the_next_page() {
        let mut bus = SlotProbeBus::new(0x6000);
        install_slot_leaf(&mut bus, 0, 0x8000);
        let mut cpu = Cpu::new();
        cpu.reset(0);
        cpu.state_mut().ptcr = PageTableControl::from_raw(0x1001);

        assert_eq!(
            cpu.read_virtual(
                &mut bus,
                0,
                SegmentSelector::Ds,
                0xfff,
                AccessDomain::Current,
                Size::Quad,
            )
            .unwrap(),
            slot_test_data(SlotWidth::Q).as_u64()
        );
        assert_eq!(bus.slot_requests, [SlotRequest::read(0x8fff, SlotWidth::Q)]);
        assert!(!bus.byte_reads.contains(&0x4008));
    }

    #[test]
    fn acknowledged_slot_failure_preserves_cause_final_address_and_retry_safety() {
        let mut bus = SlotProbeBus::new(0x6000);
        install_slot_leaf(&mut bus, 0, 0x8000);
        let failure = AcknowledgedBusFailure::new(
            BusFailureCause::DataError,
            0xfeed_cafe,
            RetrySafety::EffectMayHaveOccurred,
        );
        bus.slot_failure = Some(failure);
        let mut cpu = Cpu::new();
        cpu.reset(0x55);
        cpu.state_mut().ptcr = PageTableControl::from_raw(0x1001);

        assert!(matches!(
            cpu.read_virtual(
                &mut bus,
                0x55,
                SegmentSelector::Ds,
                0x123,
                AccessDomain::Current,
                Size::Long,
            ),
            Err(Trap::AcknowledgedBusFailure {
                pc: 0x55,
                context: crate::BusFaultContext {
                    failure: actual,
                    effective_address: 0x123,
                    linear_address: Some(0x123),
                    access_kind: AccessKind::Read,
                    access_size: Some(3),
                    ..
                },
            }) if actual == failure
        ));
        assert_eq!(bus.slot_requests, [SlotRequest::read(0x8123, SlotWidth::L)]);
        assert!(bus.byte_reads.iter().all(|&address| address < 0x8000));
    }

    #[test]
    fn raw_addressed_bus_errors_have_architectural_failure_metadata() {
        let cases = [
            (
                BusError::OutOfRange { addr: 0x10 },
                BusFailureCause::NoResponder,
                0x10,
            ),
            (
                BusError::Unmapped { addr: 0x20 },
                BusFailureCause::NoResponder,
                0x20,
            ),
            (
                BusError::ReadOnly { addr: 0x30 },
                BusFailureCause::AccessDenied,
                0x30,
            ),
            (
                BusError::InvalidRange {
                    start: 0x40,
                    end: 0x48,
                },
                BusFailureCause::Other,
                0x40,
            ),
            (
                BusError::Device {
                    addr: 0x50,
                    message: "device failure".into(),
                },
                BusFailureCause::Other,
                0x50,
            ),
        ];
        for (error, cause, final_address) in cases {
            assert_eq!(
                super::raw_bus_failure(&error),
                Some(AcknowledgedBusFailure::new(
                    cause,
                    final_address,
                    RetrySafety::RetrySafe,
                ))
            );
        }
        assert_eq!(super::raw_bus_failure(&BusError::TransactionActive), None);
        assert_eq!(super::raw_bus_failure(&BusError::NoTransaction), None);
    }

    #[test]
    fn byte_and_page_walk_bus_errors_preserve_access_and_walk_context() {
        let mut cpu = Cpu::new();
        cpu.reset(0x55);
        let mut byte_bus = Ram::new(1);
        assert!(matches!(
            cpu.read_virtual(
                &mut byte_bus,
                0x55,
                SegmentSelector::Ds,
                0x20,
                AccessDomain::Current,
                Size::Byte,
            ),
            Err(Trap::AcknowledgedBusFailure {
                pc: 0x55,
                context: crate::BusFaultContext {
                    failure: AcknowledgedBusFailure {
                        cause: BusFailureCause::NoResponder,
                        final_address: 0x20,
                        retry_safety: RetrySafety::RetrySafe,
                    },
                    effective_address: 0x20,
                    linear_address: Some(0x20),
                    access_kind: AccessKind::Read,
                    access_size: Some(1),
                    walk_level: 0,
                    ..
                },
            })
        ));

        let mut page_bus = Ram::new(0x4000);
        install_four_level_root(&mut page_bus);
        cpu.reset(0x66);
        cpu.state_mut().ptcr = PageTableControl::from_raw(0x1001);
        assert!(matches!(
            cpu.read_virtual(
                &mut page_bus,
                0x66,
                SegmentSelector::Ds,
                0x123,
                AccessDomain::Current,
                Size::Long,
            ),
            Err(Trap::AcknowledgedBusFailure {
                pc: 0x66,
                context: crate::BusFaultContext {
                    failure: AcknowledgedBusFailure {
                        cause: BusFailureCause::NoResponder,
                        final_address: 0x4000,
                        retry_safety: RetrySafety::RetrySafe,
                    },
                    effective_address: 0x123,
                    linear_address: Some(0x123),
                    access_kind: AccessKind::Read,
                    walk_level: 1,
                    ..
                },
            })
        ));
    }

    #[test]
    fn lifecycle_and_slot_protocol_errors_remain_internal() {
        let cpu = Cpu::new();
        assert!(matches!(
            cpu.bus_access_trap(
                0x10,
                BusError::TransactionActive,
                0x20,
                Some(0x20),
                AccessKind::Read,
                AccessDomain::Current,
                Some(SegmentSelector::Ds),
                Some(1),
                Some(0),
                false,
                0,
            ),
            Trap::Bus {
                pc: 0x10,
                error: BusError::TransactionActive,
            }
        ));
        assert!(matches!(
            cpu.slot_access_transaction_trap(
                0x10,
                SlotTransactionError::Bus(BusError::ReadOnly { addr: 0x31 }),
                0x20,
                0x120,
                AccessKind::Write,
                AccessDomain::User,
                SegmentSelector::Ds,
                2,
            ),
            Trap::AcknowledgedBusFailure {
                pc: 0x10,
                context: crate::BusFaultContext {
                    failure: AcknowledgedBusFailure {
                        cause: BusFailureCause::AccessDenied,
                        final_address: 0x31,
                        retry_safety: RetrySafety::RetrySafe,
                    },
                    effective_address: 0x20,
                    linear_address: Some(0x120),
                    access_kind: AccessKind::Write,
                    access_domain: AccessDomain::User,
                    access_size: Some(2),
                    ..
                },
            }
        ));
        assert!(matches!(
            cpu.slot_access_transaction_trap(
                0x10,
                SlotTransactionError::Protocol {
                    addr: 0x30,
                    error: SlotProtocolError::WidthMismatch,
                },
                0x20,
                0x20,
                AccessKind::Read,
                AccessDomain::Current,
                SegmentSelector::Ds,
                1,
            ),
            Trap::SlotTransaction {
                pc: 0x10,
                error: SlotTransactionError::Protocol {
                    addr: 0x30,
                    error: SlotProtocolError::WidthMismatch,
                },
            }
        ));
    }

    #[test]
    fn successful_slot_before_retry_safe_failure_clears_retry_safe_in_bus_error_frame() {
        let mut bus = SlotProbeBus::new(0x20_000);
        install_four_level_root(&mut bus.ram);
        map_low_page(&mut bus.ram, 0, 0x8000, PTE_W | PTE_X);
        map_low_page(
            &mut bus.ram,
            1,
            0x9000,
            PTE_W | PTE_CP | PTE_A | PTE_D | PTE_AT,
        );
        map_low_page(&mut bus.ram, 2, 0xa000, PTE_X);
        map_low_page(&mut bus.ram, 3, 0xb000, PTE_W);
        bus.ram.write_u8(0x8000, 0x14).unwrap(); // PUSHP PAIR4
        bus.slot_failure = Some(AcknowledgedBusFailure::new(
            BusFailureCause::Timeout,
            0xfeed_cafe,
            RetrySafety::RetrySafe,
        ));
        bus.slot_failure_request = Some(2);
        bus.clear_log();

        let mut cpu = Cpu::new();
        cpu.reset(0);
        cpu.state_mut().ptcr = PageTableControl::from_raw(0x1001);
        cpu.state_mut().ecr = crate::EventControl::from_raw(1);
        cpu.state_mut().epc = 0x2000;
        cpu.state_mut().fsp = 0x4000;
        cpu.state_mut().sp = 0x2000;
        cpu.state_mut().r[8] = 0x8888;
        cpu.state_mut().r[9] = 0x9999;

        assert_eq!(cpu.step(&mut bus), StepResult::Running);
        assert_eq!(bus.slot_requests.len(), 2);
        assert_eq!(cpu.state().pc, 0x2000);
        assert_eq!(cpu.state().sp, 0x3fa0);

        let frame = 0xbfa0;
        assert_eq!(bus.ram.read_u64(frame + 8).unwrap(), 0x1a);
        assert_eq!(bus.ram.read_u64(frame + 32).unwrap(), 0x2000);
        let error_code = bus.ram.read_u64(frame + 64).unwrap();
        assert_eq!(error_code & 0xff, BusFailureCause::Timeout as u64);
        assert_eq!(error_code >> 8 & 0b11, 2);
        assert_eq!(error_code >> 12 & 0b111, 0);
        assert_eq!(error_code >> 16 & 0xff, 0xff);
        assert_eq!(error_code >> 27 & 0b111, 4);
        assert_eq!(error_code >> 30 & 1, 0);
        assert_eq!(bus.ram.read_u64(frame + 72).unwrap(), 0x1ff0);
        assert_eq!(bus.ram.read_u64(frame + 80).unwrap(), 0x1ff0);
        assert_eq!(bus.ram.read_u64(frame + 88).unwrap(), 0xfeed_cafe);
    }

    #[test]
    fn byte_range_crossing_into_slot_leaf_faults_without_data_or_slot_access() {
        let mut bus = SlotProbeBus::new(0x9000);
        install_four_level_root(&mut bus.ram);
        map_low_page(&mut bus.ram, 0, 0x8000, PTE_W);
        map_low_page(
            &mut bus.ram,
            1,
            0xa000,
            PTE_W | PTE_CP | PTE_A | PTE_D | PTE_AT,
        );
        bus.ram.write_u8(0x8fff, 0x5a).unwrap();
        let mut cpu = Cpu::new();
        cpu.reset(0);
        cpu.state_mut().ptcr = PageTableControl::from_raw(0x1001);

        assert!(matches!(
            cpu.read_virtual(
                &mut bus,
                0,
                SegmentSelector::Ds,
                0xfff,
                AccessDomain::Current,
                Size::Word,
            ),
            Err(Trap::PageFault {
                context: crate::PageFaultContext {
                    reason: PageFaultReason::AddressType,
                    ..
                },
                ..
            })
        ));
        assert!(bus.slot_requests.is_empty());
        assert!(!bus.byte_reads.contains(&0x8fff));

        bus.clear_log();
        assert!(matches!(
            cpu.write_virtual(
                &mut bus,
                0,
                SegmentSelector::Ds,
                0xfff,
                AccessDomain::Current,
                Size::Word,
                0xffff,
            ),
            Err(Trap::PageFault {
                context: crate::PageFaultContext {
                    reason: PageFaultReason::AddressType,
                    ..
                },
                ..
            })
        ));
        assert!(bus.slot_requests.is_empty());
        assert!(!bus.byte_writes.contains(&0x8fff));
        assert_eq!(bus.ram.read_u8(0x8fff).unwrap(), 0x5a);
    }

    #[test]
    fn byte_ranges_never_wrap_at_the_end_of_the_address_space() {
        let mut bus = SlotProbeBus::new(1);
        let mut cpu = Cpu::new();
        cpu.reset(0x55);

        assert!(matches!(
            cpu.read_virtual(
                &mut bus,
                0x55,
                SegmentSelector::Ds,
                u64::MAX,
                AccessDomain::Current,
                Size::Word,
            ),
            Err(Trap::PageFault {
                pc: 0x55,
                context: crate::PageFaultContext {
                    effective_address: u64::MAX,
                    linear_address: None,
                    reason: PageFaultReason::SegmentBounds,
                    access_kind: AccessKind::Read,
                    ..
                },
            })
        ));
        assert!(bus.byte_reads.is_empty());

        assert!(matches!(
            cpu.write_virtual(
                &mut bus,
                0x55,
                SegmentSelector::Ds,
                u64::MAX,
                AccessDomain::Current,
                Size::Quad,
                0,
            ),
            Err(Trap::PageFault {
                context: crate::PageFaultContext {
                    reason: PageFaultReason::SegmentBounds,
                    access_kind: AccessKind::Write,
                    ..
                },
                ..
            })
        ));
        assert!(bus.byte_writes.is_empty());
    }

    #[test]
    fn cmpxchg_sets_dirty_only_when_the_store_commits_and_writes_exact_flags() {
        let instruction = encoded_form(
            "extralong.cmpxchg_x_order_o_rn_x_rn_d_ea_e",
            &[('z', 3), ('o', 0), ('x', 2), ('d', 3), ('e', 0x11)],
            &[],
        );
        let mut ram = Ram::new(0x10_000);
        install_four_level_root(&mut ram);
        map_low_page(&mut ram, 0, 0x8000, PTE_W | PTE_X);
        map_low_page(&mut ram, 1, 0x9000, PTE_W);
        ram.load(0x8000, &instruction).unwrap();
        ram.write_u64(0x9000, 5).unwrap();
        let mut cpu = Cpu::new();
        cpu.reset(0);
        cpu.state_mut().ptcr = PageTableControl::from_raw(0x1001);
        cpu.state_mut().r[1] = 0x1000;
        cpu.state_mut().r[2] = 4;
        cpu.state_mut().r[3] = 9;
        cpu.state_mut().flags = Flags::all();

        assert_eq!(cpu.step(&mut ram), StepResult::Running);
        assert_eq!(ram.read_u64(0x9000).unwrap(), 5);
        assert_eq!(ram.read_u64(0x4008).unwrap() & PTE_D, 0);
        assert_eq!(cpu.state().r[2], 5);
        assert!(cpu.state().flags.is_empty());

        cpu.state_mut().pc = 0;
        cpu.state_mut().r[2] = 5;
        cpu.state_mut().flags = Flags::all();
        assert_eq!(cpu.step(&mut ram), StepResult::Running);
        assert_eq!(ram.read_u64(0x9000).unwrap(), 9);
        assert_ne!(ram.read_u64(0x4008).unwrap() & PTE_D, 0);
        assert_eq!(cpu.state().r[2], 5);
        assert_eq!(cpu.state().flags, Flags::Z);
    }

    #[test]
    fn fetch_operand_is_captured_before_overlapping_ext0_base_or_index_update() {
        struct Case {
            descriptor: &'static [u8],
            address: u64,
            source_value: u64,
            extra_register: Option<(usize, u64)>,
        }
        let cases = [
            Case {
                descriptor: &[0x94],
                address: 0x40,
                source_value: 0x40,
                extra_register: None,
            },
            Case {
                descriptor: &[0x90, 0x12],
                address: 0x50,
                source_value: 2,
                extra_register: Some((1, 0x40)),
            },
        ];
        for case in cases {
            let instruction = encoded_form(
                "extralong.fetchadd_x_order_o_rn_s_ea_e",
                &[('z', 3), ('o', 0), ('s', 2), ('e', 0x74)],
                case.descriptor,
            );
            let mut ram = Ram::new(0x100);
            ram.load(0, &instruction).unwrap();
            ram.write_u64(case.address, 5).unwrap();
            let mut cpu = Cpu::new();
            cpu.reset(0);
            cpu.state_mut().r[2] = case.source_value;
            if let Some((register, value)) = case.extra_register {
                cpu.state_mut().r[register] = value;
            }

            assert_eq!(cpu.step(&mut ram), StepResult::Running);
            assert_eq!(ram.read_u64(case.address).unwrap(), 5 + case.source_value);
            assert_eq!(cpu.state().r[2], 5);
        }
    }

    #[test]
    fn cmpxchg_operands_are_captured_before_overlapping_ext0_updates() {
        struct Case {
            descriptor: &'static [u8],
            address: u64,
            operand_value: u64,
            extra_register: Option<(usize, u64)>,
            final_operand: u64,
        }
        let expected_cases = [
            Case {
                descriptor: &[0x94],
                address: 0x40,
                operand_value: 0x40,
                extra_register: None,
                final_operand: 0x40,
            },
            Case {
                descriptor: &[0x90, 0x12],
                address: 0x50,
                operand_value: 2,
                extra_register: Some((1, 0x40)),
                final_operand: 2,
            },
        ];
        for case in expected_cases {
            let instruction = encoded_form(
                "extralong.cmpxchg_x_order_o_rn_x_rn_d_ea_e",
                &[('z', 3), ('o', 0), ('x', 2), ('d', 3), ('e', 0x74)],
                case.descriptor,
            );
            let mut ram = Ram::new(0x100);
            ram.load(0, &instruction).unwrap();
            ram.write_u64(case.address, case.operand_value).unwrap();
            let mut cpu = Cpu::new();
            cpu.reset(0);
            cpu.state_mut().r[2] = case.operand_value;
            cpu.state_mut().r[3] = 0xdead_beef;
            if let Some((register, value)) = case.extra_register {
                cpu.state_mut().r[register] = value;
            }

            assert_eq!(cpu.step(&mut ram), StepResult::Running);
            assert_eq!(ram.read_u64(case.address).unwrap(), 0xdead_beef);
            assert_eq!(cpu.state().r[2], case.final_operand);
            assert_eq!(cpu.state().flags, Flags::Z);
        }

        let desired_cases = [
            Case {
                descriptor: &[0x9c],
                address: 0x40,
                operand_value: 0x40,
                extra_register: None,
                final_operand: 0x48,
            },
            Case {
                descriptor: &[0x90, 0x13],
                address: 0x50,
                operand_value: 2,
                extra_register: Some((1, 0x40)),
                final_operand: 3,
            },
        ];
        for case in desired_cases {
            let instruction = encoded_form(
                "extralong.cmpxchg_x_order_o_rn_x_rn_d_ea_e",
                &[('z', 3), ('o', 0), ('x', 2), ('d', 3), ('e', 0x74)],
                case.descriptor,
            );
            let mut ram = Ram::new(0x100);
            ram.load(0, &instruction).unwrap();
            ram.write_u64(case.address, 0x55).unwrap();
            let mut cpu = Cpu::new();
            cpu.reset(0);
            cpu.state_mut().r[2] = 0x55;
            cpu.state_mut().r[3] = case.operand_value;
            if let Some((register, value)) = case.extra_register {
                cpu.state_mut().r[register] = value;
            }

            assert_eq!(cpu.step(&mut ram), StepResult::Running);
            assert_eq!(ram.read_u64(case.address).unwrap(), case.operand_value);
            assert_eq!(cpu.state().r[2], 0x55);
            assert_eq!(cpu.state().r[3], case.final_operand);
            assert_eq!(cpu.state().flags, Flags::Z);
        }
    }

    #[test]
    fn bounds_operands_follow_low_value_high_order_with_overlapping_ext0_updates() {
        struct Case {
            descriptor: &'static [u8],
            address: u64,
            low: usize,
            high: usize,
            r1: u64,
            r2: u64,
            r3: u64,
            memory: u64,
            final_r2: u64,
        }
        let cases = [
            Case {
                descriptor: &[0x94],
                address: 0x40,
                low: 2,
                high: 3,
                r1: 0,
                r2: 0x40,
                r3: 0x48,
                memory: 0x44,
                final_r2: 0x48,
            },
            Case {
                descriptor: &[0x90, 0x12],
                address: 0x50,
                low: 2,
                high: 3,
                r1: 0x40,
                r2: 2,
                r3: 3,
                memory: 2,
                final_r2: 3,
            },
            Case {
                descriptor: &[0x94],
                address: 0x40,
                low: 3,
                high: 2,
                r1: 0,
                r2: 0x40,
                r3: 0,
                memory: 0x44,
                final_r2: 0x48,
            },
            Case {
                descriptor: &[0x90, 0x12],
                address: 0x50,
                low: 3,
                high: 2,
                r1: 0x40,
                r2: 2,
                r3: 0,
                memory: 3,
                final_r2: 3,
            },
        ];
        for case in cases {
            let instruction = encoded_form(
                "extralong.bnduii_x_rn_l_ea_e_rn_h",
                &[
                    ('z', 3),
                    ('l', case.low as u64),
                    ('e', 0x74),
                    ('h', case.high as u64),
                ],
                case.descriptor,
            );
            let mut ram = Ram::new(0x100);
            ram.load(0, &instruction).unwrap();
            ram.write_u64(case.address, case.memory).unwrap();
            let mut cpu = Cpu::new();
            cpu.reset(0);
            cpu.state_mut().r[1] = case.r1;
            cpu.state_mut().r[2] = case.r2;
            cpu.state_mut().r[3] = case.r3;
            cpu.state_mut().flags = Flags::all();

            assert_eq!(cpu.step(&mut ram), StepResult::Running);
            assert!(!cpu.state().flags.contains(Flags::V));
            assert_eq!(cpu.state().r[2], case.final_r2);
        }
    }

    #[test]
    fn atomic_and_bounds_faults_rollback_overlapping_ext0_updates() {
        let instructions = [
            encoded_form(
                "extralong.fetchadd_x_order_o_rn_s_ea_e",
                &[('z', 3), ('o', 0), ('s', 2), ('e', 0x74)],
                &[0x94],
            ),
            encoded_form(
                "extralong.bnduii_x_rn_l_ea_e_rn_h",
                &[('z', 3), ('l', 1), ('e', 0x74), ('h', 3)],
                &[0x94],
            ),
        ];
        for instruction in instructions {
            let mut ram = Ram::new(0x80);
            ram.load(0, &instruction).unwrap();
            let mut cpu = Cpu::new();
            cpu.reset(0);
            cpu.state_mut().r[1] = 0;
            cpu.state_mut().r[2] = 0x100;
            cpu.state_mut().r[3] = u64::MAX;
            cpu.state_mut().flags = Flags::all();

            assert_eq!(cpu.step(&mut ram), StepResult::Halted);
            assert_eq!(cpu.state().pc, 0);
            assert_eq!(cpu.state().r[2], 0x100);
            assert_eq!(cpu.state().flags, Flags::all());
        }
    }

    #[test]
    fn slot_atomic_reports_address_type_before_alignment_without_slot_access() {
        let instruction = encoded_form(
            "extralong.fetchadd_x_order_o_rn_s_ea_e",
            &[('z', 3), ('o', 0), ('s', 2), ('e', 0x11)],
            &[],
        );
        let mut bus = SlotProbeBus::new(0x9000);
        install_four_level_root(&mut bus.ram);
        map_low_page(&mut bus.ram, 0, 0x8000, PTE_W | PTE_X);
        map_low_page(
            &mut bus.ram,
            1,
            0xa000,
            PTE_W | PTE_CP | PTE_A | PTE_D | PTE_AT,
        );
        bus.ram.load(0x8000, &instruction).unwrap();
        let mut cpu = Cpu::new();
        cpu.reset(0);
        cpu.state_mut().ptcr = PageTableControl::from_raw(0x1001);
        cpu.state_mut().r[1] = 0x1001;
        cpu.state_mut().r[2] = 1;

        assert!(matches!(
            cpu.step_transaction(&mut bus, 0),
            Err(Trap::PageFault {
                context: crate::PageFaultContext {
                    reason: PageFaultReason::AddressType,
                    atomic: true,
                    ..
                },
                ..
            })
        ));
        assert!(bus.slot_requests.is_empty());
    }

    #[test]
    fn slot_fetch_prefetch_and_maintenance_never_issue_slot_transactions() {
        let mut fetch_bus = SlotProbeBus::new(0x6000);
        install_slot_leaf(&mut fetch_bus, 0, 0x8000);
        let mut cpu = Cpu::new();
        cpu.reset(0);
        cpu.state_mut().ptcr = PageTableControl::from_raw(0x1001);
        assert!(matches!(
            cpu.translate_fetch(&mut fetch_bus, 0, 0),
            Err(Trap::PageFault {
                context: crate::PageFaultContext {
                    reason: PageFaultReason::AddressType,
                    ..
                },
                ..
            })
        ));
        assert!(fetch_bus.slot_requests.is_empty());

        for form in ["long.prefetch_ea_e", "long.invdcache_ea_e"] {
            let instruction = encoded_form(form, &[('e', 0x11)], &[]);
            let mut bus = SlotProbeBus::new(0x9000);
            install_four_level_root(&mut bus.ram);
            map_low_page(&mut bus.ram, 0, 0x8000, PTE_W | PTE_X);
            map_low_page(
                &mut bus.ram,
                1,
                0xa000,
                PTE_W | PTE_CP | PTE_A | PTE_D | PTE_AT,
            );
            bus.ram.load(0x8000, &instruction).unwrap();
            let mut cpu = Cpu::new();
            cpu.reset(0);
            cpu.state_mut().ptcr = PageTableControl::from_raw(0x1001);
            cpu.state_mut().r[1] = 0x1000;

            assert!(cpu.step_transaction(&mut bus, 0).is_ok(), "{form}");
            assert!(bus.slot_requests.is_empty(), "{form}");
        }
    }

    #[test]
    fn invpage_validates_only_the_linear_address_without_walking_the_target_page() {
        let instruction = encoded_form("long.invpage_ea_e", &[('e', 0x11)], &[]);
        let mut ram = Ram::new(0x10_000);
        install_four_level_root(&mut ram);
        map_low_page(&mut ram, 0, 0x8000, PTE_W | PTE_X);
        ram.load(0x8000, &instruction).unwrap();
        let mut cpu = Cpu::new();
        cpu.reset(0);
        cpu.state_mut().ptcr = PageTableControl::from_raw(0x1001);
        cpu.state_mut().r[1] = 0x1000; // Deliberately unmapped target page.

        assert_eq!(cpu.step(&mut ram), StepResult::Running);
        assert_eq!(cpu.state().pc, instruction.len() as u64);
        assert_eq!(ram.read_u64(0x4008).unwrap(), 0);
    }

    #[test]
    fn ptquery_returns_the_requested_walk_level_entry() {
        let mut ram = Ram::new(0x10_000);
        install_four_level_root(&mut ram);
        map_low_page(&mut ram, 0, 0x8000, PTE_W | PTE_X);
        map_low_page(&mut ram, 1, 0x9000, PTE_W | PTE_U);
        ram.load(0, &[0xc7, 0xef, 0x09, 0x00]).unwrap(); // PTQUERY 1, R0, R2

        let mut cpu = Cpu::new();
        cpu.reset(0);
        cpu.state_mut().ptcr = PageTableControl::from_raw(0x1000);
        cpu.state_mut().r[0] = 0x1000;
        assert_eq!(cpu.step(&mut ram), StepResult::Running);
        assert_eq!(cpu.state().r[2], 0x9000 | PTE_P | PTE_W | PTE_U);
        assert_eq!(cpu.state().flags, Flags::Z | Flags::N | Flags::C);
    }

    #[test]
    fn ptquery_reserved_level_is_illegal_before_privilege_check() {
        for level in [0, 6, 7] {
            let instruction = encoded_form(
                "long.ptquery_pt_level_i_ea_e_rn_d",
                &[('i', level), ('e', 0), ('d', 2)],
                &[],
            );
            let mut ram = Ram::new(instruction.len());
            ram.load(0, &instruction).unwrap();
            let mut cpu = Cpu::new();
            cpu.reset(0);
            cpu.state_mut().status.remove(crate::Status::PM);

            let result = cpu.step_transaction(&mut ram, 0);
            assert!(
                matches!(
                    result,
                    Err(Trap::IllegalInstruction {
                        cause: crate::trap::IllegalInstructionCause::ReservedEncoding,
                        ..
                    })
                ),
                "level {level} produced {result:?}"
            );
        }
    }

    #[test]
    fn ptquery_noncanonical_address_is_an_unsuccessful_query() {
        let instruction = encoded_form(
            "long.ptquery_pt_level_i_ea_e_rn_d",
            &[('i', 1), ('e', 0), ('d', 2)],
            &[],
        );
        let mut ram = Ram::new(instruction.len());
        ram.load(0, &instruction).unwrap();
        let mut cpu = Cpu::new();
        cpu.reset(0);
        cpu.state_mut().r[0] = 1 << 48;
        cpu.state_mut().r[2] = u64::MAX;
        cpu.state_mut().flags = Flags::all();

        assert_eq!(cpu.step(&mut ram), StepResult::Running);
        assert_eq!(cpu.state().r[2], 0);
        assert!(cpu.state().flags.is_empty());
    }

    #[test]
    fn ordinary_add_preserves_flags() {
        let mut ram = Ram::new(4);
        // short ADD.L R0, R1: payload 000010_0_0000_0001 = 0x0201
        ram.write_u8(0, 0x82).unwrap();
        ram.write_u8(1, 0x01).unwrap();
        let mut cpu = Cpu::new();
        cpu.reset(0);
        cpu.state_mut().r[0] = 2;
        cpu.state_mut().r[1] = 3;
        cpu.state_mut().flags = Flags::C;
        assert_eq!(cpu.step(&mut ram), StepResult::Running);
        assert_eq!(cpu.state().r[1], 5);
        assert_eq!(cpu.state().flags, Flags::C);
    }

    #[test]
    fn lea_accepts_a_signed_immediate_effective_address() {
        let bytes = [0xd1, 0xbb, 0x0e, 0x60, 0x90, 0x01, 0x00];
        let mut ram = Ram::new(bytes.len());
        for (index, byte) in bytes.into_iter().enumerate() {
            ram.write_u8(index as u64, byte).unwrap();
        }
        let mut cpu = Cpu::new();
        cpu.reset(0);

        assert_eq!(cpu.step(&mut ram), StepResult::Running);
        assert_eq!(cpu.state().r[6], 102_496);
        assert_eq!(cpu.state().pc, 7);
    }

    #[test]
    fn lea_returns_the_untranslated_explicit_segment_offset() {
        let bytes = [0xd5, 0xfd, 0x02, 0xa3, 0x00, 0x00, 0x00, 0x00];
        let mut ram = Ram::new(bytes.len());
        ram.load(0, &bytes).unwrap();
        let mut cpu = Cpu::new();
        cpu.reset(0);
        cpu.state_mut().segments.set(
            crate::SegmentSelector::Gs0,
            crate::SegmentRegister::from_raw(0x23_003),
        );
        cpu.state_mut().r[10] = 0xaaaa;

        assert_eq!(cpu.step(&mut ram), StepResult::Running);
        assert_eq!(cpu.state().r[10], 0);
    }

    #[test]
    fn seglea_reports_bounds_with_v_instead_of_trapping() {
        let bytes = [0xcf, 0xc7, 0x85, 0x70, 0xa3, 0x00];
        let mut ram = Ram::new(bytes.len());
        ram.load(0, &bytes).unwrap();
        let mut cpu = Cpu::new();
        cpu.reset(0);
        cpu.state_mut().segments.set(
            crate::SegmentSelector::Gs0,
            crate::SegmentRegister::from_raw(0x23_003),
        );
        cpu.state_mut().r[10] = 0xaaaa;

        assert_eq!(cpu.step(&mut ram), StepResult::Running);
        assert_eq!(cpu.state().r[10], 0xaaaa);
        assert!(cpu.state().flags.contains(Flags::V));
    }

    #[test]
    fn pushp_and_popp_use_the_canonical_pair_index() {
        let mut ram = Ram::new(64);
        ram.write_u8(0, 0x14).unwrap(); // PUSHP 4 selects R8:R9.
        ram.write_u8(1, 0x1c).unwrap(); // POPP 4 restores R9:R8.
        let mut cpu = Cpu::new();
        cpu.reset(0);
        cpu.state_mut().sp = 64;
        cpu.state_mut().r[8] = 0x8888;
        cpu.state_mut().r[9] = 0x9999;

        assert_eq!(cpu.step(&mut ram), StepResult::Running);
        assert_eq!(cpu.state().sp, 48);
        assert_eq!(ram.read_u64(48).unwrap(), 0x9999);
        assert_eq!(ram.read_u64(56).unwrap(), 0x8888);

        cpu.state_mut().r[8] = 0;
        cpu.state_mut().r[9] = 0;
        assert_eq!(cpu.step(&mut ram), StepResult::Running);
        assert_eq!(cpu.state().sp, 64);
        assert_eq!(cpu.state().r[8], 0x8888);
        assert_eq!(cpu.state().r[9], 0x9999);
    }

    #[test]
    fn integer_pair_stack_uses_two_q_slot_transactions_without_byte_fallback() {
        let mut push_bus = SlotProbeBus::new(0x20_000);
        install_four_level_root(&mut push_bus.ram);
        map_low_page(&mut push_bus.ram, 0, 0x8000, PTE_W | PTE_X);
        map_low_page(
            &mut push_bus.ram,
            1,
            0x9000,
            PTE_W | PTE_CP | PTE_A | PTE_D | PTE_AT,
        );
        push_bus.ram.write_u8(0x8000, 0x14).unwrap(); // PUSHP PAIR4
        let mut cpu = Cpu::new();
        cpu.reset(0);
        cpu.state_mut().ptcr = PageTableControl::from_raw(0x1001);
        cpu.state_mut().sp = 0x2000;
        cpu.state_mut().r[8] = 0x8888;
        cpu.state_mut().r[9] = 0x9999;
        push_bus.clear_log();

        assert_eq!(cpu.step(&mut push_bus), StepResult::Running);
        assert_eq!(cpu.state().sp, 0x1ff0);
        assert_eq!(push_bus.slot_requests.len(), 2);
        assert_eq!(push_bus.slot_requests[0].address(), 0x9ff8);
        assert_eq!(
            push_bus.slot_requests[0].write_data(),
            Some(SlotData::Q(0x8888))
        );
        assert_eq!(push_bus.slot_requests[1].address(), 0x9ff0);
        assert_eq!(
            push_bus.slot_requests[1].write_data(),
            Some(SlotData::Q(0x9999))
        );
        assert!(
            push_bus
                .byte_writes
                .iter()
                .all(|&address| !(0x9000..0xa000).contains(&address))
        );

        let mut pop_bus = SlotProbeBus::new(0x20_000);
        install_four_level_root(&mut pop_bus.ram);
        map_low_page(&mut pop_bus.ram, 0, 0x8000, PTE_W | PTE_X);
        map_low_page(
            &mut pop_bus.ram,
            2,
            0xa000,
            PTE_W | PTE_CP | PTE_A | PTE_D | PTE_AT,
        );
        pop_bus.ram.write_u8(0x8000, 0x1c).unwrap(); // POPP PAIR4
        cpu.reset(0);
        cpu.state_mut().ptcr = PageTableControl::from_raw(0x1001);
        cpu.state_mut().sp = 0x2000;
        pop_bus.clear_log();

        assert_eq!(cpu.step(&mut pop_bus), StepResult::Running);
        assert_eq!(cpu.state().sp, 0x2010);
        assert_eq!(pop_bus.slot_requests.len(), 2);
        assert_eq!(pop_bus.slot_requests[0].address(), 0xa000);
        assert_eq!(pop_bus.slot_requests[1].address(), 0xa008);
        assert!(
            pop_bus
                .slot_requests
                .iter()
                .all(|request| request.width() == SlotWidth::Q)
        );
        assert_eq!(cpu.state().r[8], slot_test_data(SlotWidth::Q).as_u64());
        assert_eq!(cpu.state().r[9], slot_test_data(SlotWidth::Q).as_u64());
        assert!(
            pop_bus
                .byte_reads
                .iter()
                .all(|&address| !(0xa000..0xb000).contains(&address))
        );
    }

    #[test]
    fn floating_pair_stack_supports_at1_q_slots() {
        let mut bus = SlotProbeBus::new(0x20_000);
        install_four_level_root(&mut bus.ram);
        map_low_page(&mut bus.ram, 0, 0x8000, PTE_W | PTE_X);
        map_low_page(
            &mut bus.ram,
            1,
            0x9000,
            PTE_W | PTE_CP | PTE_A | PTE_D | PTE_AT,
        );
        bus.ram.write_u8(0x8000, 0x74).unwrap(); // FPUSHP FPAIR4
        let mut cpu = Cpu::new();
        cpu.reset(0);
        cpu.state_mut().ptcr = PageTableControl::from_raw(0x1001);
        cpu.state_mut().sp = 0x2000;
        cpu.state_mut().f[8] = 0x8888;
        cpu.state_mut().f[9] = 0x9999;
        bus.clear_log();

        assert_eq!(cpu.step(&mut bus), StepResult::Running);
        assert_eq!(cpu.state().sp, 0x1ff0);
        assert_eq!(bus.slot_requests.len(), 2);
        assert_eq!(bus.slot_requests[0].address(), 0x9ff8);
        assert_eq!(bus.slot_requests[0].write_data(), Some(SlotData::Q(0x8888)));
        assert_eq!(bus.slot_requests[1].address(), 0x9ff0);
        assert_eq!(bus.slot_requests[1].write_data(), Some(SlotData::Q(0x9999)));
    }

    #[test]
    fn ext0_explicit_segment_indexed_store_uses_base_and_index() {
        let bytes = [0xc8, 0x02, 0xf4, 0x92, 0x02]; // MOV.B R5, [DS:R0 + R2]
        let mut ram = Ram::new(64);
        for (index, byte) in bytes.into_iter().enumerate() {
            ram.write_u8(index as u64, byte).unwrap();
        }
        let mut cpu = Cpu::new();
        cpu.reset(0);
        cpu.state_mut().r[0] = 32;
        cpu.state_mut().r[2] = 3;
        cpu.state_mut().r[5] = 0xaa;

        assert_eq!(cpu.step(&mut ram), StepResult::Running);
        assert_eq!(ram.read_u8(35).unwrap(), 0xaa);
        assert_eq!(cpu.state().pc, 5);
    }

    #[test]
    fn ext0_index_is_scaled_by_the_ea_interpretation_width() {
        let bytes = [0xc8, 0x19, 0x74, 0x92, 0x13]; // MOV.Q R2, [DS:R1 + R3]
        let mut ram = Ram::new(128);
        for (index, byte) in bytes.into_iter().enumerate() {
            ram.write_u8(index as u64, byte).unwrap();
        }
        let mut cpu = Cpu::new();
        cpu.reset(0);
        cpu.state_mut().r[1] = 20;
        cpu.state_mut().r[2] = 0x1122_3344_5566_7788;
        cpu.state_mut().r[3] = 8;

        assert_eq!(cpu.step(&mut ram), StepResult::Running);
        assert_eq!(ram.read_u64(84).unwrap(), 0x1122_3344_5566_7788);
        assert_eq!(ram.read_u64(28).unwrap(), 0);
    }

    #[test]
    fn ext0_index_scaling_covers_all_integer_ea_widths() {
        let cases = [
            ("medium.mov_x_rn_s_ea_e", 0, Size::Byte),
            ("medium.mov_x_rn_s_ea_e", 1, Size::Word),
            ("medium.mov_x_rn_s_ea_e.2", 0, Size::Long),
            ("medium.mov_x_rn_s_ea_e.2", 1, Size::Quad),
        ];
        for (id, selector, size) in cases {
            let bytes = encoded_form(id, &[('z', selector), ('s', 2), ('e', 0x74)], &[0x92, 0x13]);
            let mut ram = Ram::new(0x100);
            ram.load(0, &bytes).unwrap();
            let mut cpu = Cpu::new();
            cpu.reset(0);
            cpu.state_mut().r[1] = 0x80;
            cpu.state_mut().r[2] = 0x1122_3344_5566_77a5;
            cpu.state_mut().r[3] = 2;

            assert_eq!(cpu.step(&mut ram), StepResult::Running, "{id}");
            let address = 0x80 + size.bytes() as u64 * 2;
            assert_eq!(
                super::read_bus(&mut ram, address, size).unwrap(),
                cpu.state().r[2] & super::size_mask(size),
                "{id}"
            );
        }
    }

    #[test]
    fn ext0_index_auto_update_changes_one_element_before_scaling() {
        for (descriptor, address, final_index) in [([0x90, 0x13], 0x50, 3), ([0x91, 0x13], 0x48, 1)]
        {
            let bytes = encoded_form(
                "medium.mov_x_rn_s_ea_e.2",
                &[('z', 1), ('s', 2), ('e', 0x74)],
                &descriptor,
            );
            let mut ram = Ram::new(0x100);
            ram.load(0, &bytes).unwrap();
            let mut cpu = Cpu::new();
            cpu.reset(0);
            cpu.state_mut().r[1] = 0x40;
            cpu.state_mut().r[2] = 0x1122_3344_5566_7788;
            cpu.state_mut().r[3] = 2;

            assert_eq!(cpu.step(&mut ram), StepResult::Running);
            assert_eq!(ram.read_u64(address).unwrap(), cpu.state().r[2]);
            assert_eq!(cpu.state().r[3], final_index);
        }
    }

    #[test]
    fn read_modify_write_executors_resolve_ext0_base_once() {
        let cases = [
            (
                encoded_form(
                    "medium.add_x_rn_s_ea_e.2",
                    &[('z', 1), ('s', 2), ('e', 0x74)],
                    &[0x8c],
                ),
                3,
                5,
                8,
            ),
            (
                encoded_form("medium.inc_x_ea.2", &[('z', 1), ('e', 0x74)], &[0x8c]),
                0,
                5,
                6,
            ),
            (
                encoded_form(
                    "long.shl_x_imm6_i_ea_e",
                    &[('z', 3), ('i', 1), ('e', 0x74)],
                    &[0x8c],
                ),
                0,
                5,
                10,
            ),
            (
                encoded_form("long.bset_imm6_i_ea_e", &[('i', 1), ('e', 0x74)], &[0x8c]),
                0,
                4,
                6,
            ),
            (
                encoded_form(
                    "long.maxu_x_rn_s_ea_e",
                    &[('z', 3), ('s', 2), ('e', 0x74)],
                    &[0x8c],
                ),
                7,
                5,
                7,
            ),
            (
                encoded_form("medium.revbyte_q_ea", &[('e', 0x74)], &[0x8c]),
                0,
                0x0102_0304_0506_0708,
                0x0807_0605_0403_0201,
            ),
        ];

        for (instruction, source, initial, expected) in cases {
            let mut ram = Ram::new(0x200);
            ram.load(0, &instruction).unwrap();
            ram.write_u64(0x80, initial).unwrap();
            ram.write_u64(0x88, 0xfeed_face_cafe_beef).unwrap();
            let mut cpu = Cpu::new();
            cpu.reset(0);
            cpu.state_mut().r[1] = 0x80;
            cpu.state_mut().r[2] = source;

            assert_eq!(cpu.step(&mut ram), StepResult::Running);
            assert_eq!(ram.read_u64(0x80).unwrap(), expected);
            assert_eq!(ram.read_u64(0x88).unwrap(), 0xfeed_face_cafe_beef);
            assert_eq!(cpu.state().r[1], 0x88);
        }
    }

    #[test]
    fn read_modify_write_resolves_ext0_index_once() {
        let instruction =
            encoded_form("medium.inc_x_ea.2", &[('z', 1), ('e', 0x74)], &[0x90, 0x13]);
        let mut ram = Ram::new(0x200);
        ram.load(0, &instruction).unwrap();
        ram.write_u64(0x90, 5).unwrap();
        ram.write_u64(0x98, 0xfeed_face_cafe_beef).unwrap();
        let mut cpu = Cpu::new();
        cpu.reset(0);
        cpu.state_mut().r[1] = 0x80;
        cpu.state_mut().r[3] = 2;

        assert_eq!(cpu.step(&mut ram), StepResult::Running);
        assert_eq!(ram.read_u64(0x90).unwrap(), 6);
        assert_eq!(ram.read_u64(0x98).unwrap(), 0xfeed_face_cafe_beef);
        assert_eq!(cpu.state().r[3], 3);
    }

    #[test]
    fn exchange_reuses_resolved_ea_and_final_register_write_wins_over_auto_update() {
        for (id, register_field, expected_memory) in [
            ("medium.xchg_x_rn_s_ea_e.2", 's', 0x80),
            ("medium.xchg_x_ea_e_rn_d.2", 'd', 0x88),
        ] {
            let instruction =
                encoded_form(id, &[('z', 1), (register_field, 2), ('e', 0x74)], &[0x94]);
            let mut ram = Ram::new(0x200);
            ram.load(0, &instruction).unwrap();
            ram.write_u64(0x80, 0x1111).unwrap();
            let mut cpu = Cpu::new();
            cpu.reset(0);
            cpu.state_mut().r[2] = 0x80;

            assert_eq!(cpu.step(&mut ram), StepResult::Running, "{id}");
            assert_eq!(ram.read_u64(0x80).unwrap(), expected_memory, "{id}");
            assert_eq!(cpu.state().r[2], 0x1111, "{id}");
        }

        for (id, register_field, expected_memory) in [
            ("medium.xchg_x_rn_s_ea_e.2", 's', 2),
            ("medium.xchg_x_ea_e_rn_d.2", 'd', 3),
        ] {
            let instruction = encoded_form(
                id,
                &[('z', 1), (register_field, 2), ('e', 0x74)],
                &[0x90, 0x12],
            );
            let mut ram = Ram::new(0x200);
            ram.load(0, &instruction).unwrap();
            ram.write_u64(0x90, 0x1111).unwrap();
            let mut cpu = Cpu::new();
            cpu.reset(0);
            cpu.state_mut().r[1] = 0x80;
            cpu.state_mut().r[2] = 2;

            assert_eq!(cpu.step(&mut ram), StepResult::Running, "{id}");
            assert_eq!(ram.read_u64(0x90).unwrap(), expected_memory, "{id}");
            assert_eq!(cpu.state().r[2], 0x1111, "{id}");
        }
    }

    #[test]
    fn zero_count_shift_still_reads_writes_faults_and_updates_once() {
        let instruction = encoded_form(
            "long.shl_x_imm6_i_ea_e",
            &[('z', 3), ('i', 0), ('e', 0x74)],
            &[0x8c],
        );
        let mut bus = SlotProbeBus::new(0x200);
        bus.ram.load(0, &instruction).unwrap();
        bus.ram.write_u64(0x80, 0x1122_3344_5566_7788).unwrap();
        bus.clear_log();
        let mut cpu = Cpu::new();
        cpu.reset(0);
        cpu.state_mut().r[1] = 0x80;

        assert_eq!(cpu.step(&mut bus), StepResult::Running);
        assert_eq!(bus.ram.read_u64(0x80).unwrap(), 0x1122_3344_5566_7788);
        assert_eq!(cpu.state().r[1], 0x88);
        assert_eq!(
            bus.byte_reads
                .iter()
                .filter(|&&address| (0x80..0x88).contains(&address))
                .count(),
            8
        );
        assert_eq!(
            bus.byte_writes
                .iter()
                .filter(|&&address| (0x80..0x88).contains(&address))
                .count(),
            8
        );

        let mut bus = SlotProbeBus::new(0x200);
        bus.ram.load(0, &instruction).unwrap();
        bus.ram.write_u64(0x80, 0x1122_3344_5566_7788).unwrap();
        bus.read_only_from = Some(0x80);
        bus.clear_log();
        let mut cpu = Cpu::new();
        cpu.reset(0);
        cpu.state_mut().r[1] = 0x80;

        assert!(matches!(
            cpu.step(&mut bus),
            StepResult::Trap(_) | StepResult::Halted
        ));
        assert_eq!(cpu.state().pc, 0);
        assert_eq!(cpu.state().r[1], 0x80);
        assert_eq!(bus.ram.read_u64(0x80).unwrap(), 0x1122_3344_5566_7788);
        assert_eq!(
            bus.byte_reads
                .iter()
                .filter(|&&address| (0x80..0x88).contains(&address))
                .count(),
            8
        );
        assert_eq!(
            bus.byte_writes
                .iter()
                .filter(|&&address| (0x80..0x88).contains(&address))
                .copied()
                .collect::<Vec<_>>(),
            vec![0x80]
        );
    }

    #[test]
    fn ext0_same_register_base_and_index_follow_term_order() {
        for (descriptor, address, final_register) in [([0x90, 0x11], 36, 5), ([0x91, 0x11], 28, 3)]
        {
            let bytes = encoded_form(
                "medium.mov_x_rn_s_ea_e.2",
                &[('z', 1), ('s', 2), ('e', 0x74)],
                &descriptor,
            );
            let mut ram = Ram::new(0x80);
            ram.load(0, &bytes).unwrap();
            let mut cpu = Cpu::new();
            cpu.reset(0);
            cpu.state_mut().r[1] = 4;
            cpu.state_mut().r[2] = 0x8877_6655_4433_2211;

            assert_eq!(cpu.step(&mut ram), StepResult::Running);
            assert_eq!(ram.read_u64(address).unwrap(), cpu.state().r[2]);
            assert_eq!(cpu.state().r[1], final_register);
        }
    }

    #[test]
    fn ext0_uses_fpu_and_extension_destination_widths() {
        let fmov = encoded_form(
            "long.fmov_x_fn_s_ea_d",
            &[('z', 0), ('s', 0), ('e', 0x74)],
            &[0x92, 0x13],
        );
        let extend = encoded_form(
            "medium.extzq_b_rn_s_ea_e",
            &[('s', 2), ('e', 0x74)],
            &[0x92, 0x13],
        );
        let mut ram = Ram::new(0x100);
        ram.load(0, &fmov).unwrap();
        ram.load(fmov.len() as u64, &extend).unwrap();
        let mut cpu = Cpu::new();
        cpu.reset(0);
        cpu.state_mut().r[1] = 0x80;
        cpu.state_mut().r[2] = 0xa5;
        cpu.state_mut().r[3] = 2;
        cpu.state_mut().f[0] = 0xffff_ffff_3f80_0000;

        assert_eq!(cpu.step(&mut ram), StepResult::Running);
        assert_eq!(ram.read_u32(0x88).unwrap(), 0x3f80_0000);
        assert_eq!(ram.read_u32(0x90).unwrap(), 0);
        assert_eq!(cpu.step(&mut ram), StepResult::Running);
        assert_eq!(ram.read_u64(0x90).unwrap(), 0xa5);
    }

    #[test]
    fn memory_destination_uses_its_own_payload_after_an_immediate_source() {
        let bytes = [0xcf, 0xe0, 0xb6, 0x26, 0x18, 0x91]; // MOV.L 24, [R6 - 111]
        let mut ram = Ram::new(300);
        for (index, byte) in bytes.into_iter().enumerate() {
            ram.write_u8(index as u64, byte).unwrap();
        }
        let mut cpu = Cpu::new();
        cpu.reset(0);
        cpu.state_mut().r[6] = 200;

        assert_eq!(cpu.step(&mut ram), StepResult::Running);
        assert_eq!(ram.read_u32(89).unwrap(), 24);
        assert_eq!(ram.read_u32(224).unwrap(), 0);
    }

    #[test]
    fn memory_alu_immediate_starts_after_the_ea_payload() {
        let bytes = encoded_form(
            "long.add_x_imm16s_ea_e",
            &[('z', 3), ('e', 0x20)],
            &[0x10, 0xfe, 0xff],
        );
        let mut ram = Ram::new(0x100);
        ram.load(0, &bytes).unwrap();
        ram.write_u64(0x90, 1).unwrap();
        let mut cpu = Cpu::new();
        cpu.reset(0);
        cpu.state_mut().r[0] = 0x80;

        assert_eq!(cpu.step(&mut ram), StepResult::Running);
        assert_eq!(ram.read_u64(0x90).unwrap(), u64::MAX);
    }

    #[test]
    fn signed_appended_immediates_ignore_extended_record_padding() {
        let add_sp = encoded_form("medium.add_q_ea_sp", &[], &[0xfe, 0xff, 0x7f]);
        let jump = encoded_form("medium.jmp_ea", &[], &[0xfe, 0xff, 0x7f]);

        let mut add_ram = Ram::new(16);
        add_ram.load(0, &add_sp).unwrap();
        let mut cpu = Cpu::new();
        cpu.reset(0);
        cpu.state_mut().sp = 100;
        assert_eq!(cpu.step(&mut add_ram), StepResult::Running);
        assert_eq!(cpu.state().sp, 98);

        let mut jump_ram = Ram::new(16);
        jump_ram.load(0, &jump).unwrap();
        cpu.reset(0);
        assert_eq!(cpu.step(&mut jump_ram), StepResult::Running);
        assert_eq!(cpu.state().pc, jump.len() as u64 - 2);
    }

    #[test]
    fn fused_test_jump_sign_extends_its_actual_displacement_width() {
        let bytes = [0xcb, 0xc5, 0x16, 0x2c, 0xee]; // TESTJEQ.L R12, R12, -18
        let mut ram = Ram::new(32);
        for (index, byte) in bytes.into_iter().enumerate() {
            ram.write_u8(20 + index as u64, byte).unwrap();
        }
        let mut cpu = Cpu::new();
        cpu.reset(20);
        cpu.state_mut().r[12] = 0;

        assert_eq!(cpu.step(&mut ram), StepResult::Running);
        assert_eq!(cpu.state().pc, 7);
    }

    #[test]
    fn control_register_unknown_selectors_fault_without_mutation() {
        let mut ram = Ram::new(64);
        let mut cpu = Cpu::new();
        cpu.reset(0x20);
        cpu.state_mut().r[4] = 0xfeed_face_cafe_beef;

        let rdcr = decoded_form("long.rdcr_ea_rn_d", &[('d', 4)], &0xffff_u16.to_le_bytes());
        let before = cpu.state().clone();
        assert_eq!(
            cpu.execute(&mut ram, 0x20, &rdcr),
            Err(Trap::InvalidControlState {
                pc: 0x20,
                cause: InvalidControlCause::InvalidSelector,
            })
        );
        assert_eq!(cpu.state(), &before);

        let wrcr = decoded_form("long.wrcr_rn_s_ea", &[('s', 4)], &0xffff_u16.to_le_bytes());
        assert_eq!(
            cpu.execute(&mut ram, 0x20, &wrcr),
            Err(Trap::InvalidControlState {
                pc: 0x20,
                cause: InvalidControlCause::InvalidSelector,
            })
        );
        assert_eq!(cpu.state(), &before);
    }

    #[test]
    fn control_register_images_are_validated_before_commit() {
        let mut ram = Ram::new(64);
        let mut cpu = Cpu::new();
        cpu.reset(0x20);
        cpu.state_mut().ptcr = PageTableControl::from_raw(0x1001);
        cpu.state_mut().ascr = AddressSpaceControl::from_raw((7 << 16) | 1);

        let wrcr_ptcr = decoded_form("long.wrcr_rn_s_ea", &[('s', 1)], &0_u16.to_le_bytes());
        for (image, cause) in [
            (1 << 1, InvalidControlCause::ReservedBits),
            (2 << 8, InvalidControlCause::InvalidImage),
            ((1 << 48) | 1, InvalidControlCause::InvalidImage),
        ] {
            cpu.state_mut().r[1] = image;
            let before = cpu.state().clone();
            assert_eq!(
                cpu.execute(&mut ram, 0x20, &wrcr_ptcr),
                Err(Trap::InvalidControlState { pc: 0x20, cause })
            );
            assert_eq!(cpu.state(), &before);
        }

        let valid_wide_ptcr = (1 << 52) | (1 << 8) | 1;
        cpu.state_mut().r[1] = valid_wide_ptcr;
        assert_eq!(
            cpu.execute(&mut ram, 0x20, &wrcr_ptcr),
            Ok(StepResult::Running)
        );
        assert_eq!(cpu.state().ptcr.raw(), valid_wide_ptcr);

        let wrcr_ascr = decoded_form("long.wrcr_rn_s_ea", &[('s', 1)], &1_u16.to_le_bytes());
        cpu.state_mut().r[1] = 1 << 1;
        let before = cpu.state().clone();
        assert_eq!(
            cpu.execute(&mut ram, 0x20, &wrcr_ascr),
            Err(Trap::InvalidControlState {
                pc: 0x20,
                cause: InvalidControlCause::ReservedBits,
            })
        );
        assert_eq!(cpu.state(), &before);

        let wrcr_spc = decoded_form("long.wrcr_rn_s_ea", &[('s', 1)], &0x0100_u16.to_le_bytes());
        cpu.state_mut().r[1] = 0x123;
        let before = cpu.state().clone();
        assert_eq!(
            cpu.execute(&mut ram, 0x20, &wrcr_spc),
            Err(Trap::InvalidControlState {
                pc: 0x20,
                cause: InvalidControlCause::InvalidImage,
            })
        );
        assert_eq!(cpu.state(), &before);

        let invalid_segment = 0xffff_ffff_ffff_f000 | (0x1f << 7) | (0x3f << 1);
        assert!(!SegmentRegister::from_raw(invalid_segment).valid());
        let wrcr_scs = decoded_form("long.wrcr_rn_s_ea", &[('s', 1)], &0x0101_u16.to_le_bytes());
        cpu.state_mut().r[1] = invalid_segment;
        let before = cpu.state().clone();
        assert_eq!(
            cpu.execute(&mut ram, 0x20, &wrcr_scs),
            Err(Trap::InvalidControlState {
                pc: 0x20,
                cause: InvalidControlCause::InvalidImage,
            })
        );
        assert_eq!(cpu.state(), &before);

        let wrcr_ssp = decoded_form("long.wrcr_rn_s_ea", &[('s', 1)], &0x0201_u16.to_le_bytes());
        cpu.state_mut().r[1] = 0x41;
        let before = cpu.state().clone();
        assert_eq!(
            cpu.execute(&mut ram, 0x20, &wrcr_ssp),
            Err(Trap::InvalidControlState {
                pc: 0x20,
                cause: InvalidControlCause::InvalidImage,
            })
        );
        assert_eq!(cpu.state(), &before);
    }

    #[test]
    fn translation_switches_reuse_ptcr_validation_and_commit_atomically() {
        let mut ram = Ram::new(64);
        let mut cpu = Cpu::new();
        cpu.reset(0x20);
        cpu.state_mut().ptcr = PageTableControl::from_raw(0x1001);
        cpu.state_mut().ascr = AddressSpaceControl::from_raw((7 << 16) | 1);
        cpu.state_mut().r[1] = 2 << 8;
        cpu.state_mut().r[2] = 9;

        for instruction in [
            decoded_form("long.swpt_rn_p", &[('p', 1)], &[]),
            decoded_form("long.swpta_rn_p_rn_a", &[('p', 1), ('a', 2)], &[]),
        ] {
            let before = cpu.state().clone();
            assert_eq!(
                cpu.execute(&mut ram, 0x20, &instruction),
                Err(Trap::InvalidControlState {
                    pc: 0x20,
                    cause: InvalidControlCause::InvalidImage,
                })
            );
            assert_eq!(cpu.state(), &before);
        }
    }

    #[test]
    fn urctl_validates_structural_images_and_sysret_validates_the_complete_bank() {
        let mut ram = Ram::new(64);
        let mut cpu = Cpu::new();
        cpu.reset(0x20);
        let wrcr_urctl = decoded_form("long.wrcr_rn_s_ea", &[('s', 1)], &0x010d_u16.to_le_bytes());

        cpu.state_mut().r[1] = 1 << 4;
        let before = cpu.state().clone();
        assert_eq!(
            cpu.execute(&mut ram, 0x20, &wrcr_urctl),
            Err(Trap::InvalidControlState {
                pc: 0x20,
                cause: InvalidControlCause::ReservedBits,
            })
        );
        assert_eq!(cpu.state(), &before);

        cpu.state_mut().r[1] = super::URCTL_VALID | (u64::from(Status::PM.bits()) << 16);
        let before = cpu.state().clone();
        assert_eq!(
            cpu.execute(&mut ram, 0x20, &wrcr_urctl),
            Err(Trap::InvalidControlState {
                pc: 0x20,
                cause: InvalidControlCause::InvalidImage,
            })
        );
        assert_eq!(cpu.state(), &before);

        let invalid_segment = 0xffff_ffff_ffff_f000 | (0x1f << 7) | (0x3f << 1);
        let invalid_segment = SegmentRegister::from_raw(invalid_segment);
        for (urcs, urds, urss) in [
            (
                invalid_segment,
                SegmentRegister::disabled(),
                SegmentRegister::disabled(),
            ),
            (
                SegmentRegister::disabled(),
                invalid_segment,
                SegmentRegister::disabled(),
            ),
            (
                SegmentRegister::disabled(),
                SegmentRegister::disabled(),
                invalid_segment,
            ),
        ] {
            cpu.state_mut().urcs = urcs;
            cpu.state_mut().urds = urds;
            cpu.state_mut().urss = urss;
            cpu.state_mut().r[1] = super::URCTL_VALID;
            let before = cpu.state().clone();
            assert_eq!(
                cpu.execute(&mut ram, 0x20, &wrcr_urctl),
                Err(Trap::InvalidControlState {
                    pc: 0x20,
                    cause: InvalidControlCause::InvalidImage,
                })
            );
            assert_eq!(cpu.state(), &before);
        }

        cpu.state_mut().urcs = SegmentRegister::disabled();
        cpu.state_mut().urds = SegmentRegister::disabled();
        cpu.state_mut().urss = SegmentRegister::from_raw(3);
        cpu.state_mut().urpc = 0x20;
        cpu.state_mut().ursp = 0x1000;
        let control =
            super::URCTL_VALID | u64::from(Flags::C.bits()) | (u64::from(Status::IE.bits()) << 16);
        cpu.state_mut().r[1] = control;
        assert_eq!(
            cpu.execute(&mut ram, 0x20, &wrcr_urctl),
            Ok(StepResult::Running)
        );
        assert_eq!(cpu.state().urctl, control);

        let sysret = decoded_form("extrashort.sysret", &[], &[]);
        let before = cpu.state().clone();
        assert_eq!(
            cpu.execute(&mut ram, 0x20, &sysret),
            Err(Trap::InvalidControlState {
                pc: 0x20,
                cause: InvalidControlCause::InvalidImage,
            })
        );
        assert_eq!(cpu.state(), &before);
    }

    #[test]
    fn control_register_selector_writes_supervisor_entry_pc() {
        let bytes = [0xcf, 0xef, 0x47, 0x10, 0x00, 0x01]; // WRCR R0, SPC
        let mut ram = Ram::new(bytes.len());
        for (index, byte) in bytes.into_iter().enumerate() {
            ram.write_u8(index as u64, byte).unwrap();
        }
        let mut cpu = Cpu::new();
        cpu.reset(0);
        cpu.state_mut().r[0] = 0x1230;

        assert_eq!(cpu.step(&mut ram), StepResult::Running);
        assert_eq!(cpu.state().spc, 0x1230);
    }

    #[test]
    fn decrement_jump_reads_a_quad_target_through_its_pc_relative_ea() {
        let mut ram = Ram::new(32);
        for (index, byte) in [0xcb, 0xc3, 0x81, 0xe4, 0xf4].into_iter().enumerate() {
            ram.write_u8(16 + index as u64, byte).unwrap();
        }
        ram.write_u64(4, 4).unwrap();
        let mut cpu = Cpu::new();
        cpu.reset(16);
        cpu.state_mut().r[3] = 2;

        assert_eq!(cpu.step(&mut ram), StepResult::Running);
        assert_eq!(cpu.state().r[3], 1);
        assert_eq!(cpu.state().pc, 4);
    }

    #[test]
    fn increment_jump_ne_compares_the_incremented_index_with_the_bound() {
        let bytes = [0xcf, 0xf1, 0x0c, 0x04, 0xe4, 0x11];
        let mut ram = Ram::new(32);
        for (index, byte) in bytes.into_iter().enumerate() {
            ram.write_u8(index as u64, byte).unwrap();
        }
        ram.write_u64(17, 17).unwrap();
        let mut cpu = Cpu::new();
        cpu.reset(0);
        cpu.state_mut().r[0] = 0;
        cpu.state_mut().r[9] = 2;
        cpu.state_mut().flags = Flags::empty();

        assert_eq!(cpu.step(&mut ram), StepResult::Running);
        assert_eq!(cpu.state().r[0], 1);
        assert_eq!(cpu.state().pc, 17);
        assert_eq!(cpu.state().flags, Flags::empty());
    }

    #[test]
    fn increment_jump_stops_at_the_bound_before_accessing_its_target() {
        let bytes = [0xcf, 0xf1, 0x08, 0x04, 0xe4, 0x11];
        let mut ram = Ram::new(17);
        for (index, byte) in bytes.into_iter().enumerate() {
            ram.write_u8(index as u64, byte).unwrap();
        }
        let mut cpu = Cpu::new();
        cpu.reset(0);
        cpu.state_mut().r[0] = 1;
        cpu.state_mut().r[9] = 2;
        cpu.state_mut().flags = Flags::Z;

        assert_eq!(cpu.step(&mut ram), StepResult::Running);
        assert_eq!(cpu.state().r[0], 2);
        assert_eq!(cpu.state().pc, bytes.len() as u64);
        assert_eq!(cpu.state().flags, Flags::Z);
    }

    #[test]
    fn long_call_and_return_round_trip_the_atomic_far_frame_layout() {
        let lcall = decoded_form("long.lcall_rn_r_ea_e", &[('r', 1), ('e', 0)], &[]);
        let lret = decoded_form("extrashort.lret", &[], &[]);
        let mut ram = Ram::new(0x400);
        let mut cpu = Cpu::new();
        cpu.reset(0x20);
        let old_cs = SegmentRegister::from_raw(4);
        let new_cs = SegmentRegister::from_raw(2);
        cpu.state_mut().segments.set(SegmentSelector::Cs, old_cs);
        cpu.state_mut().sp = 0x180;
        cpu.state_mut().r[0] = 0x40;
        cpu.state_mut().r[1] = new_cs.raw();

        assert_eq!(cpu.execute(&mut ram, 0x20, &lcall), Ok(StepResult::Running));
        assert_eq!(cpu.state().sp, 0x170);
        assert_eq!(cpu.state().segments.cs(), new_cs);
        assert_eq!(cpu.state().pc, 0x40);
        assert_eq!(ram.read_u64(0x170).unwrap(), 0x24);
        assert_eq!(ram.read_u64(0x178).unwrap(), old_cs.raw());

        assert_eq!(cpu.execute(&mut ram, 0x40, &lret), Ok(StepResult::Running));
        assert_eq!(cpu.state().sp, 0x180);
        assert_eq!(cpu.state().segments.cs(), old_cs);
        assert_eq!(cpu.state().pc, 0x24);
    }

    #[test]
    fn long_call_probes_both_old_stack_stores_before_memory_or_state_commit() {
        let lcall = decoded_form("long.lcall_rn_r_ea_e", &[('r', 1), ('e', 0)], &[]);
        let mut ram = Ram::new(0x9000);
        install_four_level_root(&mut ram);
        map_low_page(&mut ram, 1, 0x5000, PTE_W);
        map_low_page(&mut ram, 2, 0x6000, PTE_X);
        let sentinel = 0xfeed_face_dead_beef;
        ram.write_u64(0x5000, sentinel).unwrap();

        let mut cpu = Cpu::new();
        cpu.reset(0x80);
        cpu.state_mut().ptcr = PageTableControl::from_raw(0x1001);
        cpu.state_mut().sp = 0x1008;
        cpu.state_mut().r[0] = 0x2000;
        cpu.state_mut().r[1] = SegmentRegister::disabled().raw();
        let before = cpu.state().clone();

        assert!(matches!(
            cpu.execute(&mut ram, 0x80, &lcall),
            Err(Trap::PageFault {
                context: crate::PageFaultContext {
                    effective_address: 0x0ff8,
                    reason: PageFaultReason::NotPresent,
                    access_kind: AccessKind::Write,
                    segment: Some(SegmentSelector::Ss),
                    ..
                },
                ..
            })
        ));
        assert_eq!(cpu.state(), &before);
        assert_eq!(ram.read_u64(0x5000).unwrap(), sentinel);
    }

    #[test]
    fn long_return_validates_the_complete_frame_and_target_before_committing_state() {
        let lret = decoded_form("extrashort.lret", &[], &[]);
        let mut ram = Ram::new(0x9000);
        install_four_level_root(&mut ram);
        map_low_page(&mut ram, 0, 0x5000, PTE_W);
        ram.write_u64(0x5100, 0x2000).unwrap();
        ram.write_u64(0x5108, SegmentRegister::disabled().raw())
            .unwrap();

        let mut cpu = Cpu::new();
        cpu.reset(0x80);
        cpu.state_mut().ptcr = PageTableControl::from_raw(0x1001);
        cpu.state_mut().sp = 0x100;
        let before = cpu.state().clone();

        assert!(matches!(
            cpu.execute(&mut ram, 0x80, &lret),
            Err(Trap::PageFault {
                context: crate::PageFaultContext {
                    effective_address: 0x2000,
                    reason: PageFaultReason::NotPresent,
                    access_kind: AccessKind::InstructionFetch,
                    segment: Some(SegmentSelector::Cs),
                    ..
                },
                ..
            })
        ));
        assert_eq!(cpu.state(), &before);
    }

    #[test]
    fn memory_to_memory_compare_uses_each_ea_payload() {
        let bytes = [0xcf, 0xe1, 0xf0, 0x60, 0x40, 0x28];
        let mut ram = Ram::new(256);
        for (index, byte) in bytes.into_iter().enumerate() {
            ram.write_u8(index as u64, byte).unwrap();
        }
        ram.write_u64(192, 7).unwrap();
        ram.write_u64(168, 9).unwrap();
        let mut cpu = Cpu::new();
        cpu.reset(0);
        cpu.state_mut().sp = 128;

        assert_eq!(cpu.step(&mut ram), StepResult::Running);
        assert!(!cpu.state().flags.contains(Flags::Z));
        assert_eq!(cpu.state().pc, bytes.len() as u64);
    }

    #[test]
    fn register_to_ea_extend_reads_the_source_register() {
        let bytes = [0xc3, 0x56, 0x01]; // EXTZQ.B R12, R1
        let mut ram = Ram::new(bytes.len());
        for (index, byte) in bytes.into_iter().enumerate() {
            ram.write_u8(index as u64, byte).unwrap();
        }
        let mut cpu = Cpu::new();
        cpu.reset(0);
        cpu.state_mut().r[12] = 1;
        cpu.state_mut().r[1] = 81;

        assert_eq!(cpu.step(&mut ram), StepResult::Running);
        assert_eq!(cpu.state().r[1], 1);
    }

    #[test]
    fn current_size_selector_executes_quad_shift_width() {
        let bytes = [0xc7, 0xed, 0xc6, 0x01]; // SHL.Q 12, R1
        let mut ram = Ram::new(bytes.len());
        for (index, byte) in bytes.into_iter().enumerate() {
            ram.write_u8(index as u64, byte).unwrap();
        }
        let mut cpu = Cpu::new();
        cpu.reset(0);
        cpu.state_mut().r[1] = 16;

        assert_eq!(cpu.step(&mut ram), StepResult::Running);
        assert_eq!(cpu.state().r[1], 0x1_0000);
    }

    #[test]
    fn canonical_popp_pair_seven_is_not_reinterpreted_by_following_opcode() {
        let mut ram = Ram::new(32);
        ram.load(0, &[0x1f, 0x65]).unwrap(); // POPP PAIR7; CLR.Q R5
        ram.write_u64(16, 0x1111).unwrap();
        ram.write_u64(24, 0x2222).unwrap();
        let mut cpu = Cpu::new();
        cpu.reset(0);
        cpu.state_mut().sp = 16;
        cpu.state_mut().r[5] = u64::MAX;

        assert_eq!(cpu.step(&mut ram), StepResult::Running);
        assert_eq!(cpu.state().pc, 1);
        assert_eq!(cpu.state().sp, 32);
        assert_eq!((cpu.state().r[14], cpu.state().r[15]), (0x2222, 0x1111));
        assert_eq!(cpu.step(&mut ram), StepResult::Running);
        assert_eq!(cpu.state().pc, 2);
        assert_eq!(cpu.state().r[5], 0);
    }

    #[test]
    fn fpu_binary_uses_soft_effects_zeroes_s_upper_bits_and_accrues_fflags() {
        let add = encoded_form(
            "medium.fadd_x_fn_s_fn_d",
            &[('z', 0), ('s', 1), ('d', 0)],
            &[],
        );
        let divide = encoded_form(
            "medium.fdiv_x_fn_s_fn_d",
            &[('z', 1), ('s', 3), ('d', 2)],
            &[],
        );
        let mut ram = Ram::new(add.len() + divide.len());
        ram.load(0, &add).unwrap();
        ram.load(add.len() as u64, &divide).unwrap();
        let mut cpu = Cpu::new();
        cpu.reset(0);
        cpu.state_mut().f[0] = 0xffff_ffff_3f80_0000;
        cpu.state_mut().f[1] = 0x4000_0000;
        cpu.state_mut().f[2] = 1.0_f64.to_bits();
        cpu.state_mut().f[3] = 0.0_f64.to_bits();
        cpu.state_mut().fflags = crate::fpu::env::FpCauses::NV.bits();

        assert_eq!(cpu.step(&mut ram), StepResult::Running);
        assert_eq!(cpu.state().f[0], 0x4040_0000);
        assert_eq!(cpu.state().fflags, crate::fpu::env::FpCauses::NV.bits());
        assert_eq!(cpu.step(&mut ram), StepResult::Running);
        assert_eq!(cpu.state().f[2], f64::INFINITY.to_bits());
        assert_eq!(
            cpu.state().fflags,
            crate::fpu::env::FpCauses::NV
                .union(crate::fpu::env::FpCauses::DZ)
                .bits()
        );
    }

    #[test]
    fn enabled_fpu_fault_is_typed_and_precedes_every_architectural_commit() {
        let bytes = encoded_form(
            "medium.fdiv_x_fn_s_fn_d",
            &[('z', 1), ('s', 1), ('d', 0)],
            &[],
        );
        let instruction = bedrock_isa::decode(&bytes).unwrap();
        let mut ram = Ram::new(bytes.len());
        let mut cpu = Cpu::new();
        cpu.reset(0);
        cpu.state_mut().f[0] = 1.0_f64.to_bits();
        cpu.state_mut().f[1] = 0;
        cpu.state_mut().fstatus = crate::fpu::env::FpCauses::DZ.bits();
        cpu.state_mut().fflags = crate::fpu::env::FpCauses::NV.bits();
        cpu.state_mut().flags = Flags::C | Flags::Z;
        let before = cpu.state().clone();

        assert!(matches!(
            cpu.execute(&mut ram, 0, &instruction),
            Err(crate::Trap::FloatingPointFault { causes, .. })
                if causes == crate::fpu::env::FpCauses::DZ
        ));
        assert_eq!(cpu.state(), &before);
    }

    #[test]
    fn fpu_unary_memory_destination_fault_precedes_enabled_fp_fault() {
        let bytes = encoded_form(
            "long.fsqrt_x_fn_s_ea_d",
            &[('z', 1), ('s', 0), ('e', 0x11)],
            &[],
        );
        let instruction = bedrock_isa::decode(&bytes).unwrap();
        let mut ram = Ram::new(0x10_000);
        install_four_level_root(&mut ram);
        let mut cpu = Cpu::new();
        cpu.reset(0);
        cpu.state_mut().ptcr = PageTableControl::from_raw(0x1001);
        cpu.state_mut().r[1] = 0x1000;
        cpu.state_mut().f[0] = (-1.0_f64).to_bits();
        cpu.state_mut().fstatus = crate::fpu::env::FpCauses::NV.bits();
        let before = cpu.state().clone();

        assert!(matches!(
            cpu.execute(&mut ram, 0, &instruction),
            Err(Trap::PageFault {
                context: crate::PageFaultContext {
                    reason: PageFaultReason::NotPresent,
                    access_kind: AccessKind::Write,
                    access_size: Some(4),
                    operand: Some(1),
                    ..
                },
                ..
            })
        ));
        assert_eq!(cpu.state(), &before);
    }

    #[test]
    fn fpu_fault_after_at1_destination_preflight_issues_no_slot_transaction() {
        let bytes = encoded_form(
            "long.fsqrt_x_fn_s_ea_d",
            &[('z', 1), ('s', 0), ('e', 0x11)],
            &[],
        );
        let instruction = bedrock_isa::decode(&bytes).unwrap();
        let mut bus = SlotProbeBus::new(0x10_000);
        install_four_level_root(&mut bus.ram);
        map_low_page(
            &mut bus.ram,
            1,
            0x9000,
            PTE_W | PTE_CP | PTE_A | PTE_D | PTE_AT,
        );
        let mut cpu = Cpu::new();
        cpu.reset(0);
        cpu.state_mut().ptcr = PageTableControl::from_raw(0x1001);
        cpu.state_mut().r[1] = 0x1000;
        cpu.state_mut().f[0] = (-1.0_f64).to_bits();
        cpu.state_mut().fstatus = crate::fpu::env::FpCauses::NV.bits();

        assert!(matches!(
            cpu.execute(&mut bus, 0, &instruction),
            Err(Trap::FloatingPointFault { causes, .. })
                if causes == crate::fpu::env::FpCauses::NV
        ));
        assert!(bus.slot_requests.is_empty());
    }

    #[test]
    fn illegal_destination_overlap_precedes_operand_and_fpu_state_access() {
        let divmod = encoded_form(
            "extralong.divmodu_x_ea_e_rn_q_rn_r",
            &[('z', 3), ('e', 0x10), ('q', 1), ('r', 1)],
            &[],
        );
        let fsincosa = encoded_form(
            "extralong.fsincosa_x_fn_s_fn_d_fn_c",
            &[('z', 1), ('s', 0), ('d', 2), ('c', 2)],
            &[],
        );
        let mut cpu = Cpu::new();
        cpu.reset(0);
        cpu.state_mut().r[0] = u64::MAX;
        cpu.state_mut().fstatus = 1 << 15;
        let mut ram = Ram::new(8);

        for bytes in [divmod, fsincosa] {
            let instruction = bedrock_isa::decode(&bytes).unwrap();
            assert_eq!(
                cpu.execute(&mut ram, 0, &instruction),
                Err(Trap::IllegalInstruction {
                    pc: 0,
                    cause: crate::trap::IllegalInstructionCause::InvalidOperandRelation,
                })
            );
        }
    }

    #[test]
    fn all_four_fused_opcodes_preserve_encoded_lhs_rhs_destination_order() {
        let cases = [
            ("long.fmadd_x_fn_l_fn_r_fn_d", 10.0_f64),
            ("long.fmsub_x_fn_l_fn_r_fn_d", 2.0_f64),
            ("long.fnmadd_x_fn_l_fn_r_fn_d", -10.0_f64),
            ("long.fnmsub_x_fn_l_fn_r_fn_d", -2.0_f64),
        ];
        for (id, expected) in cases {
            let bytes = encoded_form(id, &[('z', 1), ('l', 1), ('r', 2), ('d', 0)], &[]);
            let mut ram = Ram::new(bytes.len());
            ram.load(0, &bytes).unwrap();
            let mut cpu = Cpu::new();
            cpu.reset(0);
            cpu.state_mut().f[0] = 4.0_f64.to_bits();
            cpu.state_mut().f[1] = 2.0_f64.to_bits();
            cpu.state_mut().f[2] = 3.0_f64.to_bits();
            assert_eq!(cpu.step(&mut ram), StepResult::Running, "{id}");
            assert_eq!(cpu.state().f[0], expected.to_bits(), "{id}");
        }
    }

    #[test]
    fn base_other_families_cover_memory_result_conversion_compare_and_bounds_masks() {
        let abs = encoded_form(
            "long.fabs_x_fn_s_ea_d",
            &[('z', 0), ('s', 1), ('e', 0x6a)],
            &0x100_u32.to_le_bytes(),
        );
        let class = encoded_form(
            "long.fclass_x_fn_s_rn_d",
            &[('z', 0), ('s', 2), ('d', 3)],
            &[],
        );
        let compare = encoded_form(
            "medium.fcmp_x_fn_s_fn_d",
            &[('z', 1), ('s', 4), ('d', 5)],
            &[],
        );
        let bounds = encoded_form(
            "long.fbndix_x_fn_l_fn_v_fn_h",
            &[('z', 1), ('l', 6), ('v', 7), ('h', 8)],
            &[],
        );
        let mut program = Vec::new();
        program.extend_from_slice(&abs);
        program.extend_from_slice(&class);
        program.extend_from_slice(&compare);
        program.extend_from_slice(&bounds);
        let mut ram = Ram::new(0x200);
        ram.load(0, &program).unwrap();
        let mut cpu = Cpu::new();
        cpu.reset(0);
        cpu.state_mut().f[1] = 0xffff_ffff_bfc0_0000;
        cpu.state_mut().f[2] = 0x7f80_0001;
        cpu.state_mut().f[4] = 2.0_f64.to_bits();
        cpu.state_mut().f[5] = 1.0_f64.to_bits();
        cpu.state_mut().f[6] = 0.0_f64.to_bits();
        cpu.state_mut().f[7] = 1.0_f64.to_bits();
        cpu.state_mut().f[8] = 1.0_f64.to_bits();
        cpu.state_mut().flags = Flags::C | Flags::N;

        assert_eq!(cpu.step(&mut ram), StepResult::Running);
        assert_eq!(ram.read_u32(0x100).unwrap(), 0x3fc0_0000);
        assert_eq!(cpu.step(&mut ram), StepResult::Running);
        assert_eq!(cpu.state().r[3], 1 << 8);
        assert_eq!(cpu.step(&mut ram), StepResult::Running);
        assert_eq!(cpu.state().flags, Flags::N | Flags::C);
        assert_eq!(cpu.step(&mut ram), StepResult::Running);
        assert_eq!(cpu.state().flags, Flags::N | Flags::C | Flags::V);
    }

    #[test]
    fn every_fptransa_opcode_routes_to_its_frozen_contract_operation() {
        use crate::fpu::trans::contracts::TransOperation;
        let cases = [
            ("long.fsina_x_fn_s_fn_d", TransOperation::Sine),
            ("long.fcosa_x_fn_s_fn_d", TransOperation::Cosine),
            ("long.ftana_x_fn_s_fn_d", TransOperation::Tangent),
            (
                "extralong.fsincosa_x_fn_s_fn_d_fn_c",
                TransOperation::SineCosine,
            ),
            ("long.fasina_x_fn_s_fn_d", TransOperation::ArcSine),
            ("long.facosa_x_fn_s_fn_d", TransOperation::ArcCosine),
            ("long.fatana_x_fn_s_fn_d", TransOperation::ArcTangent),
            ("long.fsinha_x_fn_s_fn_d", TransOperation::HyperbolicSine),
            ("long.fcosha_x_fn_s_fn_d", TransOperation::HyperbolicCosine),
            ("long.ftanha_x_fn_s_fn_d", TransOperation::HyperbolicTangent),
            (
                "long.fatanha_x_fn_s_fn_d",
                TransOperation::HyperbolicArcTangent,
            ),
            ("long.fetoxa_x_fn_s_fn_d", TransOperation::Exponential),
            (
                "long.fetoxm1a_x_fn_s_fn_d",
                TransOperation::ExponentialMinusOne,
            ),
            (
                "long.ftwotoxa_x_fn_s_fn_d",
                TransOperation::ExponentialBaseTwo,
            ),
            (
                "long.ftentoxa_x_fn_s_fn_d",
                TransOperation::ExponentialBaseTen,
            ),
            ("long.flogna_x_fn_s_fn_d", TransOperation::NaturalLogarithm),
            (
                "long.flognp1a_x_fn_s_fn_d",
                TransOperation::NaturalLogarithmPlusOne,
            ),
            ("long.flog2a_x_fn_s_fn_d", TransOperation::LogarithmBaseTwo),
            ("long.flog10a_x_fn_s_fn_d", TransOperation::LogarithmBaseTen),
        ];
        for (id, operation) in cases {
            let fields = if operation == TransOperation::SineCosine {
                vec![('z', 1), ('s', 1), ('d', 0), ('c', 2)]
            } else {
                vec![('z', 1), ('s', 1), ('d', 0)]
            };
            let bytes = encoded_form(id, &fields, &[]);
            let mut ram = Ram::new(bytes.len());
            ram.load(0, &bytes).unwrap();
            let mut cpu = Cpu::new();
            cpu.reset(0);
            let operand = [0_u64];
            let request = crate::fpu::effect::FpRequest {
                format: crate::fpu::format::FpFormat::D,
                status: crate::fpu::env::FpStatus::decode(0).unwrap(),
                operands: &operand,
            };
            let expected = crate::fpu::execute_trans(operation, request);
            assert_eq!(cpu.step(&mut ram), StepResult::Running, "{id}");
            match expected {
                crate::fpu::effect::FpEffect::Commit {
                    result: crate::fpu::effect::FpResult::Float(value),
                    causes,
                } => {
                    assert_eq!(cpu.state().f[0], value, "{id}");
                    assert_eq!(cpu.state().fflags, causes.bits(), "{id}");
                }
                crate::fpu::effect::FpEffect::Commit {
                    result: crate::fpu::effect::FpResult::FloatPair(first, second),
                    causes,
                } => {
                    assert_eq!(
                        (cpu.state().f[0], cpu.state().f[2]),
                        (first, second),
                        "{id}"
                    );
                    assert_eq!(cpu.state().fflags, causes.bits(), "{id}");
                }
                other => panic!("unexpected frozen effect for {id}: {other:?}"),
            }
        }
    }

    #[test]
    fn fpu_conversions_cover_signed_unsigned_integer_and_format_domains() {
        let signed_to_float = encoded_form(
            "long.fcvt_x_rn_s_fn_d",
            &[('z', 1), ('s', 1), ('d', 0)],
            &[],
        );
        let unsigned_to_float = encoded_form(
            "long.fcvtu_x_rn_s_fn_d",
            &[('z', 1), ('s', 2), ('d', 3)],
            &[],
        );
        let float_to_signed = encoded_form(
            "long.fcvt_x_fn_s_rn_d",
            &[('z', 1), ('s', 0), ('d', 4)],
            &[],
        );
        let double_to_single = encoded_form(
            "long.fcvt_x_fn_s_fn_d",
            &[('z', 0), ('s', 5), ('d', 6)],
            &[],
        );
        let mut program = Vec::new();
        program.extend_from_slice(&signed_to_float);
        program.extend_from_slice(&unsigned_to_float);
        program.extend_from_slice(&float_to_signed);
        program.extend_from_slice(&double_to_single);
        let mut ram = Ram::new(program.len());
        ram.load(0, &program).unwrap();
        let mut cpu = Cpu::new();
        cpu.reset(0);
        cpu.state_mut().r[1] = (-2_i64) as u64;
        cpu.state_mut().r[2] = u64::MAX;
        cpu.state_mut().f[5] = 1.5_f64.to_bits();

        assert_eq!(cpu.step(&mut ram), StepResult::Running);
        assert_eq!(cpu.state().f[0], (-2.0_f64).to_bits());
        assert_eq!(cpu.step(&mut ram), StepResult::Running);
        assert_eq!(cpu.state().f[3], (u64::MAX as f64).to_bits());
        assert_eq!(cpu.step(&mut ram), StepResult::Running);
        assert_eq!(cpu.state().r[4], (-2_i64) as u64);
        assert_eq!(cpu.step(&mut ram), StepResult::Running);
        assert_eq!(cpu.state().f[6], 1.5_f32.to_bits() as u64);
    }

    #[test]
    fn floating_pair_stack_uses_the_canonical_pair_mapping_and_word_order() {
        let push = encoded_form("extrashort.fpushp_pair_id_i", &[('i', 4)], &[]);
        let pop = encoded_form("extrashort.fpopp_pair_id_i", &[('i', 4)], &[]);
        let mut ram = Ram::new(64);
        ram.load(0, &push).unwrap();
        ram.load(push.len() as u64, &pop).unwrap();
        let mut cpu = Cpu::new();
        cpu.reset(0);
        cpu.state_mut().sp = 64;
        cpu.state_mut().f[8] = 0x8888;
        cpu.state_mut().f[9] = 0x9999;

        assert_eq!(cpu.step(&mut ram), StepResult::Running);
        assert_eq!(cpu.state().sp, 48);
        assert_eq!(ram.read_u64(48).unwrap(), 0x9999);
        assert_eq!(ram.read_u64(56).unwrap(), 0x8888);

        cpu.state_mut().f[8] = 0;
        cpu.state_mut().f[9] = 0;
        assert_eq!(cpu.step(&mut ram), StepResult::Running);
        assert_eq!(cpu.state().sp, 64);
        assert_eq!(cpu.state().f[8], 0x8888);
        assert_eq!(cpu.state().f[9], 0x9999);
    }

    #[test]
    fn cpuid_executes_the_frozen_query_contract() {
        let bytes = encoded_form("medium.cpuid_rn_r", &[('r', 3)], &[]);
        let mut ram = Ram::new(bytes.len());
        ram.load(0, &bytes).unwrap();
        let mut cpu = Cpu::new();
        cpu.reset(0);
        let selector = (1_u64 << 32) | (1 << 16) | 4;
        cpu.state_mut().r[3] = selector;

        assert_eq!(cpu.step(&mut ram), StepResult::Running);
        assert_eq!(cpu.state().r[3], crate::cpuid::query(selector));
    }

    #[test]
    fn save_restore_round_trips_the_fixed_image_and_honors_clear_fp_components() {
        let save = encoded_form("long.save_ea_e", &[('e', 15)], &[]);
        let restore = encoded_form("long.restore_ea_e", &[('e', 15)], &[]);
        let restore_pc = save.len() as u64;
        let mut ram = Ram::new(0x2000);
        ram.load(0, &save).unwrap();
        ram.load(restore_pc, &restore).unwrap();
        let mut cpu = Cpu::new();
        cpu.reset(0);
        cpu.state_mut().r[0] = 0x1234;
        cpu.state_mut().r[15] = 0x1000;
        cpu.state_mut().f[0] = 1.25_f64.to_bits();
        cpu.state_mut().fflags = crate::fpu::env::FpCauses::NX.bits();
        cpu.state_mut().fstatus = crate::fpu::env::FpCauses::DZ.bits();
        cpu.state_mut().flags = Flags::C | Flags::Z;
        cpu.state_mut().status = crate::Status::empty();
        let saved_gs = crate::SegmentRegister::from_raw(0x23_003);
        cpu.state_mut()
            .segments
            .set(crate::SegmentSelector::Gs0, saved_gs);

        assert_eq!(cpu.step(&mut ram), StepResult::Running);
        assert_eq!(ram.read_u64(0x1008).unwrap(), 1);
        assert_eq!(ram.read_u64(0x10c0).unwrap(), 1.25_f64.to_bits());
        assert_eq!(ram.read_u64(0x1140).unwrap(), 1 << 4);
        assert_eq!(ram.read_u64(0x1148).unwrap(), 1 << 1);

        cpu.state_mut().r[0] = 0;
        cpu.state_mut().f[0] = 0;
        cpu.state_mut().fflags = 0;
        cpu.state_mut().fstatus = 0;
        cpu.state_mut().flags = Flags::empty();
        cpu.state_mut().status = crate::Status::IE;
        cpu.state_mut().segments.set(
            crate::SegmentSelector::Gs0,
            crate::SegmentRegister::disabled(),
        );
        assert_eq!(cpu.step(&mut ram), StepResult::Running);
        assert_eq!(cpu.state().r[0], 0x1234);
        assert_eq!(cpu.state().f[0], 1.25_f64.to_bits());
        assert_eq!(cpu.state().fflags, crate::fpu::env::FpCauses::NX.bits());
        assert_eq!(cpu.state().fstatus, crate::fpu::env::FpCauses::DZ.bits());
        assert_eq!(cpu.state().flags, Flags::C | Flags::Z);
        assert_eq!(cpu.state().status, crate::Status::IE);
        assert_eq!(
            cpu.state().segments.get(crate::SegmentSelector::Gs0),
            saved_gs
        );

        ram.write_u64(0x1008, 0).unwrap();
        cpu.state_mut().pc = restore_pc;
        cpu.state_mut().f = [u64::MAX; 16];
        cpu.state_mut().fflags = crate::fpu::env::FpCauses::NV.bits();
        cpu.state_mut().fstatus = crate::fpu::env::FpCauses::NV.bits();
        assert_eq!(cpu.step(&mut ram), StepResult::Running);
        assert_eq!(cpu.state().f, [0; 16]);
        assert_eq!(cpu.state().fflags, 0);
        assert_eq!(cpu.state().fstatus, 0);
    }

    #[test]
    fn save_omits_clean_fp_component_without_touching_its_image() {
        let save = encoded_form("long.save_ea_e", &[('e', 15)], &[]);
        let mut bus = SlotProbeBus::new(0x2000);
        bus.ram.load(0, &save).unwrap();
        for address in 0x10c0..0x1180 {
            bus.ram.write_u8(address, 0xa5).unwrap();
        }
        bus.clear_log();

        let mut cpu = Cpu::new();
        cpu.reset(0);
        cpu.state_mut().r[15] = 0x1000;

        assert_eq!(cpu.step(&mut bus), StepResult::Running);
        assert_eq!(bus.ram.read_u64(0x1008).unwrap(), 0);
        assert!((0x10c0..0x1180).all(|address| bus.ram.read_u8(address).unwrap() == 0xa5));
        assert!(bus.byte_writes.iter().all(|&address| address < 0x10c0));
    }

    #[test]
    fn restore_validates_header_and_bitmap_before_reading_state_images() {
        let bytes = encoded_form("long.restore_ea_e", &[('e', 15)], &[]);
        let instruction = bedrock_isa::decode(&bytes).unwrap();
        let mut bus = SlotProbeBus::new(0x2000);
        bus.ram.write_u64(0x1000, 1 << 63).unwrap();
        bus.ram.write_u64(0x1008, 1).unwrap();
        bus.clear_log();
        let mut cpu = Cpu::new();
        cpu.reset(0);
        cpu.state_mut().r[15] = 0x1000;
        let before = cpu.state().clone();

        assert_eq!(
            cpu.execute(&mut bus, 0, &instruction),
            Err(Trap::InvalidControlState {
                pc: 0,
                cause: InvalidControlCause::ReservedBits,
            })
        );
        assert_eq!(cpu.state(), &before);
        assert_eq!(bus.byte_reads, (0x1000..0x1010).collect::<Vec<_>>());
    }

    #[test]
    fn restore_clear_fp_bitmap_installs_initial_state_without_reading_extension() {
        let bytes = encoded_form("long.restore_ea_e", &[('e', 15)], &[]);
        let instruction = bedrock_isa::decode(&bytes).unwrap();
        let mut bus = SlotProbeBus::new(0x2000);
        bus.ram.write_u64(0x1000, 0).unwrap();
        bus.ram.write_u64(0x1008, 0).unwrap();
        for index in 0..16_u64 {
            bus.ram
                .write_u64(0x1010 + index * 8, 0x100 + index)
                .unwrap();
        }
        for address in 0x10c0..0x1180 {
            bus.ram.write_u8(address, 0xa5).unwrap();
        }
        bus.clear_log();
        let mut cpu = Cpu::new();
        cpu.reset(0);
        cpu.state_mut().status = Status::empty();
        cpu.state_mut().r[15] = 0x1000;
        cpu.state_mut().f = [u64::MAX; 16];
        cpu.state_mut().fflags = crate::fpu::env::FpCauses::NV.bits();
        cpu.state_mut().fstatus = crate::fpu::env::FpCauses::DZ.bits();

        assert_eq!(
            cpu.execute(&mut bus, 0, &instruction),
            Ok(StepResult::Running)
        );
        assert_eq!(
            cpu.state().r,
            core::array::from_fn(|index| 0x100 + index as u64)
        );
        assert_eq!(cpu.state().f, [0; 16]);
        assert_eq!(cpu.state().fflags, 0);
        assert_eq!(cpu.state().fstatus, 0);
        assert!(bus.byte_reads.iter().all(|&address| address < 0x10c0));
    }

    #[test]
    fn restore_rejects_reserved_fp_image_bits_before_any_state_commit() {
        let bytes = encoded_form("long.restore_ea_e", &[('e', 15)], &[]);
        let instruction = bedrock_isa::decode(&bytes).unwrap();
        let mut ram = Ram::new(0x2000);
        ram.write_u64(0x1008, 1).unwrap();
        ram.write_u64(0x1178, 1).unwrap();
        let mut cpu = Cpu::new();
        cpu.reset(0);
        cpu.state_mut().r[15] = 0x1000;
        cpu.state_mut().r[0] = 0xfeed;
        let before = cpu.state().clone();

        assert!(matches!(
            cpu.execute(&mut ram, 0, &instruction),
            Err(crate::Trap::InvalidControlState {
                cause: crate::exception::InvalidControlCause::ReservedBits,
                ..
            })
        ));
        assert_eq!(cpu.state(), &before);
    }

    #[test]
    fn fpu_state_writes_reject_reserved_bits_without_commit() {
        let cases = [
            ("long.wrfflags_rn_s", 1_u64 << 5),
            ("long.wrfstatus_rn_s", 1_u64 << 10),
        ];
        for (id, value) in cases {
            let bytes = encoded_form(id, &[('s', 1)], &[]);
            let instruction = bedrock_isa::decode(&bytes).unwrap();
            let mut cpu = Cpu::new();
            cpu.reset(0);
            cpu.state_mut().r[1] = value;
            let before = cpu.state().clone();
            let mut ram = Ram::new(bytes.len());
            assert!(matches!(
                cpu.execute(&mut ram, 0, &instruction),
                Err(crate::Trap::InvalidControlState {
                    cause: crate::exception::InvalidControlCause::ReservedBits,
                    ..
                })
            ));
            assert_eq!(cpu.state(), &before, "{id}");
        }
    }

    #[test]
    fn mandatory_performance_counters_count_cycles_retirements_and_page_walks() {
        let mut ram = Ram::new(8);
        ram.load(0, &[0xc2, 0x40, 0x00, 0x0e]).unwrap();
        let mut cpu = Cpu::new();
        cpu.reset(0);
        cpu.state_mut().pmc = 1;
        cpu.state_mut().r[0] = 2;

        assert_eq!(cpu.step(&mut ram), StepResult::Running);
        assert_eq!(cpu.step(&mut ram), StepResult::Running);
        assert_eq!(cpu.step(&mut ram), StepResult::Running);
        assert_eq!(cpu.cycle_counter.get(), 3);
        assert_eq!(cpu.instret_counter.get(), 3);
        assert_eq!(cpu.ptwalk_counter.get(), 0);

        assert_ne!(cpu.step(&mut ram), StepResult::Running);
        assert_eq!(cpu.cycle_counter.get(), 4);
        assert_eq!(cpu.instret_counter.get(), 3);

        cpu.cycle_counter.set(11);
        cpu.instret_counter.set(12);
        cpu.ptwalk_counter.set(13);
        for (counter, expected) in [(1_u16, 11), (2, 12), (3, 13)] {
            let bytes = encoded_form("long.rdpmc_ea_rn_d", &[('d', 4)], &counter.to_le_bytes());
            let instruction = bedrock_isa::decode(&bytes).unwrap();
            cpu.execute(&mut ram, 0, &instruction).unwrap();
            assert_eq!(cpu.state().r[4], expected);
        }

        let invalid = encoded_form("long.rdpmc_ea_rn_d", &[('d', 4)], &[0, 0]);
        assert!(matches!(
            cpu.execute(&mut ram, 0, &bedrock_isa::decode(&invalid).unwrap()),
            Err(crate::Trap::InvalidControlState {
                cause: crate::exception::InvalidControlCause::InvalidSelector,
                ..
            })
        ));

        let reserved_pmc =
            encoded_form("long.wrcr_rn_s_ea", &[('s', 1)], &0x1100_u16.to_le_bytes());
        cpu.state_mut().r[1] = 2;
        assert!(matches!(
            cpu.execute(&mut ram, 0, &bedrock_isa::decode(&reserved_pmc).unwrap()),
            Err(crate::Trap::InvalidControlState {
                cause: crate::exception::InvalidControlCause::ReservedBits,
                ..
            })
        ));

        cpu.reset(0x40);
        assert_eq!(
            (
                cpu.cycle_counter.get(),
                cpu.instret_counter.get(),
                cpu.ptwalk_counter.get()
            ),
            (0, 0, 0)
        );
    }

    #[test]
    fn ptwalk_counter_records_paged_translations_after_canonical_validation() {
        let mut ram = Ram::new(0x10_000);
        install_four_level_root(&mut ram);
        map_low_page(&mut ram, 0, 0x8000, PTE_W | PTE_X);
        ram.write_u8(0x8000, 0x01).unwrap();
        let mut cpu = Cpu::new();
        cpu.reset(0);
        cpu.state_mut().ptcr = PageTableControl::from_raw(0x1001);
        cpu.state_mut().pmc = 1;

        assert_eq!(cpu.step(&mut ram), StepResult::Running);
        assert!(cpu.ptwalk_counter.get() > 0);

        cpu.ptwalk_counter.set(0);
        cpu.state_mut().pc = 0x0001_0000_0000_0000;
        assert_ne!(cpu.step(&mut ram), StepResult::Running);
        assert_eq!(cpu.ptwalk_counter.get(), 0);
    }

    #[test]
    fn syscall_prioritizes_transition_state_and_validates_before_commit() {
        let instruction = decoded_form("extrashort.syscall", &[], &[]);
        let mut ram = Ram::new(0x200);
        let mut cpu = Cpu::new();
        cpu.reset(0x20);
        cpu.state_mut().spc = 3;
        cpu.state_mut().status = Status::PM;

        let before = cpu.state().clone();
        assert_eq!(
            cpu.execute(&mut ram, 0x20, &instruction),
            Err(Trap::InvalidControlState {
                pc: 0x20,
                cause: InvalidControlCause::InvalidTransition,
            })
        );
        assert_eq!(cpu.state(), &before);

        cpu.state_mut().status = Status::empty();
        let before = cpu.state().clone();
        assert_eq!(
            cpu.execute(&mut ram, 0x20, &instruction),
            Err(Trap::InvalidControlState {
                pc: 0x20,
                cause: InvalidControlCause::InvalidImage,
            })
        );
        assert_eq!(cpu.state(), &before);

        cpu.state_mut().spc = 0x100;
        cpu.state_mut().sss = SegmentRegister::from_raw(1 << 1);
        cpu.state_mut().ssp = 0x1000;
        let before = cpu.state().clone();
        assert_eq!(
            cpu.execute(&mut ram, 0x20, &instruction),
            Err(Trap::InvalidControlState {
                pc: 0x20,
                cause: InvalidControlCause::InvalidImage,
            })
        );
        assert_eq!(cpu.state(), &before);
    }

    #[test]
    fn sysret_prioritizes_transition_state_and_revalidates_before_commit() {
        let instruction = decoded_form("extrashort.sysret", &[], &[]);
        let mut ram = Ram::new(0x200);
        let mut cpu = Cpu::new();
        cpu.reset(0x20);
        cpu.state_mut().status = Status::PM | Status::EA;
        cpu.state_mut().urctl = super::URCTL_VALID | (1 << 63);

        let before = cpu.state().clone();
        assert_eq!(
            cpu.execute(&mut ram, 0x20, &instruction),
            Err(Trap::InvalidControlState {
                pc: 0x20,
                cause: InvalidControlCause::InvalidTransition,
            })
        );
        assert_eq!(cpu.state(), &before);

        cpu.state_mut().status = Status::PM;
        cpu.state_mut().urctl = 1 << 63;
        let before = cpu.state().clone();
        assert_eq!(
            cpu.execute(&mut ram, 0x20, &instruction),
            Err(Trap::InvalidControlState {
                pc: 0x20,
                cause: InvalidControlCause::InvalidTransition,
            })
        );
        assert_eq!(cpu.state(), &before);

        cpu.state_mut().urctl = super::URCTL_VALID | (1 << 4);
        let before = cpu.state().clone();
        assert_eq!(
            cpu.execute(&mut ram, 0x20, &instruction),
            Err(Trap::InvalidControlState {
                pc: 0x20,
                cause: InvalidControlCause::ReservedBits,
            })
        );
        assert_eq!(cpu.state(), &before);

        let invalid_segment = 0xffff_ffff_ffff_f000 | (0x1f << 7) | (0x3f << 1);
        cpu.state_mut().urctl = super::URCTL_VALID;
        cpu.state_mut().urcs = SegmentRegister::from_raw(invalid_segment);
        let before = cpu.state().clone();
        assert_eq!(
            cpu.execute(&mut ram, 0x20, &instruction),
            Err(Trap::InvalidControlState {
                pc: 0x20,
                cause: InvalidControlCause::InvalidImage,
            })
        );
        assert_eq!(cpu.state(), &before);
    }

    #[test]
    fn syscall_and_sysret_round_trip_the_user_control_state() {
        let mut ram = Ram::new(512);
        ram.write_u8(0, 0x05).unwrap(); // SYSCALL
        ram.write_u8(0x100, 0x06).unwrap(); // SYSRET
        let mut cpu = Cpu::new();
        cpu.reset(0);
        cpu.state_mut().status = crate::Status::empty();
        cpu.state_mut().sp = 128;
        cpu.state_mut().spc = 0x100;
        cpu.state_mut().ssp = 512;

        assert_eq!(cpu.step(&mut ram), StepResult::Running);
        assert_eq!(cpu.state().pc, 0x100);
        assert_eq!(cpu.state().sp, 512);
        assert!(cpu.state().status.contains(crate::Status::PM));
        assert_eq!(cpu.state().urpc, 1);
        assert_eq!(cpu.state().ursp, 128);
        assert_ne!(cpu.state().urctl & (1 << 32), 0);

        assert_eq!(cpu.step(&mut ram), StepResult::Running);
        assert_eq!(cpu.state().pc, 1);
        assert_eq!(cpu.state().sp, 128);
        assert!(!cpu.state().status.contains(crate::Status::PM));
        assert_eq!(cpu.state().urctl & (1 << 32), 0);
    }

    #[test]
    fn scalar_repeat_uses_frozen_body_and_unsigned_counter() {
        let mut ram = Ram::new(8);
        for (index, byte) in [0xc2, 0x40, 0x00, 0x0e].into_iter().enumerate() {
            ram.write_u8(index as u64, byte).unwrap();
        }
        let mut cpu = Cpu::new();
        cpu.reset(0);
        cpu.state_mut().r[0] = 2;
        assert_eq!(cpu.step(&mut ram), StepResult::Running);
        assert_eq!(cpu.state().pc, 3);
        ram.write_u8(3, 0x00).unwrap();
        assert_eq!(cpu.step(&mut ram), StepResult::Running);
        assert_eq!(cpu.state().r[0], 1);
        assert_eq!(cpu.state().pc, 3);
        assert_eq!(cpu.step(&mut ram), StepResult::Running);
        assert_eq!(cpu.state().r[0], 0);
        assert_eq!(cpu.state().pc, 4);
    }

    #[test]
    fn repeat_group_validates_and_repeats_byte_counted_body() {
        let mut ram = Ram::new(12);
        for (index, byte) in [0xc8, 0x26, 0x80, 0x01, 0x00, 0x0e].into_iter().enumerate() {
            ram.write_u8(index as u64, byte).unwrap();
        }
        let mut cpu = Cpu::new();
        cpu.reset(0);
        cpu.state_mut().r[0] = 2;
        assert_eq!(cpu.step(&mut ram), StepResult::Running);
        assert_eq!(cpu.state().pc, 5);
        assert_eq!(cpu.step(&mut ram), StepResult::Running);
        assert_eq!(cpu.state().r[0], 1);
        assert_eq!(cpu.state().pc, 5);
        assert_eq!(cpu.step(&mut ram), StepResult::Running);
        assert_eq!(cpu.state().r[0], 0);
        assert_eq!(cpu.state().pc, 6);
        assert!(cpu.repeat.is_none());
    }

    #[test]
    fn repeat_group_with_zero_loop_control_executes_once() {
        let body = encoded_form("extrashort.clr_q_rn_r", &[('r', 1)], &[]);
        let body_bytes = u16::try_from(body.len()).unwrap().to_le_bytes();
        let repeat = encoded_form("medium.repg_rn_r_ea", &[('r', 0)], &body_bytes);
        let body_pc = repeat.len() as u64;
        let after_pc = body_pc + body.len() as u64;
        let mut ram = Ram::new(64);
        ram.load(0, &[repeat, body].concat()).unwrap();
        let mut cpu = Cpu::new();
        cpu.reset(0);
        cpu.state_mut().r[0] = 0;
        cpu.state_mut().r[1] = u64::MAX;

        assert_eq!(cpu.step(&mut ram), StepResult::Running);
        assert_eq!(cpu.state().pc, body_pc);
        assert_eq!(cpu.step(&mut ram), StepResult::Running);
        assert_eq!(cpu.state().r[0], 0);
        assert_eq!(cpu.state().r[1], 0);
        assert_eq!(cpu.state().pc, after_pc);
    }

    #[test]
    fn repeat_group_with_one_loop_control_executes_once() {
        let body = encoded_form("extrashort.clr_q_rn_r", &[('r', 1)], &[]);
        let body_bytes = u16::try_from(body.len()).unwrap().to_le_bytes();
        let repeat = encoded_form("medium.repg_rn_r_ea", &[('r', 0)], &body_bytes);
        let body_pc = repeat.len() as u64;
        let after_pc = body_pc + body.len() as u64;
        let mut ram = Ram::new(64);
        ram.load(0, &[repeat, body].concat()).unwrap();
        let mut cpu = Cpu::new();
        cpu.reset(0);
        cpu.state_mut().r[0] = 1;
        cpu.state_mut().r[1] = u64::MAX;

        assert_eq!(cpu.step(&mut ram), StepResult::Running);
        assert_eq!(cpu.state().pc, body_pc);
        assert_eq!(cpu.step(&mut ram), StepResult::Running);
        assert_eq!(cpu.state().r[0], 0);
        assert_eq!(cpu.state().r[1], 0);
        assert_eq!(cpu.state().pc, after_pc);
        assert!(cpu.repeat.is_none());
    }

    #[test]
    fn repeat_group_uses_body_writes_of_zero_or_one_as_live_loop_control() {
        let set_control = encoded_form(
            "short.mov_x_rn_s_rn_d",
            &[('z', 1), ('s', 1), ('d', 0)],
            &[],
        );
        let clear_other = encoded_form("extrashort.clr_q_rn_r", &[('r', 2)], &[]);
        let mut body = set_control.clone();
        body.extend_from_slice(&clear_other);
        let body_bytes = u16::try_from(body.len()).unwrap().to_le_bytes();
        let repeat = encoded_form("medium.repg_rn_r_ea", &[('r', 0)], &body_bytes);
        let body_pc = repeat.len() as u64;
        let second_pc = body_pc + set_control.len() as u64;
        let after_pc = body_pc + body.len() as u64;
        let mut ram = Ram::new(64);
        ram.load(0, &[repeat, body].concat()).unwrap();

        for written_control in [0, 1] {
            let mut cpu = Cpu::new();
            cpu.reset(0);
            cpu.state_mut().r[0] = 99;
            cpu.state_mut().r[1] = written_control;
            cpu.state_mut().r[2] = u64::MAX;

            assert_eq!(cpu.step(&mut ram), StepResult::Running);
            assert_eq!(cpu.state().pc, body_pc);
            assert_eq!(cpu.step(&mut ram), StepResult::Running);
            assert_eq!(cpu.state().r[0], written_control);
            assert_eq!(cpu.state().pc, second_pc);
            assert_eq!(cpu.step(&mut ram), StepResult::Running);
            assert_eq!(cpu.state().r[0], 0);
            assert_eq!(cpu.state().r[2], 0);
            assert_eq!(cpu.state().pc, after_pc);
            assert!(cpu.repeat.is_none());
        }
    }

    #[test]
    fn repeat_group_continuation_accepts_zero_live_loop_control() {
        let body = encoded_form("extrashort.clr_q_rn_r", &[('r', 1)], &[]);
        let mut ram = Ram::new(64);
        ram.load(0, &body).unwrap();
        let mut cpu = Cpu::new();
        cpu.reset(0);
        cpu.state_mut().r[0] = 0;
        cpu.state_mut().r[1] = u64::MAX;
        let saved_cs = cpu.state().segments.cs();
        let continuation = RepeatContinuation::new(
            0,
            0,
            RepeatKind::Group,
            0,
            u16::try_from(body.len()).unwrap(),
        )
        .unwrap();
        cpu.repeat = cpu
            .restore_repeat_continuation(&mut ram, 0x20, 0, Some(continuation), saved_cs, true)
            .unwrap();

        assert_eq!(cpu.step(&mut ram), StepResult::Running);
        assert_eq!(cpu.state().r[0], 0);
        assert_eq!(cpu.state().r[1], 0);
        assert_eq!(cpu.state().pc, body.len() as u64);
        assert!(cpu.repeat.is_none());
    }

    #[test]
    fn repeat_group_eret_resumes_with_zero_live_loop_control() {
        let clear_control = encoded_form("extrashort.clr_q_rn_r", &[('r', 0)], &[]);
        let divide = encoded_form(
            "long.divu_x_ea_e_rn_d",
            &[('z', 3), ('e', 2), ('d', 3)],
            &[],
        );
        let mut body = clear_control.clone();
        body.extend_from_slice(&divide);
        let body_bytes = u16::try_from(body.len()).unwrap();
        let repeat = encoded_form(
            "medium.repg_rn_r_ea",
            &[('r', 0)],
            &body_bytes.to_le_bytes(),
        );
        let body_pc = repeat.len() as u64;
        let divide_pc = body_pc + clear_control.len() as u64;
        let after_pc = body_pc + body.len() as u64;

        let fix_divisor = encoded_form(
            "short.mov_x_rn_s_rn_d",
            &[('z', 1), ('s', 4), ('d', 2)],
            &[],
        );
        let handler_pc = 0x100;
        let mut handler = fix_divisor.clone();
        handler.push(0x04); // ERET

        let mut ram = Ram::new(0x2000);
        ram.load(0, &[repeat, body].concat()).unwrap();
        ram.load(handler_pc, &handler).unwrap();
        let mut cpu = Cpu::new();
        cpu.reset(0);
        cpu.state_mut().ecr = crate::EventControl::from_raw(1);
        cpu.state_mut().epc = handler_pc;
        cpu.state_mut().fsp = 0x1000;
        cpu.state_mut().r[0] = u64::MAX;
        cpu.state_mut().r[2] = 0;
        cpu.state_mut().r[3] = 8;
        cpu.state_mut().r[4] = 2;

        assert_eq!(cpu.step(&mut ram), StepResult::Running); // REPG
        assert_eq!(cpu.state().pc, body_pc);
        assert_eq!(cpu.step(&mut ram), StepResult::Running); // CLR.Q R0
        assert_eq!(cpu.state().r[0], 0);
        assert_eq!(cpu.state().pc, divide_pc);

        assert_eq!(cpu.step(&mut ram), StepResult::Running); // Divide error event
        assert_eq!(cpu.state().pc, handler_pc);
        assert_eq!(cpu.state().r[0], 0);
        assert_eq!(cpu.state().r[3], 8);
        assert!(cpu.repeat.is_none());
        let continuation = RepeatContinuation::new(
            0,
            0,
            RepeatKind::Group,
            u16::try_from(clear_control.len()).unwrap(),
            body_bytes,
        )
        .unwrap();
        assert_eq!(
            ram.read_u64(cpu.state().sp + 16).unwrap(),
            continuation.encode()
        );

        assert_eq!(cpu.step(&mut ram), StepResult::Running); // MOV.Q R4, R2
        assert_eq!(cpu.state().r[2], 2);
        assert_eq!(cpu.step(&mut ram), StepResult::Running); // ERET
        assert_eq!(cpu.state().pc, divide_pc);
        assert_eq!(cpu.state().r[0], 0);
        assert!(cpu.repeat.is_some());

        assert_eq!(cpu.step(&mut ram), StepResult::Running); // DIVU.Q R2, R3
        assert_eq!(cpu.state().r[3], 4);
        assert_eq!(cpu.state().r[0], 0);
        assert_eq!(cpu.state().pc, after_pc);
        assert!(cpu.repeat.is_none());
    }

    #[test]
    fn repcc_flags_observes_the_post_body_flags_image() {
        let repeat = encoded_form("medium.repcc_rn_r", &[('c', 3), ('r', 0)], &[]);
        let body = encoded_form(
            "short.cmp_x_rn_s_rn_d",
            &[('z', 1), ('s', 1), ('d', 2)],
            &[],
        );
        let body_pc = repeat.len() as u64;
        let after_pc = body_pc + body.len() as u64;
        let mut ram = Ram::new(64);
        ram.load(0, &[repeat, body].concat()).unwrap();
        let mut cpu = Cpu::new();
        cpu.reset(0);
        cpu.state_mut().r[0] = 3;
        cpu.state_mut().r[1] = 0x55;
        cpu.state_mut().r[2] = 0x55;
        cpu.state_mut().flags = Flags::empty();

        assert_eq!(cpu.step(&mut ram), StepResult::Running);
        assert_eq!(cpu.state().pc, body_pc);
        assert_eq!(cpu.step(&mut ram), StepResult::Running);
        assert_eq!(cpu.state().flags, Flags::Z);
        assert_eq!(cpu.state().r[0], 2);
        assert_eq!(cpu.state().pc, after_pc);
    }

    #[test]
    fn repcc_result_is_captured_before_counter_destination_suppression() {
        let repeat = encoded_form("medium.repcc_rn_r", &[('c', 3), ('r', 1)], &[]);
        let body = encoded_form("extrashort.clr_q_rn_r", &[('r', 1)], &[]);
        let after_pc = (repeat.len() + body.len()) as u64;
        let mut ram = Ram::new(64);
        ram.load(0, &[repeat, body].concat()).unwrap();
        let mut cpu = Cpu::new();
        cpu.reset(0);
        cpu.state_mut().r[1] = 3;
        cpu.state_mut().flags = Flags::C | Flags::V;

        assert_eq!(cpu.step(&mut ram), StepResult::Running);
        assert_eq!(cpu.step(&mut ram), StepResult::Running);
        assert_eq!(cpu.state().r[1], 2);
        assert_eq!(cpu.state().pc, after_pc);
        assert_eq!(cpu.state().flags, Flags::C | Flags::V);
    }

    #[test]
    fn repcc_source_is_captured_before_ea_auto_update() {
        let repeat = encoded_form("medium.repcc_rn_r", &[('c', 2), ('r', 0)], &[]);
        let body = encoded_form(
            "long.movnt_x_rn_s_ea_e",
            &[('z', 0), ('s', 1), ('e', 0x74)],
            &[0x8c],
        );
        let body_pc = repeat.len() as u64;
        let mut ram = Ram::new(0x200);
        ram.load(0, &[repeat, body].concat()).unwrap();
        let mut cpu = Cpu::new();
        cpu.reset(0);
        cpu.state_mut().r[0] = 2;
        cpu.state_mut().r[1] = 0x100;
        cpu.state_mut().flags = Flags::C | Flags::V;

        assert_eq!(cpu.step(&mut ram), StepResult::Running);
        assert_eq!(cpu.step(&mut ram), StepResult::Running);
        assert_eq!(cpu.state().r[0], 1);
        assert_eq!(cpu.state().r[1], 0x101);
        assert_eq!(cpu.state().pc, body_pc);
        assert_eq!(cpu.state().flags, Flags::C | Flags::V);
        assert_eq!(ram.read_u8(0x100).unwrap(), 0);
    }

    #[test]
    fn repcc_memory_result_uses_the_successful_write_without_an_extra_read() {
        let repeat = encoded_form("medium.repcc_rn_r", &[('c', 3), ('r', 0)], &[]);
        let body = encoded_form(
            "medium.clr_x_ea",
            &[('z', 0), ('e', 0x6a)],
            &0x100_u32.to_le_bytes(),
        );
        let after_pc = (repeat.len() + body.len()) as u64;
        let mut bus = SlotProbeBus::new(0x200);
        bus.ram.load(0, &[repeat, body].concat()).unwrap();
        bus.ram.write_u8(0x100, 0x55).unwrap();
        let mut cpu = Cpu::new();
        cpu.reset(0);
        cpu.state_mut().r[0] = 3;
        cpu.state_mut().flags = Flags::C | Flags::V;

        assert_eq!(cpu.step(&mut bus), StepResult::Running);
        bus.clear_log();
        assert_eq!(cpu.step(&mut bus), StepResult::Running);
        assert_eq!(cpu.state().r[0], 2);
        assert_eq!(cpu.state().pc, after_pc);
        assert_eq!(cpu.state().flags, Flags::C | Flags::V);
        assert!(bus.byte_reads.is_empty());
        assert_eq!(bus.byte_writes, [0x100]);
        assert_eq!(bus.ram.read_u8(0x100).unwrap(), 0);
    }
}
