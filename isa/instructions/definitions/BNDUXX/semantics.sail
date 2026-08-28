
function execute_BNDUXX(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) = {
    let result : Execution_result = match execute_bounds_comparison_local(instruction, state, false, false, false) {
        Some(result) => result,
        None() => match start_memory_transaction(instruction, state) {
            Some(result) => result,
            None() => faulted(state, instruction.form.operation, IllegalInstruction, "unresolved bounds form"),
        },
    };
    Some(result)
}
