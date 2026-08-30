function clause register_result_extension(Op_VFNMADD) = RegisterZeroExtend

function clause repeat_semantics(Op_VFNMADD) = RepeatObserveDestination

function clause vector_semantics(Op_VFNMADD) =
    {
        vector_default_semantics() with
        fp_basic = true,
        fp_primitive = true,
        fp_scalar_operation = Some(fp_arithmetic_semantic_operation(FpArithmeticFusedNegatedMultiplyAdd)),
        fp_arity = 3,
    }

function lower_VFNMADD_uops(instruction : Decoded_instruction) -> option(list(Uop)) = {
    let address = uop_location_make_temporary(40);
    let memory = uop_location_make_temporary(41);
    let output = uop_location_make_temporary(42);
    let commit_kind : Commit_kind = match vector_memory_operand(instruction.operands) {
        Some(_) => CommitMemory,
        None() => CommitRegisters,
    };
    let compute = {
        uop_make(
            UopVectorFp(Op_VFNMADD),
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

function execute_VFNMADD(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
    match lower_VFNMADD_uops(instruction) {
        Some(program) => Some(uop_program_execute(program, instruction, state)),
        None() => Some(faulted(state, instruction.form.operation, IllegalInstruction,
                               "VFNMADD could not be lowered to micro-operations")),
    }
