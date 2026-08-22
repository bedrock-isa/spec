use bedrock_bus::{AccessWidth, BusError, BusResult, Device};
use std::collections::VecDeque;

pub const DEFAULT_KEYBOARD_CAPACITY: usize = 256;
const STATUS_DATA_AVAILABLE: u32 = 1 << 0;
const STATUS_OVERFLOW: u32 = 1 << 1;

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct KeyboardDevice {
    enabled: bool,
    overflow: bool,
    capacity: usize,
    queue: VecDeque<u32>,
    read_latch: u32,
    transaction_active: bool,
    transaction: Option<KeyboardShadow>,
}

#[derive(Debug, Clone, PartialEq, Eq)]
struct KeyboardShadow {
    enabled: bool,
    overflow: bool,
    queue: VecDeque<u32>,
    read_latch: u32,
}

impl Default for KeyboardDevice {
    fn default() -> Self {
        Self::new(DEFAULT_KEYBOARD_CAPACITY)
    }
}

impl KeyboardDevice {
    pub fn new(capacity: usize) -> Self {
        Self {
            enabled: true,
            overflow: false,
            capacity,
            queue: VecDeque::with_capacity(capacity),
            read_latch: 0,
            transaction_active: false,
            transaction: None,
        }
    }

    pub fn push_event(&mut self, event: u32) {
        if !self.enabled {
            return;
        }

        if self.queue.len() >= self.capacity {
            self.overflow = true;
            return;
        }

        self.queue.push_back(event);
    }

    pub fn queued_len(&self) -> usize {
        self.queue.len()
    }

    pub fn capacity(&self) -> usize {
        self.capacity
    }

    pub fn has_overflowed(&self) -> bool {
        self.overflow
    }

    pub fn set_enabled(&mut self, enabled: bool) {
        self.enabled = enabled;
    }

    pub fn clear(&mut self) {
        self.queue.clear();
        self.overflow = false;
        self.read_latch = 0;
    }

    pub fn status(&self) -> u32 {
        if let Some(shadow) = &self.transaction {
            return status_for(&shadow.queue, shadow.overflow);
        }
        status_for(&self.queue, self.overflow)
    }

    fn ensure_shadow(&mut self) -> &mut KeyboardShadow {
        self.transaction.get_or_insert_with(|| KeyboardShadow {
            enabled: self.enabled,
            overflow: self.overflow,
            queue: self.queue.clone(),
            read_latch: self.read_latch,
        })
    }

    pub fn is_enabled(&self) -> bool {
        self.enabled
    }

    fn apply_control(&mut self, value: u8) {
        self.enabled = (value & 1) != 0;
        if (value & 0x02) != 0 {
            self.clear();
        }
    }
}

impl Device for KeyboardDevice {
    fn begin_transaction(&mut self) -> BusResult<()> {
        if self.transaction_active {
            return Err(BusError::TransactionActive);
        }
        self.transaction_active = true;
        self.transaction = None;
        Ok(())
    }

    fn commit_transaction(&mut self) {
        if let Some(shadow) = self.transaction.take() {
            self.enabled = shadow.enabled;
            self.overflow = shadow.overflow;
            self.queue = shadow.queue;
            self.read_latch = shadow.read_latch;
        }
        self.transaction_active = false;
    }

    fn rollback_transaction(&mut self) {
        self.transaction = None;
        self.transaction_active = false;
    }

    fn read(&mut self, offset: u64, width: AccessWidth) -> BusResult<u64> {
        let end = offset
            .checked_add(width.bytes() - 1)
            .ok_or(BusError::OutOfRange { addr: offset })?;
        if end > 0x07 {
            return Err(BusError::Unmapped { addr: end });
        }
        if self.transaction_active {
            let shadow = self.ensure_shadow();
            return Ok(read_keyboard_width(
                &mut shadow.queue,
                shadow.overflow,
                &mut shadow.read_latch,
                offset,
                width,
            ));
        }
        Ok(read_keyboard_width(
            &mut self.queue,
            self.overflow,
            &mut self.read_latch,
            offset,
            width,
        ))
    }

    fn write(&mut self, offset: u64, width: AccessWidth, value: u64) -> BusResult<()> {
        let end = offset
            .checked_add(width.bytes() - 1)
            .ok_or(BusError::OutOfRange { addr: offset })?;
        for current in offset..=end {
            match current {
                0x08..=0x0b => {}
                0x00..=0x07 => return Err(BusError::ReadOnly { addr: current }),
                _ => return Err(BusError::Unmapped { addr: current }),
            }
        }
        let control = if offset == 0x08 {
            Some(value as u8)
        } else {
            None
        };
        if self.transaction_active {
            let shadow = self.ensure_shadow();
            if let Some(control) = control {
                shadow.enabled = (control & 1) != 0;
                if control & 0x02 != 0 {
                    shadow.queue.clear();
                    shadow.overflow = false;
                    shadow.read_latch = 0;
                }
            }
            return Ok(());
        }
        if let Some(control) = control {
            self.apply_control(control);
        }
        Ok(())
    }
}

fn read_keyboard_width(
    queue: &mut VecDeque<u32>,
    overflow: bool,
    read_latch: &mut u32,
    offset: u64,
    width: AccessWidth,
) -> u64 {
    let status = status_for(queue, overflow);
    if offset <= 0x04 && offset + width.bytes() > 0x04 {
        *read_latch = queue.pop_front().unwrap_or(0);
    }
    let mut result = 0;
    for byte in 0..width.bytes() {
        let current = offset + byte;
        let register = if current <= 0x03 { status } else { *read_latch };
        result |= u64::from((register >> ((current & 0x03) * 8)) & 0xff) << (byte * 8);
    }
    result
}

fn status_for(queue: &VecDeque<u32>, overflow: bool) -> u32 {
    let mut status = 0;
    if !queue.is_empty() {
        status |= STATUS_DATA_AVAILABLE;
    }
    if overflow {
        status |= STATUS_OVERFLOW;
    }
    status
}

#[cfg(test)]
mod tests {
    use super::KeyboardDevice;
    use bedrock_bus::Device;

    #[test]
    fn keyboard_reports_and_pops_events() {
        let mut keyboard = KeyboardDevice::new(4);
        keyboard.push_event(0x0001_0041);

        assert_eq!(keyboard.read_u8(0).unwrap() & 0x01, 0x01);
        assert_eq!(keyboard.read_u8(4).unwrap(), 0x41);
        assert_eq!(keyboard.read_u8(5).unwrap(), 0x00);
        assert_eq!(keyboard.read_u8(6).unwrap(), 0x01);
        assert_eq!(keyboard.read_u8(7).unwrap(), 0x00);
        assert_eq!(keyboard.read_u8(0).unwrap() & 0x01, 0x00);
    }

    #[test]
    fn keyboard_transaction_rolls_back_destructive_read() {
        let mut keyboard = KeyboardDevice::new(4);
        keyboard.push_event(0x41);
        keyboard.begin_transaction().unwrap();
        assert_eq!(keyboard.read_u8(4).unwrap(), 0x41);
        keyboard.rollback_transaction();
        assert_eq!(keyboard.queued_len(), 1);
    }
}
