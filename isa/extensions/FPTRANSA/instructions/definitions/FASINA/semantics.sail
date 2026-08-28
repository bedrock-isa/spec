
function lower_FASINA_uops(instruction : Decoded_instruction) -> option(list(Micro_operation)) =
    match lower_fp_unary_operands(instruction) {
        Some(operands) => {
            let width = operation_width(instruction);
            let contract = uop_temporary(32);
            let compute = {
                make_uop(
                    UopFpOperation(Op_FASINA),
                    operands.source,
                    uop_none(),
                    operands.destination,
                    Operand_dst,
                    width,
                    operands.commit_kind,
                ) with
                auxiliary = contract,
            };
            Some(
                append_uops(
                    [|
                        make_uop(UopFpContractQuery(), uop_none(), uop_none(), contract, Operand_src, width, CommitNone),
                        make_uop(
                            UopFpContractValidate(),
                            contract,
                            uop_none(),
                            uop_none(),
                            Operand_src,
                            width,
                            CommitNone,
                        ),
                    |],
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
                ),
            )
        },
        None() => None(),
    }

function execute_FASINA(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
    match lower_FASINA_uops(instruction) {
        Some(program) => Some(execute_uop_program(program, instruction, state)),
        None() => Some(
            faulted(
                state,
                instruction.form.operation,
                IllegalInstruction,
                "FASINA could not be lowered to micro-operations",
            ),
        ),
    }
