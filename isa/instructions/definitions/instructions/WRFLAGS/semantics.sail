function execute_WRFLAGS_local_entry(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) =
  if instruction.form.operation != Op_WRFLAGS then None()
  else {
    let local_candidate : option(Execution_result) = match value_named(instruction, state, "src") {
    None() => None(),
    Some(source) => if (source & 0x000000000000FFF0) != 0x0000000000000000 then Some(faulted(state, Op_WRFLAGS, IllegalInstruction, "reserved FLAGS bits"))
    else Some(local_result(state, instruction, { state with flags = source[3 .. 0] }, CommitRegisters)),
  };
    let result : Execution_result = match local_candidate {
            Some(result) => result,
            None() => start_system_request(instruction, state)
          };
    Some(result)
  }


function execute_WRFLAGS(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) =
  if instruction.form.operation != Op_WRFLAGS then None()
  else match execute_WRFLAGS_local_entry(instruction, state) {
    Some(result) => Some(result),
    None() => Some(start_system_request(instruction, state)),
  }
