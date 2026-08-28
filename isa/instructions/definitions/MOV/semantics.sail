
function lower_MOV_uops(instruction : Decoded_instruction) -> option(list(Micro_operation)) =
    match (operand_named(instruction, Operand_src), operand_named(instruction, Operand_dst)) {
        (Some(source_operand), Some(destination_operand)) => {
            let width = operation_width(instruction);
            let source = lower_uop_operand(source_operand, width, 0, true);
            let destination = lower_uop_operand(destination_operand, width, source.next_temporary, false);
            let transfer = if destination.memory then {
                    [|
                        make_uop(
                            UopMemoryStore(),
                            source.value,
                            destination.address,
                            uop_none(),
                            Operand_dst,
                            width,
                            CommitMemory,
                        ),
                    |]
                } else {
                    [|
                        make_uop(
                            UopMove(),
                            source.value,
                            uop_none(),
                            destination.value,
                            Operand_dst,
                            width,
                            CommitRegisters,
                        ),
                    |]
                };
            let commit_kind = if source.memory | destination.memory then { CommitMemory } else { CommitRegisters };
            Some(
                append_uops(
                    source.program,
                    append_uops(
                        destination.program,
                        append_uops(
                            transfer,
                            [|
                                make_uop(
                                    UopCommit(),
                                    uop_none(),
                                    uop_none(),
                                    uop_none(),
                                    Operand_dst,
                                    width,
                                    commit_kind,
                                ),
                            |],
                        ),
                    ),
                ),
            )
        },
        _ => None(),
    }

function execute_MOV(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
    match lower_MOV_uops(instruction) {
        Some(program) => Some(execute_uop_program(program, instruction, state)),
        None() => Some(
            faulted(
                state,
                instruction.form.operation,
                IllegalInstruction,
                "MOV could not be lowered to micro-operations",
            ),
        ),
    }
