use bitflags::bitflags;

bitflags! {
    #[derive(Debug, Clone, Copy, PartialEq, Eq, Default)]
    pub struct Flags: u16 {
        const V = 1 << 0;
        const C = 1 << 1;
        const N = 1 << 2;
        const Z = 1 << 3;
    }
}

impl Flags {
    pub fn condition(self, condition: u8) -> bool {
        match condition & 0x0f {
            0x0 => true,
            0x1 => false,
            0x2 => self.contains(Self::Z),
            0x3 => !self.contains(Self::Z),
            0x4 => self.contains(Self::C),
            0x5 => !self.contains(Self::C),
            0x6 => self.contains(Self::N),
            0x7 => !self.contains(Self::N),
            0x8 => self.contains(Self::V),
            0x9 => !self.contains(Self::V),
            0xa => self.intersects(Self::C | Self::Z),
            0xb => !self.intersects(Self::C | Self::Z),
            0xc => self.contains(Self::N) != self.contains(Self::V),
            0xd => self.contains(Self::N) == self.contains(Self::V),
            0xe => self.contains(Self::Z) || self.contains(Self::N) != self.contains(Self::V),
            _ => !self.contains(Self::Z) && self.contains(Self::N) == self.contains(Self::V),
        }
    }
}

bitflags! {
    #[derive(Debug, Clone, Copy, PartialEq, Eq, Default)]
    pub struct Status: u16 {
        const EA = 1 << 0;
        const NI = 1 << 1;
        const TF = 1 << 2;
        const RF = 1 << 3;
        const PM = 1 << 4;
        const IE = 1 << 5;
        const EDEPTH0 = 1 << 6;
        const EDEPTH1 = 1 << 7;
        const EDEPTH2 = 1 << 8;
        const EDEPTH3 = 1 << 9;
        const UO = 1 << 10;
    }
}

impl Status {
    pub const EDEPTH_MASK: u16 = 0x03c0;
    pub const HARDWARE_MANAGED_MASK: u16 =
        Self::EA.bits() | Self::PM.bits() | Self::EDEPTH_MASK | Self::UO.bits();

    pub const fn event_depth(self) -> u8 {
        ((self.bits() & Self::EDEPTH_MASK) >> 6) as u8
    }

    pub fn with_event_state(self, depth: u8, user_origin: bool) -> Self {
        let mut raw = (self.bits() & !Self::EDEPTH_MASK) | (u16::from(depth & 0x0f) << 6);
        if user_origin {
            raw |= Self::UO.bits();
        } else {
            raw &= !Self::UO.bits();
        }
        Self::from_bits_retain(raw)
    }
}
