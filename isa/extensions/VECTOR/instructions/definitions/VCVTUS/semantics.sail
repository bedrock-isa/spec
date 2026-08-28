function clause register_result_extension(Op_VCVTUS) = RegisterZeroExtend

function clause repeat_semantics(Op_VCVTUS) = RepeatObserveDestination

function clause vector_semantics(Op_VCVTUS) =
    {
        vector_default_semantics() with
        fp_conversion = true,
        fp_conversion_destination_bytes = 4,
        fp_conversion_destination_fp = true,
        fp_conversion_unsigned = true,
    }

function execute_VCVTUS(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
    Some(
        uop_program_execute(
            [|
                uop_make(
                    UopVectorFp(Op_VCVTUS),
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
