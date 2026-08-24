function execute_BKPT_local_entry(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) =
  if instruction.form.operation != Op_BKPT then None()
  else {
    let result : Execution_result =
    start_event_control(instruction, state);
    Some(result)
  }


function execute_BKPT(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) =
  if instruction.form.operation != Op_BKPT then None()
  else match execute_BKPT_local_entry(instruction, state) {
    Some(result) => Some(result),
    None() => Some(start_event_control(instruction, state)),
  }
