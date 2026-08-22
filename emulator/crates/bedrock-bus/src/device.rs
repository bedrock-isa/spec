use crate::error::BusResult;

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
#[repr(u8)]
pub enum AccessWidth {
    Byte = 1,
    Word = 2,
    Long = 4,
    Quad = 8,
}

impl AccessWidth {
    pub const fn bytes(self) -> u64 {
        self as u64
    }
}

pub trait Device {
    fn begin_transaction(&mut self) -> BusResult<()>;
    fn commit_transaction(&mut self);
    fn rollback_transaction(&mut self);

    /// Performs one device-visible access of exactly `width` bytes.
    fn read(&mut self, offset: u64, width: AccessWidth) -> BusResult<u64>;
    /// Performs one device-visible access of exactly `width` bytes.
    fn write(&mut self, offset: u64, width: AccessWidth, value: u64) -> BusResult<()>;

    fn read_u8(&mut self, offset: u64) -> BusResult<u8> {
        self.read(offset, AccessWidth::Byte)
            .map(|value| value as u8)
    }

    fn write_u8(&mut self, offset: u64, value: u8) -> BusResult<()> {
        self.write(offset, AccessWidth::Byte, u64::from(value))
    }

    fn tick(&mut self, _cycles: u64) {}
}
