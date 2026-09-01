function clause control_state_value(state, ControlRegister_BASE_DTRSEL) =
  sail_zero_extend(state.debug_trigger_file.selector, 64)

function clause control_state_with_value(
  state, ControlRegister_BASE_DTRSEL, value
) = {
  var updated = state;
  updated.debug_trigger_file.selector = value[17 .. 0];
  updated
}

function clause control_register_is_user_bank(ControlRegister_BASE_DTRSEL) = false

function clause control_register_write_needs_transition(ControlRegister_BASE_DTRSEL, _, _) = false

function clause control_register_written_value(ControlRegister_BASE_DTRSEL, source, _) = source

function clause control_register_write_fault(
  ControlRegister_BASE_DTRSEL, source, before, _
) =
  if (source & 0xFFFFFFFFFFFC0000) != 0x0000000000000000 then
    Some(ReservedControlBitsFault)
  else if unsigned(source[15 .. 0]) >= before.controls.debug_trigger_file.slot_count
          | unsigned(source[17 .. 16]) >= 3 then
    Some(InvalidControlSelectorFault)
  else None()
