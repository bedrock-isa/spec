use bedrock_core::StepResult;

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct TraceEvent {
    pub pc: u64,
    pub result: StepResult,
}
