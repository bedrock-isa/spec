
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
        None() => start_system_request(instruction, state),
    };
    Some(result)
}

union clause Uop_kind = UopInstruction_WRFFLAGS : unit

function clause execute_uop(UopInstruction_WRFFLAGS(), _, values, instruction, _, speculative) =
    match execute_WRFFLAGS_primitive(instruction, speculative) {
        Some(result) => uop_local_result_step(result, speculative, values),
        None() => uop_fault(
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
        execute_uop_program(
            [|
                make_uop(
                    UopInstruction_WRFFLAGS(),
                    uop_none(),
                    uop_none(),
                    uop_none(),
                    Operand_dst,
                    operation_width(instruction),
                    CommitRegisters,
                ),
                make_uop(
                    UopCommit(),
                    uop_none(),
                    uop_none(),
                    uop_none(),
                    Operand_dst,
                    operation_width(instruction),
                    CommitRegisters,
                ),
            |],
            instruction,
            state,
        ),
    )
