
function lower_FCOPYSIGN_uops(instruction : Decoded_instruction) -> option(list(Micro_operation)) =
    match (lower_fp_binary_sources(instruction), operand_named(instruction, Operand_dst)) {
        (Some(sources), Some(destination)) => {
            let width = operation_width(instruction);
            Some(
                append_uops(
                    sources.program,
                    [|
                        make_uop(
                            UopFpData(FpDataCopySign),
                            sources.source0,
                            sources.source1,
                            direct_uop_location(destination),
                            Operand_dst,
                            width,
                            CommitRegisters,
                        ),
                        make_uop(UopCommit(), uop_none(), uop_none(), uop_none(), Operand_dst, width, CommitRegisters),
                    |],
                ),
            )
        },
        _ => None(),
    }

function execute_FCOPYSIGN(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
    match lower_FCOPYSIGN_uops(instruction) {
        Some(program) => Some(execute_uop_program(program, instruction, state)),
        None() => Some(
            faulted(
                state,
                instruction.form.operation,
                IllegalInstruction,
                "FCOPYSIGN could not be lowered to micro-operations",
            ),
        ),
    }
