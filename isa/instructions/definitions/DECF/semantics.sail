
function execute_DECF(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) = {
    let result : Execution_result = match execute_integer_single_operand_arithmetic_local(
        instruction,
        state,
        IntegerArithmeticSubtract,
        true,
    ) {
        Some(result) => result,
        None() => match start_memory_transaction(instruction, state) {
            Some(result) => result,
            None() => faulted(state, instruction.form.operation, IllegalInstruction, "unresolved integer unary form"),
        },
    };
    Some(result)
}
