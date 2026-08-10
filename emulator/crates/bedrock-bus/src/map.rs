use crate::bus::{Bus, SlotAcknowledgement, SlotRequest};
use crate::device::Device;
use crate::error::{
    AcknowledgedBusFailure, BusError, BusFailureCause, BusResult, RetrySafety, SlotProtocolError,
    SlotResult, SlotTransactionError,
};

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

    fn slot_transaction(&mut self, request: SlotRequest) -> SlotResult<SlotAcknowledgement> {
        let address = request.address();
        let Some((device, offset, base)) = self.device_mut(address) else {
            return Ok(SlotAcknowledgement::failed(AcknowledgedBusFailure::new(
                BusFailureCause::NoResponder,
                address,
                RetrySafety::RetrySafe,
            )));
        };
        let mapped_request = request.with_address(offset);
        device
            .slot_transaction(mapped_request)
            .map_err(|error| rebase_slot_error(error, base, address))?
            .validate_for(request)?
            .rebase_failure(base, address)
    }
}

fn rebase_slot_error(
    error: SlotTransactionError,
    base: u64,
    request_address: u64,
) -> SlotTransactionError {
    fn rebase_address(
        address: u64,
        base: u64,
        request_address: u64,
    ) -> Result<u64, SlotTransactionError> {
        base.checked_add(address)
            .ok_or(SlotTransactionError::Protocol {
                addr: request_address,
                error: SlotProtocolError::AddressOverflow,
            })
    }

    match error {
        SlotTransactionError::Protocol { addr, error } => {
            match rebase_address(addr, base, request_address) {
                Ok(addr) => SlotTransactionError::Protocol { addr, error },
                Err(overflow) => overflow,
            }
        }
        SlotTransactionError::Bus(error) => match error.checked_rebase(base) {
            Some(error) => SlotTransactionError::Bus(error),
            None => SlotTransactionError::Protocol {
                addr: request_address,
                error: SlotProtocolError::AddressOverflow,
            },
        },
    }
}

#[cfg(test)]
mod tests {
    use super::MappedBus;
    use crate::{
        AcknowledgedBusFailure, AddressRange, Bus, BusError, BusFailureCause, BusResult, Device,
        RetrySafety, SlotAcknowledgement, SlotData, SlotDirection, SlotOutcome, SlotProtocolError,
        SlotRequest, SlotResult, SlotTransactionError, SlotWidth,
    };
    use std::cell::RefCell;
    use std::rc::Rc;

    #[derive(Default)]
    struct ProbeState {
        slot_requests: Vec<SlotRequest>,
        byte_reads: usize,
        byte_writes: usize,
    }

    struct ProbeDevice(Rc<RefCell<ProbeState>>);

    impl Device for ProbeDevice {
        fn begin_transaction(&mut self) -> BusResult<()> {
            Ok(())
        }

        fn commit_transaction(&mut self) {}

        fn rollback_transaction(&mut self) {}

        fn read_u8(&mut self, _offset: u64) -> BusResult<u8> {
            self.0.borrow_mut().byte_reads += 1;
            Ok(0)
        }

        fn write_u8(&mut self, _offset: u64, _value: u8) -> BusResult<()> {
            self.0.borrow_mut().byte_writes += 1;
            Ok(())
        }

        fn slot_transaction(&mut self, request: SlotRequest) -> SlotResult<SlotAcknowledgement> {
            self.0.borrow_mut().slot_requests.push(request);
            match request.direction() {
                SlotDirection::Read => {
                    SlotAcknowledgement::read(request, data_for_width(request.width()))
                }
                SlotDirection::Write => SlotAcknowledgement::write(request),
            }
        }
    }

    const fn data_for_width(width: SlotWidth) -> SlotData {
        match width {
            SlotWidth::B => SlotData::B(0xa5),
            SlotWidth::W => SlotData::W(0xb6a5),
            SlotWidth::L => SlotData::L(0xd8c7_b6a5),
            SlotWidth::Q => SlotData::Q(0x1020_3040_d8c7_b6a5),
        }
    }

