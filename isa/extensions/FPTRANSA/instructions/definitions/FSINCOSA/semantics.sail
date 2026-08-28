
function lower_FSINCOSA_uops(instruction : Decoded_instruction) -> option(list(Micro_operation)) =
    match (
        fp_source_at(instruction.operands, 0, 0),
        operand_named(instruction, Operand_sin_dst),
        operand_named(instruction, Operand_cos_dst),
    ) {
        (Some(source_operand), Some(sin_destination), Some(cos_destination)) => {
            let width = operation_width(instruction);
            let source = lower_uop_operand(source_operand, width, 0, true);
            let contract = uop_temporary(32);
            let compute = {
                make_uop_pair(
                    UopFpOperation(Op_FSINCOSA),
                    source.value,
                    uop_none(),
                    direct_uop_location(sin_destination),
                    direct_uop_location(cos_destination),
                    Operand_sin_dst,
                    width,
                    CommitRegisters,
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
                        source.program,
                        [|
                            compute,
                            make_uop(
                                UopCommit(),
                                uop_none(),
                                uop_none(),
                                uop_none(),
                                Operand_sin_dst,
                                width,
                                CommitRegisters,
                            ),
                        |],
                    ),
                ),
            )
        },
        _ => None(),
    }

function execute_FSINCOSA(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
    match lower_FSINCOSA_uops(instruction) {
        Some(program) => Some(execute_uop_program(program, instruction, state)),
        None() => Some(
            faulted(
                state,
                instruction.form.operation,
                IllegalInstruction,
                "FSINCOSA could not be lowered to micro-operations",
            ),
        ),
    }
