function clause fp_semantics(Op_FTEST) =
  Some(fp_info(FpPathR, 1, FpResultFlags, fflags_nv,
                             fp_flags_all, false, 0))


function clause register_result_extension(Op_FTEST) = RegisterZeroExtend

function clause repeat_semantics(Op_FTEST) = RepeatObserveDestination

function lower_FTEST_uops(instruction : Decoded_instruction) -> option(list(Uop)) =
    match fp_source_at(instruction.operands, 0, 0) {
        Some(source_operand) => {
            let source = uop_operand_lower(source_operand, operation_width(instruction), 0, true);
            Some(
                uop_program_append(
                    source.program,
                    [|
                        uop_make(
                            UopFpOperation(Op_FTEST),
                            source.value,
                            uop_location_make_none(),
                            uop_location_make_none(),
                            Operand_src,
                            operation_width(instruction),
                            CommitRegisters,
                        ),
                        uop_make(
                            UopCommit(),
                            uop_location_make_none(),
                            uop_location_make_none(),
                            uop_location_make_none(),
                            Operand_src,
                            operation_width(instruction),
                            CommitRegisters,
                        ),
                    |],
                ),
            )
        },
        None() => None(),
    }

function execute_FTEST(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
    match lower_FTEST_uops(instruction) {
        Some(program) => Some(uop_program_execute(program, instruction, state)),
        None() => Some(
            faulted(
                state,
                instruction.form.operation,
                IllegalInstruction,
                "FTEST could not be lowered to micro-operations",
            ),
        ),
    }
