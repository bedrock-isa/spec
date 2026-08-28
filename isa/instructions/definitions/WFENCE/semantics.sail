
function execute_WFENCE(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) = {
    let result : Execution_result = route_environment(instruction, state, FenceOperation, CommitControl, false);
    Some(result)
}
