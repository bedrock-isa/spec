function execute_VREDXOR_primitive(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) = {
    let operation = instruction.form.operation;
    let element_bytes = operation_width(instruction);
    let lanes = tdiv_int(state.vector_length_bytes, element_bytes);
    match (
        vector_register_index(instruction, Operand_src),
        predicate_register_index(instruction, Operand_govern),
        operand_named(instruction, Operand_dst),
    ) {
        (Some(source), Some(predicate), Some(destination)) => {
            var updated = state;
            updated.registers[unsigned(destination.value[3 .. 0])] = get_slice_int(
                64,
                vector_integer_reduction_image(
                    operation,
                    state.vector_registers[unsigned(source)],
                    state.predicate_registers[unsigned(predicate)],
                    0,
                    lanes,
                    element_bytes,
                    vector_integer_reduction_identity(operation, element_bytes),
                ),
                0,
            );
            Some(vector_finish(instruction, state, updated))
        },
        _ => None(),
    }
}

union clause Uop_kind = UopInstruction_VREDXOR : unit

function clause execute_uop(UopInstruction_VREDXOR(), _, values, instruction, before, speculative) =
    match execute_VREDXOR_primitive(instruction, speculative) {
        Some(result) => vector_local_result_uop_step(result, instruction, before, speculative, values),
        None() => uop_fault(
            faulted(
                before,
                instruction.form.operation,
                IllegalInstruction,
                "VREDXOR local vector primitive rejected its instruction",
            ),
        ),
    }

function execute_VREDXOR(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
    Some(
        execute_uop_program(
            [|
                make_uop(
                    UopInstruction_VREDXOR(),
                    uop_none(),
                    uop_none(),
                    uop_none(),
                    Operand_dst,
                    operation_width(instruction),
                    CommitRegisters,
                ),
                make_uop(
                    UopCommit(),
                    uop_none(),
                    uop_none(),
                    uop_none(),
                    Operand_dst,
                    operation_width(instruction),
                    CommitRegisters,
                ),
            |],
            instruction,
            state,
        ),
    )
