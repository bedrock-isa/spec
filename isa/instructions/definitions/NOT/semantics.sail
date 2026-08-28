function execute_NOT_primitive(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) = {
    let width = operation_width(instruction);
    match unary_operand_local(instruction, state) {
        None() => None(),
        Some((old, destination)) => {
            let updated = write_local_destination(
                state,
                instruction.form.operation,
                destination,
                narrow_bits(not_vec(old), width),
            );
            Some(local_result(state, instruction, updated, CommitRegisters))
        },
    }
}

function execute_NOT(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) = {
    let result : Execution_result = match execute_NOT_primitive(instruction, state) {
        Some(result) => result,
        None() => match start_memory_transaction(instruction, state) {
            Some(result) => result,
            None() => faulted(state, instruction.form.operation, IllegalInstruction, "unresolved integer unary form"),
        },
    };
    Some(result)
}
