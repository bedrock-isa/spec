function clause control_state_value(state, ControlRegister_BASE_ITOP) =
  sail_zero_extend(interrupt_top(state.interrupt_file), 64)

function clause control_state_with_value(state, ControlRegister_BASE_ITOP, _) = state

function clause control_register_is_user_bank(ControlRegister_BASE_ITOP) = false

function clause control_register_write_needs_transition(ControlRegister_BASE_ITOP, _, _) = false

function clause control_register_written_value(ControlRegister_BASE_ITOP, source, _) = source

function clause control_register_write_fault(ControlRegister_BASE_ITOP, _, _, _) =
  Some(InvalidControlSelectorFault)

