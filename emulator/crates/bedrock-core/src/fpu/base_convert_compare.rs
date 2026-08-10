//! Pure base floating-point conversion, classification, and comparison operations.

use core::cmp::Ordering;

use rustc_apfloat::{
    Float, FloatConvert, Round, Status as ApStatus, StatusAnd,
    ieee::{Double, Single},
};

use crate::{
    Flags,
    fpu::{
        effect::{FpEffect, FpRequest, FpResult, finish_float, finish_result},
        env::{FpCauses, FpStatus},
        format::{FpClass, FpFormat},
    },
};

/// Selects the rounding rule used by the integral-valued instructions.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum IntegralRounding {
    Dynamic,
    NearestEven,
    TowardZero,
    TowardNegative,
    TowardPositive,
}

impl IntegralRounding {
    const fn resolve(self, status: FpStatus) -> Round {
        match self {
            Self::Dynamic => status.rounding.apfloat(),
            Self::NearestEven => Round::NearestTiesToEven,
            Self::TowardZero => Round::TowardZero,
            Self::TowardNegative => Round::TowardNegative,
            Self::TowardPositive => Round::TowardPositive,
        }
    }
}

/// The four architectural floating-point relations.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum FpRelation {
    Greater,
    Equal,
    Less,
    Unordered,
}

impl FpRelation {
    pub const fn flags(self) -> Flags {
        match self {
            Self::Greater => Flags::empty(),
            Self::Equal => Flags::Z,
            Self::Less => Flags::N.union(Flags::C),
            Self::Unordered => Flags::V,
        }
    }
}

/// Endpoint inclusion for one of the four `FBND**` instructions.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum BoundsMode {
    ExclusiveExclusive,
    ExclusiveInclusive,
    InclusiveExclusive,
    InclusiveInclusive,
}

impl BoundsMode {
    const fn low_inclusive(self) -> bool {
        matches!(self, Self::InclusiveExclusive | Self::InclusiveInclusive)
    }

    const fn high_inclusive(self) -> bool {
        matches!(self, Self::ExclusiveInclusive | Self::InclusiveInclusive)
    }
}

/// A pure integer-FLAGS result. CPU integration applies `value` only under `mask`
/// and only when `effect` commits.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct FpFlagsEffect {
    pub effect: FpEffect,
    pub mask: Flags,
    pub value: Flags,
}

pub const fn abs_bits(format: FpFormat, bits: u64) -> u64 {
    format.canonical_bits(bits) & !format.sign_mask()
}

pub const fn negate_bits(format: FpFormat, bits: u64) -> u64 {
    format.canonical_bits(bits) ^ format.sign_mask()
}

pub const fn copy_sign_bits(format: FpFormat, sign_source: u64, magnitude_source: u64) -> u64 {
    (format.canonical_bits(magnitude_source) & !format.sign_mask())
        | (format.canonical_bits(sign_source) & format.sign_mask())
}

/// Returns the complete raw register images for `FXCHG`.
pub const fn exchange_bits(lhs: u64, rhs: u64) -> (u64, u64) {
    (rhs, lhs)
}

/// Selects the complete raw source image after CPU integration evaluates the
/// encoded integer condition for `FMOVcc`.
pub const fn conditional_move_bits(take_source: bool, source: u64, destination: u64) -> u64 {
    if take_source { source } else { destination }
}

/// Implements FINT, FINTRZ, FROUND, FTRUNC, FCEIL, and FFLOOR.
pub fn round_integral(
    format: FpFormat,
    status: FpStatus,
    operand: u64,
    rounding: IntegralRounding,
) -> FpEffect {
    let operands = [operand];
    let request = FpRequest {
        format,
        status,
        operands: &operands,
    };
    if let Some(nan) = request.selected_nan() {
        return finish_float(request, nan, request.signaling_nan_cause());
    }

    let input = status.preprocess(format, operand);
    let (rounded, causes) = round_integral_bits(format, input, rounding.resolve(status));
    finish_float(request, rounded, causes)
}

/// Implements FCLASS without DAZ, NaN quieting, or an exception cause.
pub fn classify(format: FpFormat, status: FpStatus, operand: u64) -> FpEffect {
    finish_result(
        status,
        FpResult::Integer(class_bitmap(format, operand)),
        FpCauses::default(),
    )
}

