
function clause control_register_is_user_bank(ControlRegister_BASE_FSS) = false

function clause control_register_write_needs_transition(ControlRegister_BASE_FSS, _, _) = false

function clause control_register_written_value(ControlRegister_BASE_FSS, source, _) = source

function clause control_register_write_fault(
  ControlRegister_BASE_FSS, source, _, _
) =
  if not_bool(segment_image_valid(source))
  then Some(InvalidControlImageFault) else None()

