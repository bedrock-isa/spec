function execute_DJcc_local_entry(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) =
  if instruction.form.operation != Op_DJcc then None()
  else {
    let result : Execution_result =
    execute_count_jump(instruction, state);
    Some(result)
  }


function execute_DJcc(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) =
  if instruction.form.operation != Op_DJcc then None()
  else match execute_DJcc_local_entry(instruction, state) {
    Some(result) => Some(result),
    None() => Some(execute_count_jump(instruction, state)),
  }
