
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
        None() => start_system_request(instruction, state),
    };
    Some(result)
}

union clause Uop_kind = UopInstruction_WRFSTATUS : unit

function clause execute_uop(UopInstruction_WRFSTATUS(), _, values, instruction, _, speculative) =
    match execute_WRFSTATUS_primitive(instruction, speculative) {
        Some(result) => uop_local_result_step(result, speculative, values),
        None() => uop_fault(
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
        execute_uop_program(
            [|
                make_uop(
                    UopInstruction_WRFSTATUS(),
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
