//! Pure approximate exponential and logarithmic FPTRANSA operations.

use fpmath::{SoftF32, SoftF64};

use crate::fpu::{
    effect::{FpEffect, FpRequest},
    env::FpCauses,
    format::{FpClass, FpFormat},
};

use super::{
    TransOutput, TransPrepared,
    contracts::{TransDomain, TransOperation},
    finish, prepare,
};

#[derive(Clone, Copy)]
enum ExpLogOperation {
    Exponential,
    ExponentialMinusOne,
    ExponentialBaseTwo,
    ExponentialBaseTen,
    NaturalLogarithm,
    NaturalLogarithmPlusOne,
    LogarithmBaseTwo,
    LogarithmBaseTen,
}

/// Executes one exponential or logarithmic FPTRANSA operation.
pub fn execute(operation: TransOperation, request: FpRequest<'_>) -> FpEffect {
    match operation {
        TransOperation::Exponential => exponential(request),
        TransOperation::ExponentialMinusOne => exponential_minus_one(request),
        TransOperation::ExponentialBaseTwo => exponential_base_two(request),
        TransOperation::ExponentialBaseTen => exponential_base_ten(request),
        TransOperation::NaturalLogarithm => natural_logarithm(request),
        TransOperation::NaturalLogarithmPlusOne => natural_logarithm_plus_one(request),
        TransOperation::LogarithmBaseTwo => logarithm_base_two(request),
        TransOperation::LogarithmBaseTen => logarithm_base_ten(request),
        _ => panic!("non-exponential/logarithmic operation passed to the evaluator"),
    }
}

/// Computes the bounded approximate `e^x` result.
fn exponential(request: FpRequest<'_>) -> FpEffect {
    evaluate(
        request,
        TransOperation::Exponential,
        ExpLogOperation::Exponential,
    )
}

/// Computes the bounded approximate `e^x - 1` result without an intermediate result.
fn exponential_minus_one(request: FpRequest<'_>) -> FpEffect {
    evaluate(
        request,
        TransOperation::ExponentialMinusOne,
        ExpLogOperation::ExponentialMinusOne,
    )
}

/// Computes the bounded approximate `2^x` result.
fn exponential_base_two(request: FpRequest<'_>) -> FpEffect {
    evaluate(
        request,
        TransOperation::ExponentialBaseTwo,
        ExpLogOperation::ExponentialBaseTwo,
    )
}

/// Computes the bounded approximate `10^x` result.
fn exponential_base_ten(request: FpRequest<'_>) -> FpEffect {
    evaluate(
        request,
        TransOperation::ExponentialBaseTen,
        ExpLogOperation::ExponentialBaseTen,
    )
}

/// Computes the bounded approximate natural logarithm.
fn natural_logarithm(request: FpRequest<'_>) -> FpEffect {
    evaluate(
        request,
        TransOperation::NaturalLogarithm,
        ExpLogOperation::NaturalLogarithm,
    )
}

/// Computes the bounded approximate `ln(1 + x)` result without an intermediate sum.
fn natural_logarithm_plus_one(request: FpRequest<'_>) -> FpEffect {
    evaluate(
        request,
        TransOperation::NaturalLogarithmPlusOne,
        ExpLogOperation::NaturalLogarithmPlusOne,
    )
}

/// Computes the bounded approximate base-two logarithm.
fn logarithm_base_two(request: FpRequest<'_>) -> FpEffect {
    evaluate(
        request,
        TransOperation::LogarithmBaseTwo,
        ExpLogOperation::LogarithmBaseTwo,
    )
}

/// Computes the bounded approximate base-ten logarithm.
fn logarithm_base_ten(request: FpRequest<'_>) -> FpEffect {
    evaluate(
        request,
        TransOperation::LogarithmBaseTen,
        ExpLogOperation::LogarithmBaseTen,
    )
}

