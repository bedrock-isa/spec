const BASE_CLASS: u32 = 0;
const EXTENSION_CLASS: u32 = 1;
const IMPLEMENTATION_CLASS: u32 = 2;

const VENDOR_ID: u16 = 0x4252;
const ARCHITECTURE_ID: u16 = 1;
const IMPLEMENTATION_ID: u32 = 0x454d_5531;
const ARCHITECTURE_REVISION: u16 = 1;
const IMPLEMENTATION_REVISION: u16 = 1;
const VENDOR_NAME: &[u8] = b"Bedrock";
const PROCESSOR_NAME: &[u8] = b"Bedrock Emulator";
pub(crate) const TIMEBASE_TICKS_PER_SECOND: u64 = 1_000_000_000;

const FPTRANSA_CONTRACT_IDS: &[u16] = &[
    0x0001, 0x0002, 0x0003, 0x0004, 0x0011, 0x0012, 0x0013, 0x0021, 0x0022, 0x0023, 0x0024, 0x0031,
    0x0032, 0x0033, 0x0034, 0x0041, 0x0042, 0x0043, 0x0044,
];

pub(crate) fn cpuid_query(selector: u64) -> u64 {
    let class = (selector >> 32) as u32;
    let leaf = (selector >> 16) as u16;
    let index = selector as u16;
    match (class, leaf, index) {
        (BASE_CLASS, 0, 0) => header_with_class(2, 2, 18),
        (BASE_CLASS, 0, 1) => {
            (u64::from(VENDOR_ID) << 48)
                | (u64::from(ARCHITECTURE_ID) << 32)
                | u64::from(IMPLEMENTATION_ID)
        }
        (BASE_CLASS, 0, 2) => {
            (u64::from(IMPLEMENTATION_REVISION) << 16) | u64::from(ARCHITECTURE_REVISION)
        }
        (BASE_CLASS, 0, 3..=10) => name_word(VENDOR_NAME, usize::from(index - 3)),
        (BASE_CLASS, 0, 11..=18) => name_word(PROCESSOR_NAME, usize::from(index - 11)),
        (BASE_CLASS, 2, 0) => 1,
        (BASE_CLASS, 2, 1) => 0x0101,
        (EXTENSION_CLASS, 0, 0) => header_with_leaf(3, 1),
        (EXTENSION_CLASS, 0, 1) => 0b1111,
        (EXTENSION_CLASS, 1, 0) => 1,
        (EXTENSION_CLASS, 1, 1) => 0x0101,
        (EXTENSION_CLASS, 2, 0) => 0x0044,
        (EXTENSION_CLASS, 2, id) if FPTRANSA_CONTRACT_IDS.contains(&id) => {
            (1_u64 << 63) | (1_u64 << 32) | (0x0100_u64 << 16) | 0x0100
        }
        (EXTENSION_CLASS, 3, 0) => 1,
        (EXTENSION_CLASS, 3, 1) => 0x0107,
        (IMPLEMENTATION_CLASS, 0, 0) => header_with_leaf(6, 0),
        (IMPLEMENTATION_CLASS, 1, 0) => 1,
        (IMPLEMENTATION_CLASS, 1, 1) => 64,
        (IMPLEMENTATION_CLASS, 2, 0) => 3,
        (IMPLEMENTATION_CLASS, 2, 1..=3) => 1,
        (IMPLEMENTATION_CLASS, 3, 0) => 1,
        (IMPLEMENTATION_CLASS, 3, 1) => 56,
        (IMPLEMENTATION_CLASS, 5, 0) => 1,
        (IMPLEMENTATION_CLASS, 5, 1) => TIMEBASE_TICKS_PER_SECOND,
        (IMPLEMENTATION_CLASS, 6, 0) => 1,
        (IMPLEMENTATION_CLASS, 6, 1) => 4,
        _ => 0,
    }
}

const fn header_with_class(max_class: u32, max_leaf: u16, max_index: u16) -> u64 {
    ((max_class as u64) << 32) | ((max_leaf as u64) << 16) | max_index as u64
}

const fn header_with_leaf(max_leaf: u16, max_index: u16) -> u64 {
    ((max_leaf as u64) << 16) | max_index as u64
}

fn name_word(name: &[u8], word_index: usize) -> u64 {
    let start = word_index * 8;
    let mut result = 0;
    for byte_index in 0..8 {
        if let Some(byte) = name.get(start + byte_index) {
            result |= u64::from(*byte) << (byte_index * 8);
        }
    }
    result
}

#[cfg(test)]
mod tests {
    use super::{TIMEBASE_TICKS_PER_SECOND, cpuid_query};

    const fn selector(class: u32, leaf: u16, index: u16) -> u64 {
        ((class as u64) << 32) | ((leaf as u64) << 16) | index as u64
    }

    #[test]
    fn cpuid_reports_stable_identity_and_sparse_contracts() {
        assert_eq!(cpuid_query(selector(0, 0, 0)), 0x0000_0002_0002_0012);
        assert_eq!(cpuid_query(selector(0, 2, 0)), 1);
        assert_eq!(cpuid_query(selector(0, 2, 1)), 0x0101);
        assert_eq!(cpuid_query(selector(1, 1, 1)), 0x0101);
        assert_eq!(cpuid_query(selector(1, 3, 1)), 0x0107);
        assert_eq!(cpuid_query(selector(2, 4, 0)), 0);
        assert_eq!(cpuid_query(selector(1, 2, 0)), 0x44);
        assert_ne!(cpuid_query(selector(1, 2, 0x44)), 0);
        assert_eq!(cpuid_query(selector(1, 2, 0x10)), 0);
        assert_eq!(cpuid_query(u64::MAX), 0);
    }

    #[test]
    fn cpuid_reports_the_invariant_timebase_rate() {
        assert_eq!(cpuid_query(selector(2, 0, 0)), 0x0006_0000);
        assert_eq!(cpuid_query(selector(2, 5, 1)), TIMEBASE_TICKS_PER_SECOND);
    }

    #[test]
    fn cpuid_reports_architectural_debug_trigger_capacity() {
        assert_eq!(cpuid_query(selector(2, 6, 0)), 1);
        assert_eq!(cpuid_query(selector(2, 6, 1)), 4);
    }
}