pub const fn class_bitmap(format: FpFormat, operand: u64) -> u64 {
    let negative = format.sign(operand);
    let bit = match (format.classify(operand), negative) {
        (FpClass::Infinity, true) => 0,
        (FpClass::Normal, true) => 1,
        (FpClass::Subnormal, true) => 2,
        (FpClass::Zero, true) => 3,
        (FpClass::Zero, false) => 4,
        (FpClass::Subnormal, false) => 5,
        (FpClass::Normal, false) => 6,
        (FpClass::Infinity, false) => 7,
        (FpClass::SignalingNan, _) => 8,
        (FpClass::QuietNan, _) => 9,
    };
    1 << bit
}

/// Implements FGETEXP's encoded-exponent rule, including numeric results for
/// infinity and NaN source encodings.
pub fn get_exponent(format: FpFormat, status: FpStatus, operand: u64) -> FpEffect {
    let operands = [operand];
    let request = FpRequest {
        format,
        status,
        operands: &operands,
    };
    let canonical = format.canonical_bits(operand);
    let (field, bias) = match format {
        FpFormat::S => ((canonical & format.exponent_mask()) >> 23, 127_i128),
        FpFormat::D => ((canonical & format.exponent_mask()) >> 52, 1023_i128),
    };
    let exponent = if field == 0 { 1 } else { field as i128 } - bias;
    let (result, conversion_causes) =
        signed_to_float_bits(format, exponent, status.rounding.apfloat());
    let causes = request.signaling_nan_cause().union(conversion_causes);
    finish_float(request, result, causes)
}

/// Implements FGETMAN's native-format significand extraction.
pub fn get_mantissa(format: FpFormat, status: FpStatus, operand: u64) -> FpEffect {
    let operands = [operand];
    let request = FpRequest {
        format,
        status,
        operands: &operands,
    };
    if let Some(nan) = request.selected_nan() {
        return finish_float(request, nan, request.signaling_nan_cause());
    }

    let input = status.preprocess(format, operand);
    let result = if format.classify(input) == FpClass::Normal {
        let biased_one = match format {
            FpFormat::S => 0x3f80_0000,
            FpFormat::D => 0x3ff0_0000_0000_0000,
        };
        (input & !format.exponent_mask()) | biased_one
    } else {
        input
    };
    finish_float(request, result, FpCauses::default())
}

/// Implements FCMP. The architectural relation is destination compared with
/// source, matching the instruction's source,destination operand order.
pub fn compare(format: FpFormat, status: FpStatus, source: u64, destination: u64) -> FpFlagsEffect {
    let operands = [source, destination];
    let request = FpRequest {
        format,
        status,
        operands: &operands,
    };
    let relation = numeric_relation(
        format,
        status.preprocess(format, destination),
        status.preprocess(format, source),
    );
    finish_flags(
        status,
        Flags::all(),
        relation.flags(),
        request.signaling_nan_cause(),
    )
}

/// Implements FTEST by comparing the operand with positive zero.
pub fn test(format: FpFormat, status: FpStatus, operand: u64) -> FpFlagsEffect {
    let operands = [operand];
    let request = FpRequest {
        format,
        status,
        operands: &operands,
    };
    let relation = numeric_relation(format, status.preprocess(format, operand), 0);
    finish_flags(
        status,
        Flags::all(),
        relation.flags(),
        request.signaling_nan_cause(),
    )
}

/// Implements all four floating-point bounds checks. Only V is selected for
/// update; Z, N, and C remain outside the mask.
pub fn bounds(
    format: FpFormat,
    status: FpStatus,
    low: u64,
    value: u64,
    high: u64,
    mode: BoundsMode,
) -> FpFlagsEffect {
    let operands = [low, value, high];
    let request = FpRequest {
        format,
        status,
        operands: &operands,
    };
    let low = status.preprocess(format, low);
    let value = status.preprocess(format, value);
    let high = status.preprocess(format, high);

    let low_relation = numeric_relation(format, value, low);
    let high_relation = numeric_relation(format, value, high);
    let low_ok = matches!(low_relation, FpRelation::Greater)
        || mode.low_inclusive() && matches!(low_relation, FpRelation::Equal);
    let high_ok = matches!(high_relation, FpRelation::Less)
        || mode.high_inclusive() && matches!(high_relation, FpRelation::Equal);
    let out_of_bounds = !low_ok || !high_ok;
    finish_flags(
        status,
        Flags::V,
        if out_of_bounds {
            Flags::V
        } else {
            Flags::empty()
        },
        request.signaling_nan_cause(),
    )
}

