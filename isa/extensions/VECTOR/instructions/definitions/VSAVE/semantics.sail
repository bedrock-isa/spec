function clause register_result_extension(Op_VSAVE) = RegisterZeroExtend
function clause repeat_semantics(Op_VSAVE) = RepeatObserveDestination

function execute_VSAVE(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
  match lower_vector_state_record_uops(instruction, false) {
    Some(program) => Some(uop_program_execute(program, instruction, state)),
    None() => Some(faulted(state, instruction.form.operation, IllegalInstruction,
                           "VSAVE could not be lowered")),
  }
