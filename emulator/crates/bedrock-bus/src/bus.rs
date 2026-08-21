use crate::error::{BusError, BusResult};

pub trait Bus {
    fn begin_transaction(&mut self) -> BusResult<()>;
    fn commit_transaction(&mut self);
    fn rollback_transaction(&mut self);

    fn read_u8(&mut self, addr: u64) -> BusResult<u8>;
    fn write_u8(&mut self, addr: u64, value: u8) -> BusResult<()>;

    fn read_u16(&mut self, addr: u64) -> BusResult<u16> {
        checked_transfer_end(addr, 2)?;
        let mut value = 0u16;
        for byte_index in 0..2 {
            let byte_addr = checked_byte_address(addr, byte_index)?;
            value |= (self.read_u8(byte_addr)? as u16) << (byte_index * 8);
        }
        Ok(value)
    }

    fn read_u32(&mut self, addr: u64) -> BusResult<u32> {
        checked_transfer_end(addr, 4)?;
        let mut value = 0u32;
        for byte_index in 0..4 {
            let byte_addr = checked_byte_address(addr, byte_index)?;
            value |= (self.read_u8(byte_addr)? as u32) << (byte_index * 8);
        }
        Ok(value)
    }

    fn read_u64(&mut self, addr: u64) -> BusResult<u64> {
        checked_transfer_end(addr, 8)?;
        let mut value = 0u64;
        for byte_index in 0..8 {
            let byte_addr = checked_byte_address(addr, byte_index)?;
            value |= (self.read_u8(byte_addr)? as u64) << (byte_index * 8);
        }
        Ok(value)
    }

    fn write_u16(&mut self, addr: u64, value: u16) -> BusResult<()> {
        checked_transfer_end(addr, 2)?;
        for byte_index in 0..2 {
            let byte_addr = checked_byte_address(addr, byte_index)?;
            self.write_u8(byte_addr, ((value >> (byte_index * 8)) & 0xff) as u8)?;
        }
        Ok(())
    }

    fn write_u32(&mut self, addr: u64, value: u32) -> BusResult<()> {
        checked_transfer_end(addr, 4)?;
        for byte_index in 0..4 {
            let byte_addr = checked_byte_address(addr, byte_index)?;
            self.write_u8(byte_addr, ((value >> (byte_index * 8)) & 0xff) as u8)?;
        }
        Ok(())
    }

    fn write_u64(&mut self, addr: u64, value: u64) -> BusResult<()> {
        checked_transfer_end(addr, 8)?;
        for byte_index in 0..8 {
            let byte_addr = checked_byte_address(addr, byte_index)?;
            self.write_u8(byte_addr, ((value >> (byte_index * 8)) & 0xff) as u8)?;
        }
        Ok(())
    }
}

fn checked_transfer_end(addr: u64, byte_count: u64) -> BusResult<u64> {
    checked_byte_address(addr, byte_count - 1)
}

fn checked_byte_address(addr: u64, byte_index: u64) -> BusResult<u64> {
    addr.checked_add(byte_index)
        .ok_or(BusError::OutOfRange { addr })
}

#[cfg(test)]
mod tests {
    use super::Bus;
    use crate::{BusError, BusResult};

    #[derive(Default)]
    struct ByteOnlyBus {
        byte_reads: usize,
        byte_writes: usize,
    }

    impl Bus for ByteOnlyBus {
        fn begin_transaction(&mut self) -> BusResult<()> {
            Ok(())
        }

        fn commit_transaction(&mut self) {}

        fn rollback_transaction(&mut self) {}

        fn read_u8(&mut self, _addr: u64) -> BusResult<u8> {
            self.byte_reads += 1;
            Ok(0)
        }

        fn write_u8(&mut self, _addr: u64, _value: u8) -> BusResult<()> {
            self.byte_writes += 1;
            Ok(())
        }
    }

    #[test]
    fn default_multibyte_access_rejects_overflow_before_any_byte_access() {
        let mut bus = ByteOnlyBus::default();

        assert_eq!(
            bus.read_u16(u64::MAX),
            Err(BusError::OutOfRange { addr: u64::MAX })
        );
        assert_eq!(
            bus.read_u32(u64::MAX - 2),
            Err(BusError::OutOfRange { addr: u64::MAX - 2 })
        );
        assert_eq!(
            bus.read_u64(u64::MAX - 6),
            Err(BusError::OutOfRange { addr: u64::MAX - 6 })
        );
        assert_eq!(
            bus.write_u16(u64::MAX, 0),
            Err(BusError::OutOfRange { addr: u64::MAX })
        );
        assert_eq!(
            bus.write_u32(u64::MAX - 2, 0),
            Err(BusError::OutOfRange { addr: u64::MAX - 2 })
        );
        assert_eq!(
            bus.write_u64(u64::MAX - 6, 0),
            Err(BusError::OutOfRange { addr: u64::MAX - 6 })
        );
        assert_eq!(bus.byte_reads, 0);
        assert_eq!(bus.byte_writes, 0);
    }
}
