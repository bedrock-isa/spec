use bedrock_bus::{
    AcknowledgedBusFailure, Bus, BusError, BusFailureCause, BusResult, Device, Ram, RetrySafety,
    SlotAcknowledgement, SlotDirection, SlotOutcome, SlotProtocolError, SlotRequest, SlotResult,
    SlotTransactionError,
};
use bedrock_devices::{FramebufferDevice, KeyboardDevice};

pub const RAM_BASE: u64 = 0x0000_0000;
pub const RAM_SIZE: u64 = 0x0010_0000;
pub const FRAMEBUFFER_VRAM_BASE: u64 = 0x00f0_0000;
pub const FRAMEBUFFER_VRAM_SIZE: u64 = 0x0001_0000;
pub const DISPLAY_REGISTERS_BASE: u64 = 0x00f1_0000;
pub const DISPLAY_REGISTERS_SIZE: u64 = 0x0000_0100;
pub const KEYBOARD_REGISTERS_BASE: u64 = 0x00f2_0000;
pub const KEYBOARD_REGISTERS_SIZE: u64 = 0x0000_0100;

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Board {
    ram: Ram,
    framebuffer: FramebufferDevice,
    keyboard: KeyboardDevice,
    transaction_active: bool,
}

impl Default for Board {
    fn default() -> Self {
        Self::new()
    }
}

impl Board {
    pub fn new() -> Self {
        Self {
            ram: Ram::new(RAM_SIZE as usize),
            framebuffer: FramebufferDevice::default(),
            keyboard: KeyboardDevice::default(),
            transaction_active: false,
        }
    }

    pub fn ram(&self) -> &Ram {
        &self.ram
    }

    pub fn ram_mut(&mut self) -> &mut Ram {
        &mut self.ram
    }

    pub fn framebuffer(&self) -> &FramebufferDevice {
        &self.framebuffer
    }

    pub fn framebuffer_mut(&mut self) -> &mut FramebufferDevice {
        &mut self.framebuffer
    }

    pub fn keyboard(&self) -> &KeyboardDevice {
        &self.keyboard
    }

    pub fn keyboard_mut(&mut self) -> &mut KeyboardDevice {
        &mut self.keyboard
    }

    pub fn load_ram(&mut self, addr: u64, data: &[u8]) -> BusResult<()> {
        self.ram.load(addr, data)
    }
}

impl Bus for Board {
    fn begin_transaction(&mut self) -> BusResult<()> {
        if self.transaction_active {
            return Err(BusError::TransactionActive);
        }
        Bus::begin_transaction(&mut self.ram)?;
        if let Err(error) = Device::begin_transaction(&mut self.framebuffer) {
            Bus::rollback_transaction(&mut self.ram);
            return Err(error);
        }
        if let Err(error) = Device::begin_transaction(&mut self.keyboard) {
            Device::rollback_transaction(&mut self.framebuffer);
            Bus::rollback_transaction(&mut self.ram);
            return Err(error);
        }
        self.transaction_active = true;
        Ok(())
    }

    fn commit_transaction(&mut self) {
        if !self.transaction_active {
            return;
        }
        Bus::commit_transaction(&mut self.ram);
        Device::commit_transaction(&mut self.framebuffer);
        Device::commit_transaction(&mut self.keyboard);
        self.transaction_active = false;
    }

    fn rollback_transaction(&mut self) {
        if !self.transaction_active {
            return;
        }
        Bus::rollback_transaction(&mut self.ram);
        Device::rollback_transaction(&mut self.framebuffer);
        Device::rollback_transaction(&mut self.keyboard);
        self.transaction_active = false;
    }

