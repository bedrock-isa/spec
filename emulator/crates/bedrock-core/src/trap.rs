use crate::exception::InvalidControlCause;
use crate::{AccessDomain, AccessKind, PageFaultReason, SegmentSelector};
use bedrock_bus::{AcknowledgedBusFailure, BusError, SlotTransactionError};
use bedrock_isa::DecodeError;
use thiserror::Error;

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct PageFaultContext {
    pub effective_address: u64,
    pub linear_address: Option<u64>,
    pub reason: PageFaultReason,
    pub access_kind: AccessKind,
    pub access_domain: AccessDomain,
    pub segment: Option<SegmentSelector>,
    pub asid: u16,
    pub access_size: Option<u8>,
    pub operand: Option<u8>,
    pub atomic: bool,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct BusFaultContext {
    pub failure: AcknowledgedBusFailure,
    pub effective_address: u64,
    pub linear_address: Option<u64>,
    pub access_kind: AccessKind,
    pub access_domain: AccessDomain,
    pub segment: Option<SegmentSelector>,
    pub asid: u16,
    pub access_size: Option<u8>,
    pub operand: Option<u8>,
    pub atomic: bool,
    pub walk_level: u8,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
#[repr(u8)]
pub enum IllegalInstructionCause {
    InvalidOpcode = 0,
    InvalidEffectiveAddress = 1,
    ReservedEncoding = 2,
    UnavailableExtension = 3,
    ExplicitIllegal = 4,
    InsufficientLength = 5,
    InvalidOperandRelation = 6,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
#[repr(u8)]
pub enum DivideErrorCause {
    ZeroDivisor = 0,
    SignedOverflow = 1,
}

#[derive(Debug, Clone, PartialEq, Eq, Error)]
pub enum Trap {
    #[error("decode fault at 0x{pc:016x}: {error}")]
    Decode { pc: u64, error: DecodeError },
    #[error("bus fault at 0x{pc:016x}: {error}")]
    Bus { pc: u64, error: BusError },
    #[error("slot transaction fault at 0x{pc:016x}: {error}")]
    SlotTransaction {
        pc: u64,
        error: SlotTransactionError,
    },
    #[error("acknowledged bus failure at 0x{pc:016x}: {context:?}")]
    AcknowledgedBusFailure { pc: u64, context: BusFaultContext },
    #[error("illegal instruction at 0x{pc:016x}: cause {cause:?}")]
    IllegalInstruction {
        pc: u64,
        cause: IllegalInstructionCause,
    },
    #[error("privileged instruction at 0x{pc:016x}")]
    PrivilegeFault { pc: u64 },
    #[error("divide error at 0x{pc:016x}: cause {cause:?}")]
    DivideError { pc: u64, cause: DivideErrorCause },
    #[error("invalid control state at 0x{pc:016x}: cause {cause:?}")]
    InvalidControlState { pc: u64, cause: InvalidControlCause },
    #[error("floating-point fault at 0x{pc:016x}: causes {causes:?}")]
    FloatingPointFault {
        pc: u64,
        causes: crate::fpu::env::FpCauses,
    },
    #[error("page fault at 0x{address:016x} while executing 0x{pc:016x}: {reason:?}", address = context.linear_address.unwrap_or(context.effective_address), reason = context.reason)]
    PageFault { pc: u64, context: PageFaultContext },
}
