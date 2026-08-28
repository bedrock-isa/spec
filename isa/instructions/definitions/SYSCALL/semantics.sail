
function execute_SYSCALL(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) = {
    let result : Execution_result = start_event_control(instruction, state);
    Some(result)
}
