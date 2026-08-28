
function execute_RDCR(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) = {
    let local_candidate : option(Execution_result) = match value_named(instruction, state, Operand_cr) {
        None() => None(),
        Some(raw_selector) => {
            let selector = unsigned(raw_selector[15 .. 0]);
            match control_index(selector) {
                Some(index) => Some(read_state_register(instruction, state, state.controls[unsigned(index)])),
                None() => Some(faulted(state, Op_RDCR, InvalidControlState, "unknown control-register selector")),
            }
        },
    };
    let result : Execution_result = match local_candidate {
        Some(result) => result,
        None() => start_system_request(instruction, state),
    };
    Some(result)
}
