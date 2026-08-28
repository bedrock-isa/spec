function clause register_result_extension(Op_VREVBYTE) = RegisterZeroExtend

function clause repeat_semantics(Op_VREVBYTE) = RepeatObserveDestination

function clause vector_semantics(Op_VREVBYTE) =
    {
        vector_default_semantics() with
        integer_unary = Some(VectorUnaryReverseBytes),
    }

function execute_VREVBYTE_primitive(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) = {
    let operation = instruction.form.operation;
    let element_bytes = operation_width(instruction);
    let lanes = tdiv_int(state.vector_length_bytes, element_bytes);
    let empty = zero_vector_bytes(tdiv_int(state.vector_length_bytes, 8));
    let zero_vector = zero_vector_bytes(state.vector_length_bytes);
    let fp_form : bool = match condition_size_field(instruction.fields) {
        Some(selector) => selector >= 5,
        None() => false,
    };
    if (true | true | true | true | true | true | true | true) & not_bool(fp_form) then {
        match (vector_register_index(instruction, Operand_dst), predicate_register_index(instruction, Operand_govern)) {
            (Some(destination), Some(predicate)) => {
                var updated = state;
                updated.vector_registers[unsigned(destination)] = vector_integer_unary_image(
                    operation,
                    state.vector_registers[unsigned(destination)],
                    state.predicate_registers[unsigned(predicate)],
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

union clause Uop_kind = UopInstruction_VREVBYTE : unit

function clause execute_uop(UopInstruction_VREVBYTE(), _, values, instruction, before, speculative) =
    match execute_VREVBYTE_primitive(instruction, speculative) {
        Some(result) => vector_uop_step_from_local_result(result, instruction, before, speculative, values),
        None() => uop_step_fault(
            faulted(
                before,
                instruction.form.operation,
                IllegalInstruction,
                "VREVBYTE local vector primitive rejected its instruction",
            ),
        ),
    }

function execute_VREVBYTE(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
    Some(
        uop_program_execute(
            [|
                uop_make(
                    UopInstruction_VREVBYTE(),
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
