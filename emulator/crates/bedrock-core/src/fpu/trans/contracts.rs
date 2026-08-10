//! Stable FPTRANSA operation and accuracy-contract descriptors.

use crate::fpu::env::FpCauses;

pub const CONTRACT_COUNT: usize = 19;
pub const CONTRACT_REVISION: u8 = 1;
pub const ADVERTISED_MAX_ULP_Q8_8: u16 = 0x0100;
pub const MAX_CONTRACT_ID: u16 = 0x0044;

const NV: FpCauses = FpCauses::NV;
const NV_UF: FpCauses = NV.union(FpCauses::UF);
const NV_OF: FpCauses = NV.union(FpCauses::OF);
const NV_DZ_UF: FpCauses = NV.union(FpCauses::DZ).union(FpCauses::UF);
const NV_OF_UF: FpCauses = NV.union(FpCauses::OF).union(FpCauses::UF);

/// Code-level identity for one stable FPTRANSA accuracy contract.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub enum TransOperation {
    Sine,
    Cosine,
    Tangent,
    SineCosine,
    ArcSine,
    ArcCosine,
    ArcTangent,
    HyperbolicSine,
    HyperbolicCosine,
    HyperbolicTangent,
    HyperbolicArcTangent,
    Exponential,
    ExponentialMinusOne,
    ExponentialBaseTwo,
    ExponentialBaseTen,
    NaturalLogarithm,
    NaturalLogarithmPlusOne,
    LogarithmBaseTwo,
    LogarithmBaseTen,
}

/// The exact-reference input domain named by the accuracy contract.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum TransDomain {
    FiniteAbsLePiOverFour,
    FiniteAbsLeOne,
    FiniteOrSignedInfinity,
    PositiveOrPositiveInfinityZeroDz,
    FiniteGeMinusOneOrPositiveInfinityMinusOneDz,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum TransResultArity {
    Single,
    Pair,
}

/// One present revision-1 FPTRANSA accuracy contract.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct TransContract {
    pub operation: TransOperation,
    pub contract_id: u16,
    pub operation_name: &'static str,
    pub revision: u8,
    pub present: bool,
    pub s_max_ulp_q8_8: u16,
    pub d_max_ulp_q8_8: u16,
    pub domain: TransDomain,
    pub cause_mask: FpCauses,
    pub result_arity: TransResultArity,
}

impl TransContract {
    const fn new(
        operation: TransOperation,
        contract_id: u16,
        operation_name: &'static str,
        domain: TransDomain,
        cause_mask: FpCauses,
        result_arity: TransResultArity,
    ) -> Self {
        Self {
            operation,
            contract_id,
            operation_name,
            revision: CONTRACT_REVISION,
            present: true,
            s_max_ulp_q8_8: ADVERTISED_MAX_ULP_Q8_8,
            d_max_ulp_q8_8: ADVERTISED_MAX_ULP_Q8_8,
            domain,
            cause_mask,
            result_arity,
        }
    }

    /// Encodes the sparse FPTRANSA_ACCURACY CPUID result for this contract.
    pub const fn cpuid_result(self) -> u64 {
        let present = if self.present { 1_u64 << 63 } else { 0 };
        present
            | ((self.revision as u64) << 32)
            | ((self.d_max_ulp_q8_8 as u64) << 16)
            | self.s_max_ulp_q8_8 as u64
    }
}

