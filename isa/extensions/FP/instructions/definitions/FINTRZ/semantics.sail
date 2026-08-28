function clause fp_semantics(Op_FINTRZ) =
  Some(fp_info(FpPathR, 1, FpResultByForm, 0b10001,
                              fp_flags_none, false, 0))


function clause register_result_extension(Op_FINTRZ) = RegisterZeroExtend

function clause repeat_semantics(Op_FINTRZ) = RepeatObserveDestination

function lower_FINTRZ_uops(instruction : Decoded_instruction) -> option(list(Uop)) =
    match fp_operands_lower_unary(instruction) {
        Some(operands) => {
            let width = operation_width(instruction);
            Some(
                uop_program_append(
                    operands.before_compute,
                    uop_make(
                        UopFpOperation(Op_FINTRZ),
                        operands.source,
                        uop_location_make_none(),
                        operands.destination,
                        Operand_dst,
                        width,
                        operands.commit_kind,
                    ) ::
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
            )
        },
        None() => None(),
    }

function execute_FINTRZ(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
    match lower_FINTRZ_uops(instruction) {
        Some(program) => Some(uop_program_execute(program, instruction, state)),
        None() => Some(
            faulted(
                state,
                instruction.form.operation,
                IllegalInstruction,
                "FINTRZ could not be lowered to micro-operations",
            ),
        ),
    }
