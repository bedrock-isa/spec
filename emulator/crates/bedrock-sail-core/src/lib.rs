use std::ffi::{CString, c_char, c_void};
use std::fmt;
use std::sync::{Mutex, MutexGuard};

mod bus;
mod numeric;
mod platform;
mod translation;
pub use bus::SailBusExecutionError;

const ABI_VERSION: u32 = 5;
pub const MAX_INSTRUCTION_BYTES: usize = 18;
pub const REGISTER_COUNT: usize = 16;
pub const FLOATING_REGISTER_COUNT: usize = 16;
pub const SEGMENT_COUNT: usize = 9;
pub const CONTROL_COUNT: usize = 32;
pub const VECTOR_REGISTER_COUNT: usize = 32;
pub const PREDICATE_REGISTER_COUNT: usize = 16;
pub const VECTOR_LENGTH_BYTES: usize = 16;
pub const PREDICATE_LENGTH_BYTES: usize = 2;

static SAIL_RUNTIME: Mutex<()> = Mutex::new(());

fn runtime_lock() -> MutexGuard<'static, ()> {
    SAIL_RUNTIME
        .lock()
        .unwrap_or_else(|poisoned| poisoned.into_inner())
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
#[repr(i32)]
pub enum SailCoreStatus {
    Ok = 0,
    InvalidInstruction = 1,
    NeedsEnvironment = 2,
    Fault = 3,
    BadArgument = 4,
    OutOfMemory = 5,
    BadState = 6,
}

impl SailCoreStatus {
    fn from_raw(raw: i32) -> Self {
        match raw {
            0 => Self::Ok,
            1 => Self::InvalidInstruction,
            2 => Self::NeedsEnvironment,
            3 => Self::Fault,
            4 => Self::BadArgument,
            5 => Self::OutOfMemory,
            6 => Self::BadState,
            _ => panic!("emulator-core returned unknown status {raw}"),
        }
    }
}

#[derive(Debug)]
pub enum SailCoreCreateError {
    Status(SailCoreStatus),
}

impl fmt::Display for SailCoreCreateError {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::Status(status) => write!(formatter, "failed to create Sail core: {status:?}"),
        }
    }
}

impl std::error::Error for SailCoreCreateError {}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Default)]
#[repr(C)]
pub struct SailCoreFault {
    pub kind: i32,
    pub operation: i32,
    pub error_code: u64,
    pub bus_error: u8,
}

#[derive(Debug, Clone, PartialEq, Eq, Default)]
#[repr(C)]
pub struct SailCoreState {
    pub registers: [u64; REGISTER_COUNT],
    pub floating_registers: [u64; FLOATING_REGISTER_COUNT],
    pub vector_registers: [[u8; VECTOR_LENGTH_BYTES]; VECTOR_REGISTER_COUNT],
    pub predicate_registers: [[u8; PREDICATE_LENGTH_BYTES]; PREDICATE_REGISTER_COUNT],
    pub sp: u64,
    pub pc: u64,
    pub flags: u64,
    pub status: u64,
    pub segments: [u64; SEGMENT_COUNT],
    pub controls: [u64; CONTROL_COUNT],
    pub fstatus: u64,
    pub fflags: u64,
    pub current_dfa: u8,
    pub supervisor: u8,
    pub halted: u8,
    pub run_state: i32,
    pub fp_enabled: u8,
    pub fptrans_enabled: u8,
    pub vector_enabled: u8,
    pub cache_maintenance_granule: i64,
    pub fp_component_alignment: i64,
    pub fp_component_bitmap_bit: i64,
    pub fp_component_id: i64,
    pub fp_component_init_policy: i64,
    pub fp_component_modified: u8,
    pub fp_component_offset: i64,
    pub fp_component_present: u8,
    pub fp_component_size: i64,
    pub vector_component_alignment: i64,
    pub vector_component_bitmap_bit: i64,
    pub vector_component_id: i64,
    pub vector_component_init_policy: i64,
    pub vector_component_modified: u8,
    pub vector_component_offset: i64,
    pub vector_component_present: u8,
    pub vector_component_size: i64,
    pub vector_length_bytes: i64,
    pub machine_check_error_code: u64,
    pub machine_check_event_aux: u64,
    pub machine_check_fault_ea: u64,
    pub machine_check_fault_linear: u64,
    pub machine_check_payload: u64,
    pub machine_check_pending: u8,
    pub nmi_latched_source: u64,
    pub nmi_relatched: u8,
    pub nmi_relatched_source: u64,
    pub repeat_active: u8,
    pub repeat_body_start: u64,
    pub repeat_condition: u64,
    pub repeat_counter: u64,
    pub repeat_prefix_start: u64,
    pub repeat_remaining: u64,
    pub repeat_fixed_body: [u8; MAX_INSTRUCTION_BYTES],
    pub repeat_fixed_body_length: usize,
    pub save_area_size: i64,
    pub save_bitmap_words: i64,
    pub save_fixed_size: i64,
    pub save_format: u64,
}

