function clause control_state_value(state, ControlRegister_BASE_ITHRESH) =
  sail_zero_extend(state.interrupt_file.threshold, 64)

function clause control_state_with_value(
  state, ControlRegister_BASE_ITHRESH, value
) = {
  var updated = state;
  updated.interrupt_file.threshold = value[23 .. 0];
  updated
}

function clause control_register_is_user_bank(ControlRegister_BASE_ITHRESH) = false

function clause control_register_write_needs_transition(ControlRegister_BASE_ITHRESH, _, _) = false

function clause control_register_written_value(ControlRegister_BASE_ITHRESH, source, _) = source

function clause control_register_write_fault(
  ControlRegister_BASE_ITHRESH, source, _, _
) =
  if source[63 .. 24] != 0x0000000000
  then Some(ReservedControlBitsFault) else None()

