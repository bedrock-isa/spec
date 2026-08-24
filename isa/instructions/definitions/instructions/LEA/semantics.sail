function execute_LEA_local_entry(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) =
  if instruction.form.operation != Op_LEA then None()
  else execute_lea_transaction(instruction, state)


function execute_LEA(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) =
  if instruction.form.operation != Op_LEA then None()
  else match execute_LEA_local_entry(instruction, state) {
    Some(result) => Some(result),
    None() => Some(match execute_lea_transaction(instruction, state) { Some(result) => result, None() => faulted(state, instruction.form.operation, IllegalInstruction, "unresolved EA utility form") }),
  }
