function execute_VFLOOR(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) = {
    let address = uop_temporary(40);
    let memory = uop_temporary(41);
    let output = uop_temporary(42);
    let commit_kind : Commit_kind = match vector_memory_operand(instruction.operands) {
        Some(_) => CommitMemory,
        None() => CommitRegisters,
    };
    let compute = {
        make_uop(
            UopVectorFp(Op_VFLOOR),
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
}
