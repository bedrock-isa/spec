
function clause control_register_is_user_bank(ControlRegister_BASE_BOOTPC) = false

function clause control_register_write_needs_transition(ControlRegister_BASE_BOOTPC, _, _) = false

function clause control_register_written_value(ControlRegister_BASE_BOOTPC, source, _) = source

function clause control_register_write_fault(ControlRegister_BASE_BOOTPC, _, _, _) = None()

