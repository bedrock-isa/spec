
function execute_SEGLEA(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) = {
    Some(
        match execute_lea_transaction(instruction, state) {
            Some(result) => result,
            None() => faulted(state, instruction.form.operation, IllegalInstruction, "unresolved EA utility form"),
        },
    )
}
