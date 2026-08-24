function execute_NOP_local_entry(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) =
  if instruction.form.operation != Op_NOP then None()
  else {
    let result : Execution_result =
    completed(state, advance_pc(state, instruction), CommitControl, [||]);
    Some(result)
  }


function execute_NOP(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) =
  if instruction.form.operation != Op_NOP then None()
  else match execute_NOP_local_entry(instruction, state) {
    Some(result) => Some(result),
    None() => Some(completed(state, advance_pc(state, instruction), CommitControl, [||])),
  }
