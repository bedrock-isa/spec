use crate::error::{
    AcknowledgedBusFailure, BusError, BusFailureCause, BusResult, RetrySafety, SlotProtocolError,
    SlotResult, SlotTransactionError,
};

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum SlotWidth {
    B,
    W,
    L,
    Q,
}

impl SlotWidth {
    pub const fn bytes(self) -> u8 {
        match self {
            Self::B => 1,
            Self::W => 2,
            Self::L => 4,
            Self::Q => 8,
        }
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum SlotDirection {
    Read,
    Write,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum SlotData {
    B(u8),
    W(u16),
    L(u32),
    Q(u64),
}

impl SlotData {
    pub const fn width(self) -> SlotWidth {
        match self {
            Self::B(_) => SlotWidth::B,
            Self::W(_) => SlotWidth::W,
            Self::L(_) => SlotWidth::L,
            Self::Q(_) => SlotWidth::Q,
        }
    }

    pub const fn as_u64(self) -> u64 {
        match self {
            Self::B(value) => value as u64,
            Self::W(value) => value as u64,
            Self::L(value) => value as u64,
            Self::Q(value) => value,
        }
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct SlotRequest {
    address: u64,
    width: SlotWidth,
    direction: SlotDirection,
    write_data: Option<SlotData>,
}

impl SlotRequest {
    pub const fn read(address: u64, width: SlotWidth) -> Self {
        Self {
            address,
            width,
            direction: SlotDirection::Read,
            write_data: None,
        }
    }

    pub const fn write(address: u64, data: SlotData) -> Self {
        Self {
            address,
            width: data.width(),
            direction: SlotDirection::Write,
            write_data: Some(data),
        }
    }

    pub const fn address(self) -> u64 {
        self.address
    }

    pub const fn width(self) -> SlotWidth {
        self.width
    }

    pub const fn direction(self) -> SlotDirection {
        self.direction
    }

    pub const fn write_data(self) -> Option<SlotData> {
        self.write_data
    }

    pub(crate) const fn with_address(self, address: u64) -> Self {
        Self { address, ..self }
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum SlotOutcome {
    Read(SlotData),
    Write,
    Failed(AcknowledgedBusFailure),
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct SlotAcknowledgement {
    outcome: SlotOutcome,
}

impl SlotAcknowledgement {
    pub fn read(request: SlotRequest, data: SlotData) -> SlotResult<Self> {
        if request.direction != SlotDirection::Read {
            return Err(SlotTransactionError::Protocol {
                addr: request.address,
                error: SlotProtocolError::DirectionMismatch,
            });
        }
        if request.width != data.width() {
            return Err(SlotTransactionError::Protocol {
                addr: request.address,
                error: SlotProtocolError::WidthMismatch,
            });
        }
        Ok(Self {
            outcome: SlotOutcome::Read(data),
        })
    }

    pub fn write(request: SlotRequest) -> SlotResult<Self> {
        if request.direction != SlotDirection::Write {
            return Err(SlotTransactionError::Protocol {
                addr: request.address,
                error: SlotProtocolError::DirectionMismatch,
            });
        }
        Ok(Self {
            outcome: SlotOutcome::Write,
        })
    }

    pub const fn failed(failure: AcknowledgedBusFailure) -> Self {
        Self {
            outcome: SlotOutcome::Failed(failure),
        }
    }

    pub const fn outcome(self) -> SlotOutcome {
        self.outcome
    }

    pub const fn failure(self) -> Option<AcknowledgedBusFailure> {
        match self.outcome {
            SlotOutcome::Failed(failure) => Some(failure),
            SlotOutcome::Read(_) | SlotOutcome::Write => None,
        }
    }

    pub fn validate_for(self, request: SlotRequest) -> SlotResult<Self> {
        match self.outcome {
            SlotOutcome::Read(_) if request.direction != SlotDirection::Read => {
                Err(SlotTransactionError::Protocol {
                    addr: request.address,
                    error: SlotProtocolError::DirectionMismatch,
                })
            }
            SlotOutcome::Read(data) if data.width() != request.width => {
                Err(SlotTransactionError::Protocol {
                    addr: request.address,
                    error: SlotProtocolError::WidthMismatch,
                })
            }
            SlotOutcome::Write if request.direction != SlotDirection::Write => {
                Err(SlotTransactionError::Protocol {
                    addr: request.address,
                    error: SlotProtocolError::DirectionMismatch,
                })
            }
            SlotOutcome::Read(_) | SlotOutcome::Write | SlotOutcome::Failed(_) => Ok(self),
        }
    }

    pub(crate) fn rebase_failure(self, base: u64, request_address: u64) -> SlotResult<Self> {
        let SlotOutcome::Failed(mut failure) = self.outcome else {
            return Ok(self);
        };
        failure.final_address =
            base.checked_add(failure.final_address)
                .ok_or(SlotTransactionError::Protocol {
                    addr: request_address,
                    error: SlotProtocolError::AddressOverflow,
                })?;
        Ok(Self::failed(failure))
    }
}

pub trait Bus {
    fn begin_transaction(&mut self) -> BusResult<()>;
    fn commit_transaction(&mut self);
    fn rollback_transaction(&mut self);

    fn read_u8(&mut self, addr: u64) -> BusResult<u8>;
    fn write_u8(&mut self, addr: u64, value: u8) -> BusResult<()>;

    fn slot_transaction(&mut self, request: SlotRequest) -> SlotResult<SlotAcknowledgement> {
        Ok(SlotAcknowledgement::failed(AcknowledgedBusFailure::new(
            BusFailureCause::Other,
            request.address(),
            RetrySafety::RetrySafe,
        )))
    }

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
    use super::{Bus, SlotAcknowledgement, SlotData, SlotOutcome, SlotRequest, SlotWidth};
    use crate::{
        AcknowledgedBusFailure, BusError, BusFailureCause, BusResult, RetrySafety,
        SlotProtocolError, SlotTransactionError,
    };

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
    fn default_slot_transaction_fails_closed_without_byte_access() {
        let mut bus = ByteOnlyBus::default();
        let acknowledgement = bus
            .slot_transaction(SlotRequest::write(4095, SlotData::Q(u64::MAX)))
            .unwrap();

        assert_eq!(
            acknowledgement.failure(),
            Some(AcknowledgedBusFailure::new(
                BusFailureCause::Other,
                4095,
                RetrySafety::RetrySafe,
            ))
        );
        assert_eq!(bus.byte_reads, 0);
        assert_eq!(bus.byte_writes, 0);
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

    #[test]
    fn acknowledgement_construction_enforces_direction_and_width() {
        let read = SlotRequest::read(1, SlotWidth::W);
        assert_eq!(
            SlotAcknowledgement::read(read, SlotData::W(0x1234))
                .unwrap()
                .outcome(),
            SlotOutcome::Read(SlotData::W(0x1234))
        );
        assert_eq!(
            SlotAcknowledgement::read(read, SlotData::B(0x12)).unwrap_err(),
            SlotTransactionError::Protocol {
                addr: 1,
                error: SlotProtocolError::WidthMismatch,
            }
        );
        assert_eq!(
            SlotAcknowledgement::write(read).unwrap_err(),
            SlotTransactionError::Protocol {
                addr: 1,
                error: SlotProtocolError::DirectionMismatch,
            }
        );
    }
}
