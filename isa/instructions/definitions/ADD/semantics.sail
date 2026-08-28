
function add_source_operand(instruction : Decoded_instruction) -> option(Decoded_operand) =
    match operand_named(instruction, Operand_src) {
        Some(source) => Some(source),
        None() => operand_named(instruction, Operand_imm),
    }

function lower_ADD_uops(instruction : Decoded_instruction) -> option(list(Micro_operation)) =
    match (add_source_operand(instruction), operand_named(instruction, Operand_dst)) {
        (Some(source_operand), Some(destination_operand)) => {
            let width = operation_width(instruction);
            let source = lower_uop_operand(source_operand, width, 0, true);
            let destination = lower_uop_operand(destination_operand, width, source.next_temporary, true);
            let arithmetic = make_uop(
                UopIntegerAdd(),
                destination.value,
                source.value,
                destination.value,
                Operand_dst,
                width,
                CommitRegisters,
            );
            let store = if destination.memory then {
                    [|
                        make_uop(
                            UopMemoryStore(),
                            destination.value,
                            destination.address,
                            uop_none(),
                            Operand_dst,
                            width,
                            CommitMemory,
                        ),
                    |]
                } else {
                    [||]
                };
            let commit_kind = if source.memory | destination.memory then { CommitMemory } else { CommitRegisters };
            Some(
                append_uops(
                    source.program,
                    append_uops(
                        destination.program,
                        arithmetic ::
                            append_uops(
                                store,
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

function execute_ADD(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
    match lower_ADD_uops(instruction) {
        Some(program) => Some(execute_uop_program(program, instruction, state)),
        None() => Some(
            faulted(
                state,
                instruction.form.operation,
                IllegalInstruction,
                "ADD could not be lowered to micro-operations",
            ),
        ),
    }
