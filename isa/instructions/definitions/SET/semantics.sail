
function execute_SET(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) = {
    let result : Execution_result = match execute_set_local(instruction, state) {
        Some(result) => result,
        None() => match start_memory_transaction(instruction, state) {
            Some(result) => result,
            None() => faulted(state, Op_SET, IllegalInstruction, "unresolved SET form"),
        },
    };
    Some(result)
}
