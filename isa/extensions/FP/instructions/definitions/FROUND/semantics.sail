function clause fp_semantics(Op_FROUND) =
  Some(fp_info(FpPathR, 1, FpResultByForm, 0b10001,
                              fp_flags_none, false, 0))


function clause register_result_extension(Op_FROUND) = RegisterZeroExtend

function clause repeat_semantics(Op_FROUND) = RepeatObserveDestination

function lower_FROUND_uops(instruction : Decoded_instruction) -> option(list(Uop)) =
    match fp_operands_lower_unary(instruction) {
        Some(operands) => {
            let width = operation_width(instruction);
            let compute = uop_make(
                UopFpConvert(FpConvertRound),
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

function execute_FROUND(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
    match lower_FROUND_uops(instruction) {
        Some(program) => Some(uop_program_execute(program, instruction, state)),
        None() => Some(
            faulted(
                state,
                instruction.form.operation,
                IllegalInstruction,
                "FROUND could not be lowered to micro-operations",
            ),
        ),
    }
