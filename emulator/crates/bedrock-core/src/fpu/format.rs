//! Raw IEEE-754 S/D format operations.

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum FpFormat {
    S,
    D,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum FpClass {
    Zero,
    Subnormal,
    Normal,
    Infinity,
    QuietNan,
    SignalingNan,
}

impl FpFormat {
    pub const fn value_mask(self) -> u64 {
        match self {
            Self::S => u32::MAX as u64,
            Self::D => u64::MAX,
        }
    }
    pub const fn sign_mask(self) -> u64 {
        match self {
            Self::S => 1 << 31,
            Self::D => 1 << 63,
        }
    }
    pub const fn exponent_mask(self) -> u64 {
        match self {
            Self::S => 0x7f80_0000,
            Self::D => 0x7ff0_0000_0000_0000,
        }
    }
    pub const fn fraction_mask(self) -> u64 {
        match self {
            Self::S => 0x007f_ffff,
            Self::D => 0x000f_ffff_ffff_ffff,
        }
    }
    pub const fn quiet_bit(self) -> u64 {
        match self {
            Self::S => 0x0040_0000,
            Self::D => 0x0008_0000_0000_0000,
        }
    }
    pub const fn default_nan(self) -> u64 {
        match self {
            Self::S => 0x7fc0_0000,
            Self::D => 0x7ff8_0000_0000_0000,
        }
    }
    pub const fn canonical_bits(self, bits: u64) -> u64 {
        bits & self.value_mask()
    }
    pub const fn sign(self, bits: u64) -> bool {
        self.canonical_bits(bits) & self.sign_mask() != 0
    }
    pub const fn signed_zero(self, negative: bool) -> u64 {
        if negative { self.sign_mask() } else { 0 }
    }
    pub const fn classify(self, bits: u64) -> FpClass {
        let bits = self.canonical_bits(bits);
        let exponent = bits & self.exponent_mask();
        let fraction = bits & self.fraction_mask();
        if exponent == 0 {
            if fraction == 0 {
                FpClass::Zero
            } else {
                FpClass::Subnormal
            }
        } else if exponent == self.exponent_mask() {
            if fraction == 0 {
                FpClass::Infinity
            } else if fraction & self.quiet_bit() == 0 {
                FpClass::SignalingNan
            } else {
                FpClass::QuietNan
            }
        } else {
            FpClass::Normal
        }
    }
    pub const fn is_nan(self, bits: u64) -> bool {
        matches!(
            self.classify(bits),
            FpClass::QuietNan | FpClass::SignalingNan
        )
    }
    pub const fn is_subnormal(self, bits: u64) -> bool {
        matches!(self.classify(bits), FpClass::Subnormal)
    }
    pub const fn quiet_nan(self, bits: u64) -> u64 {
        self.canonical_bits(bits) | self.quiet_bit()
    }
    pub const fn daz(self, bits: u64) -> u64 {
        if self.is_subnormal(bits) {
            self.signed_zero(self.sign(bits))
        } else {
            self.canonical_bits(bits)
        }
    }
    pub fn select_nan(self, operands: &[u64]) -> Option<u64> {
        for &operand in operands {
            if self.classify(operand) == FpClass::SignalingNan {
                return Some(self.quiet_nan(operand));
            }
        }
        for &operand in operands {
            if self.classify(operand) == FpClass::QuietNan {
                return Some(self.quiet_nan(operand));
            }
        }
        None
    }
}

#[cfg(test)]
mod tests {
    use super::{FpClass, FpFormat};
    #[test]
    fn classification_uses_architectural_bits() {
        assert_eq!(FpFormat::S.classify(1), FpClass::Subnormal);
        assert_eq!(
            FpFormat::D.classify(0x7ff0_0000_0000_0001),
            FpClass::SignalingNan
        );
        assert_eq!(
            FpFormat::D.classify(0x7ff8_0000_0000_0001),
            FpClass::QuietNan
        );
    }
    #[test]
    fn daz_preserves_subnormal_sign() {
        assert_eq!(FpFormat::S.daz(0x8000_0001), 0x8000_0000);
    }
    #[test]
    fn nan_selection_is_ordered() {
        let f = FpFormat::S;
        assert_eq!(f.select_nan(&[0x7fc0_0123, 0xff80_0456]), Some(0xffc0_0456));
        assert_eq!(f.select_nan(&[0x7fc0_0123, 0x7fc0_0456]), Some(0x7fc0_0123));
    }
}
