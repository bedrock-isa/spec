function clause register_result_extension(Op_VMULHSU) = RegisterZeroExtend

function clause repeat_semantics(Op_VMULHSU) = RepeatObserveDestination

function clause vector_semantics(Op_VMULHSU) =
    {
        vector_default_semantics() with
        integer_binary = Some(VectorIntegerMultiplyHighSignedUnsigned),
    }


function lower_VMULHSU_uops(instruction : Decoded_instruction) -> option(list(Uop)) = {
    let address = uop_location_make_temporary(40);
    let memory = uop_location_make_temporary(41);
    let output = uop_location_make_temporary(42);
    let commit_kind : Commit_kind = match vector_memory_operand(instruction.operands) {
        Some(_) => CommitMemory,
        None() => CommitRegisters,
    };
    let compute = {
        uop_make(
            UopVectorCompute(Op_VMULHSU),
            uop_location_make_none(),
            uop_location_make_none(),
            output,
            Operand_dst,
            operation_width(instruction),
            commit_kind,
        ) with
        auxiliary = memory,
    };
    Some([|
        uop_make(UopVectorCalcEa(), uop_location_make_none(), uop_location_make_none(), address,
                 Operand_dst, operation_width(instruction), CommitNone),
        uop_make(UopVectorMemoryLoad(), address, uop_location_make_none(), memory,
                 Operand_dst, operation_width(instruction), CommitMemory),
        compute,
        uop_make(UopVectorMemoryStore(), address, output, uop_location_make_none(),
                 Operand_dst, operation_width(instruction), CommitMemory),
        uop_make(UopCommit(), uop_location_make_none(), uop_location_make_none(), uop_location_make_none(),
                 Operand_dst, operation_width(instruction), commit_kind),
    |])
}

function execute_VMULHSU(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
    match lower_VMULHSU_uops(instruction) {
        Some(program) => Some(uop_program_execute(program, instruction, state)),
        None() => Some(faulted(state, instruction.form.operation, IllegalInstruction,
                               "VMULHSU could not be lowered to micro-operations")),
    }
