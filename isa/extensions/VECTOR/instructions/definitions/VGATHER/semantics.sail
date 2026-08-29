function clause register_result_extension(Op_VGATHER) = RegisterZeroExtend

function clause repeat_semantics(Op_VGATHER) = RepeatObserveDestination

function clause vector_semantics(Op_VGATHER) =
    {
        vector_default_semantics() with
        memory = Some(VectorGather),
    }

function lower_VGATHER_uops(instruction : Decoded_instruction) -> option(list(Uop)) =
    Some([|
        uop_make(UopVectorStepPrepare(Op_VGATHER), uop_location_make_none(), uop_location_make_none(),
                 uop_location_make_temporary(40), Operand_completion, operation_width(instruction), CommitRegisters),
        uop_make(UopVectorStepIssue(Op_VGATHER), uop_location_make_temporary(40), uop_location_make_none(),
                 uop_location_make_temporary(41), Operand_completion, operation_width(instruction), CommitMemory),
        uop_make(UopVectorStepCommit(Op_VGATHER), uop_location_make_temporary(40), uop_location_make_temporary(41),
                 uop_location_make_none(), Operand_completion, operation_width(instruction), CommitMemory),
    |])

function execute_VGATHER(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
    match lower_VGATHER_uops(instruction) {
        Some(program) => Some(uop_program_execute(program, instruction, state)),
        None() => Some(faulted(state, instruction.form.operation, IllegalInstruction,
                               "VGATHER could not be lowered to micro-operations")),
    }
