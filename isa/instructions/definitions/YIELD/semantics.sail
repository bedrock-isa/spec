
function execute_YIELD(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) = {
    let result : Execution_result = completed(
        state,
        advance_pc(state, instruction),
        CommitControl,
        [|typed_effect(NoEffect, instruction, state, 0x0000000000000000, 0x0000000000000000, 0, 0, false)|],
    );
    Some(result)
}
