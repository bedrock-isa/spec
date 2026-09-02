
function clause control_register_is_user_bank(ControlRegister_BASE_PTCR) = false

function clause control_register_write_needs_transition(ControlRegister_BASE_PTCR, _, _) = true

function clause control_register_written_value(ControlRegister_BASE_PTCR, source, _) = source

function ptcr_image_fault(source : bits(64)) -> option(Fault_kind) =
  if (source & 0xFF00000000003FF0) != 0x0000000000000000 then
    Some(ReservedControlBitsFault)
  else if source[0] == bitone
    & source[3 .. 1] != 0b010
    & source[3 .. 1] != 0b011 then
    Some(InvalidControlImageFault)
  else None()

function clause control_register_write_fault(
  ControlRegister_BASE_PTCR, source, _, _
) = ptcr_image_fault(source)
