
function clause control_register_is_user_bank(ControlRegister_BASE_EPC) = false

function clause control_register_write_needs_transition(ControlRegister_BASE_EPC, _, _) = true

function clause control_register_written_value(ControlRegister_BASE_EPC, source, _) = source

function clause control_register_write_fault(ControlRegister_BASE_EPC, _, _, _) = None()

