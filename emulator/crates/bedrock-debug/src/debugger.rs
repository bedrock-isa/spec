use crate::breakpoint::BreakpointSet;
use crate::trace::TraceEvent;
use bedrock_core::StepResult;
use bedrock_machine::Machine;
use std::collections::VecDeque;

#[derive(Debug, Clone)]
pub struct Debugger {
    breakpoints: BreakpointSet,
    trace: VecDeque<TraceEvent>,
    trace_limit: usize,
}

impl Default for Debugger {
    fn default() -> Self {
        Self {
            breakpoints: BreakpointSet::default(),
            trace: VecDeque::new(),
            trace_limit: 1024,
        }
    }
}

impl Debugger {
    pub fn breakpoints(&self) -> &BreakpointSet {
        &self.breakpoints
    }

    pub fn breakpoints_mut(&mut self) -> &mut BreakpointSet {
        &mut self.breakpoints
    }

    pub fn trace(&self) -> &VecDeque<TraceEvent> {
        &self.trace
    }

    pub fn step(&mut self, machine: &mut Machine) -> StepResult {
        let pc = machine.state().pc;
        if self.breakpoints.contains_enabled(pc) {
            return StepResult::Breakpoint;
        }

        self.step_ignore_breakpoints(machine)
    }

    pub fn run_step(&self, machine: &mut Machine) -> StepResult {
        let pc = machine.state().pc;
        if self.breakpoints.contains_enabled(pc) {
            return StepResult::Breakpoint;
        }

        machine.step()
    }

    pub fn step_ignore_breakpoints(&mut self, machine: &mut Machine) -> StepResult {
        let pc = machine.state().pc;
        let result = machine.step();
        self.record_trace(TraceEvent {
            pc,
            result: result.clone(),
        });
        result
    }

    fn record_trace(&mut self, event: TraceEvent) {
        if self.trace.len() == self.trace_limit {
            self.trace.pop_front();
        }
        self.trace.push_back(event);
    }
}

#[cfg(test)]
mod tests {
    use super::Debugger;
    use bedrock_core::StepResult;
    use bedrock_machine::Machine;

    #[test]
    fn run_step_checks_breakpoints_without_recording_trace() {
        let mut machine = Machine::new();
        machine.load_program(0, &[0x01]).unwrap();
        machine.processor_reset(0);
        let mut debugger = Debugger::default();
        debugger.breakpoints_mut().add(0);

        assert_eq!(debugger.run_step(&mut machine), StepResult::Breakpoint);
        assert!(debugger.trace().is_empty());

        debugger.breakpoints_mut().remove(0);
        assert_eq!(debugger.run_step(&mut machine), StepResult::Running);
        assert!(debugger.trace().is_empty());
    }
}