#[derive(Debug, Clone, PartialEq, Eq, Default)]
pub struct SailCoreRequest {
    pub kind: i32,
    pub operation: i32,
    pub form_id: i32,
    pub access: i32,
    pub role: i32,
    pub domain: i32,
    pub segment: i64,
    pub segment_image: u64,
    pub width: i64,
    pub ordinal: i64,
    pub range_length: i64,
    pub range_wrap: bool,
    pub range_end_at_modulus: bool,
    pub effective_address: u64,
    pub linear_address: u64,
    pub value: u64,
    pub desired: u64,
    pub expected: u64,
    pub range_start: u64,
    pub range_end: u64,
    pub address_translation: bool,
    pub commit_point: bool,
    pub memory_order: i64,
    pub cache_policy: i64,
    pub suppress_fault: bool,
    pub selector: u64,
    pub auxiliary: u64,
    pub body_length: i64,
    pub payload: Vec<u8>,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Default)]
pub struct SailCoreNumericOperand {
    pub valid: bool,
    pub kind: i32,
    pub bits: u64,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Default)]
pub struct SailCoreNumericRequest {
    pub valid: bool,
    pub shape: i32,
    pub path: i32,
    pub element_width: i64,
    pub lane_count: i64,
    pub result_kind: i32,
    pub operand_count: i64,
    pub operands: [SailCoreNumericOperand; 3],
    pub result_bytes: i64,
    pub predicate_bytes: i64,
    pub rounding_mode: u64,
    pub daz: bool,
    pub ftz: bool,
    pub dn: bool,
    pub allowed_causes: u64,
    pub flags_mask: u64,
    pub transcendental: bool,
    pub contract_id: u64,
    pub contract_word: u64,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Default)]
pub struct SailCoreNumericResponse {
    pub valid: bool,
    pub primary: u64,
    pub secondary: u64,
    pub primary_nan_origin: i32,
    pub secondary_nan_origin: i32,
    pub flags_mask: u8,
    pub flags_value: u8,
    pub generated_causes: u8,
    pub accuracy_mask: u8,
    pub error0_q8_8_up: u16,
    pub error1_q8_8_up: u16,
}

#[derive(Debug, Clone, PartialEq, Eq, Default)]
pub struct SailCoreResponse {
    pub kind: i32,
    pub success: bool,
    pub fault_kind: i32,
    pub fault_cause: i64,
    pub detail: String,
    pub value: u64,
    pub secondary_value: u64,
    pub flags: u8,
    pub write_flags: bool,
    pub generated_fflags: u8,
    pub bounds_passed: bool,
    pub cache_policy: i64,
    pub access_class: i32,
    pub physical_class: i32,
    pub atomic_store_happened: bool,
    pub body: Vec<u8>,
    pub known: bool,
    pub present: bool,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Default)]
pub struct SailCoreEnvironmentState {
    pub cycle_counter: u64,
    pub retired_instruction_counter: u64,
    pub page_walk_counter: u64,
}

