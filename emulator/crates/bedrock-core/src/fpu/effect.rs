//! Pure floating-point operation requests and commit decisions.

use crate::fpu::{
    env::{FpCauses, FpStatus},
    format::{FpClass, FpFormat},
};

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct FpRequest<'a> {
    pub format: FpFormat,
    pub status: FpStatus,
    /// Source operands in ISA-defined source order.
    pub operands: &'a [u64],
}

impl<'a> FpRequest<'a> {
    pub fn preprocessed_operands(&self) -> impl Iterator<Item = u64> + '_ {
        self.operands
            .iter()
            .copied()
            .map(|bits| self.status.preprocess(self.format, bits))
    }
    pub fn selected_nan(&self) -> Option<u64> {
        self.format.select_nan(self.operands)
    }
    pub fn signaling_nan_cause(&self) -> FpCauses {
        if self
            .operands
            .iter()
            .any(|&bits| self.format.classify(bits) == FpClass::SignalingNan)
        {
            FpCauses::NV
        } else {
            FpCauses::default()
        }
    }
}

/// A result image owned by CPU integration, not a register update.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum FpResult {
    None,
    Float(u64),
    FloatPair(u64, u64),
    Integer(u64),
}

/// The pure result of common post-processing and enabled-cause decision.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum FpEffect {
    Commit { result: FpResult, causes: FpCauses },
    Fault { causes: FpCauses },
}

impl FpEffect {
    pub const fn causes(self) -> FpCauses {
        match self {
            Self::Commit { causes, .. } | Self::Fault { causes } => causes,
        }
    }
    pub const fn should_commit(self) -> bool {
        matches!(self, Self::Commit { .. })
    }

    pub const fn with_causes(self, status: FpStatus, additional: FpCauses) -> Self {
        let causes = self.causes().union(additional);
        match self {
            Self::Commit { result, .. } if !status.traps(causes) => Self::Commit { result, causes },
            Self::Commit { .. } | Self::Fault { .. } => Self::Fault { causes },
        }
    }
}

/// Applies DN and FTZ to an already rounded result, then makes the required pre-commit enabled-exception decision.
pub fn finish_float(request: FpRequest<'_>, rounded: u64, mut causes: FpCauses) -> FpEffect {
    let format = request.format;
    let mut result = format.canonical_bits(rounded);
    if format.is_nan(result) && request.status.default_nan {
        result = format.default_nan();
    }
    if request.status.ftz && format.is_subnormal(result) {
        result = format.signed_zero(format.sign(result));
        causes = causes.union(FpCauses::UF).union(FpCauses::NX);
    }
    finish_result(request.status, FpResult::Float(result), causes)
}

/// Makes the same enabled-exception decision for integer or multi-result instructions after instruction-specific rules.
pub const fn finish_result(status: FpStatus, result: FpResult, causes: FpCauses) -> FpEffect {
    if status.traps(causes) {
        FpEffect::Fault { causes }
    } else {
        FpEffect::Commit { result, causes }
    }
}

#[cfg(test)]
mod tests {
    use super::{FpEffect, FpRequest, FpResult, finish_float, finish_result};
    use crate::fpu::{
        env::{FpCauses, FpStatus},
        format::FpFormat,
    };
    #[test]
    fn dn_replaces_a_selected_nan_only_after_selection() {
        let request = FpRequest {
            format: FpFormat::S,
            status: FpStatus::decode(1 << 9).unwrap(),
            operands: &[0x7f80_0123],
        };
        assert_eq!(request.selected_nan(), Some(0x7fc0_0123));
        assert_eq!(
            finish_float(request, request.selected_nan().unwrap(), FpCauses::NV),
            FpEffect::Commit {
                result: FpResult::Float(0x7fc0_0000),
                causes: FpCauses::NV
            }
        );
    }
    #[test]
    fn ftz_adds_underflow_and_inexact_and_preserves_sign() {
        let request = FpRequest {
            format: FpFormat::D,
            status: FpStatus::decode(1 << 7).unwrap(),
            operands: &[],
        };
        assert_eq!(
            finish_float(request, 0x8000_0000_0000_0001, FpCauses::default()),
            FpEffect::Commit {
                result: FpResult::Float(0x8000_0000_0000_0000),
                causes: FpCauses::UF.union(FpCauses::NX)
            }
        );
    }
    #[test]
    fn an_enabled_cause_faults_before_any_result_can_commit() {
        let request = FpRequest {
            format: FpFormat::S,
            status: FpStatus::decode(FpCauses::DZ.bits()).unwrap(),
            operands: &[],
        };
        assert_eq!(
            finish_float(request, 0x7f80_0000, FpCauses::DZ),
            FpEffect::Fault {
                causes: FpCauses::DZ
            }
        );
        assert_eq!(
            finish_result(request.status, FpResult::Integer(7), FpCauses::DZ),
            FpEffect::Fault {
                causes: FpCauses::DZ
            }
        );
    }
}
