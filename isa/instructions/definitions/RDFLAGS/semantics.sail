
function execute_RDFLAGS(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) = {
    let result : Execution_result = match Some(
        read_state_register(instruction, state, sail_zero_extend(state.flags, 64)),
    ) {
        Some(result) => result,
        None() => start_system_request(instruction, state),
    };
    Some(result)
}
