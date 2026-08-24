function execute_SETF_local_entry(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) =
  if instruction.form.operation != Op_SETF then None()
  else {
    let local_candidate : option(Execution_result) = match value_named(instruction, state, "mask") {
    Some(mask) => {
      let selected = mask[3 .. 0];
      Some(local_result(state, instruction, { state with flags = selected }, CommitRegisters))
    },
    None() => None(),
  };
    let result : Execution_result = match local_candidate {
            Some(result) => result,
            None() => start_system_request(instruction, state)
          };
    Some(result)
  }


function execute_SETF(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) =
  if instruction.form.operation != Op_SETF then None()
  else match execute_SETF_local_entry(instruction, state) {
    Some(result) => Some(result),
    None() => Some(start_system_request(instruction, state)),
  }
