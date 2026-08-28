function execute_CMP_primitive(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) = {
    let width = operation_width(instruction);
    match (first_binary_operand(instruction.operands), second_binary_operand(instruction.operands)) {
        (Some(source_operand), Some(destination_operand)) => match (
            local_operand_value(state, source_operand),
            local_operand_value(state, destination_operand),
        ) {
            (Some(source), Some(destination)) => {
                let (_, flags) = sub_with_flags(destination, source, 0, width);
                Some(local_result(state, instruction, { state with flags = flags }, CommitRegisters))
            },
            _ => None(),
        },
        _ => None(),
    }
}

function execute_CMP(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) = {
    let result : Execution_result = match execute_CMP_primitive(instruction, state) {
        Some(result) => result,
        None() => match start_memory_transaction(instruction, state) {
            Some(result) => result,
            None() => faulted(state, instruction.form.operation, IllegalInstruction, "unresolved integer ALU form"),
        },
    };
    Some(result)
}
