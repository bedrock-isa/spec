
function execute_CMPXCHG(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) = {
    let result : Execution_result = match start_atomic_transaction(instruction, state) {
        Some(result) => result,
        None() => faulted(state, instruction.form.operation, IllegalInstruction, "missing atomic memory operand"),
    };
    Some(result)
}
