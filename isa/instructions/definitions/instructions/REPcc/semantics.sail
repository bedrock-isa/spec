function execute_REPcc_local_entry(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) =
  if instruction.form.operation != Op_REPcc then None()
  else {
    let result : Execution_result =
    start_repeat_transaction(instruction, state);
    Some(result)
  }


function execute_REPcc(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) =
  if instruction.form.operation != Op_REPcc then None()
  else match execute_REPcc_local_entry(instruction, state) {
    Some(result) => Some(result),
    None() => Some(start_repeat_transaction(instruction, state)),
  }
