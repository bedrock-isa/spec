
function execute_LJMP(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) = {
    let result : Execution_result = match start_control_transaction(instruction, state) {
        Some(result) => result,
        None() => faulted(state, Op_LJMP, IllegalInstruction, "missing LJMP target"),
    };
    Some(result)
}
