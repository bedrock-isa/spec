function execute_CMPJcc(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
    Some(
        match execute_subtract_compare_jump_local(instruction, state) {
            Some(result) => result,
            None() => faulted(state, Op_CMPJcc, IllegalInstruction, "CMPJcc local operands"),
        },
    )
