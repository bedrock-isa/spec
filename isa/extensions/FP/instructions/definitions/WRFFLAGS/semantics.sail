function clause fp_semantics(Op_WRFFLAGS) = None()

function clause register_result_extension(Op_WRFFLAGS) = RegisterZeroExtend

function clause repeat_semantics(Op_WRFFLAGS) = RepeatObserveDestination

function execute_WRFFLAGS_primitive(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) = {
    let local_candidate : option(Execution_result) = match value_named(instruction, state, Operand_src) {
        None() => None(),
        Some(source) => if (source & 0x000000000000FFE0) != 0x0000000000000000 then {
            Some(faulted(state, Op_WRFFLAGS, InvalidControlState, "reserved FFLAGS bits"))
        } else {
            Some(
                local_result(
                    state,
                    instruction,
                    {
                        state with
                        fflags = source[4 .. 0],
                        fp_component_modified = true,
                    },
                    CommitRegisters,
                ),
            )
        },
    };
    let result : Execution_result = match local_candidate {
        Some(result) => result,
        None() => faulted(state, instruction.form.operation, IllegalInstruction, "missing WRFFLAGS source"),
    };
    Some(result)
}

union clause Uop_kind = UopInstruction_WRFFLAGS : unit

function clause execute_uop(UopInstruction_WRFFLAGS(), _, values, instruction, _, speculative) =
    match execute_WRFFLAGS_primitive(instruction, speculative) {
        Some(result) => uop_step_from_local_result(result, speculative, values),
        None() => uop_step_fault(
            faulted(
                speculative,
                instruction.form.operation,
                IllegalInstruction,
                "WRFFLAGS local primitive rejected its instruction",
            ),
        ),
    }

function execute_WRFFLAGS(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
    Some(
        uop_program_execute(
            [|
                uop_make(
                    UopInstruction_WRFFLAGS(),
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
