function clause fp_semantics(Op_FPOPP) =
Some(fp_raw_result_info(fp_info(FpPathStack, 2, FpResultFnPair64, fflags_none,
                             fp_flags_none, false, 0)))


function clause register_result_extension(Op_FPOPP) = RegisterZeroExtend

function clause repeat_semantics(Op_FPOPP) = RepeatObserveDestination

function lower_FPOPP_uops(instruction : Decoded_instruction) -> option(list(Uop)) =
    match operand_named(instruction, Operand_pair_id) {
        Some(pair) => {
            let first = unsigned(pair.value[2 .. 0]) * 2;
            Some(
                [|
                    uop_make(UopStackRange(false), uop_location_make_sp(), uop_location_make_none(), uop_location_make_none(), Operand_pair_id, 16, CommitMemory),
                    uop_make(UopStackLoad(0), uop_location_make_sp(), uop_location_make_none(), uop_location_make_temporary(0), Operand_pair_id, 8, CommitMemory),
                    uop_make(UopStackLoad(8), uop_location_make_sp(), uop_location_make_none(), uop_location_make_temporary(1), Operand_pair_id, 8, CommitMemory),
                    uop_make_pair(
                        UopFpPairMove(),
                        uop_location_make_temporary(1),
                        uop_location_make_temporary(0),
                        uop_location_make_fp_register(first),
                        uop_location_make_fp_register(first + 1),
                        Operand_pair_id,
                        8,
                        CommitRegisters,
                    ),
                    uop_make(
                        UopIntegerAdd(),
                        uop_location_make_sp(),
                        uop_location_make_immediate(bits_from_int(16)),
                        uop_location_make_sp(),
                        Operand_pair_id,
                        8,
                        CommitRegisters,
                    ),
                    uop_make(UopCommit(), uop_location_make_none(), uop_location_make_none(), uop_location_make_none(), Operand_pair_id, 16, CommitRegisters),
                |],
            )
        },
        None() => None(),
    }

function execute_FPOPP(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
    match lower_FPOPP_uops(instruction) {
        Some(program) => Some(uop_program_execute(program, instruction, state)),
        None() => Some(
            faulted(
                state,
                instruction.form.operation,
                IllegalInstruction,
                "FPOPP could not be lowered to micro-operations",
            ),
        ),
    }