#[derive(Clone, Copy, Default)]
#[repr(C)]
struct RawSailCoreRequest {
    kind: i32,
    operation: i32,
    form_id: i32,
    access: i32,
    role: i32,
    domain: i32,
    segment: i64,
    segment_image: u64,
    width: i64,
    ordinal: i64,
    range_length: i64,
    range_wrap: u8,
    range_end_at_modulus: u8,
    effective_address: u64,
    linear_address: u64,
    value: u64,
    desired: u64,
    expected: u64,
    range_start: u64,
    range_end: u64,
    address_translation: u8,
    commit_point: u8,
    memory_order: i64,
    cache_policy: i64,
    suppress_fault: u8,
    selector: u64,
    auxiliary: u64,
    body_length: i64,
    payload_length: usize,
}

#[derive(Clone, Copy)]
#[repr(C)]
struct RawSailCoreResponse {
    kind: i32,
    success: u8,
    fault_kind: i32,
    fault_cause: i64,
    detail: *const c_char,
    value: u64,
    secondary_value: u64,
    flags: u8,
    write_flags: u8,
    generated_fflags: u8,
    bounds_passed: u8,
    cache_policy: i64,
    access_class: i32,
    physical_class: i32,
    atomic_store_happened: u8,
    body_bytes: *const u8,
    body_length: usize,
    known: u8,
    present: u8,
}

impl RawSailCoreRequest {
    fn into_request(self, payload: Vec<u8>) -> SailCoreRequest {
        SailCoreRequest {
            kind: self.kind,
            operation: self.operation,
            form_id: self.form_id,
            access: self.access,
            role: self.role,
            domain: self.domain,
            segment: self.segment,
            segment_image: self.segment_image,
            width: self.width,
            ordinal: self.ordinal,
            range_length: self.range_length,
            range_wrap: self.range_wrap != 0,
            range_end_at_modulus: self.range_end_at_modulus != 0,
            effective_address: self.effective_address,
            linear_address: self.linear_address,
            value: self.value,
            desired: self.desired,
            expected: self.expected,
            range_start: self.range_start,
            range_end: self.range_end,
            address_translation: self.address_translation != 0,
            commit_point: self.commit_point != 0,
            memory_order: self.memory_order,
            cache_policy: self.cache_policy,
            suppress_fault: self.suppress_fault != 0,
            selector: self.selector,
            auxiliary: self.auxiliary,
            body_length: self.body_length,
            payload,
        }
    }
}

impl RawSailCoreResponse {
    fn from_response(response: &SailCoreResponse, detail: *const c_char) -> Self {
        Self {
            kind: response.kind,
            success: response.success.into(),
            fault_kind: response.fault_kind,
            fault_cause: response.fault_cause,
            detail,
            value: response.value,
            secondary_value: response.secondary_value,
            flags: response.flags,
            write_flags: response.write_flags.into(),
            generated_fflags: response.generated_fflags,
            bounds_passed: response.bounds_passed.into(),
            cache_policy: response.cache_policy,
            access_class: response.access_class,
            physical_class: response.physical_class,
            atomic_store_happened: response.atomic_store_happened.into(),
            body_bytes: response.body.as_ptr(),
            body_length: response.body.len(),
            known: response.known.into(),
            present: response.present.into(),
        }
    }
}

pub struct SailCore {
    raw: *mut c_void,
    environment: SailCoreEnvironmentState,
}

// The core pointer is exclusively owned by `SailCore`. Moving that ownership
// to an execution thread is safe; all access still requires `&self`/`&mut self`
// and the generated Sail runtime is serialized by `SAIL_RUNTIME`.
unsafe impl Send for SailCore {}

impl fmt::Debug for SailCore {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        formatter.debug_struct("SailCore").finish_non_exhaustive()
    }
}