fn evaluate(
    request: FpRequest<'_>,
    operation: TransOperation,
    exp_log_operation: ExpLogOperation,
) -> FpEffect {
    let (domain, input) = match prepare(operation, request) {
        TransPrepared::Evaluate { contract, input } => (contract.domain, input),
        TransPrepared::Complete(effect) => return effect,
    };
    let (output, causes) = evaluate_prepared(request.format, input, domain, exp_log_operation);
    finish(operation, request, output, causes)
}

fn evaluate_prepared(
    format: FpFormat,
    input: u64,
    domain: TransDomain,
    operation: ExpLogOperation,
) -> (TransOutput, FpCauses) {
    match domain {
        TransDomain::FiniteOrSignedInfinity => evaluate_exponential(format, input, operation),
        TransDomain::PositiveOrPositiveInfinityZeroDz => {
            evaluate_positive_log(format, input, operation)
        }
        TransDomain::FiniteGeMinusOneOrPositiveInfinityMinusOneDz => {
            evaluate_log_one_plus(format, input)
        }
        TransDomain::FiniteAbsLePiOverFour | TransDomain::FiniteAbsLeOne => {
            unreachable!("non-exponential/logarithmic domain passed to the evaluator")
        }
    }
}

fn evaluate_exponential(
    format: FpFormat,
    input: u64,
    operation: ExpLogOperation,
) -> (TransOutput, FpCauses) {
    let result = soft_evaluate(format, input, operation);
    let input_class = format.classify(input);
    let result_class = format.classify(result);
    let finite_input = matches!(
        input_class,
        FpClass::Zero | FpClass::Subnormal | FpClass::Normal
    );
    let exact_zero =
        matches!(operation, ExpLogOperation::ExponentialMinusOne) && input_class == FpClass::Zero;

    let mut causes = FpCauses::default();
    if finite_input && result_class == FpClass::Infinity {
        causes = causes.union(FpCauses::OF);
    }
    if finite_input
        && (result_class == FpClass::Subnormal || (result_class == FpClass::Zero && !exact_zero))
    {
        causes = causes.union(FpCauses::UF);
    }
    if matches!(operation, ExpLogOperation::ExponentialMinusOne)
        && format.sign(input)
        && (input & !format.sign_mask()) == minimum_normal(format)
    {
        causes = causes.union(FpCauses::UF);
    }
    (TransOutput::Approximation(result), causes)
}

fn evaluate_positive_log(
    format: FpFormat,
    input: u64,
    operation: ExpLogOperation,
) -> (TransOutput, FpCauses) {
    if format.classify(input) == FpClass::Zero {
        return (
            TransOutput::Approximation(negative_infinity(format)),
            FpCauses::DZ,
        );
    }
    if format.sign(input) {
        return (TransOutput::DefaultNan, FpCauses::default());
    }

    let result = soft_evaluate(format, input, operation);
    let exact_zero = input == one(format);
    (
        TransOutput::Approximation(result),
        underflow_cause(format, result, exact_zero),
    )
}

fn evaluate_log_one_plus(format: FpFormat, input: u64) -> (TransOutput, FpCauses) {
    let negative_one = one(format) | format.sign_mask();
    if input == negative_one {
        return (
            TransOutput::Approximation(negative_infinity(format)),
            FpCauses::DZ,
        );
    }
    if format.sign(input) && (input & !format.sign_mask()) > one(format) {
        return (TransOutput::DefaultNan, FpCauses::default());
    }

    let result = soft_evaluate(format, input, ExpLogOperation::NaturalLogarithmPlusOne);
    let exact_result_is_tiny_at_normal_boundary =
        !format.sign(input) && input == minimum_normal(format);
    let causes = if exact_result_is_tiny_at_normal_boundary {
        FpCauses::UF
    } else {
        underflow_cause(format, result, format.classify(input) == FpClass::Zero)
    };
    (TransOutput::Approximation(result), causes)
}

fn underflow_cause(format: FpFormat, result: u64, exact_zero: bool) -> FpCauses {
    match format.classify(result) {
        FpClass::Subnormal => FpCauses::UF,
        FpClass::Zero if !exact_zero => FpCauses::UF,
        _ => FpCauses::default(),
    }
}

