pub const IMPLEMENTATION_PABITS: u8 = 56;
const PTCR_ROOT_MASK: u64 = ((1u64 << IMPLEMENTATION_PABITS) - 1) & !0x3fff;
const PTCR_TT_MASK: u64 = 0b111 << 1;
const PTCR_DEFINED_MASK: u64 = PTCR_ROOT_MASK | PTCR_TT_MASK | 1;

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum AccessDomain {
    Current,
    User,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum AccessKind {
    InstructionFetch,
    Read,
    Write,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
#[repr(u8)]
pub enum SegmentSelector {
    Cs = 0,
    Ds = 1,
    Ss = 2,
    Gs0 = 3,
    Gs1 = 4,
    Gs2 = 5,
    Gs3 = 6,
    Gs4 = 7,
    Gs5 = 8,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Default)]
pub struct SegmentRegister(u64);

impl SegmentRegister {
    pub const fn from_raw(raw: u64) -> Self {
        Self(raw)
    }
    pub const fn raw(self) -> u64 {
        self.0
    }
    pub const fn disabled() -> Self {
        Self(0)
    }
    pub const fn base(self) -> u64 {
        (self.0 >> 12) << 12
    }
    pub const fn exponent(self) -> u8 {
        ((self.0 >> 7) & 0x1f) as u8
    }
    pub const fn mantissa(self) -> u8 {
        ((self.0 >> 1) & 0x3f) as u8
    }
    pub const fn bounds_only(self) -> bool {
        self.0 & 1 != 0
    }
    pub const fn enabled(self) -> bool {
        self.mantissa() != 0
    }
    pub const fn valid(self) -> bool {
        if !self.enabled() {
            return true;
        }
        let limit = (self.base() as u128) + ((self.mantissa() as u128) << self.exponent()) * 4096;
        limit <= (u64::MAX as u128) + 1
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Default)]
pub struct SegmentRegisters {
    values: [SegmentRegister; 9],
}

impl SegmentRegisters {
    pub fn get(&self, selector: SegmentSelector) -> SegmentRegister {
        self.values[selector as usize]
    }
    pub fn set(&mut self, selector: SegmentSelector, value: SegmentRegister) {
        self.values[selector as usize] = value;
    }
    pub fn cs(&self) -> SegmentRegister {
        self.get(SegmentSelector::Cs)
    }
    pub fn ds(&self) -> SegmentRegister {
        self.get(SegmentSelector::Ds)
    }
    pub fn ss(&self) -> SegmentRegister {
        self.get(SegmentSelector::Ss)
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Default)]
pub struct PageTableControl(u64);

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum TranslationTableFormat {
    La45,
    La56,
}

impl PageTableControl {
    pub const fn from_raw(raw: u64) -> Self {
        Self(raw)
    }
    pub const fn raw(self) -> u64 {
        self.0
    }
    pub const fn disabled() -> Self {
        Self(0)
    }
    pub const fn paging_enabled(self) -> bool {
        self.0 & 1 != 0
    }
    pub const fn translation_table_format(self) -> Option<TranslationTableFormat> {
        match (self.0 & PTCR_TT_MASK) >> 1 {
            0b010 => Some(TranslationTableFormat::La45),
            0b011 => Some(TranslationTableFormat::La56),
            _ => None,
        }
    }
    pub const fn physical_address_bits(self) -> u8 {
        IMPLEMENTATION_PABITS
    }
    pub const fn reserved_bits_clear(self) -> bool {
        self.0 & !PTCR_DEFINED_MASK == 0
    }
    pub const fn valid(self) -> bool {
        self.reserved_bits_clear()
            && (!self.paging_enabled() || self.translation_table_format().is_some())
    }
    pub const fn root_table_addr(self) -> u64 {
        self.0 & PTCR_ROOT_MASK
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Default)]
pub struct AddressSpaceControl(u64);

impl AddressSpaceControl {
    pub const fn from_raw(raw: u64) -> Self {
        Self(raw)
    }
    pub const fn raw(self) -> u64 {
        self.0
    }
    pub const fn asid_enabled(self) -> bool {
        self.0 & 1 != 0
    }
    pub const fn asid(self) -> u16 {
        (self.0 >> 16) as u16
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum PageFaultReason {
    SegmentBounds,
    NonCanonical,
    NotPresent,
    ReadOnly,
    Privilege,
    Execute,
    InvalidEntry,
    PagingFormatUnavailable,
    AtomicAlignment,
    MemoryType,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum AccessFaultReason {
    PhysicalAddress,
    MmioAlignment,
    MmioOperation,
}

impl AccessFaultReason {
    pub const fn code(self) -> u8 {
        match self {
            Self::PhysicalAddress => 0,
            Self::MmioAlignment => 1,
            Self::MmioOperation => 2,
        }
    }
}

impl PageFaultReason {
    pub const fn code(self) -> u8 {
        match self {
            Self::NotPresent => 0,
            Self::ReadOnly | Self::Privilege | Self::Execute => 1,
            Self::InvalidEntry | Self::PagingFormatUnavailable => 2,
            Self::NonCanonical => 3,
            Self::SegmentBounds => 4,
            Self::AtomicAlignment => 5,
            Self::MemoryType => 6,
        }
    }
}
