
function lower_FXCHG_uops(instruction : Decoded_instruction) -> option(list(Micro_operation)) =
    match (
        lower_fp_binary_sources(instruction),
        fp_writable_fn_at(instruction.operands, 0, 0),
        fp_writable_fn_at(instruction.operands, 1, 0),
    ) {
        (Some(sources), Some(first), Some(second)) => Some(
            append_uops(
                sources.program,
                [|
                    make_uop_pair(
                        UopFpOperation(Op_FXCHG),
                        sources.source0,
                        sources.source1,
                        direct_uop_location(first),
                        direct_uop_location(second),
                        Operand_lhs,
                        operation_width(instruction),
                        CommitRegisters,
                    ),
                    make_uop(
                        UopCommit(),
                        uop_none(),
                        uop_none(),
                        uop_none(),
                        Operand_lhs,
                        operation_width(instruction),
                        CommitRegisters,
                    ),
                |],
            ),
        ),
        _ => None(),
    }

function execute_FXCHG(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
    match lower_FXCHG_uops(instruction) {
        Some(program) => Some(execute_uop_program(program, instruction, state)),
        None() => Some(
            faulted(
                state,
                instruction.form.operation,
                IllegalInstruction,
                "FXCHG could not be lowered to micro-operations",
            ),
        ),
    }
