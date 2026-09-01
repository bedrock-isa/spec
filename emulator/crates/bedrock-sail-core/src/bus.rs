use super::{SailCore, SailCoreFault, SailCoreRequest, SailCoreResponse, SailCoreStatus};
use crate::translation::{self, TranslationAccess, TranslationError};
use bedrock_bus::{Bus, BusError};
use std::fmt;

const REQUEST_TRANSLATION_EXECUTE_PROBE: i32 = 1;
const REQUEST_MEMORY_PROBE: i32 = 2;
const REQUEST_MEMORY_READ: i32 = 3;
const REQUEST_MEMORY_STORE: i32 = 4;
const REQUEST_COMPOUND_MEMORY_STORE: i32 = 5;
const REQUEST_NON_TEMPORAL_STORE: i32 = 6;
const REQUEST_STACK_RANGE: i32 = 7;
const REQUEST_SEGMENT_BOUNDS: i32 = 8;
const REQUEST_ATOMIC_RMW: i32 = 9;
const REQUEST_ADDRESS_TRANSLATE: i32 = 10;
const REQUEST_PHYSICAL_PTE_READ: i32 = 11;
const REQUEST_CACHE_MAINTENANCE: i32 = 12;
const REQUEST_PREFETCH_HINT: i32 = 13;
const REQUEST_FENCE_COMPLETION: i32 = 14;
const REQUEST_TLB_INVALIDATE: i32 = 15;
const REQUEST_TRANSLATION_QUERY: i32 = 16;
const REQUEST_CONTEXT_SWITCH: i32 = 17;
const REQUEST_STATE_SAVE: i32 = 18;
const REQUEST_STATE_RESTORE: i32 = 19;
const REQUEST_REPEAT_BODY_FETCH: i32 = 20;
const REQUEST_EVENT_FRAME_ACCESS: i32 = 21;
const REQUEST_CPUID_QUERY: i32 = 22;
const REQUEST_PERFORMANCE_COUNTER: i32 = 23;
const REQUEST_CONTROL_TRANSITION: i32 = 24;
const REQUEST_RESET_SERIALIZE: i32 = 25;
const REQUEST_VECTOR_MEMORY_READ: i32 = 26;
const REQUEST_VECTOR_MEMORY_WRITE: i32 = 27;

const RESPONSE_TRANSLATION: i32 = 0;
const RESPONSE_PROBE: i32 = 1;
const RESPONSE_READ: i32 = 2;
const RESPONSE_STORE_ACK: i32 = 3;
const RESPONSE_STACK_RANGE: i32 = 4;
const RESPONSE_SEGMENT_BOUNDS: i32 = 5;
const RESPONSE_ATOMIC: i32 = 7;
const RESPONSE_ADDRESS_TRANSLATION: i32 = 8;
const RESPONSE_PTE_READ: i32 = 9;
const RESPONSE_CACHE_MAINTENANCE: i32 = 10;
const RESPONSE_FENCE_COMPLETION: i32 = 11;
const RESPONSE_TLB_OPERATION: i32 = 12;
const RESPONSE_TRANSLATION_QUERY: i32 = 13;
const RESPONSE_CONTEXT_SWITCH: i32 = 14;
const RESPONSE_STATE_SAVE: i32 = 15;
const RESPONSE_STATE_RESTORE: i32 = 16;
const RESPONSE_REPEAT_FETCH: i32 = 17;
const RESPONSE_EVENT_FRAME: i32 = 18;
const RESPONSE_CPUID_QUERY: i32 = 20;
const RESPONSE_PERFORMANCE_COUNTER: i32 = 21;
const RESPONSE_CONTROL_TRANSITION: i32 = 22;
const RESPONSE_RESET_SERIALIZE: i32 = 23;
const RESPONSE_VECTOR_MEMORY: i32 = 19;

const ACCESS_LOAD: i32 = 1;
const ACCESS_STORE: i32 = 2;
const ACCESS_READ_MODIFY_WRITE: i32 = 3;
const ACCESS_EXECUTE: i32 = 4;
const ACCESS_STACK_READ: i32 = 5;
const ACCESS_STACK_WRITE: i32 = 6;
const ACCESS_ADDRESS_ONLY: i32 = 7;

const ROLE_EVENT_ENTRY_TARGET: i32 = 6;
const ROLE_EVENT_FRAME_RANGE: i32 = 7;
const ROLE_EVENT_FRAME_STORE: i32 = 8;

#[derive(Debug)]
pub enum SailBusExecutionError {
    Core(SailCoreStatus),
    Fault {
        fault: SailCoreFault,
        request: Option<Box<SailCoreRequest>>,
    },
    Bus(BusError),
    UnsupportedRequest(i32),
    UnsupportedNumericOperation(i32),
    InvalidFraming {
        first: u8,
        second: Option<u8>,
    },
}

