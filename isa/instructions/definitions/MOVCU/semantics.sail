
function execute_MOVCU(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) = {
    let result : Execution_result = match execute_integer_move_local(instruction, state) {
        Some(result) => result,
        None() => match start_stack_transaction(instruction, state) {
            Some(result) => result,
            None() => match start_memory_transaction(instruction, state) {
                Some(result) => result,
                None() => faulted(
                    state,
                    instruction.form.operation,
                    IllegalInstruction,
                    "unresolved data-movement form",
                ),
            },
        },
    };
    Some(result)
}
