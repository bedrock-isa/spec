//! Deterministic circular FPTRANSA operations.

use fpmath::{SoftF32, SoftF64};

use crate::fpu::{
    effect::{FpEffect, FpRequest},
    env::FpCauses,
    format::FpFormat,
};

use super::{
    TransOutput, TransPrepared,
    contracts::{TransDomain, TransOperation},
    finish, prepare,
};

type UnaryS = fn(SoftF32) -> SoftF32;
type UnaryD = fn(SoftF64) -> SoftF64;
type PairS = fn(SoftF32) -> (SoftF32, SoftF32);
type PairD = fn(SoftF64) -> (SoftF64, SoftF64);

/// Executes one circular FPTRANSA operation without architectural state access.
pub fn execute(operation: TransOperation, request: FpRequest<'_>) -> FpEffect {
    match operation {
        TransOperation::Sine => unary(operation, request, fpmath::sin, fpmath::sin),
        TransOperation::Cosine => unary(operation, request, fpmath::cos, fpmath::cos),
        TransOperation::Tangent => unary(operation, request, fpmath::tan, fpmath::tan),
        TransOperation::SineCosine => pair(operation, request, fpmath::sin_cos, fpmath::sin_cos),
        TransOperation::ArcSine => unary(operation, request, fpmath::asin, fpmath::asin),
        TransOperation::ArcCosine => unary(operation, request, fpmath::acos, fpmath::acos),
        TransOperation::ArcTangent => unary(operation, request, fpmath::atan, fpmath::atan),
        _ => panic!("non-circular operation passed to circular evaluator"),
    }
}

fn unary(
    operation: TransOperation,
    request: FpRequest<'_>,
    evaluate_s: UnaryS,
    evaluate_d: UnaryD,
) -> FpEffect {
    match prepare(operation, request) {
        TransPrepared::Complete(effect) => effect,
        TransPrepared::Evaluate { contract, input } => {
            if !domain_contains(contract.domain, request.format, input) {
                return finish(
                    operation,
                    request,
                    TransOutput::DefaultNan,
                    FpCauses::default(),
                );
            }

            let result = evaluate_unary(request.format, input, evaluate_s, evaluate_d);
            finish(
                operation,
                request,
                TransOutput::Approximation(result),
                underflow_for(operation, request.format, input),
            )
        }
    }
}

fn pair(
    operation: TransOperation,
    request: FpRequest<'_>,
    evaluate_s: PairS,
    evaluate_d: PairD,
) -> FpEffect {
    match prepare(operation, request) {
        TransPrepared::Complete(effect) => effect,
        TransPrepared::Evaluate { contract, input } => {
            if !domain_contains(contract.domain, request.format, input) {
                return finish(
                    operation,
                    request,
                    TransOutput::DefaultNanPair,
                    FpCauses::default(),
                );
            }

            let (first, second) = evaluate_pair(request.format, input, evaluate_s, evaluate_d);
            finish(
                operation,
                request,
                TransOutput::ApproximationPair(first, second),
                underflow_for(operation, request.format, input),
            )
        }
    }
}

fn evaluate_unary(format: FpFormat, input: u64, evaluate_s: UnaryS, evaluate_d: UnaryD) -> u64 {
    match format {
        FpFormat::S => u64::from(evaluate_s(SoftF32::from_bits(input as u32)).to_bits()),
        FpFormat::D => evaluate_d(SoftF64::from_bits(input)).to_bits(),
    }
}

fn evaluate_pair(format: FpFormat, input: u64, evaluate_s: PairS, evaluate_d: PairD) -> (u64, u64) {
    match format {
        FpFormat::S => {
            let (first, second) = evaluate_s(SoftF32::from_bits(input as u32));
            (u64::from(first.to_bits()), u64::from(second.to_bits()))
        }
        FpFormat::D => {
            let (first, second) = evaluate_d(SoftF64::from_bits(input));
            (first.to_bits(), second.to_bits())
        }
    }
}

fn domain_contains(domain: TransDomain, format: FpFormat, input: u64) -> bool {
    let magnitude = input & !format.sign_mask();
    match domain {
        TransDomain::FiniteAbsLePiOverFour => magnitude <= pi_over_four_floor(format),
        TransDomain::FiniteAbsLeOne => magnitude <= one(format),
        TransDomain::FiniteOrSignedInfinity => true,
        TransDomain::PositiveOrPositiveInfinityZeroDz
        | TransDomain::FiniteGeMinusOneOrPositiveInfinityMinusOneDz => {
            unreachable!("non-circular domain passed to circular evaluator")
        }
    }
}

const fn pi_over_four_floor(format: FpFormat) -> u64 {
    match format {
        FpFormat::S => 0x3f49_0fda,
        FpFormat::D => 0x3fe9_21fb_5444_2d18,
    }
}

const fn one(format: FpFormat) -> u64 {
    match format {
        FpFormat::S => 0x3f80_0000,
        FpFormat::D => 0x3ff0_0000_0000_0000,
    }
}

