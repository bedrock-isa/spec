function execute_OR_primitive(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) = {
    let width = operation_width(instruction);
    match binary_operands_local(instruction, state) {
        None() => None(),
        Some((source, destination, destination_ref)) => {
            let updated = write_local_destination(
                state,
                instruction.form.operation,
                destination_ref,
                narrow_bits(destination | source, width),
            );
            Some(local_result(state, instruction, updated, CommitRegisters))
        },
    }
}

function execute_OR(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) = {
    let result : Execution_result = match execute_OR_primitive(instruction, state) {
        Some(result) => result,
        None() => match start_memory_transaction(instruction, state) {
            Some(result) => result,
            None() => faulted(state, instruction.form.operation, IllegalInstruction, "unresolved integer ALU form"),
        },
    };
    Some(result)
}
