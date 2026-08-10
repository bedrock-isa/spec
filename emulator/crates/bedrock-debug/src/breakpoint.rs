#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct Breakpoint {
    pub addr: u64,
    pub enabled: bool,
}

#[derive(Debug, Clone, PartialEq, Eq, Default)]
pub struct BreakpointSet {
    breakpoints: Vec<Breakpoint>,
}

impl BreakpointSet {
    pub fn add(&mut self, addr: u64) {
        if self.breakpoints.iter().any(|bp| bp.addr == addr) {
            return;
        }
        self.breakpoints.push(Breakpoint {
            addr,
            enabled: true,
        });
    }

    pub fn remove(&mut self, addr: u64) {
        self.breakpoints.retain(|bp| bp.addr != addr);
    }

    pub fn contains_enabled(&self, addr: u64) -> bool {
        self.breakpoints
            .iter()
            .any(|bp| bp.enabled && bp.addr == addr)
    }

    pub fn all(&self) -> &[Breakpoint] {
        &self.breakpoints
    }
}