impl SailCore {
    pub fn new() -> Result<Self, SailCoreCreateError> {
        let _runtime = runtime_lock();
        let version = unsafe { ffi::bedrock_core_abi_version() };
        assert_eq!(version, ABI_VERSION, "emulator-core ABI version mismatch");
        let state_size = unsafe { ffi::bedrock_core_state_size() };
        assert_eq!(
            state_size,
            std::mem::size_of::<SailCoreState>(),
            "emulator-core state ABI layout mismatch"
        );
        let raw = unsafe { ffi::bedrock_core_create() };
        if raw.is_null() {
            return Err(SailCoreCreateError::Status(SailCoreStatus::OutOfMemory));
        }
        Ok(Self {
            raw,
            environment: SailCoreEnvironmentState::default(),
        })
    }

    pub fn reset(&mut self) -> SailCoreStatus {
        let _runtime = runtime_lock();
        let status = SailCoreStatus::from_raw(unsafe { ffi::bedrock_core_reset(self.raw) });
        if status == SailCoreStatus::Ok {
            self.environment = SailCoreEnvironmentState::default();
        }
        status
    }
    pub fn pc(&self) -> Result<u64, SailCoreStatus> {
        let _runtime = runtime_lock();
        read_value(self.raw, |raw, value| unsafe {
            ffi::bedrock_core_get_pc(raw, value)
        })
    }
    pub fn set_pc(&mut self, value: u64) -> SailCoreStatus {
        let _runtime = runtime_lock();
        SailCoreStatus::from_raw(unsafe { ffi::bedrock_core_set_pc(self.raw, value) })
    }
    pub fn sp(&self) -> Result<u64, SailCoreStatus> {
        let _runtime = runtime_lock();
        read_value(self.raw, |raw, value| unsafe {
            ffi::bedrock_core_get_sp(raw, value)
        })
    }
    pub fn set_sp(&mut self, value: u64) -> SailCoreStatus {
        let _runtime = runtime_lock();
        SailCoreStatus::from_raw(unsafe { ffi::bedrock_core_set_sp(self.raw, value) })
    }
    pub fn register(&self, index: u32) -> Result<u64, SailCoreStatus> {
        let _runtime = runtime_lock();
        read_value(self.raw, |raw, value| unsafe {
            ffi::bedrock_core_get_register(raw, index, value)
        })
    }
    pub fn set_register(&mut self, index: u32, value: u64) -> SailCoreStatus {
        let _runtime = runtime_lock();
        SailCoreStatus::from_raw(unsafe { ffi::bedrock_core_set_register(self.raw, index, value) })
    }
    pub fn status(&self) -> Result<u64, SailCoreStatus> {
        let _runtime = runtime_lock();
        read_value(self.raw, |raw, value| unsafe {
            ffi::bedrock_core_get_status(raw, value)
        })
    }
    pub fn control(&self, index: u32) -> Result<u64, SailCoreStatus> {
        let _runtime = runtime_lock();
        read_value(self.raw, |raw, value| unsafe {
            ffi::bedrock_core_get_control(raw, index, value)
        })
    }
    pub fn is_supervisor(&self) -> Result<bool, SailCoreStatus> {
        let _runtime = runtime_lock();
        let mut value = 0;
        let status = SailCoreStatus::from_raw(unsafe {
            ffi::bedrock_core_is_supervisor(self.raw, &mut value)
        });
        if status == SailCoreStatus::Ok {
            Ok(value != 0)
        } else {
            Err(status)
        }
    }
    pub fn state(&self) -> Result<SailCoreState, SailCoreStatus> {
        let _runtime = runtime_lock();
        let mut state = SailCoreState::default();
        let status =
            SailCoreStatus::from_raw(unsafe { ffi::bedrock_core_get_state(self.raw, &mut state) });
        if status == SailCoreStatus::Ok {
            Ok(state)
        } else {
            Err(status)
        }
    }
    pub fn set_state(&mut self, state: SailCoreState) -> SailCoreStatus {
        let _runtime = runtime_lock();
        SailCoreStatus::from_raw(unsafe { ffi::bedrock_core_set_state(self.raw, &state) })
    }
    pub fn execute(&mut self, bytes: &[u8]) -> SailCoreStatus {
        if bytes.is_empty() || bytes.len() > MAX_INSTRUCTION_BYTES {
            return SailCoreStatus::BadArgument;
        }
        let _runtime = runtime_lock();
        SailCoreStatus::from_raw(unsafe {
            ffi::bedrock_core_execute(self.raw, bytes.as_ptr(), bytes.len())
        })
    }
    pub fn last_fault(&self) -> Result<SailCoreFault, SailCoreStatus> {
        let _runtime = runtime_lock();
        let mut fault = SailCoreFault::default();
        let status =
            SailCoreStatus::from_raw(unsafe { ffi::bedrock_core_last_fault(self.raw, &mut fault) });
        if status == SailCoreStatus::Fault {
            Ok(fault)
        } else {
            Err(status)
        }
    }
    pub fn last_request(&self) -> Result<SailCoreRequest, SailCoreStatus> {
        let _runtime = runtime_lock();
        let mut request = RawSailCoreRequest::default();
        let status = SailCoreStatus::from_raw(unsafe {
            ffi::bedrock_core_last_request(self.raw, &mut request)
        });
        if status != SailCoreStatus::NeedsEnvironment {
            return Err(status);
        }
        let mut payload_length = 0;
        let payload_status = SailCoreStatus::from_raw(unsafe {
            ffi::bedrock_core_request_payload(
                self.raw,
                std::ptr::null_mut(),
                0,
                &mut payload_length,
            )
        });
        if payload_status != SailCoreStatus::NeedsEnvironment {
            return Err(payload_status);
        }
        let mut payload = vec![0; payload_length];
        let payload_status = SailCoreStatus::from_raw(unsafe {
            ffi::bedrock_core_request_payload(
                self.raw,
                payload.as_mut_ptr(),
                payload.len(),
                &mut payload_length,
            )
        });
        if payload_status == SailCoreStatus::NeedsEnvironment {
            Ok(request.into_request(payload))
        } else {
            Err(payload_status)
        }
    }
    pub fn resume(&mut self, response: SailCoreResponse) -> SailCoreStatus {
        let detail = match CString::new(response.detail.as_str()) {
            Ok(detail) => detail,
            Err(_) => return SailCoreStatus::BadArgument,
        };
        let raw_response = RawSailCoreResponse::from_response(&response, detail.as_ptr());
        let _runtime = runtime_lock();
        SailCoreStatus::from_raw(unsafe { ffi::bedrock_core_resume(self.raw, &raw_response) })
    }
    pub fn cancel(&mut self) -> SailCoreStatus {
        let _runtime = runtime_lock();
        SailCoreStatus::from_raw(unsafe { ffi::bedrock_core_cancel(self.raw) })
    }

