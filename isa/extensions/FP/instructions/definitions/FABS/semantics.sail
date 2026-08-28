function clause fp_semantics(Op_FABS) =
Some(fp_exact_info(fp_info(FpPathR, 1, FpResultByForm, fflags_none,
                            fp_flags_none, false, 0), FpExactAbsolute))


function clause register_result_extension(Op_FABS) = RegisterZeroExtend

function clause repeat_semantics(Op_FABS) = RepeatObserveDestination

function lower_FABS_uops(instruction : Decoded_instruction) -> option(list(Uop)) =
    match fp_operands_lower_unary(instruction) {
        Some(operands) => {
            let width = operation_width(instruction);
            let compute = uop_make(
                UopFpArithmetic(FpArithmeticAbsolute),
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

function execute_FABS(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
    match lower_FABS_uops(instruction) {
        Some(program) => Some(uop_program_execute(program, instruction, state)),
        None() => Some(
            faulted(
                state,
                instruction.form.operation,
                IllegalInstruction,
                "FABS could not be lowered to micro-operations",
            ),
        ),
    }
