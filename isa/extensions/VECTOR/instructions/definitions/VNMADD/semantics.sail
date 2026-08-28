function clause register_result_extension(Op_VNMADD) = RegisterZeroExtend

function clause repeat_semantics(Op_VNMADD) = RepeatObserveDestination

function clause vector_semantics(Op_VNMADD) =
    {
        vector_default_semantics() with
        fp_basic = true,
        fp_primitive = true,
        fp_scalar_operation = Some(fp_arithmetic_semantic_operation(FpArithmeticFusedNegatedMultiplyAdd)),
        fp_arity = 3,
    }

function execute_VNMADD(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
    Some(
        uop_program_execute(
            [|
                uop_make(
                    UopVectorFp(Op_VNMADD),
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
