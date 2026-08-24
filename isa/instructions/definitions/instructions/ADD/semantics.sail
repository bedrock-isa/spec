function execute_ADD_local_entry(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) =
  if instruction.form.operation != Op_ADD then None()
  else match execute_sp_arithmetic_local(instruction, state) {
    Some(result) => Some(result),
    None() => execute_binary_local(instruction, state),
  }


function execute_ADD(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) =
  if instruction.form.operation != Op_ADD then None()
  else match execute_ADD_local_entry(instruction, state) {
    Some(result) => Some(result),
    None() => Some(match start_memory_transaction(instruction, state) {
      Some(result) => result,
      None() => faulted(state, instruction.form.operation, IllegalInstruction, "unresolved integer ALU form")
    }),
  }
