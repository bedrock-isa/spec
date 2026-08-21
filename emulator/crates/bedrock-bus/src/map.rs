use crate::bus::Bus;
use crate::device::Device;
use crate::error::{BusError, BusResult};

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct AddressRange {
    pub start: u64,
    pub end_exclusive: u64,
}

impl AddressRange {
    pub fn new(start: u64, end_exclusive: u64) -> BusResult<Self> {
        if end_exclusive <= start {
            return Err(BusError::InvalidRange {
                start,
                end: end_exclusive,
            });
        }
        Ok(Self {
            start,
            end_exclusive,
        })
    }

    pub fn from_start_len(start: u64, len: u64) -> BusResult<Self> {
        let end_exclusive = start.checked_add(len).ok_or(BusError::InvalidRange {
            start,
            end: u64::MAX,
        })?;
        Self::new(start, end_exclusive)
    }

    pub fn contains(self, addr: u64) -> bool {
        self.start <= addr && addr < self.end_exclusive
    }

    pub fn offset(self, addr: u64) -> Option<u64> {
        self.contains(addr).then_some(addr - self.start)
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct MapEntry<T> {
    pub range: AddressRange,
    pub target: T,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct AddressMap<T> {
    entries: Vec<MapEntry<T>>,
}

impl<T> Default for AddressMap<T> {
    fn default() -> Self {
        Self {
            entries: Vec::new(),
        }
    }
}

impl<T> AddressMap<T> {
    pub fn new() -> Self {
        Self::default()
    }

    pub fn add(&mut self, range: AddressRange, target: T) {
        self.entries.push(MapEntry { range, target });
    }

    pub fn entries(&self) -> &[MapEntry<T>] {
        &self.entries
    }

    pub fn find(&self, addr: u64) -> Option<&MapEntry<T>> {
        self.entries.iter().find(|entry| entry.range.contains(addr))
    }
}

pub struct MappedDevice {
    range: AddressRange,
    device: Box<dyn Device>,
}

#[derive(Default)]
pub struct MappedBus {
    devices: Vec<MappedDevice>,
    transaction_active: bool,
}

impl MappedBus {
    pub fn new() -> Self {
        Self::default()
    }

    pub fn add_device(&mut self, range: AddressRange, device: Box<dyn Device>) {
        self.devices.push(MappedDevice { range, device });
    }

    fn device_mut(&mut self, addr: u64) -> Option<(&mut dyn Device, u64, u64)> {
        for mapped in &mut self.devices {
            if let Some(offset) = mapped.range.offset(addr) {
                return Some((mapped.device.as_mut(), offset, mapped.range.start));
            }
        }
        None
    }
}

impl Bus for MappedBus {
    fn begin_transaction(&mut self) -> BusResult<()> {
        if self.transaction_active {
            return Err(BusError::TransactionActive);
        }
        for index in 0..self.devices.len() {
            if let Err(error) = self.devices[index].device.begin_transaction() {
                for mapped in &mut self.devices[..index] {
                    mapped.device.rollback_transaction();
                }
                return Err(error);
            }
        }
        self.transaction_active = true;
        Ok(())
    }

    fn commit_transaction(&mut self) {
        if !self.transaction_active {
            return;
        }
        for mapped in &mut self.devices {
            mapped.device.commit_transaction();
        }
        self.transaction_active = false;
    }

    fn rollback_transaction(&mut self) {
        if !self.transaction_active {
            return;
        }
        for mapped in &mut self.devices {
            mapped.device.rollback_transaction();
        }
        self.transaction_active = false;
    }

    fn read_u8(&mut self, addr: u64) -> BusResult<u8> {
        let Some((device, offset, base)) = self.device_mut(addr) else {
            return Err(BusError::Unmapped { addr });
        };
        device
            .read_u8(offset)
            .map_err(|error| error.rebase_or_out_of_range(base, addr))
    }

    fn write_u8(&mut self, addr: u64, value: u8) -> BusResult<()> {
        let Some((device, offset, base)) = self.device_mut(addr) else {
            return Err(BusError::Unmapped { addr });
        };
        device
            .write_u8(offset, value)
            .map_err(|error| error.rebase_or_out_of_range(base, addr))
    }
}

#[cfg(test)]
mod tests {
    use super::MappedBus;
    use crate::{AddressRange, Bus, BusError, BusResult, Device};

    #[test]
    fn unmapped_access_returns_bus_error() {
        let mut bus = MappedBus::new();

        assert_eq!(
            bus.read_u8(0xfeed_beef).unwrap_err(),
            BusError::Unmapped { addr: 0xfeed_beef }
        );
    }

    struct ErrorByteDevice(BusError);

    impl Device for ErrorByteDevice {
        fn begin_transaction(&mut self) -> BusResult<()> {
            Ok(())
        }

        fn commit_transaction(&mut self) {}

        fn rollback_transaction(&mut self) {}

        fn read_u8(&mut self, _offset: u64) -> BusResult<u8> {
            Err(self.0.clone())
        }

        fn write_u8(&mut self, _offset: u64, _value: u8) -> BusResult<()> {
            Err(self.0.clone())
        }
    }

    fn route_byte_error(
        range: AddressRange,
        request_address: u64,
        error: BusError,
        write: bool,
    ) -> BusError {
        let mut bus = MappedBus::new();
        bus.add_device(range, Box::new(ErrorByteDevice(error)));
        if write {
            bus.write_u8(request_address, 0).unwrap_err()
        } else {
            bus.read_u8(request_address).unwrap_err()
        }
    }

    #[test]
    fn mapped_byte_errors_rebase_every_local_address_for_reads_and_writes() {
        let base = 0x8000;
        let range = AddressRange::from_start_len(base, 0x100).unwrap();
        let request_address = base + 1;
        let cases = [
            (
                BusError::OutOfRange { addr: 2 },
                BusError::OutOfRange { addr: base + 2 },
            ),
            (
                BusError::Unmapped { addr: 3 },
                BusError::Unmapped { addr: base + 3 },
            ),
            (
                BusError::InvalidRange { start: 4, end: 9 },
                BusError::InvalidRange {
                    start: base + 4,
                    end: base + 9,
                },
            ),
            (
                BusError::ReadOnly { addr: 5 },
                BusError::ReadOnly { addr: base + 5 },
            ),
            (
                BusError::Device {
                    addr: 6,
                    message: "device detail".into(),
                },
                BusError::Device {
                    addr: base + 6,
                    message: "device detail".into(),
                },
            ),
        ];

        for (local, expected) in cases {
            assert_eq!(
                route_byte_error(range, request_address, local.clone(), false),
                expected
            );
            assert_eq!(
                route_byte_error(range, request_address, local, true),
                expected
            );
        }
    }

    #[test]
    fn mapped_byte_lifecycle_errors_are_preserved_for_reads_and_writes() {
        let base = 0x8000;
        let range = AddressRange::from_start_len(base, 0x100).unwrap();

        for error in [BusError::TransactionActive, BusError::NoTransaction] {
            assert_eq!(route_byte_error(range, base, error.clone(), false), error);
            assert_eq!(route_byte_error(range, base, error.clone(), true), error);
        }
    }

    #[test]
    fn mapped_byte_error_rebase_overflow_reports_original_request_address() {
        let base = u64::MAX - 0x10;
        let range = AddressRange::new(base, u64::MAX).unwrap();
        let request_address = base + 1;
        let overflowing = 0x11;
        let errors = [
            BusError::OutOfRange { addr: overflowing },
            BusError::Unmapped { addr: overflowing },
            BusError::InvalidRange {
                start: overflowing,
                end: 0,
            },
            BusError::InvalidRange {
                start: 0,
                end: overflowing,
            },
            BusError::ReadOnly { addr: overflowing },
            BusError::Device {
                addr: overflowing,
                message: "overflow".into(),
            },
        ];
        let expected = BusError::OutOfRange {
            addr: request_address,
        };

        for error in errors {
            assert_eq!(
                route_byte_error(range, request_address, error.clone(), false),
                expected
            );
            assert_eq!(
                route_byte_error(range, request_address, error, true),
                expected
            );
        }
    }
}