/// Implements the Fn-to-Fn FCVT/FCVTU family. The destination format selects
/// the opposite source format as specified by the ISA.
pub fn convert_format(
    destination_format: FpFormat,
    status: FpStatus,
    source_bits: u64,
) -> FpEffect {
    let source_format = match destination_format {
        FpFormat::S => FpFormat::D,
        FpFormat::D => FpFormat::S,
    };
    let source = status.preprocess(source_format, source_bits);
    let (rounded, mut causes) = match destination_format {
        FpFormat::S => {
            let mut loses_info = false;
            let result: StatusAnd<Single> = Double::from_bits(source as u128)
                .convert_r(status.rounding.apfloat(), &mut loses_info);
            (
                result.value.to_bits() as u64,
                FpCauses::from_apfloat(result.status),
            )
        }
        FpFormat::D => {
            let mut loses_info = false;
            let result: StatusAnd<Double> = Single::from_bits(source as u128)
                .convert_r(status.rounding.apfloat(), &mut loses_info);
            (
                result.value.to_bits() as u64,
                FpCauses::from_apfloat(result.status),
            )
        }
    };

    // rustc_apfloat 0.2.3 reports a directed overflow rounded to the largest
    // finite Single as INEXACT only. The ISA always accrues both OF and NX.
    if destination_format == FpFormat::S
        && matches!(source_format.classify(source), FpClass::Normal)
        && source & !source_format.sign_mask() > 0x47ef_ffff_e000_0000
    {
        causes = causes.union(FpCauses::OF).union(FpCauses::NX);
    }

    let request = FpRequest {
        format: destination_format,
        status,
        operands: &[],
    };
    finish_float(request, rounded, causes)
}

pub fn signed_integer_to_float(format: FpFormat, status: FpStatus, integer_bits: u64) -> FpEffect {
    let integer = integer_bits as i64 as i128;
    let (rounded, causes) = signed_to_float_bits(format, integer, status.rounding.apfloat());
    finish_float(
        FpRequest {
            format,
            status,
            operands: &[],
        },
        rounded,
        causes,
    )
}

pub fn unsigned_integer_to_float(format: FpFormat, status: FpStatus, integer: u64) -> FpEffect {
    let result = match format {
        FpFormat::S => Single::from_u128_r(integer as u128, status.rounding.apfloat())
            .map(|value| value.to_bits() as u64),
        FpFormat::D => Double::from_u128_r(integer as u128, status.rounding.apfloat())
            .map(|value| value.to_bits() as u64),
    };
    finish_float(
        FpRequest {
            format,
            status,
            operands: &[],
        },
        result.value,
        FpCauses::from_apfloat(result.status),
    )
}

pub fn float_to_signed_integer(format: FpFormat, status: FpStatus, source_bits: u64) -> FpEffect {
    let source = status.preprocess(format, source_bits);
    let (value, ap_status) = match format {
        FpFormat::S => {
            let mut exact = true;
            let result =
                Single::from_bits(source as u128).to_i128_r(64, Round::TowardZero, &mut exact);
            (result.value as u64, result.status)
        }
        FpFormat::D => {
            let mut exact = true;
            let result =
                Double::from_bits(source as u128).to_i128_r(64, Round::TowardZero, &mut exact);
            (result.value as u64, result.status)
        }
    };
    finish_integer_conversion(status, value, ap_status)
}

pub fn float_to_unsigned_integer(format: FpFormat, status: FpStatus, source_bits: u64) -> FpEffect {
    let source = status.preprocess(format, source_bits);
    let class = format.classify(source);
    if format.sign(source)
        && !matches!(
            class,
            FpClass::Zero | FpClass::QuietNan | FpClass::SignalingNan
        )
    {
        return finish_result(status, FpResult::Integer(0), FpCauses::NV);
    }

    let (value, ap_status) = match format {
        FpFormat::S => {
            let mut exact = true;
            let result =
                Single::from_bits(source as u128).to_u128_r(64, Round::TowardZero, &mut exact);
            (result.value as u64, result.status)
        }
        FpFormat::D => {
            let mut exact = true;
            let result =
                Double::from_bits(source as u128).to_u128_r(64, Round::TowardZero, &mut exact);
            (result.value as u64, result.status)
        }
    };
    finish_integer_conversion(status, value, ap_status)
}

