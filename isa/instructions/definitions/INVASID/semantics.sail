
function execute_INVASID(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) = {
    let result : Execution_result = start_tlb_context_transaction(instruction, state);
    Some(result)
}
