function clause register_result_extension(Op_PMOV) = RegisterZeroExtend

function clause repeat_semantics(Op_PMOV) = RepeatObserveDestination

function clause vector_semantics(Op_PMOV) =
    {
        vector_default_semantics() with
        memory = Some(VectorPredicateMove),
    }

function execute_PMOV(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) = {
    let address = uop_location_make_temporary(40);
    let memory = uop_location_make_temporary(41);
    let output = uop_location_make_temporary(42);
    let compute = {
        uop_make(
            UopVectorMemoryCompute(Op_PMOV),
            uop_location_make_none(),
            uop_location_make_none(),
            output,
            Operand_dst,
            operation_width(instruction),
            CommitMemory,
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
                    CommitMemory,
                ),
            |],
            instruction,
            state,
        ),
    )
}