fn round_integral_bits(format: FpFormat, bits: u64, round: Round) -> (u64, FpCauses) {
    let result = match format {
        FpFormat::S => Single::from_bits(bits as u128)
            .round_to_integral(round)
            .map(|value| value.to_bits() as u64),
        FpFormat::D => Double::from_bits(bits as u128)
            .round_to_integral(round)
            .map(|value| value.to_bits() as u64),
    };
    (result.value, FpCauses::from_apfloat(result.status))
}

fn signed_to_float_bits(format: FpFormat, value: i128, round: Round) -> (u64, FpCauses) {
    let result = match format {
        FpFormat::S => Single::from_i128_r(value, round).map(|value| value.to_bits() as u64),
        FpFormat::D => Double::from_i128_r(value, round).map(|value| value.to_bits() as u64),
    };
    (result.value, FpCauses::from_apfloat(result.status))
}

fn numeric_relation(format: FpFormat, lhs: u64, rhs: u64) -> FpRelation {
    let ordering = match format {
        FpFormat::S => Single::from_bits(lhs as u128).partial_cmp(&Single::from_bits(rhs as u128)),
        FpFormat::D => Double::from_bits(lhs as u128).partial_cmp(&Double::from_bits(rhs as u128)),
    };
    match ordering {
        Some(Ordering::Greater) => FpRelation::Greater,
        Some(Ordering::Equal) => FpRelation::Equal,
        Some(Ordering::Less) => FpRelation::Less,
        None => FpRelation::Unordered,
    }
}

fn finish_flags(status: FpStatus, mask: Flags, value: Flags, causes: FpCauses) -> FpFlagsEffect {
    FpFlagsEffect {
        effect: finish_result(status, FpResult::None, causes),
        mask,
        value,
    }
}

fn finish_integer_conversion(status: FpStatus, value: u64, ap_status: ApStatus) -> FpEffect {
    let causes = if ap_status.contains(ApStatus::INVALID_OP) {
        FpCauses::NV
    } else {
        FpCauses::from_apfloat(ap_status)
    };
    finish_result(status, FpResult::Integer(value), causes)
}

#[cfg(test)]
mod tests {
    use super::*;