    fn read_u8(&mut self, addr: u64) -> BusResult<u8> {
        if let Some(offset) = offset_in(addr, RAM_BASE, RAM_SIZE) {
            return Bus::read_u8(&mut self.ram, offset)
                .map_err(|error| error.rebase_or_out_of_range(RAM_BASE, addr));
        }
        if let Some(offset) = offset_in(addr, FRAMEBUFFER_VRAM_BASE, FRAMEBUFFER_VRAM_SIZE) {
            return self
                .framebuffer
                .read_vram_u8(offset)
                .map_err(|error| error.rebase_or_out_of_range(FRAMEBUFFER_VRAM_BASE, addr));
        }
        if let Some(offset) = offset_in(addr, DISPLAY_REGISTERS_BASE, DISPLAY_REGISTERS_SIZE) {
            return self
                .framebuffer
                .read_register_u8(offset)
                .map_err(|error| error.rebase_or_out_of_range(DISPLAY_REGISTERS_BASE, addr));
        }
        if let Some(offset) = offset_in(addr, KEYBOARD_REGISTERS_BASE, KEYBOARD_REGISTERS_SIZE) {
            return self
                .keyboard
                .read_u8(offset)
                .map_err(|error| error.rebase_or_out_of_range(KEYBOARD_REGISTERS_BASE, addr));
        }
        Err(BusError::Unmapped { addr })
    }

    fn write_u8(&mut self, addr: u64, value: u8) -> BusResult<()> {
        if let Some(offset) = offset_in(addr, RAM_BASE, RAM_SIZE) {
            return Bus::write_u8(&mut self.ram, offset, value)
                .map_err(|error| error.rebase_or_out_of_range(RAM_BASE, addr));
        }
        if let Some(offset) = offset_in(addr, FRAMEBUFFER_VRAM_BASE, FRAMEBUFFER_VRAM_SIZE) {
            return self
                .framebuffer
                .write_vram_u8(offset, value)
                .map_err(|error| error.rebase_or_out_of_range(FRAMEBUFFER_VRAM_BASE, addr));
        }
        if let Some(offset) = offset_in(addr, DISPLAY_REGISTERS_BASE, DISPLAY_REGISTERS_SIZE) {
            return self
                .framebuffer
                .write_register_u8(offset, value)
                .map_err(|error| error.rebase_or_out_of_range(DISPLAY_REGISTERS_BASE, addr));
        }
        if let Some(offset) = offset_in(addr, KEYBOARD_REGISTERS_BASE, KEYBOARD_REGISTERS_SIZE) {
            return self
                .keyboard
                .write_u8(offset, value)
                .map_err(|error| error.rebase_or_out_of_range(KEYBOARD_REGISTERS_BASE, addr));
        }
        Err(BusError::Unmapped { addr })
    }

    fn slot_transaction(&mut self, request: SlotRequest) -> SlotResult<SlotAcknowledgement> {
        let address = request.address();
        let Some((offset, base, target)) = slot_target(address) else {
            return Ok(SlotAcknowledgement::failed(AcknowledgedBusFailure::new(
                BusFailureCause::NoResponder,
                address,
                RetrySafety::RetrySafe,
            )));
        };
        let mapped_request = slot_request_at(request, offset);
        let acknowledgement = match target {
            SlotTarget::Ram => Bus::slot_transaction(&mut self.ram, mapped_request),
            SlotTarget::Framebuffer => {
                Device::slot_transaction(&mut self.framebuffer, mapped_request)
            }
            SlotTarget::Keyboard => Device::slot_transaction(&mut self.keyboard, mapped_request),
        }
        .map_err(|error| rebase_slot_error(error, base, address))?;

        validate_slot_acknowledgement(acknowledgement, request)?;
        rebase_slot_acknowledgement(acknowledgement, base, address)
    }
}

#[derive(Clone, Copy)]
enum SlotTarget {
    Ram,
    Framebuffer,
    Keyboard,
}

fn slot_target(addr: u64) -> Option<(u64, u64, SlotTarget)> {
    if let Some(offset) = offset_in(addr, RAM_BASE, RAM_SIZE) {
        return Some((offset, RAM_BASE, SlotTarget::Ram));
    }
    if let Some(offset) = offset_in(addr, FRAMEBUFFER_VRAM_BASE, FRAMEBUFFER_VRAM_SIZE) {
        return Some((offset, FRAMEBUFFER_VRAM_BASE, SlotTarget::Framebuffer));
    }
    if let Some(offset) = offset_in(addr, DISPLAY_REGISTERS_BASE, DISPLAY_REGISTERS_SIZE) {
        return Some((offset, DISPLAY_REGISTERS_BASE, SlotTarget::Framebuffer));
    }
    if let Some(offset) = offset_in(addr, KEYBOARD_REGISTERS_BASE, KEYBOARD_REGISTERS_SIZE) {
        return Some((offset, KEYBOARD_REGISTERS_BASE, SlotTarget::Keyboard));
    }
    None
}

