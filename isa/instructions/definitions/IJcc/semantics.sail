
function execute_IJcc(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) = {
    let result : Execution_result = execute_count_jump(instruction, state);
    Some(result)
}
