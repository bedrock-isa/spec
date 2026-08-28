
function lower_FMOVcc_uops(instruction : Decoded_instruction) -> option(list(Micro_operation)) =
    match lower_fp_unary_operands(instruction) {
        Some(operands) => {
            let width = operation_width(instruction);
            Some(
                append_uops(
                    operands.before_compute,
                    make_uop(
                        UopFpOperation(Op_FMOVcc),
                        operands.source,
                        uop_none(),
                        operands.destination,
                        Operand_dst,
                        width,
                        operands.commit_kind,
                    ) ::
                        append_uops(
                            operands.after_compute,
                            [|
                                make_uop(
                                    UopCommit(),
                                    uop_none(),
                                    uop_none(),
                                    uop_none(),
                                    Operand_dst,
                                    width,
                                    operands.commit_kind,
                                ),
                            |],
                        ),
                ),
            )
        },
        None() => None(),
    }

function execute_FMOVcc(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
    match lower_FMOVcc_uops(instruction) {
        Some(program) => Some(execute_uop_program(program, instruction, state)),
        None() => Some(
            faulted(
                state,
                instruction.form.operation,
                IllegalInstruction,
                "FMOVcc could not be lowered to micro-operations",
            ),
        ),
    }
