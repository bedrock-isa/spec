function clause fp_semantics(Op_FMSUB) =
  Some(fp_info(FpPathR, 3, FpResultFnByFormat, 0b10111,
                             fp_flags_none, false, 0))


function clause register_result_extension(Op_FMSUB) = RegisterZeroExtend

function clause repeat_semantics(Op_FMSUB) = RepeatObserveDestination

function lower_FMSUB_uops(instruction : Decoded_instruction) -> option(list(Uop)) =
    match (fp_operands_lower_ternary(instruction), operand_named(instruction, Operand_dst)) {
        (Some(sources), Some(destination_operand)) => {
            let width = operation_width(instruction);
            let compute = uop_make_ternary(
                UopFpArithmetic(FpArithmeticFusedMultiplySubtract),
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

function execute_FMSUB(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
    match lower_FMSUB_uops(instruction) {
        Some(program) => Some(uop_program_execute(program, instruction, state)),
        None() => Some(
            faulted(
                state,
                instruction.form.operation,
                IllegalInstruction,
                "FMSUB could not be lowered to micro-operations",
            ),
        ),
    }
