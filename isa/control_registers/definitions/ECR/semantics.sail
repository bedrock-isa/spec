
function clause control_register_is_user_bank(ControlRegister_BASE_ECR) = false

function clause control_register_write_needs_transition(
  ControlRegister_BASE_ECR, source, state
) =
  source[0] == bitone
  & control_register_value(state, ControlRegister_BASE_ECR)[0] == bitzero

function clause control_register_written_value(
  ControlRegister_BASE_ECR, source, state
) =
  (source & 0x0000000000000F01)
  | (control_register_value(state, ControlRegister_BASE_ECR)
     & 0x0000000000000080)

function clause control_register_write_fault(
  ControlRegister_BASE_ECR, source, before, candidate
) =
  if (source & 0xFFFFFFFFFFFFF07E) != 0x0000000000000000 then
    Some(ReservedControlBitsFault)
  else if source[0] == bitone
    & control_register_value(before, ControlRegister_BASE_ECR)[0] == bitzero
    & not_bool(event_control_bank_valid(candidate)) then
    Some(InvalidControlTransitionFault)
  else None()