impl fmt::Display for SailBusExecutionError {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::Core(status) => write!(formatter, "Sail core returned {status:?}"),
            Self::Fault { fault, .. } => {
                write!(formatter, "Sail execution fault: {fault:?}")
            }
            Self::Bus(error) => error.fmt(formatter),
            Self::UnsupportedRequest(kind) => {
                write!(
                    formatter,
                    "unsupported Sail environment request kind {kind}"
                )
            }
            Self::UnsupportedNumericOperation(operation) => {
                write!(formatter, "unsupported Sail numeric operation {operation}")
            }
            Self::InvalidFraming { first, second } => write!(
                formatter,
                "invalid instruction framing bytes {first:#04x}, {second:?}"
            ),
        }
    }
}

impl std::error::Error for SailBusExecutionError {}

impl From<BusError> for SailBusExecutionError {
    fn from(error: BusError) -> Self {
        Self::Bus(error)
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
enum SailBusCompletion {
    Retired,
    VectorLane,
}

impl SailCore {
    /// Fetches and executes one instruction at the current PC.
    pub fn step_on_bus(&mut self, bus: &mut impl Bus) -> Result<(), SailBusExecutionError> {
        let monitoring_enabled =
            self.control(0x1100).map_err(SailBusExecutionError::Core)? & 1 != 0;
        if monitoring_enabled {
            self.environment.cycle_counter = self.environment.cycle_counter.wrapping_add(1);
        }
        bus.begin_transaction()?;
        let result = (|| {
            let pc = self.pc().map_err(SailBusExecutionError::Core)?;
            let bytes = fetch_virtual_instruction(self, bus, pc)?;
            self.execute_bus_transaction(bus, &bytes)
        })();
        if let Ok(completion) = &result {
            bus.commit_transaction();
            if monitoring_enabled && *completion == SailBusCompletion::Retired {
                self.environment.retired_instruction_counter =
                    self.environment.retired_instruction_counter.wrapping_add(1);
            }
        } else {
            bus.rollback_transaction();
        }
        result.map(|_| ())
    }

    /// Executes one already-framed instruction inside one bus transaction.
    ///
    pub fn execute_on_bus(
        &mut self,
        bus: &mut impl Bus,
        bytes: &[u8],
    ) -> Result<(), SailBusExecutionError> {
        bus.begin_transaction()?;
        let result = self.execute_bus_transaction(bus, bytes);
        if result.is_ok() {
            bus.commit_transaction();
        } else {
            bus.rollback_transaction();
        }
        result.map(|_| ())
    }

    fn execute_bus_transaction(
        &mut self,
        bus: &mut impl Bus,
        bytes: &[u8],
    ) -> Result<SailBusCompletion, SailBusExecutionError> {
        let mut status = self.execute(bytes);
        let mut active_request = None;
        loop {
            match status {
                SailCoreStatus::Ok => return Ok(SailBusCompletion::Retired),
                SailCoreStatus::VectorLane => return Ok(SailBusCompletion::VectorLane),
                SailCoreStatus::NeedsEnvironment => {
                    let request = self.last_request().map_err(SailBusExecutionError::Core)?;
                    active_request = Some(Box::new(request.clone()));
                    let response = match service_request(self, bus, &request) {
                        Ok(response) => response,
                        Err(error) => {
                            let cancel = self.cancel();
                            if cancel != SailCoreStatus::Ok {
                                return Err(SailBusExecutionError::Core(cancel));
                            }
                            return Err(error);
                        }
                    };
                    status = self.resume(response);
                }
                SailCoreStatus::Fault => {
                    return Err(SailBusExecutionError::Fault {
                        fault: self.last_fault().map_err(SailBusExecutionError::Core)?,
                        request: active_request,
                    });
                }
                other => return Err(SailBusExecutionError::Core(other)),
            }
        }
    }
}

fn fetch_instruction(bus: &mut impl Bus, pc: u64) -> Result<Vec<u8>, SailBusExecutionError> {
    fetch_instruction_with(pc, |address| Ok(bus.read_u8(address)?))
}

fn fetch_virtual_instruction(
    core: &mut SailCore,
    bus: &mut impl Bus,
    pc: u64,
) -> Result<Vec<u8>, SailBusExecutionError> {
    let state = core.state().map_err(SailBusExecutionError::Core)?;
    let ptcr = state.controls.base_ptcr;
    fetch_instruction_with(pc, |effective| {
        let linear = translation::segment_linear(state.segments[0], effective)
            .map_err(|fault| fetch_translation_fault(fault, effective, effective))?;
        if ptcr & 1 != 0 {
            core.environment.page_walk_counter = core.environment.page_walk_counter.wrapping_add(1);
        }
        let translated = translation::translate(
            bus,
            linear,
            ptcr,
            TranslationAccess::Execute,
            false,
            state.supervisor != 0,
        )
        .map_err(|error| match error {
            TranslationError::Fault(fault) => fetch_translation_fault(fault, effective, linear),
            TranslationError::Bus(error) => SailBusExecutionError::Bus(error),
        })?;
        if translated.access_class != 0 {
            return Err(fetch_translation_fault(
                translation::TranslationFault {
                    kind: translation::FAULT_ACCESS,
                    cause: 2,
                    detail: "instruction fetch from MMIO is not permitted".to_owned(),
                },
                effective,
                linear,
            ));
        }
        if translated.physical_class != 0 {
            return Err(fetch_translation_fault(
                translation::TranslationFault {
                    kind: translation::FAULT_TRANSLATION,
                    cause: 6,
                    detail: "Normal instruction mapping targets Device memory".to_owned(),
                },
                effective,
                linear,
            ));
        }
        Ok(bus.read_u8(translated.address)?)
    })
}

fn fetch_translation_fault(
    fault: translation::TranslationFault,
    effective: u64,
    linear: u64,
) -> SailBusExecutionError {
    SailBusExecutionError::Fault {
        fault: SailCoreFault {
            kind: fault.kind,
            error_code: fault.cause as u64 | (3 << 8) | (1 << 27),
            ..SailCoreFault::default()
        },
        request: Some(Box::new(SailCoreRequest {
            access: ACCESS_EXECUTE,
            domain: 2,
            segment: 0,
            width: 1,
            effective_address: effective,
            linear_address: linear,
            address_translation: true,
            ..SailCoreRequest::default()
        })),
    }
}

fn fetch_instruction_with(
    pc: u64,
    mut read: impl FnMut(u64) -> Result<u8, SailBusExecutionError>,
) -> Result<Vec<u8>, SailBusExecutionError> {
    let first = read(pc)?;
    let (length, second) = if first & 0x80 == 0 {
        (1usize, None)
    } else if first & 0xc0 == 0x80 {
        (2usize, None)
    } else {
        let second_address = pc.checked_add(1).ok_or(BusError::OutOfRange { addr: pc })?;
        let second = read(second_address)?;
        let length = usize::from(3 + ((first >> 2) & 0x0f));
        let selector = ((first & 0x03) << 4) | (second >> 4);
        let allocation_prefix = ((first & 0x03) << 6) | (second >> 2);
        let minimum = if selector <= 59 {
            3
        } else if selector <= 62 {
            4
        } else if allocation_prefix == 255 {
            6
        } else {
            5
        };
        if length < minimum {
            return Err(SailBusExecutionError::InvalidFraming {
                first,
                second: Some(second),
            });
        }
        (length, Some(second))
    };
    let mut bytes = Vec::with_capacity(length);
    bytes.push(first);
    if let Some(second) = second {
        bytes.push(second);
    }
    while bytes.len() < length {
        let address = pc
            .checked_add(bytes.len() as u64)
            .ok_or(BusError::OutOfRange { addr: pc })?;
        bytes.push(read(address)?);
    }
    Ok(bytes)
}

fn service_request(
    core: &mut SailCore,
    bus: &mut impl Bus,
    request: &SailCoreRequest,
) -> Result<SailCoreResponse, SailBusExecutionError> {
    let response_kind = match request.kind {
        REQUEST_TRANSLATION_EXECUTE_PROBE => RESPONSE_TRANSLATION,
        REQUEST_MEMORY_PROBE => RESPONSE_PROBE,
        REQUEST_MEMORY_READ => RESPONSE_READ,
        REQUEST_MEMORY_STORE | REQUEST_COMPOUND_MEMORY_STORE | REQUEST_NON_TEMPORAL_STORE => {
            RESPONSE_STORE_ACK
        }
        REQUEST_STACK_RANGE => RESPONSE_STACK_RANGE,
        REQUEST_SEGMENT_BOUNDS => RESPONSE_SEGMENT_BOUNDS,
        REQUEST_ATOMIC_RMW => RESPONSE_ATOMIC,
        REQUEST_ADDRESS_TRANSLATE => RESPONSE_ADDRESS_TRANSLATION,
        REQUEST_PHYSICAL_PTE_READ => RESPONSE_PTE_READ,
        REQUEST_CACHE_MAINTENANCE | REQUEST_PREFETCH_HINT => RESPONSE_CACHE_MAINTENANCE,
        REQUEST_FENCE_COMPLETION => RESPONSE_FENCE_COMPLETION,
        REQUEST_TLB_INVALIDATE => RESPONSE_TLB_OPERATION,
        REQUEST_TRANSLATION_QUERY => RESPONSE_TRANSLATION_QUERY,
        REQUEST_CONTEXT_SWITCH => RESPONSE_CONTEXT_SWITCH,
        REQUEST_STATE_SAVE => RESPONSE_STATE_SAVE,
        REQUEST_STATE_RESTORE => RESPONSE_STATE_RESTORE,
        REQUEST_REPEAT_BODY_FETCH => RESPONSE_REPEAT_FETCH,
        REQUEST_EVENT_FRAME_ACCESS => RESPONSE_EVENT_FRAME,
        REQUEST_CPUID_QUERY => RESPONSE_CPUID_QUERY,
        REQUEST_PERFORMANCE_COUNTER => RESPONSE_PERFORMANCE_COUNTER,
        REQUEST_CONTROL_TRANSITION => RESPONSE_CONTROL_TRANSITION,
        REQUEST_RESET_SERIALIZE => RESPONSE_RESET_SERIALIZE,
        REQUEST_VECTOR_MEMORY_READ | REQUEST_VECTOR_MEMORY_WRITE => RESPONSE_VECTOR_MEMORY,
        kind => return Err(SailBusExecutionError::UnsupportedRequest(kind)),
    };

    let mut response = SailCoreResponse {
        kind: response_kind,
        success: true,
        bounds_passed: true,
        known: true,
        present: true,
        ..SailCoreResponse::default()
    };

    match request.kind {
        REQUEST_CPUID_QUERY => {
            response.value = crate::platform::cpuid_query(request.selector);
            return Ok(response);
        }
        REQUEST_PERFORMANCE_COUNTER => {
            let value = match request.selector {
                1 => Some(core.environment.cycle_counter),
                2 => Some(core.environment.retired_instruction_counter),
                3 => Some(core.environment.page_walk_counter),
                _ => None,
            };
            response.known = value.is_some();
            response.present = value.is_some();
            response.value = value.unwrap_or_default();
            return Ok(response);
        }
        REQUEST_FENCE_COMPLETION
        | REQUEST_TLB_INVALIDATE
        | REQUEST_TRANSLATION_QUERY
        | REQUEST_CONTEXT_SWITCH
        | REQUEST_CONTROL_TRANSITION
        | REQUEST_RESET_SERIALIZE => return Ok(response),
        _ => {}
    }
    if request.kind == REQUEST_STACK_RANGE || request.kind == REQUEST_SEGMENT_BOUNDS {
        response.bounds_passed = stack_range_in_bounds(request);
        return Ok(response);
    }

    if request.address_translation {
        let ptcr = core.control(0).map_err(SailBusExecutionError::Core)?;
        if ptcr & 1 != 0 {
            core.environment.page_walk_counter = core.environment.page_walk_counter.wrapping_add(1);
        }
        let access = match request.access {
            ACCESS_STORE | ACCESS_READ_MODIFY_WRITE | ACCESS_STACK_WRITE => {
                TranslationAccess::Write
            }
            ACCESS_EXECUTE => TranslationAccess::Execute,
            _ => TranslationAccess::Read,
        };
        let supervisor = match request.role {
            ROLE_EVENT_ENTRY_TARGET | ROLE_EVENT_FRAME_RANGE | ROLE_EVENT_FRAME_STORE => true,
            _ => core.is_supervisor().map_err(SailBusExecutionError::Core)?,
        };
        match translation::translate(
            bus,
            request.linear_address,
            ptcr,
            access,
            request.domain == 1,
            supervisor,
        ) {
            Ok(translated) => {
                response.access_class = translated.access_class;
                response.physical_class = translated.physical_class;
                response.cache_policy = translated.cache_policy;
                response.value = translated.address;
            }
            Err(TranslationError::Fault(fault)) => {
                response.success = false;
                response.fault_kind = fault.kind;
                response.fault_cause = fault.cause;
                response.detail = fault.detail;
                return Ok(response);
            }
            Err(TranslationError::Bus(error)) => return Err(error.into()),
        }
    } else {
        match translation::translate(
            bus,
            request.linear_address,
            0,
            TranslationAccess::Read,
            false,
            true,
        ) {
            Ok(translated) => {
                response.access_class = translated.access_class;
                response.physical_class = translated.physical_class;
            }
            Err(TranslationError::Fault(fault)) => {
                response.success = false;
                response.fault_kind = fault.kind;
                response.fault_cause = fault.cause;
                response.detail = fault.detail;
                return Ok(response);
            }
            Err(TranslationError::Bus(error)) => return Err(error.into()),
        }
    }
    let address = if request.address_translation {
        response.value
    } else {
        request.linear_address
    };

    let operation = match request.kind {
        REQUEST_TRANSLATION_EXECUTE_PROBE | REQUEST_MEMORY_PROBE => Ok(()),
        REQUEST_ADDRESS_TRANSLATE => {
            response.value = address;
            Ok(())
        }
        REQUEST_MEMORY_READ | REQUEST_PHYSICAL_PTE_READ => {
            read_width(bus, address, request.width).map(|value| response.value = value)
        }
        REQUEST_MEMORY_STORE | REQUEST_NON_TEMPORAL_STORE => {
            write_width(bus, address, request.width, request.value)
        }
        REQUEST_COMPOUND_MEMORY_STORE => write_compound(bus, address, request),
        REQUEST_ATOMIC_RMW => service_atomic(bus, address, request, &mut response),
        REQUEST_CACHE_MAINTENANCE
        | REQUEST_PREFETCH_HINT
        | REQUEST_FENCE_COMPLETION
        | REQUEST_TLB_INVALIDATE
        | REQUEST_TRANSLATION_QUERY
        | REQUEST_CONTEXT_SWITCH => Ok(()),
        REQUEST_STATE_SAVE => write_payload(bus, address, &request.payload),
        REQUEST_STATE_RESTORE => service_blob_access(bus, address, request, &mut response),
        REQUEST_REPEAT_BODY_FETCH => match fetch_instruction(bus, address) {
            Ok(body) => {
                response.body = body;
                Ok(())
            }
            Err(SailBusExecutionError::Bus(error)) => Err(error),
            Err(error) => Err(BusError::Device {
                addr: address,
                message: error.to_string(),
            }),
        },
        REQUEST_EVENT_FRAME_ACCESS => service_blob_access(bus, address, request, &mut response),
        REQUEST_VECTOR_MEMORY_WRITE if request.selector == 1 && request.access == ACCESS_STORE => {
            let result = write_payload(bus, address, &request.payload);
            if result.is_ok() {
                response.atomic_store_happened = true;
            }
            result
        }
        REQUEST_VECTOR_MEMORY_READ | REQUEST_VECTOR_MEMORY_WRITE => {
            service_blob_access(bus, address, request, &mut response)
        }
        _ => unreachable!(),
    };
    if let Err(error) = operation {
        response.success = false;
        response.fault_kind = translation::FAULT_ACCESS;
        response.fault_cause = 0;
        response.detail = error.to_string();
    }
    Ok(response)
}

fn service_blob_access(
    bus: &mut impl Bus,
    address: u64,
    request: &SailCoreRequest,
    response: &mut SailCoreResponse,
) -> Result<(), BusError> {
    match request.access {
        ACCESS_LOAD | ACCESS_READ_MODIFY_WRITE | ACCESS_STACK_READ => {
            response.body = read_payload(bus, address, request.body_length)?;
            Ok(())
        }
        ACCESS_STORE | ACCESS_STACK_WRITE => write_payload(bus, address, &request.payload),
        ACCESS_ADDRESS_ONLY => Ok(()),
        _ => Err(BusError::InvalidRange {
            start: address,
            end: address,
        }),
    }
}

fn read_payload(bus: &mut impl Bus, address: u64, length: i64) -> Result<Vec<u8>, BusError> {
    let length = usize::try_from(length).map_err(|_| BusError::InvalidRange {
        start: address,
        end: address,
    })?;
    let mut bytes = Vec::with_capacity(length);
    for offset in 0..length {
        let current = address
            .checked_add(offset as u64)
            .ok_or(BusError::OutOfRange { addr: address })?;
        bytes.push(bus.read_u8(current)?);
    }
    Ok(bytes)
}

fn write_payload(bus: &mut impl Bus, address: u64, bytes: &[u8]) -> Result<(), BusError> {
    for (offset, byte) in bytes.iter().copied().enumerate() {
        let current = address
            .checked_add(offset as u64)
            .ok_or(BusError::OutOfRange { addr: address })?;
        bus.write_u8(current, byte)?;
    }
    Ok(())
}

fn stack_range_in_bounds(request: &SailCoreRequest) -> bool {
    if request.range_length < 0 {
        return false;
    }
    let image = request.segment_image;
    let mantissa = (image >> 1) & 0x3f;
    if mantissa == 0 {
        return u128::from(request.range_start) + request.range_length as u128
            <= u128::from(u64::MAX) + 1;
    }
    let exponent = (image >> 7) & 0x1f;
    let base = u128::from((image >> 12) << 12);
    let span = (u128::from(mantissa) << exponent) * 4096;
    let start = u128::from(request.range_start);
    let end = start + request.range_length as u128;
    if image & 1 != 0 {
        base <= start && end <= base + span
    } else {
        end <= span
    }
}

fn read_width(bus: &mut impl Bus, address: u64, width: i64) -> Result<u64, BusError> {
    match width {
        1 => bus.read_u8(address).map(u64::from),
        2 => bus.read_u16(address).map(u64::from),
        4 => bus.read_u32(address).map(u64::from),
        8 => bus.read_u64(address),
        _ => Err(BusError::InvalidRange {
            start: address,
            end: address,
        }),
    }
}

fn write_width(bus: &mut impl Bus, address: u64, width: i64, value: u64) -> Result<(), BusError> {
    match width {
        1 => bus.write_u8(address, value as u8),
        2 => bus.write_u16(address, value as u16),
        4 => bus.write_u32(address, value as u32),
        8 => bus.write_u64(address, value),
        _ => Err(BusError::InvalidRange {
            start: address,
            end: address,
        }),
    }
}

fn write_compound(
    bus: &mut impl Bus,
    address: u64,
    request: &SailCoreRequest,
) -> Result<(), BusError> {
    if request.width != 16 {
        return Err(BusError::InvalidRange {
            start: address,
            end: address,
        });
    }
    bus.write_u64(address, request.value)?;
    let high = address
        .checked_add(8)
        .ok_or(BusError::OutOfRange { addr: address })?;
    bus.write_u64(high, request.desired)
}

fn service_atomic(
    bus: &mut impl Bus,
    address: u64,
    request: &SailCoreRequest,
    response: &mut SailCoreResponse,
) -> Result<(), BusError> {
    if request.width != 8 {
        return Err(BusError::InvalidRange {
            start: address,
            end: address,
        });
    }
    if request.selector == 0 {
        match bus.compare_exchange_u64(address, request.expected, request.desired)? {
            Ok(observed) => {
                response.value = observed;
                response.atomic_store_happened = true;
            }
            Err(observed) => response.value = observed,
        }
        return Ok(());
    }
    let observed = bus.read_u64(address)?;
    let desired = match request.selector {
        1 => observed.wrapping_add(request.value),
        2 => observed & request.value,
        3 => observed | request.value,
        4 => observed.wrapping_sub(request.value),
        5 => observed ^ request.value,
        _ => {
            return Err(BusError::Device {
                addr: address,
                message: format!("unknown atomic selector {}", request.selector),
            });
        }
    };
    bus.write_u64(address, desired)?;
    response.value = observed;
    response.atomic_store_happened = true;
    Ok(())
}

#[cfg(test)]
mod tests {
    use crate::{SailCore, SailCoreStatus};
    use bedrock_bus::{Bus, Ram};

    #[test]
    fn push_round_trips_through_ram_bus() {
        let mut core = SailCore::new().unwrap();
        let mut ram = Ram::new(0x10_0000);
        assert_eq!(core.set_sp(0x10_0000), SailCoreStatus::Ok);
        assert_eq!(
            core.set_register(0, 0x1122_3344_5566_7788),
            SailCoreStatus::Ok
        );

        core.execute_on_bus(&mut ram, &[0x30]).unwrap();

        assert_eq!(core.pc(), Ok(1));
        assert_eq!(core.sp(), Ok(0x0f_fff8));
        assert_eq!(ram.read_u64(0x0f_fff8).unwrap(), 0x1122_3344_5566_7788);
    }

    #[test]
    fn push_uses_host_page_walk_when_paging_is_enabled() {
        const TABLE: u64 = 0x1f;
        const LEAF_RW: u64 = 0x0d;
        let mut core = SailCore::new().unwrap();
        let mut ram = Ram::new(0x10_000);
        ram.write_u64(0x1000, 0x2000 | TABLE).unwrap();
        ram.write_u64(0x2000, 0x3000 | TABLE).unwrap();
        ram.write_u64(0x3000, 0x4000 | TABLE).unwrap();
        ram.write_u64(0x4040, 0x9000 | LEAF_RW).unwrap();
        let mut state = core.state().unwrap();
        state.controls.base_ptcr = 0x1001;
        state.status |= 1 << 4;
        state.supervisor = 1;
        state.sp = 0x8008;
        state.registers[0] = 0x1122_3344_5566_7788;
        assert_eq!(core.set_state(state), SailCoreStatus::Ok);

        core.execute_on_bus(&mut ram, &[0x30]).unwrap();

        assert_eq!(core.sp(), Ok(0x8000));
        assert_eq!(ram.read_u64(0x9000).unwrap(), 0x1122_3344_5566_7788);
        assert_eq!(core.environment_state().page_walk_counter, 1);
    }

    #[test]
    fn paging_fault_cause_round_trips_through_sail() {
        let mut core = SailCore::new().unwrap();
        let mut ram = Ram::new(0x10_000);
        let mut state = core.state().unwrap();
        state.controls.base_ptcr = 0x1001;
        state.status |= 1 << 4;
        state.supervisor = 1;
        state.sp = 0x0001_0000_0000_0008;
        state.registers[0] = 1;
        assert_eq!(core.set_state(state), SailCoreStatus::Ok);

        let error = core.execute_on_bus(&mut ram, &[0x30]).unwrap_err();

        let super::SailBusExecutionError::Fault { fault, .. } = error else {
            panic!("expected architectural paging fault");
        };
        assert_eq!(fault.kind, crate::translation::FAULT_TRANSLATION);
        assert_eq!(fault.error_code & 0xff, 3);
    }

    #[test]
    fn failed_bus_execution_rolls_back_and_leaves_core_reusable() {
        let mut core = SailCore::new().unwrap();
        let mut ram = Ram::new(16);
        assert_eq!(core.set_sp(4), SailCoreStatus::Ok);
        assert!(matches!(
            core.execute_on_bus(&mut ram, &[0x30]),
            Err(super::SailBusExecutionError::Fault { .. })
        ));
        assert_eq!(core.pc(), Ok(0));
        assert_eq!(core.sp(), Ok(4));

        core.execute_on_bus(&mut ram, &[0x01]).unwrap();
        assert_eq!(core.pc(), Ok(1));
    }

    #[test]
    fn step_fetches_framed_instruction_from_ram() {
        let mut core = SailCore::new().unwrap();
        let mut ram = Ram::new(16);
        ram.load(0, &[0x01, 0x01]).unwrap();

        core.step_on_bus(&mut ram).unwrap();
        core.step_on_bus(&mut ram).unwrap();

        assert_eq!(core.pc(), Ok(2));
    }

    #[test]
    fn cpuid_request_round_trips_through_the_host_platform() {
        let mut core = SailCore::new().unwrap();
        let mut ram = Ram::new(16);
        assert_eq!(core.set_register(0, 0), SailCoreStatus::Ok);

        core.execute_on_bus(&mut ram, &[0xc3, 0xb4, 0x00]).unwrap();

        assert_eq!(core.register(0), Ok(0x0000_0002_0000_0012));
        assert_eq!(core.pc(), Ok(3));
    }

    #[test]
    fn scalar_fp_executes_through_the_linked_numeric_primitive() {
        let mut core = SailCore::new().unwrap();
        let mut ram = Ram::new(16);
        let mut state = core.state().unwrap();
        state.fp_enabled = 1;
        state.floating_registers[0] = u64::from(1.0_f32.to_bits());
        state.floating_registers[1] = u64::from(2.0_f32.to_bits());
        assert_eq!(core.set_state(state), SailCoreStatus::Ok);

        // medium.fadd_x_fn_s_fn_d, S, F1 -> F0
        core.execute_on_bus(&mut ram, &[0xc2, 0x82, 0x10]).unwrap();

        assert_eq!(core.pc(), Ok(3));
        assert_eq!(
            core.state().unwrap().floating_registers[0],
            u64::from(3.0_f32.to_bits())
        );
        assert_eq!(core.state().unwrap().fflags, 0);
    }

    #[test]
    fn vector_fp_executes_lane_wise_inside_the_sail_model() {
        let mut core = SailCore::new().unwrap();
        let mut ram = Ram::new(16);
        let mut state = core.state().unwrap();
        state.fp_enabled = 1;
        state.predicate_registers[0] = [0xff, 0xff];
        for lane in 0..4 {
            state.vector_registers[0][lane * 4..lane * 4 + 4]
                .copy_from_slice(&1.0_f32.to_bits().to_le_bytes());
            state.vector_registers[1][lane * 4..lane * 4 + 4]
                .copy_from_slice(&2.0_f32.to_bits().to_le_bytes());
        }
        assert_eq!(core.set_state(state), SailCoreStatus::Ok);

        // VFADD.S P0, V1, V0
        core.execute_on_bus(&mut ram, &[0xcb, 0xf7, 0x83, 0x00, 0x20])
            .unwrap();

        let state = core.state().unwrap();
        for lane in 0..4 {
            assert_eq!(
                &state.vector_registers[0][lane * 4..lane * 4 + 4],
                &3.0_f32.to_bits().to_le_bytes()
            );
        }
        assert_eq!(state.fflags, 0);
    }

    #[test]
    fn vector_half_arithmetic_classification_and_compare_round_trip() {
        let mut core = SailCore::new().unwrap();
        let mut ram = Ram::new(16);
        let mut state = core.state().unwrap();
        state.fp_enabled = 1;
        state.predicate_registers[0] = [0xff, 0xff];
        for lane in 0..8 {
            state.vector_registers[0][lane * 2..lane * 2 + 2]
                .copy_from_slice(&0x3c00_u16.to_le_bytes());
            state.vector_registers[1][lane * 2..lane * 2 + 2]
                .copy_from_slice(&0x4000_u16.to_le_bytes());
        }
        assert_eq!(core.set_state(state), SailCoreStatus::Ok);

        // VFADD.H P0, V1, V0
        core.execute_on_bus(&mut ram, &[0xcb, 0xf7, 0x82, 0x80, 0x20])
            .unwrap();
        let state = core.state().unwrap();
        for lane in 0..8 {
            assert_eq!(
                &state.vector_registers[0][lane * 2..lane * 2 + 2],
                &0x4200_u16.to_le_bytes()
            );
        }

        // VFCLASS.H P0, V0: positive normal -> class bit 6.
        core.execute_on_bus(&mut ram, &[0xc7, 0xe8, 0x84, 0x00])
            .unwrap();
        let state = core.state().unwrap();
        for lane in 0..8 {
            assert_eq!(
                &state.vector_registers[0][lane * 2..lane * 2 + 2],
                &0x0040_u16.to_le_bytes()
            );
        }

        let mut state = state;
        state.vector_registers[0] = state.vector_registers[1];
        assert_eq!(core.set_state(state), SailCoreStatus::Ok);
        // VFCMPEQ.H P0, V1, V0, P1
        core.execute_on_bus(&mut ram, &[0xcb, 0xf5, 0x48, 0x04, 0x20])
            .unwrap();
        assert_eq!(core.state().unwrap().predicate_registers[1], [0x55, 0x55]);
    }

    #[test]
    fn vector_conversions_use_container_layout() {
        let mut core = SailCore::new().unwrap();
        let mut ram = Ram::new(16);
        let mut state = core.state().unwrap();
        state.fp_enabled = 1;
        state.predicate_registers[0] = [0x11, 0x11];
        for base in (0..16).step_by(4) {
            state.vector_registers[1][base..base + 2].copy_from_slice(&0x3c00_u16.to_le_bytes());
        }
        assert_eq!(core.set_state(state), SailCoreStatus::Ok);

        // VFCVTS.H P0, V1, V0
        core.execute_on_bus(&mut ram, &[0xcb, 0xf7, 0xa2, 0x80, 0x20])
            .unwrap();
        let state = core.state().unwrap();
        for base in (0..16).step_by(4) {
            assert_eq!(
                &state.vector_registers[0][base..base + 4],
                &1.0_f32.to_bits().to_le_bytes()
            );
        }
    }

    #[test]
    fn vector_fp_reduction_executes_inside_the_sail_model() {
        let mut core = SailCore::new().unwrap();
        let mut ram = Ram::new(16);
        let mut state = core.state().unwrap();
        state.fp_enabled = 1;
        state.predicate_registers[0] = [0x55, 0x55];
        for lane in 0..8 {
            state.vector_registers[1][lane * 2..lane * 2 + 2]
                .copy_from_slice(&0x3c00_u16.to_le_bytes());
        }
        assert_eq!(core.set_state(state), SailCoreStatus::Ok);
        // VFREDADD.H P0, V1, F0
        core.execute_on_bus(&mut ram, &[0xcb, 0xf7, 0xec, 0x80, 0x01])
            .unwrap();
        assert_eq!(core.state().unwrap().floating_registers[0], 0x4800);
    }

    #[test]
    fn fptransa_request_round_trips_with_accuracy_evidence() {
        let mut core = SailCore::new().unwrap();
        let mut ram = Ram::new(16);
        let mut state = core.state().unwrap();
        state.fp_enabled = 1;
        state.fptrans_enabled = 1;
        state.floating_registers[1] = 0;
        assert_eq!(core.set_state(state), SailCoreStatus::Ok);

        // FSINA.S F1, F0
        core.execute_on_bus(&mut ram, &[0xc7, 0xe7, 0x29, 0x10])
            .unwrap();
        assert_eq!(core.state().unwrap().floating_registers[0], 0);
    }

    #[test]
    fn performance_counter_request_observes_retired_steps() {
        let mut core = SailCore::new().unwrap();
        let mut ram = Ram::new(16);
        let mut state = core.state().unwrap();
        state.controls.base_pmc = 1;
        assert_eq!(core.set_state(state), SailCoreStatus::Ok);
        ram.load(0, &[0x01, 0xcb, 0xb4, 0x51, 0x01, 0x00]).unwrap();

        core.step_on_bus(&mut ram).unwrap();
        core.step_on_bus(&mut ram).unwrap();

        assert_eq!(core.register(1), Ok(2));
        assert_eq!(core.environment.retired_instruction_counter, 2);
    }

    #[test]
    fn resumable_scatter_stores_one_lane_per_step_and_retires_once() {
        const VSCATTER_B_SCALAR_STRIDE: [u8; 6] = [0xcf, 0xfc, 0x18, 0x02, 0x02, 0x43];

        let mut core = SailCore::new().unwrap();
        let mut ram = Ram::new(0x200);
        ram.load(0, &VSCATTER_B_SCALAR_STRIDE).unwrap();
        ram.load(0x100, &[0xa0, 0xa1, 0xa2, 0xa3, 0xa4]).unwrap();
        let mut state = core.state().unwrap();
        state.controls.base_pmc = 1;
        state.registers[1] = 0x100;
        state.registers[2] = 1;
        state.predicate_registers[0] = [0x05, 0x00];
        state.predicate_registers[1] = [0xf2, 0xff];
        state.vector_registers[3][0] = 0x11;
        state.vector_registers[3][2] = 0x33;
        assert_eq!(core.set_state(state), SailCoreStatus::Ok);

        core.step_on_bus(&mut ram).unwrap();

        assert_eq!(
            &ram.as_slice()[0x100..0x105],
            &[0x11, 0xa1, 0xa2, 0xa3, 0xa4]
        );
        assert_eq!(core.pc(), Ok(0));
        assert_eq!(core.state().unwrap().predicate_registers[1], [0x01, 0x00]);
        assert_eq!(core.environment.retired_instruction_counter, 0);

        core.step_on_bus(&mut ram).unwrap();

        assert_eq!(
            &ram.as_slice()[0x100..0x105],
            &[0x11, 0xa1, 0x33, 0xa3, 0xa4]
        );
        assert_eq!(core.pc(), Ok(VSCATTER_B_SCALAR_STRIDE.len() as u64));
        assert_eq!(core.state().unwrap().predicate_registers[1], [0x05, 0x00]);
        assert_eq!(core.environment.retired_instruction_counter, 1);
    }
}
