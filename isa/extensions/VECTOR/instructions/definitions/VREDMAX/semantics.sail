function clause register_result_extension(Op_VREDMAX) = RegisterZeroExtend

function clause repeat_semantics(Op_VREDMAX) = RepeatObserveDestination

function clause vector_semantics(Op_VREDMAX) =
    {
        vector_default_semantics() with
        reduction = true,
        fp_reduction_operation = Some(fp_compare_semantic_operation(FpCompareMaximum)),
        fp_reduction_identity = VectorFpReductionNegativeInfinity,
        fp_allowed_causes = fflags_nv,
    }

function execute_VREDMAX(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) = {
    let address = uop_location_make_temporary(40);
    let memory = uop_location_make_temporary(41);
    let output = uop_location_make_temporary(42);
    let commit_kind : Commit_kind = match vector_memory_operand(instruction.operands) {
        Some(_) => CommitMemory,
        None() => CommitRegisters,
    };
    let compute = {
        uop_make(
            UopVectorFp(Op_VREDMAX),
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
