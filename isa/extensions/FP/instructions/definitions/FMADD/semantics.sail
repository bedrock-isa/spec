
function lower_FMADD_uops(instruction : Decoded_instruction) -> option(list(Micro_operation)) =
    match (lower_fp_ternary_sources(instruction), operand_named(instruction, Operand_dst)) {
        (Some(sources), Some(destination_operand)) => {
            let width = operation_width(instruction);
            let compute = make_uop3(
                UopFpArithmetic(FpArithmeticFusedMultiplyAdd),
                sources.source0,
                sources.source1,
                sources.source2,
                direct_uop_location(destination_operand),
                Operand_dst,
                width,
                CommitRegisters,
            );
            Some(
                append_uops(
                    sources.program,
                    [|
                        compute,
                        make_uop(UopCommit(), uop_none(), uop_none(), uop_none(), Operand_dst, width, CommitRegisters),
                    |],
                ),
            )
        },
        _ => None(),
    }

function execute_FMADD(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
    match lower_FMADD_uops(instruction) {
        Some(program) => Some(execute_uop_program(program, instruction, state)),
        None() => Some(
            faulted(
                state,
                instruction.form.operation,
                IllegalInstruction,
                "FMADD could not be lowered to micro-operations",
            ),
        ),
    }
