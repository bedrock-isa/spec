
function lower_FTRUNC_uops(instruction : Decoded_instruction) -> option(list(Micro_operation)) =
    match lower_fp_unary_operands(instruction) {
        Some(operands) => {
            let width = operation_width(instruction);
            let compute = make_uop(
                UopFpConvert(FpConvertTruncate),
                operands.source,
                uop_none(),
                operands.destination,
                Operand_dst,
                width,
                operands.commit_kind,
            );
            Some(
                append_uops(
                    operands.before_compute,
                    compute ::
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

function execute_FTRUNC(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
    match lower_FTRUNC_uops(instruction) {
        Some(program) => Some(execute_uop_program(program, instruction, state)),
        None() => Some(
            faulted(
                state,
                instruction.form.operation,
                IllegalInstruction,
                "FTRUNC could not be lowered to micro-operations",
            ),
        ),
    }