    pub fn environment_state(&self) -> SailCoreEnvironmentState {
        self.environment
    }

    pub fn set_environment_state(&mut self, state: SailCoreEnvironmentState) {
        self.environment = state;
    }
}

impl Drop for SailCore {
    fn drop(&mut self) {
        let _runtime = runtime_lock();
        unsafe { ffi::bedrock_core_destroy(self.raw) };
    }
}

fn read_value(
    raw: *mut c_void,
    call: impl FnOnce(*mut c_void, *mut u64) -> i32,
) -> Result<u64, SailCoreStatus> {
    let mut value = 0;
    match SailCoreStatus::from_raw(call(raw, &mut value)) {
        SailCoreStatus::Ok => Ok(value),
        other => Err(other),
    }
}

mod ffi {
    use std::ffi::c_void;
    unsafe extern "C" {
        pub fn bedrock_core_abi_version() -> u32;
        pub fn bedrock_core_state_size() -> usize;
        pub fn bedrock_core_create() -> *mut c_void;
        pub fn bedrock_core_destroy(core: *mut c_void);
        pub fn bedrock_core_reset(core: *mut c_void) -> i32;
        pub fn bedrock_core_get_pc(core: *mut c_void, value: *mut u64) -> i32;
        pub fn bedrock_core_set_pc(core: *mut c_void, value: u64) -> i32;
        pub fn bedrock_core_get_sp(core: *mut c_void, value: *mut u64) -> i32;
        pub fn bedrock_core_set_sp(core: *mut c_void, value: u64) -> i32;
        pub fn bedrock_core_get_register(core: *mut c_void, index: u32, value: *mut u64) -> i32;
        pub fn bedrock_core_set_register(core: *mut c_void, index: u32, value: u64) -> i32;
        pub fn bedrock_core_get_status(core: *mut c_void, value: *mut u64) -> i32;
        pub fn bedrock_core_get_control(core: *mut c_void, index: u32, value: *mut u64) -> i32;
        pub fn bedrock_core_is_supervisor(core: *mut c_void, value: *mut u8) -> i32;
        pub fn bedrock_core_get_state(core: *mut c_void, state: *mut super::SailCoreState) -> i32;
        pub fn bedrock_core_set_state(core: *mut c_void, state: *const super::SailCoreState)
        -> i32;
        pub fn bedrock_core_execute(core: *mut c_void, bytes: *const u8, length: usize) -> i32;
        pub fn bedrock_core_last_fault(core: *mut c_void, fault: *mut super::SailCoreFault) -> i32;
        pub fn bedrock_core_last_request(
            core: *mut c_void,
            request: *mut super::RawSailCoreRequest,
        ) -> i32;
        pub fn bedrock_core_request_payload(
            core: *mut c_void,
            buffer: *mut u8,
            capacity: usize,
            length: *mut usize,
        ) -> i32;
        pub fn bedrock_core_cancel(core: *mut c_void) -> i32;
        pub fn bedrock_core_resume(
            core: *mut c_void,
            response: *const super::RawSailCoreResponse,
        ) -> i32;
    }
}

