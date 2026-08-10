use crate::CompactEa;

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum DecodedOperand {
    Register(u8),
    FloatingRegister(u8),
    EffectiveAddress(CompactEa),
    Immediate(u64),
    Condition(u8),
    SizeSelector(u8),
    Bits { kind: crate::FieldKind, value: u64 },
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Size {
    Byte,
    Word,
    Long,
    Quad,
}

impl Size {
    pub const fn bytes(self) -> usize {
        match self {
            Self::Byte => 1,
            Self::Word => 2,
            Self::Long => 4,
            Self::Quad => 8,
        }
    }
}
