function clause register_result_extension(Op_SSAVE) = RegisterZeroExtend
function clause repeat_semantics(Op_SSAVE) = RepeatObserveDestination

function execute_SSAVE(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
  match lower_base_state_record_uops(instruction, true, false) {
    Some(program) => Some(uop_program_execute(program, instruction, state)),
    None() => Some(faulted(state, instruction.form.operation, IllegalInstruction,
                           "SSAVE could not be lowered")),
  }
