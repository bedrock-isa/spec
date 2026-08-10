//! Deterministic FPTRANSA hyperbolic domain evaluators.

use fpmath::{SoftF32, SoftF64};

use crate::fpu::{
    effect::{FpEffect, FpRequest},
    env::FpCauses,
    format::{FpClass, FpFormat},
    trans::{
        TransOutput, TransPrepared,
        contracts::{TransDomain, TransOperation},
        finish, prepare,
    },
};

/// Executes one hyperbolic FPTRANSA operation without architectural state access.
pub fn execute(operation: TransOperation, request: FpRequest<'_>) -> FpEffect {
    match operation {
        TransOperation::HyperbolicSine
        | TransOperation::HyperbolicCosine
        | TransOperation::HyperbolicTangent
        | TransOperation::HyperbolicArcTangent => {}
        _ => panic!("non-hyperbolic operation passed to the hyperbolic evaluator"),
    }

    let (domain, input) = match prepare(operation, request) {
        TransPrepared::Complete(effect) => return effect,
        TransPrepared::Evaluate { contract, input } => (contract.domain, input),
    };
    let (output, causes) = evaluate_prepared(operation, domain, request.format, input);
    finish(operation, request, output, causes)
}

fn evaluate_prepared(
    operation: TransOperation,
    domain: TransDomain,
    format: FpFormat,
    input: u64,
) -> (TransOutput, FpCauses) {
    if !domain_contains(domain, format, input) {
        return (TransOutput::DefaultNan, FpCauses::default());
    }

    let output = TransOutput::Approximation(match format {
        FpFormat::S => evaluate_s(operation, input as u32) as u64,
        FpFormat::D => evaluate_d(operation, input),
    });
    let result = match output {
        TransOutput::Approximation(result) => result,
        _ => unreachable!(),
    };

    let mut causes = FpCauses::default();
    if matches!(
        operation,
        TransOperation::HyperbolicSine | TransOperation::HyperbolicCosine
    ) && format.classify(input) != FpClass::Infinity
        && format.classify(result) == FpClass::Infinity
    {
        causes = causes.union(FpCauses::OF);
    }
    if operation == TransOperation::HyperbolicArcTangent
        && magnitude(format, input) == positive_one(format)
    {
        causes = causes.union(FpCauses::DZ);
    }
    if exact_result_is_tiny(operation, format, input) {
        causes = causes.union(FpCauses::UF);
    }

    (output, causes)
}

fn domain_contains(domain: TransDomain, format: FpFormat, input: u64) -> bool {
    match domain {
        TransDomain::FiniteOrSignedInfinity => true,
        TransDomain::FiniteAbsLeOne => magnitude(format, input) <= positive_one(format),
        TransDomain::FiniteAbsLePiOverFour
        | TransDomain::PositiveOrPositiveInfinityZeroDz
        | TransDomain::FiniteGeMinusOneOrPositiveInfinityMinusOneDz => {
            unreachable!("non-hyperbolic domain passed to the hyperbolic evaluator")
        }
    }
}

fn evaluate_s(operation: TransOperation, input: u32) -> u32 {
    let input = SoftF32::from_bits(input);
    match operation {
        TransOperation::HyperbolicSine => fpmath::sinh(input),
        TransOperation::HyperbolicCosine => fpmath::cosh(input),
        TransOperation::HyperbolicTangent => fpmath::tanh(input),
        TransOperation::HyperbolicArcTangent => fpmath::atanh(input),
        _ => unreachable!(),
    }
    .to_bits()
}

fn evaluate_d(operation: TransOperation, input: u64) -> u64 {
    let input = SoftF64::from_bits(input);
    match operation {
        TransOperation::HyperbolicSine => fpmath::sinh(input),
        TransOperation::HyperbolicCosine => fpmath::cosh(input),
        TransOperation::HyperbolicTangent => fpmath::tanh(input),
        TransOperation::HyperbolicArcTangent => fpmath::atanh(input),
        _ => unreachable!(),
    }
    .to_bits()
}

