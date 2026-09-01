function clause control_state_value(state, ControlRegister_BASE_DTRDATA) =
  debug_trigger_selected_value(state.debug_trigger_file)

function clause control_state_with_value(
  state, ControlRegister_BASE_DTRDATA, value
) =
  { state with debug_trigger_file = debug_trigger_file_with_selected_value(
      state.debug_trigger_file, value) }

function clause control_register_is_user_bank(ControlRegister_BASE_DTRDATA) = false

function clause control_register_write_needs_transition(ControlRegister_BASE_DTRDATA, _, _) = false

function clause control_register_written_value(ControlRegister_BASE_DTRDATA, source, _) = source

function clause control_register_write_fault(
  ControlRegister_BASE_DTRDATA, source, before, _
) = debug_trigger_selected_write_fault(before.controls.debug_trigger_file, source)