fn soft_evaluate(format: FpFormat, input: u64, operation: ExpLogOperation) -> u64 {
    match format {
        FpFormat::S => {
            let input = SoftF32::from_bits(input as u32);
            let result = match operation {
                ExpLogOperation::Exponential => fpmath::exp(input),
                ExpLogOperation::ExponentialMinusOne => fpmath::exp_m1(input),
                ExpLogOperation::ExponentialBaseTwo => fpmath::exp2(input),
                ExpLogOperation::ExponentialBaseTen => fpmath::exp10(input),
                ExpLogOperation::NaturalLogarithm => fpmath::log(input),
                ExpLogOperation::NaturalLogarithmPlusOne => fpmath::log_1p(input),
                ExpLogOperation::LogarithmBaseTwo => fpmath::log2(input),
                ExpLogOperation::LogarithmBaseTen => fpmath::log10(input),
            };
            result.to_bits() as u64
        }
        FpFormat::D => {
            let input = SoftF64::from_bits(input);
            let result = match operation {
                ExpLogOperation::Exponential => fpmath::exp(input),
                ExpLogOperation::ExponentialMinusOne => fpmath::exp_m1(input),
                ExpLogOperation::ExponentialBaseTwo => fpmath::exp2(input),
                ExpLogOperation::ExponentialBaseTen => fpmath::exp10(input),
                ExpLogOperation::NaturalLogarithm => fpmath::log(input),
                ExpLogOperation::NaturalLogarithmPlusOne => fpmath::log_1p(input),
                ExpLogOperation::LogarithmBaseTwo => fpmath::log2(input),
                ExpLogOperation::LogarithmBaseTen => fpmath::log10(input),
            };
            result.to_bits()
        }
    }
}

const fn one(format: FpFormat) -> u64 {
    match format {
        FpFormat::S => 0x3f80_0000,
        FpFormat::D => 0x3ff0_0000_0000_0000,
    }
}

const fn negative_infinity(format: FpFormat) -> u64 {
    format.sign_mask() | format.exponent_mask()
}

const fn minimum_normal(format: FpFormat) -> u64 {
    match format {
        FpFormat::S => 0x0080_0000,
        FpFormat::D => 0x0010_0000_0000_0000,
    }
}

#[cfg(test)]
mod tests {
    use super::{
        execute, exponential, exponential_base_ten, exponential_base_two, exponential_minus_one,
        logarithm_base_ten, logarithm_base_two, natural_logarithm, natural_logarithm_plus_one,
    };
    use crate::fpu::{
        effect::{FpEffect, FpRequest, FpResult},
        env::{FpCauses, FpStatus},
        format::{FpClass, FpFormat},
        trans::contracts::TransOperation,
    };

