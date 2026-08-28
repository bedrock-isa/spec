function execute_VREDADD(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) = {
    let operation = instruction.form.operation;
    let element_bytes = operation_width(instruction);
    let lanes = tdiv_int(state.vector_length_bytes, element_bytes);
    match operand_named(instruction, Operand_dst) {
        Some(destination) => if destination.operand_type == OperandType_Fn then {
            let address = uop_temporary(40);
            let memory = uop_temporary(41);
            let output = uop_temporary(42);
            let commit_kind : Commit_kind = match vector_memory_operand(instruction.operands) {
                Some(_) => CommitMemory,
                None() => CommitRegisters,
            };
            let compute = {
                make_uop(
                    UopVectorFp(Op_VREDADD),
                    uop_none(),
                    uop_none(),
                    output,
                    Operand_dst,
                    operation_width(instruction),
                    commit_kind,
                ) with
                auxiliary = memory,
            };
            Some(
                execute_uop_program(
                    [|
                        make_uop(
                            UopVectorCalcEa(),
                            uop_none(),
                            uop_none(),
                            address,
                            Operand_dst,
                            operation_width(instruction),
                            CommitNone,
                        ),
                        make_uop(
                            UopVectorMemoryLoad(),
                            address,
                            uop_none(),
                            memory,
                            Operand_dst,
                            operation_width(instruction),
                            CommitMemory,
                        ),
                        compute,
                        make_uop(
                            UopVectorMemoryStore(),
                            address,
                            output,
                            uop_none(),
                            Operand_dst,
                            operation_width(instruction),
                            CommitMemory,
                        ),
                        make_uop(
                            UopCommit(),
                            uop_none(),
                            uop_none(),
                            uop_none(),
                            Operand_dst,
                            operation_width(instruction),
                            commit_kind,
                        ),
                    |],
                    instruction,
                    state,
                ),
            )
        } else {
            match (
                vector_register_index(instruction, Operand_src),
                predicate_register_index(instruction, Operand_govern),
                operand_named(instruction, Operand_dst),
            ) {
                (Some(source), Some(predicate), Some(destination)) => {
                    var updated = state;
                    updated.registers[unsigned(destination.value[3 .. 0])] = get_slice_int(
                        64,
                        vector_integer_reduction_image(
                            operation,
                            state.vector_registers[unsigned(source)],
                            state.predicate_registers[unsigned(predicate)],
                            0,
                            lanes,
                            element_bytes,
                            vector_integer_reduction_identity(operation, element_bytes),
                        ),
                        0,
                    );
                    Some(vector_finish(instruction, state, updated))
                },
                _ => None(),
            }
        },
        None() => None(),
    }
}
