function clause register_result_extension(Op_VCVTUQ) = RegisterZeroExtend

function clause repeat_semantics(Op_VCVTUQ) = RepeatObserveDestination

function clause vector_semantics(Op_VCVTUQ) =
    {
        vector_default_semantics() with
        fp_conversion = true,
        fp_conversion_destination_bytes = 8,
        fp_conversion_destination_fp = false,
        fp_conversion_unsigned = true,
    }

function execute_VCVTUQ(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
    Some(
        uop_program_execute(
            [|
                uop_make(
                    UopVectorFp(Op_VCVTUQ),
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
