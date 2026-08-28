function clause register_result_extension(Op_PFALSE) = RegisterZeroExtend

function clause repeat_semantics(Op_PFALSE) = RepeatObserveDestination

function clause vector_semantics(Op_PFALSE) = vector_default_semantics()

function execute_PFALSE_primitive(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) = {
    let element_bytes = operation_width(instruction);
    let lanes = tdiv_int(state.vector_length_bytes, element_bytes);
    let empty = zero_vector_bytes(tdiv_int(state.vector_length_bytes, 8));
    match predicate_register_index(instruction, Operand_dst) {
        None() => None(),
        Some(destination) => {
            var updated = state;
            updated.predicate_registers[unsigned(destination)] = predicate_fill_typed(
                empty,
                0,
                lanes,
                element_bytes,
                0,
                0,
            );
            Some(vector_finish(instruction, state, updated))
        },
    }
}

union clause Uop_kind = UopInstruction_PFALSE : unit

function clause execute_uop(UopInstruction_PFALSE(), _, values, instruction, before, speculative) =
    match execute_PFALSE_primitive(instruction, speculative) {
        Some(result) => vector_uop_step_from_local_result(result, instruction, before, speculative, values),
        None() => uop_step_fault(
            faulted(
                before,
                instruction.form.operation,
                IllegalInstruction,
                "PFALSE local vector primitive rejected its instruction",
            ),
        ),
    }

function execute_PFALSE(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
    Some(
        uop_program_execute(
            [|
                uop_make(
                    UopInstruction_PFALSE(),
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
