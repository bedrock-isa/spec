function clause register_result_extension(Op_CFISRESTORE) = RegisterZeroExtend

function clause repeat_semantics(Op_CFISRESTORE) = RepeatObserveDestination

function lower_CFISRESTORE_uops(instruction : Decoded_instruction)
  -> option(list(Uop)) = lower_cfi_state_record_uops(instruction, true)

function execute_CFISRESTORE(instruction : Decoded_instruction,
                             state : Cpu_state) -> option(Execution_result) =
  match lower_CFISRESTORE_uops(instruction) {
    Some(program) => Some(uop_program_execute(program, instruction, state)),
    None() => Some(faulted(
      state, Op_CFISRESTORE, IllegalInstruction,
      "CFISRESTORE could not be lowered"
    )),
  }