    #[test]
    fn unmapped_access_returns_bus_error() {
        let mut bus = MappedBus::new();

        assert_eq!(
            bus.read_u8(0xfeed_beef).unwrap_err(),
            BusError::Unmapped { addr: 0xfeed_beef }
        );
    }

    #[test]
    fn every_slot_width_and_boundary_uses_one_slot_call_and_no_byte_calls() {
        let state = Rc::new(RefCell::new(ProbeState::default()));
        let mut bus = MappedBus::new();
        bus.add_device(
            AddressRange::from_start_len(0, 4096).unwrap(),
            Box::new(ProbeDevice(Rc::clone(&state))),
        );

        let widths = [SlotWidth::B, SlotWidth::W, SlotWidth::L, SlotWidth::Q];
        let addresses = [0, 1, 4095];
        let mut calls = 0;
        for address in addresses {
            for width in widths {
                let acknowledgement = bus
                    .slot_transaction(SlotRequest::read(address, width))
                    .unwrap();
                calls += 1;
                assert_eq!(state.borrow().slot_requests.len(), calls);
                assert_eq!(
                    acknowledgement.outcome(),
                    SlotOutcome::Read(data_for_width(width))
                );

                let data = data_for_width(width);
                let acknowledgement = bus
                    .slot_transaction(SlotRequest::write(address, data))
                    .unwrap();
                calls += 1;
                assert_eq!(state.borrow().slot_requests.len(), calls);
                assert_eq!(acknowledgement.outcome(), SlotOutcome::Write);
            }
        }

        let state = state.borrow();
        assert_eq!(state.byte_reads, 0);
        assert_eq!(state.byte_writes, 0);
        assert_eq!(state.slot_requests.len(), 24);
        for request in &state.slot_requests {
            if let Some(data) = request.write_data() {
                assert_eq!(data.width(), request.width());
            }
        }
    }

