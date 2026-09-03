function clause register_result_extension(Op_SRESTORE) = RegisterZeroExtend
function clause repeat_semantics(Op_SRESTORE) = RepeatObserveDestination

function execute_SRESTORE(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
  match lower_base_state_record_uops(instruction, true, true) {
    Some(program) => Some(uop_program_execute(program, instruction, state)),
    None() => Some(faulted(state, instruction.form.operation, IllegalInstruction,
                           "SRESTORE could not be lowered")),
  }
