function clause register_result_extension(Op_PUZIPHI) = RegisterZeroExtend

function clause repeat_semantics(Op_PUZIPHI) = RepeatObserveDestination

function clause vector_semantics(Op_PUZIPHI) =
    {
        vector_default_semantics() with
        predicate_pair = Some(PredicateUnzipHigh),
    }

function execute_PUZIPHI_primitive(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) = {
    let operation = instruction.form.operation;
    let element_bytes = operation_width(instruction);
    let lanes = tdiv_int(state.vector_length_bytes, element_bytes);
    let empty = zero_vector_bytes(tdiv_int(state.vector_length_bytes, 8));
    let zero_vector = zero_vector_bytes(state.vector_length_bytes);
    let fp_form : bool = match condition_size_field(instruction.fields) {
        Some(selector) => selector >= 5,
        None() => false,
    };
    if true | true | true | true | true | true then {
        match (
            predicate_register_index(instruction, Operand_lhs),
            predicate_register_index(instruction, Operand_rhs),
            predicate_register_index(instruction, Operand_dst),
        ) {
            (Some(left), Some(right), Some(destination)) => {
                var updated = state;
                updated.predicate_registers[unsigned(destination)] = predicate_pair_image(
                    operation,
                    state.predicate_registers[unsigned(left)],
                    state.predicate_registers[unsigned(right)],
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

union clause Uop_kind = UopInstruction_PUZIPHI : unit

function clause execute_uop(UopInstruction_PUZIPHI(), _, values, instruction, before, speculative) =
    match execute_PUZIPHI_primitive(instruction, speculative) {
        Some(result) => vector_uop_step_from_local_result(result, instruction, before, speculative, values),
        None() => uop_step_fault(
            faulted(
                before,
                instruction.form.operation,
                IllegalInstruction,
                "PUZIPHI local vector primitive rejected its instruction",
            ),
        ),
    }

function execute_PUZIPHI(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
    Some(
        uop_program_execute(
            [|
                uop_make(
                    UopInstruction_PUZIPHI(),
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
