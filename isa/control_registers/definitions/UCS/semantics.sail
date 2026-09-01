
function clause control_register_is_user_bank(ControlRegister_BASE_UCS) = true

function clause control_register_write_needs_transition(
  ControlRegister_BASE_UCS, _, state
) =
  control_register_value(state, ControlRegister_BASE_UCTL)[32] == bitone

function clause control_register_written_value(ControlRegister_BASE_UCS, source, _) = source

function clause control_register_write_fault(ControlRegister_BASE_UCS, _, _, _) = None()
