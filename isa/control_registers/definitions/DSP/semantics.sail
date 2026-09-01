
function clause control_register_is_user_bank(ControlRegister_BASE_DSP) = false

function clause control_register_write_needs_transition(ControlRegister_BASE_DSP, _, _) = false

function clause control_register_written_value(ControlRegister_BASE_DSP, source, _) = source

function clause control_register_write_fault(
  ControlRegister_BASE_DSP, source, _, _
) =
  if (source & 0x000000000000003F) != 0x0000000000000000
  then Some(InvalidControlImageFault) else None()

