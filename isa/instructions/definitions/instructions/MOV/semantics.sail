function execute_MOV_local_entry(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) =
  if instruction.form.operation != Op_MOV then None()
  else {
    let local_candidate : option(Execution_result) = match execute_move_sp_local(instruction, state) {
    Some(result) => Some(result),
    None() => execute_binary_local(instruction, state),
  };
    let result : Execution_result = match local_candidate {
            Some(result) => result,
            None() => match start_stack_transaction(instruction, state) { Some(result) => result, None() => match start_memory_transaction(instruction, state) { Some(result) => result, None() => faulted(state, instruction.form.operation, IllegalInstruction, "unresolved data-movement form") } }
          };
    Some(result)
  }


function execute_MOV(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) =
  if instruction.form.operation != Op_MOV then None()
  else match execute_MOV_local_entry(instruction, state) {
    Some(result) => Some(result),
    None() => Some(match start_stack_transaction(instruction, state) { Some(result) => result, None() => match start_memory_transaction(instruction, state) { Some(result) => result, None() => faulted(state, instruction.form.operation, IllegalInstruction, "unresolved data-movement form") } }),
  }
