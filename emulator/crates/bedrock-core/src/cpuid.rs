//! Pure architectural discovery results for this emulator implementation.

use crate::fpu::trans::contracts::{MAX_CONTRACT_ID, contract_by_id};

const BASE_CLASS: u32 = 0;
const EXTENSION_CLASS: u32 = 1;
const IMPLEMENTATION_CLASS: u32 = 2;

const BASE_IDENTITY_LEAF: u16 = 0;
const EXTENSION_DIRECTORY_LEAF: u16 = 0;
const FPTRANSA_ACCURACY_LEAF: u16 = 1;
const IMPLEMENTATION_DIRECTORY_LEAF: u16 = 0;
const CACHE_TOPOLOGY_LEAF: u16 = 1;
const PERFORMANCE_COUNTERS_LEAF: u16 = 2;
const SAVE_AREA_LAYOUT_LEAF: u16 = 4;

// These values are the emulator's stable implementation-defined CPUID identity.
// The numeric IDs deliberately spell "BR" and "EMU1" where their field widths
// permit it. Changing any value or name is a CPUID compatibility revision.
const VENDOR_ID: u16 = 0x4252;
const ARCHITECTURE_ID: u16 = 1;
const IMPLEMENTATION_ID: u32 = 0x454d_5531;
const ARCHITECTURE_REVISION: u16 = 1;
const IMPLEMENTATION_REVISION: u16 = 1;
const VENDOR_NAME: &[u8] = b"Bedrock";
const PROCESSOR_NAME: &[u8] = b"Bedrock Emulator";

// This cacheless implementation selects one 64-byte maintenance block and
// reports no cache descriptors. The value is stable within its coherence domain.
pub const MAINTENANCE_GRANULE_BYTES: u16 = 64;

pub const SAVE_AREA_SIZE_BYTES: u64 = 0x0180;
pub const SAVE_FIXED_SIZE_BYTES: u16 = 0x00c0;
pub const SAVE_BITMAP_WORDS: u16 = 1;
pub const SAVE_FORMAT: u8 = 0;
pub const SAVE_FP_COMPONENT_ID: u16 = 1;
pub const SAVE_FP_BITMAP_BIT: u8 = 0;
pub const SAVE_FP_OFFSET_BYTES: u32 = 0x00c0;
pub const SAVE_FP_MAX_SIZE_BYTES: u32 = 0x00c0;
pub const SAVE_FP_ALIGNMENT_BYTES: u16 = 64;
pub const SAVE_FP_INIT_POLICY: u8 = 1;

