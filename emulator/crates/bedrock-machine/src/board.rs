use bedrock_bus::{Bus, BusError, BusResult, Device, Ram};
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
}

fn offset_in(addr: u64, base: u64, size: u64) -> Option<u64> {
    let end = base.checked_add(size)?;
    (base <= addr && addr < end).then(|| addr - base)
}

#[cfg(test)]
mod tests {
    use super::{
        Board, DISPLAY_REGISTERS_BASE, FRAMEBUFFER_VRAM_BASE, KEYBOARD_REGISTERS_BASE, RAM_BASE,
    };
    use bedrock_bus::{Bus, BusError};

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
}
