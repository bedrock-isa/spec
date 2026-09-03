function clause register_result_extension(Op_FRESTORE) = RegisterZeroExtend
function clause repeat_semantics(Op_FRESTORE) = RepeatObserveDestination

function execute_FRESTORE(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
  match lower_fp_state_record_uops(instruction, true) {
    Some(program) => Some(uop_program_execute(program, instruction, state)),
    None() => Some(faulted(state, instruction.form.operation, IllegalInstruction,
                           "FRESTORE could not be lowered")),
  }
