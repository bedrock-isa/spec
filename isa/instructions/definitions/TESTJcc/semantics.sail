function execute_TESTJcc(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
    Some(
        match execute_and_compare_jump_local(instruction, state) {
            Some(result) => result,
            None() => faulted(state, Op_TESTJcc, IllegalInstruction, "TESTJcc local operands"),
        },
    )
