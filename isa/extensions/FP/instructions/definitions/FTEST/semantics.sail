
function lower_FTEST_uops(instruction : Decoded_instruction) -> option(list(Micro_operation)) =
    match fp_source_at(instruction.operands, 0, 0) {
        Some(source_operand) => {
            let source = lower_uop_operand(source_operand, operation_width(instruction), 0, true);
            Some(
                append_uops(
                    source.program,
                    [|
                        make_uop(
                            UopFpOperation(Op_FTEST),
                            source.value,
                            uop_none(),
                            uop_none(),
                            Operand_src,
                            operation_width(instruction),
                            CommitRegisters,
                        ),
                        make_uop(
                            UopCommit(),
                            uop_none(),
                            uop_none(),
                            uop_none(),
                            Operand_src,
                            operation_width(instruction),
                            CommitRegisters,
                        ),
                    |],
                ),
            )
        },
        None() => None(),
    }

function execute_FTEST(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
    match lower_FTEST_uops(instruction) {
        Some(program) => Some(execute_uop_program(program, instruction, state)),
        None() => Some(
            faulted(
                state,
                instruction.form.operation,
                IllegalInstruction,
                "FTEST could not be lowered to micro-operations",
            ),
        ),
    }
