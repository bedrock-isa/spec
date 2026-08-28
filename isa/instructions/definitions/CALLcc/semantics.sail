
function execute_CALLcc(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) = {
    let result : Execution_result = match start_control_transaction(instruction, state) {
        Some(result) => result,
        None() => faulted(state, Op_CALLcc, IllegalInstruction, "missing CALLcc target"),
    };
    Some(result)
}
