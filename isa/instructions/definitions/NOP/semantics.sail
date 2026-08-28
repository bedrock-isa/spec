
function execute_NOP(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) = {
    let result : Execution_result = completed(state, advance_pc(state, instruction), CommitControl, [||]);
    Some(result)
}
