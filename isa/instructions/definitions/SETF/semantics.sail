
function execute_SETF(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) = {
    let local_candidate : option(Execution_result) = match value_named(instruction, state, Operand_mask) {
        Some(mask) => {
            let selected = mask[3 .. 0];
            Some(local_result(state, instruction, { state with flags = selected }, CommitRegisters))
        },
        None() => None(),
    };
    let result : Execution_result = match local_candidate {
        Some(result) => result,
        None() => start_system_request(instruction, state),
    };
    Some(result)
}
