
function execute_FBNDXX(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) = {
    let result : Execution_result = start_fp_transaction(instruction, state);
    Some(result)
}
