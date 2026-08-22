use bedrock_bus::{AccessWidth, Bus, BusError, BusResult, Device, PhysicalMemoryClass, Ram};
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

    fn read_access(&mut self, addr: u64, width: AccessWidth) -> BusResult<u64> {
        if let Some(offset) = offset_in(addr, RAM_BASE, RAM_SIZE) {
            return Device::read(&mut self.ram, offset, width)
                .map_err(|error| error.rebase_or_out_of_range(RAM_BASE, addr));
        }
        if let Some(offset) = offset_in(addr, FRAMEBUFFER_VRAM_BASE, FRAMEBUFFER_VRAM_SIZE) {
            return self
                .framebuffer
                .read_vram(offset, width)
                .map_err(|error| error.rebase_or_out_of_range(FRAMEBUFFER_VRAM_BASE, addr));
        }
        if let Some(offset) = offset_in(addr, DISPLAY_REGISTERS_BASE, DISPLAY_REGISTERS_SIZE) {
            return self
                .framebuffer
                .read_register(offset, width)
                .map_err(|error| error.rebase_or_out_of_range(DISPLAY_REGISTERS_BASE, addr));
        }
        if let Some(offset) = offset_in(addr, KEYBOARD_REGISTERS_BASE, KEYBOARD_REGISTERS_SIZE) {
            return Device::read(&mut self.keyboard, offset, width)
                .map_err(|error| error.rebase_or_out_of_range(KEYBOARD_REGISTERS_BASE, addr));
        }
        Err(BusError::Unmapped { addr })
    }

    fn write_access(&mut self, addr: u64, width: AccessWidth, value: u64) -> BusResult<()> {
        if let Some(offset) = offset_in(addr, RAM_BASE, RAM_SIZE) {
            return Device::write(&mut self.ram, offset, width, value)
                .map_err(|error| error.rebase_or_out_of_range(RAM_BASE, addr));
        }
        if let Some(offset) = offset_in(addr, FRAMEBUFFER_VRAM_BASE, FRAMEBUFFER_VRAM_SIZE) {
            return self
                .framebuffer
                .write_vram(offset, width, value)
                .map_err(|error| error.rebase_or_out_of_range(FRAMEBUFFER_VRAM_BASE, addr));
        }
        if let Some(offset) = offset_in(addr, DISPLAY_REGISTERS_BASE, DISPLAY_REGISTERS_SIZE) {
            return self
                .framebuffer
                .write_register(offset, width, value)
                .map_err(|error| error.rebase_or_out_of_range(DISPLAY_REGISTERS_BASE, addr));
        }
        if let Some(offset) = offset_in(addr, KEYBOARD_REGISTERS_BASE, KEYBOARD_REGISTERS_SIZE) {
            return Device::write(&mut self.keyboard, offset, width, value)
                .map_err(|error| error.rebase_or_out_of_range(KEYBOARD_REGISTERS_BASE, addr));
        }
        Err(BusError::Unmapped { addr })
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

    fn physical_memory_class(&self, addr: u64) -> PhysicalMemoryClass {
        if offset_in(addr, RAM_BASE, RAM_SIZE).is_some() {
            PhysicalMemoryClass::Normal
        } else if offset_in(addr, FRAMEBUFFER_VRAM_BASE, FRAMEBUFFER_VRAM_SIZE).is_some()
            || offset_in(addr, DISPLAY_REGISTERS_BASE, DISPLAY_REGISTERS_SIZE).is_some()
            || offset_in(addr, KEYBOARD_REGISTERS_BASE, KEYBOARD_REGISTERS_SIZE).is_some()
        {
            PhysicalMemoryClass::Device
        } else {
            // Unmapped accesses still fail at the target bus event. Classifying
            // holes as Normal avoids inventing a Device mapping for them.
            PhysicalMemoryClass::Normal
        }
    }

    fn read_u8(&mut self, addr: u64) -> BusResult<u8> {
        self.read_access(addr, AccessWidth::Byte)
            .map(|value| value as u8)
    }

    fn write_u8(&mut self, addr: u64, value: u8) -> BusResult<()> {
        self.write_access(addr, AccessWidth::Byte, u64::from(value))
    }

    fn read_u16(&mut self, addr: u64) -> BusResult<u16> {
        self.read_access(addr, AccessWidth::Word)
            .map(|value| value as u16)
    }

    fn read_u32(&mut self, addr: u64) -> BusResult<u32> {
        self.read_access(addr, AccessWidth::Long)
            .map(|value| value as u32)
    }

    fn read_u64(&mut self, addr: u64) -> BusResult<u64> {
        self.read_access(addr, AccessWidth::Quad)
    }

    fn write_u16(&mut self, addr: u64, value: u16) -> BusResult<()> {
        self.write_access(addr, AccessWidth::Word, u64::from(value))
    }

    fn write_u32(&mut self, addr: u64, value: u32) -> BusResult<()> {
        self.write_access(addr, AccessWidth::Long, u64::from(value))
    }

    fn write_u64(&mut self, addr: u64, value: u64) -> BusResult<()> {
        self.write_access(addr, AccessWidth::Quad, value)
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
    use bedrock_bus::{Bus, BusError, PhysicalMemoryClass};

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
    fn board_preserves_wide_mmio_event_width_and_side_effect_count() {
        let mut board = Board::new();
        board.write_u32(FRAMEBUFFER_VRAM_BASE, 0x4433_2211).unwrap();
        assert_eq!(board.framebuffer().dirty_seq(), 1);
        assert_eq!(board.read_u32(FRAMEBUFFER_VRAM_BASE).unwrap(), 0x4433_2211);

        board.keyboard_mut().push_event(0x0001_0041);
        board.keyboard_mut().push_event(0x0002_0042);
        assert_eq!(
            board.read_u32(KEYBOARD_REGISTERS_BASE + 4).unwrap(),
            0x0001_0041
        );
        assert_eq!(board.keyboard().queued_len(), 1);
        assert_eq!(
            board.read_u32(KEYBOARD_REGISTERS_BASE + 4).unwrap(),
            0x0002_0042
        );
        assert_eq!(board.keyboard().queued_len(), 0);
    }

    #[test]
    fn board_reports_platform_physical_memory_classes() {
        let board = Board::new();
        assert_eq!(
            board.physical_memory_class(RAM_BASE),
            PhysicalMemoryClass::Normal
        );
        assert_eq!(
            board.physical_memory_class(FRAMEBUFFER_VRAM_BASE),
            PhysicalMemoryClass::Device
        );
        assert_eq!(
            board.physical_memory_class(DISPLAY_REGISTERS_BASE),
            PhysicalMemoryClass::Device
        );
        assert_eq!(
            board.physical_memory_class(KEYBOARD_REGISTERS_BASE),
            PhysicalMemoryClass::Device
        );
    }
}
