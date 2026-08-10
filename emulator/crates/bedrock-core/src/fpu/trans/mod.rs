//! Common deterministic FPTRANSA processing and domain module ownership.

pub mod circular;
pub mod contracts;
pub mod exp_log;
pub mod hyperbolic;

use crate::fpu::{
    effect::{FpEffect, FpRequest, FpResult, finish_result},
    env::FpCauses,
};

use self::contracts::{TransContract, TransOperation, TransResultArity, contract_for_operation};

/// Result of common input processing before domain-specific evaluation.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum TransPrepared {
    Evaluate {
        contract: &'static TransContract,
        input: u64,
    },
    Complete(FpEffect),
}

/// A nearest-even formatted result supplied by a domain evaluator.
///
/// `DefaultNan` variants represent a NaN produced by the operation itself;
/// propagated operand NaNs are handled by [`prepare`].
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum TransOutput {
    Approximation(u64),
    ApproximationPair(u64, u64),
    DefaultNan,
    DefaultNanPair,
}

#[derive(Debug, Clone, Copy)]
enum FinalValue {
    Approximation(u64),
    PropagatedNan(u64),
    DefaultNan,
}

/// Applies the common input order: operand count, ordered NaN selection, then DAZ.
///
/// FPTRANSA instructions have one source operand. `FSTATUS.RM` is deliberately
/// not consulted; domain evaluators use the pinned nearest-even soft-float path.
pub fn prepare(operation: TransOperation, request: FpRequest<'_>) -> TransPrepared {
    assert_eq!(
        request.operands.len(),
        1,
        "FPTRANSA operation received the wrong operand count"
    );
    let contract = contract_for_operation(operation);
    if let Some(nan) = request.selected_nan() {
        let value = FinalValue::PropagatedNan(nan);
        let values = values_for_arity(contract.result_arity, value);
        return TransPrepared::Complete(finish_values(
            contract,
            request,
            values,
            request.signaling_nan_cause(),
        ));
    }

    TransPrepared::Evaluate {
        contract,
        input: request
            .status
            .preprocess(request.format, request.operands[0]),
    }
}

/// Applies operation-produced default NaN, DN, FTZ, the FPTRANSA cause mask,
/// and the enabled-cause decision to a domain evaluator result.
pub fn finish(
    operation: TransOperation,
    request: FpRequest<'_>,
    output: TransOutput,
    causes: FpCauses,
) -> FpEffect {
    let contract = contract_for_operation(operation);
    let values = match output {
        TransOutput::Approximation(value) => {
            assert_eq!(contract.result_arity, TransResultArity::Single);
            [Some(FinalValue::Approximation(value)), None]
        }
        TransOutput::ApproximationPair(first, second) => {
            assert_eq!(contract.result_arity, TransResultArity::Pair);
            [
                Some(FinalValue::Approximation(first)),
                Some(FinalValue::Approximation(second)),
            ]
        }
        TransOutput::DefaultNan => {
            assert_eq!(contract.result_arity, TransResultArity::Single);
            [Some(FinalValue::DefaultNan), None]
        }
        TransOutput::DefaultNanPair => {
            assert_eq!(contract.result_arity, TransResultArity::Pair);
            [Some(FinalValue::DefaultNan), Some(FinalValue::DefaultNan)]
        }
    };
    finish_values(contract, request, values, causes)
}

fn values_for_arity(arity: TransResultArity, value: FinalValue) -> [Option<FinalValue>; 2] {
    match arity {
        TransResultArity::Single => [Some(value), None],
        TransResultArity::Pair => [Some(value), Some(value)],
    }
}

fn finish_values(
    contract: &'static TransContract,
    request: FpRequest<'_>,
    values: [Option<FinalValue>; 2],
    causes: FpCauses,
) -> FpEffect {
    let mut causes = without_nx(causes);
    let first = postprocess_value(
        request,
        values[0].expect("FPTRANSA result is missing"),
        &mut causes,
    );
    let result = match values[1] {
        Some(second) => FpResult::FloatPair(first, postprocess_value(request, second, &mut causes)),
        None => FpResult::Float(first),
    };

    assert_eq!(
        causes.bits() & !contract.cause_mask.bits(),
        0,
        "FPTRANSA domain produced a cause excluded by its contract"
    );
    finish_result(request.status, result, causes)
}

