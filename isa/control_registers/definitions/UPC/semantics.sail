
function clause control_register_is_user_bank(ControlRegister_BASE_UPC) = true

function clause control_register_write_needs_transition(
  ControlRegister_BASE_UPC, _, state
) =
  control_register_value(state, ControlRegister_BASE_UCTL)[32] == bitone

function clause control_register_written_value(ControlRegister_BASE_UPC, source, _) = source

function clause control_register_write_fault(ControlRegister_BASE_UPC, _, _, _) = None()
