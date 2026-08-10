//! Pure base floating-point arithmetic operations.

use core::cmp::Ordering;

use rustc_apfloat::{
    Float, FloatConvert, Round, StatusAnd,
    ieee::{Double, Quad, Single},
};

use crate::fpu::{
    effect::{FpEffect, FpRequest, finish_float},
    env::{FpCauses, RoundingMode},
    format::{FpClass, FpFormat},
};

#[derive(Clone, Copy)]
enum BinaryOperation {
    Add,
    Subtract,
    Multiply,
    Divide,
}

#[derive(Clone, Copy)]
enum FusedOperation {
    MultiplyAdd,
    MultiplySubtract,
    NegatedMultiplyAdd,
    NegatedMultiplySubtract,
}

#[derive(Clone, Copy)]
enum Extremum {
    Minimum,
    Maximum,
}

#[derive(Clone, Copy)]
enum RemainderOperation {
    Modulo,
    Remainder,
}

/// Adds `dst + src`. Operands are `[src, dst]` in ISA source order.
pub fn add(request: FpRequest<'_>) -> FpEffect {
    binary(request, BinaryOperation::Add)
}

/// Subtracts `dst - src`. Operands are `[src, dst]` in ISA source order.
pub fn subtract(request: FpRequest<'_>) -> FpEffect {
    binary(request, BinaryOperation::Subtract)
}

/// Multiplies `dst * src`. Operands are `[src, dst]` in ISA source order.
pub fn multiply(request: FpRequest<'_>) -> FpEffect {
    binary(request, BinaryOperation::Multiply)
}

/// Divides `dst / src`. Operands are `[src, dst]` in ISA source order.
pub fn divide(request: FpRequest<'_>) -> FpEffect {
    binary(request, BinaryOperation::Divide)
}

/// Computes `lhs * rhs + dst` with one final rounding.
/// Operands are `[lhs, rhs, dst]` in ISA source order.
pub fn fused_multiply_add(request: FpRequest<'_>) -> FpEffect {
    fused(request, FusedOperation::MultiplyAdd)
}

/// Computes `lhs * rhs - dst` with one final rounding.
/// Operands are `[lhs, rhs, dst]` in ISA source order.
pub fn fused_multiply_subtract(request: FpRequest<'_>) -> FpEffect {
    fused(request, FusedOperation::MultiplySubtract)
}

/// Computes `-(lhs * rhs + dst)` with one final rounding.
/// Operands are `[lhs, rhs, dst]` in ISA source order.
pub fn fused_negated_multiply_add(request: FpRequest<'_>) -> FpEffect {
    fused(request, FusedOperation::NegatedMultiplyAdd)
}

/// Computes `-(lhs * rhs - dst)` with one final rounding.
/// Operands are `[lhs, rhs, dst]` in ISA source order.
pub fn fused_negated_multiply_subtract(request: FpRequest<'_>) -> FpEffect {
    fused(request, FusedOperation::NegatedMultiplySubtract)
}

/// Computes the square root. The sole operand is `[src]`.
pub fn square_root(request: FpRequest<'_>) -> FpEffect {
    let [src] = preprocessed(request);
    if let Some(nan) = request.selected_nan() {
        return finish_float(request, nan, request.signaling_nan_cause());
    }

    match request.format.classify(src) {
        FpClass::Zero => finish_float(request, src, FpCauses::default()),
        FpClass::Infinity if !request.format.sign(src) => {
            finish_float(request, src, FpCauses::default())
        }
        _ if request.format.sign(src) => {
            finish_float(request, request.format.default_nan(), FpCauses::NV)
        }
        FpClass::Normal | FpClass::Subnormal => match request.format {
            FpFormat::S => square_root_apfloat::<Single>(
                request,
                src,
                fpmath::sqrt(fpmath::SoftF32::from_bits(src as u32)).to_bits() as u64,
            ),
            FpFormat::D => square_root_apfloat::<Double>(
                request,
                src,
                fpmath::sqrt(fpmath::SoftF64::from_bits(src)).to_bits(),
            ),
        },
        FpClass::Infinity | FpClass::QuietNan | FpClass::SignalingNan => unreachable!(),
    }
}

/// Selects the numeric minimum. Operands are `[src, dst]` in ISA source order.
pub fn minimum(request: FpRequest<'_>) -> FpEffect {
    extremum(request, Extremum::Minimum)
}

/// Selects the numeric maximum. Operands are `[src, dst]` in ISA source order.
pub fn maximum(request: FpRequest<'_>) -> FpEffect {
    extremum(request, Extremum::Maximum)
}

