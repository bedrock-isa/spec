function request_role_for_ea(role : option(Ea_role)) -> Request_role = match role {
  Some(EaRole_value) => RequestRoleValue,
  Some(EaRole_address) => RequestRoleAddress,
  Some(EaRole_control_target) => RequestRoleControlTarget,
  _ => RequestRoleNone,
}

function request_domain_for_operand(domain : option(Operand_domain)) -> Request_domain = match domain {
  Some(OperandDomain_user) => RequestDomainUser,
  None() => RequestDomainCurrent,
}

function request_for_evaluation(kind : Primitive_request_kind, ordinal : int,
                                evaluation : Ea_evaluation, access : Transaction_access,
                                value : bits(64), commit_point : bool) -> Primitive_request = struct {
  kind = kind, ordinal = ordinal, role = request_role_for_ea(evaluation.role),
  domain = request_domain_for_operand(evaluation.domain),
  segment = evaluation.segment, segment_image = evaluation.segment_image,
  width = evaluation.width, range_start = evaluation.effective_address,
  range_end = add_bits(evaluation.effective_address, get_slice_int(64, evaluation.width, 0)),
  range_length = evaluation.width,
  range_wrap = unsigned(evaluation.effective_address) + evaluation.width > 18446744073709551616,
  range_end_at_modulus = unsigned(evaluation.effective_address) + evaluation.width
                         == 18446744073709551616,
  effective_address = evaluation.effective_address, linear_address = evaluation.linear_address,
  access = access, value = value, address_translation = true, commit_point = commit_point,
  memory_order = ordinal, cache_policy = 0, suppress_fault = false,
  staged_updates = evaluation.staged_updates, selector = 0x0000000000000000,
  expected = 0x0000000000000000, desired = 0x0000000000000000,
  auxiliary = 0x0000000000000000, body_length = 0, payload_bytes = [||]
}

function waiting_transaction(family : Transaction_family,
                             before : Cpu_state, after : Cpu_state,
                             instruction : Decoded_instruction, kind : Commit_kind,
                             destination : Commit_destination, phase : Continuation_phase,
                             ordinal : int, first : bits(64), second : bits(64),
                             request : Primitive_request) -> Execution_result = struct {
  state = before,
  pending = { empty_pending(Some(after), instruction.form.operation, kind) with
    destination = destination, instruction = Some(instruction),
    continuation = pending_for_family(family, {
      empty_transaction_continuation() with phase = phase, ordinal = ordinal,
      captured_first = first, captured_second = second
    }) },
  request = request, effects = [||], fault = None(), awaiting_environment = true
}

// Scalar memory execution itself is expressed by typed calc-EA/load/store/probe uops.
