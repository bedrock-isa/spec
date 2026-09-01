function clause control_state_value(state, ControlRegister_BASE_ISEL) =
  sail_zero_extend(state.interrupt_file.selector, 64)

function clause control_state_with_value(
  state, ControlRegister_BASE_ISEL, value
) = {
  var updated = state;
  updated.interrupt_file.selector = value[19 .. 0];
  updated
}

function clause control_register_is_user_bank(ControlRegister_BASE_ISEL) = false

function clause control_register_write_needs_transition(ControlRegister_BASE_ISEL, _, _) = false

function clause control_register_written_value(ControlRegister_BASE_ISEL, source, _) = source

function clause control_register_write_fault(
  ControlRegister_BASE_ISEL, source, before, _
) =
  if source[63 .. 20] != 0x00000000000 then
    Some(ReservedControlBitsFault)
  else if not_bool(interrupt_word_valid(
    before.controls.interrupt_file, unsigned(source[17 .. 0])
  )) then Some(InvalidControlSelectorFault)
  else None()

