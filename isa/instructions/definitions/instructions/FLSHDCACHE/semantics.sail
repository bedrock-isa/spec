function execute_FLSHDCACHE_local_entry(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) =
  if instruction.form.operation != Op_FLSHDCACHE then None()
  else {
    let result : Execution_result =
    if instruction.form.operation == Op_MOVNT then match start_memory_transaction(instruction, state) { Some(result) => result, None() => faulted(state, Op_MOVNT, IllegalInstruction, "missing non-temporal store operand") } else match start_cache_transaction(instruction, state) { Some(result) => result, None() => faulted(state, instruction.form.operation, IllegalInstruction, "missing cache address operand") };
    Some(result)
  }


function execute_FLSHDCACHE(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) =
  if instruction.form.operation != Op_FLSHDCACHE then None()
  else match execute_FLSHDCACHE_local_entry(instruction, state) {
    Some(result) => Some(result),
    None() => Some(if instruction.form.operation == Op_MOVNT then match start_memory_transaction(instruction, state) { Some(result) => result, None() => faulted(state, Op_MOVNT, IllegalInstruction, "missing non-temporal store operand") } else match start_cache_transaction(instruction, state) { Some(result) => result, None() => faulted(state, instruction.form.operation, IllegalInstruction, "missing cache address operand") }),
  }
