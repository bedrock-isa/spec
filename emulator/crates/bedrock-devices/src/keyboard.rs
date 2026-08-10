use bedrock_bus::{BusError, BusResult, Device};
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

    fn read_u8(&mut self, offset: u64) -> BusResult<u8> {
        if self.transaction_active {
            let shadow = self.ensure_shadow();
            let value = match offset {
                0x00..=0x03 => status_for(&shadow.queue, shadow.overflow),
                0x04 => {
                    shadow.read_latch = shadow.queue.pop_front().unwrap_or(0);
                    shadow.read_latch
                }
                0x05..=0x07 => shadow.read_latch,
                _ => return Err(BusError::Unmapped { addr: offset }),
            };
            return Ok(((value >> ((offset & 0x03) * 8)) & 0xff) as u8);
        }
        let value = match offset {
            0x00..=0x03 => self.status(),
            0x04 => {
                self.read_latch = self.queue.pop_front().unwrap_or(0);
                self.read_latch
            }
            0x05..=0x07 => self.read_latch,
            _ => return Err(BusError::Unmapped { addr: offset }),
        };
        Ok(((value >> ((offset & 0x03) * 8)) & 0xff) as u8)
    }

    fn write_u8(&mut self, offset: u64, value: u8) -> BusResult<()> {
        if self.transaction_active {
            let shadow = self.ensure_shadow();
            match offset {
                0x08 => {
                    shadow.enabled = (value & 1) != 0;
                    if value & 0x02 != 0 {
                        shadow.queue.clear();
                        shadow.overflow = false;
                        shadow.read_latch = 0;
                    }
                    return Ok(());
                }
                0x09..=0x0b => return Ok(()),
                0x00..=0x07 => return Err(BusError::ReadOnly { addr: offset }),
                _ => return Err(BusError::Unmapped { addr: offset }),
            }
        }
        match offset {
            0x08 => {
                self.apply_control(value);
                Ok(())
            }
            0x09..=0x0b => Ok(()),
            0x00..=0x07 => Err(BusError::ReadOnly { addr: offset }),
            _ => Err(BusError::Unmapped { addr: offset }),
        }
    }
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
