
function execute_ILLEGAL(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) = {
    let result : Execution_result = faulted(state, Op_ILLEGAL, IllegalInstruction, "explicit ILLEGAL");
    Some(result)
}
