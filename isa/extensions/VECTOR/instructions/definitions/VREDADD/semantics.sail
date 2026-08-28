function clause register_result_extension(Op_VREDADD) = RegisterZeroExtend

function clause repeat_semantics(Op_VREDADD) = RepeatObserveDestination

function clause vector_semantics(Op_VREDADD) =
    {
        vector_default_semantics() with
        integer_reduction = Some(VectorReduceAdd),
        reduction = true,
        fp_reduction_operation = Some(fp_arithmetic_semantic_operation(FpArithmeticAdd)),
        fp_reduction_identity = VectorFpReductionZero,
    }

function execute_VREDADD(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) = {
    let operation = instruction.form.operation;
    let element_bytes = operation_width(instruction);
    let lanes = tdiv_int(state.vector_length_bytes, element_bytes);
    match operand_named(instruction, Operand_dst) {
        Some(destination) => if destination.operand_type == OperandType_Fn then {
            let address = uop_location_make_temporary(40);
            let memory = uop_location_make_temporary(41);
            let output = uop_location_make_temporary(42);
            let commit_kind : Commit_kind = match vector_memory_operand(instruction.operands) {
                Some(_) => CommitMemory,
                None() => CommitRegisters,
            };
            let compute = {
                uop_make(
                    UopVectorFp(Op_VREDADD),
                    uop_location_make_none(),
                    uop_location_make_none(),
                    output,
                    Operand_dst,
                    operation_width(instruction),
                    commit_kind,
                ) with
                auxiliary = memory,
            };
            Some(
                uop_program_execute(
                    [|
                        uop_make(
                            UopVectorCalcEa(),
                            uop_location_make_none(),
                            uop_location_make_none(),
                            address,
                            Operand_dst,
                            operation_width(instruction),
                            CommitNone,
                        ),
                        uop_make(
                            UopVectorMemoryLoad(),
                            address,
                            uop_location_make_none(),
                            memory,
                            Operand_dst,
                            operation_width(instruction),
                            CommitMemory,
                        ),
                        compute,
                        uop_make(
                            UopVectorMemoryStore(),
                            address,
                            output,
                            uop_location_make_none(),
                            Operand_dst,
                            operation_width(instruction),
                            CommitMemory,
                        ),
                        uop_make(
                            UopCommit(),
                            uop_location_make_none(),
                            uop_location_make_none(),
                            uop_location_make_none(),
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
