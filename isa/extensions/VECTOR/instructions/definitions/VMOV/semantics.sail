function clause register_result_extension(Op_VMOV) = RegisterZeroExtend

function clause repeat_semantics(Op_VMOV) = RepeatObserveDestination

function clause vector_semantics(Op_VMOV) =
    {
        vector_default_semantics() with
        memory = Some(VectorMoveMerge),
    }

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
        Some(result) => vector_uop_step_from_local_result(result, instruction, before, speculative, values),
        None() => uop_step_fault(
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
        uop_program_execute(
            [|
                uop_make(
                    UopInstruction_VMOV(),
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