fn underflow_for(operation: TransOperation, format: FpFormat, input: u64) -> FpCauses {
    let magnitude = input & !format.sign_mask();
    let minimum_normal = match format {
        FpFormat::S => 0x0080_0000,
        FpFormat::D => 0x0010_0000_0000_0000,
    };
    let exact_result_is_tiny = match operation {
        TransOperation::Sine | TransOperation::SineCosine | TransOperation::ArcTangent => {
            magnitude != 0 && magnitude <= minimum_normal
        }
        TransOperation::Tangent | TransOperation::ArcSine => {
            magnitude != 0 && magnitude < minimum_normal
        }
        TransOperation::Cosine | TransOperation::ArcCosine => false,
        _ => unreachable!("non-circular operation passed to circular underflow evaluation"),
    };
    if exact_result_is_tiny {
        FpCauses::UF
    } else {
        FpCauses::default()
    }
}

#[cfg(test)]
mod tests {
    use super::execute;
    use crate::fpu::{
        effect::{FpEffect, FpRequest, FpResult},
        env::{FpCauses, FpStatus},
        format::FpFormat,
        trans::contracts::TransOperation,
    };

    fn request(format: FpFormat, status: u16, operand: &[u64; 1]) -> FpRequest<'_> {
        FpRequest {
            format,
            status: FpStatus::decode(status).unwrap(),
            operands: operand,
        }
    }

    fn run(operation: TransOperation, format: FpFormat, status: u16, operand: u64) -> FpEffect {
        let operands = [operand];
        execute(operation, request(format, status, &operands))
    }

    fn committed_float(effect: FpEffect) -> (u64, FpCauses) {
        match effect {
            FpEffect::Commit {
                result: FpResult::Float(value),
                causes,
            } => (value, causes),
            other => panic!("expected committed float, got {other:?}"),
        }
    }

    fn zero_and_one(format: FpFormat) -> (u64, u64) {
        match format {
            FpFormat::S => (0x8000_0000, 0x3f80_0000),
            FpFormat::D => (0x8000_0000_0000_0000, 0x3ff0_0000_0000_0000),
        }
    }

    #[test]
    fn all_seven_operations_preserve_their_zero_or_one_anchors_in_s_and_d() {
        for format in [FpFormat::S, FpFormat::D] {
            let (negative_zero, one) = zero_and_one(format);
            for operation in [
                TransOperation::Sine,
                TransOperation::Tangent,
                TransOperation::ArcSine,
                TransOperation::ArcTangent,
            ] {
                assert_eq!(
                    run(operation, format, 0, negative_zero),
                    FpEffect::Commit {
                        result: FpResult::Float(negative_zero),
                        causes: FpCauses::default(),
                    }
                );
            }
            assert_eq!(
                run(TransOperation::Cosine, format, 0, negative_zero),
                FpEffect::Commit {
                    result: FpResult::Float(one),
                    causes: FpCauses::default(),
                }
            );
            assert_eq!(
                run(TransOperation::SineCosine, format, 0, negative_zero),
                FpEffect::Commit {
                    result: FpResult::FloatPair(negative_zero, one),
                    causes: FpCauses::default(),
                }
            );

            assert_eq!(
                run(TransOperation::ArcCosine, format, 0, one),
                FpEffect::Commit {
                    result: FpResult::Float(0),
                    causes: FpCauses::default(),
                }
            );
        }
    }

    #[test]
    fn pi_over_four_domain_uses_the_exact_representable_boundary() {
        let cases = [
            (FpFormat::S, 0x3f49_0fda, 0x3f49_0fdb),
            (FpFormat::D, 0x3fe9_21fb_5444_2d18, 0x3fe9_21fb_5444_2d19),
        ];
        for (format, endpoint, above) in cases {
            for operation in [
                TransOperation::Sine,
                TransOperation::Cosine,
                TransOperation::Tangent,
            ] {
                let (_, causes) = committed_float(run(operation, format, 0, endpoint));
                assert_eq!(causes, FpCauses::default());
                assert_eq!(
                    run(operation, format, 0, above),
                    FpEffect::Commit {
                        result: FpResult::Float(format.default_nan()),
                        causes: FpCauses::NV,
                    }
                );
            }

            assert!(matches!(
                run(TransOperation::SineCosine, format, 0, endpoint),
                FpEffect::Commit {
                    result: FpResult::FloatPair(_, _),
                    causes
                } if causes.is_empty()
            ));
            assert_eq!(
                run(TransOperation::SineCosine, format, 0, above),
                FpEffect::Commit {
                    result: FpResult::FloatPair(format.default_nan(), format.default_nan()),
                    causes: FpCauses::NV,
                }
            );
        }
    }

    #[test]
    fn inverse_domain_endpoints_and_infinities_follow_the_contract() {
        let cases = [
            (FpFormat::S, 0x3f80_0000, 0x3f80_0001, 0x7f80_0000),
            (
                FpFormat::D,
                0x3ff0_0000_0000_0000,
                0x3ff0_0000_0000_0001,
                0x7ff0_0000_0000_0000,
            ),
        ];
        for (format, one, above_one, infinity) in cases {
            for operation in [TransOperation::ArcSine, TransOperation::ArcCosine] {
                let (_, causes) = committed_float(run(operation, format, 0, one));
                assert_eq!(causes, FpCauses::default());
                assert_eq!(
                    run(operation, format, 0, above_one),
                    FpEffect::Commit {
                        result: FpResult::Float(format.default_nan()),
                        causes: FpCauses::NV,
                    }
                );
                assert_eq!(
                    run(operation, format, 0, infinity),
                    FpEffect::Commit {
                        result: FpResult::Float(format.default_nan()),
                        causes: FpCauses::NV,
                    }
                );
            }

            let (atan_infinity, causes) =
                committed_float(run(TransOperation::ArcTangent, format, 0, infinity));
            assert_eq!(causes, FpCauses::default());
            assert_eq!(
                atan_infinity,
                match format {
                    FpFormat::S => 0x3fc9_0fdb,
                    FpFormat::D => 0x3ff9_21fb_5444_2d18,
                }
            );
        }
    }

    #[test]
    fn infinities_and_nans_use_common_special_value_processing() {
        let cases = [
            (FpFormat::S, 0x7f80_0000, 0x7fc0_0123),
            (FpFormat::D, 0x7ff0_0000_0000_0000, 0x7ff8_0000_0000_0123),
        ];
        for (format, infinity, quiet_nan) in cases {
            for operation in [
                TransOperation::Sine,
                TransOperation::Cosine,
                TransOperation::Tangent,
            ] {
                assert_eq!(
                    run(operation, format, 0, infinity),
                    FpEffect::Commit {
                        result: FpResult::Float(format.default_nan()),
                        causes: FpCauses::NV,
                    }
                );
                assert_eq!(
                    run(operation, format, 0, quiet_nan),
                    FpEffect::Commit {
                        result: FpResult::Float(quiet_nan),
                        causes: FpCauses::default(),
                    }
                );
            }
        }
    }

    #[test]
    fn daz_dn_and_ftz_are_applied_through_the_common_engine() {
        let cases = [
            (FpFormat::S, 1, 0x7fc0_0123),
            (FpFormat::D, 1, 0x7ff8_0000_0000_0123),
        ];
        for (format, minimum_subnormal, quiet_nan) in cases {
            assert_eq!(
                run(TransOperation::Sine, format, 1 << 8, minimum_subnormal),
                FpEffect::Commit {
                    result: FpResult::Float(0),
                    causes: FpCauses::default(),
                }
            );
            assert_eq!(
                run(TransOperation::Sine, format, 1 << 9, quiet_nan),
                FpEffect::Commit {
                    result: FpResult::Float(format.default_nan()),
                    causes: FpCauses::default(),
                }
            );
            assert_eq!(
                run(TransOperation::Sine, format, 1 << 7, minimum_subnormal),
                FpEffect::Commit {
                    result: FpResult::Float(0),
                    causes: FpCauses::UF,
                }
            );
        }
    }

    #[test]
    fn exact_underflow_boundary_distinguishes_functions() {
        let cases = [
            (FpFormat::S, 0x0080_0000),
            (FpFormat::D, 0x0010_0000_0000_0000),
        ];
        for (format, minimum_normal) in cases {
            for operation in [
                TransOperation::Sine,
                TransOperation::SineCosine,
                TransOperation::ArcTangent,
            ] {
                assert_eq!(
                    run(operation, format, 0, minimum_normal).causes(),
                    FpCauses::UF
                );
            }
            for operation in [TransOperation::Tangent, TransOperation::ArcSine] {
                assert_eq!(
                    run(operation, format, 0, minimum_normal).causes(),
                    FpCauses::default()
                );
            }
        }
    }

    #[test]
    fn enabled_nv_and_uf_fault_before_single_or_pair_commit() {
        assert_eq!(
            run(
                TransOperation::Sine,
                FpFormat::S,
                FpCauses::NV.bits(),
                0x3f80_0000,
            ),
            FpEffect::Fault {
                causes: FpCauses::NV,
            }
        );
        assert_eq!(
            run(
                TransOperation::SineCosine,
                FpFormat::S,
                FpCauses::NV.bits(),
                0x3f80_0000,
            ),
            FpEffect::Fault {
                causes: FpCauses::NV,
            }
        );

        assert_eq!(
            run(TransOperation::Sine, FpFormat::D, FpCauses::UF.bits(), 1,),
            FpEffect::Fault {
                causes: FpCauses::UF,
            }
        );
        assert_eq!(
            run(
                TransOperation::SineCosine,
                FpFormat::D,
                FpCauses::UF.bits(),
                1,
            ),
            FpEffect::Fault {
                causes: FpCauses::UF,
            }
        );
    }

    #[test]
    fn rounding_mode_bits_do_not_change_any_circular_result() {
        let baseline = run(TransOperation::Sine, FpFormat::S, 0, 0x3e80_0000);
        for rounding in 1..4 {
            assert_eq!(
                run(
                    TransOperation::Sine,
                    FpFormat::S,
                    rounding << 5,
                    0x3e80_0000,
                ),
                baseline
            );
        }
    }
}
