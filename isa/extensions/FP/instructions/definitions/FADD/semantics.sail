function clause fp_semantics(Op_FADD) =
  Some(fp_info(FpPathR, 2, FpResultFnByFormat, 0b10111,
                            fp_flags_none, false, 0))


function clause register_result_extension(Op_FADD) = RegisterZeroExtend

function clause repeat_semantics(Op_FADD) = RepeatObserveDestination

function lower_FADD_uops(instruction : Decoded_instruction) -> option(list(Uop)) =
    match (
        fp_source_at(instruction.operands, 0, 0),
        fp_source_at(instruction.operands, 1, 0),
        operand_named(instruction, Operand_dst),
    ) {
        (Some(source_operand), Some(accumulator_operand), Some(destination_operand)) => {
            let width = operation_width(instruction);
            let source = uop_operand_lower(source_operand, width, 0, true);
            let accumulator = uop_operand_lower(accumulator_operand, width, source.next_temporary, true);
            let destination = uop_operand_location(destination_operand);
            let arithmetic = uop_make(
                UopFpArithmetic(FpArithmeticAdd),
                source.value,
                accumulator.value,
                destination,
                Operand_dst,
                width,
                CommitRegisters,
            );
            Some(
                uop_program_append(
                    source.program,
                    uop_program_append(
                        accumulator.program,
                        [|
                            arithmetic,
                            uop_make(
                                UopCommit(),
                                uop_location_make_none(),
                                uop_location_make_none(),
                                uop_location_make_none(),
                                Operand_dst,
                                width,
                                CommitRegisters,
                            ),
                        |],
                    ),
                ),
            )
        },
        _ => None(),
    }

function execute_FADD(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
    match lower_FADD_uops(instruction) {
        Some(program) => Some(uop_program_execute(program, instruction, state)),
        None() => Some(
            faulted(
                state,
                instruction.form.operation,
                IllegalInstruction,
                "FADD could not be lowered to micro-operations",
            ),
        ),
    }
