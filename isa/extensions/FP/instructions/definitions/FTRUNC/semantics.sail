function clause fp_semantics(Op_FTRUNC) =
  Some(fp_info(FpPathR, 1, FpResultByForm, 0b10001,
                              fp_flags_none, false, 0))


function clause register_result_extension(Op_FTRUNC) = RegisterZeroExtend

function clause repeat_semantics(Op_FTRUNC) = RepeatObserveDestination

function lower_FTRUNC_uops(instruction : Decoded_instruction) -> option(list(Uop)) =
    match fp_operands_lower_unary(instruction) {
        Some(operands) => {
            let width = operation_width(instruction);
            let compute = uop_make(
                UopFpConvert(FpConvertTruncate),
                operands.source,
                uop_location_make_none(),
                operands.destination,
                Operand_dst,
                width,
                operands.commit_kind,
            );
            Some(
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
            )
        },
        None() => None(),
    }

function execute_FTRUNC(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
    match lower_FTRUNC_uops(instruction) {
        Some(program) => Some(uop_program_execute(program, instruction, state)),
        None() => Some(
            faulted(
                state,
                instruction.form.operation,
                IllegalInstruction,
                "FTRUNC could not be lowered to micro-operations",
            ),
        ),
    }
