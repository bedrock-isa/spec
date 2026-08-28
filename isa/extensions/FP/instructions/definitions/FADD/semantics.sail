
function lower_FADD_uops(instruction : Decoded_instruction) -> option(list(Micro_operation)) =
    match (
        fp_source_at(instruction.operands, 0, 0),
        fp_source_at(instruction.operands, 1, 0),
        operand_named(instruction, Operand_dst),
    ) {
        (Some(source_operand), Some(accumulator_operand), Some(destination_operand)) => {
            let width = operation_width(instruction);
            let source = lower_uop_operand(source_operand, width, 0, true);
            let accumulator = lower_uop_operand(accumulator_operand, width, source.next_temporary, true);
            let destination = direct_uop_location(destination_operand);
            let arithmetic = make_uop(
                UopFpArithmetic(FpArithmeticAdd),
                source.value,
                accumulator.value,
                destination,
                Operand_dst,
                width,
                CommitRegisters,
            );
            Some(
                append_uops(
                    source.program,
                    append_uops(
                        accumulator.program,
                        [|
                            arithmetic,
                            make_uop(
                                UopCommit(),
                                uop_none(),
                                uop_none(),
                                uop_none(),
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
        Some(program) => Some(execute_uop_program(program, instruction, state)),
        None() => Some(
            faulted(
                state,
                instruction.form.operation,
                IllegalInstruction,
                "FADD could not be lowered to micro-operations",
            ),
        ),
    }
