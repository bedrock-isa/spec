function clause fp_semantics(Op_FMOVCR) =
Some(fp_exact_info(fp_info(FpPathR, 0, FpResultFn64, fflags_none,
                              fp_flags_none, false, 0), FpExactMoveConstant))


function clause register_result_extension(Op_FMOVCR) = RegisterZeroExtend

function clause repeat_semantics(Op_FMOVCR) = RepeatObserveDestination

function lower_FMOVCR_uops(instruction : Decoded_instruction) -> option(list(Uop)) =
    match operand_named(instruction, Operand_dst) {
        Some(destination) => Some(
            [|
                uop_make(
                    UopFpOperation(Op_FMOVCR),
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

function execute_FMOVCR(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
    match lower_FMOVCR_uops(instruction) {
        Some(program) => Some(uop_program_execute(program, instruction, state)),
        None() => Some(
            faulted(
                state,
                instruction.form.operation,
                IllegalInstruction,
                "FMOVCR could not be lowered to micro-operations",
            ),
        ),
    }
