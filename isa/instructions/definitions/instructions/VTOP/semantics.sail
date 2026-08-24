function execute_VTOP_local_entry(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) =
  if instruction.form.operation != Op_VTOP then None()
  else {
    let local_candidate : option(Execution_result) =
      if state.controls[0][0] == bitzero then match (value_named(instruction, state, "virt"), destination_named(instruction, "phys", 8)) {
    (Some(address), Some(destination)) => { var updated = write_local_destination(state, instruction.form.operation, destination, address); updated.flags = 0b1111; Some(local_result(state, instruction, updated, CommitRegisters)) },
    _ => None(),
  } else None();
    let result : Execution_result = match local_candidate {
            Some(result) => result,
            None() => start_tlb_context_transaction(instruction, state)
          };
    Some(result)
  }


function execute_VTOP(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) =
  if instruction.form.operation != Op_VTOP then None()
  else match execute_VTOP_local_entry(instruction, state) {
    Some(result) => Some(result),
    None() => Some(start_tlb_context_transaction(instruction, state)),
  }
