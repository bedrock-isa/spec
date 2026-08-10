use bedrock_bus::{Bus, BusError};
use thiserror::Error;

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
    pub const fn five_level(self) -> bool {
        self.0 & (1 << 7) != 0
    }
    pub const fn physical_address_bits(self) -> Option<u8> {
        match (self.0 >> 8) & 0xf {
            0 => Some(48),
            1 => Some(56),
            _ => None,
        }
    }
    pub const fn reserved_bits_clear(self) -> bool {
        self.0 & 0x7e == 0
    }
    pub const fn root_table_addr(self) -> u64 {
        self.0 & !0xfff
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
    AddressType,
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
            Self::AddressType => 6,
        }
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Error)]
pub enum TranslationFault {
    #[error("non-canonical address 0x{address:016x}")]
    NonCanonical { address: u64 },
    #[error("page fault at 0x{address:016x}: {reason:?}")]
    Page {
        address: u64,
        reason: PageFaultReason,
    },
}

#[derive(Debug, Clone, PartialEq, Eq, Error)]
pub enum PageWalkError {
    #[error(transparent)]
    Translation(#[from] TranslationFault),
    #[error("bus fault while accessing level-{level} PTE: {error}")]
    Bus { error: BusError, level: u8 },
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum TranslatedTarget {
    Byte(u64),
    Slot(u64),
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct PageWalkResult {
    pub target: TranslatedTarget,
    pub leaf_entry: u64,
    pub entries: [u64; 5],
    pub levels: u8,
    pub user: bool,
    pub writable: bool,
    pub executable: bool,
}

impl PageWalkResult {
    pub fn entry_at_level(self, level: u8) -> Option<u64> {
        (level != 0 && level <= self.levels).then(|| self.entries[usize::from(level - 1)])
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct PageQueryResult {
    pub value: u64,
    pub valid: bool,
    pub user: bool,
    pub writable: bool,
    pub executable: bool,
}

impl PageQueryResult {
    const fn success(value: u64, user: bool, writable: bool, executable: bool) -> Self {
        Self {
            value,
            valid: true,
            user,
            writable,
            executable,
        }
    }

    const fn failure_with_value(value: u64) -> Self {
        Self {
            value,
            valid: false,
            user: false,
            writable: false,
            executable: false,
        }
    }

    const fn failure() -> Self {
        Self::failure_with_value(0)
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Default)]
pub struct MemoryTranslation {
    pub segments: SegmentRegisters,
    pub ptcr: PageTableControl,
    pub ascr: AddressSpaceControl,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
struct PageWalkOptions {
    update_accessed_dirty: bool,
    enforce_permissions: bool,
}

impl MemoryTranslation {
    pub fn segment_linear_address(
        &self,
        segment: SegmentSelector,
        offset: u64,
    ) -> Result<u64, TranslationFault> {
        let descriptor = self.segments.get(segment);
        if !descriptor.enabled() {
            return Ok(offset);
        }

        let base = u128::from(descriptor.base());
        let span = (u128::from(descriptor.mantissa()) << descriptor.exponent()) * 4096;
        let candidate = u128::from(offset);
        let valid = if descriptor.bounds_only() {
            base <= candidate && candidate < base + span
        } else {
            candidate < span
        };
        if !valid {
            return Err(TranslationFault::Page {
                address: offset,
                reason: PageFaultReason::SegmentBounds,
            });
        }
        if descriptor.bounds_only() {
            Ok(offset)
        } else {
            Ok(base.wrapping_add(candidate) as u64)
        }
    }

    pub fn segment_address(
        &self,
        segment: SegmentSelector,
        offset: u64,
    ) -> Result<u64, TranslationFault> {
        let linear = self.segment_linear_address(segment, offset)?;
        self.validate_linear_address(linear)?;
        Ok(linear)
    }

    pub fn validate_linear_address(&self, linear: u64) -> Result<(), TranslationFault> {
        if !self.ptcr.paging_enabled() {
            return Ok(());
        }
        let address_bits = if self.ptcr.paging_enabled() && self.ptcr.five_level() {
            57
        } else {
            48
        };
        if is_canonical(linear, address_bits) {
            Ok(())
        } else {
            Err(TranslationFault::NonCanonical { address: linear })
        }
    }

    pub fn page_address<B: Bus>(
        &self,
        bus: &mut B,
        linear: u64,
        domain: AccessDomain,
        kind: AccessKind,
        supervisor: bool,
        update_accessed_dirty: bool,
    ) -> Result<PageWalkResult, PageWalkError> {
        self.walk_page_address(
            bus,
            linear,
            domain,
            kind,
            supervisor,
            PageWalkOptions {
                update_accessed_dirty,
                enforce_permissions: true,
            },
        )
    }

    fn walk_page_address<B: Bus>(
        &self,
        bus: &mut B,
        linear: u64,
        domain: AccessDomain,
        kind: AccessKind,
        supervisor: bool,
        options: PageWalkOptions,
    ) -> Result<PageWalkResult, PageWalkError> {
        if !self.ptcr.paging_enabled() {
            return Ok(PageWalkResult {
                target: TranslatedTarget::Byte(linear),
                leaf_entry: 0,
                entries: [0; 5],
                levels: 0,
                user: true,
                writable: true,
                executable: true,
            });
        }

        let pabits = self
            .ptcr
            .physical_address_bits()
            .ok_or_else(|| page_fault(linear, PageFaultReason::PagingFormatUnavailable))?;
        let physical_mask = (1u64 << pabits) - 1;
        let root = self.ptcr.root_table_addr();
        if !self.ptcr.reserved_bits_clear() || root & !physical_mask != 0 {
            return Err(page_fault(linear, PageFaultReason::PagingFormatUnavailable).into());
        }

        let shifts: &[u8] = if self.ptcr.five_level() {
            &[48, 39, 30, 21, 12]
        } else {
            &[39, 30, 21, 12]
        };
        let pfn_mask = physical_mask & !0xfff;
        let mut table = root;
        let mut effective_w = true;
        let mut effective_x = true;
        let mut effective_u = true;
        let mut traversed = Vec::with_capacity(shifts.len());
        let mut entries = [0u64; 5];

        for (index, shift) in shifts.iter().copied().enumerate() {
            let architectural_level = (shifts.len() - index) as u8;
            let entry_address = table
                .checked_add(((linear >> shift) & 0x1ff) * 8)
                .filter(|address| address & !physical_mask == 0)
                .ok_or_else(|| page_fault(linear, PageFaultReason::InvalidEntry))?;
            let entry = bus
                .read_u64(entry_address)
                .map_err(|error| PageWalkError::Bus {
                    error,
                    level: architectural_level,
                })?;
            if entry & PTE_PRESENT == 0 {
                return Err(page_fault(linear, PageFaultReason::NotPresent).into());
            }

            let leaf = index + 1 == shifts.len();
            let structurally_valid = if leaf {
                valid_leaf_entry(entry)
            } else {
                valid_table_entry(entry)
            };
            if !structurally_valid {
                return Err(page_fault(linear, PageFaultReason::InvalidEntry).into());
            }

            effective_w &= entry & PTE_WRITABLE != 0;
            effective_x &= entry & PTE_EXECUTABLE != 0;
            effective_u &= entry & PTE_USER != 0;
            traversed.push((entry_address, entry));
            entries[usize::from(architectural_level - 1)] = entry;

            if options.enforce_permissions {
                let requires_user_mapping = domain == AccessDomain::User || !supervisor;
                if (requires_user_mapping && !effective_u)
                    || (!requires_user_mapping && leaf && effective_u)
                {
                    return Err(page_fault(linear, PageFaultReason::Privilege).into());
                }
                // Slot targets cannot fetch instructions. At a structurally
                // valid slot leaf, address type precedes execute permission.
                if leaf && kind == AccessKind::InstructionFetch && entry & PTE_ADDRESSING_TYPE != 0
                {
                    return Err(page_fault(linear, PageFaultReason::AddressType).into());
                }
                if kind == AccessKind::Write && !effective_w {
                    return Err(page_fault(linear, PageFaultReason::ReadOnly).into());
                }
                if kind == AccessKind::InstructionFetch && !effective_x {
                    return Err(page_fault(linear, PageFaultReason::Execute).into());
                }
            }

            if !leaf {
                table = entry & pfn_mask;
            }
        }

        let leaf_entry = traversed.last().expect("page walk has a leaf").1;
        let target = if leaf_entry & PTE_ADDRESSING_TYPE == 0 {
            TranslatedTarget::Byte((leaf_entry & pfn_mask) | (linear & 0xfff))
        } else {
            TranslatedTarget::Slot((leaf_entry & pfn_mask) | (linear & 0xfff))
        };

        if options.update_accessed_dirty && matches!(target, TranslatedTarget::Byte(_)) {
            let last = traversed.len() - 1;
            for (index, (address, entry)) in traversed.iter().copied().enumerate() {
                let mut updated = entry | PTE_ACCESSED;
                if index == last && kind == AccessKind::Write {
                    updated |= PTE_DIRTY;
                }
                if updated != entry {
                    let level = (shifts.len() - index) as u8;
                    bus.write_u64(address, updated)
                        .map_err(|error| PageWalkError::Bus { error, level })?;
                }
            }
        }

        Ok(PageWalkResult {
            target,
            leaf_entry,
            entries,
            levels: shifts.len() as u8,
            user: effective_u,
            writable: effective_w,
            executable: effective_x,
        })
    }

    pub fn translation_query_starts_walk(&self, linear: u64) -> bool {
        self.ptcr.paging_enabled() && self.validate_linear_address(linear).is_ok()
    }

    pub fn query_translation<B: Bus>(
        &self,
        bus: &mut B,
        linear: u64,
    ) -> Result<PageQueryResult, PageWalkError> {
        if !self.ptcr.paging_enabled() {
            return Ok(PageQueryResult::success(linear, true, true, true));
        }
        if self.validate_linear_address(linear).is_err() {
            return Ok(PageQueryResult::failure());
        }

        match self.walk_page_address(
            bus,
            linear,
            AccessDomain::Current,
            AccessKind::Read,
            true,
            PageWalkOptions {
                update_accessed_dirty: false,
                enforce_permissions: false,
            },
        ) {
            Ok(walk) => {
                let value = match walk.target {
                    TranslatedTarget::Byte(address) | TranslatedTarget::Slot(address) => address,
                };
                Ok(PageQueryResult::success(
                    value,
                    walk.user,
                    walk.writable,
                    walk.executable,
                ))
            }
            Err(PageWalkError::Translation(_)) => Ok(PageQueryResult::failure()),
            Err(error @ PageWalkError::Bus { .. }) => Err(error),
        }
    }

    pub fn page_query_starts_walk(&self, linear: u64, requested_level: u8) -> bool {
        let levels = if self.ptcr.five_level() { 5 } else { 4 };
        (1..=levels).contains(&requested_level)
            && is_canonical(linear, if levels == 5 { 57 } else { 48 })
    }

    pub fn query_page_entry<B: Bus>(
        &self,
        bus: &mut B,
        linear: u64,
        requested_level: u8,
    ) -> Result<PageQueryResult, PageWalkError> {
        if !(1..=5).contains(&requested_level) {
            return Ok(PageQueryResult::failure());
        }
        let address_bits = if self.ptcr.five_level() { 57 } else { 48 };
        if !is_canonical(linear, address_bits) {
            return Ok(PageQueryResult::failure());
        }

        let Some(pabits) = self.ptcr.physical_address_bits() else {
            return Ok(PageQueryResult::failure());
        };
        let physical_mask = (1u64 << pabits) - 1;
        let root = self.ptcr.root_table_addr();
        if !self.ptcr.reserved_bits_clear() || root & !physical_mask != 0 {
            return Ok(PageQueryResult::failure());
        }

        let shifts: &[u8] = if self.ptcr.five_level() {
            &[48, 39, 30, 21, 12]
        } else {
            &[39, 30, 21, 12]
        };
        if usize::from(requested_level) > shifts.len() {
            return Ok(PageQueryResult::failure());
        }

        let pfn_mask = physical_mask & !0xfff;
        let mut table = root;
        let mut effective_w = true;
        let mut effective_x = true;
        let mut effective_u = true;
        for (index, shift) in shifts.iter().copied().enumerate() {
            let Some(entry_address) = table
                .checked_add(((linear >> shift) & 0x1ff) * 8)
                .filter(|address| address & !physical_mask == 0)
            else {
                return Ok(PageQueryResult::failure());
            };
            let level = (shifts.len() - index) as u8;
            let entry = bus
                .read_u64(entry_address)
                .map_err(|error| PageWalkError::Bus { error, level })?;
            effective_w &= entry & PTE_WRITABLE != 0;
            effective_x &= entry & PTE_EXECUTABLE != 0;
            effective_u &= entry & PTE_USER != 0;
            if level == requested_level {
                let valid = if level == 1 {
                    valid_leaf_entry(entry)
                } else {
                    valid_table_entry(entry)
                };
                return Ok(if valid {
                    PageQueryResult::success(entry, effective_u, effective_w, effective_x)
                } else {
                    PageQueryResult::failure_with_value(entry)
                });
            }
            if !valid_table_entry(entry) {
                return Ok(PageQueryResult::failure());
            }
            table = entry & pfn_mask;
        }
        unreachable!("requested page-table level was validated")
    }
}

const PTE_PRESENT: u64 = 1 << 0;
const PTE_WRITABLE: u64 = 1 << 1;
const PTE_EXECUTABLE: u64 = 1 << 2;
const PTE_USER: u64 = 1 << 3;
const PTE_GLOBAL: u64 = 1 << 4;
const PTE_ACCESSED: u64 = 1 << 5;
const PTE_DIRTY: u64 = 1 << 6;
const PTE_ADDRESSING_TYPE: u64 = 1 << 7;
const PTE_CP_MASK: u64 = 0b11 << 8;
const PTE_CP_SLOT: u64 = 0b01 << 8;
const PTE_TABLE: u64 = 1 << 11;

const fn valid_table_entry(entry: u64) -> bool {
    entry & (PTE_PRESENT | PTE_TABLE) == (PTE_PRESENT | PTE_TABLE)
        && entry & (PTE_DIRTY | PTE_GLOBAL | PTE_ADDRESSING_TYPE) == 0
}

const fn valid_leaf_entry(entry: u64) -> bool {
    if entry & PTE_PRESENT == 0 || entry & PTE_TABLE != 0 {
        return false;
    }
    if entry & PTE_ADDRESSING_TYPE == 0 {
        return true;
    }
    entry & PTE_CP_MASK == PTE_CP_SLOT
        && entry & PTE_EXECUTABLE == 0
        && entry & (PTE_ACCESSED | PTE_DIRTY) == (PTE_ACCESSED | PTE_DIRTY)
}

fn page_fault(address: u64, reason: PageFaultReason) -> TranslationFault {
    TranslationFault::Page { address, reason }
}

fn is_canonical(address: u64, bits: u8) -> bool {
    let shift = 64 - bits;
    (((address << shift) as i64) >> shift) as u64 == address
}

#[cfg(test)]
mod tests {
    use super::*;
    use bedrock_bus::{Bus, BusResult, Ram};

    const TABLE_PERMISSIONS: u64 = PTE_PRESENT | PTE_WRITABLE | PTE_EXECUTABLE | PTE_USER;
    const FIVE_LEVEL_ENTRY_ADDRESSES: [u64; 5] = [0x1000, 0x2000, 0x3000, 0x4000, 0x5000];

    struct ReadTrackingBus {
        ram: Ram,
        pte_reads: Vec<u64>,
    }

    impl Bus for ReadTrackingBus {
        fn begin_transaction(&mut self) -> BusResult<()> {
            Bus::begin_transaction(&mut self.ram)
        }

        fn commit_transaction(&mut self) {
            Bus::commit_transaction(&mut self.ram);
        }

        fn rollback_transaction(&mut self) {
            Bus::rollback_transaction(&mut self.ram);
        }

        fn read_u8(&mut self, addr: u64) -> BusResult<u8> {
            Bus::read_u8(&mut self.ram, addr)
        }

        fn write_u8(&mut self, addr: u64, value: u8) -> BusResult<()> {
            Bus::write_u8(&mut self.ram, addr, value)
        }

        fn read_u64(&mut self, addr: u64) -> BusResult<u64> {
            self.pte_reads.push(addr);
            Bus::read_u64(&mut self.ram, addr)
        }

        fn write_u64(&mut self, addr: u64, value: u64) -> BusResult<()> {
            Bus::write_u64(&mut self.ram, addr, value)
        }
    }

    fn four_level_mapping(ram: &mut Ram, leaf_permissions: u64) -> MemoryTranslation {
        ram.write_u64(0x1000, 0x2000 | TABLE_PERMISSIONS | PTE_TABLE)
            .unwrap();
        ram.write_u64(0x2000, 0x3000 | TABLE_PERMISSIONS | PTE_TABLE)
            .unwrap();
        ram.write_u64(0x3000, 0x4000 | TABLE_PERMISSIONS | PTE_TABLE)
            .unwrap();
        ram.write_u64(0x4000, 0x8000 | PTE_PRESENT | leaf_permissions)
            .unwrap();
        MemoryTranslation {
            ptcr: PageTableControl::from_raw(0x1000 | 1),
            ..MemoryTranslation::default()
        }
    }

    fn four_level_slot_mapping(ram: &mut Ram, leaf_bits: u64) -> MemoryTranslation {
        four_level_mapping(
            ram,
            PTE_WRITABLE
                | PTE_USER
                | PTE_ADDRESSING_TYPE
                | PTE_CP_SLOT
                | PTE_ACCESSED
                | PTE_DIRTY
                | leaf_bits,
        )
    }

    fn tracked_five_level_mapping(
        level: u8,
        update_entry: impl FnOnce(u64) -> u64,
        lower_not_present: bool,
    ) -> (MemoryTranslation, ReadTrackingBus) {
        assert!((1..=5).contains(&level));
        let mut ram = Ram::new(0x10_000);
        for (address, next_table) in FIVE_LEVEL_ENTRY_ADDRESSES
            .iter()
            .copied()
            .zip([0x2000, 0x3000, 0x4000, 0x5000])
        {
            ram.write_u64(address, next_table | TABLE_PERMISSIONS | PTE_TABLE)
                .unwrap();
        }
        ram.write_u64(FIVE_LEVEL_ENTRY_ADDRESSES[4], 0x8000 | TABLE_PERMISSIONS)
            .unwrap();

        let index = usize::from(5 - level);
        let address = FIVE_LEVEL_ENTRY_ADDRESSES[index];
        let entry = ram.read_u64(address).unwrap();
        ram.write_u64(address, update_entry(entry)).unwrap();
        if lower_not_present && level > 1 {
            ram.write_u64(FIVE_LEVEL_ENTRY_ADDRESSES[index + 1], 0)
                .unwrap();
        }

        (
            MemoryTranslation {
                ptcr: PageTableControl::from_raw(0x1000 | (1 << 7) | 1),
                ..MemoryTranslation::default()
            },
            ReadTrackingBus {
                ram,
                pte_reads: Vec::new(),
            },
        )
    }

    fn assert_level_fault(
        level: u8,
        update_entry: impl FnOnce(u64) -> u64,
        lower_not_present: bool,
        domain: AccessDomain,
        kind: AccessKind,
        supervisor: bool,
        reason: PageFaultReason,
    ) {
        let (translation, mut bus) =
            tracked_five_level_mapping(level, update_entry, lower_not_present);
        assert_eq!(
            translation
                .page_address(&mut bus, 0, domain, kind, supervisor, false)
                .unwrap_err(),
            PageWalkError::Translation(TranslationFault::Page { address: 0, reason }),
            "architectural level {level}"
        );
        let consumed = usize::from(6 - level);
        assert_eq!(
            bus.pte_reads,
            FIVE_LEVEL_ENTRY_ADDRESSES[..consumed],
            "architectural level {level} read a lower PTE"
        );
    }

    #[test]
    fn not_present_precedes_structure_and_permissions_at_every_level() {
        for level in 1..=5 {
            assert_level_fault(
                level,
                |entry| {
                    (entry | PTE_DIRTY | PTE_TABLE)
                        & !(PTE_PRESENT | PTE_USER | PTE_WRITABLE | PTE_EXECUTABLE)
                },
                true,
                AccessDomain::User,
                AccessKind::Write,
                true,
                PageFaultReason::NotPresent,
            );
        }
    }

    #[test]
    fn structural_validity_precedes_permissions_at_every_level() {
        for level in 1..=5 {
            assert_level_fault(
                level,
                |entry| {
                    let structurally_invalid = if level == 1 {
                        entry | PTE_TABLE
                    } else {
                        entry | PTE_DIRTY
                    };
                    structurally_invalid & !(PTE_USER | PTE_WRITABLE | PTE_EXECUTABLE)
                },
                true,
                AccessDomain::User,
                AccessKind::Write,
                true,
                PageFaultReason::InvalidEntry,
            );
        }
    }

    #[test]
    fn user_privilege_denial_stops_before_the_next_level() {
        for level in 1..=5 {
            assert_level_fault(
                level,
                |entry| entry & !PTE_USER,
                true,
                AccessDomain::User,
                AccessKind::Read,
                true,
                PageFaultReason::Privilege,
            );
        }
    }

    #[test]
    fn write_denial_stops_before_the_next_level() {
        for level in 1..=5 {
            assert_level_fault(
                level,
                |entry| entry & !PTE_WRITABLE,
                true,
                AccessDomain::User,
                AccessKind::Write,
                true,
                PageFaultReason::ReadOnly,
            );
        }
    }

    #[test]
    fn execute_denial_stops_before_the_next_level() {
        for level in 1..=5 {
            assert_level_fault(
                level,
                |entry| entry & !PTE_EXECUTABLE,
                true,
                AccessDomain::User,
                AccessKind::InstructionFetch,
                true,
                PageFaultReason::Execute,
            );
        }
    }

    #[test]
    fn paging_disabled_returns_a_byte_target() {
        let translation = MemoryTranslation::default();
        let mut ram = Ram::new(1);

        for linear in [0x1234_5678, u64::MAX] {
            assert_eq!(
                translation
                    .page_address(
                        &mut ram,
                        linear,
                        AccessDomain::Current,
                        AccessKind::Read,
                        true,
                        true,
                    )
                    .unwrap()
                    .target,
                TranslatedTarget::Byte(linear)
            );
            assert_eq!(
                translation.segment_address(SegmentSelector::Ds, linear),
                Ok(linear)
            );
        }
    }

    #[test]
    fn slot_leaf_preserves_each_page_offset() {
        let mut ram = Ram::new(0x10_000);
        let translation = four_level_slot_mapping(&mut ram, 0);

        for offset in [0, 1, 0xfff] {
            assert_eq!(
                translation
                    .page_address(
                        &mut ram,
                        offset,
                        AccessDomain::User,
                        AccessKind::Read,
                        true,
                        true,
                    )
                    .unwrap()
                    .target,
                TranslatedTarget::Slot(0x8000 | offset)
            );
        }
    }

    #[test]
    fn malformed_slot_leaf_bits_are_invalid_individually() {
        for (name, clear, set) in [
            ("CP", PTE_CP_MASK, 0),
            ("X", 0, PTE_EXECUTABLE),
            ("A", PTE_ACCESSED, 0),
            ("D", PTE_DIRTY, 0),
        ] {
            let mut ram = Ram::new(0x10_000);
            let translation = four_level_slot_mapping(&mut ram, 0);
            let leaf = ram.read_u64(0x4000).unwrap();
            ram.write_u64(0x4000, (leaf & !clear) | set).unwrap();
            assert!(
                matches!(
                    translation.page_address(
                        &mut ram,
                        0,
                        AccessDomain::Current,
                        AccessKind::Read,
                        true,
                        true,
                    ),
                    Err(PageWalkError::Translation(TranslationFault::Page {
                        reason: PageFaultReason::InvalidEntry,
                        ..
                    }))
                ),
                "malformed slot leaf with {name} bit"
            );
        }
    }

    #[test]
    fn slot_leaf_requires_cp_one_encoding() {
        for cp in [0, 2, 3] {
            let mut ram = Ram::new(0x10_000);
            let translation = four_level_slot_mapping(&mut ram, 0);
            let leaf = ram.read_u64(0x4000).unwrap();
            ram.write_u64(0x4000, (leaf & !PTE_CP_MASK) | (cp << 8))
                .unwrap();

            assert!(matches!(
                translation.page_address(
                    &mut ram,
                    0,
                    AccessDomain::User,
                    AccessKind::Read,
                    true,
                    true,
                ),
                Err(PageWalkError::Translation(TranslationFault::Page {
                    reason: PageFaultReason::InvalidEntry,
                    ..
                }))
            ));
        }
    }

    #[test]
    fn slot_leaf_allows_global_bit() {
        let mut ram = Ram::new(0x10_000);
        let translation = four_level_slot_mapping(&mut ram, PTE_GLOBAL);

        assert_eq!(
            translation
                .page_address(
                    &mut ram,
                    0,
                    AccessDomain::User,
                    AccessKind::Read,
                    true,
                    true,
                )
                .unwrap()
                .target,
            TranslatedTarget::Slot(0x8000)
        );
    }

    #[test]
    fn non_leaf_ignores_cp_but_rejects_global_dirty_and_address_type() {
        let mut ram = Ram::new(0x10_000);
        let translation = four_level_mapping(&mut ram, PTE_WRITABLE | PTE_USER);
        let entry = ram.read_u64(0x2000).unwrap();
        ram.write_u64(0x2000, entry | PTE_CP_MASK).unwrap();
        assert_eq!(
            translation
                .page_address(
                    &mut ram,
                    0,
                    AccessDomain::User,
                    AccessKind::Read,
                    true,
                    false,
                )
                .unwrap()
                .target,
            TranslatedTarget::Byte(0x8000)
        );

        for bit in [PTE_GLOBAL, PTE_DIRTY, PTE_ADDRESSING_TYPE] {
            ram.write_u64(0x2000, entry | bit).unwrap();
            assert!(matches!(
                translation.page_address(
                    &mut ram,
                    0,
                    AccessDomain::Current,
                    AccessKind::Read,
                    true,
                    false,
                ),
                Err(PageWalkError::Translation(TranslationFault::Page {
                    reason: PageFaultReason::InvalidEntry,
                    ..
                }))
            ));
        }
    }

    #[test]
    fn slot_leaf_never_updates_accessed_or_dirty_bits() {
        let mut ram = Ram::new(0x10_000);
        let translation = four_level_slot_mapping(&mut ram, 0);
        let before = [0x1000, 0x2000, 0x3000, 0x4000].map(|address| ram.read_u64(address).unwrap());

        translation
            .page_address(
                &mut ram,
                0,
                AccessDomain::User,
                AccessKind::Write,
                true,
                true,
            )
            .unwrap();

        for (address, entry) in [0x1000, 0x2000, 0x3000, 0x4000].into_iter().zip(before) {
            assert_eq!(ram.read_u64(address).unwrap(), entry);
        }
    }

    #[test]
    fn slot_fetch_reports_address_type_before_execute_permission() {
        let mut ram = Ram::new(0x10_000);
        let translation = four_level_slot_mapping(&mut ram, 0);

        assert!(matches!(
            translation.page_address(
                &mut ram,
                0,
                AccessDomain::User,
                AccessKind::InstructionFetch,
                true,
                true,
            ),
            Err(PageWalkError::Translation(TranslationFault::Page {
                reason: PageFaultReason::AddressType,
                ..
            }))
        ));
    }

    #[test]
    fn slot_fetch_reports_privilege_before_address_type_for_user_access() {
        let mut ram = Ram::new(0x10_000);
        let translation = four_level_slot_mapping(&mut ram, 0);
        let leaf = ram.read_u64(0x4000).unwrap();
        ram.write_u64(0x4000, leaf & !PTE_USER).unwrap();

        assert!(matches!(
            translation.page_address(
                &mut ram,
                0,
                AccessDomain::Current,
                AccessKind::InstructionFetch,
                false,
                true,
            ),
            Err(PageWalkError::Translation(TranslationFault::Page {
                reason: PageFaultReason::Privilege,
                ..
            }))
        ));

        ram.write_u64(0x4000, leaf).unwrap();
        assert!(matches!(
            translation.page_address(
                &mut ram,
                0,
                AccessDomain::Current,
                AccessKind::InstructionFetch,
                false,
                true,
            ),
            Err(PageWalkError::Translation(TranslationFault::Page {
                reason: PageFaultReason::AddressType,
                ..
            }))
        ));
    }

    #[test]
    fn segment_window_translates_and_checks_bounds() {
        // base_page=2, e=0, m=1, translated-window mode.
        let mut translation = MemoryTranslation::default();
        translation.segments.set(
            SegmentSelector::Ds,
            SegmentRegister::from_raw((2 << 12) | (1 << 1)),
        );
        assert_eq!(
            translation.segment_address(SegmentSelector::Ds, 0x20),
            Ok(0x2020)
        );
        assert!(matches!(
            translation.segment_address(SegmentSelector::Ds, 0x1000),
            Err(TranslationFault::Page {
                reason: PageFaultReason::SegmentBounds,
                ..
            })
        ));
    }

    #[test]
    fn la57_accepts_addresses_outside_la48() {
        let translation = MemoryTranslation {
            ptcr: PageTableControl::from_raw((1 << 7) | 1),
            ..MemoryTranslation::default()
        };
        assert_eq!(
            translation.segment_address(SegmentSelector::Cs, 1 << 48),
            Ok(1 << 48)
        );
    }

    #[test]
    fn four_level_walk_translates_and_updates_accessed_dirty_bits() {
        let mut ram = Ram::new(0x10_000);
        let translation = four_level_mapping(&mut ram, PTE_WRITABLE | PTE_EXECUTABLE | PTE_USER);

        let read = translation
            .page_address(
                &mut ram,
                0x123,
                AccessDomain::User,
                AccessKind::Read,
                true,
                true,
            )
            .unwrap();
        assert_eq!(read.target, TranslatedTarget::Byte(0x8123));
        assert_eq!(read.entry_at_level(1).unwrap() & !0xfff, 0x8000);
        for address in [0x1000, 0x2000, 0x3000, 0x4000] {
            assert_ne!(ram.read_u64(address).unwrap() & PTE_ACCESSED, 0);
        }
        assert_eq!(ram.read_u64(0x4000).unwrap() & PTE_DIRTY, 0);

        translation
            .page_address(
                &mut ram,
                0x123,
                AccessDomain::User,
                AccessKind::Write,
                true,
                true,
            )
            .unwrap();
        assert_ne!(ram.read_u64(0x4000).unwrap() & PTE_DIRTY, 0);
    }

    #[test]
    fn access_domain_and_current_mode_require_the_matching_mapping_privilege() {
        let mut ram = Ram::new(0x10_000);
        let supervisor_mapping = four_level_mapping(&mut ram, PTE_WRITABLE | PTE_EXECUTABLE);

        assert_eq!(
            supervisor_mapping
                .page_address(
                    &mut ram,
                    0,
                    AccessDomain::Current,
                    AccessKind::Read,
                    true,
                    false,
                )
                .unwrap()
                .target,
            TranslatedTarget::Byte(0x8000)
        );
        let supervisor_query = supervisor_mapping.query_translation(&mut ram, 0).unwrap();
        assert!(supervisor_query.valid && !supervisor_query.user);
        for (domain, supervisor) in [(AccessDomain::User, true), (AccessDomain::Current, false)] {
            assert!(matches!(
                supervisor_mapping.page_address(
                    &mut ram,
                    0,
                    domain,
                    AccessKind::Read,
                    supervisor,
                    false,
                ),
                Err(PageWalkError::Translation(TranslationFault::Page {
                    reason: PageFaultReason::Privilege,
                    ..
                }))
            ));
        }

        let user_mapping = four_level_mapping(&mut ram, PTE_WRITABLE | PTE_EXECUTABLE | PTE_USER);
        assert!(matches!(
            user_mapping.page_address(
                &mut ram,
                0,
                AccessDomain::Current,
                AccessKind::Read,
                true,
                false,
            ),
            Err(PageWalkError::Translation(TranslationFault::Page {
                reason: PageFaultReason::Privilege,
                ..
            }))
        ));
        let user_query = user_mapping.query_translation(&mut ram, 0).unwrap();
        assert!(user_query.valid && user_query.user);
        for (domain, supervisor) in [(AccessDomain::User, true), (AccessDomain::Current, false)] {
            assert_eq!(
                user_mapping
                    .page_address(&mut ram, 0, domain, AccessKind::Read, supervisor, false,)
                    .unwrap()
                    .target,
                TranslatedTarget::Byte(0x8000)
            );
        }
    }

    #[test]
    fn execute_and_write_permissions_are_accumulated_across_non_leaf_entries() {
        let mut ram = Ram::new(0x10_000);
        let translation = four_level_mapping(&mut ram, PTE_WRITABLE | PTE_EXECUTABLE | PTE_USER);
        let l3 = ram.read_u64(0x2000).unwrap();
        ram.write_u64(0x2000, l3 & !(PTE_WRITABLE | PTE_EXECUTABLE))
            .unwrap();

        assert!(matches!(
            translation.page_address(
                &mut ram,
                0,
                AccessDomain::Current,
                AccessKind::Write,
                true,
                false,
            ),
            Err(PageWalkError::Translation(TranslationFault::Page {
                reason: PageFaultReason::ReadOnly,
                ..
            }))
        ));
        assert!(matches!(
            translation.page_address(
                &mut ram,
                0,
                AccessDomain::Current,
                AccessKind::InstructionFetch,
                true,
                false,
            ),
            Err(PageWalkError::Translation(TranslationFault::Page {
                reason: PageFaultReason::Execute,
                ..
            }))
        ));
    }

    #[test]
    fn page_query_stops_at_the_requested_level() {
        let mut ram = Ram::new(0x10_000);
        ram.write_u64(0x1000, 0x2000 | TABLE_PERMISSIONS | PTE_TABLE)
            .unwrap();
        ram.write_u64(0x2000, 0x3000 | TABLE_PERMISSIONS | PTE_TABLE)
            .unwrap();
        ram.write_u64(0x3000, 0x4000 | TABLE_PERMISSIONS | PTE_TABLE)
            .unwrap();
        let translation = MemoryTranslation {
            // PTQUERY ignores PE.
            ptcr: PageTableControl::from_raw(0x1000),
            ..MemoryTranslation::default()
        };

        let level_two = translation.query_page_entry(&mut ram, 0, 2).unwrap();
        assert!(level_two.valid);
        assert_eq!(level_two.value & !0xfff, 0x4000);

        let level_one = translation.query_page_entry(&mut ram, 0, 1).unwrap();
        assert!(!level_one.valid);
        assert_eq!(level_one.value, 0);
    }

    #[test]
    fn translation_query_with_paging_disabled_is_unrestricted_identity() {
        let translation = MemoryTranslation::default();
        let mut ram = Ram::new(0);
        let result = translation.query_translation(&mut ram, u64::MAX).unwrap();

        assert_eq!(result.value, u64::MAX);
        assert!(
            result.valid && result.user && result.writable && result.executable,
            "paging-disabled identity translation has no PTE permission restriction"
        );
    }

    #[test]
    fn translation_query_reports_permissions_without_accessed_or_dirty_updates() {
        let mut ram = Ram::new(0x10_000);
        let translation = four_level_mapping(&mut ram, PTE_WRITABLE | PTE_USER);
        let before = [0x1000, 0x2000, 0x3000, 0x4000].map(|address| ram.read_u64(address).unwrap());

        let result = translation.query_translation(&mut ram, 0x123).unwrap();
        assert_eq!(result.value, 0x8123);
        assert!(result.valid && result.user && result.writable);
        assert!(!result.executable);
        for (address, entry) in [0x1000, 0x2000, 0x3000, 0x4000].into_iter().zip(before) {
            assert_eq!(ram.read_u64(address).unwrap(), entry);
        }
    }

    #[test]
    fn translation_and_page_queries_report_valid_slot_leaf_without_slot_access() {
        let mut ram = Ram::new(0x10_000);
        let translation = four_level_slot_mapping(&mut ram, PTE_GLOBAL);
        let leaf = ram.read_u64(0x4000).unwrap();

        let translated = translation.query_translation(&mut ram, 0x123).unwrap();
        assert_eq!(translated.value, 0x8123);
        assert!(translated.valid && translated.user && translated.writable);
        assert!(!translated.executable);

        let queried = translation.query_page_entry(&mut ram, 0x123, 1).unwrap();
        assert_eq!(queried.value, leaf);
        assert!(queried.valid && queried.user && queried.writable);
        assert!(!queried.executable);
    }

    #[test]
    fn page_query_returns_each_malformed_slot_leaf_raw_with_cleared_permissions() {
        let malformed_fields = [
            (PTE_CP_MASK, 0),
            (PTE_CP_MASK, 0b10 << 8),
            (PTE_CP_MASK, 0b11 << 8),
            (0, PTE_EXECUTABLE),
            (PTE_ACCESSED, 0),
            (PTE_DIRTY, 0),
        ];
        for (clear, set) in malformed_fields {
            let mut ram = Ram::new(0x10_000);
            let translation = four_level_slot_mapping(&mut ram, 0);
            let leaf = (ram.read_u64(0x4000).unwrap() & !clear) | set;
            ram.write_u64(0x4000, leaf).unwrap();

            assert_eq!(
                translation.query_page_entry(&mut ram, 0, 1).unwrap(),
                PageQueryResult::failure_with_value(leaf)
            );
        }
    }

    #[test]
    fn query_page_walk_bus_errors_are_not_soft_failures() {
        let translation = MemoryTranslation {
            ptcr: PageTableControl::from_raw(0x1001),
            ..MemoryTranslation::default()
        };
        let mut ram = Ram::new(1);
        let expected = BusError::OutOfRange { addr: 0x1000 };

        assert_eq!(
            translation.query_translation(&mut ram, 0).unwrap_err(),
            PageWalkError::Bus {
                error: expected.clone(),
                level: 4,
            }
        );
        assert_eq!(
            translation.query_page_entry(&mut ram, 0, 1).unwrap_err(),
            PageWalkError::Bus {
                error: expected,
                level: 4,
            }
        );
    }

    #[test]
    fn translation_query_turns_canonical_and_walk_failures_into_zero() {
        let mut ram = Ram::new(0x10_000);
        let translation = four_level_mapping(&mut ram, PTE_WRITABLE | PTE_USER);
        let malformed = ram.read_u64(0x2000).unwrap() | PTE_GLOBAL;
        ram.write_u64(0x2000, malformed).unwrap();

        for linear in [0, 1 << 48] {
            assert_eq!(
                translation.query_translation(&mut ram, linear).unwrap(),
                PageQueryResult::failure()
            );
        }
    }

    #[test]
    fn page_query_returns_a_malformed_requested_entry_but_not_a_later_entry() {
        let mut ram = Ram::new(0x10_000);
        ram.write_u64(0x1000, 0x2000 | TABLE_PERMISSIONS | PTE_TABLE)
            .unwrap();
        ram.write_u64(0x2000, 0x3000 | TABLE_PERMISSIONS | PTE_TABLE)
            .unwrap();
        let malformed = 0x4000 | TABLE_PERMISSIONS | PTE_TABLE | PTE_DIRTY;
        ram.write_u64(0x3000, malformed).unwrap();
        let translation = MemoryTranslation {
            ptcr: PageTableControl::from_raw(0x1000),
            ..MemoryTranslation::default()
        };

        let requested = translation.query_page_entry(&mut ram, 0, 2).unwrap();
        assert_eq!(requested.value, malformed);
        assert!(!requested.valid);
        assert!(!requested.user && !requested.writable && !requested.executable);

        assert_eq!(
            translation.query_page_entry(&mut ram, 0, 1).unwrap(),
            PageQueryResult::failure()
        );
    }

    #[test]
    fn page_query_uses_la57_even_when_paging_is_disabled() {
        let mut ram = Ram::new(0x10_000);
        let root_entry = 0x2000 | TABLE_PERMISSIONS | PTE_TABLE;
        ram.write_u64(0x1008, root_entry).unwrap();
        let translation = MemoryTranslation {
            ptcr: PageTableControl::from_raw(0x1000 | (1 << 7)),
            ..MemoryTranslation::default()
        };

        let result = translation.query_page_entry(&mut ram, 1 << 48, 5).unwrap();
        assert_eq!(result.value, root_entry);
        assert!(result.valid && result.user && result.writable && result.executable);

        let la48 = MemoryTranslation {
            ptcr: PageTableControl::from_raw(0x1000),
            ..MemoryTranslation::default()
        };
        assert_eq!(
            la48.query_page_entry(&mut ram, 0, 5).unwrap(),
            PageQueryResult::failure()
        );
    }

    #[test]
    fn segment_image_validation_accepts_disabled_and_rejects_wrapping_limit() {
        assert!(SegmentRegister::disabled().valid());
        let overflowing = SegmentRegister::from_raw(!0xfffu64 | (31 << 7) | (63 << 1));
        assert!(!overflowing.valid());
    }
}
