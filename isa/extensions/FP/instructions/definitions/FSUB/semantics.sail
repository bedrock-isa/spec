function clause fp_semantics(Op_FSUB) =
  Some(fp_info(FpPathR, 2, FpResultFnByFormat, 0b10111,
                            fp_flags_none, false, 0))


function clause register_result_extension(Op_FSUB) = RegisterZeroExtend

function clause repeat_semantics(Op_FSUB) = RepeatObserveDestination

function lower_FSUB_uops(instruction : Decoded_instruction) -> option(list(Uop)) =
    match (fp_operands_lower_binary(instruction), operand_named(instruction, Operand_dst)) {
        (Some(sources), Some(destination_operand)) => {
            let width = operation_width(instruction);
            let compute = uop_make_ternary(
                UopFpArithmetic(FpArithmeticSubtract),
                sources.source0,
                sources.source1,
                sources.source2,
                uop_operand_location(destination_operand),
                Operand_dst,
                width,
                CommitRegisters,
            );
            Some(
                uop_program_append(
                    sources.program,
                    [|
                        compute,
                        uop_make(UopCommit(), uop_location_make_none(), uop_location_make_none(), uop_location_make_none(), Operand_dst, width, CommitRegisters),
                    |],
                ),
            )
        },
        _ => None(),
    }

function execute_FSUB(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
    match lower_FSUB_uops(instruction) {
        Some(program) => Some(uop_program_execute(program, instruction, state)),
        None() => Some(
            faulted(
                state,
                instruction.form.operation,
                IllegalInstruction,
                "FSUB could not be lowered to micro-operations",
            ),
        ),
    }
