function clause control_state_value(state, ControlRegister_BASE_ICAP) =
  sail_zero_extend(state.interrupt_file.max_id, 64)

function clause control_state_with_value(state, ControlRegister_BASE_ICAP, _) = state

function clause control_register_is_user_bank(ControlRegister_BASE_ICAP) = false

function clause control_register_write_needs_transition(ControlRegister_BASE_ICAP, _, _) = false

function clause control_register_written_value(ControlRegister_BASE_ICAP, source, _) = source

function clause control_register_write_fault(ControlRegister_BASE_ICAP, _, _, _) =
  Some(InvalidControlSelectorFault)

