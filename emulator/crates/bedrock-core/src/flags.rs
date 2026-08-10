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
    }
}
