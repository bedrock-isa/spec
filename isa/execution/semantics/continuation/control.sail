function resume_control_phase(previous : Execution_result, response : Transaction_response)
  -> Execution_result = match pending_transaction(previous.pending).phase {
    PhaseCpuidQuery => commit_response_destination(
      previous, if response.known then response.value else 0x0000000000000000,
      { response with write_flags = false, generated_fflags = 0b00000 }
    ),
    PhasePerformanceCounter =>
      if previous.request.selector == 0x0000000000000000
         | not_bool(response.known) | not_bool(response.present) then
        faulted(previous.state, previous.pending.operation, InvalidControlState,
                "performance counter is absent or selector zero")
      else commit_response_destination(
        previous, response.value,
        { response with write_flags = false, generated_fflags = 0b00000 }
      ),
    PhaseControlTransition =>
      if previous.request.role == RequestRoleUserReturnTarget then
        completed(previous.state, pending_after(previous), CommitControl, [||])
      else match control_register_from_selector(unsigned(pending_transaction(previous.pending).captured_first[15 .. 0])) {
        None() => faulted(previous.state, previous.pending.operation,
                          InvalidControlSelectorFault, "unknown control-register selector"),
        Some(control) => {
          let updated = control_register_with_value(
            pending_after(previous), control,
            pending_transaction(previous.pending).captured_second
          );
          completed(previous.state, updated, CommitControl, [||])
        },
      },
    PhaseResetSerialize => completed(
      previous.state, warm_reset_state(previous.state), CommitControl, [||]
    ),
    PhaseIntegerExternal => commit_response_destination(previous, response.value, response),
    _ => faulted(previous.state, previous.pending.operation,
                 InvalidControlState, "unexpected transaction phase"),
  }