/// Computes `dst - trunc(dst / src) * src` exactly. Operands are `[src, dst]`.
pub fn modulo(request: FpRequest<'_>) -> FpEffect {
    remainder(request, RemainderOperation::Modulo)
}

/// Computes the IEEE remainder of `dst / src`. Operands are `[src, dst]`.
pub fn ieee_remainder(request: FpRequest<'_>) -> FpEffect {
    remainder(request, RemainderOperation::Remainder)
}

/// Computes `dst * 2^k`, where `k` is `src` rounded under `FSTATUS.RM`.
/// Operands are `[src, dst]` in ISA source order.
pub fn scale(request: FpRequest<'_>) -> FpEffect {
    let operands = preprocessed::<2>(request);
    if let Some(nan) = request.selected_nan() {
        return finish_float(request, nan, request.signaling_nan_cause());
    }

    match request.format {
        FpFormat::S => scale_apfloat::<Single>(request, operands),
        FpFormat::D => scale_apfloat::<Double>(request, operands),
    }
}

fn preprocessed<const N: usize>(request: FpRequest<'_>) -> [u64; N] {
    assert_eq!(
        request.operands.len(),
        N,
        "base floating-point operation received the wrong operand count"
    );
    core::array::from_fn(|index| {
        request
            .status
            .preprocess(request.format, request.operands[index])
    })
}

fn binary(request: FpRequest<'_>, operation: BinaryOperation) -> FpEffect {
    let operands = preprocessed::<2>(request);
    match request.format {
        FpFormat::S => binary_apfloat::<Single>(request, operands, operation),
        FpFormat::D => binary_apfloat::<Double>(request, operands, operation),
    }
}

fn binary_apfloat<F: Float>(
    request: FpRequest<'_>,
    [src, dst]: [u64; 2],
    operation: BinaryOperation,
) -> FpEffect {
    let src = F::from_bits(src as u128);
    let dst = F::from_bits(dst as u128);
    let round = request.status.rounding.apfloat();
    let computed = match operation {
        BinaryOperation::Add => dst.add_r(src, round),
        BinaryOperation::Subtract => dst.sub_r(src, round),
        BinaryOperation::Multiply => dst.mul_r(src, round),
        BinaryOperation::Divide => dst.div_r(src, round),
    };
    finish_apfloat(request, computed)
}

fn fused(request: FpRequest<'_>, operation: FusedOperation) -> FpEffect {
    let operands = preprocessed::<3>(request);
    match request.format {
        FpFormat::S => fused_apfloat::<Single>(request, operands, operation),
        FpFormat::D => fused_apfloat::<Double>(request, operands, operation),
    }
}

fn fused_apfloat<F: Float>(
    request: FpRequest<'_>,
    [lhs, rhs, dst]: [u64; 3],
    operation: FusedOperation,
) -> FpEffect {
    let lhs = F::from_bits(lhs as u128);
    let rhs = F::from_bits(rhs as u128);
    let dst = F::from_bits(dst as u128);
    let round = request.status.rounding.apfloat();
    let computed = match operation {
        FusedOperation::MultiplyAdd => lhs.mul_add_r(rhs, dst, round),
        FusedOperation::MultiplySubtract => lhs.mul_add_r(rhs, -dst, round),
        FusedOperation::NegatedMultiplyAdd => (-lhs).mul_add_r(rhs, -dst, round),
        FusedOperation::NegatedMultiplySubtract => (-lhs).mul_add_r(rhs, dst, round),
    };
    finish_apfloat(request, computed)
}

fn finish_apfloat<F: Float>(request: FpRequest<'_>, computed: StatusAnd<F>) -> FpEffect {
    let causes = request
        .signaling_nan_cause()
        .union(FpCauses::from_apfloat(computed.status));
    let rounded = if computed.value.is_nan() {
        request
            .selected_nan()
            .unwrap_or_else(|| request.format.default_nan())
    } else {
        computed.value.to_bits() as u64
    };
    finish_float(request, rounded, causes)
}

