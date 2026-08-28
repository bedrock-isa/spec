
function lower_FPUSHP_uops(instruction : Decoded_instruction) -> option(list(Micro_operation)) =
    match operand_named(instruction, Operand_pair_id) {
        Some(pair) => {
            let first = unsigned(pair.value[2 .. 0]) * 2;
            Some(
                [|
                    make_uop(
                        UopIntegerAdd(),
                        uop_sp(),
                        uop_immediate(bits_from_int(0 - 16)),
                        uop_sp(),
                        Operand_pair_id,
                        8,
                        CommitRegisters,
                    ),
                    make_uop(UopStackRange(true), uop_sp(), uop_none(), uop_none(), Operand_pair_id, 16, CommitMemory),
                    make_uop(
                        UopStackStorePair(),
                        uop_fp_register(first),
                        uop_fp_register(first + 1),
                        uop_sp(),
                        Operand_pair_id,
                        16,
                        CommitMemory,
                    ),
                    make_uop(UopCommit(), uop_none(), uop_none(), uop_none(), Operand_pair_id, 16, CommitMemory),
                |],
            )
        },
        None() => None(),
    }

function execute_FPUSHP(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
    match lower_FPUSHP_uops(instruction) {
        Some(program) => Some(execute_uop_program(program, instruction, state)),
        None() => Some(
            faulted(
                state,
                instruction.form.operation,
                IllegalInstruction,
                "FPUSHP could not be lowered to micro-operations",
            ),
        ),
    }
