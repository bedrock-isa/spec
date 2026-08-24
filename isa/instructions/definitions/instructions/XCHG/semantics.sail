function execute_XCHG_local_entry(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) =
  if instruction.form.operation != Op_XCHG then None()
  else {
    let result : Execution_result =
    match execute_xchg_local(instruction, state) {
            Some(result) => result,
            None() => match start_stack_transaction(instruction, state) { Some(result) => result, None() => match start_memory_transaction(instruction, state) { Some(result) => result, None() => faulted(state, instruction.form.operation, IllegalInstruction, "unresolved data-movement form") } }
          };
    Some(result)
  }


function execute_XCHG(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) =
  if instruction.form.operation != Op_XCHG then None()
  else match execute_XCHG_local_entry(instruction, state) {
    Some(result) => Some(result),
    None() => Some(match start_stack_transaction(instruction, state) { Some(result) => result, None() => match start_memory_transaction(instruction, state) { Some(result) => result, None() => faulted(state, instruction.form.operation, IllegalInstruction, "unresolved data-movement form") } }),
  }
