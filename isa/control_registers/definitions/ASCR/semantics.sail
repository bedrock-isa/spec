
function clause control_register_is_user_bank(ControlRegister_BASE_ASCR) = false

function clause control_register_write_needs_transition(ControlRegister_BASE_ASCR, _, _) = true

function clause control_register_written_value(ControlRegister_BASE_ASCR, source, _) = source

function clause control_register_write_fault(
  ControlRegister_BASE_ASCR, source, _, _
) =
  if (source & 0xFFFFFFFF0000FFFE) != 0x0000000000000000
  then Some(ReservedControlBitsFault) else None()

