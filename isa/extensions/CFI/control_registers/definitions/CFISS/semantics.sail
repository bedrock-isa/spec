
function clause control_register_is_user_bank(ControlRegister_CFI_CFISS) = false

function clause control_register_write_needs_transition(ControlRegister_CFI_CFISS, _, _) = false

function clause control_register_written_value(ControlRegister_CFI_CFISS, source, _) = source

function clause control_register_write_fault(
  ControlRegister_CFI_CFISS, source, _, candidate
) =
  if not_bool(cfi_shadow_segment_valid(source)) then
    Some(InvalidControlImageFault)
  else if cfi_shadow_enabled(candidate)
    & not_bool(cfi_shadow_push_state_valid(candidate)) then
    Some(InvalidControlTransitionFault)
  else None()

