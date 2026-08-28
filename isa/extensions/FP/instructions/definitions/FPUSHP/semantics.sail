function clause fp_semantics(Op_FPUSHP) =
  Some(fp_info(FpPathStack, 2, FpResultMemory64, fflags_none,
                              fp_flags_none, false, 0))


function clause register_result_extension(Op_FPUSHP) = RegisterZeroExtend

function clause repeat_semantics(Op_FPUSHP) = RepeatObserveDestination

function lower_FPUSHP_uops(instruction : Decoded_instruction) -> option(list(Uop)) =
    match operand_named(instruction, Operand_pair_id) {
        Some(pair) => {
            let first = unsigned(pair.value[2 .. 0]) * 2;
            Some(
                [|
                    uop_make(
                        UopIntegerAdd(),
                        uop_location_make_sp(),
                        uop_location_make_immediate(bits_from_int(0 - 16)),
                        uop_location_make_sp(),
                        Operand_pair_id,
                        8,
                        CommitRegisters,
                    ),
                    uop_make(UopStackRange(true), uop_location_make_sp(), uop_location_make_none(), uop_location_make_none(), Operand_pair_id, 16, CommitMemory),
                    uop_make(
                        UopStackStorePair(),
                        uop_location_make_fp_register(first),
                        uop_location_make_fp_register(first + 1),
                        uop_location_make_sp(),
                        Operand_pair_id,
                        16,
                        CommitMemory,
                    ),
                    uop_make(UopCommit(), uop_location_make_none(), uop_location_make_none(), uop_location_make_none(), Operand_pair_id, 16, CommitMemory),
                |],
            )
        },
        None() => None(),
    }

function execute_FPUSHP(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
    match lower_FPUSHP_uops(instruction) {
        Some(program) => Some(uop_program_execute(program, instruction, state)),
        None() => Some(
            faulted(
                state,
                instruction.form.operation,
                IllegalInstruction,
                "FPUSHP could not be lowered to micro-operations",
            ),
        ),
    }
