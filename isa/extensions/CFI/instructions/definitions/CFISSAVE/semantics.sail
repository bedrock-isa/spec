function clause register_result_extension(Op_CFISSAVE) = RegisterZeroExtend

function clause repeat_semantics(Op_CFISSAVE) = RepeatObserveDestination

function lower_CFISSAVE_uops(instruction : Decoded_instruction)
  -> option(list(Uop)) = lower_cfi_state_record_uops(instruction, false)

function execute_CFISSAVE(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) =
  match lower_CFISSAVE_uops(instruction) {
    Some(program) => Some(uop_program_execute(program, instruction, state)),
    None() => Some(faulted(
      state, Op_CFISSAVE, IllegalInstruction, "CFISSAVE could not be lowered"
    )),
  }
