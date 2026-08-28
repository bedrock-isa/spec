function clause fp_semantics(Op_RDFFLAGS) = None()

function clause register_result_extension(Op_RDFFLAGS) = RegisterZeroExtend

function clause repeat_semantics(Op_RDFFLAGS) = RepeatObserveDestination

function execute_RDFFLAGS_primitive(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) = {
    let result : Execution_result = match Some(
        read_state_register(instruction, state, sail_zero_extend(state.fflags, 64)),
    ) {
        Some(result) => result,
        None() => faulted(state, instruction.form.operation, IllegalInstruction, "missing RDFFLAGS destination"),
    };
    Some(result)
}

union clause Uop_kind = UopInstruction_RDFFLAGS : unit

function clause execute_uop(UopInstruction_RDFFLAGS(), _, values, instruction, _, speculative) =
    match execute_RDFFLAGS_primitive(instruction, speculative) {
        Some(result) => uop_step_from_local_result(result, speculative, values),
        None() => uop_step_fault(
            faulted(
                speculative,
                instruction.form.operation,
                IllegalInstruction,
                "RDFFLAGS local primitive rejected its instruction",
            ),
        ),
    }

function execute_RDFFLAGS(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
    Some(
        uop_program_execute(
            [|
                uop_make(
                    UopInstruction_RDFFLAGS(),
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
