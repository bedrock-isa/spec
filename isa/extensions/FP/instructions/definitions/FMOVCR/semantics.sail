
function lower_FMOVCR_uops(instruction : Decoded_instruction) -> option(list(Micro_operation)) =
    match operand_named(instruction, Operand_dst) {
        Some(destination) => Some(
            [|
                make_uop(
                    UopFpOperation(Op_FMOVCR),
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

function execute_FMOVCR(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
    match lower_FMOVCR_uops(instruction) {
        Some(program) => Some(execute_uop_program(program, instruction, state)),
        None() => Some(
            faulted(
                state,
                instruction.form.operation,
                IllegalInstruction,
                "FMOVCR could not be lowered to micro-operations",
            ),
        ),
    }
