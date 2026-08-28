function clause fp_semantics(Op_FCOPYSIGN) =
Some(fp_exact_info(fp_info(FpPathR, 2, FpResultFnByFormat, fflags_none,
                                fp_flags_none, false, 0), FpExactCopySign))


function clause register_result_extension(Op_FCOPYSIGN) = RegisterZeroExtend

function clause repeat_semantics(Op_FCOPYSIGN) = RepeatObserveDestination

function lower_FCOPYSIGN_uops(instruction : Decoded_instruction) -> option(list(Uop)) =
    match (fp_operands_lower_binary(instruction), operand_named(instruction, Operand_dst)) {
        (Some(sources), Some(destination)) => {
            let width = operation_width(instruction);
            Some(
                uop_program_append(
                    sources.program,
                    [|
                        uop_make(
                            UopFpData(FpDataCopySign),
                            sources.source0,
                            sources.source1,
                            uop_operand_location(destination),
                            Operand_dst,
                            width,
                            CommitRegisters,
                        ),
                        uop_make(UopCommit(), uop_location_make_none(), uop_location_make_none(), uop_location_make_none(), Operand_dst, width, CommitRegisters),
                    |],
                ),
            )
        },
        _ => None(),
    }

function execute_FCOPYSIGN(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
    match lower_FCOPYSIGN_uops(instruction) {
        Some(program) => Some(uop_program_execute(program, instruction, state)),
        None() => Some(
            faulted(
                state,
                instruction.form.operation,
                IllegalInstruction,
                "FCOPYSIGN could not be lowered to micro-operations",
            ),
        ),
    }
