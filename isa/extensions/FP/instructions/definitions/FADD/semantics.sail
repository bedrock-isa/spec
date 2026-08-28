
function execute_FADD(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
    Some(start_fp_transaction(instruction, state))