#[cfg(test)]
mod tests {
    use super::{SailCore, SailCoreResponse, SailCoreStatus};

    #[test]
    fn executes_generated_nop_and_exposes_register_state() {
        let mut core = SailCore::new().unwrap();
        assert_eq!(core.pc(), Ok(0));
        assert_eq!(
            core.set_register(7, 0x55aa_55aa_55aa_55aa),
            SailCoreStatus::Ok
        );
        assert_eq!(core.register(7), Ok(0x55aa_55aa_55aa_55aa));
        assert_eq!(core.execute(&[0x01]), SailCoreStatus::Ok);
        assert_eq!(core.pc(), Ok(1));
    }

    #[test]
    fn sub_quad_register_moves_zero_extend_the_result() {
        for (instruction, expected) in [
            ([0xa6, 0x01], 0x88),
            ([0xa7, 0x01], 0x7788),
            ([0x80, 0x01], 0x5566_7788),
        ] {
            let mut core = SailCore::new().unwrap();
            assert_eq!(
                core.set_register(0, 0x1122_3344_5566_7788),
                SailCoreStatus::Ok
            );
            assert_eq!(
                core.set_register(1, 0xffff_ffff_ffff_ffff),
                SailCoreStatus::Ok
            );
            assert_eq!(core.execute(&instruction), SailCoreStatus::Ok);
            assert_eq!(core.register(1), Ok(expected));
        }
    }

    #[test]
    fn register_add_executes_through_the_uop_program() {
        let mut core = SailCore::new().unwrap();
        assert_eq!(
            core.set_register(0, 0xffff_ffff_0000_0002),
            SailCoreStatus::Ok
        );
        assert_eq!(
            core.set_register(1, 0xffff_ffff_0000_0003),
            SailCoreStatus::Ok
        );

        // ADD.L R0, R1
        assert_eq!(core.execute(&[0x82, 0x01]), SailCoreStatus::Ok);
        assert_eq!(core.register(1), Ok(5));
        assert_eq!(core.pc(), Ok(2));
    }

