
function execute_LCALL(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) = {
    let result : Execution_result = match start_control_transaction(instruction, state) {
        Some(result) => result,
        None() => faulted(state, Op_LCALL, IllegalInstruction, "missing LCALL target"),
    };
    Some(result)
}
