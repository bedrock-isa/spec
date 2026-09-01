function start_system_request(system_operation : System_request_uop_operation,
                              instruction : Decoded_instruction, state : Cpu_state)
  -> Execution_result = {
  let operation = instruction.form.operation;
  let kind = if system_operation == SystemCpuid then CpuidQueryRequest
    else if system_operation == SystemPerformanceCounter then PerformanceCounterRequest
    else ControlTransitionRequest;
  let phase = if system_operation == SystemCpuid then PhaseCpuidQuery
    else if system_operation == SystemPerformanceCounter then PhasePerformanceCounter
    else PhaseControlTransition;
  let selector : bits(64) = if system_operation == SystemCpuid then match value_named(instruction, state, Operand_reg) {
      Some(value) => value, None() => 0x0000000000000000
    }
    else if system_operation == SystemPerformanceCounter then match value_named(instruction, state, Operand_counter_id) {
      Some(value) => value & 0x000000000000FFFF, None() => 0x0000000000000000
    }
    else match value_named(instruction, state, Operand_cr) {
      Some(value) => value & 0x000000000000FFFF, None() => 0x0000000000000000
    };
  let value : bits(64) = if system_operation == SystemWriteControl then match value_named(instruction, state, Operand_src) {
      Some(item) => item, None() => 0x0000000000000000
    } else 0x0000000000000000;
  let wrcr_selector = unsigned(selector[15 .. 0]);
  let selected_control = control_register_from_selector(wrcr_selector);
  let candidate = if system_operation == SystemWriteControl then
    match selected_control {
      Some(control) => control_register_with_value(
        state, control, control_register_written_value(control, value, state)
      ),
      None() => state,
    }
    else state;
  let user_bank_write = system_operation == SystemWriteControl
    & (match selected_control {
      Some(control) => control_register_is_user_bank(control),
      None() => false,
    });
  let user_bank_live = control_register_value(
    candidate, ControlRegister_BASE_UCTL
  )[32] == bitone;
  let write_fault : option(Fault_kind) = if system_operation == SystemWriteControl then
    match selected_control {
      Some(control) => control_register_write_fault(control, value, state, candidate),
      None() => Some(InvalidControlSelectorFault),
    }
    else None();
  let entry_invalid = system_operation == SystemWriteControl
    & selected_control_is(selected_control, ControlRegister_BASE_EPC)
    & (value & 0x000000000000000F) != 0x0000000000000000;
  let uctl_invalid = system_operation == SystemWriteControl
    & selected_control_is(selected_control, ControlRegister_BASE_UCTL)
    & ((value & 0xFFFFFFFE00000000) != 0x0000000000000000
       | (value & 0x00000000FFD10000) != 0x0000000000000000
       | value[15 .. 4] != 0x000);
  let user_bank_invalid = user_bank_write
    & ((status_user_origin(state.status) & not_bool(user_bank_live))
       | (user_bank_live & not_bool(user_return_bank_image_valid(candidate))));
  let base_request = { empty_primitive_request() with
    kind = kind, role = RequestRoleNone, selector = selector,
    value = if system_operation == SystemWriteControl then match selected_control {
      Some(control) => control_register_written_value(control, value, state),
      None() => value,
    } else value,
    access = if system_operation == SystemWriteControl then AccessStore else AccessLoad,
    commit_point = true };
  let request = if user_bank_write & user_bank_live then {
      target_probe_request(
        0,
        control_register_value(candidate, ControlRegister_BASE_UCS),
        control_register_value(candidate, ControlRegister_BASE_UPC)
      ) with
      kind = ControlTransitionRequest, role = RequestRoleUserBankTarget,
      selector = selector, value = value, commit_point = true
    } else base_request;
  if system_operation == SystemPerformanceCounter & selector == 0x0000000000000000 then faulted(
    state, operation, InvalidControlState, "RDPMC selector zero"
  )
  else match write_fault {
    Some(kind) => faulted(state, operation, kind, "invalid control-register write"),
    None() =>
      if entry_invalid | uctl_invalid then faulted(
        state, operation, InvalidControlImageFault,
        "invalid control-register image"
      )
      else if user_bank_invalid then faulted(
        state, operation, InvalidControlTransitionFault,
        "invalid control-register transition"
      )
      else waiting_transaction(TransactionControl,
        state, advance_pc(state, instruction), instruction, CommitControl,
        commit_destination_for(instruction.operands, 8), phase, 0, selector, request.value, request
      ),
  }
}
