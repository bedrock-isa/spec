
function lower_FCMP_uops(instruction : Decoded_instruction) -> option(list(Micro_operation)) =
    match lower_fp_binary_sources(instruction) {
        Some(sources) => {
            let width = operation_width(instruction);
            let destination : Uop_location = match operand_named(instruction, Operand_dst) {
                Some(operand) => direct_uop_location(operand),
                None() => uop_none(),
            };
            let compute = make_uop(
                UopFpCompare(FpCompareOrdered),
                sources.source0,
                sources.source1,
                destination,
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
        None() => None(),
    }

function execute_FCMP(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
    match lower_FCMP_uops(instruction) {
        Some(program) => Some(execute_uop_program(program, instruction, state)),
        None() => Some(
            faulted(
                state,
                instruction.form.operation,
                IllegalInstruction,
                "FCMP could not be lowered to micro-operations",
            ),
        ),
    }