    #[test]
    fn memory_move_resumes_the_uop_program_after_a_load() {
        const REQUEST_MEMORY_READ: i32 = 3;
        const RESPONSE_READ: i32 = 2;

        let mut core = SailCore::new().unwrap();
        assert_eq!(core.set_register(0, 0x100), SailCoreStatus::Ok);

        // MOV.B [R0], R0
        assert_eq!(
            core.execute(&[0xc1, 0x00, 0x00]),
            SailCoreStatus::NeedsEnvironment
        );
        let request = core.last_request().unwrap();
        assert_eq!(request.kind, REQUEST_MEMORY_READ);
        assert_eq!(request.effective_address, 0x100);
        assert_eq!(request.width, 1);

        assert_eq!(
            core.resume(SailCoreResponse {
                kind: RESPONSE_READ,
                success: true,
                value: 0xa5,
                known: true,
                present: true,
                ..SailCoreResponse::default()
            }),
            SailCoreStatus::Ok
        );
        assert_eq!(core.register(0), Ok(0xa5));
        assert_eq!(core.pc(), Ok(3));
    }

    #[test]
    fn ea_postincrement_is_an_explicit_speculative_uop() {
        const RESPONSE_READ: i32 = 2;

        let mut core = SailCore::new().unwrap();
        assert_eq!(core.set_register(2, 0x100), SailCoreStatus::Ok);
        assert_eq!(core.set_register(3, 4), SailCoreStatus::Ok);

        // MOV.B [DS:R2 + R3++], R0
        assert_eq!(
            core.execute(&[0xc9, 0x00, 0x68, 0x80, 0x23]),
            SailCoreStatus::NeedsEnvironment
        );
        let request = core.last_request().unwrap();
        assert_eq!(request.effective_address, 0x104);
        // The postincrement remains speculative until the instruction commits.
        assert_eq!(core.register(3), Ok(4));

        assert_eq!(
            core.resume(SailCoreResponse {
                kind: RESPONSE_READ,
                success: true,
                value: 0x7b,
                known: true,
                present: true,
                ..SailCoreResponse::default()
            }),
            SailCoreStatus::Ok
        );
        assert_eq!(core.register(0), Ok(0x7b));
        assert_eq!(core.register(3), Ok(5));
        assert_eq!(core.pc(), Ok(5));
    }

    #[test]
    fn resumes_push_through_environment_requests() {
        const REQUEST_MEMORY_PROBE: i32 = 2;
        const REQUEST_MEMORY_STORE: i32 = 4;
        const REQUEST_STACK_RANGE: i32 = 7;
        const RESPONSE_PROBE: i32 = 1;
        const RESPONSE_STORE_ACK: i32 = 3;
        const RESPONSE_STACK_RANGE: i32 = 4;

        let mut core = SailCore::new().unwrap();
        assert_eq!(core.set_sp(0x1000), SailCoreStatus::Ok);
        assert_eq!(
            core.set_register(0, 0x1122_3344_5566_7788),
            SailCoreStatus::Ok
        );
        assert_eq!(core.execute(&[0x30]), SailCoreStatus::NeedsEnvironment);

        let mut status = SailCoreStatus::NeedsEnvironment;
        for _ in 0..8 {
            if status != SailCoreStatus::NeedsEnvironment {
                break;
            }
            let request = core.last_request().unwrap();
            assert!(request.payload.is_empty());
            let response_kind = match request.kind {
                REQUEST_STACK_RANGE => RESPONSE_STACK_RANGE,
                REQUEST_MEMORY_PROBE => RESPONSE_PROBE,
                REQUEST_MEMORY_STORE => {
                    assert_eq!(request.value, 0x1122_3344_5566_7788);
                    RESPONSE_STORE_ACK
                }
                kind => panic!("unexpected PUSH environment request {kind}"),
            };
            status = core.resume(SailCoreResponse {
                kind: response_kind,
                success: true,
                bounds_passed: true,
                known: true,
                present: true,
                ..SailCoreResponse::default()
            });
        }

        assert_eq!(status, SailCoreStatus::Ok);
        assert_eq!(core.pc(), Ok(1));
        assert_eq!(core.sp(), Ok(0x0ff8));
        assert_eq!(
            core.resume(SailCoreResponse::default()),
            SailCoreStatus::BadState
        );
    }

