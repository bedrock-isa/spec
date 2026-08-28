function clause fp_semantics(Op_WRFSTATUS) = None()

function clause register_result_extension(Op_WRFSTATUS) = RegisterZeroExtend

function clause repeat_semantics(Op_WRFSTATUS) = RepeatObserveDestination

function execute_WRFSTATUS_primitive(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) = {
    let local_candidate : option(Execution_result) = match value_named(instruction, state, Operand_src) {
        None() => None(),
        Some(source) => if (source & 0x000000000000FC00) != 0x0000000000000000 then {
            Some(faulted(state, Op_WRFSTATUS, InvalidControlState, "reserved FSTATUS bits"))
        } else {
            Some(
                local_result(
                    state,
                    instruction,
                    {
                        state with
                        fstatus = source & 0x00000000000003FF,
                        fp_component_modified = true,
                    },
                    CommitRegisters,
                ),
            )
        },
    };
    let result : Execution_result = match local_candidate {
        Some(result) => result,
        None() => faulted(state, instruction.form.operation, IllegalInstruction, "missing WRFSTATUS source"),
    };
    Some(result)
}

union clause Uop_kind = UopInstruction_WRFSTATUS : unit

function clause execute_uop(UopInstruction_WRFSTATUS(), _, values, instruction, _, speculative) =
    match execute_WRFSTATUS_primitive(instruction, speculative) {
        Some(result) => uop_step_from_local_result(result, speculative, values),
        None() => uop_step_fault(
            faulted(
                speculative,
                instruction.form.operation,
                IllegalInstruction,
                "WRFSTATUS local primitive rejected its instruction",
            ),
        ),
    }

function execute_WRFSTATUS(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
    Some(
        uop_program_execute(
            [|
                uop_make(
                    UopInstruction_WRFSTATUS(),
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
