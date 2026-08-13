pub mod decode;
pub mod ea;
pub mod generated {
    include!(concat!(env!("OUT_DIR"), "/generated.rs"));
}
pub mod header;
pub mod instruction;
pub mod operand;
pub mod table;

pub use decode::{DecodeError, DecodedField, DecodedInstruction, decode};
pub use ea::{AutoUpdate, CompactEa, DisplacementWidth, ExtendedDescriptor};
pub use generated::{FormId, ISA_INPUT_SHA256, Opcode};
pub use header::{HeaderError, InstructionHeader, MAX_INSTRUCTION_BYTES, decode_header};
pub use instruction::InstructionAttributes;
pub use operand::{DecodedOperand, Size};
pub use table::{
    ConstraintPredicate, DestinationOverlapRule, EncodingClass, FieldKind, FlagsEffect,
    InstructionSet, RepeatObservation, RepeatObservedOperand, RepeatOperandLocation,
};
