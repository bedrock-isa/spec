function clause register_result_extension(Op_VREDMAXU) = RegisterZeroExtend

function clause repeat_semantics(Op_VREDMAXU) = RepeatObserveDestination

function clause vector_semantics(Op_VREDMAXU) =
    {
        vector_default_semantics() with
        integer_reduction = Some(VectorReduceMaximumUnsigned),
        reduction = true,
        fp_allowed_causes = fflags_none,
    }

function execute_VREDMAXU_primitive(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) = {
    let operation = instruction.form.operation;
    let element_bytes = operation_width(instruction);
    let lanes = tdiv_int(state.vector_length_bytes, element_bytes);
    match (
        vector_register_index(instruction, Operand_src),
        predicate_register_index(instruction, Operand_govern),
        operand_named(instruction, Operand_dst),
    ) {
        (Some(source), Some(predicate), Some(destination)) => {
            var updated = state;
            updated.registers[unsigned(destination.value[3 .. 0])] = get_slice_int(
                64,
                vector_integer_reduction_image(
                    operation,
                    state.vector_registers[unsigned(source)],
                    state.predicate_registers[unsigned(predicate)],
                    0,
                    lanes,
                    element_bytes,
                    vector_integer_reduction_identity(operation, element_bytes),
                ),
                0,
            );
            Some(vector_finish(instruction, state, updated))
        },
        _ => None(),
    }
}

union clause Uop_kind = UopInstruction_VREDMAXU : unit

function clause execute_uop(UopInstruction_VREDMAXU(), _, values, instruction, before, speculative) =
    match execute_VREDMAXU_primitive(instruction, speculative) {
        Some(result) => vector_uop_step_from_local_result(result, instruction, before, speculative, values),
        None() => uop_step_fault(
            faulted(
                before,
                instruction.form.operation,
                IllegalInstruction,
                "VREDMAXU local vector primitive rejected its instruction",
            ),
        ),
    }

function execute_VREDMAXU(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
    Some(
        uop_program_execute(
            [|
                uop_make(
                    UopInstruction_VREDMAXU(),
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
