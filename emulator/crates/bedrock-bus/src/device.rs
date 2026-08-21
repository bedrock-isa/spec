use crate::error::BusResult;

pub trait Device {
    fn begin_transaction(&mut self) -> BusResult<()>;
    fn commit_transaction(&mut self);
    fn rollback_transaction(&mut self);

    fn read_u8(&mut self, offset: u64) -> BusResult<u8>;
    fn write_u8(&mut self, offset: u64, value: u8) -> BusResult<()>;

    fn tick(&mut self, _cycles: u64) {}
}