/// Returns the stable 64-bit result for one CPUID selector.
///
/// Unknown classes, leaves, sparse indexes, and indexes beyond a leaf's header
/// return zero as required by the architectural query model.
pub fn query(selector: u64) -> u64 {
    let class = (selector >> 32) as u32;
    let leaf = (selector >> 16) as u16;
    let index = selector as u16;

    match (class, leaf, index) {
        (BASE_CLASS, BASE_IDENTITY_LEAF, 0) => header_with_class(2, 0, 18),
        (BASE_CLASS, BASE_IDENTITY_LEAF, 1) => {
            ((VENDOR_ID as u64) << 48) | ((ARCHITECTURE_ID as u64) << 32) | IMPLEMENTATION_ID as u64
        }
        (BASE_CLASS, BASE_IDENTITY_LEAF, 2) => {
            ((IMPLEMENTATION_REVISION as u64) << 16) | ARCHITECTURE_REVISION as u64
        }
        (BASE_CLASS, BASE_IDENTITY_LEAF, 3..=10) => name_word(VENDOR_NAME, usize::from(index - 3)),
        (BASE_CLASS, BASE_IDENTITY_LEAF, 11..=18) => {
            name_word(PROCESSOR_NAME, usize::from(index - 11))
        }

        (EXTENSION_CLASS, EXTENSION_DIRECTORY_LEAF, 0) => header_with_leaf(1, 1),
        (EXTENSION_CLASS, EXTENSION_DIRECTORY_LEAF, 1) => (1 << 0) | (1 << 1),
        (EXTENSION_CLASS, FPTRANSA_ACCURACY_LEAF, 0) => leaf_header(MAX_CONTRACT_ID),
        (EXTENSION_CLASS, FPTRANSA_ACCURACY_LEAF, contract_id) => {
            contract_by_id(contract_id).map_or(0, |contract| contract.cpuid_result())
        }

        (IMPLEMENTATION_CLASS, IMPLEMENTATION_DIRECTORY_LEAF, 0) => header_with_leaf(4, 0),
        (IMPLEMENTATION_CLASS, CACHE_TOPOLOGY_LEAF, 0) => leaf_header(1),
        (IMPLEMENTATION_CLASS, CACHE_TOPOLOGY_LEAF, 1) => MAINTENANCE_GRANULE_BYTES as u64,
        (IMPLEMENTATION_CLASS, PERFORMANCE_COUNTERS_LEAF, 0) => leaf_header(3),
        (IMPLEMENTATION_CLASS, PERFORMANCE_COUNTERS_LEAF, 1..=3) => 1,
        (IMPLEMENTATION_CLASS, SAVE_AREA_LAYOUT_LEAF, 0) => leaf_header(4),
        (IMPLEMENTATION_CLASS, SAVE_AREA_LAYOUT_LEAF, 1) => SAVE_AREA_SIZE_BYTES,
        (IMPLEMENTATION_CLASS, SAVE_AREA_LAYOUT_LEAF, 2) => {
            ((SAVE_FORMAT as u64) << 48)
                | ((SAVE_BITMAP_WORDS as u64) << 32)
                | (1_u64 << 16)
                | SAVE_FIXED_SIZE_BYTES as u64
        }
        (IMPLEMENTATION_CLASS, SAVE_AREA_LAYOUT_LEAF, 3) => {
            ((SAVE_FP_OFFSET_BYTES as u64) << 32)
                | ((SAVE_FP_BITMAP_BIT as u64) << 16)
                | SAVE_FP_COMPONENT_ID as u64
        }
        (IMPLEMENTATION_CLASS, SAVE_AREA_LAYOUT_LEAF, 4) => {
            ((SAVE_FP_INIT_POLICY as u64) << 48)
                | ((SAVE_FP_ALIGNMENT_BYTES as u64) << 32)
                | SAVE_FP_MAX_SIZE_BYTES as u64
        }
        _ => 0,
    }
}

const fn header_with_class(max_class: u32, max_leaf: u16, max_index: u16) -> u64 {
    ((max_class as u64) << 32) | ((max_leaf as u64) << 16) | max_index as u64
}

const fn header_with_leaf(max_leaf: u16, max_index: u16) -> u64 {
    ((max_leaf as u64) << 16) | max_index as u64
}

const fn leaf_header(max_index: u16) -> u64 {
    max_index as u64
}

fn name_word(name: &[u8], word_index: usize) -> u64 {
    let start = word_index * 8;
    let mut result = 0_u64;
    for byte_index in 0..8 {
        if let Some(byte) = name.get(start + byte_index) {
            result |= u64::from(*byte) << (byte_index * 8);
        }
    }
    result
}

#[cfg(test)]
mod tests {
    use super::{
        ARCHITECTURE_ID, ARCHITECTURE_REVISION, IMPLEMENTATION_ID, IMPLEMENTATION_REVISION,
        MAINTENANCE_GRANULE_BYTES, PROCESSOR_NAME, SAVE_AREA_SIZE_BYTES, SAVE_BITMAP_WORDS,
        SAVE_FIXED_SIZE_BYTES, SAVE_FORMAT, SAVE_FP_ALIGNMENT_BYTES, SAVE_FP_BITMAP_BIT,
        SAVE_FP_COMPONENT_ID, SAVE_FP_INIT_POLICY, SAVE_FP_MAX_SIZE_BYTES, SAVE_FP_OFFSET_BYTES,
        VENDOR_ID, VENDOR_NAME, query,
    };
    use crate::fpu::trans::contracts::{CONTRACTS, MAX_CONTRACT_ID, contract_by_id};

    const fn selector(class: u32, leaf: u16, index: u16) -> u64 {
        ((class as u64) << 32) | ((leaf as u64) << 16) | index as u64
    }

    fn decoded_name(first_index: u16) -> [u8; 64] {
        let mut result = [0_u8; 64];
        for word in 0..8_u16 {
            result[usize::from(word) * 8..usize::from(word + 1) * 8]
                .copy_from_slice(&query(selector(0, 0, first_index + word)).to_le_bytes());
        }
        result
    }

