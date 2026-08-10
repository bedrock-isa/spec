#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum WatchAccess {
    Read,
    Write,
    ReadWrite,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct Watchpoint {
    pub start: u64,
    pub end_exclusive: u64,
    pub access: WatchAccess,
    pub enabled: bool,
}

impl Watchpoint {
    pub fn contains(self, addr: u64) -> bool {
        self.enabled && self.start <= addr && addr < self.end_exclusive
    }
}