/// The sole implementation-owned FPTRANSA operation/accuracy table.
pub const CONTRACTS: [TransContract; CONTRACT_COUNT] = [
    TransContract::new(
        TransOperation::Sine,
        0x0001,
        "FSINA",
        TransDomain::FiniteAbsLePiOverFour,
        NV_UF,
        TransResultArity::Single,
    ),
    TransContract::new(
        TransOperation::Cosine,
        0x0002,
        "FCOSA",
        TransDomain::FiniteAbsLePiOverFour,
        NV,
        TransResultArity::Single,
    ),
    TransContract::new(
        TransOperation::Tangent,
        0x0003,
        "FTANA",
        TransDomain::FiniteAbsLePiOverFour,
        NV_UF,
        TransResultArity::Single,
    ),
    TransContract::new(
        TransOperation::SineCosine,
        0x0004,
        "FSINCOSA",
        TransDomain::FiniteAbsLePiOverFour,
        NV_UF,
        TransResultArity::Pair,
    ),
    TransContract::new(
        TransOperation::ArcSine,
        0x0011,
        "FASINA",
        TransDomain::FiniteAbsLeOne,
        NV_UF,
        TransResultArity::Single,
    ),
    TransContract::new(
        TransOperation::ArcCosine,
        0x0012,
        "FACOSA",
        TransDomain::FiniteAbsLeOne,
        NV_UF,
        TransResultArity::Single,
    ),
    TransContract::new(
        TransOperation::ArcTangent,
        0x0013,
        "FATANA",
        TransDomain::FiniteOrSignedInfinity,
        NV_UF,
        TransResultArity::Single,
    ),
    TransContract::new(
        TransOperation::HyperbolicSine,
        0x0021,
        "FSINHA",
        TransDomain::FiniteOrSignedInfinity,
        NV_OF_UF,
        TransResultArity::Single,
    ),
    TransContract::new(
        TransOperation::HyperbolicCosine,
        0x0022,
        "FCOSHA",
        TransDomain::FiniteOrSignedInfinity,
        NV_OF,
        TransResultArity::Single,
    ),
    TransContract::new(
        TransOperation::HyperbolicTangent,
        0x0023,
        "FTANHA",
        TransDomain::FiniteOrSignedInfinity,
        NV_UF,
        TransResultArity::Single,
    ),
    TransContract::new(
        TransOperation::HyperbolicArcTangent,
        0x0024,
        "FATANHA",
        TransDomain::FiniteAbsLeOne,
        NV_DZ_UF,
        TransResultArity::Single,
    ),
    TransContract::new(
        TransOperation::Exponential,
        0x0031,
        "FETOXA",
        TransDomain::FiniteOrSignedInfinity,
        NV_OF_UF,
        TransResultArity::Single,
    ),
    TransContract::new(
        TransOperation::ExponentialMinusOne,
        0x0032,
        "FETOXM1A",
        TransDomain::FiniteOrSignedInfinity,
        NV_OF_UF,
        TransResultArity::Single,
    ),
    TransContract::new(
        TransOperation::ExponentialBaseTwo,
        0x0033,
        "FTWOTOXA",
        TransDomain::FiniteOrSignedInfinity,
        NV_OF_UF,
        TransResultArity::Single,
    ),
    TransContract::new(
        TransOperation::ExponentialBaseTen,
        0x0034,
        "FTENTOXA",
        TransDomain::FiniteOrSignedInfinity,
        NV_OF_UF,
        TransResultArity::Single,
    ),
    TransContract::new(
        TransOperation::NaturalLogarithm,
        0x0041,
        "FLOGNA",
        TransDomain::PositiveOrPositiveInfinityZeroDz,
        NV_DZ_UF,
        TransResultArity::Single,
    ),
    TransContract::new(
        TransOperation::NaturalLogarithmPlusOne,
        0x0042,
        "FLOGNP1A",
        TransDomain::FiniteGeMinusOneOrPositiveInfinityMinusOneDz,
        NV_DZ_UF,
        TransResultArity::Single,
    ),
    TransContract::new(
        TransOperation::LogarithmBaseTwo,
        0x0043,
        "FLOG2A",
        TransDomain::PositiveOrPositiveInfinityZeroDz,
        NV_DZ_UF,
        TransResultArity::Single,
    ),
    TransContract::new(
        TransOperation::LogarithmBaseTen,
        0x0044,
        "FLOG10A",
        TransDomain::PositiveOrPositiveInfinityZeroDz,
        NV_DZ_UF,
        TransResultArity::Single,
    ),
];

pub fn contract_by_id(contract_id: u16) -> Option<&'static TransContract> {
    CONTRACTS
        .iter()
        .find(|contract| contract.contract_id == contract_id)
}

pub fn contract_for_operation(operation: TransOperation) -> &'static TransContract {
    CONTRACTS
        .iter()
        .find(|contract| contract.operation == operation)
        .expect("every FPTRANSA operation must have exactly one contract")
}

#[cfg(test)]
mod tests {
    use super::{
        ADVERTISED_MAX_ULP_Q8_8, CONTRACT_COUNT, CONTRACT_REVISION, CONTRACTS, MAX_CONTRACT_ID,
        TransDomain, TransOperation, TransResultArity, contract_by_id, contract_for_operation,
    };
    use crate::fpu::env::FpCauses;

