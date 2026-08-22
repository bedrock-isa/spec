use crate::bus::Bus;
use crate::device::{AccessWidth, Device};
use crate::error::{BusError, BusResult};
use std::collections::BTreeMap;

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Ram {
    bytes: Vec<u8>,
    transaction: Option<BTreeMap<usize, u8>>,
}

impl Ram {
    pub fn new(size: usize) -> Self {
        Self {
            bytes: vec![0; size],
            transaction: None,
        }
    }

    pub fn len(&self) -> usize {
        self.bytes.len()
    }

    pub fn is_empty(&self) -> bool {
        self.bytes.is_empty()
    }

    pub fn as_slice(&self) -> &[u8] {
        &self.bytes
    }

    pub fn as_mut_slice(&mut self) -> &mut [u8] {
        &mut self.bytes
    }

    pub fn load(&mut self, addr: u64, data: &[u8]) -> BusResult<()> {
        let start = usize::try_from(addr).map_err(|_| BusError::OutOfRange { addr })?;
        let end = start
            .checked_add(data.len())
            .ok_or(BusError::OutOfRange { addr })?;

        if end > self.bytes.len() {
            return Err(BusError::OutOfRange { addr });
        }

        self.bytes[start..end].copy_from_slice(data);
        Ok(())
    }

    fn index(&self, addr: u64) -> BusResult<usize> {
        let index = usize::try_from(addr).map_err(|_| BusError::OutOfRange { addr })?;
        if index >= self.bytes.len() {
            return Err(BusError::OutOfRange { addr });
        }
        Ok(index)
    }
}

impl Bus for Ram {
    fn begin_transaction(&mut self) -> BusResult<()> {
        if self.transaction.is_some() {
            return Err(BusError::TransactionActive);
        }
        self.transaction = Some(BTreeMap::new());
        Ok(())
    }

    fn commit_transaction(&mut self) {
        if let Some(writes) = self.transaction.take() {
            for (index, value) in writes {
                self.bytes[index] = value;
            }
        }
    }

    fn rollback_transaction(&mut self) {
        self.transaction = None;
    }

    fn read_u8(&mut self, addr: u64) -> BusResult<u8> {
        let index = self.index(addr)?;
        Ok(self
            .transaction
            .as_ref()
            .and_then(|writes| writes.get(&index).copied())
            .unwrap_or(self.bytes[index]))
    }

    fn write_u8(&mut self, addr: u64, value: u8) -> BusResult<()> {
        let index = self.index(addr)?;
        if let Some(writes) = &mut self.transaction {
            writes.insert(index, value);
        } else {
            self.bytes[index] = value;
        }
        Ok(())
    }
}

impl Device for Ram {
    fn begin_transaction(&mut self) -> BusResult<()> {
        Bus::begin_transaction(self)
    }

    fn commit_transaction(&mut self) {
        Bus::commit_transaction(self)
    }

    fn rollback_transaction(&mut self) {
        Bus::rollback_transaction(self)
    }

    fn read(&mut self, offset: u64, width: AccessWidth) -> BusResult<u64> {
        match width {
            AccessWidth::Byte => Bus::read_u8(self, offset).map(u64::from),
            AccessWidth::Word => Bus::read_u16(self, offset).map(u64::from),
            AccessWidth::Long => Bus::read_u32(self, offset).map(u64::from),
            AccessWidth::Quad => Bus::read_u64(self, offset),
        }
    }

    fn write(&mut self, offset: u64, width: AccessWidth, value: u64) -> BusResult<()> {
        match width {
            AccessWidth::Byte => Bus::write_u8(self, offset, value as u8),
            AccessWidth::Word => Bus::write_u16(self, offset, value as u16),
            AccessWidth::Long => Bus::write_u32(self, offset, value as u32),
            AccessWidth::Quad => Bus::write_u64(self, offset, value),
        }
    }
}

#[cfg(test)]
mod tests {
    use super::Ram;
    use crate::Bus;

    #[test]
    fn reads_and_writes_little_endian_values() {
        let mut ram = Ram::new(16);

        ram.write_u16(0, 0x1234).unwrap();
        ram.write_u32(2, 0x89ab_cdef).unwrap();
        ram.write_u64(6, 0x0123_4567_89ab_cdef).unwrap();

        assert_eq!(ram.as_slice()[0], 0x34);
        assert_eq!(ram.as_slice()[1], 0x12);
        assert_eq!(ram.read_u16(0).unwrap(), 0x1234);
        assert_eq!(ram.read_u32(2).unwrap(), 0x89ab_cdef);
        assert_eq!(ram.read_u64(6).unwrap(), 0x0123_4567_89ab_cdef);
    }

    #[test]
    fn transaction_stages_and_rolls_back_writes() {
        let mut ram = Ram::new(4);
        ram.write_u8(0, 1).unwrap();
        ram.begin_transaction().unwrap();
        ram.write_u8(0, 2).unwrap();
        assert_eq!(ram.read_u8(0).unwrap(), 2);
        ram.rollback_transaction();
        assert_eq!(ram.read_u8(0).unwrap(), 1);
    }
}
