use crate::board::{Board, RAM_BASE, RAM_SIZE};
use crate::loader::{ElfLoadError, ElfLoadOptions, ElfLoadResult, load_elf};
use bedrock_bus::BusResult;
use bedrock_core::{Cpu, CpuState, StepResult};

pub const DEFAULT_STACK_POINTER: u64 = RAM_BASE + RAM_SIZE;

#[derive(Debug, Clone, PartialEq, Eq, Default)]
pub struct Machine {
    cpu: Cpu,
    board: Board,
}

impl Machine {
    pub fn new() -> Self {
        Self::default()
    }

    pub fn cpu(&self) -> &Cpu {
        &self.cpu
    }

    pub fn cpu_mut(&mut self) -> &mut Cpu {
        &mut self.cpu
    }

    pub fn state(&self) -> &CpuState {
        self.cpu.state()
    }

    pub fn board(&self) -> &Board {
        &self.board
    }

    pub fn board_mut(&mut self) -> &mut Board {
        &mut self.board
    }

    pub fn processor_reset(&mut self, pc: u64) {
        self.cpu.reset(pc);
        self.cpu.state_mut().sp = DEFAULT_STACK_POINTER;
    }

    pub fn system_reset(&mut self, pc: u64) {
        self.board = Board::new();
        self.processor_reset(pc);
    }

    pub fn load_program(&mut self, addr: u64, bytes: &[u8]) -> BusResult<()> {
        self.board.load_ram(addr, bytes)
    }

    pub fn load_elf(
        &mut self,
        bytes: &[u8],
        options: ElfLoadOptions,
    ) -> Result<ElfLoadResult, ElfLoadError> {
        let result = load_elf(&mut self.board, bytes, options)?;
        self.processor_reset(result.entry);
        Ok(result)
    }

    pub fn step(&mut self) -> StepResult {
        self.cpu.step(&mut self.board)
    }
}

#[cfg(test)]
mod tests {
    use super::Machine;
    use bedrock_core::Status;

    #[test]
    fn processor_reset_preserves_board_state() {
        let mut machine = Machine::new();
        machine
            .board_mut()
            .framebuffer_mut()
            .write_vram_u8(0, 0xaa)
            .unwrap();
        machine.board_mut().keyboard_mut().push_event(0x0001_0041);
        machine.cpu_mut().state_mut().r[0] = 0xfeed;

        machine.processor_reset(0x1234);

        assert_eq!(machine.state().pc, 0x1234);
        assert_eq!(machine.state().sp, super::DEFAULT_STACK_POINTER);
        assert_eq!(machine.state().status, Status::PM);
        assert_eq!(machine.state().r[0], 0);
        assert_eq!(machine.board().framebuffer().vram()[0], 0xaa);
        assert_eq!(machine.board().keyboard().queued_len(), 1);
    }

    #[test]
    fn system_reset_clears_board_state() {
        let mut machine = Machine::new();
        machine
            .board_mut()
            .framebuffer_mut()
            .write_vram_u8(0, 0xaa)
            .unwrap();
        machine.board_mut().keyboard_mut().push_event(0x0001_0041);
        machine.cpu_mut().state_mut().r[0] = 0xfeed;

        machine.system_reset(0x5678);

        assert_eq!(machine.state().pc, 0x5678);
        assert_eq!(machine.state().sp, super::DEFAULT_STACK_POINTER);
        assert_eq!(machine.state().status, Status::PM);
        assert_eq!(machine.state().r[0], 0);
        assert_eq!(machine.board().framebuffer().vram()[0], 0);
        assert_eq!(machine.board().keyboard().queued_len(), 0);
    }
}