    #[test]
    fn all_nineteen_contracts_have_the_exact_stable_identity_and_domain() {
        let expected = [
            (
                TransOperation::Sine,
                0x0001,
                "FSINA",
                TransDomain::FiniteAbsLePiOverFour,
            ),
            (
                TransOperation::Cosine,
                0x0002,
                "FCOSA",
                TransDomain::FiniteAbsLePiOverFour,
            ),
            (
                TransOperation::Tangent,
                0x0003,
                "FTANA",
                TransDomain::FiniteAbsLePiOverFour,
            ),
            (
                TransOperation::SineCosine,
                0x0004,
                "FSINCOSA",
                TransDomain::FiniteAbsLePiOverFour,
            ),
            (
                TransOperation::ArcSine,
                0x0011,
                "FASINA",
                TransDomain::FiniteAbsLeOne,
            ),
            (
                TransOperation::ArcCosine,
                0x0012,
                "FACOSA",
                TransDomain::FiniteAbsLeOne,
            ),
            (
                TransOperation::ArcTangent,
                0x0013,
                "FATANA",
                TransDomain::FiniteOrSignedInfinity,
            ),
            (
                TransOperation::HyperbolicSine,
                0x0021,
                "FSINHA",
                TransDomain::FiniteOrSignedInfinity,
            ),
            (
                TransOperation::HyperbolicCosine,
                0x0022,
                "FCOSHA",
                TransDomain::FiniteOrSignedInfinity,
            ),
            (
                TransOperation::HyperbolicTangent,
                0x0023,
                "FTANHA",
                TransDomain::FiniteOrSignedInfinity,
            ),
            (
                TransOperation::HyperbolicArcTangent,
                0x0024,
                "FATANHA",
                TransDomain::FiniteAbsLeOne,
            ),
            (
                TransOperation::Exponential,
                0x0031,
                "FETOXA",
                TransDomain::FiniteOrSignedInfinity,
            ),
            (
                TransOperation::ExponentialMinusOne,
                0x0032,
                "FETOXM1A",
                TransDomain::FiniteOrSignedInfinity,
            ),
            (
                TransOperation::ExponentialBaseTwo,
                0x0033,
                "FTWOTOXA",
                TransDomain::FiniteOrSignedInfinity,
            ),
            (
                TransOperation::ExponentialBaseTen,
                0x0034,
                "FTENTOXA",
                TransDomain::FiniteOrSignedInfinity,
            ),
            (
                TransOperation::NaturalLogarithm,
                0x0041,
                "FLOGNA",
                TransDomain::PositiveOrPositiveInfinityZeroDz,
            ),
            (
                TransOperation::NaturalLogarithmPlusOne,
                0x0042,
                "FLOGNP1A",
                TransDomain::FiniteGeMinusOneOrPositiveInfinityMinusOneDz,
            ),
            (
                TransOperation::LogarithmBaseTwo,
                0x0043,
                "FLOG2A",
                TransDomain::PositiveOrPositiveInfinityZeroDz,
            ),
            (
                TransOperation::LogarithmBaseTen,
                0x0044,
                "FLOG10A",
                TransDomain::PositiveOrPositiveInfinityZeroDz,
            ),
        ];

        assert_eq!(CONTRACTS.len(), CONTRACT_COUNT);
        for (contract, expected) in CONTRACTS.iter().zip(expected) {
            assert_eq!(
                (
                    contract.operation,
                    contract.contract_id,
                    contract.operation_name,
                    contract.domain,
                ),
                expected
            );
        }
    }

    #[test]
    fn every_contract_is_present_revision_one_and_advertises_one_ulp_for_both_formats() {
        assert_eq!(MAX_CONTRACT_ID, 0x0044);
        for contract in CONTRACTS {
            assert!(contract.present);
            assert_eq!(contract.revision, CONTRACT_REVISION);
            assert_eq!(contract.s_max_ulp_q8_8, ADVERTISED_MAX_ULP_Q8_8);
            assert_eq!(contract.d_max_ulp_q8_8, ADVERTISED_MAX_ULP_Q8_8);
            assert_eq!(contract.cpuid_result(), 0x8000_0001_0100_0100);
        }
    }

    #[test]
    fn cause_masks_and_pair_arity_match_all_instruction_contracts() {
        let expected_masks = [
            0x09, 0x01, 0x09, 0x09, 0x09, 0x09, 0x09, 0x0d, 0x05, 0x09, 0x0b, 0x0d, 0x0d, 0x0d,
            0x0d, 0x0b, 0x0b, 0x0b, 0x0b,
        ];
        for (contract, expected_mask) in CONTRACTS.iter().zip(expected_masks) {
            assert_eq!(contract.cause_mask.bits(), expected_mask);
            assert_eq!(contract.cause_mask.bits() & FpCauses::NX.bits(), 0);
            assert_eq!(
                contract.result_arity,
                if contract.operation == TransOperation::SineCosine {
                    TransResultArity::Pair
                } else {
                    TransResultArity::Single
                }
            );
        }
    }

    #[test]
    fn sparse_lookup_has_one_unique_entry_for_every_operation_and_id() {
        for (index, contract) in CONTRACTS.iter().enumerate() {
            assert_eq!(contract_by_id(contract.contract_id), Some(contract));
            assert_eq!(contract_for_operation(contract.operation), contract);
            assert!(
                !CONTRACTS[..index]
                    .iter()
                    .any(|prior| prior.contract_id == contract.contract_id)
            );
            assert!(
                !CONTRACTS[..index]
                    .iter()
                    .any(|prior| prior.operation == contract.operation)
            );
        }
        for unassigned in [
            0x0000, 0x0005, 0x0010, 0x0014, 0x0020, 0x0025, 0x0030, 0x0035, 0x0040, 0x0045,
        ] {
            assert_eq!(contract_by_id(unassigned), None);
        }
    }
}
