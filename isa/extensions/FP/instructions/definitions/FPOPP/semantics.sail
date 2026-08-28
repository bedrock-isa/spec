
function lower_FPOPP_uops(instruction : Decoded_instruction) -> option(list(Micro_operation)) =
    match operand_named(instruction, Operand_pair_id) {
        Some(pair) => {
            let first = unsigned(pair.value[2 .. 0]) * 2;
            Some(
                [|
                    make_uop(UopStackRange(false), uop_sp(), uop_none(), uop_none(), Operand_pair_id, 16, CommitMemory),
                    make_uop(UopStackLoad(0), uop_sp(), uop_none(), uop_temporary(0), Operand_pair_id, 8, CommitMemory),
                    make_uop(UopStackLoad(8), uop_sp(), uop_none(), uop_temporary(1), Operand_pair_id, 8, CommitMemory),
                    make_uop_pair(
                        UopFpPairMove(),
                        uop_temporary(1),
                        uop_temporary(0),
                        uop_fp_register(first),
                        uop_fp_register(first + 1),
                        Operand_pair_id,
                        8,
                        CommitRegisters,
                    ),
                    make_uop(
                        UopIntegerAdd(),
                        uop_sp(),
                        uop_immediate(bits_from_int(16)),
                        uop_sp(),
                        Operand_pair_id,
                        8,
                        CommitRegisters,
                    ),
                    make_uop(UopCommit(), uop_none(), uop_none(), uop_none(), Operand_pair_id, 16, CommitRegisters),
                |],
            )
        },
        None() => None(),
    }

function execute_FPOPP(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
    match lower_FPOPP_uops(instruction) {
        Some(program) => Some(execute_uop_program(program, instruction, state)),
        None() => Some(
            faulted(
                state,
                instruction.form.operation,
                IllegalInstruction,
                "FPOPP could not be lowered to micro-operations",
            ),
        ),
    }
