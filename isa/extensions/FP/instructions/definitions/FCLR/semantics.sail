function clause fp_semantics(Op_FCLR) =
Some(fp_exact_info(fp_info(FpPathR, 0, FpResultFn64, fflags_none,
                            fp_flags_none, false, 0), FpExactClear))


function clause register_result_extension(Op_FCLR) = RegisterZeroExtend

function clause repeat_semantics(Op_FCLR) = RepeatObserveDestination

function lower_FCLR_uops(instruction : Decoded_instruction) -> option(list(Uop)) =
    match operand_named(instruction, Operand_dst) {
        Some(destination) => Some(
            [|
                uop_make(
                    UopFpOperation(Op_FCLR),
                    uop_location_make_none(),
                    uop_location_make_none(),
                    uop_operand_location(destination),
                    Operand_dst,
                    operation_width(instruction),
                    CommitRegisters,
                ),
                uop_make(
                    UopCommit(),
                    uop_location_make_none(),
                    uop_location_make_none(),
                    uop_location_make_none(),
                    Operand_dst,
                    operation_width(instruction),
                    CommitRegisters,
                ),
            |],
        ),
        None() => None(),
    }

function execute_FCLR(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
    match lower_FCLR_uops(instruction) {
        Some(program) => Some(uop_program_execute(program, instruction, state)),
        None() => Some(
            faulted(
                state,
                instruction.form.operation,
                IllegalInstruction,
                "FCLR could not be lowered to micro-operations",
            ),
        ),
    }
