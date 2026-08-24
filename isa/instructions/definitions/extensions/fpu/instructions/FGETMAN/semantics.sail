function execute_FGETMAN_local_entry(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) =
  if instruction.form.operation != Op_FGETMAN then None()
  else {
    let result : Execution_result =
    start_fp_transaction(instruction, state);
    Some(result)
  }


function execute_FGETMAN(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) =
  if instruction.form.operation != Op_FGETMAN then None()
  else match execute_FGETMAN_local_entry(instruction, state) {
    Some(result) => Some(result),
    None() => Some(start_fp_transaction(instruction, state)),
  }
