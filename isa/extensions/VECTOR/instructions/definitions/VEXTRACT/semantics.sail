function clause register_result_extension(Op_VEXTRACT) = RegisterZeroExtend

function clause repeat_semantics(Op_VEXTRACT) = RepeatObserveDestination

function clause vector_semantics(Op_VEXTRACT) =
    {
        vector_default_semantics() with
        fp_allowed_causes = fflags_none,
    }

function execute_VEXTRACT_primitive(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) = {
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
            vector_register_index(instruction, Operand_src),
            value_named(instruction, state, Operand_index),
            operand_named(instruction, Operand_dst),
        ) {
            (Some(source), Some(index_value), Some(destination)) => {
                let index = unsigned(index_value);
                if index >= lanes then {
                    Some(
                        faulted_with_error_code(
                            state,
                            operation,
                            VectorRangeFault,
                            "VEXTRACT lane index exceeds the lane count",
                            0x0000000000000001,
                        ),
                    )
                } else {
                    var updated = state;
                    updated.registers[unsigned(destination.value[3 .. 0])] = get_slice_int(
                        64,
                        vector_lane_unsigned(state.vector_registers[unsigned(source)], index, element_bytes),
                        0,
                    );
                    Some(vector_finish(instruction, state, updated))
                }
            },
            _ => None(),
        }
    } else {
        None()
    }
}

union clause Uop_kind = UopInstruction_VEXTRACT : unit

function clause execute_uop(UopInstruction_VEXTRACT(), _, values, instruction, before, speculative) =
    match execute_VEXTRACT_primitive(instruction, speculative) {
        Some(result) => vector_uop_step_from_local_result(result, instruction, before, speculative, values),
        None() => uop_step_fault(
            faulted(
                before,
                instruction.form.operation,
                IllegalInstruction,
                "VEXTRACT local vector primitive rejected its instruction",
            ),
        ),
    }

function execute_VEXTRACT(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
    Some(
        uop_program_execute(
            [|
                uop_make(
                    UopInstruction_VEXTRACT(),
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
