
function execute_TRACE(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) = {
    let result : Execution_result = completed(
        state,
        advance_pc(state, instruction),
        CommitControl,
        [|
            typed_effect(
                TraceMarker,
                instruction,
                state,
                state.pc,
                match value_named(instruction, state, Operand_marker) {
                    Some(value) => value,
                    None() => 0x0000000000000000,
                },
                2,
                0,
                false,
            ),
        |],
    );
    Some(result)
}
