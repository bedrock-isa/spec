
function lower_FBNDII_uops(instruction : Decoded_instruction) -> option(list(Micro_operation)) =
    match lower_fp_ternary_sources(instruction) {
        Some(sources) => Some(
            append_uops(
                sources.program,
                [|
                    make_uop3(
                        UopFpOperation(Op_FBNDII),
                        sources.source0,
                        sources.source1,
                        sources.source2,
                        uop_none(),
                        Operand_value,
                        operation_width(instruction),
                        CommitRegisters,
                    ),
                    make_uop(
                        UopCommit(),
                        uop_none(),
                        uop_none(),
                        uop_none(),
                        Operand_value,
                        operation_width(instruction),
                        CommitRegisters,
                    ),
                |],
            ),
        ),
        None() => None(),
    }

function execute_FBNDII(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
    match lower_FBNDII_uops(instruction) {
        Some(program) => Some(execute_uop_program(program, instruction, state)),
        None() => Some(
            faulted(
                state,
                instruction.form.operation,
                IllegalInstruction,
                "FBNDII could not be lowered to micro-operations",
            ),
        ),
    }
