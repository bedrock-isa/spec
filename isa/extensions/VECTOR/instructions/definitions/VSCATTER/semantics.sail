function clause register_result_extension(Op_VSCATTER) = RegisterZeroExtend

function clause repeat_semantics(Op_VSCATTER) = RepeatObserveDestination

function clause vector_semantics(Op_VSCATTER) =
    {
        vector_default_semantics() with
        memory = Some(VectorScatter),
    }

function lower_VSCATTER_uops(instruction : Decoded_instruction) -> option(list(Uop)) =
    Some([|
        uop_make(UopVectorStepPrepare(Op_VSCATTER), uop_location_make_none(), uop_location_make_none(),
                 uop_location_make_temporary(40), Operand_completion, operation_width(instruction), CommitRegisters),
        uop_make(UopVectorStepIssue(Op_VSCATTER), uop_location_make_temporary(40), uop_location_make_none(),
                 uop_location_make_temporary(41), Operand_completion, operation_width(instruction), CommitMemory),
        uop_make(UopVectorStepCommit(Op_VSCATTER), uop_location_make_temporary(40), uop_location_make_temporary(41),
                 uop_location_make_none(), Operand_completion, operation_width(instruction), CommitMemory),
    |])

function execute_VSCATTER(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
    match lower_VSCATTER_uops(instruction) {
        Some(program) => Some(uop_program_execute(program, instruction, state)),
        None() => Some(faulted(state, instruction.form.operation, IllegalInstruction,
                               "VSCATTER could not be lowered to micro-operations")),
    }
