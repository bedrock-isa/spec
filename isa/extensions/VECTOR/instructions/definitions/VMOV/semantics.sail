function execute_VMOV_primitive(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) = {
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
        match (vector_register_index(instruction, Operand_src), vector_register_index(instruction, Operand_dst)) {
            (Some(source), Some(destination)) => {
                var updated = state;
                updated.vector_registers[unsigned(destination)] = match predicate_register_index(
                    instruction,
                    Operand_govern,
                ) {
                    Some(predicate) => vector_merge_image(
                        state.vector_registers[unsigned(destination)],
                        state.vector_registers[unsigned(source)],
                        state.predicate_registers[unsigned(predicate)],
                        0,
                        lanes,
                        element_bytes,
                    ),
                    None() => state.vector_registers[unsigned(source)],
                };
                Some(vector_finish(instruction, state, updated))
            },
            _ => None(),
        }
    } else {
        None()
    }
}

union clause Uop_kind = UopInstruction_VMOV : unit

function clause execute_uop(UopInstruction_VMOV(), _, values, instruction, before, speculative) =
    match execute_VMOV_primitive(instruction, speculative) {
        Some(result) => vector_local_result_uop_step(result, instruction, before, speculative, values),
        None() => uop_fault(
            faulted(
                before,
                instruction.form.operation,
                IllegalInstruction,
                "VMOV local vector primitive rejected its instruction",
            ),
        ),
    }

function execute_VMOV(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
    Some(
        execute_uop_program(
            [|
                make_uop(
                    UopInstruction_VMOV(),
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
