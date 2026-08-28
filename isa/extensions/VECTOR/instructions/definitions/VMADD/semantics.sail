function clause register_result_extension(Op_VMADD) = RegisterZeroExtend

function clause repeat_semantics(Op_VMADD) = RepeatObserveDestination

function clause vector_semantics(Op_VMADD) =
    {
        vector_default_semantics() with
        fp_basic = true,
        fp_primitive = true,
        fp_scalar_operation = Some(fp_arithmetic_semantic_operation(FpArithmeticFusedMultiplyAdd)),
        fp_arity = 3,
    }

function execute_VMADD(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
    Some(
        uop_program_execute(
            [|
                uop_make(
                    UopVectorFp(Op_VMADD),
                    uop_location_make_none(),
                    uop_location_make_none(),
                    uop_location_make_none(),
                    Operand_dst,
                    operation_width(instruction),
                    CommitRegisters,
                ),
                uop_make(
                    UopCommit(),
                    uop_location_make_none(),
                    uop_location_make_none(),
                    uop_location_make_none(),
                    Operand_dst,
                    operation_width(instruction),
                    CommitRegisters,
                ),
            |],
            instruction,
            state,
        ),
    )
