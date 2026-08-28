function execute_PLAST_primitive(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) = {
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
        match (predicate_register_index(instruction, Operand_predicate), operand_named(instruction, Operand_dst)) {
            (Some(source), Some(destination)) => {
                let result = if operation == Op_PCOUNT then {
                        predicate_count(state.predicate_registers[unsigned(source)], 0, lanes, element_bytes, 0)
                    } else {
                        if operation == Op_PFIRST then {
                            predicate_first(state.predicate_registers[unsigned(source)], 0, lanes, element_bytes)
                        } else {
                            predicate_last(state.predicate_registers[unsigned(source)], lanes - 1, element_bytes)
                        }
                    };
                var updated = state;
                updated.registers[unsigned(destination.value[3 .. 0])] =
                    if result < 0 then {
                        0xFFFFFFFFFFFFFFFF
                    } else {
                        get_slice_int(64, result, 0)
                    };
                Some(vector_finish(instruction, state, updated))
            },
            _ => None(),
        }
    } else {
        None()
    }
}

union clause Uop_kind = UopInstruction_PLAST : unit

function clause execute_uop(UopInstruction_PLAST(), _, values, instruction, before, speculative) =
    match execute_PLAST_primitive(instruction, speculative) {
        Some(result) => vector_local_result_uop_step(result, instruction, before, speculative, values),
        None() => uop_fault(
            faulted(
                before,
                instruction.form.operation,
                IllegalInstruction,
                "PLAST local vector primitive rejected its instruction",
            ),
        ),
    }

function execute_PLAST(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
    Some(
        execute_uop_program(
            [|
                make_uop(
                    UopInstruction_PLAST(),
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
