function clause fp_semantics(Op_FETOXA) =
  Some(fp_info(FpPathR, 1, FpResultFnByFormat, 0b10110,
                              fp_flags_none, true, 49))


function clause register_result_extension(Op_FETOXA) = RegisterZeroExtend

function clause repeat_semantics(Op_FETOXA) = RepeatObserveDestination

function lower_FETOXA_uops(instruction : Decoded_instruction) -> option(list(Uop)) =
    match fp_operands_lower_unary(instruction) {
        Some(operands) => {
            let width = operation_width(instruction);
            let contract = uop_location_make_temporary(32);
            let compute = {
                uop_make(
                    UopFpOperation(Op_FETOXA),
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

function execute_FETOXA(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
    match lower_FETOXA_uops(instruction) {
        Some(program) => Some(uop_program_execute(program, instruction, state)),
        None() => Some(
            faulted(
                state,
                instruction.form.operation,
                IllegalInstruction,
                "FETOXA could not be lowered to micro-operations",
            ),
        ),
    }
