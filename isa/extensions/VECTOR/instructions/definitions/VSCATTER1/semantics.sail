function clause register_result_extension(Op_VSCATTER1) = RegisterZeroExtend

function clause repeat_semantics(Op_VSCATTER1) = RepeatObserveDestination

function clause vector_semantics(Op_VSCATTER1) =
    {
        vector_default_semantics() with
        memory = Some(VectorScatterOne),
    }

function execute_VSCATTER1(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
    Some(
        uop_program_execute(
            [|
                uop_make(
                    UopVectorStepPrepare(Op_VSCATTER1),
                    uop_location_make_none(),
                    uop_location_make_none(),
                    uop_location_make_temporary(40),
                    Operand_cursor,
                    operation_width(instruction),
                    CommitRegisters,
                ),
                uop_make(
                    UopVectorStepIssue(Op_VSCATTER1),
                    uop_location_make_temporary(40),
                    uop_location_make_none(),
                    uop_location_make_temporary(41),
                    Operand_cursor,
                    operation_width(instruction),
                    CommitMemory,
                ),
                uop_make(
                    UopVectorStepCommit(Op_VSCATTER1),
                    uop_location_make_temporary(40),
                    uop_location_make_temporary(41),
                    uop_location_make_none(),
                    Operand_cursor,
                    operation_width(instruction),
                    CommitMemory,
                ),
            |],
            instruction,
            state,
        ),
    )
