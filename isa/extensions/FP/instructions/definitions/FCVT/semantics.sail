function clause fp_semantics(Op_FCVT) =
Some(fp_conversion_info(fp_info(FpPathR, 1, FpResultByForm, 0b10111,
                            fp_flags_none, false, 0), false))


function clause register_result_extension(Op_FCVT) = RegisterZeroExtend

function clause repeat_semantics(Op_FCVT) = RepeatObserveDestination

function lower_FCVT_uops(instruction : Decoded_instruction) -> option(list(Uop)) =
    match fp_operands_lower_unary(instruction) {
        Some(operands) => {
            let width = operation_width(instruction);
            let compute = uop_make(
                UopFpConvert(FpConvertSigned),
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

function execute_FCVT(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
    match lower_FCVT_uops(instruction) {
        Some(program) => Some(uop_program_execute(program, instruction, state)),
        None() => Some(
            faulted(
                state,
                instruction.form.operation,
                IllegalInstruction,
                "FCVT could not be lowered to micro-operations",
            ),
        ),
    }
