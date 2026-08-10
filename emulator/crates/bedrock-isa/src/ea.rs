#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum DisplacementWidth {
    Bits8,
    Bits16,
    Bits32,
    Bits64,
}

impl DisplacementWidth {
    pub const fn bytes(self) -> usize {
        match self {
            Self::Bits8 => 1,
            Self::Bits16 => 2,
            Self::Bits32 => 4,
            Self::Bits64 => 8,
        }
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum CompactEa {
    Register(u8),
    RegisterIndirect(u8),
    RegisterDisplacement {
        register: u8,
        width: DisplacementWidth,
    },
    StackDisplacement(DisplacementWidth),
    ProgramCounterDisplacement(DisplacementWidth),
    StackPointer,
    StackIndirect,
    Absolute32,
    Absolute64,
    Immediate(DisplacementWidth),
    Ext0 {
        displacement: Option<DisplacementWidth>,
    },
    Reserved(u8),
}

impl CompactEa {
    pub const fn decode(value: u8) -> Self {
        let value = value & 0x7f;
        match value >> 4 {
            0b000 => Self::Register(value & 0x0f),
            0b001 => Self::RegisterIndirect(value & 0x0f),
            0b010 => Self::RegisterDisplacement {
                register: value & 0x0f,
                width: DisplacementWidth::Bits8,
            },
            0b011 => Self::RegisterDisplacement {
                register: value & 0x0f,
                width: DisplacementWidth::Bits16,
            },
            0b100 => Self::RegisterDisplacement {
                register: value & 0x0f,
                width: DisplacementWidth::Bits32,
            },
            0b101 => Self::RegisterDisplacement {
                register: value & 0x0f,
                width: DisplacementWidth::Bits64,
            },
            _ => match value {
                0x60 => Self::StackDisplacement(DisplacementWidth::Bits8),
                0x61 => Self::StackDisplacement(DisplacementWidth::Bits16),
                0x62 => Self::StackDisplacement(DisplacementWidth::Bits32),
                0x63 => Self::StackDisplacement(DisplacementWidth::Bits64),
                0x64 => Self::ProgramCounterDisplacement(DisplacementWidth::Bits8),
                0x65 => Self::ProgramCounterDisplacement(DisplacementWidth::Bits16),
                0x66 => Self::ProgramCounterDisplacement(DisplacementWidth::Bits32),
                0x67 => Self::ProgramCounterDisplacement(DisplacementWidth::Bits64),
                0x68 => Self::StackPointer,
                0x69 => Self::StackIndirect,
                0x6a => Self::Absolute32,
                0x6b => Self::Absolute64,
                0x6c => Self::Immediate(DisplacementWidth::Bits8),
                0x6d => Self::Immediate(DisplacementWidth::Bits16),
                0x6e => Self::Immediate(DisplacementWidth::Bits32),
                0x6f => Self::Immediate(DisplacementWidth::Bits64),
                0x70 => Self::Ext0 {
                    displacement: Some(DisplacementWidth::Bits8),
                },
                0x71 => Self::Ext0 {
                    displacement: Some(DisplacementWidth::Bits16),
                },
                0x72 => Self::Ext0 {
                    displacement: Some(DisplacementWidth::Bits32),
                },
                0x73 => Self::Ext0 {
                    displacement: Some(DisplacementWidth::Bits64),
                },
                0x74 => Self::Ext0 { displacement: None },
                other => Self::Reserved(other),
            },
        }
    }

    pub const fn appended_bytes(self) -> usize {
        match self {
            Self::RegisterDisplacement { width, .. }
            | Self::StackDisplacement(width)
            | Self::ProgramCounterDisplacement(width)
            | Self::Immediate(width) => width.bytes(),
            Self::Absolute32 => 4,
            Self::Absolute64 => 8,
            Self::Ext0 { displacement } => {
                1 + match displacement {
                    Some(width) => width.bytes(),
                    None => 0,
                }
            }
            _ => 0,
        }
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum AutoUpdate {
    None,
    PostIncrement,
    PreDecrement,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct Ext0Descriptor {
    pub raw: u16,
    pub segment: Option<u8>,
    pub base: Option<u8>,
    pub index: Option<u8>,
    pub base_update: AutoUpdate,
    pub index_update: AutoUpdate,
}

impl Ext0Descriptor {
    pub fn decode(bytes: &[u8]) -> Option<(Self, usize)> {
        let first = *bytes.first()?;
        if first & 0x80 == 0 {
            return Some((
                Self {
                    raw: u16::from(first),
                    segment: Some((first >> 4) & 0x07),
                    base: Some(first & 0x0f),
                    index: None,
                    base_update: AutoUpdate::None,
                    index_update: AutoUpdate::None,
                },
                1,
            ));
        }

        if first & 0x87 == 0x84 || first & 0x87 == 0x85 {
            return Some((
                Self {
                    raw: u16::from(first),
                    segment: None,
                    base: Some((first >> 3) & 0x0f),
                    index: None,
                    base_update: if first & 0x07 == 4 {
                        AutoUpdate::PostIncrement
                    } else {
                        AutoUpdate::PreDecrement
                    },
                    index_update: AutoUpdate::None,
                },
                1,
            ));
        }

        let segment = Some((first >> 4) & 0x07);
        let mode = first & 0x0f;
        if mode == 3 {
            return Some((
                Self {
                    raw: u16::from(first),
                    segment,
                    base: None,
                    index: None,
                    base_update: AutoUpdate::None,
                    index_update: AutoUpdate::None,
                },
                1,
            ));
        }

        let second = *bytes.get(1)?;
        let raw = (u16::from(first) << 8) | u16::from(second);
        let (segment, base, index, base_update, index_update) = if first == 0x8a || first == 0x8b {
            let index_mode = second >> 4;
            if index_mode > 2 {
                return None;
            }
            (
                None,
                None,
                Some(second & 0x0f),
                AutoUpdate::None,
                index_auto_update(index_mode),
            )
        } else {
            match mode {
                0..=2 => (
                    segment,
                    Some(second >> 4),
                    Some(second & 0x0f),
                    AutoUpdate::None,
                    index_auto_update(mode),
                ),
                8 if second & 0x0f <= 1 => (
                    segment,
                    Some(second >> 4),
                    None,
                    if second & 0x0f == 0 {
                        AutoUpdate::PostIncrement
                    } else {
                        AutoUpdate::PreDecrement
                    },
                    AutoUpdate::None,
                ),
                9 if second >> 4 <= 2 => (
                    segment,
                    None,
                    Some(second & 0x0f),
                    AutoUpdate::None,
                    index_auto_update(second >> 4),
                ),
                _ => return None,
            }
        };
        Some((
            Self {
                raw,
                segment,
                base,
                index,
                base_update,
                index_update,
            },
            2,
        ))
    }
}

const fn index_auto_update(mode: u8) -> AutoUpdate {
    match mode {
        0 => AutoUpdate::PostIncrement,
        1 => AutoUpdate::PreDecrement,
        _ => AutoUpdate::None,
    }
}

#[cfg(test)]
mod tests {
    use super::{AutoUpdate, Ext0Descriptor};

    #[test]
    fn decodes_one_and_two_byte_ext0_descriptors() {
        let (base, bytes) = Ext0Descriptor::decode(&[0x12]).unwrap();
        assert_eq!(bytes, 1);
        assert_eq!(base.segment, Some(1));
        assert_eq!(base.base, Some(2));

        let (indexed, bytes) = Ext0Descriptor::decode(&[0x92, 0x02]).unwrap();
        assert_eq!(bytes, 2);
        assert_eq!(indexed.segment, Some(1));
        assert_eq!(indexed.base, Some(0));
        assert_eq!(indexed.index, Some(2));
        assert_eq!(indexed.index_update, AutoUpdate::None);

        let (postincrement, bytes) = Ext0Descriptor::decode(&[0xac]).unwrap();
        assert_eq!(bytes, 1);
        assert_eq!(postincrement.segment, None);
        assert_eq!(postincrement.base, Some(5));
        assert_eq!(postincrement.base_update, AutoUpdate::PostIncrement);
    }
}
