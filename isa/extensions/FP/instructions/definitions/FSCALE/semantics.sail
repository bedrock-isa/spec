function clause fp_semantics(Op_FSCALE) =
  Some(fp_info(FpPathR, 2, FpResultFnByFormat, 0b10111,
                              fp_flags_none, false, 0))


function clause register_result_extension(Op_FSCALE) = RegisterZeroExtend

function clause repeat_semantics(Op_FSCALE) = RepeatObserveDestination

function lower_FSCALE_uops(instruction : Decoded_instruction) -> option(list(Uop)) =
    match (fp_operands_lower_binary(instruction), operand_named(instruction, Operand_dst)) {
        (Some(sources), Some(destination)) => {
            let width = operation_width(instruction);
            Some(
                uop_program_append(
                    sources.program,
                    [|
                        uop_make(
                            UopFpOperation(Op_FSCALE),
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

function execute_FSCALE(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
    match lower_FSCALE_uops(instruction) {
        Some(program) => Some(uop_program_execute(program, instruction, state)),
        None() => Some(
            faulted(
                state,
                instruction.form.operation,
                IllegalInstruction,
                "FSCALE could not be lowered to micro-operations",
            ),
        ),
    }
