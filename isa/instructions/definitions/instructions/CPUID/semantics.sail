function execute_CPUID_local_entry(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) =
  if instruction.form.operation != Op_CPUID then None()
  else {
    let result : Execution_result = start_system_request(instruction, state);
    Some(result)
  }


function execute_CPUID(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) =
  if instruction.form.operation != Op_CPUID then None()
  else match execute_CPUID_local_entry(instruction, state) {
    Some(result) => Some(result),
    None() => Some(start_system_request(instruction, state)),
  }
