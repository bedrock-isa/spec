use bedrock_bus::{AccessWidth, BusError, BusResult, Device};
use std::collections::BTreeMap;

pub const DEFAULT_FRAMEBUFFER_WIDTH: u32 = 320;
pub const DEFAULT_FRAMEBUFFER_HEIGHT: u32 = 200;
pub const RGB332_FORMAT_ID: u32 = 1;

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct FramebufferDevice {
    width: u32,
    height: u32,
    vram: Vec<u8>,
    enabled: bool,
    control: u32,
    dirty_seq: u64,
    transaction: Option<FramebufferTransaction>,
}

#[derive(Debug, Clone, PartialEq, Eq, Default)]
struct FramebufferTransaction {
    vram_writes: BTreeMap<usize, u8>,
    control: Option<u32>,
    dirty_writes: u64,
}

impl Default for FramebufferDevice {
    fn default() -> Self {
        Self::new(DEFAULT_FRAMEBUFFER_WIDTH, DEFAULT_FRAMEBUFFER_HEIGHT)
    }
}

impl FramebufferDevice {
    pub fn new(width: u32, height: u32) -> Self {
        let len = width as usize * height as usize;
        Self {
            width,
            height,
            vram: vec![0; len],
            enabled: true,
            control: 1,
            dirty_seq: 0,
            transaction: None,
        }
    }

    pub fn width(&self) -> u32 {
        self.width
    }

    pub fn height(&self) -> u32 {
        self.height
    }

    pub fn vram_len(&self) -> usize {
        self.vram.len()
    }

    pub fn dirty_seq(&self) -> u64 {
        self.dirty_seq
    }

    pub fn is_enabled(&self) -> bool {
        self.enabled
    }

    pub fn vram(&self) -> &[u8] {
        &self.vram
    }

    pub fn read_vram_u8(&mut self, offset: u64) -> BusResult<u8> {
        self.read_vram(offset, AccessWidth::Byte)
            .map(|value| value as u8)
    }

    pub fn write_vram_u8(&mut self, offset: u64, value: u8) -> BusResult<()> {
        self.write_vram(offset, AccessWidth::Byte, u64::from(value))
    }

    pub fn read_vram(&mut self, offset: u64, width: AccessWidth) -> BusResult<u64> {
        let indices = self.vram_indices(offset, width)?;
        let mut value = 0;
        for (byte, index) in indices.into_iter().enumerate() {
            let current = self
                .transaction
                .as_ref()
                .and_then(|transaction| transaction.vram_writes.get(&index).copied())
                .unwrap_or(self.vram[index]);
            value |= u64::from(current) << (byte * 8);
        }
        Ok(value)
    }

    pub fn write_vram(&mut self, offset: u64, width: AccessWidth, value: u64) -> BusResult<()> {
        let indices = self.vram_indices(offset, width)?;
        if let Some(transaction) = &mut self.transaction {
            for (byte, index) in indices.into_iter().enumerate() {
                transaction
                    .vram_writes
                    .insert(index, (value >> (byte * 8)) as u8);
            }
            transaction.dirty_writes = transaction.dirty_writes.wrapping_add(1);
        } else {
            for (byte, index) in indices.into_iter().enumerate() {
                self.vram[index] = (value >> (byte * 8)) as u8;
            }
            self.dirty_seq = self.dirty_seq.wrapping_add(1);
        }
        Ok(())
    }

    pub fn read_register_u8(&self, offset: u64) -> BusResult<u8> {
        self.read_register(offset, AccessWidth::Byte)
            .map(|value| value as u8)
    }

    pub fn read_register(&self, offset: u64, width: AccessWidth) -> BusResult<u64> {
        let mut result = 0;
        for byte in 0..width.bytes() {
            let current = offset
                .checked_add(byte)
                .ok_or(BusError::OutOfRange { addr: offset })?;
            result |= u64::from(self.read_register_byte(current)?) << (byte * 8);
        }
        Ok(result)
    }

    fn read_register_byte(&self, offset: u64) -> BusResult<u8> {
        let value = match offset {
            0x00..=0x03 => self.width as u64,
            0x04..=0x07 => self.height as u64,
            0x08..=0x0b => RGB332_FORMAT_ID as u64,
            0x0c..=0x0f => self
                .transaction
                .as_ref()
                .and_then(|transaction| transaction.control)
                .unwrap_or(self.control) as u64,
            0x10..=0x17 => self.dirty_seq.wrapping_add(
                self.transaction
                    .as_ref()
                    .map_or(0, |transaction| transaction.dirty_writes),
            ),
            _ => return Err(BusError::Unmapped { addr: offset }),
        };
        Ok(((value >> ((offset & 0x07) * 8)) & 0xff) as u8)
    }

    pub fn write_register_u8(&mut self, offset: u64, value: u8) -> BusResult<()> {
        self.write_register(offset, AccessWidth::Byte, u64::from(value))
    }

