
function lower_FCLR_uops(instruction : Decoded_instruction) -> option(list(Micro_operation)) =
    match operand_named(instruction, Operand_dst) {
        Some(destination) => Some(
            [|
                make_uop(
                    UopFpOperation(Op_FCLR),
                    uop_none(),
                    uop_none(),
                    direct_uop_location(destination),
                    Operand_dst,
                    operation_width(instruction),
                    CommitRegisters,
                ),
                make_uop(
                    UopCommit(),
                    uop_none(),
                    uop_none(),
                    uop_none(),
                    Operand_dst,
                    operation_width(instruction),
                    CommitRegisters,
                ),
            |],
        ),
        None() => None(),
    }

function execute_FCLR(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
    match lower_FCLR_uops(instruction) {
        Some(program) => Some(execute_uop_program(program, instruction, state)),
        None() => Some(
            faulted(
                state,
                instruction.form.operation,
                IllegalInstruction,
                "FCLR could not be lowered to micro-operations",
            ),
        ),
    }
