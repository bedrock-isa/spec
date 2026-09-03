function clause register_result_extension(Op_VRESTORE) = RegisterZeroExtend
function clause repeat_semantics(Op_VRESTORE) = RepeatObserveDestination

function execute_VRESTORE(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
  match lower_vector_state_record_uops(instruction, true) {
    Some(program) => Some(uop_program_execute(program, instruction, state)),
    None() => Some(faulted(state, instruction.form.operation, IllegalInstruction,
                           "VRESTORE could not be lowered")),
  }