    pub fn write_register(&mut self, offset: u64, width: AccessWidth, value: u64) -> BusResult<()> {
        for byte in 0..width.bytes() {
            let current = offset
                .checked_add(byte)
                .ok_or(BusError::OutOfRange { addr: offset })?;
            match current {
                0x0c..=0x0f => {}
                0x00..=0x0b | 0x10..=0x17 => {
                    return Err(BusError::ReadOnly { addr: current });
                }
                _ => return Err(BusError::Unmapped { addr: current }),
            }
        }
        let mut control = self
            .transaction
            .as_ref()
            .and_then(|transaction| transaction.control)
            .unwrap_or(self.control);
        for byte in 0..width.bytes() {
            let shift = ((offset + byte - 0x0c) * 8) as u32;
            control &= !(0xff << shift);
            control |= (((value >> (byte * 8)) & 0xff) as u32) << shift;
        }
        if let Some(transaction) = &mut self.transaction {
            transaction.control = Some(control);
        } else {
            self.control = control;
            self.enabled = (self.control & 1) != 0;
        }
        Ok(())
    }

    pub fn rgb332_rgba(&self) -> Vec<u8> {
        let mut rgba = Vec::with_capacity(self.vram.len() * 4);
        for pixel in &self.vram {
            let r = (((pixel >> 5) & 0x07) as u16 * 255 / 7) as u8;
            let g = (((pixel >> 2) & 0x07) as u16 * 255 / 7) as u8;
            let b = ((pixel & 0x03) as u16 * 255 / 3) as u8;
            rgba.extend_from_slice(&[r, g, b, 0xff]);
        }
        rgba
    }

    fn vram_index(&self, offset: u64) -> BusResult<usize> {
        let index = usize::try_from(offset).map_err(|_| BusError::Unmapped { addr: offset })?;
        if index >= self.vram.len() {
            return Err(BusError::Unmapped { addr: offset });
        }
        Ok(index)
    }

    fn vram_indices(&self, offset: u64, width: AccessWidth) -> BusResult<Vec<usize>> {
        (0..width.bytes())
            .map(|byte| {
                offset
                    .checked_add(byte)
                    .ok_or(BusError::OutOfRange { addr: offset })
                    .and_then(|current| self.vram_index(current))
            })
            .collect()
    }
}

impl Device for FramebufferDevice {
    fn begin_transaction(&mut self) -> BusResult<()> {
        if self.transaction.is_some() {
            return Err(BusError::TransactionActive);
        }
        self.transaction = Some(FramebufferTransaction::default());
        Ok(())
    }

    fn commit_transaction(&mut self) {
        let Some(transaction) = self.transaction.take() else {
            return;
        };
        for (index, value) in transaction.vram_writes {
            self.vram[index] = value;
        }
        if let Some(control) = transaction.control {
            self.control = control;
            self.enabled = (control & 1) != 0;
        }
        self.dirty_seq = self.dirty_seq.wrapping_add(transaction.dirty_writes);
    }

    fn rollback_transaction(&mut self) {
        self.transaction = None;
    }

    fn read(&mut self, offset: u64, width: AccessWidth) -> BusResult<u64> {
        self.read_vram(offset, width)
    }

    fn write(&mut self, offset: u64, width: AccessWidth, value: u64) -> BusResult<()> {
        self.write_vram(offset, width, value)
    }
}

#[cfg(test)]
mod tests {
    use super::FramebufferDevice;
    use std::time::Instant;

    #[test]
    fn framebuffer_vram_read_write_marks_dirty() {
        let mut framebuffer = FramebufferDevice::default();

        framebuffer.write_vram_u8(12, 0xe3).unwrap();

        assert_eq!(framebuffer.read_vram_u8(12).unwrap(), 0xe3);
        assert_eq!(framebuffer.dirty_seq(), 1);
    }

    #[test]
    fn framebuffer_transaction_rolls_back_pixels_and_dirty_sequence() {
        use bedrock_bus::Device;
        let mut framebuffer = FramebufferDevice::default();
        framebuffer.begin_transaction().unwrap();
        framebuffer.write_vram_u8(4, 0xaa).unwrap();
        assert_eq!(framebuffer.read_vram_u8(4).unwrap(), 0xaa);
        framebuffer.rollback_transaction();
        assert_eq!(framebuffer.vram()[4], 0);
        assert_eq!(framebuffer.dirty_seq(), 0);
    }

    #[test]
    #[ignore]
    fn profile_rgb332_rgba_conversion() {
        const ITERATIONS: usize = 1_000;

        let mut framebuffer = FramebufferDevice::default();
        for index in 0..framebuffer.vram_len() as u64 {
            framebuffer.write_vram_u8(index, index as u8).unwrap();
        }

        let started = Instant::now();
        let mut bytes = 0;
        for _ in 0..ITERATIONS {
            bytes += framebuffer.rgb332_rgba().len();
        }
        let elapsed = started.elapsed();

        eprintln!(
            "rgb332_rgba {ITERATIONS}x {elapsed:?} ({:.3} ms/frame, {} bytes)",
            elapsed.as_secs_f64() * 1000.0 / ITERATIONS as f64,
            bytes
        );
    }
}
