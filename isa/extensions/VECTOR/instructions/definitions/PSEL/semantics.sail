function execute_PSEL_primitive(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) = {
    let operation = instruction.form.operation;
    let element_bytes = operation_width(instruction);
    let lanes = tdiv_int(state.vector_length_bytes, element_bytes);
    let empty = zero_vector_bytes(tdiv_int(state.vector_length_bytes, 8));
    let zero_vector = zero_vector_bytes(state.vector_length_bytes);
    let fp_form : bool = match condition_size_field(instruction.fields) {
        Some(selector) => selector >= 5,
        None() => false,
    };
    if true then {
        match (
            predicate_register_index(instruction, Operand_select),
            predicate_register_index(instruction, Operand_src),
            predicate_register_index(instruction, Operand_dst),
        ) {
            (Some(select), Some(source), Some(destination)) => {
                var updated = state;
                updated.predicate_registers[unsigned(destination)] = predicate_raw_select(
                    state.predicate_registers[unsigned(select)],
                    state.predicate_registers[unsigned(source)],
                    state.predicate_registers[unsigned(destination)],
                );
                Some(vector_finish(instruction, state, updated))
            },
            _ => None(),
        }
    } else {
        None()
    }
}

union clause Uop_kind = UopInstruction_PSEL : unit

function clause execute_uop(UopInstruction_PSEL(), _, values, instruction, before, speculative) =
    match execute_PSEL_primitive(instruction, speculative) {
        Some(result) => vector_local_result_uop_step(result, instruction, before, speculative, values),
        None() => uop_fault(
            faulted(
                before,
                instruction.form.operation,
                IllegalInstruction,
                "PSEL local vector primitive rejected its instruction",
            ),
        ),
    }

function execute_PSEL(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
    Some(
        execute_uop_program(
            [|
                make_uop(
                    UopInstruction_PSEL(),
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
