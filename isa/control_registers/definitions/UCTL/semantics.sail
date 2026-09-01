
function clause control_register_is_user_bank(ControlRegister_BASE_UCTL) = true

function clause control_register_write_needs_transition(
  ControlRegister_BASE_UCTL, source, state
) =
  control_register_value(state, ControlRegister_BASE_UCTL)[32] == bitone
  | source[32] == bitone

function clause control_register_written_value(ControlRegister_BASE_UCTL, source, _) = source

function clause control_register_write_fault(
  ControlRegister_BASE_UCTL, source, _, _
) =
  if (source & 0xFFFFFFFE00000000) != 0x0000000000000000
  then Some(ReservedControlBitsFault) else None()
