function execute_FETCHADD_local_entry(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) =
  if instruction.form.operation != Op_FETCHADD then None()
  else {
    let result : Execution_result =
    match start_atomic_transaction(instruction, state) { Some(result) => result, None() => faulted(state, instruction.form.operation, IllegalInstruction, "missing atomic memory operand") };
    Some(result)
  }


function execute_FETCHADD(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) =
  if instruction.form.operation != Op_FETCHADD then None()
  else match execute_FETCHADD_local_entry(instruction, state) {
    Some(result) => Some(result),
    None() => Some(match start_atomic_transaction(instruction, state) { Some(result) => result, None() => faulted(state, instruction.form.operation, IllegalInstruction, "missing atomic memory operand") }),
  }
