function clause register_result_extension(Op_WAIT) = RegisterZeroExtend

function clause repeat_semantics(Op_WAIT) = RepeatObserveDestination

function lower_WAIT_uops(instruction : Decoded_instruction) -> option(list(Uop)) =
    match (operand_named(instruction, Operand_expected), operand_named(instruction, Operand_memory)) {
        (Some(expected), Some(memory_operand)) => {
            let width = operation_width(instruction);
            let memory = uop_operand_lower(memory_operand, width, 0, false);
            let wait = uop_make(
                UopAddressWait(),
                memory.address,
                uop_operand_location(expected),
                uop_location_make_none(),
                Operand_memory,
                width,
                CommitMemory,
            );
            Some(uop_program_build(memory.program, [|wait|], Operand_memory, width, CommitMemory))
        },
        _ => None(),
    }

function execute_WAIT(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
    match lower_WAIT_uops(instruction) {
        Some(program) => Some(uop_program_execute(program, instruction, state)),
        None() => Some(faulted(state, instruction.form.operation, IllegalInstruction, "WAIT could not be lowered")),
    }
