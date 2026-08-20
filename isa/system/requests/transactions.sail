function start_system_request(instruction : Decoded_instruction, state : Cpu_state)
  -> Execution_result = {
  let operation = instruction.form.operation;
  let kind = if operation == Op_CPUID then CpuidQueryRequest
    else if operation == Op_RDPMC then PerformanceCounterRequest
    else ControlTransitionRequest;
  let phase = if operation == Op_CPUID then PhaseCpuidQuery
    else if operation == Op_RDPMC then PhasePerformanceCounter
    else PhaseControlTransition;
  let selector : bits(64) = if operation == Op_CPUID then match value_named(instruction, state, "reg") {
      Some(value) => value, None() => 0x0000000000000000
    }
    else if operation == Op_RDPMC then match value_named(instruction, state, "counter_id") {
      Some(value) => value & 0x000000000000FFFF, None() => 0x0000000000000000
    }
    else match value_named(instruction, state, "cr") {
      Some(value) => value & 0x000000000000FFFF, None() => 0x0000000000000000
    };
  let value : bits(64) = if operation == Op_WRCR then match value_named(instruction, state, "src") {
      Some(item) => item, None() => 0x0000000000000000
    } else 0x0000000000000000;
  let wrcr_selector = unsigned(selector[15 .. 0]);
  let ptcr_invalid = operation == Op_WRCR & wrcr_selector == 0
    & ((value[11 .. 8] != 0x0 & value[11 .. 8] != 0x1)
       | value[6 .. 1] != 0b000000
       | (value[11 .. 8] == 0x0 & value[63 .. 48] != 0x0000)
       | (value[11 .. 8] == 0x1 & value[63 .. 56] != 0x00));
  let ascr_invalid = operation == Op_WRCR & wrcr_selector == 1
    & (value[63 .. 32] != 0x00000000 | value[15 .. 1] != 0b000000000000000);
  let entry_invalid = operation == Op_WRCR & (wrcr_selector == 256 | wrcr_selector == 272)
    & (value & 0x000000000000000F) != 0x0000000000000000;
  let urctl_invalid = operation == Op_WRCR & wrcr_selector == 269
    & ((value & 0xFFFFFFFE00000000) != 0x0000000000000000
       | value[31 .. 22] != 0b0000000000 | value[20] == bitone | value[16] == bitone
       | value[15 .. 4] != 0x000
       | not_bool(segment_image_valid(state.controls[8]))
       | not_bool(segment_image_valid(state.controls[9]))
       | not_bool(segment_image_valid(state.controls[10])));
  let ecr_invalid = operation == Op_WRCR & wrcr_selector == 2
    & ((value & 0xFFFFFFFFFFFFF07E) != 0x0000000000000000
       | (value[0] == bitone & not_bool(event_control_bank_valid(state))));
  let request = { empty_primitive_request() with
    kind = kind, role = instruction.form.family, selector = selector,
    value = if operation == Op_WRCR & wrcr_selector == 2 then
      (value & 0x0000000000000F01) | (state.controls[2] & 0x0000000000000080)
      else value,
    access = if operation == Op_WRCR then AccessStore else AccessLoad,
    commit_point = true, state_image = state };
  if operation == Op_RDPMC & selector == 0x0000000000000000 then faulted(
    state, operation, InvalidControlState, "RDPMC selector zero"
  )
  else if ptcr_invalid | ascr_invalid | entry_invalid | urctl_invalid | ecr_invalid then faulted(
    state, operation, InvalidControlState, "invalid control-register transition image"
  )
  else waiting_transaction(
    state, advance_pc(state, instruction), instruction, CommitControl,
    commit_destination_for(instruction.operands, 8), phase, 0, selector, request.value, request
  )
}