    #[test]
    fn all_defined_leaf_headers_encode_maximum_selectors() {
        let expected = [
            (selector(0, 0, 0), 0x0000_0002_0000_0012),
            (selector(1, 0, 0), 0x0000_0000_0001_0001),
            (selector(1, 1, 0), 0x0000_0000_0000_0044),
            (selector(2, 0, 0), 0x0000_0000_0004_0000),
            (selector(2, 1, 0), 0x0000_0000_0000_0001),
            (selector(2, 2, 0), 0x0000_0000_0000_0003),
            (selector(2, 4, 0), 0x0000_0000_0000_0004),
        ];
        for (selector, result) in expected {
            assert_eq!(query(selector), result);
        }
    }

    #[test]
    fn base_identity_and_names_are_stable_and_zero_padded() {
        assert_eq!(
            query(selector(0, 0, 1)),
            ((VENDOR_ID as u64) << 48)
                | ((ARCHITECTURE_ID as u64) << 32)
                | IMPLEMENTATION_ID as u64
        );
        assert_eq!(
            query(selector(0, 0, 2)),
            ((IMPLEMENTATION_REVISION as u64) << 16) | ARCHITECTURE_REVISION as u64
        );

        let vendor = decoded_name(3);
        assert_eq!(&vendor[..VENDOR_NAME.len()], VENDOR_NAME);
        assert!(vendor[VENDOR_NAME.len()..].iter().all(|&byte| byte == 0));
        let processor = decoded_name(11);
        assert_eq!(&processor[..PROCESSOR_NAME.len()], PROCESSOR_NAME);
        assert!(
            processor[PROCESSOR_NAME.len()..]
                .iter()
                .all(|&byte| byte == 0)
        );
    }

    #[test]
    fn extension_bits_and_all_nineteen_accuracy_results_share_the_contract_owner() {
        assert_eq!(query(selector(1, 0, 1)), 0b11);
        assert_eq!(CONTRACTS.len(), 19);
        for contract in CONTRACTS {
            assert_eq!(
                query(selector(1, 1, contract.contract_id)),
                contract.cpuid_result()
            );
        }
    }

    #[test]
    fn sparse_accuracy_holes_and_unknown_selectors_return_zero() {
        for contract_id in 1..=MAX_CONTRACT_ID {
            let expected =
                contract_by_id(contract_id).map_or(0, |contract| contract.cpuid_result());
            assert_eq!(query(selector(1, 1, contract_id)), expected);
        }
        for unknown in [
            selector(0, 0, 19),
            selector(0, 1, 0),
            selector(1, 0, 2),
            selector(1, 1, MAX_CONTRACT_ID + 1),
            selector(1, 2, 0),
            selector(2, 1, 2),
            selector(2, 2, 4),
            selector(2, 3, 0),
            selector(2, 4, 5),
            selector(3, 0, 0),
            u64::MAX,
        ] {
            assert_eq!(query(unknown), 0);
        }
    }

    #[test]
    fn cacheless_topology_and_mandatory_counters_have_exact_encodings() {
        assert_eq!(MAINTENANCE_GRANULE_BYTES, 64);
        assert_eq!(query(selector(2, 1, 1)), 64);
        assert_eq!(query(selector(2, 1, 2)), 0);
        for counter_id in 1..=3 {
            assert_eq!(query(selector(2, 2, counter_id)), 1);
        }
    }

    #[test]
    fn single_fp_save_component_has_the_authoritative_layout() {
        assert_eq!(SAVE_AREA_SIZE_BYTES, 0x0180);
        assert_eq!(SAVE_FIXED_SIZE_BYTES, 0x00c0);
        assert_eq!(SAVE_BITMAP_WORDS, 1);
        assert_eq!(SAVE_FORMAT, 0);
        assert_eq!(SAVE_FP_COMPONENT_ID, 1);
        assert_eq!(SAVE_FP_BITMAP_BIT, 0);
        assert_eq!(SAVE_FP_OFFSET_BYTES, 0x00c0);
        assert_eq!(SAVE_FP_MAX_SIZE_BYTES, 0x00c0);
        assert_eq!(SAVE_FP_ALIGNMENT_BYTES, 64);
        assert_eq!(SAVE_FP_INIT_POLICY, 1);

        assert_eq!(query(selector(2, 4, 1)), 0x0000_0000_0000_0180);
        assert_eq!(query(selector(2, 4, 2)), 0x0000_0001_0001_00c0);
        assert_eq!(query(selector(2, 4, 3)), 0x0000_00c0_0000_0001);
        assert_eq!(query(selector(2, 4, 4)), 0x0001_0040_0000_00c0);
    }
}
