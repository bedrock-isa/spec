use crate::bus::{SlotAcknowledgement, SlotRequest};
use crate::error::{AcknowledgedBusFailure, BusFailureCause, BusResult, RetrySafety, SlotResult};

pub trait Device {
    fn begin_transaction(&mut self) -> BusResult<()>;
    fn commit_transaction(&mut self);
    fn rollback_transaction(&mut self);

    fn read_u8(&mut self, offset: u64) -> BusResult<u8>;
    fn write_u8(&mut self, offset: u64, value: u8) -> BusResult<()>;

    fn slot_transaction(&mut self, request: SlotRequest) -> SlotResult<SlotAcknowledgement> {
        Ok(SlotAcknowledgement::failed(AcknowledgedBusFailure::new(
            BusFailureCause::Other,
            request.address(),
            RetrySafety::RetrySafe,
        )))
    }

    fn tick(&mut self, _cycles: u64) {}
}

#[cfg(test)]
mod tests {
    use super::Device;
    use crate::{
        AcknowledgedBusFailure, BusFailureCause, BusResult, RetrySafety, SlotData, SlotRequest,
    };

    #[derive(Default)]
    struct ByteOnlyDevice {
        byte_reads: usize,
        byte_writes: usize,
    }

    impl Device for ByteOnlyDevice {
        fn begin_transaction(&mut self) -> BusResult<()> {
            Ok(())
        }

        fn commit_transaction(&mut self) {}

        fn rollback_transaction(&mut self) {}

        fn read_u8(&mut self, _offset: u64) -> BusResult<u8> {
            self.byte_reads += 1;
            Ok(0)
        }

        fn write_u8(&mut self, _offset: u64, _value: u8) -> BusResult<()> {
            self.byte_writes += 1;
            Ok(())
        }
    }

    #[test]
    fn default_device_slot_transaction_is_unsupported_and_side_effect_free() {
        let mut device = ByteOnlyDevice::default();
        let acknowledgement = device
            .slot_transaction(SlotRequest::write(1, SlotData::L(0x1234_5678)))
            .unwrap();

        assert_eq!(
            acknowledgement.failure(),
            Some(AcknowledgedBusFailure::new(
                BusFailureCause::Other,
                1,
                RetrySafety::RetrySafe,
            ))
        );
        assert_eq!(device.byte_reads, 0);
        assert_eq!(device.byte_writes, 0);
    }
}
