
function clause control_register_is_user_bank(ControlRegister_CFI_CFICTL) = false

function clause control_register_write_needs_transition(ControlRegister_CFI_CFICTL, _, _) = false

function clause control_register_written_value(ControlRegister_CFI_CFICTL, source, _) = source

function clause control_register_write_fault(
  ControlRegister_CFI_CFICTL, source, _, candidate
) =
  if (source & 0xFFFFFFFFFFFFFFFC) != 0x0000000000000000 then
    Some(ReservedControlBitsFault)
  else if source[1] == bitone
    & not_bool(cfi_shadow_push_state_valid(candidate)) then
    Some(InvalidControlTransitionFault)
  else None()

