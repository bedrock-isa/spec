
function execute_SUB(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) = {
    let local_candidate : option(Execution_result) = match execute_sp_arithmetic_local(
        instruction,
        state,
        IntegerArithmeticSubtract,
    ) {
        Some(result) => Some(result),
        None() => execute_integer_arithmetic_local(instruction, state, IntegerArithmeticSubtract),
    };
    let result : Execution_result = match local_candidate {
        Some(result) => result,
        None() => match start_memory_transaction(instruction, state) {
            Some(result) => result,
            None() => faulted(state, instruction.form.operation, IllegalInstruction, "unresolved integer ALU form"),
        },
    };
    Some(result)
}
