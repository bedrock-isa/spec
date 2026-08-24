function execute_WRFSTATUS_local_entry(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) =
  if instruction.form.operation != Op_WRFSTATUS then None()
  else {
    let local_candidate : option(Execution_result) = match value_named(instruction, state, "src") {
    None() => None(),
    Some(source) => if (source & 0x000000000000FC00) != 0x0000000000000000 then
      Some(faulted(state, Op_WRFSTATUS, InvalidControlState, "reserved FSTATUS bits"))
    else Some(local_result(state, instruction, { state with fstatus = source & 0x00000000000003FF, fp_component_modified = true }, CommitRegisters)),
  };
    let result : Execution_result = match local_candidate {
            Some(result) => result,
            None() => start_system_request(instruction, state)
          };
    Some(result)
  }


function execute_WRFSTATUS(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) =
  if instruction.form.operation != Op_WRFSTATUS then None()
  else match execute_WRFSTATUS_local_entry(instruction, state) {
    Some(result) => Some(result),
    None() => Some(start_system_request(instruction, state)),
  }