    type Operation = fn(FpRequest<'_>) -> FpEffect;

    fn run(operation: Operation, format: FpFormat, input: u64, status: u16) -> FpEffect {
        let operands = [input];
        operation(FpRequest {
            format,
            status: FpStatus::decode(status).unwrap(),
            operands: &operands,
        })
    }

    fn run_public(
        operation: TransOperation,
        format: FpFormat,
        input: u64,
        status: u16,
    ) -> FpEffect {
        let operands = [input];
        execute(
            operation,
            FpRequest {
                format,
                status: FpStatus::decode(status).unwrap(),
                operands: &operands,
            },
        )
    }

    fn committed(effect: FpEffect) -> (u64, FpCauses) {
        match effect {
            FpEffect::Commit {
                result: FpResult::Float(result),
                causes,
            } => (result, causes),
            other => panic!("expected one committed floating-point result, got {other:?}"),
        }
    }

    fn constants(format: FpFormat) -> (u64, u64, u64, u64, u64, u64) {
        match format {
            FpFormat::S => (
                0x8000_0000,
                0x3f80_0000,
                0x4000_0000,
                0x42c8_0000,
                0x7f80_0000,
                0xff80_0000,
            ),
            FpFormat::D => (
                0x8000_0000_0000_0000,
                0x3ff0_0000_0000_0000,
                0x4000_0000_0000_0000,
                0x4059_0000_0000_0000,
                0x7ff0_0000_0000_0000,
                0xfff0_0000_0000_0000,
            ),
        }
    }

    #[test]
    fn all_eight_exact_anchors_hold_in_both_formats() {
        for format in [FpFormat::S, FpFormat::D] {
            let (negative_zero, one, two, hundred, _, _) = constants(format);
            let cases = [
                (TransOperation::Exponential, 0, one),
                (
                    TransOperation::ExponentialMinusOne,
                    negative_zero,
                    negative_zero,
                ),
                (TransOperation::ExponentialBaseTwo, 0, one),
                (TransOperation::ExponentialBaseTen, 0, one),
                (TransOperation::NaturalLogarithm, one, 0),
                (
                    TransOperation::NaturalLogarithmPlusOne,
                    negative_zero,
                    negative_zero,
                ),
                (TransOperation::LogarithmBaseTwo, two, one),
                (TransOperation::LogarithmBaseTen, hundred, two),
            ];
            for (operation, input, expected) in cases {
                assert_eq!(
                    committed(run_public(operation, format, input, 0)),
                    (expected, FpCauses::default())
                );
            }
        }
    }

    #[test]
    fn signed_infinities_follow_each_exponential_contract_in_both_formats() {
        for format in [FpFormat::S, FpFormat::D] {
            let (_, one, _, _, infinity, negative_infinity) = constants(format);
            for operation in [
                exponential as Operation,
                exponential_base_two,
                exponential_base_ten,
            ] {
                assert_eq!(
                    committed(run(operation, format, infinity, 0)),
                    (infinity, FpCauses::default())
                );
                assert_eq!(
                    committed(run(operation, format, negative_infinity, 0)),
                    (0, FpCauses::default())
                );
            }
            assert_eq!(
                committed(run(exponential_minus_one, format, infinity, 0)),
                (infinity, FpCauses::default())
            );
            assert_eq!(
                committed(run(exponential_minus_one, format, negative_infinity, 0)),
                (one | format.sign_mask(), FpCauses::default())
            );
        }
    }

    #[test]
    fn logarithm_zero_and_negative_boundaries_accrue_dz_or_nv() {
        for format in [FpFormat::S, FpFormat::D] {
            let (negative_zero, one, two, _, _, negative_infinity) = constants(format);
            for operation in [
                natural_logarithm as Operation,
                logarithm_base_two,
                logarithm_base_ten,
            ] {
                for zero in [0, negative_zero] {
                    assert_eq!(
                        committed(run(operation, format, zero, 0)),
                        (negative_infinity, FpCauses::DZ)
                    );
                }
                assert_eq!(
                    committed(run(operation, format, one | format.sign_mask(), 0)),
                    (format.default_nan(), FpCauses::NV)
                );
            }
            assert_eq!(
                committed(run(
                    natural_logarithm_plus_one,
                    format,
                    one | format.sign_mask(),
                    0
                )),
                (negative_infinity, FpCauses::DZ)
            );
            assert_eq!(
                committed(run(
                    natural_logarithm_plus_one,
                    format,
                    two | format.sign_mask(),
                    0
                )),
                (format.default_nan(), FpCauses::NV)
            );
        }
    }

    #[test]
    fn overflow_underflow_and_ftz_are_reported_in_both_formats() {
        let cases = [
            (
                FpFormat::S,
                0x42b2_0000,
                0xc2d0_0000,
                0x4300_0000,
                0xc2fe_0000,
            ),
            (
                FpFormat::D,
                0x4086_3000_0000_0000,
                0xc087_5000_0000_0000,
                0x4090_0000_0000_0000,
                0xc08f_f800_0000_0000,
            ),
        ];
        for (format, exp_overflow, exp_underflow, exp2_overflow, exp2_underflow) in cases {
            let (_, _, _, _, infinity, _) = constants(format);
            assert_eq!(
                committed(run(exponential, format, exp_overflow, 0)),
                (infinity, FpCauses::OF)
            );
            let (underflowed, causes) = committed(run(exponential, format, exp_underflow, 0));
            assert!(matches!(
                format.classify(underflowed),
                FpClass::Zero | FpClass::Subnormal
            ));
            assert_eq!(causes, FpCauses::UF);
            assert_eq!(
                committed(run(exponential_base_two, format, exp2_overflow, 0)),
                (infinity, FpCauses::OF)
            );
            let (subnormal, causes) =
                committed(run(exponential_base_two, format, exp2_underflow, 0));
            assert_eq!(format.classify(subnormal), FpClass::Subnormal);
            assert_eq!(causes, FpCauses::UF);
            assert_eq!(
                committed(run(exponential_base_two, format, exp2_underflow, 1 << 7)),
                (0, FpCauses::UF)
            );
        }
    }

    #[test]
    fn expm1_and_exp10_cover_tiny_and_range_boundaries_in_both_formats() {
        let cases = [
            (FpFormat::S, 0x421c_0000, 0xc218_0000),
            (FpFormat::D, 0x4073_5000_0000_0000, 0xc073_4000_0000_0000),
        ];
        for (format, overflow, underflow) in cases {
            let (_, _, _, _, infinity, _) = constants(format);
            assert_eq!(
                committed(run(exponential_minus_one, format, 1, 0)),
                (1, FpCauses::UF)
            );
            let minimum_normal = match format {
                FpFormat::S => 0x0080_0000,
                FpFormat::D => 0x0010_0000_0000_0000,
            };
            assert_eq!(
                committed(run(
                    exponential_minus_one,
                    format,
                    minimum_normal | format.sign_mask(),
                    0
                )),
                (minimum_normal | format.sign_mask(), FpCauses::UF)
            );
            assert_eq!(
                committed(run(natural_logarithm_plus_one, format, minimum_normal, 0)),
                (minimum_normal, FpCauses::UF)
            );
            assert_eq!(
                committed(run(exponential_base_ten, format, overflow, 0)),
                (infinity, FpCauses::OF)
            );
            let (tiny, causes) = committed(run(exponential_base_ten, format, underflow, 0));
            assert!(matches!(
                format.classify(tiny),
                FpClass::Zero | FpClass::Subnormal
            ));
            assert_eq!(causes, FpCauses::UF);
        }
    }

    #[test]
    fn daz_dn_rounding_modes_and_enabled_causes_flow_through_the_common_lead() {
        for format in [FpFormat::S, FpFormat::D] {
            let (negative_zero, one, _, _, _, _) = constants(format);
            assert_eq!(
                committed(run(
                    exponential_minus_one,
                    format,
                    format.sign_mask() | 1,
                    1 << 8
                )),
                (negative_zero, FpCauses::default())
            );

            let quiet_nan = format.default_nan() | 0x123;
            assert_eq!(
                committed(run(exponential, format, quiet_nan, 1 << 9)),
                (format.default_nan(), FpCauses::default())
            );

            let nearest = committed(run(exponential, format, one, 0));
            for rounding in 1..4 {
                assert_eq!(
                    committed(run(exponential, format, one, rounding << 5)),
                    nearest
                );
            }

            let overflow_input = match format {
                FpFormat::S => 0x4300_0000,
                FpFormat::D => 0x4090_0000_0000_0000,
            };
            assert_eq!(
                run(
                    exponential_base_two,
                    format,
                    overflow_input,
                    FpCauses::OF.bits()
                ),
                FpEffect::Fault {
                    causes: FpCauses::OF
                }
            );
            assert_eq!(
                run(natural_logarithm, format, 0, FpCauses::DZ.bits()),
                FpEffect::Fault {
                    causes: FpCauses::DZ
                }
            );
        }
    }
}
