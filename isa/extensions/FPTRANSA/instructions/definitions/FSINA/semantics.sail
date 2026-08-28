function clause fp_semantics(Op_FSINA) =
  Some(fp_info(FpPathR, 1, FpResultFnByFormat, 0b10010,
                             fp_flags_none, true, 1))


function clause register_result_extension(Op_FSINA) = RegisterZeroExtend

function clause repeat_semantics(Op_FSINA) = RepeatObserveDestination

function lower_FSINA_uops(instruction : Decoded_instruction) -> option(list(Uop)) =
    match fp_operands_lower_unary(instruction) {
        Some(operands) => {
            let width = operation_width(instruction);
            let contract = uop_location_make_temporary(32);
            let compute = {
                uop_make(
                    UopFpOperation(Op_FSINA),
                    operands.source,
                    uop_location_make_none(),
                    operands.destination,
                    Operand_dst,
                    width,
                    operands.commit_kind,
                ) with
                auxiliary = contract,
            };
            Some(
                uop_program_append(
                    [|
                        uop_make(UopFpContractQuery(), uop_location_make_none(), uop_location_make_none(), contract, Operand_src, width, CommitNone),
                        uop_make(
                            UopFpContractValidate(),
                            contract,
                            uop_location_make_none(),
                            uop_location_make_none(),
                            Operand_src,
                            width,
                            CommitNone,
                        ),
                    |],
                    uop_program_append(
                        operands.before_compute,
                        compute ::
                            uop_program_append(
                                operands.after_compute,
                                [|
                                    uop_make(
                                        UopCommit(),
                                        uop_location_make_none(),
                                        uop_location_make_none(),
                                        uop_location_make_none(),
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

function execute_FSINA(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
    match lower_FSINA_uops(instruction) {
        Some(program) => Some(uop_program_execute(program, instruction, state)),
        None() => Some(
            faulted(
                state,
                instruction.form.operation,
                IllegalInstruction,
                "FSINA could not be lowered to micro-operations",
            ),
        ),
    }
