
function execute_RDPMC(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) = {
    let result : Execution_result = start_system_request(instruction, state);
    Some(result)
}
