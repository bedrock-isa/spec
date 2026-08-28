function execute_CLR_primitive(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) = {
    let width = operation_width(instruction);
    match operand_named(instruction, Operand_dst) {
        None() => None(),
        Some(operand) => match local_destination(operand, width) {
            None() => None(),
            Some(destination) => {
                let updated = write_local_destination(
                    state,
                    instruction.form.operation,
                    destination,
                    0x0000000000000000,
                );
                Some(local_result(state, instruction, updated, CommitRegisters))
            },
        },
    }
}

function execute_CLR(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) = {
    let result : Execution_result = match execute_CLR_primitive(instruction, state) {
        Some(result) => result,
        None() => match start_memory_transaction(instruction, state) {
            Some(result) => result,
            None() => faulted(state, instruction.form.operation, IllegalInstruction, "unresolved integer unary form"),
        },
    };
    Some(result)
}