fn postprocess_value(request: FpRequest<'_>, value: FinalValue, causes: &mut FpCauses) -> u64 {
    let format = request.format;
    let mut result = match value {
        FinalValue::Approximation(bits) => {
            let bits = format.canonical_bits(bits);
            assert!(
                !format.is_nan(bits),
                "operation-produced NaN must use the FPTRANSA default-NaN output"
            );
            bits
        }
        FinalValue::PropagatedNan(bits) => {
            assert!(format.is_nan(bits));
            format.quiet_nan(bits)
        }
        FinalValue::DefaultNan => {
            *causes = causes.union(FpCauses::NV);
            format.default_nan()
        }
    };

    if format.is_nan(result) && request.status.default_nan {
        result = format.default_nan();
    }
    if request.status.ftz && format.is_subnormal(result) {
        result = format.signed_zero(format.sign(result));
        *causes = causes.union(FpCauses::UF);
    }
    result
}

fn without_nx(causes: FpCauses) -> FpCauses {
    let mut result = FpCauses::default();
    for cause in [FpCauses::NV, FpCauses::DZ, FpCauses::OF, FpCauses::UF] {
        if causes.bits() & cause.bits() != 0 {
            result = result.union(cause);
        }
    }
    result
}

#[cfg(test)]
mod tests {
    use super::{TransOutput, TransPrepared, finish, prepare};
    use crate::fpu::{
        effect::{FpEffect, FpRequest, FpResult},
        env::{FpCauses, FpStatus},
        format::FpFormat,
        trans::contracts::{TransOperation, TransResultArity},
    };

    #[test]
    fn prepare_applies_daz_and_ignores_every_rounding_mode() {
        let operand = [0x8000_0001];
        for rounding in 0..4 {
            let request = FpRequest {
                format: FpFormat::S,
                status: FpStatus::decode((rounding << 5) | (1 << 8)).unwrap(),
                operands: &operand,
            };
            assert_eq!(
                prepare(TransOperation::Sine, request),
                TransPrepared::Evaluate {
                    contract: super::contract_for_operation(TransOperation::Sine),
                    input: 0x8000_0000,
                }
            );
        }
    }

    #[test]
    fn signaling_nan_is_quieted_before_dn_and_accrues_only_nv() {
        let operand = [0xff80_0123];
        let request = FpRequest {
            format: FpFormat::S,
            status: FpStatus::decode(0).unwrap(),
            operands: &operand,
        };
        assert_eq!(
            prepare(TransOperation::Sine, request),
            TransPrepared::Complete(FpEffect::Commit {
                result: FpResult::Float(0xffc0_0123),
                causes: FpCauses::NV,
            })
        );

        let dn_request = FpRequest {
            status: FpStatus::decode(1 << 9).unwrap(),
            ..request
        };
        assert_eq!(
            prepare(TransOperation::Sine, dn_request),
            TransPrepared::Complete(FpEffect::Commit {
                result: FpResult::Float(0x7fc0_0000),
                causes: FpCauses::NV,
            })
        );
    }

    #[test]
    fn quiet_nan_never_accrues_or_faults_for_nx() {
        let operand = [0x7ff8_0000_0000_0042];
        let request = FpRequest {
            format: FpFormat::D,
            status: FpStatus::decode(FpCauses::NX.bits()).unwrap(),
            operands: &operand,
        };
        assert_eq!(
            prepare(TransOperation::NaturalLogarithm, request),
            TransPrepared::Complete(FpEffect::Commit {
                result: FpResult::Float(operand[0]),
                causes: FpCauses::default(),
            })
        );
    }

    #[test]
    fn operation_nan_is_always_the_architectural_default_and_adds_nv() {
        let operand = [0xc000_0000];
        let request = FpRequest {
            format: FpFormat::S,
            status: FpStatus::decode(0).unwrap(),
            operands: &operand,
        };
        assert_eq!(
            finish(
                TransOperation::NaturalLogarithm,
                request,
                TransOutput::DefaultNan,
                FpCauses::default(),
            ),
            FpEffect::Commit {
                result: FpResult::Float(0x7fc0_0000),
                causes: FpCauses::NV,
            }
        );
    }

