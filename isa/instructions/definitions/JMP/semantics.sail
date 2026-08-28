
function execute_JMP(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) = {
    let result : Execution_result = match start_control_transaction(instruction, state) {
        Some(result) => result,
        None() => faulted(state, Op_JMP, IllegalInstruction, "missing JMP target"),
    };
    Some(result)
}
