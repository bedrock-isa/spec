function clause register_result_extension(Op_VSUB) = RegisterZeroExtend

function clause repeat_semantics(Op_VSUB) = RepeatObserveDestination

function clause vector_semantics(Op_VSUB) =
    {
        vector_default_semantics() with
        integer_binary = Some(VectorIntegerSubtract),
        fp_basic = true,
        fp_primitive = true,
        fp_scalar_operation = Some(fp_arithmetic_semantic_operation(FpArithmeticSubtract)),
    }

function execute_VSUB_integer(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) = {
    let operation = instruction.form.operation;
    let element_bytes = operation_width(instruction);
    let lanes = tdiv_int(state.vector_length_bytes, element_bytes);
    let empty = zero_vector_bytes(tdiv_int(state.vector_length_bytes, 8));
    let zero_vector = zero_vector_bytes(state.vector_length_bytes);
    let fp_form : bool = match condition_size_field(instruction.fields) {
        Some(selector) => selector >= 5,
        None() => false,
    };
    if (true | true | true | true | true | true | true | true | true | true | true | true | true) & not_bool(fp_form) then {
        match (
            vector_register_index(instruction, Operand_src),
            vector_register_index(instruction, Operand_dst),
            predicate_register_index(instruction, Operand_govern),
        ) {
            (Some(source), Some(destination), Some(predicate)) => {
                var updated = state;
                updated.vector_registers[unsigned(destination)] = vector_integer_binary_image(
                    operation,
                    state.vector_registers[unsigned(destination)],
                    state.vector_registers[unsigned(source)],
                    state.predicate_registers[unsigned(predicate)],
                    0,
                    lanes,
                    element_bytes,
                );
                Some(vector_finish(instruction, state, updated))
            },
            _ => None(),
        }
    } else {
        None()
    }
}

function execute_VSUB_floating(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) = {
    let address = uop_location_make_temporary(40);
    let memory = uop_location_make_temporary(41);
    let output = uop_location_make_temporary(42);
    let commit_kind : Commit_kind = match vector_memory_operand(instruction.operands) {
        Some(_) => CommitMemory,
        None() => CommitRegisters,
    };
    let compute = {
        uop_make(
            UopVectorFp(Op_VSUB),
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
}
