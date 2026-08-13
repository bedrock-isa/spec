function zero_registers() -> Registers = [
  0x0000000000000000, 0x0000000000000000, 0x0000000000000000, 0x0000000000000000,
  0x0000000000000000, 0x0000000000000000, 0x0000000000000000, 0x0000000000000000,
  0x0000000000000000, 0x0000000000000000, 0x0000000000000000, 0x0000000000000000,
  0x0000000000000000, 0x0000000000000000, 0x0000000000000000, 0x0000000000000000
]

function zero_floating_registers() -> Floating_registers = [
  0x0000000000000000, 0x0000000000000000, 0x0000000000000000, 0x0000000000000000,
  0x0000000000000000, 0x0000000000000000, 0x0000000000000000, 0x0000000000000000,
  0x0000000000000000, 0x0000000000000000, 0x0000000000000000, 0x0000000000000000,
  0x0000000000000000, 0x0000000000000000, 0x0000000000000000, 0x0000000000000000
]

function zero_segments() -> Segment_registers = [
  0x0000000000000000, 0x0000000000000000, 0x0000000000000000, 0x0000000000000000,
  0x0000000000000000, 0x0000000000000000, 0x0000000000000000, 0x0000000000000000,
  0x0000000000000000
]

function zero_controls() -> Control_registers = [
  0x0000000000000000, 0x0000000000000000, 0x0000000000000000, 0x0000000000000000,
  0x0000000000000000, 0x0000000000000000, 0x0000000000000000, 0x0000000000000000,
  0x0000000000000000, 0x0000000000000000, 0x0000000000000000, 0x0000000000000000,
  0x0000000000000000, 0x0000000000000000, 0x0000000000000000, 0x0000000000000000,
  0x0000000000000000, 0x0000000000000000, 0x0000000000000000, 0x0000000000000000,
  0x0000000000000000, 0x0000000000000000, 0x0000000000000000, 0x0000000000000000,
  0x0000000000000000, 0x0000000000000000, 0x0000000000000000, 0x0000000000000000,
  0x0000000000000000, 0x0000000000000000, 0x0000000000000000, 0x0000000000000000
]

function initial_cpu() -> Cpu_state = struct {
  registers = zero_registers(),
  floating_registers = zero_floating_registers(),
  segments = zero_segments(),
  controls = zero_controls(),
  sp = 0x0000000000000000,
  pc = 0x0000000000000000,
  flags = 0x0,
  status = 0x0000000000000000,
  fflags = 0b00000,
  fstatus = 0x0000000000000000,
  supervisor = false,
  fp_enabled = false,
  fptrans_enabled = false,
  halted = false,
  run_state = Running,
  event_depth = 0,
  event_stack_level = 0,
  cache_maintenance_granule = 64,
  save_area_size = 384,
  save_fixed_size = 192,
  save_format = 0x0,
  save_bitmap_words = 1,
  fp_component_present = true,
  fp_component_id = 1,
  fp_component_bitmap_bit = 0,
  fp_component_offset = 192,
  fp_component_size = 192,
  fp_component_alignment = 64,
  fp_component_init_policy = 1,
  fp_component_modified = false,
  repeat_state = struct {
    active = false, grouped = false, counter = 0x0, remaining = 0x0000000000000000,
    condition = 0x0, body_bytes = 0x0000, body_start = 0x0000000000000000,
    fixed_body = [||], group_progress = 0
  },
  nmi_latched_source = 0x000000,
  nmi_relatched = false,
  nmi_relatched_source = 0x000000,
  machine_check_pending = false,
  machine_check_payload = 0x00000000,
  machine_check_error_code = 0x0000000000000000,
  machine_check_fault_ea = 0x0000000000000000,
  machine_check_fault_linear = 0x0000000000000000,
  machine_check_event_aux = 0x0000000000000000
}

function next_pc(state : Cpu_state, instruction : Decoded_instruction) -> bits(64) =
  add_bits(state.pc, get_slice_int(64, instruction.encoded_length, 0))

function advance_pc(state : Cpu_state, instruction : Decoded_instruction) -> Cpu_state =
  { state with pc = next_pc(state, instruction) }

function typed_effect(kind : Effect_kind, instruction : Decoded_instruction, state : Cpu_state,
                      address : bits(64), value : bits(64), width : int,
                      order : int, suppress_fault : bool) -> Architectural_effect = struct {
  kind = kind, operation = instruction.form.operation, form_id = instruction.form.form_id,
  operands = instruction.operands, pc = state.pc, status = state.status, flags = state.flags,
  fstatus = state.fstatus, fflags = state.fflags, address = address, value = value,
  width = width, order = order, suppress_fault = suppress_fault
}

function empty_destination() -> Commit_destination = struct {
  kind = "", index = 0x0, width = 0
}

function empty_primitive_request() -> Primitive_request = struct {
  kind = NoPrimitiveRequest, ordinal = 0, role = "", domain = "", segment = 0,
  segment_image = 0x0000000000000000,
  width = 0, range_start = 0x0000000000000000, range_end = 0x0000000000000000,
  range_length = 0, range_wrap = false, range_end_at_modulus = false,
  effective_address = 0x0000000000000000, linear_address = 0x0000000000000000,
  access = NoTransactionAccess, value = 0x0000000000000000,
  address_translation = false, commit_point = false, memory_order = 0,
  address_type = 0, cache_policy = 0,
  suppress_fault = false, staged_updates = [||], selector = 0x0000000000000000,
  expected = 0x0000000000000000, desired = 0x0000000000000000,
  auxiliary = 0x0000000000000000, body_length = 0, payload_bytes = [||],
  fp_request = empty_fp_request(),
  state_image = initial_cpu()
}

function empty_pending(before : Cpu_state, after : Cpu_state,
                       operation : Semantic_operation, kind : Commit_kind) -> Pending_commit = struct {
  kind = kind, operation = operation, destination = empty_destination(),
  before = before, after = after, instruction = None(), phase = ContinuationNone,
  ordinal = 0, captured_first = 0x0000000000000000,
  captured_second = 0x0000000000000000, memory_writes = [||], atomic = true
  , repeat_prefix = None(), repeat_body = None(), repeat_bytes = [||],
  repeat_tail = [||], repeat_tail_length = 0,
  repeat_parent_active = false, repeat_parent_grouped = false,
  event = None(), event_attempt = 0, boundary_class = BoundaryOrdinary
  , fp_pending = empty_fp_pending()
}

function completed(_before : Cpu_state, after : Cpu_state, kind : Commit_kind,
                   effects : list(Architectural_effect)) -> Execution_result = struct {
  state = after,
  pending = empty_pending(_before, after, Op_NOP, kind),
  request = empty_primitive_request(),
  effects = effects,
  fault = None(),
  awaiting_environment = false
}

function faulted(state : Cpu_state, operation : Semantic_operation,
                 kind : Fault_kind, detail : string) -> Execution_result = struct {
  state = state,
  pending = empty_pending(state, state, operation, CommitNone),
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

function faulted_with_error_code(state : Cpu_state, operation : Semantic_operation,
                                 kind : Fault_kind, detail : string,
                                 error_code : bits(64)) -> Execution_result = {
  let base = faulted(state, operation, kind, detail);
  { base with fault = Some(struct {
      kind = kind, operation = operation, detail = detail,
      error_code = error_code, bus_error = false
    }) }
}

