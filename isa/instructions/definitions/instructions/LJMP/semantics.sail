function execute_LJMP_local_entry(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) =
  if instruction.form.operation != Op_LJMP then None()
  else {
    let result : Execution_result =
    match start_control_transaction(instruction, state) {
    Some(result) => result, None() => faulted(state, Op_LJMP, IllegalInstruction, "missing LJMP target")
  };
    Some(result)
  }


function execute_LJMP(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) =
  if instruction.form.operation != Op_LJMP then None()
  else match execute_LJMP_local_entry(instruction, state) {
    Some(result) => Some(result),
    None() => Some(match start_control_transaction(instruction, state) {
    Some(result) => result, None() => faulted(state, Op_LJMP, IllegalInstruction, "missing LJMP target")
  }),
  }