fn square_root_apfloat<F>(request: FpRequest<'_>, src: u64, nearest_bits: u64) -> FpEffect
where
    F: Float + FloatConvert<Quad>,
{
    let src = F::from_bits(src as u128);
    let nearest = F::from_bits(nearest_bits as u128);
    let src_quad = convert_exact::<F, Quad>(src);
    let nearest_quad = convert_exact::<F, Quad>(nearest);
    let square = nearest_quad
        .mul_r(nearest_quad, Round::NearestTiesToEven)
        .value;
    let relation = square
        .partial_cmp(&src_quad)
        .expect("finite square-root operands are ordered");

    let rounded = match (request.status.rounding, relation) {
        (_, Ordering::Equal) | (RoundingMode::NearestEven, _) => nearest,
        (RoundingMode::TowardPositive, Ordering::Less) => nearest.next_up().value,
        (RoundingMode::TowardPositive, Ordering::Greater) => nearest,
        (RoundingMode::TowardZero | RoundingMode::TowardNegative, Ordering::Greater) => {
            nearest.next_down().value
        }
        (RoundingMode::TowardZero | RoundingMode::TowardNegative, Ordering::Less) => nearest,
    };
    let causes = if relation == Ordering::Equal {
        FpCauses::default()
    } else {
        FpCauses::NX
    };
    finish_float(request, rounded.to_bits() as u64, causes)
}

fn extremum(request: FpRequest<'_>, operation: Extremum) -> FpEffect {
    let [src, dst] = preprocessed(request);
    let src_nan = request.format.is_nan(src);
    let dst_nan = request.format.is_nan(dst);
    let rounded = match (src_nan, dst_nan) {
        (true, true) => request
            .selected_nan()
            .expect("two NaN operands have a selected NaN"),
        (true, false) => dst,
        (false, true) => src,
        (false, false)
            if request.format.classify(src) == FpClass::Zero
                && request.format.classify(dst) == FpClass::Zero =>
        {
            request.format.signed_zero(match operation {
                Extremum::Minimum => request.format.sign(src) || request.format.sign(dst),
                Extremum::Maximum => request.format.sign(src) && request.format.sign(dst),
            })
        }
        (false, false) => {
            let src_less = numeric_less(request.format, src, dst);
            match operation {
                Extremum::Minimum if src_less => src,
                Extremum::Maximum if !src_less => src,
                _ => dst,
            }
        }
    };
    finish_float(request, rounded, request.signaling_nan_cause())
}

fn numeric_less(format: FpFormat, lhs: u64, rhs: u64) -> bool {
    let lhs = format.canonical_bits(lhs);
    let rhs = format.canonical_bits(rhs);
    match (format.sign(lhs), format.sign(rhs)) {
        (true, false) => true,
        (false, true) => false,
        (true, true) => lhs > rhs,
        (false, false) => lhs < rhs,
    }
}

fn remainder(request: FpRequest<'_>, operation: RemainderOperation) -> FpEffect {
    let operands = preprocessed::<2>(request);
    match request.format {
        FpFormat::S => remainder_apfloat::<Single>(request, operands, operation),
        FpFormat::D => remainder_apfloat::<Double>(request, operands, operation),
    }
}

fn remainder_apfloat<F: Float>(
    request: FpRequest<'_>,
    [src, dst]: [u64; 2],
    operation: RemainderOperation,
) -> FpEffect {
    let src = F::from_bits(src as u128);
    let dst = F::from_bits(dst as u128);
    let computed = match operation {
        RemainderOperation::Modulo => dst.c_fmod(src),
        RemainderOperation::Remainder => dst.ieee_rem(src),
    };
    finish_apfloat(request, computed)
}

fn scale_apfloat<F>(request: FpRequest<'_>, [src, dst]: [u64; 2]) -> FpEffect
where
    F: Float + FloatConvert<Quad>,
    Quad: FloatConvert<F>,
{
    let round = request.status.rounding.apfloat();
    let src = F::from_bits(src as u128);
    let dst = F::from_bits(dst as u128);
    let integral = src.round_to_integral(round);
    let mut causes = FpCauses::from_apfloat(integral.status);

    if dst.is_zero() || dst.is_infinite() {
        return finish_float(request, dst.to_bits() as u64, causes);
    }

    let mut exact = false;
    let exponent = integral
        .value
        .to_i128_r(128, Round::TowardZero, &mut exact)
        .value;
    // This range is beyond every binary32/binary64 overflow and underflow
    // boundary while remaining exactly representable in binary128.
    let exponent = exponent.clamp(-4096, 4096) as i32;
    let scaled = convert_exact::<F, Quad>(dst).scalbn_r(exponent, Round::NearestTiesToEven);
    let mut loses_info = false;
    let converted: StatusAnd<F> = scaled.convert_r(round, &mut loses_info);
    causes = causes.union(FpCauses::from_apfloat(converted.status));
    finish_float(request, converted.value.to_bits() as u64, causes)
}

fn convert_exact<F, T>(value: F) -> T
where
    F: Float + FloatConvert<T>,
    T: Float,
{
    let mut loses_info = false;
    let converted: StatusAnd<T> = value.convert_r(Round::NearestTiesToEven, &mut loses_info);
    debug_assert!(converted.status.is_empty());
    debug_assert!(!loses_info);
    converted.value
}

#[cfg(test)]
mod tests {
    use super::{
        add, divide, fused_multiply_add, fused_multiply_subtract, fused_negated_multiply_add,
        fused_negated_multiply_subtract, ieee_remainder, maximum, minimum, modulo, multiply, scale,
        square_root, subtract,
    };
    use crate::fpu::{
        effect::{FpEffect, FpRequest, FpResult},
        env::{FpCauses, FpStatus},
        format::FpFormat,
    };

    fn request<'a>(format: FpFormat, status: u16, operands: &'a [u64]) -> FpRequest<'a> {
        FpRequest {
            format,
            status: FpStatus::decode(status).unwrap(),
            operands,
        }
    }

    fn committed_float(effect: FpEffect) -> (u64, FpCauses) {
        match effect {
            FpEffect::Commit {
                result: FpResult::Float(bits),
                causes,
            } => (bits, causes),
            other => panic!("expected committed float, got {other:?}"),
        }
    }

    #[test]
    fn add_obeys_rounding_and_binary_operand_order() {
        let operands = [0x3380_0000, 0x3f80_0000];
        assert_eq!(
            committed_float(add(request(FpFormat::S, 0, &operands))),
            (0x3f80_0000, FpCauses::NX)
        );
        assert_eq!(
            committed_float(add(request(FpFormat::S, 3 << 5, &operands))),
            (0x3f80_0001, FpCauses::NX)
        );

        let operands = [0x3ff0_0000_0000_0000, 0x4008_0000_0000_0000];
        assert_eq!(
            committed_float(subtract(request(FpFormat::D, 0, &operands))),
            (0x4000_0000_0000_0000, FpCauses::default())
        );
    }

    #[test]
    fn nan_selection_prefers_the_first_signaling_nan() {
        let operands = [0x7fc0_0123, 0xff80_0456];
        assert_eq!(
            committed_float(add(request(FpFormat::S, 0, &operands))),
            (0xffc0_0456, FpCauses::NV)
        );
        assert_eq!(
            committed_float(add(request(FpFormat::S, 1 << 9, &operands))),
            (0x7fc0_0000, FpCauses::NV)
        );
    }

    #[test]
    fn invalid_infinity_and_zero_cases_use_the_default_nan() {
        let operands = [0x7f80_0000, 0xff80_0000];
        assert_eq!(
            committed_float(add(request(FpFormat::S, 0, &operands))),
            (0x7fc0_0000, FpCauses::NV)
        );

        let operands = [0, 0];
        assert_eq!(
            committed_float(divide(request(FpFormat::S, 0, &operands))),
            (0x7fc0_0000, FpCauses::NV)
        );
    }

    #[test]
    fn divide_by_zero_faults_before_commit_when_enabled() {
        let operands = [0, 0x3f80_0000];
        assert_eq!(
            divide(request(FpFormat::S, 0, &operands)),
            FpEffect::Commit {
                result: FpResult::Float(0x7f80_0000),
                causes: FpCauses::DZ,
            }
        );
        assert_eq!(
            divide(request(FpFormat::S, FpCauses::DZ.bits(), &operands)),
            FpEffect::Fault {
                causes: FpCauses::DZ,
            }
        );
    }

    #[test]
    fn arithmetic_reports_overflow_underflow_and_inexact() {
        let overflow = [0x4000_0000, 0x7f7f_ffff];
        assert_eq!(
            committed_float(multiply(request(FpFormat::S, 0, &overflow))),
            (0x7f80_0000, FpCauses::OF.union(FpCauses::NX))
        );

        let underflow = [0x4000_0000, 1];
        assert_eq!(
            committed_float(divide(request(FpFormat::S, 0, &underflow))),
            (0, FpCauses::UF.union(FpCauses::NX))
        );
    }

    #[test]
    fn daz_and_ftz_apply_at_the_common_boundaries() {
        let daz = [1, 0];
        assert_eq!(
            committed_float(add(request(FpFormat::S, 1 << 8, &daz))),
            (0, FpCauses::default())
        );

        let ftz = [0x3f00_0000, 0x0080_0000];
        assert_eq!(
            committed_float(multiply(request(FpFormat::S, 1 << 7, &ftz))),
            (0, FpCauses::UF.union(FpCauses::NX))
        );
    }

    #[test]
    fn fused_operations_round_only_the_complete_expression() {
        let cancellation = [0x3f80_0001, 0x3f7f_fffe, 0xbf80_0000];
        assert_eq!(
            committed_float(fused_multiply_add(request(FpFormat::S, 0, &cancellation))),
            (0xa880_0000, FpCauses::default())
        );

        let operands = [0x4000_0000, 0x4040_0000, 0x4080_0000];
        assert_eq!(
            committed_float(fused_multiply_add(request(FpFormat::S, 0, &operands))).0,
            0x4120_0000
        );
        assert_eq!(
            committed_float(fused_multiply_subtract(request(FpFormat::S, 0, &operands))).0,
            0x4000_0000
        );
        assert_eq!(
            committed_float(fused_negated_multiply_add(request(
                FpFormat::S,
                0,
                &operands
            )))
            .0,
            0xc120_0000
        );
        assert_eq!(
            committed_float(fused_negated_multiply_subtract(request(
                FpFormat::S,
                0,
                &operands
            )))
            .0,
            0xc000_0000
        );
    }

    #[test]
    fn square_root_adjusts_the_nearest_soft_result_for_directed_modes() {
        let operands = [0x4000_0000];
        assert_eq!(
            committed_float(square_root(request(FpFormat::S, 0, &operands))),
            (0x3fb5_04f3, FpCauses::NX)
        );
        assert_eq!(
            committed_float(square_root(request(FpFormat::S, 3 << 5, &operands))),
            (0x3fb5_04f4, FpCauses::NX)
        );

        let exact = [0x4010_0000_0000_0000];
        assert_eq!(
            committed_float(square_root(request(FpFormat::D, 0, &exact))),
            (0x4000_0000_0000_0000, FpCauses::default())
        );
    }

    #[test]
    fn square_root_preserves_negative_zero_and_invalidates_negative_values() {
        let negative_zero = [0x8000_0000];
        assert_eq!(
            committed_float(square_root(request(FpFormat::S, 0, &negative_zero))),
            (0x8000_0000, FpCauses::default())
        );
        let negative = [0xbf80_0000];
        assert_eq!(
            committed_float(square_root(request(FpFormat::S, 0, &negative))),
            (0x7fc0_0000, FpCauses::NV)
        );
    }

    #[test]
    fn minimum_and_maximum_distinguish_signed_zero() {
        let operands = [0, 0x8000_0000];
        assert_eq!(
            committed_float(minimum(request(FpFormat::S, 0, &operands))).0,
            0x8000_0000
        );
        assert_eq!(
            committed_float(maximum(request(FpFormat::S, 0, &operands))).0,
            0
        );

        let signaling_and_number = [0x7f80_0123, 0x3f80_0000];
        assert_eq!(
            committed_float(minimum(request(FpFormat::S, 0, &signaling_and_number))),
            (0x3f80_0000, FpCauses::NV)
        );
    }

    #[test]
    fn modulo_and_remainder_use_distinct_quotient_rounding() {
        let operands = [0x4080_0000, 0x40e0_0000];
        assert_eq!(
            committed_float(modulo(request(FpFormat::S, 0, &operands))),
            (0x4040_0000, FpCauses::default())
        );
        assert_eq!(
            committed_float(ieee_remainder(request(FpFormat::S, 0, &operands))),
            (0xbf80_0000, FpCauses::default())
        );

        let invalid = [0, 0x3f80_0000];
        assert_eq!(
            committed_float(modulo(request(FpFormat::S, 0, &invalid))),
            (0x7fc0_0000, FpCauses::NV)
        );
    }

    #[test]
    fn scale_rounds_its_exponent_and_handles_unbounded_scale_values() {
        let rounded = [0x3fc0_0000, 0x3f80_0000];
        assert_eq!(
            committed_float(scale(request(FpFormat::S, 0, &rounded))),
            (0x4080_0000, FpCauses::NX)
        );
        assert_eq!(
            committed_float(scale(request(FpFormat::S, 1 << 5, &rounded))),
            (0x4000_0000, FpCauses::NX)
        );

        let positive_infinity = [0x7f80_0000, 0x3f80_0000];
        assert_eq!(
            committed_float(scale(request(FpFormat::S, 0, &positive_infinity))),
            (0x7f80_0000, FpCauses::OF.union(FpCauses::NX))
        );
        let negative_infinity = [0xff80_0000, 0x3f80_0000];
        assert_eq!(
            committed_float(scale(request(FpFormat::S, 0, &negative_infinity))),
            (0, FpCauses::UF.union(FpCauses::NX))
        );
    }
}
