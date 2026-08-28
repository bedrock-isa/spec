
function execute_RDFSTATUS(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) = {
    let result : Execution_result = match Some(read_state_register(instruction, state, narrow_bits(state.fstatus, 2))) {
        Some(result) => result,
        None() => start_system_request(instruction, state),
    };
    Some(result)
}
