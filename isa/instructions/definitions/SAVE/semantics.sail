function clause register_result_extension(Op_SAVE) = RegisterZeroExtend

function clause repeat_semantics(Op_SAVE) = RepeatObserveDestination

function lower_SAVE_uops(instruction : Decoded_instruction) -> option(list(Uop)) =
  lower_base_state_record_uops(instruction, false, false)

function execute_SAVE(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
  match lower_SAVE_uops(instruction) {
    Some(program) => Some(uop_program_execute(program, instruction, state)),
    None() => Some(faulted(state, instruction.form.operation, IllegalInstruction,
                           "SAVE could not be lowered")),
  }
