
function clause control_register_is_user_bank(ControlRegister_CFI_CFISP) = false

function clause control_register_write_needs_transition(ControlRegister_CFI_CFISP, _, _) = false

function clause control_register_written_value(ControlRegister_CFI_CFISP, source, _) = source

function clause control_register_write_fault(
  ControlRegister_CFI_CFISP, source, _, candidate
) =
  if (source & 0x000000000000000F) != 0x0000000000000000 then
    Some(InvalidControlImageFault)
  else if cfi_shadow_enabled(candidate)
    & not_bool(cfi_shadow_push_state_valid(candidate)) then
    Some(InvalidControlTransitionFault)
  else None()

