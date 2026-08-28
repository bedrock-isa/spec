function execute_VTESTZ_primitive(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) = {
    let operation = instruction.form.operation;
    let element_bytes = operation_width(instruction);
    let lanes = tdiv_int(state.vector_length_bytes, element_bytes);
    let empty = zero_vector_bytes(tdiv_int(state.vector_length_bytes, 8));
    let zero_vector = zero_vector_bytes(state.vector_length_bytes);
    let fp_form : bool = match condition_size_field(instruction.fields) {
        Some(selector) => selector >= 5,
        None() => false,
    };
    if (true | true | true) & not_bool(fp_form) then {
        match (
            vector_register_index(instruction, Operand_lhs),
            vector_register_index(instruction, Operand_rhs),
            predicate_register_index(instruction, Operand_govern),
            predicate_register_index(instruction, Operand_dst),
        ) {
            (Some(left), Some(right), Some(govern), Some(destination)) => {
                let condition : int = match operand_named(instruction, Operand_cc) {
                    Some(value) => unsigned(value.value[3 .. 0]),
                    None() => 0,
                };
                var updated = state;
                updated.predicate_registers[unsigned(destination)] = vector_integer_compare_image(
                    operation,
                    condition,
                    state.vector_registers[unsigned(left)],
                    state.vector_registers[unsigned(right)],
                    state.predicate_registers[unsigned(govern)],
                    empty,
                    0,
                    lanes,
                    element_bytes,
                );
                Some(vector_finish(instruction, state, updated))
            },
            _ => None(),
        }
    } else {
        None()
    }
}

union clause Uop_kind = UopInstruction_VTESTZ : unit

function clause execute_uop(UopInstruction_VTESTZ(), _, values, instruction, before, speculative) =
    match execute_VTESTZ_primitive(instruction, speculative) {
        Some(result) => vector_local_result_uop_step(result, instruction, before, speculative, values),
        None() => uop_fault(
            faulted(
                before,
                instruction.form.operation,
                IllegalInstruction,
                "VTESTZ local vector primitive rejected its instruction",
            ),
        ),
    }

function execute_VTESTZ(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
    Some(
        execute_uop_program(
            [|
                make_uop(
                    UopInstruction_VTESTZ(),
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
