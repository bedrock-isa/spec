pub mod board;
#[path = "architecture/exception.rs"]
pub mod exception;
#[path = "architecture/flags.rs"]
pub mod flags;
pub mod loader;
pub mod machine;
#[path = "architecture/state.rs"]
pub mod state;
#[path = "architecture/step.rs"]
pub mod step;
#[path = "architecture/translation.rs"]
pub mod translation;
#[path = "architecture/trap.rs"]
pub mod trap;

pub use board::Board;
pub use exception::{EventControl, ExceptionFrameType, InvalidControlCause};
pub use flags::{Flags, Status};
pub use loader::{ElfLoadError, ElfLoadOptions, ElfLoadResult, LoadedSegment, SegmentPermissions};
pub use machine::Machine;
pub use state::{
    CPU_REGISTER_INFOS, CpuRegister, CpuRegisterInfo, CpuRegisterSet, CpuState, PREDICATE_BYTES,
    PREDICATE_REGISTER_COUNT, PredicateRegister, VECTOR_REGISTER_COUNT, VLEN_BITS, VLEN_BYTES,
    VectorRegister,
};
pub use step::StepResult;
pub use translation::{
    AccessDomain, AccessFaultReason, AccessKind, AddressSpaceControl, PageFaultReason,
    PageTableControl, SegmentRegister, SegmentRegisters, SegmentSelector, TranslationTableFormat,
};
pub use trap::{
    AccessFaultContext, BusFaultContext, ControlFlowIntegrityCause, DivideErrorCause,
    IllegalInstructionCause, PageFaultContext, Trap, VectorRangeErrorCause,
};

#[derive(Debug, Clone, Copy, PartialEq, Eq, Default)]
pub struct FpCauses(u8);

impl FpCauses {
    pub const NX: Self = Self(1 << 0);
    pub const UF: Self = Self(1 << 1);
    pub const OF: Self = Self(1 << 2);
    pub const DZ: Self = Self(1 << 3);
    pub const NV: Self = Self(1 << 4);

    pub const fn bits(self) -> u8 {
        self.0
    }

    pub const fn from_bits_truncate(bits: u8) -> Self {
        Self(bits & 0x1f)
    }
}
