
function execute_REPcc(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) = {
    let result : Execution_result = start_repeat_transaction(instruction, state);
    Some(result)
}
