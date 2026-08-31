function clause register_result_extension(Op_WAKE) = RegisterZeroExtend

function clause repeat_semantics(Op_WAKE) = RepeatObserveDestination

function lower_WAKE_uops(instruction : Decoded_instruction) -> option(list(Uop)) =
    match operand_named(instruction, Operand_address) {
        Some(address_operand) => {
            let address = uop_operand_lower(address_operand, 1, 0, false);
            let wake = uop_make(
                UopAddressWake(),
                address.address,
                uop_location_make_none(),
                uop_location_make_none(),
                Operand_address,
                1,
                CommitControl,
            );
            Some(uop_program_build(address.program, [|wake|], Operand_address, 1, CommitControl))
        },
        None() => None(),
    }

function execute_WAKE(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
    match lower_WAKE_uops(instruction) {
        Some(program) => Some(uop_program_execute(program, instruction, state)),
        None() => Some(faulted(state, instruction.form.operation, IllegalInstruction, "WAKE could not be lowered")),
    }
