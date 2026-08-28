function execute_VTRUNCL_primitive(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) = {
    let operation = instruction.form.operation;
    let element_bytes = operation_width(instruction);
    let lanes = tdiv_int(state.vector_length_bytes, element_bytes);
    let empty = zero_vector_bytes(tdiv_int(state.vector_length_bytes, 8));
    let zero_vector = zero_vector_bytes(state.vector_length_bytes);
    let fp_form : bool = match condition_size_field(instruction.fields) {
        Some(selector) => selector >= 5,
        None() => false,
    };
    if true | true | true | true | true | true | true | true | true then {
        match (
            vector_register_index(instruction, Operand_src),
            vector_register_index(instruction, Operand_dst),
            predicate_register_index(instruction, Operand_govern),
        ) {
            (Some(source), Some(destination), Some(predicate)) => {
                let destination_bytes = vector_width_change_destination_bytes(operation);
                let container_bytes = if element_bytes > destination_bytes then {
                        element_bytes
                    } else {
                        destination_bytes
                    };
                var updated = state;
                updated.vector_registers[unsigned(destination)] = vector_width_change_image(
                    operation,
                    state.vector_registers[unsigned(destination)],
                    state.vector_registers[unsigned(source)],
                    state.predicate_registers[unsigned(predicate)],
                    0,
                    tdiv_int(state.vector_length_bytes, container_bytes),
                    element_bytes,
                    destination_bytes,
                );
                Some(vector_finish(instruction, state, updated))
            },
            _ => None(),
        }
    } else {
        None()
    }
}

union clause Uop_kind = UopInstruction_VTRUNCL : unit

function clause execute_uop(UopInstruction_VTRUNCL(), _, values, instruction, before, speculative) =
    match execute_VTRUNCL_primitive(instruction, speculative) {
        Some(result) => vector_local_result_uop_step(result, instruction, before, speculative, values),
        None() => uop_fault(
            faulted(
                before,
                instruction.form.operation,
                IllegalInstruction,
                "VTRUNCL local vector primitive rejected its instruction",
            ),
        ),
    }

function execute_VTRUNCL(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
    Some(
        execute_uop_program(
            [|
                make_uop(
                    UopInstruction_VTRUNCL(),
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
