function execute_FCOSA_local_entry(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) =
  if instruction.form.operation != Op_FCOSA then None()
  else {
    let result : Execution_result =
    start_fp_transaction(instruction, state);
    Some(result)
  }


function execute_FCOSA(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) =
  if instruction.form.operation != Op_FCOSA then None()
  else match execute_FCOSA_local_entry(instruction, state) {
    Some(result) => Some(result),
    None() => Some(start_fp_transaction(instruction, state)),
  }
