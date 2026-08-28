function execute_SBB_primitive(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) = {
    let width = operation_width(instruction);
    match binary_operands_local(instruction, state) {
        None() => None(),
        Some((source, destination, destination_ref)) => {
            let (value, flags) = sub_with_flags(destination, source, if flag_c(state.flags) then 1 else 0, width);
            var updated = write_local_destination(
                state,
                instruction.form.operation,
                destination_ref,
                narrow_bits(value, width),
            );
            updated.flags = flags;
            Some(local_result(state, instruction, updated, CommitRegisters))
        },
    }
}

function execute_SBB(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) = {
    let result : Execution_result = match execute_SBB_primitive(instruction, state) {
        Some(result) => result,
        None() => match start_memory_transaction(instruction, state) {
            Some(result) => result,
            None() => faulted(state, instruction.form.operation, IllegalInstruction, "unresolved integer ALU form"),
        },
    };
    Some(result)
}