    #[test]
    fn ftz_adds_uf_but_never_nx_or_an_nx_fault() {
        let operand = [0x0080_0000];
        let request = FpRequest {
            format: FpFormat::S,
            status: FpStatus::decode((1 << 7) | FpCauses::NX.bits()).unwrap(),
            operands: &operand,
        };
        assert_eq!(
            finish(
                TransOperation::Sine,
                request,
                TransOutput::Approximation(0x8000_0001),
                FpCauses::NX,
            ),
            FpEffect::Commit {
                result: FpResult::Float(0x8000_0000),
                causes: FpCauses::UF,
            }
        );

        let trapping = FpRequest {
            status: FpStatus::decode((1 << 7) | FpCauses::UF.bits()).unwrap(),
            ..request
        };
        assert_eq!(
            finish(
                TransOperation::Sine,
                trapping,
                TransOutput::Approximation(1),
                FpCauses::default(),
            ),
            FpEffect::Fault {
                causes: FpCauses::UF,
            }
        );
    }

    #[test]
    fn sincos_nan_and_numeric_results_remain_one_atomic_pair_effect() {
        let nan_operand = [0x7f80_0001];
        let nan_request = FpRequest {
            format: FpFormat::S,
            status: FpStatus::decode(0).unwrap(),
            operands: &nan_operand,
        };
        assert_eq!(
            prepare(TransOperation::SineCosine, nan_request),
            TransPrepared::Complete(FpEffect::Commit {
                result: FpResult::FloatPair(0x7fc0_0001, 0x7fc0_0001),
                causes: FpCauses::NV,
            })
        );

        let zero = [0_u64];
        let request = FpRequest {
            format: FpFormat::S,
            status: FpStatus::decode(0).unwrap(),
            operands: &zero,
        };
        assert_eq!(
            finish(
                TransOperation::SineCosine,
                request,
                TransOutput::ApproximationPair(0, 0x3f80_0000),
                FpCauses::default(),
            ),
            FpEffect::Commit {
                result: FpResult::FloatPair(0, 0x3f80_0000),
                causes: FpCauses::default(),
            }
        );
        assert_eq!(
            super::contract_for_operation(TransOperation::SineCosine).result_arity,
            TransResultArity::Pair
        );
    }

    #[test]
    fn all_allowed_causes_survive_except_nx() {
        let operand = [0_u64];
        let request = FpRequest {
            format: FpFormat::D,
            status: FpStatus::decode(0).unwrap(),
            operands: &operand,
        };
        let causes = FpCauses::NV
            .union(FpCauses::DZ)
            .union(FpCauses::UF)
            .union(FpCauses::NX);
        assert_eq!(
            finish(
                TransOperation::NaturalLogarithm,
                request,
                TransOutput::Approximation(0xfff0_0000_0000_0000),
                causes,
            ),
            FpEffect::Commit {
                result: FpResult::Float(0xfff0_0000_0000_0000),
                causes: FpCauses::NV.union(FpCauses::DZ).union(FpCauses::UF),
            }
        );
    }

    #[test]
    #[should_panic(expected = "cause excluded by its contract")]
    fn a_domain_cannot_accrue_an_operation_excluded_cause() {
        let operand = [0_u64];
        finish(
            TransOperation::Cosine,
            FpRequest {
                format: FpFormat::S,
                status: FpStatus::decode(0).unwrap(),
                operands: &operand,
            },
            TransOutput::Approximation(0x3f80_0000),
            FpCauses::OF,
        );
    }

    #[test]
    #[should_panic(expected = "operation-produced NaN")]
    fn a_domain_must_label_an_operation_produced_nan() {
        let operand = [0_u64];
        finish(
            TransOperation::Sine,
            FpRequest {
                format: FpFormat::S,
                status: FpStatus::decode(0).unwrap(),
                operands: &operand,
            },
            TransOutput::Approximation(0x7fc0_0042),
            FpCauses::NV,
        );
    }

    #[test]
    #[should_panic(expected = "wrong operand count")]
    fn every_fptransa_operation_requires_exactly_one_source() {
        prepare(
            TransOperation::Sine,
            FpRequest {
                format: FpFormat::S,
                status: FpStatus::decode(0).unwrap(),
                operands: &[],
            },
        );
    }

    #[test]
    #[should_panic]
    fn single_and_pair_outputs_cannot_cross_operation_arity() {
        let operand = [0_u64];
        finish(
            TransOperation::Sine,
            FpRequest {
                format: FpFormat::S,
                status: FpStatus::decode(0).unwrap(),
                operands: &operand,
            },
            TransOutput::ApproximationPair(0, 0x3f80_0000),
            FpCauses::default(),
        );
    }
}
