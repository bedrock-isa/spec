function clause register_result_extension(Op_RESTORE) = RegisterZeroExtend

function clause repeat_semantics(Op_RESTORE) = RepeatObserveDestination

function lower_RESTORE_uops(instruction : Decoded_instruction) -> option(list(Uop)) =
  lower_base_state_record_uops(instruction, false, true)

function execute_RESTORE(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
  match lower_RESTORE_uops(instruction) {
    Some(program) => Some(uop_program_execute(program, instruction, state)),
    None() => Some(faulted(state, instruction.form.operation, IllegalInstruction,
                           "RESTORE could not be lowered")),
  }
