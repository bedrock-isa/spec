#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct InstructionAttributes {
    pub instruction_set: crate::InstructionSet,
    pub privileged: bool,
    pub repeat_rep: bool,
    pub repeat_repcc: bool,
    pub repeat_repg: bool,
    pub repeat_observed: Option<crate::RepeatObservation>,
    pub flags: crate::FlagsEffect,
}
