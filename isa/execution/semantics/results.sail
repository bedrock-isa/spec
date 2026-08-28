function typed_effect(kind : Effect_kind, instruction : Decoded_instruction, state : Cpu_state,
                      address : bits(64), value : bits(64), width : int,
                      order : int, suppress_fault : bool) -> Architectural_effect = struct {
  kind = kind, operation = instruction.form.operation, form_id = instruction.form.form_id,
  operands = instruction.operands, pc = state.pc, status = state.status, flags = state.flags,
  fstatus = state.fstatus, fflags = state.fflags, address = address, value = value,
  width = width, order = order, suppress_fault = suppress_fault
}

function empty_destination() -> Commit_destination = struct {
  kind = DestinationNone, index = 0x0, width = 0
}

function empty_primitive_request() -> Primitive_request = struct {
  kind = NoPrimitiveRequest, ordinal = 0, role = RequestRoleNone,
  domain = RequestDomainCurrent, segment = 0,
  segment_image = 0x0000000000000000,
  width = 0, range_start = 0x0000000000000000, range_end = 0x0000000000000000,
  range_length = 0, range_wrap = false, range_end_at_modulus = false,
  effective_address = 0x0000000000000000, linear_address = 0x0000000000000000,
  access = NoTransactionAccess, value = 0x0000000000000000,
  address_translation = false, commit_point = false, memory_order = 0,
  cache_policy = 0,
  suppress_fault = false, staged_updates = [||], selector = 0x0000000000000000,
  expected = 0x0000000000000000, desired = 0x0000000000000000,
  auxiliary = 0x0000000000000000, body_length = 0, payload_bytes = [||]
}

function empty_pending(after : option(Cpu_state),
                       operation : Semantic_operation, kind : Commit_kind) -> Pending_commit = struct {
  kind = kind, operation = operation, destination = empty_destination(),
  after = after, instruction = None(), phase = ContinuationNone,
  ordinal = 0, captured_first = 0x0000000000000000,
  captured_second = 0x0000000000000000, memory_writes = [||], atomic = true
  , repeat_body = None(), repeat_bytes = [||], repeat_parent_active = false,
  event = None(), event_attempt = 0, boundary_class = BoundaryOrdinary
  , fp_pending = empty_fp_pending()
  , vector_payload0 = [||], vector_payload1 = [||]
  , uop_program = [||], uop_cursor = 0, uop_values = [||]
  , uop_pending_destination = 0
}

function completed(_before : Cpu_state, after : Cpu_state, kind : Commit_kind,
  effects : list(Architectural_effect)) -> Execution_result = struct {
  state = after,
  pending = empty_pending(None(), Op_NOP, kind),
  request = empty_primitive_request(),
  effects = effects,
  fault = None(),
  awaiting_environment = false
}

function faulted(state : Cpu_state, operation : Semantic_operation,
  kind : Fault_kind, detail : string) -> Execution_result = struct {
  state = state,
  pending = empty_pending(None(), operation, CommitNone),
  request = empty_primitive_request(),
  effects = [||],
  fault = Some(struct {
    kind = kind, operation = operation, detail = detail,
    error_code = if kind == ExtensionUnavailable then 0x0000000000000003
      else if kind == DivideOverflow then 0x0000000000000001
      else if kind == InvalidControlState then 0x0000000000000002
      else 0x0000000000000000,
    bus_error = false
  }),
  awaiting_environment = false
}

function pending_after(result : Execution_result) -> Cpu_state =
  match result.pending.after {
    Some(state) => state,
    None() => result.state,
  }

function faulted_with_error_code(state : Cpu_state, operation : Semantic_operation,
                                 kind : Fault_kind, detail : string,
                                 error_code : bits(64)) -> Execution_result = {
  let base = faulted(state, operation, kind, detail);
  { base with fault = Some(struct {
      kind = kind, operation = operation, detail = detail,
      error_code = error_code, bus_error = false
    }) }
}
