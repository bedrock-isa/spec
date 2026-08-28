function clause fp_semantics(Op_FMADD) =
  Some(fp_info(FpPathR, 3, FpResultFnByFormat, 0b10111,
                             fp_flags_none, false, 0))


function clause register_result_extension(Op_FMADD) = RegisterZeroExtend

function clause repeat_semantics(Op_FMADD) = RepeatObserveDestination

function lower_FMADD_uops(instruction : Decoded_instruction) -> option(list(Uop)) =
    match (fp_operands_lower_ternary(instruction), operand_named(instruction, Operand_dst)) {
        (Some(sources), Some(destination_operand)) => {
            let width = operation_width(instruction);
            let compute = uop_make_ternary(
                UopFpArithmetic(FpArithmeticFusedMultiplyAdd),
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

function execute_FMADD(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
    match lower_FMADD_uops(instruction) {
        Some(program) => Some(uop_program_execute(program, instruction, state)),
        None() => Some(
            faulted(
                state,
                instruction.form.operation,
                IllegalInstruction,
                "FMADD could not be lowered to micro-operations",
            ),
        ),
    }
