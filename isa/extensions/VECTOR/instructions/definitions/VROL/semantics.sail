function clause register_result_extension(Op_VROL) = RegisterZeroExtend

function clause repeat_semantics(Op_VROL) = RepeatObserveDestination

function clause vector_semantics(Op_VROL) =
    {
        vector_default_semantics() with
        shift = Some(RotateLeft),
    }

function execute_VROL_primitive(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) = {
    let operation = instruction.form.operation;
    let element_bytes = operation_width(instruction);
    let lanes = tdiv_int(state.vector_length_bytes, element_bytes);
    let empty = zero_vector_bytes(tdiv_int(state.vector_length_bytes, 8));
    let zero_vector = zero_vector_bytes(state.vector_length_bytes);
    let fp_form : bool = match condition_size_field(instruction.fields) {
        Some(selector) => selector >= 5,
        None() => false,
    };
    if true | true | true | true | true then {
        match (vector_register_index(instruction, Operand_dst), predicate_register_index(instruction, Operand_govern)) {
            (Some(destination), Some(predicate)) => {
                let count_vector = vector_register_index(instruction, Operand_src);
                let counts : list(bits(8)) = match count_vector {
                    Some(index) => state.vector_registers[unsigned(index)],
                    None() => zero_vector,
                };
                let scalar_count : int = match operand_named(instruction, Operand_count) {
                    Some(count_operand) => unsigned(immediate_value(count_operand)),
                    None() => 0,
                };
                var updated = state;
                updated.vector_registers[unsigned(destination)] = vector_shift_image(
                    operation,
                    state.vector_registers[unsigned(destination)],
                    counts,
                    scalar_count,
                    count_vector != None(),
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

union clause Uop_kind = UopInstruction_VROL : unit

function clause execute_uop(UopInstruction_VROL(), _, values, instruction, before, speculative) =
    match execute_VROL_primitive(instruction, speculative) {
        Some(result) => vector_uop_step_from_local_result(result, instruction, before, speculative, values),
        None() => uop_step_fault(
            faulted(
                before,
                instruction.form.operation,
                IllegalInstruction,
                "VROL local vector primitive rejected its instruction",
            ),
        ),
    }

function execute_VROL(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
    Some(
        uop_program_execute(
            [|
                uop_make(
                    UopInstruction_VROL(),
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