    #[test]
    fn mapped_slot_routing_preserves_offset_and_width_does_not_expand_range() {
        let state = Rc::new(RefCell::new(ProbeState::default()));
        let mut bus = MappedBus::new();
        bus.add_device(
            AddressRange::from_start_len(0x1000, 2).unwrap(),
            Box::new(ProbeDevice(Rc::clone(&state))),
        );

        let acknowledgement = bus
            .slot_transaction(SlotRequest::read(0x1001, SlotWidth::Q))
            .unwrap();
        assert_eq!(
            acknowledgement.outcome(),
            SlotOutcome::Read(data_for_width(SlotWidth::Q))
        );
        assert_eq!(state.borrow().slot_requests[0].address(), 1);

        let acknowledgement = bus
            .slot_transaction(SlotRequest::read(0x1002, SlotWidth::B))
            .unwrap();
        assert_eq!(
            acknowledgement.failure(),
            Some(AcknowledgedBusFailure::new(
                BusFailureCause::NoResponder,
                0x1002,
                RetrySafety::RetrySafe,
            ))
        );
        assert_eq!(state.borrow().slot_requests.len(), 1);
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

    struct ErrorSlotDevice(SlotTransactionError);

    impl Device for ErrorSlotDevice {
        fn begin_transaction(&mut self) -> BusResult<()> {
            Ok(())
        }

        fn commit_transaction(&mut self) {}

        fn rollback_transaction(&mut self) {}

        fn read_u8(&mut self, _offset: u64) -> BusResult<u8> {
            unreachable!()
        }

        fn write_u8(&mut self, _offset: u64, _value: u8) -> BusResult<()> {
            unreachable!()
        }

        fn slot_transaction(&mut self, _request: SlotRequest) -> SlotResult<SlotAcknowledgement> {
            Err(self.0.clone())
        }
    }

    fn route_device_error(
        range: AddressRange,
        request_address: u64,
        error: SlotTransactionError,
    ) -> SlotTransactionError {
        let mut bus = MappedBus::new();
        bus.add_device(range, Box::new(ErrorSlotDevice(error)));
        bus.slot_transaction(SlotRequest::read(request_address, SlotWidth::B))
            .unwrap_err()
    }

    #[test]
    fn mapped_device_errors_rebase_every_local_address() {
        let base = 0x8000;
        let range = AddressRange::from_start_len(base, 0x100).unwrap();
        let request_address = base + 1;
        let cases = [
            (
                SlotTransactionError::Protocol {
                    addr: 2,
                    error: SlotProtocolError::WidthMismatch,
                },
                SlotTransactionError::Protocol {
                    addr: base + 2,
                    error: SlotProtocolError::WidthMismatch,
                },
            ),
            (
                SlotTransactionError::Bus(BusError::OutOfRange { addr: 3 }),
                SlotTransactionError::Bus(BusError::OutOfRange { addr: base + 3 }),
            ),
            (
                SlotTransactionError::Bus(BusError::Unmapped { addr: 4 }),
                SlotTransactionError::Bus(BusError::Unmapped { addr: base + 4 }),
            ),
            (
                SlotTransactionError::Bus(BusError::InvalidRange { start: 5, end: 9 }),
                SlotTransactionError::Bus(BusError::InvalidRange {
                    start: base + 5,
                    end: base + 9,
                }),
            ),
            (
                SlotTransactionError::Bus(BusError::ReadOnly { addr: 6 }),
                SlotTransactionError::Bus(BusError::ReadOnly { addr: base + 6 }),
            ),
            (
                SlotTransactionError::Bus(BusError::Device {
                    addr: 7,
                    message: "device detail".into(),
                }),
                SlotTransactionError::Bus(BusError::Device {
                    addr: base + 7,
                    message: "device detail".into(),
                }),
            ),
        ];

        for (local, expected) in cases {
            assert_eq!(route_device_error(range, request_address, local), expected);
        }
    }

    #[test]
    fn mapped_device_lifecycle_errors_are_preserved() {
        let base = 0x8000;
        let range = AddressRange::from_start_len(base, 0x100).unwrap();
        for error in [BusError::TransactionActive, BusError::NoTransaction] {
            let error = SlotTransactionError::Bus(error);
            assert_eq!(route_device_error(range, base, error.clone()), error);
        }
    }

    #[test]
    fn mapped_device_error_address_overflow_uses_original_request_address() {
        let base = u64::MAX - 0x10;
        let range = AddressRange::new(base, u64::MAX).unwrap();
        let request_address = base + 1;
        let overflowing = 0x11;
        let errors = [
            SlotTransactionError::Protocol {
                addr: overflowing,
                error: SlotProtocolError::DirectionMismatch,
            },
            SlotTransactionError::Bus(BusError::OutOfRange { addr: overflowing }),
            SlotTransactionError::Bus(BusError::Unmapped { addr: overflowing }),
            SlotTransactionError::Bus(BusError::InvalidRange {
                start: overflowing,
                end: 0,
            }),
            SlotTransactionError::Bus(BusError::InvalidRange {
                start: 0,
                end: overflowing,
            }),
            SlotTransactionError::Bus(BusError::ReadOnly { addr: overflowing }),
            SlotTransactionError::Bus(BusError::Device {
                addr: overflowing,
                message: "overflow".into(),
            }),
        ];
        let expected = SlotTransactionError::Protocol {
            addr: request_address,
            error: SlotProtocolError::AddressOverflow,
        };

        for error in errors {
            assert_eq!(route_device_error(range, request_address, error), expected);
        }
    }

    struct FailingSlotDevice;

    impl Device for FailingSlotDevice {
        fn begin_transaction(&mut self) -> BusResult<()> {
            Ok(())
        }

        fn commit_transaction(&mut self) {}

        fn rollback_transaction(&mut self) {}

        fn read_u8(&mut self, _offset: u64) -> BusResult<u8> {
            unreachable!()
        }

        fn write_u8(&mut self, _offset: u64, _value: u8) -> BusResult<()> {
            unreachable!()
        }

        fn slot_transaction(&mut self, request: SlotRequest) -> SlotResult<SlotAcknowledgement> {
            Ok(SlotAcknowledgement::failed(AcknowledgedBusFailure::new(
                BusFailureCause::DataError,
                request.address(),
                RetrySafety::EffectMayHaveOccurred,
            )))
        }
    }

    #[test]
    fn mapped_failure_reports_the_final_bus_address() {
        let mut bus = MappedBus::new();
        bus.add_device(
            AddressRange::from_start_len(0x8000, 4).unwrap(),
            Box::new(FailingSlotDevice),
        );

        let acknowledgement = bus
            .slot_transaction(SlotRequest::write(0x8003, SlotData::W(0x1234)))
            .unwrap();
        assert_eq!(
            acknowledgement.failure(),
            Some(AcknowledgedBusFailure::new(
                BusFailureCause::DataError,
                0x8003,
                RetrySafety::EffectMayHaveOccurred,
            ))
        );
    }

    struct OverflowingFailureDevice;

    impl Device for OverflowingFailureDevice {
        fn begin_transaction(&mut self) -> BusResult<()> {
            Ok(())
        }

        fn commit_transaction(&mut self) {}

        fn rollback_transaction(&mut self) {}

        fn read_u8(&mut self, _offset: u64) -> BusResult<u8> {
            unreachable!()
        }

        fn write_u8(&mut self, _offset: u64, _value: u8) -> BusResult<()> {
            unreachable!()
        }

        fn slot_transaction(&mut self, _request: SlotRequest) -> SlotResult<SlotAcknowledgement> {
            Ok(SlotAcknowledgement::failed(AcknowledgedBusFailure::new(
                BusFailureCause::DataError,
                0x11,
                RetrySafety::EffectMayHaveOccurred,
            )))
        }
    }

    #[test]
    fn mapped_failure_address_overflow_uses_original_request_address() {
        let base = u64::MAX - 0x10;
        let request_address = base + 1;
        let mut bus = MappedBus::new();
        bus.add_device(
            AddressRange::new(base, u64::MAX).unwrap(),
            Box::new(OverflowingFailureDevice),
        );

        assert_eq!(
            bus.slot_transaction(SlotRequest::read(request_address, SlotWidth::B))
                .unwrap_err(),
            SlotTransactionError::Protocol {
                addr: request_address,
                error: SlotProtocolError::AddressOverflow,
            }
        );
    }

    #[derive(Default)]
    struct StagedState {
        pending: Option<SlotData>,
        committed: Option<SlotData>,
    }

    struct StagedFailingStore(Rc<RefCell<StagedState>>);

    impl Device for StagedFailingStore {
        fn begin_transaction(&mut self) -> BusResult<()> {
            self.0.borrow_mut().pending = None;
            Ok(())
        }

        fn commit_transaction(&mut self) {
            let pending = self.0.borrow_mut().pending.take();
            self.0.borrow_mut().committed = pending;
        }

        fn rollback_transaction(&mut self) {
            self.0.borrow_mut().pending = None;
        }

        fn read_u8(&mut self, _offset: u64) -> BusResult<u8> {
            unreachable!()
        }

        fn write_u8(&mut self, _offset: u64, _value: u8) -> BusResult<()> {
            unreachable!()
        }

        fn slot_transaction(&mut self, request: SlotRequest) -> SlotResult<SlotAcknowledgement> {
            self.0.borrow_mut().pending = request.write_data();
            Ok(SlotAcknowledgement::failed(AcknowledgedBusFailure::new(
                BusFailureCause::DataError,
                request.address(),
                RetrySafety::RetrySafe,
            )))
        }
    }

    #[test]
    fn failed_slot_store_is_discarded_by_transaction_rollback() {
        let state = Rc::new(RefCell::new(StagedState::default()));
        let mut bus = MappedBus::new();
        bus.add_device(
            AddressRange::from_start_len(0x400, 1).unwrap(),
            Box::new(StagedFailingStore(Rc::clone(&state))),
        );

        bus.begin_transaction().unwrap();
        let acknowledgement = bus
            .slot_transaction(SlotRequest::write(
                0x400,
                SlotData::Q(0x0123_4567_89ab_cdef),
            ))
            .unwrap();
        assert_eq!(
            acknowledgement.failure().unwrap().cause,
            BusFailureCause::DataError
        );
        bus.rollback_transaction();

        assert_eq!(state.borrow().pending, None);
        assert_eq!(state.borrow().committed, None);
    }
}
