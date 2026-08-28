
function execute_RDFSTATUS_primitive(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) = {
    let result : Execution_result = match Some(read_state_register(instruction, state, narrow_bits(state.fstatus, 2))) {
        Some(result) => result,
        None() => start_system_request(instruction, state),
    };
    Some(result)
}

union clause Uop_kind = UopInstruction_RDFSTATUS : unit

function clause execute_uop(UopInstruction_RDFSTATUS(), _, values, instruction, _, speculative) =
    match execute_RDFSTATUS_primitive(instruction, speculative) {
        Some(result) => uop_local_result_step(result, speculative, values),
        None() => uop_fault(
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
        execute_uop_program(
            [|
                make_uop(
                    UopInstruction_RDFSTATUS(),
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
