//! Architectural floating-point status and exception state.

use crate::fpu::format::FpFormat;

#[derive(Debug, Clone, Copy, PartialEq, Eq, Default)]
pub struct FpCauses(pub(crate) u8);

impl FpCauses {
    pub const NV: Self = Self(1);
    pub const DZ: Self = Self(2);
    pub const OF: Self = Self(4);
    pub const UF: Self = Self(8);
    pub const NX: Self = Self(16);
    pub const ALL: Self = Self(31);
    pub const fn from_bits(bits: u16) -> Result<Self, FpStateError> {
        if bits & !(Self::ALL.0 as u16) != 0 {
            Err(FpStateError::ReservedFflags(bits))
        } else {
            Ok(Self(bits as u8))
        }
    }
    pub const fn bits(self) -> u16 {
        self.0 as u16
    }
    pub const fn is_empty(self) -> bool {
        self.0 == 0
    }
    pub const fn union(self, other: Self) -> Self {
        Self(self.0 | other.0)
    }
    pub fn from_apfloat(status: rustc_apfloat::Status) -> Self {
        let mut causes = Self::default();
        if status.contains(rustc_apfloat::Status::INVALID_OP) {
            causes = causes.union(Self::NV);
        }
        if status.contains(rustc_apfloat::Status::DIV_BY_ZERO) {
            causes = causes.union(Self::DZ);
        }
        if status.contains(rustc_apfloat::Status::OVERFLOW) {
            causes = causes.union(Self::OF);
        }
        if status.contains(rustc_apfloat::Status::UNDERFLOW) {
            causes = causes.union(Self::UF);
        }
        if status.contains(rustc_apfloat::Status::INEXACT) {
            causes = causes.union(Self::NX);
        }
        causes
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum RoundingMode {
    NearestEven,
    TowardZero,
    TowardNegative,
    TowardPositive,
}
impl RoundingMode {
    pub const fn apfloat(self) -> rustc_apfloat::Round {
        match self {
            Self::NearestEven => rustc_apfloat::Round::NearestTiesToEven,
            Self::TowardZero => rustc_apfloat::Round::TowardZero,
            Self::TowardNegative => rustc_apfloat::Round::TowardNegative,
            Self::TowardPositive => rustc_apfloat::Round::TowardPositive,
        }
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct FpStatus {
    raw: u16,
    pub rounding: RoundingMode,
    pub ftz: bool,
    pub daz: bool,
    pub default_nan: bool,
    pub enables: FpCauses,
}
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum FpStateError {
    ReservedFstatus(u16),
    ReservedFflags(u16),
}

impl FpStatus {
    pub const ARCHITECTURAL_MASK: u16 = 0x03ff;
    pub const fn decode(raw: u16) -> Result<Self, FpStateError> {
        if raw & !Self::ARCHITECTURAL_MASK != 0 {
            return Err(FpStateError::ReservedFstatus(raw));
        }
        let rounding = match (raw >> 5) & 3 {
            0 => RoundingMode::NearestEven,
            1 => RoundingMode::TowardZero,
            2 => RoundingMode::TowardNegative,
            _ => RoundingMode::TowardPositive,
        };
        Ok(Self {
            raw,
            rounding,
            ftz: raw & (1 << 7) != 0,
            daz: raw & (1 << 8) != 0,
            default_nan: raw & (1 << 9) != 0,
            enables: FpCauses((raw & 31) as u8),
        })
    }
    pub const fn raw(self) -> u16 {
        self.raw
    }
    pub const fn enabled(self, causes: FpCauses) -> FpCauses {
        FpCauses(self.enables.0 & causes.0)
    }
    pub const fn traps(self, causes: FpCauses) -> bool {
        !self.enabled(causes).is_empty()
    }
    pub const fn preprocess(self, format: FpFormat, bits: u64) -> u64 {
        if self.daz {
            format.daz(bits)
        } else {
            format.canonical_bits(bits)
        }
    }
}

#[cfg(test)]
mod tests {
    use super::{FpCauses, FpStateError, FpStatus, RoundingMode};
    use crate::fpu::format::FpFormat;
    #[test]
    fn fstatus_decodes_every_mode_and_rejects_reserved_bits() {
        assert_eq!(
            FpStatus::decode(0).unwrap().rounding,
            RoundingMode::NearestEven
        );
        assert_eq!(
            FpStatus::decode(1 << 5).unwrap().rounding,
            RoundingMode::TowardZero
        );
        assert_eq!(
            FpStatus::decode(2 << 5).unwrap().rounding,
            RoundingMode::TowardNegative
        );
        assert_eq!(
            FpStatus::decode(3 << 5).unwrap().rounding,
            RoundingMode::TowardPositive
        );
        assert_eq!(
            FpStatus::decode(1 << 10),
            Err(FpStateError::ReservedFstatus(1 << 10))
        );
    }
    #[test]
    fn fflags_and_enable_bits_share_the_architectural_cause_mapping() {
        assert_eq!(
            FpCauses::from_bits(0x20),
            Err(FpStateError::ReservedFflags(0x20))
        );
        let status = FpStatus::decode(FpCauses::NV.bits() | FpCauses::NX.bits()).unwrap();
        assert!(status.traps(FpCauses::NV));
        assert!(!status.traps(FpCauses::DZ));
        assert_eq!(
            status.enabled(FpCauses::NV.union(FpCauses::DZ)),
            FpCauses::NV
        );
    }
    #[test]
    fn daz_only_changes_subnormal_inputs() {
        let status = FpStatus::decode(1 << 8).unwrap();
        assert_eq!(status.preprocess(FpFormat::D, 1), 0);
        assert_eq!(status.preprocess(FpFormat::S, 0x3f80_0000), 0x3f80_0000);
    }
}
