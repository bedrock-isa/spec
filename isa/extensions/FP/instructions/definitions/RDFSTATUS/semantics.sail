function clause fp_semantics(Op_RDFSTATUS) = None()

function clause register_result_extension(Op_RDFSTATUS) = RegisterZeroExtend

function clause repeat_semantics(Op_RDFSTATUS) = RepeatObserveDestination

function execute_RDFSTATUS_primitive(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) = {
    let result : Execution_result = match Some(read_state_register(instruction, state, narrow_bits(state.fstatus, 2))) {
        Some(result) => result,
        None() => faulted(state, instruction.form.operation, IllegalInstruction, "missing RDFSTATUS destination"),
    };
    Some(result)
}

union clause Uop_kind = UopInstruction_RDFSTATUS : unit

function clause execute_uop(UopInstruction_RDFSTATUS(), _, values, instruction, _, speculative) =
    match execute_RDFSTATUS_primitive(instruction, speculative) {
        Some(result) => uop_step_from_local_result(result, speculative, values),
        None() => uop_step_fault(
            faulted(
                speculative,
                instruction.form.operation,
                IllegalInstruction,
                "RDFSTATUS local primitive rejected its instruction",
            ),
        ),
    }

function execute_RDFSTATUS(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
    Some(
        uop_program_execute(
            [|
                uop_make(
                    UopInstruction_RDFSTATUS(),
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
