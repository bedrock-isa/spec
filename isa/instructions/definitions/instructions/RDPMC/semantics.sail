function execute_RDPMC_local_entry(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) =
  if instruction.form.operation != Op_RDPMC then None()
  else {
    let result : Execution_result = start_system_request(instruction, state);
    Some(result)
  }


function execute_RDPMC(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) =
  if instruction.form.operation != Op_RDPMC then None()
  else match execute_RDPMC_local_entry(instruction, state) {
    Some(result) => Some(result),
    None() => Some(start_system_request(instruction, state)),
  }
