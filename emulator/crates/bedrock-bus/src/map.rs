use crate::PhysicalMemoryClass;
use crate::bus::Bus;
use crate::device::{AccessWidth, Device};
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

    fn wide_device_mut(
        &mut self,
        addr: u64,
        width: AccessWidth,
    ) -> BusResult<(&mut dyn Device, u64, u64)> {
        let last = addr
            .checked_add(width.bytes() - 1)
            .ok_or(BusError::OutOfRange { addr })?;
        for mapped in &mut self.devices {
            if let Some(offset) = mapped.range.offset(addr) {
                if !mapped.range.contains(last) {
                    return Err(BusError::Unmapped {
                        addr: mapped.range.end_exclusive,
                    });
                }
                return Ok((mapped.device.as_mut(), offset, mapped.range.start));
            }
        }
        Err(BusError::Unmapped { addr })
    }

    fn read_device(&mut self, addr: u64, width: AccessWidth) -> BusResult<u64> {
        let (device, offset, base) = self.wide_device_mut(addr, width)?;
        device
            .read(offset, width)
            .map_err(|error| error.rebase_or_out_of_range(base, addr))
    }

    fn write_device(&mut self, addr: u64, width: AccessWidth, value: u64) -> BusResult<()> {
        let (device, offset, base) = self.wide_device_mut(addr, width)?;
        device
            .write(offset, width, value)
            .map_err(|error| error.rebase_or_out_of_range(base, addr))
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

    fn physical_memory_class(&self, addr: u64) -> PhysicalMemoryClass {
        if self
            .devices
            .iter()
            .any(|mapped| mapped.range.contains(addr))
        {
            PhysicalMemoryClass::Device
        } else {
            PhysicalMemoryClass::Normal
        }
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

    fn read_u16(&mut self, addr: u64) -> BusResult<u16> {
        self.read_device(addr, AccessWidth::Word)
            .map(|value| value as u16)
    }

    fn read_u32(&mut self, addr: u64) -> BusResult<u32> {
        self.read_device(addr, AccessWidth::Long)
            .map(|value| value as u32)
    }

    fn read_u64(&mut self, addr: u64) -> BusResult<u64> {
        self.read_device(addr, AccessWidth::Quad)
    }

    fn write_u16(&mut self, addr: u64, value: u16) -> BusResult<()> {
        self.write_device(addr, AccessWidth::Word, u64::from(value))
    }

    fn write_u32(&mut self, addr: u64, value: u32) -> BusResult<()> {
        self.write_device(addr, AccessWidth::Long, u64::from(value))
    }

    fn write_u64(&mut self, addr: u64, value: u64) -> BusResult<()> {
        self.write_device(addr, AccessWidth::Quad, value)
    }
}

#[cfg(test)]
mod tests {
    use super::MappedBus;
    use crate::{AccessWidth, AddressRange, Bus, BusError, BusResult, Device};
    use std::cell::RefCell;
    use std::rc::Rc;

    #[test]
    fn unmapped_access_returns_bus_error() {
        let mut bus = MappedBus::new();

        assert_eq!(
            bus.read_u8(0xfeed_beef).unwrap_err(),
            BusError::Unmapped { addr: 0xfeed_beef }
        );
    }

    type RecordedAccess = (bool, u64, AccessWidth, u64);

    struct RecordingDevice(Rc<RefCell<Vec<RecordedAccess>>>);

    impl Device for RecordingDevice {
        fn begin_transaction(&mut self) -> BusResult<()> {
            Ok(())
        }

        fn commit_transaction(&mut self) {}

        fn rollback_transaction(&mut self) {}

        fn read(&mut self, offset: u64, width: AccessWidth) -> BusResult<u64> {
            self.0.borrow_mut().push((false, offset, width, 0));
            Ok(0x8877_6655_4433_2211)
        }

        fn write(&mut self, offset: u64, width: AccessWidth, value: u64) -> BusResult<()> {
            self.0.borrow_mut().push((true, offset, width, value));
            Ok(())
        }
    }

    fn read_width(bus: &mut MappedBus, addr: u64, width: AccessWidth) -> BusResult<u64> {
        match width {
            AccessWidth::Byte => bus.read_u8(addr).map(u64::from),
            AccessWidth::Word => bus.read_u16(addr).map(u64::from),
            AccessWidth::Long => bus.read_u32(addr).map(u64::from),
            AccessWidth::Quad => bus.read_u64(addr),
        }
    }

    fn write_width(
        bus: &mut MappedBus,
        addr: u64,
        width: AccessWidth,
        value: u64,
    ) -> BusResult<()> {
        match width {
            AccessWidth::Byte => bus.write_u8(addr, value as u8),
            AccessWidth::Word => bus.write_u16(addr, value as u16),
            AccessWidth::Long => bus.write_u32(addr, value as u32),
            AccessWidth::Quad => bus.write_u64(addr, value),
        }
    }

    #[test]
    fn mapped_wide_accesses_are_one_width_preserving_device_event() {
        let events = Rc::new(RefCell::new(Vec::new()));
        let mut bus = MappedBus::new();
        bus.add_device(
            AddressRange::from_start_len(0x8000, 0x100).unwrap(),
            Box::new(RecordingDevice(events.clone())),
        );

        assert_eq!(bus.read_u16(0x8008).unwrap(), 0x2211);
        bus.write_u16(0x800a, 0xcdef).unwrap();
        assert_eq!(bus.read_u32(0x8010).unwrap(), 0x4433_2211);
        bus.write_u32(0x8014, 0x89ab_cdef).unwrap();
        assert_eq!(bus.read_u64(0x8020).unwrap(), 0x8877_6655_4433_2211);
        bus.write_u64(0x8028, 0x0123_4567_89ab_cdef).unwrap();

        assert_eq!(
            *events.borrow(),
            vec![
                (false, 0x08, AccessWidth::Word, 0),
                (true, 0x0a, AccessWidth::Word, 0xcdef),
                (false, 0x10, AccessWidth::Long, 0),
                (true, 0x14, AccessWidth::Long, 0x89ab_cdef),
                (false, 0x20, AccessWidth::Quad, 0),
                (true, 0x28, AccessWidth::Quad, 0x0123_4567_89ab_cdef),
            ]
        );
    }

    #[test]
    fn mapped_wide_access_rejects_mapping_crossing_before_device_event() {
        let events = Rc::new(RefCell::new(Vec::new()));
        let mut bus = MappedBus::new();
        let range = AddressRange::from_start_len(0x8000, 0x10).unwrap();
        bus.add_device(range, Box::new(RecordingDevice(events.clone())));

        for width in [AccessWidth::Word, AccessWidth::Long, AccessWidth::Quad] {
            let addr = range.end_exclusive - width.bytes() + 1;
            assert_eq!(
                read_width(&mut bus, addr, width),
                Err(BusError::Unmapped {
                    addr: range.end_exclusive
                })
            );
            assert_eq!(
                write_width(&mut bus, addr, width, u64::MAX),
                Err(BusError::Unmapped {
                    addr: range.end_exclusive
                })
            );
        }
        assert!(events.borrow().is_empty());
    }

    #[test]
    fn mapped_wide_access_rejects_address_overflow_before_device_event() {
        let events = Rc::new(RefCell::new(Vec::new()));
        let mut bus = MappedBus::new();
        bus.add_device(
            AddressRange::new(u64::MAX - 0x20, u64::MAX).unwrap(),
            Box::new(RecordingDevice(events.clone())),
        );

        for width in [AccessWidth::Word, AccessWidth::Long, AccessWidth::Quad] {
            let addr = u64::MAX - (width.bytes() - 2);
            assert_eq!(
                read_width(&mut bus, addr, width),
                Err(BusError::OutOfRange { addr })
            );
            assert_eq!(
                write_width(&mut bus, addr, width, u64::MAX),
                Err(BusError::OutOfRange { addr })
            );
        }
        assert!(events.borrow().is_empty());
    }

    struct ErrorByteDevice(BusError);

    impl Device for ErrorByteDevice {
        fn begin_transaction(&mut self) -> BusResult<()> {
            Ok(())
        }

        fn commit_transaction(&mut self) {}

        fn rollback_transaction(&mut self) {}

        fn read(&mut self, _offset: u64, _width: AccessWidth) -> BusResult<u64> {
            Err(self.0.clone())
        }

        fn write(&mut self, _offset: u64, _width: AccessWidth, _value: u64) -> BusResult<()> {
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