fn slot_request_at(request: SlotRequest, address: u64) -> SlotRequest {
    match request.direction() {
        SlotDirection::Read => SlotRequest::read(address, request.width()),
        SlotDirection::Write => SlotRequest::write(
            address,
            request
                .write_data()
                .expect("write slot requests always carry write data"),
        ),
    }
}

fn validate_slot_acknowledgement(
    acknowledgement: SlotAcknowledgement,
    request: SlotRequest,
) -> SlotResult<()> {
    match acknowledgement.outcome() {
        SlotOutcome::Read(_) if request.direction() != SlotDirection::Read => {
            Err(SlotTransactionError::Protocol {
                addr: request.address(),
                error: SlotProtocolError::DirectionMismatch,
            })
        }
        SlotOutcome::Read(data) if data.width() != request.width() => {
            Err(SlotTransactionError::Protocol {
                addr: request.address(),
                error: SlotProtocolError::WidthMismatch,
            })
        }
        SlotOutcome::Write if request.direction() != SlotDirection::Write => {
            Err(SlotTransactionError::Protocol {
                addr: request.address(),
                error: SlotProtocolError::DirectionMismatch,
            })
        }
        SlotOutcome::Read(_) | SlotOutcome::Write | SlotOutcome::Failed(_) => Ok(()),
    }
}

