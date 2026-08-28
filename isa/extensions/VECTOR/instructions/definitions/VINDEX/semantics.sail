function clause register_result_extension(Op_VINDEX) = RegisterZeroExtend

function clause repeat_semantics(Op_VINDEX) = RepeatObserveDestination

function clause vector_semantics(Op_VINDEX) = vector_default_semantics()

function execute_VINDEX_primitive(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) = {
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
        match vector_register_index(instruction, Operand_dst) {
            Some(destination) => {
                var updated = state;
                updated.vector_registers[unsigned(destination)] = vector_index_image(
                    zero_vector,
                    0,
                    lanes,
                    element_bytes,
                );
                Some(vector_finish(instruction, state, updated))
            },
            None() => None(),
        }
    } else {
        None()
    }
}

union clause Uop_kind = UopInstruction_VINDEX : unit

function clause execute_uop(UopInstruction_VINDEX(), _, values, instruction, before, speculative) =
    match execute_VINDEX_primitive(instruction, speculative) {
        Some(result) => vector_uop_step_from_local_result(result, instruction, before, speculative, values),
        None() => uop_step_fault(
            faulted(
                before,
                instruction.form.operation,
                IllegalInstruction,
                "VINDEX local vector primitive rejected its instruction",
            ),
        ),
    }

function execute_VINDEX(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
    Some(
        uop_program_execute(
            [|
                uop_make(
                    UopInstruction_VINDEX(),
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
