
function execute_PTQUERY(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
    Some(start_tlb_context_transaction(instruction, state))