fn rebase_slot_acknowledgement(
    acknowledgement: SlotAcknowledgement,
    base: u64,
    request_address: u64,
) -> SlotResult<SlotAcknowledgement> {
    let Some(mut failure) = acknowledgement.failure() else {
        return Ok(acknowledgement);
    };
    failure.final_address =
        base.checked_add(failure.final_address)
            .ok_or(SlotTransactionError::Protocol {
                addr: request_address,
                error: SlotProtocolError::AddressOverflow,
            })?;
    Ok(SlotAcknowledgement::failed(failure))
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

fn offset_in(addr: u64, base: u64, size: u64) -> Option<u64> {
    let end = base.checked_add(size)?;
    (base <= addr && addr < end).then(|| addr - base)
}

#[cfg(test)]
mod tests {
    use super::{
        Board, DISPLAY_REGISTERS_BASE, DISPLAY_REGISTERS_SIZE, FRAMEBUFFER_VRAM_BASE,
        FRAMEBUFFER_VRAM_SIZE, KEYBOARD_REGISTERS_BASE, KEYBOARD_REGISTERS_SIZE, RAM_BASE,
        RAM_SIZE, rebase_slot_error,
    };
    use bedrock_bus::{
        AcknowledgedBusFailure, Bus, BusError, BusFailureCause, RetrySafety, SlotData,
        SlotProtocolError, SlotRequest, SlotTransactionError, SlotWidth,
    };

    #[test]
    fn high_unmapped_address_returns_bus_error_without_overflow() {
        let mut board = Board::new();

        assert_eq!(
            board.read_u8(u64::MAX),
            Err(BusError::Unmapped { addr: u64::MAX })
        );
    }

    #[test]
    fn board_rebases_framebuffer_and_keyboard_byte_errors() {
        let mut board = Board::new();
        let vram_out_of_range = FRAMEBUFFER_VRAM_BASE + board.framebuffer().vram_len() as u64;
        let display_unmapped = DISPLAY_REGISTERS_BASE + 0x18;
        let keyboard_unmapped = KEYBOARD_REGISTERS_BASE + 0x0c;

        assert_eq!(
            board.read_u8(vram_out_of_range),
            Err(BusError::Unmapped {
                addr: vram_out_of_range,
            })
        );
        assert_eq!(
            board.write_u8(vram_out_of_range, 0),
            Err(BusError::Unmapped {
                addr: vram_out_of_range,
            })
        );
        assert_eq!(
            board.read_u8(display_unmapped),
            Err(BusError::Unmapped {
                addr: display_unmapped,
            })
        );
        assert_eq!(
            board.write_u8(DISPLAY_REGISTERS_BASE, 0),
            Err(BusError::ReadOnly {
                addr: DISPLAY_REGISTERS_BASE,
            })
        );
        assert_eq!(
            board.read_u8(keyboard_unmapped),
            Err(BusError::Unmapped {
                addr: keyboard_unmapped,
            })
        );
        assert_eq!(
            board.write_u8(KEYBOARD_REGISTERS_BASE, 0),
            Err(BusError::ReadOnly {
                addr: KEYBOARD_REGISTERS_BASE,
            })
        );
    }

    #[test]
    fn board_transaction_rolls_back_ram_and_mmio() {
        let mut board = Board::new();
        board.begin_transaction().unwrap();
        board.write_u8(RAM_BASE, 0xaa).unwrap();
        board.write_u8(FRAMEBUFFER_VRAM_BASE, 0xbb).unwrap();
        board.rollback_transaction();
        assert_eq!(board.read_u8(RAM_BASE).unwrap(), 0);
        assert_eq!(board.read_u8(FRAMEBUFFER_VRAM_BASE).unwrap(), 0);
    }

    #[test]
    fn q_slot_at_each_mapped_range_end_is_unsupported_at_the_global_address() {
        let mut board = Board::new();

        for (base, size) in [
            (RAM_BASE, RAM_SIZE),
            (FRAMEBUFFER_VRAM_BASE, FRAMEBUFFER_VRAM_SIZE),
            (DISPLAY_REGISTERS_BASE, DISPLAY_REGISTERS_SIZE),
            (KEYBOARD_REGISTERS_BASE, KEYBOARD_REGISTERS_SIZE),
        ] {
            let address = base + size - 1;
            let acknowledgement = board
                .slot_transaction(SlotRequest::read(address, SlotWidth::Q))
                .unwrap();

            assert_eq!(
                acknowledgement.failure(),
                Some(AcknowledgedBusFailure::new(
                    BusFailureCause::Other,
                    address,
                    RetrySafety::RetrySafe,
                ))
            );
        }
    }

    #[test]
    fn unmapped_slot_is_acknowledged_by_the_board_at_its_original_address() {
        let mut board = Board::new();
        let address = 0x00f3_0000;

        let acknowledgement = board
            .slot_transaction(SlotRequest::write(address, SlotData::Q(u64::MAX)))
            .unwrap();

        assert_eq!(
            acknowledgement.failure(),
            Some(AcknowledgedBusFailure::new(
                BusFailureCause::NoResponder,
                address,
                RetrySafety::RetrySafe,
            ))
        );
    }

    #[test]
    fn slot_requests_do_not_fall_back_to_byte_access_or_cause_byte_visible_effects() {
        let mut board = Board::new();
        board.load_ram(0, &[0x5a]).unwrap();
        board.framebuffer_mut().write_vram_u8(0, 0xa5).unwrap();
        board.keyboard_mut().push_event(0x1234_5678);
        let initial_dirty_sequence = board.framebuffer().dirty_seq();

        for address in [
            RAM_BASE,
            FRAMEBUFFER_VRAM_BASE,
            DISPLAY_REGISTERS_BASE + 0x0c,
            KEYBOARD_REGISTERS_BASE,
        ] {
            board
                .slot_transaction(SlotRequest::write(address, SlotData::Q(u64::MAX)))
                .unwrap();
        }
        board
            .slot_transaction(SlotRequest::read(KEYBOARD_REGISTERS_BASE + 4, SlotWidth::Q))
            .unwrap();

        assert_eq!(board.ram().as_slice()[0], 0x5a);
        assert_eq!(board.framebuffer().vram()[0], 0xa5);
        assert_eq!(board.framebuffer().dirty_seq(), initial_dirty_sequence);
        assert!(board.framebuffer().is_enabled());
        assert_eq!(board.keyboard().queued_len(), 1);
    }

    #[test]
    fn board_rebases_every_address_bearing_slot_error() {
        let base = 0x4000;
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
            assert_eq!(rebase_slot_error(local, base, request_address), expected);
        }
    }

    #[test]
    fn board_preserves_slot_lifecycle_errors() {
        for error in [BusError::TransactionActive, BusError::NoTransaction] {
            let error = SlotTransactionError::Bus(error);
            assert_eq!(rebase_slot_error(error.clone(), 0x4000, 0x4001), error);
        }
    }

    #[test]
    fn board_slot_error_overflow_uses_original_request_address() {
        let base = u64::MAX - 0x10;
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
            assert_eq!(rebase_slot_error(error, base, request_address), expected);
        }
    }
}
