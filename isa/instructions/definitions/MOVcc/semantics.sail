
function execute_MOVcc(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) = {
    if not_bool(predicate_holds(instruction, state)) then {
        Some(completed(state, advance_pc(state, instruction), CommitRegisters, [||]))
    } else {
        Some(
            match execute_integer_move_local(instruction, state) {
                Some(result) => result,
                None() => match start_memory_transaction(instruction, state) {
                    Some(result) => result,
                    None() => faulted(state, Op_MOVcc, IllegalInstruction, "unresolved MOVcc form"),
                },
            },
        )
    }
}
