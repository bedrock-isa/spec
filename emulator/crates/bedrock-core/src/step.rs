use crate::Trap;

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum StepResult {
    Running,
    Halted,
    Breakpoint,
    Trap(Trap),
}
