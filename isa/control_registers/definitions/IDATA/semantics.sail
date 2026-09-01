function clause control_state_value(state, ControlRegister_BASE_IDATA) =
  interrupt_idata_value(state.interrupt_file)

function clause control_state_with_value(
  state, ControlRegister_BASE_IDATA, value
) =
  { state with interrupt_file = interrupt_file_with_idata(state.interrupt_file, value) }

function clause control_register_is_user_bank(ControlRegister_BASE_IDATA) = false

function clause control_register_write_needs_transition(ControlRegister_BASE_IDATA, _, _) = false

function clause control_register_written_value(ControlRegister_BASE_IDATA, source, _) = source

function clause control_register_write_fault(
  ControlRegister_BASE_IDATA, source, before, _
) =
  if interrupt_selected_bank(before.controls.interrupt_file) == 0 then
    Some(InvalidControlSelectorFault)
  else if interrupt_word_source_has_reserved_bit(
    before.controls.interrupt_file,
    interrupt_selected_word(before.controls.interrupt_file),
    source,
    0
  ) then Some(ReservedControlBitsFault)
  else None()

