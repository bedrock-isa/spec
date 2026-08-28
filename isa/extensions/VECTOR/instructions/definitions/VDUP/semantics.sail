function execute_VDUP_primitive(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) = {
    let operation = instruction.form.operation;
    let element_bytes = operation_width(instruction);
    let lanes = tdiv_int(state.vector_length_bytes, element_bytes);
    let empty = zero_vector_bytes(tdiv_int(state.vector_length_bytes, 8));
    let zero_vector = zero_vector_bytes(state.vector_length_bytes);
    let fp_form : bool = match condition_size_field(instruction.fields) {
        Some(selector) => selector >= 5,
        None() => false,
    };
    if not_bool(fp_form) then {
        match (
            value_named(instruction, state, Operand_src),
            value_named(instruction, state, Operand_immediate),
            vector_register_index(instruction, Operand_dst),
        ) {
            (Some(source), _, Some(destination)) => {
                let image = vector_duplicate_image(zero_vector, 0, lanes, element_bytes, unsigned(source));
                var updated = state;
                updated.vector_registers[unsigned(destination)] = image;
                Some(vector_finish(instruction, state, updated))
            },
            (_, Some(source), Some(destination)) => {
                let image = vector_duplicate_image(zero_vector, 0, lanes, element_bytes, unsigned(source));
                var updated = state;
                updated.vector_registers[unsigned(destination)] = image;
                Some(vector_finish(instruction, state, updated))
            },
            _ => None(),
        }
    } else {
        None()
    }
}

union clause Uop_kind = UopInstruction_VDUP : unit

function clause execute_uop(UopInstruction_VDUP(), _, values, instruction, before, speculative) =
    match execute_VDUP_primitive(instruction, speculative) {
        Some(result) => vector_local_result_uop_step(result, instruction, before, speculative, values),
        None() => uop_fault(
            faulted(
                before,
                instruction.form.operation,
                IllegalInstruction,
                "VDUP local vector primitive rejected its instruction",
            ),
        ),
    }

function execute_VDUP(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
    Some(
        execute_uop_program(
            [|
                make_uop(
                    UopInstruction_VDUP(),
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
