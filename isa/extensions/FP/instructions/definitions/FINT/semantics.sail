function clause fp_semantics(Op_FINT) =
  Some(fp_info(FpPathR, 1, FpResultByForm, 0b10001,
                            fp_flags_none, false, 0))


function clause register_result_extension(Op_FINT) = RegisterZeroExtend

function clause repeat_semantics(Op_FINT) = RepeatObserveDestination

function lower_FINT_uops(instruction : Decoded_instruction) -> option(list(Uop)) =
    match fp_operands_lower_unary(instruction) {
        Some(operands) => {
            let width = operation_width(instruction);
            Some(
                uop_program_append(
                    operands.before_compute,
                    uop_make(
                        UopFpOperation(Op_FINT),
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

function execute_FINT(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
    match lower_FINT_uops(instruction) {
        Some(program) => Some(uop_program_execute(program, instruction, state)),
        None() => Some(
            faulted(
                state,
                instruction.form.operation,
                IllegalInstruction,
                "FINT could not be lowered to micro-operations",
            ),
        ),
    }
