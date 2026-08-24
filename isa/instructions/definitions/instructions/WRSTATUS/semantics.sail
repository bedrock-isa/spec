function execute_WRSTATUS_local_entry(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) =
  if instruction.form.operation != Op_WRSTATUS then None()
  else {
    let local_candidate : option(Execution_result) = match value_named(instruction, state, "src") {
    None() => None(),
    Some(source) => {
      let candidate = source & 0x000000000000FFFF;
      if (candidate & 0x000000000000F800) != 0x0000000000000000 | (candidate & 0x00000000000007D1) != (state.status & 0x00000000000007D1)
      then Some(faulted(state, Op_WRSTATUS, InvalidControlState, "reserved or immutable STATUS bits"))
      else Some(local_result(state, instruction, { state with status = candidate }, CommitRegisters))
    },
  };
    let result : Execution_result = match local_candidate {
      Some(result) => result,
      None() => start_system_request(instruction, state),
    };
    Some(result)
  }


function execute_WRSTATUS(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) =
  if instruction.form.operation != Op_WRSTATUS then None()
  else match execute_WRSTATUS_local_entry(instruction, state) {
    Some(result) => Some(result),
    None() => Some(start_system_request(instruction, state)),
  }
