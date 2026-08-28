function clause fp_semantics(Op_FXCHG) =
Some(fp_raw_result_info(fp_exact_info(fp_info(FpPathR, 2, FpResultFnPair64, fflags_none,
                             fp_flags_none, false, 0), FpExactExchange)))


function clause register_result_extension(Op_FXCHG) = RegisterZeroExtend

function clause repeat_semantics(Op_FXCHG) = RepeatObserveDestination

function lower_FXCHG_uops(instruction : Decoded_instruction) -> option(list(Uop)) =
    match (
        fp_operands_lower_binary(instruction),
        fp_writable_fn_at(instruction.operands, 0, 0),
        fp_writable_fn_at(instruction.operands, 1, 0),
    ) {
        (Some(sources), Some(first), Some(second)) => Some(
            uop_program_append(
                sources.program,
                [|
                    uop_make_pair(
                        UopFpOperation(Op_FXCHG),
                        sources.source0,
                        sources.source1,
                        uop_operand_location(first),
                        uop_operand_location(second),
                        Operand_lhs,
                        operation_width(instruction),
                        CommitRegisters,
                    ),
                    uop_make(
                        UopCommit(),
                        uop_location_make_none(),
                        uop_location_make_none(),
                        uop_location_make_none(),
                        Operand_lhs,
                        operation_width(instruction),
                        CommitRegisters,
                    ),
                |],
            ),
        ),
        _ => None(),
    }

function execute_FXCHG(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
    match lower_FXCHG_uops(instruction) {
        Some(program) => Some(uop_program_execute(program, instruction, state)),
        None() => Some(
            faulted(
                state,
                instruction.form.operation,
                IllegalInstruction,
                "FXCHG could not be lowered to micro-operations",
            ),
        ),
    }
