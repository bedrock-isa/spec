use bedrock_core::CpuState;

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct CpuSnapshot {
    pub state: CpuState,
}

impl CpuSnapshot {
    pub fn new(state: &CpuState) -> Self {
        Self {
            state: state.clone(),
        }
    }
}