    fn status(raw: u16) -> FpStatus {
        FpStatus::decode(raw).unwrap()
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

    fn committed_integer(effect: FpEffect) -> (u64, FpCauses) {
        match effect {
            FpEffect::Commit {
                result: FpResult::Integer(value),
                causes,
            } => (value, causes),
            other => panic!("expected committed integer, got {other:?}"),
        }
    }

    #[test]
    fn sign_exchange_and_conditional_helpers_are_raw_and_deterministic() {
        assert_eq!(abs_bits(FpFormat::S, 0xffff_ffff_8000_0001), 1);
        assert_eq!(negate_bits(FpFormat::S, 0x7f80_0123), 0xff80_0123);
        assert_eq!(
            copy_sign_bits(FpFormat::D, 0x8000_0000_0000_0000, 0x3ff8_0000_0000_0000),
            0xbff8_0000_0000_0000
        );
        assert_eq!(exchange_bits(0xaaaa, 0xbbbb), (0xbbbb, 0xaaaa));
        assert_eq!(conditional_move_bits(true, 7, 9), 7);
        assert_eq!(conditional_move_bits(false, 7, 9), 9);
    }

    #[test]
    fn integral_rounding_honors_every_dynamic_and_fixed_mode() {
        let cases = [
            (0, 0x4000_0000),
            (1 << 5, 0x3f80_0000),
            (2 << 5, 0x3f80_0000),
            (3 << 5, 0x4000_0000),
        ];
        for (raw_status, expected) in cases {
            let (bits, causes) = committed_float(round_integral(
                FpFormat::S,
                status(raw_status),
                0x3fc0_0000,
                IntegralRounding::Dynamic,
            ));
            assert_eq!(bits, expected);
            assert_eq!(causes, FpCauses::NX);
        }

        assert_eq!(
            committed_float(round_integral(
                FpFormat::S,
                status(3 << 5),
                0x4020_0000,
                IntegralRounding::NearestEven,
            )),
            (0x4000_0000, FpCauses::NX)
        );
        assert_eq!(
            committed_float(round_integral(
                FpFormat::D,
                status(0),
                0xbfe8_0000_0000_0000,
                IntegralRounding::TowardPositive,
            )),
            (0x8000_0000_0000_0000, FpCauses::NX)
        );
        assert_eq!(
            committed_float(round_integral(
                FpFormat::D,
                status(0),
                0xbfe8_0000_0000_0000,
                IntegralRounding::TowardNegative,
            )),
            (0xbff0_0000_0000_0000, FpCauses::NX)
        );
    }

    #[test]
    fn integral_rounding_preserves_nan_priority_daz_and_fault_precommit() {
        assert_eq!(
            committed_float(round_integral(
                FpFormat::S,
                status(0),
                0xff80_0123,
                IntegralRounding::TowardZero,
            )),
            (0xffc0_0123, FpCauses::NV)
        );
        assert_eq!(
            round_integral(
                FpFormat::S,
                status(FpCauses::NV.bits()),
                0x7f80_0123,
                IntegralRounding::TowardZero,
            ),
            FpEffect::Fault {
                causes: FpCauses::NV
            }
        );
        assert_eq!(
            committed_float(round_integral(
                FpFormat::S,
                status(1 << 9),
                0x7f80_0123,
                IntegralRounding::TowardZero,
            )),
            (0x7fc0_0000, FpCauses::NV)
        );
        assert_eq!(
            committed_float(round_integral(
                FpFormat::S,
                status(0),
                1,
                IntegralRounding::TowardZero,
            )),
            (0, FpCauses::NX)
        );
        assert_eq!(
            committed_float(round_integral(
                FpFormat::S,
                status(1 << 8),
                1,
                IntegralRounding::TowardZero,
            )),
            (0, FpCauses::default())
        );
    }

    #[test]
    fn classification_covers_all_ten_classes_without_daz_or_exceptions() {
        let cases = [
            (0xff80_0000, 0),
            (0xbf80_0000, 1),
            (0x8000_0001, 2),
            (0x8000_0000, 3),
            (0x0000_0000, 4),
            (0x0000_0001, 5),
            (0x3f80_0000, 6),
            (0x7f80_0000, 7),
            (0xff80_0001, 8),
            (0xffc0_0001, 9),
        ];
        for (bits, class_bit) in cases {
            assert_eq!(class_bitmap(FpFormat::S, bits), 1 << class_bit);
            assert_eq!(
                committed_integer(classify(
                    FpFormat::S,
                    status(FpCauses::NV.bits() | (1 << 8)),
                    bits,
                )),
                (1 << class_bit, FpCauses::default())
            );
        }
    }

    #[test]
    fn getexp_and_getman_cover_finite_and_special_encodings() {
        assert_eq!(
            committed_float(get_exponent(FpFormat::S, status(0), 0)),
            (0xc2fc_0000, FpCauses::default())
        );
        assert_eq!(
            committed_float(get_exponent(FpFormat::S, status(0), 1)),
            (0xc2fc_0000, FpCauses::default())
        );
        assert_eq!(
            committed_float(get_exponent(FpFormat::S, status(0), 0x7fc0_0001)),
            (0x4300_0000, FpCauses::default())
        );
        assert_eq!(
            committed_float(get_exponent(FpFormat::S, status(0), 0x7f80_0001)),
            (0x4300_0000, FpCauses::NV)
        );

        assert_eq!(
            committed_float(get_mantissa(FpFormat::S, status(0), 0xc0d0_0000)),
            (0xbfd0_0000, FpCauses::default())
        );
        assert_eq!(
            committed_float(get_mantissa(FpFormat::S, status(0), 0x8000_0000)),
            (0x8000_0000, FpCauses::default())
        );
        assert_eq!(
            committed_float(get_mantissa(FpFormat::S, status(0), 0x7f80_0000)),
            (0x7f80_0000, FpCauses::default())
        );
        assert_eq!(
            committed_float(get_mantissa(FpFormat::S, status(0), 0xff80_0042)),
            (0xffc0_0042, FpCauses::NV)
        );
        assert_eq!(
            committed_float(get_mantissa(FpFormat::S, status(1 << 9), 0xffc0_0042)),
            (0x7fc0_0000, FpCauses::default())
        );
        assert_eq!(
            committed_float(get_mantissa(FpFormat::S, status(1 << 8), 0x8000_0001)),
            (0x8000_0000, FpCauses::default())
        );
        assert_eq!(
            committed_float(get_mantissa(FpFormat::S, status(1 << 7), 0x0000_0001)),
            (0, FpCauses::UF.union(FpCauses::NX))
        );
    }

    #[test]
    fn compare_and_test_encode_relations_signed_zero_unordered_and_faults() {
        let greater = compare(FpFormat::S, status(0), 0x3f80_0000, 0x4000_0000);
        assert_eq!(greater.mask, Flags::all());
        assert_eq!(greater.value, Flags::empty());
        assert!(greater.effect.should_commit());

        assert_eq!(
            compare(FpFormat::S, status(0), 0x8000_0000, 0).value,
            Flags::Z
        );
        assert_eq!(
            compare(FpFormat::S, status(0), 0x4000_0000, 0x3f80_0000).value,
            Flags::N | Flags::C
        );
        let quiet = compare(FpFormat::S, status(0), 0x7fc0_0001, 0);
        assert_eq!(quiet.value, Flags::V);
        assert_eq!(quiet.effect.causes(), FpCauses::default());
        let signaling = compare(FpFormat::S, status(FpCauses::NV.bits()), 0x7f80_0001, 0);
        assert_eq!(signaling.value, Flags::V);
        assert_eq!(
            signaling.effect,
            FpEffect::Fault {
                causes: FpCauses::NV
            }
        );
        assert_eq!(
            test(FpFormat::D, status(0), 0xbff0_0000_0000_0000).value,
            Flags::N | Flags::C
        );
        assert_eq!(test(FpFormat::S, status(1 << 8), 1).value, Flags::Z);
    }

    #[test]
    fn bounds_honor_each_endpoint_and_preserve_non_v_flags() {
        let one = 0x3f80_0000;
        let two = 0x4000_0000;
        for (mode, low_out, high_out) in [
            (BoundsMode::ExclusiveExclusive, true, true),
            (BoundsMode::ExclusiveInclusive, true, false),
            (BoundsMode::InclusiveExclusive, false, true),
            (BoundsMode::InclusiveInclusive, false, false),
        ] {
            let at_low = bounds(FpFormat::S, status(0), one, one, two, mode);
            let at_high = bounds(FpFormat::S, status(0), one, two, two, mode);
            assert_eq!(at_low.mask, Flags::V);
            assert_eq!(at_low.value.contains(Flags::V), low_out);
            assert_eq!(at_high.value.contains(Flags::V), high_out);
        }

        let unordered = bounds(
            FpFormat::S,
            status(0),
            one,
            0x7fc0_0001,
            two,
            BoundsMode::InclusiveInclusive,
        );
        assert_eq!(unordered.value, Flags::V);
        assert_eq!(unordered.effect.causes(), FpCauses::default());
        let signaling = bounds(
            FpFormat::S,
            status(FpCauses::NV.bits()),
            one,
            0x7f80_0001,
            two,
            BoundsMode::InclusiveInclusive,
        );
        assert!(!signaling.effect.should_commit());
        assert_eq!(signaling.effect.causes(), FpCauses::NV);
    }

    #[test]
    fn format_conversion_honors_rounding_overflow_underflow_nan_and_dn() {
        assert_eq!(
            committed_float(convert_format(
                FpFormat::S,
                status(0),
                0x3ff8_0000_0000_0000,
            )),
            (0x3fc0_0000, FpCauses::default())
        );
        assert_eq!(
            committed_float(convert_format(FpFormat::D, status(0), 0x3fc0_0000,)),
            (0x3ff8_0000_0000_0000, FpCauses::default())
        );
        assert_eq!(
            committed_float(convert_format(
                FpFormat::S,
                status(0),
                0x3ff0_0000_1000_0000,
            )),
            (0x3f80_0000, FpCauses::NX)
        );
        assert_eq!(
            committed_float(convert_format(
                FpFormat::S,
                status(3 << 5),
                0x3ff0_0000_1000_0000,
            )),
            (0x3f80_0001, FpCauses::NX)
        );
        assert_eq!(
            committed_float(convert_format(
                FpFormat::S,
                status(1 << 5),
                0x7fe0_0000_0000_0000,
            )),
            (0x7f7f_ffff, FpCauses::OF.union(FpCauses::NX))
        );
        let (tiny, tiny_causes) = committed_float(convert_format(FpFormat::S, status(0), 1));
        assert_eq!(tiny, 0);
        assert_eq!(tiny_causes, FpCauses::UF.union(FpCauses::NX));

        let (nan, nan_causes) = committed_float(convert_format(
            FpFormat::S,
            status(0),
            0xfff0_0000_0000_0042,
        ));
        assert_eq!(FpFormat::S.classify(nan), FpClass::QuietNan);
        assert!(FpFormat::S.sign(nan));
        assert_eq!(nan_causes, FpCauses::NV);
        assert_eq!(
            committed_float(convert_format(
                FpFormat::S,
                status(1 << 9),
                0xfff8_0000_0000_0042,
            )),
            (0x7fc0_0000, FpCauses::default())
        );
    }

    #[test]
    fn integer_to_float_covers_signed_unsigned_extrema_and_rounding() {
        assert_eq!(
            committed_float(signed_integer_to_float(
                FpFormat::S,
                status(0),
                (-1_i64) as u64,
            )),
            (0xbf80_0000, FpCauses::default())
        );
        assert_eq!(
            committed_float(unsigned_integer_to_float(FpFormat::D, status(0), u64::MAX,)),
            (0x43f0_0000_0000_0000, FpCauses::NX)
        );
        assert_eq!(
            committed_float(unsigned_integer_to_float(
                FpFormat::D,
                status(1 << 5),
                u64::MAX,
            )),
            (0x43ef_ffff_ffff_ffff, FpCauses::NX)
        );
        assert_eq!(
            committed_float(signed_integer_to_float(
                FpFormat::D,
                status(0),
                i64::MIN as u64,
            )),
            (0xc3e0_0000_0000_0000, FpCauses::default())
        );
    }

    #[test]
    fn float_to_integer_saturates_invalid_and_separates_invalid_from_inexact() {
        assert_eq!(
            committed_integer(float_to_signed_integer(FpFormat::S, status(0), 0x4070_0000,)),
            (3, FpCauses::NX)
        );
        assert_eq!(
            committed_integer(float_to_signed_integer(FpFormat::S, status(0), 0xc070_0000,)),
            ((-3_i64) as u64, FpCauses::NX)
        );
        assert_eq!(
            committed_integer(float_to_signed_integer(
                FpFormat::D,
                status(0),
                0x43e0_0000_0000_0000,
            )),
            (i64::MAX as u64, FpCauses::NV)
        );
        assert_eq!(
            committed_integer(float_to_signed_integer(
                FpFormat::D,
                status(0),
                0xc3e0_0000_0000_0000,
            )),
            (i64::MIN as u64, FpCauses::default())
        );
        assert_eq!(
            committed_integer(float_to_signed_integer(FpFormat::S, status(0), 0x7fc0_0042,)),
            (0, FpCauses::NV)
        );
        assert_eq!(
            float_to_signed_integer(FpFormat::S, status(FpCauses::NV.bits()), 0x7f80_0000,),
            FpEffect::Fault {
                causes: FpCauses::NV
            }
        );

        assert_eq!(
            committed_integer(float_to_unsigned_integer(
                FpFormat::S,
                status(0),
                0xbf00_0000,
            )),
            (0, FpCauses::NV)
        );
        assert_eq!(
            committed_integer(float_to_unsigned_integer(
                FpFormat::S,
                status(0),
                0x8000_0000,
            )),
            (0, FpCauses::default())
        );
        assert_eq!(
            committed_integer(float_to_unsigned_integer(
                FpFormat::D,
                status(0),
                0x43f0_0000_0000_0000,
            )),
            (u64::MAX, FpCauses::NV)
        );
        assert_eq!(
            committed_integer(float_to_unsigned_integer(
                FpFormat::D,
                status(0),
                0x43ef_ffff_ffff_ffff,
            )),
            (0xffff_ffff_ffff_f800, FpCauses::default())
        );
        assert_eq!(
            committed_integer(float_to_unsigned_integer(
                FpFormat::S,
                status(1 << 8),
                0x8000_0001,
            )),
            (0, FpCauses::default())
        );
        assert_eq!(
            committed_integer(float_to_unsigned_integer(
                FpFormat::S,
                status(0),
                0x8000_0001,
            )),
            (0, FpCauses::NV)
        );
    }
}
