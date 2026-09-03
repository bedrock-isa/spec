function clause register_result_extension(Op_FSAVE) = RegisterZeroExtend
function clause repeat_semantics(Op_FSAVE) = RepeatObserveDestination

function execute_FSAVE(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
  match lower_fp_state_record_uops(instruction, false) {
    Some(program) => Some(uop_program_execute(program, instruction, state)),
    None() => Some(faulted(state, instruction.form.operation, IllegalInstruction,
                           "FSAVE could not be lowered")),
  }
