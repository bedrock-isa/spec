function clause register_result_extension(Op_VTRUNCW) = RegisterZeroExtend

function clause repeat_semantics(Op_VTRUNCW) = RepeatObserveDestination

function clause vector_semantics(Op_VTRUNCW) =
    {
        vector_default_semantics() with
        width_change = Some(VectorTruncate),
        width_change_destination_bytes = 2,
    }

function execute_VTRUNCW_primitive(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) = {
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

union clause Uop_kind = UopInstruction_VTRUNCW : unit

function clause execute_uop(UopInstruction_VTRUNCW(), _, values, instruction, before, speculative) =
    match execute_VTRUNCW_primitive(instruction, speculative) {
        Some(result) => vector_uop_step_from_local_result(result, instruction, before, speculative, values),
        None() => uop_step_fault(
            faulted(
                before,
                instruction.form.operation,
                IllegalInstruction,
                "VTRUNCW local vector primitive rejected its instruction",
            ),
        ),
    }

function execute_VTRUNCW(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
    Some(
        uop_program_execute(
            [|
                uop_make(
                    UopInstruction_VTRUNCW(),
                    uop_location_make_none(),
                    uop_location_make_none(),
                    uop_location_make_none(),
                    Operand_dst,
                    operation_width(instruction),
                    CommitRegisters,
                ),
                uop_make(
                    UopCommit(),
                    uop_location_make_none(),
                    uop_location_make_none(),
                    uop_location_make_none(),
                    Operand_dst,
                    operation_width(instruction),
                    CommitRegisters,
                ),
            |],
            instruction,
            state,
        ),
    )