fn exact_result_is_tiny(operation: TransOperation, format: FpFormat, input: u64) -> bool {
    let magnitude = magnitude(format, input);
    if magnitude == 0 {
        return false;
    }
    match operation {
        TransOperation::HyperbolicSine | TransOperation::HyperbolicArcTangent => {
            magnitude < minimum_normal(format)
        }
        TransOperation::HyperbolicTangent => magnitude <= minimum_normal(format),
        TransOperation::HyperbolicCosine => false,
        _ => unreachable!(),
    }
}

fn magnitude(format: FpFormat, bits: u64) -> u64 {
    format.canonical_bits(bits) & !format.sign_mask()
}

fn positive_one(format: FpFormat) -> u64 {
    match format {
        FpFormat::S => 0x3f80_0000,
        FpFormat::D => 0x3ff0_0000_0000_0000,
    }
}

fn minimum_normal(format: FpFormat) -> u64 {
    match format {
        FpFormat::S => 0x0080_0000,
        FpFormat::D => 0x0010_0000_0000_0000,
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

    #[derive(Clone, Copy)]
    struct FormatValues {
        format: FpFormat,
        negative_zero: u64,
        one: u64,
        infinity: u64,
        minimum_normal: u64,
        overflow_input: u64,
        half: u64,
    }

    const FORMATS: [FormatValues; 2] = [
        FormatValues {
            format: FpFormat::S,
            negative_zero: 0x8000_0000,
            one: 0x3f80_0000,
            infinity: 0x7f80_0000,
            minimum_normal: 0x0080_0000,
            overflow_input: 0x42b4_0000,
            half: 0x3f00_0000,
        },
        FormatValues {
            format: FpFormat::D,
            negative_zero: 0x8000_0000_0000_0000,
            one: 0x3ff0_0000_0000_0000,
            infinity: 0x7ff0_0000_0000_0000,
            minimum_normal: 0x0010_0000_0000_0000,
            overflow_input: 0x4086_3800_0000_0000,
            half: 0x3fe0_0000_0000_0000,
        },
    ];

    fn run(operation: TransOperation, values: FormatValues, status: u16, operand: u64) -> FpEffect {
        let operands = [operand];
        execute(
            operation,
            FpRequest {
                format: values.format,
                status: FpStatus::decode(status).unwrap(),
                operands: &operands,
            },
        )
    }

    fn commit(value: u64, causes: FpCauses) -> FpEffect {
        FpEffect::Commit {
            result: FpResult::Float(value),
            causes,
        }
    }

    #[test]
    fn exact_zero_and_infinity_anchors_hold_in_both_formats() {
        for values in FORMATS {
            let negative_infinity = values.infinity | values.negative_zero;
            let negative_one = values.one | values.negative_zero;

            for zero in [0, values.negative_zero] {
                assert_eq!(
                    run(TransOperation::HyperbolicSine, values, 0, zero),
                    commit(zero, FpCauses::default())
                );
                assert_eq!(
                    run(TransOperation::HyperbolicCosine, values, 0, zero),
                    commit(values.one, FpCauses::default())
                );
                assert_eq!(
                    run(TransOperation::HyperbolicTangent, values, 0, zero),
                    commit(zero, FpCauses::default())
                );
                assert_eq!(
                    run(TransOperation::HyperbolicArcTangent, values, 0, zero),
                    commit(zero, FpCauses::default())
                );
            }

            for infinity in [values.infinity, negative_infinity] {
                assert_eq!(
                    run(TransOperation::HyperbolicSine, values, 0, infinity),
                    commit(infinity, FpCauses::default())
                );
                assert_eq!(
                    run(TransOperation::HyperbolicCosine, values, 0, infinity),
                    commit(values.infinity, FpCauses::default())
                );
            }
            assert_eq!(
                run(
                    TransOperation::HyperbolicTangent,
                    values,
                    0,
                    values.infinity
                ),
                commit(values.one, FpCauses::default())
            );
            assert_eq!(
                run(
                    TransOperation::HyperbolicTangent,
                    values,
                    0,
                    negative_infinity
                ),
                commit(negative_one, FpCauses::default())
            );
        }
    }

    #[test]
    fn atanh_endpoints_and_domain_boundaries_are_exact_in_both_formats() {
        for values in FORMATS {
            let negative_one = values.one | values.negative_zero;
            let negative_infinity = values.infinity | values.negative_zero;
            assert_eq!(
                run(TransOperation::HyperbolicArcTangent, values, 0, values.one),
                commit(values.infinity, FpCauses::DZ)
            );
            assert_eq!(
                run(
                    TransOperation::HyperbolicArcTangent,
                    values,
                    0,
                    negative_one
                ),
                commit(negative_infinity, FpCauses::DZ)
            );

            for outside in [values.one + 1, values.infinity, negative_infinity] {
                assert_eq!(
                    run(TransOperation::HyperbolicArcTangent, values, 0, outside),
                    commit(values.format.default_nan(), FpCauses::NV)
                );
            }
        }
    }

    #[test]
    fn overflow_is_distinguished_from_infinite_input_in_both_formats() {
        for values in FORMATS {
            for operation in [
                TransOperation::HyperbolicSine,
                TransOperation::HyperbolicCosine,
            ] {
                assert_eq!(
                    run(operation, values, 0, values.overflow_input),
                    commit(values.infinity, FpCauses::OF)
                );
                assert_eq!(
                    run(operation, values, 0, values.infinity),
                    commit(values.infinity, FpCauses::default())
                );
            }
        }
    }

    #[test]
    fn tiny_exact_results_daz_and_ftz_use_the_common_lead_in_both_formats() {
        for values in FORMATS {
            for operation in [
                TransOperation::HyperbolicSine,
                TransOperation::HyperbolicTangent,
                TransOperation::HyperbolicArcTangent,
            ] {
                assert_eq!(run(operation, values, 0, 1), commit(1, FpCauses::UF));
                assert_eq!(
                    run(operation, values, 1 << 8, 1),
                    commit(0, FpCauses::default())
                );
                assert_eq!(run(operation, values, 1 << 7, 1), commit(0, FpCauses::UF));
            }
            assert_eq!(
                run(
                    TransOperation::HyperbolicTangent,
                    values,
                    0,
                    values.minimum_normal
                ),
                commit(values.minimum_normal, FpCauses::UF)
            );
            for operation in [
                TransOperation::HyperbolicSine,
                TransOperation::HyperbolicArcTangent,
            ] {
                assert_eq!(
                    run(operation, values, 0, values.minimum_normal),
                    commit(values.minimum_normal, FpCauses::default())
                );
            }
        }
    }

    #[test]
    fn dn_and_every_rounding_mode_flow_through_the_common_lead() {
        for values in FORMATS {
            let quiet_nan = values.format.default_nan() | 0x42;
            let signaling_nan = values.infinity | 1;
            for operation in [
                TransOperation::HyperbolicSine,
                TransOperation::HyperbolicCosine,
                TransOperation::HyperbolicTangent,
                TransOperation::HyperbolicArcTangent,
            ] {
                assert_eq!(
                    run(operation, values, 1 << 9, quiet_nan),
                    commit(values.format.default_nan(), FpCauses::default())
                );
                assert_eq!(
                    run(operation, values, 1 << 9, signaling_nan),
                    commit(values.format.default_nan(), FpCauses::NV)
                );
                let nearest = run(operation, values, 0, values.half);
                for rounding in 1..4 {
                    assert_eq!(run(operation, values, rounding << 5, values.half), nearest);
                }
            }
        }
    }

    #[test]
    fn enabled_causes_fault_before_a_result_can_commit() {
        for values in FORMATS {
            for (operation, operand, cause) in [
                (
                    TransOperation::HyperbolicSine,
                    values.overflow_input,
                    FpCauses::OF,
                ),
                (
                    TransOperation::HyperbolicCosine,
                    values.overflow_input,
                    FpCauses::OF,
                ),
                (TransOperation::HyperbolicTangent, 1, FpCauses::UF),
                (
                    TransOperation::HyperbolicArcTangent,
                    values.one,
                    FpCauses::DZ,
                ),
                (
                    TransOperation::HyperbolicArcTangent,
                    values.one + 1,
                    FpCauses::NV,
                ),
            ] {
                assert_eq!(
                    run(operation, values, cause.bits(), operand),
                    FpEffect::Fault { causes: cause }
                );
            }
        }
    }
}
