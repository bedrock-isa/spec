function execute_IJcc_local_entry(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) =
  if instruction.form.operation != Op_IJcc then None()
  else {
    let result : Execution_result =
    execute_count_jump(instruction, state);
    Some(result)
  }


function execute_IJcc(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) =
  if instruction.form.operation != Op_IJcc then None()
  else match execute_IJcc_local_entry(instruction, state) {
    Some(result) => Some(result),
    None() => Some(execute_count_jump(instruction, state)),
  }
