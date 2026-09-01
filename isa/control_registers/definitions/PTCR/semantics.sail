
function clause control_register_is_user_bank(ControlRegister_BASE_PTCR) = false

function clause control_register_write_needs_transition(ControlRegister_BASE_PTCR, _, _) = true

function clause control_register_written_value(ControlRegister_BASE_PTCR, source, _) = source

function clause control_register_write_fault(
  ControlRegister_BASE_PTCR, source, _, _
) =
  if (source & 0xFF00000000000F7E) != 0x0000000000000000
  then Some(ReservedControlBitsFault) else None()

