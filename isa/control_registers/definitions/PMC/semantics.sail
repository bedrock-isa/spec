
function clause control_register_is_user_bank(ControlRegister_BASE_PMC) = false

function clause control_register_write_needs_transition(ControlRegister_BASE_PMC, _, _) = false

function clause control_register_written_value(ControlRegister_BASE_PMC, source, _) = source

function clause control_register_write_fault(
  ControlRegister_BASE_PMC, source, _, _
) =
  if (source & 0xFFFFFFFFFFFFFFFE) != 0x0000000000000000
  then Some(ReservedControlBitsFault) else None()

