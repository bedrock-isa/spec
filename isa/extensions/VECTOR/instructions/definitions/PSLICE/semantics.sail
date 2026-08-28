function execute_PSLICE_primitive(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) = {
    let operation = instruction.form.operation;
    let element_bytes = operation_width(instruction);
    let lanes = tdiv_int(state.vector_length_bytes, element_bytes);
    let empty = zero_vector_bytes(tdiv_int(state.vector_length_bytes, 8));
    let zero_vector = zero_vector_bytes(state.vector_length_bytes);
    let fp_form : bool = match condition_size_field(instruction.fields) {
        Some(selector) => selector >= 5,
        None() => false,
    };
    if true | true | true then {
        match (predicate_register_index(instruction, Operand_dst), operand_named(instruction, Operand_count)) {
            (Some(destination), Some(count_operand)) => {
                let source = if operation == Op_PSLICE then {
                        match predicate_register_index(instruction, Operand_src) {
                            Some(index) => state.predicate_registers[unsigned(index)],
                            None() => empty,
                        }
                    } else {
                        empty
                    };
                var updated = state;
                updated.predicate_registers[unsigned(destination)] = predicate_slide_image(
                    operation,
                    state.predicate_registers[unsigned(destination)],
                    source,
                    empty,
                    0,
                    lanes,
                    element_bytes,
                    unsigned(immediate_value(count_operand)),
                );
                Some(vector_finish(instruction, state, updated))
            },
            _ => None(),
        }
    } else {
        None()
    }
}

union clause Uop_kind = UopInstruction_PSLICE : unit

function clause execute_uop(UopInstruction_PSLICE(), _, values, instruction, before, speculative) =
    match execute_PSLICE_primitive(instruction, speculative) {
        Some(result) => vector_local_result_uop_step(result, instruction, before, speculative, values),
        None() => uop_fault(
            faulted(
                before,
                instruction.form.operation,
                IllegalInstruction,
                "PSLICE local vector primitive rejected its instruction",
            ),
        ),
    }

function execute_PSLICE(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
    Some(
        execute_uop_program(
            [|
                make_uop(
                    UopInstruction_PSLICE(),
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