    #[test]
    fn cancelling_pending_execution_restores_idle_state() {
        let mut core = SailCore::new().unwrap();
        assert_eq!(core.set_sp(0x1000), SailCoreStatus::Ok);
        assert_eq!(core.execute(&[0x30]), SailCoreStatus::NeedsEnvironment);
        assert_eq!(core.cancel(), SailCoreStatus::Ok);
        assert_eq!(core.cancel(), SailCoreStatus::BadState);
        assert_eq!(core.execute(&[0x01]), SailCoreStatus::Ok);
        assert_eq!(core.pc(), Ok(1));
        assert_eq!(core.sp(), Ok(0x1000));
    }

    #[test]
    fn state_snapshot_round_trips_all_storage_classes() {
        let mut core = SailCore::new().unwrap();
        let original = core.state().unwrap();
        let mut state = original.clone();
        state.registers[3] = 0x1111_2222_3333_4444;
        state.floating_registers[5] = 0x5555_6666_7777_8888;
        state.vector_registers[7][11] = 0xa5;
        state.predicate_registers[9][1] = 0x5a;
        state.sp = 0x1000;
        state.pc = 0x2000;
        state.flags = 0x0d;
        state.status = 0x101;
        state.segments[2] = 0x1234_5000;
        state.controls[4] = 0xfeed_face_cafe_beef;
        state.fstatus = 0x123;
        state.fflags = 0x1f;
        let expected = state.clone();

        assert_eq!(core.set_state(state), SailCoreStatus::Ok);
        assert_eq!(core.state(), Ok(expected));
        assert_eq!(core.set_state(original.clone()), SailCoreStatus::Ok);
        assert_eq!(core.state(), Ok(original));
    }

    #[test]
    fn state_restore_is_rejected_while_execution_is_pending() {
        let mut core = SailCore::new().unwrap();
        assert_eq!(core.set_sp(0x1000), SailCoreStatus::Ok);
        let state = core.state().unwrap();
        assert_eq!(core.execute(&[0x30]), SailCoreStatus::NeedsEnvironment);
        assert_eq!(core.set_state(state), SailCoreStatus::BadState);
        assert_eq!(core.cancel(), SailCoreStatus::Ok);
    }

    #[test]
    fn scalar_and_vector_fp_execute_without_numeric_requests() {
        let mut scalar = SailCore::new().unwrap();
        let mut scalar_state = scalar.state().unwrap();
        scalar_state.fp_enabled = 1;
        scalar_state.floating_registers[0] = u64::from(1.0_f32.to_bits());
        scalar_state.floating_registers[1] = u64::from(2.0_f32.to_bits());
        assert_eq!(scalar.set_state(scalar_state), SailCoreStatus::Ok);
        assert_eq!(scalar.execute(&[0xc2, 0x82, 0x10]), SailCoreStatus::Ok);
        assert_eq!(
            scalar.state().unwrap().floating_registers[0],
            u64::from(3.0_f32.to_bits())
        );

        let mut vector = SailCore::new().unwrap();
        let mut vector_state = vector.state().unwrap();
        vector_state.fp_enabled = 1;
        vector_state.predicate_registers[0] = [0xff, 0xff];
        for lane in 0..4 {
            vector_state.vector_registers[0][lane * 4..lane * 4 + 4]
                .copy_from_slice(&1.0_f32.to_bits().to_le_bytes());
            vector_state.vector_registers[1][lane * 4..lane * 4 + 4]
                .copy_from_slice(&2.0_f32.to_bits().to_le_bytes());
        }
        assert_eq!(vector.set_state(vector_state), SailCoreStatus::Ok);
        // VADD.S P0, V1, V0
        assert_eq!(
            vector.execute(&[0xcb, 0xf7, 0x83, 0x00, 0x20]),
            SailCoreStatus::Ok
        );
        for lane in 0..4 {
            assert_eq!(
                &vector.state().unwrap().vector_registers[0][lane * 4..lane * 4 + 4],
                &3.0_f32.to_bits().to_le_bytes()
            );
        }
    }
}
