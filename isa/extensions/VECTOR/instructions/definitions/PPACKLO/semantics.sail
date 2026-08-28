function clause register_result_extension(Op_PPACKLO) = RegisterZeroExtend

function clause repeat_semantics(Op_PPACKLO) = RepeatObserveDestination

function clause vector_semantics(Op_PPACKLO) = vector_default_semantics()

function execute_PPACKLO_primitive(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) = {
    let operation = instruction.form.operation;
    let element_bytes = operation_width(instruction);
    let lanes = tdiv_int(state.vector_length_bytes, element_bytes);
    let empty = zero_vector_bytes(tdiv_int(state.vector_length_bytes, 8));
    let zero_vector = zero_vector_bytes(state.vector_length_bytes);
    let fp_form : bool = match condition_size_field(instruction.fields) {
        Some(selector) => selector >= 5,
        None() => false,
    };
    if true | true | true | true then {
        match (predicate_register_index(instruction, Operand_src), predicate_register_index(instruction, Operand_dst)) {
            (Some(source), Some(destination)) => {
                let source_image = state.predicate_registers[unsigned(source)];
                let image = predicate_pack_image(source_image, empty, 0, lanes, element_bytes, false);
                var updated = state;
                updated.predicate_registers[unsigned(destination)] = image;
                Some(vector_finish(instruction, state, updated))
            },
            _ => None(),
        }
    } else {
        None()
    }
}

union clause Uop_kind = UopInstruction_PPACKLO : unit

function clause execute_uop(UopInstruction_PPACKLO(), _, values, instruction, before, speculative) =
    match execute_PPACKLO_primitive(instruction, speculative) {
        Some(result) => vector_uop_step_from_local_result(result, instruction, before, speculative, values),
        None() => uop_step_fault(
            faulted(
                before,
                instruction.form.operation,
                IllegalInstruction,
                "PPACKLO local vector primitive rejected its instruction",
            ),
        ),
    }

function execute_PPACKLO(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
    Some(
        uop_program_execute(
            [|
                uop_make(
                    UopInstruction_PPACKLO(),
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
