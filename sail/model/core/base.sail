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

function flag_z(flags : bits(4)) -> bool = flags[3] == bitone
function flag_n(flags : bits(4)) -> bool = flags[2] == bitone
function flag_c(flags : bits(4)) -> bool = flags[1] == bitone
function flag_v(flags : bits(4)) -> bool = flags[0] == bitone

function condition_holds(condition : int, flags : bits(4)) -> bool = match condition {
  0 => true,
  1 => false,
  2 => flag_z(flags),
  3 => not_bool(flag_z(flags)),
  4 => flag_c(flags),
  5 => not_bool(flag_c(flags)),
  6 => flag_n(flags),
  7 => not_bool(flag_n(flags)),
  8 => flag_v(flags),
  9 => not_bool(flag_v(flags)),
  10 => flag_c(flags) | flag_z(flags),
  11 => not_bool(flag_c(flags)) & not_bool(flag_z(flags)),
  12 => flag_n(flags) != flag_v(flags),
  13 => flag_n(flags) == flag_v(flags),
  14 => flag_z(flags) | (flag_n(flags) != flag_v(flags)),
  _ => not_bool(flag_z(flags)) & (flag_n(flags) == flag_v(flags)),
}

function condition_field(fields : list(Decoded_field)) -> option(int) = match fields {
  [||] => None(),
  field :: tail => if field.kind == FieldCondition then Some(field.value) else condition_field(tail),
}

function predicate_holds(instruction : Decoded_instruction, state : Cpu_state) -> bool =
  match condition_field(instruction.fields) {
    Some(condition) => condition_holds(condition, state.flags),
    None() => true,
  }

function find_operand_by_name(name : string, operands : list(Decoded_operand)) -> option(Decoded_operand) =
  match operands {
    [||] => None(),
    operand :: tail => if operand.name == name then Some(operand) else find_operand_by_name(name, tail),
  }

function first_ea_operand(operands : list(Decoded_operand)) -> option(Decoded_operand) = match operands {
  [||] => None(),
  operand :: tail => match operand.ea { Some(_) => Some(operand), None() => first_ea_operand(tail) },
}

function commit_destination_for(operands : list(Decoded_operand), width : int) -> Commit_destination =
  match operands {
    [||] => empty_destination(),
    operand :: tail =>
      if operand.access == AccessWrite | operand.access == AccessReadWrite then
        if operand.type_name == "Rn" then struct {
          kind = "Rn", index = operand.value[3 .. 0], width = width
        }
        else if operand.type_name == "Fn" then struct {
          kind = "Fn", index = operand.value[3 .. 0], width = width
        }
        else if operand.type_name == "SP" then struct {
          kind = "SP", index = 0x0, width = width
        }
        else commit_destination_for(tail, width)
      else commit_destination_for(tail, width),
  }

function size_code_bytes(code : string) -> int =
  if code == "B" then 1
  else if code == "W" then 2
  else if code == "S" then 4
  else if code == "L" then 4
  else 8

function string_list_count(items : list(string)) -> int = match items {
  [||] => 0,
  _ :: tail => 1 + string_list_count(tail),
}

function string_at(items : list(string), index : int) -> string = match items {
  [||] => "Q",
  item :: tail => if index <= 0 then item else string_at(tail, index - 1),
}

val condition_size_field : list(Decoded_field) -> option(int)

function operation_width(instruction : Decoded_instruction) -> int =
  match condition_size_field(instruction.fields) {
    Some(selector) => {
      let count = string_list_count(instruction.form.sizes);
      let index = if count == 3 then selector - 1 else selector;
      size_code_bytes(string_at(instruction.form.sizes, index))
    },
    None() => match instruction.form.sizes {
      code :: _ => size_code_bytes(code),
      [||] => 8,
    },
  }

function condition_size_field(fields : list(Decoded_field)) -> option(int) = match fields {
  [||] => None(),
  field :: tail => if field.kind == FieldSize then Some(field.value) else condition_size_field(tail),
}

function ea_field_role(role : string, fields : list(Decoded_field)) -> option(int) = match fields {
  [||] => None(),
  field :: tail => if field.role == role then Some(field.value) else ea_field_role(role, tail),
}

function ea_segment_index(ea : Decoded_ea) -> int =
  if ea.segment == "CS" then 0
  else if ea.segment == "SS" then 2
  else if ea.segment == "explicit" then match ea_field_role("segment", ea.fields) {
    Some(index) => index + 1,
    None() => 1,
  }
  else 1

function ea_signed_payload(ea : Decoded_ea) -> bits(64) =
  if not_bool(ea.payload_signed) then ea.payload
  else if ea.payload_width == 8 then sail_sign_extend(ea.payload[7 .. 0], 64)
  else if ea.payload_width == 16 then sail_sign_extend(ea.payload[15 .. 0], 64)
  else if ea.payload_width == 32 then sail_sign_extend(ea.payload[31 .. 0], 64)
  else ea.payload

function staged_register(index : int, value : bits(64)) -> list(Staged_register_update) =
  [|struct { index = get_slice_int(4, index, 0), value = value }|]

function image_register(state : Cpu_state, index : int) -> bits(64) =
  state.registers[unsigned(get_slice_int(4, index, 0))]

function image_segment(state : Cpu_state, index : int) -> bits(64) = match index {
  0 => state.segments[0], 1 => state.segments[1], 2 => state.segments[2],
  3 => state.segments[3], 4 => state.segments[4], 5 => state.segments[5],
  6 => state.segments[6], 7 => state.segments[7], _ => state.segments[8],
}

struct Segment_point = {
  in_bounds : bool,
  linear : bits(64),
}

function segment_point(image : bits(64), address : bits(64)) -> Segment_point = {
  let mantissa = unsigned(image[6 .. 1]);
  if mantissa == 0 then struct { in_bounds = true, linear = address }
  else {
    let exponent = unsigned(image[11 .. 7]);
    let base = unsigned(image[63 .. 12]) * 4096;
    let span = mantissa * (2 ^ exponent) * 4096;
    let limit = base + span;
    let point = unsigned(address);
    if image[0] == bitone then struct {
      in_bounds = base <= point & point < limit,
      linear = address
    }
    else struct {
      in_bounds = point < span,
      linear = get_slice_int(64, base + point, 0)
    }
  }
}

function evaluate_decoded_ea(operand : Decoded_operand, ea : Decoded_ea,
                             image : Cpu_state, instruction_pc : bits(64), width : int)
  -> (Ea_evaluation, Cpu_state) = {
  var staged = image;
  var updates : list(Staged_register_update) = [||];
  let base_index = ea_field_role("base", ea.fields);
  let index_index = ea_field_role("index", ea.fields);
  var base_value : bits(64) = if ea.base == "SP" then image.sp
    else if ea.base == "PC" then instruction_pc
    else if ea.base == "zero" then 0x0000000000000000
    else match base_index {
      Some(index) => image_register(image, index),
      None() => 0x0000000000000000,
    };
  if ea.update_target == "b" & ea.update_mode == "predecrement" then match base_index {
    Some(index) => {
      let reg_index = unsigned(get_slice_int(4, index, 0));
      let changed = sub_bits(image.registers[reg_index], get_slice_int(64, width, 0));
      staged.registers[reg_index] = changed; base_value = changed;
      updates = staged_register(index, changed)
    },
    None() => (),
  } else ();
  var index_value : bits(64) = match index_index {
    Some(index) => image_register(image, index),
    None() => 0x0000000000000000,
  };
  if ea.update_target == "i" & ea.update_mode == "predecrement" then match index_index {
    Some(index) => {
      let reg_index = unsigned(get_slice_int(4, index, 0));
      let changed = sub_bits(image.registers[reg_index], 0x0000000000000001);
      staged.registers[reg_index] = changed; index_value = changed;
      updates = staged_register(index, changed)
    },
    None() => (),
  } else ();
  let scaled_index = sail_shiftleft(index_value, if width == 1 then 0 else if width == 2 then 1
                                                   else if width == 4 then 2 else 3);
  let offset = add_bits(add_bits(base_value, scaled_index), ea_signed_payload(ea));
  if ea.update_target == "b" & ea.update_mode == "postincrement" then match base_index {
    Some(index) => {
      let reg_index = unsigned(get_slice_int(4, index, 0));
      let changed = add_bits(image.registers[reg_index], get_slice_int(64, width, 0));
      staged.registers[reg_index] = changed; updates = staged_register(index, changed)
    },
    None() => (),
  } else if ea.update_target == "i" & ea.update_mode == "postincrement" then match index_index {
    Some(index) => {
      let reg_index = unsigned(get_slice_int(4, index, 0));
      let changed = add_bits(image.registers[reg_index], 0x0000000000000001);
      staged.registers[reg_index] = changed; updates = staged_register(index, changed)
    },
    None() => (),
  } else ();
  let direct_value = if ea.kind == "register" then match ea_field_role("value", ea.fields) {
    Some(index) => image_register(image, index), None() => image.sp
  } else if ea.kind == "immediate" then ea_signed_payload(ea) else offset;
  let point = if ea.kind == "register" | ea.kind == "immediate" then direct_value else offset;
  let segment = ea_segment_index(ea);
  let selected_segment = image_segment(image, segment);
  let translated = segment_point(selected_segment, point);
  let linear = translated.linear;
  (struct {
    operand_name = operand.name, kind = ea.kind, role = operand.ea_role,
    domain = operand.domain, segment = segment, segment_image = selected_segment, width = width,
    effective_address = point, linear_address = linear, value = direct_value,
    staged_updates = updates
  }, staged)
}

function evaluate_ea_operands_in_order(operands : list(Decoded_operand), image : Cpu_state,
                                       instruction_pc : bits(64), width : int)
  -> Ea_evaluation_set = match operands {
  [||] => struct { evaluations = [||], image = image },
  operand :: tail => match operand.ea {
    None() => evaluate_ea_operands_in_order(tail, image, instruction_pc, width),
    Some(ea) => {
      let (evaluation, next_image) = evaluate_decoded_ea(operand, ea, image, instruction_pc, width);
      let rest = evaluate_ea_operands_in_order(tail, next_image, instruction_pc, width);
      struct { evaluations = evaluation :: rest.evaluations, image = rest.image }
    },
  }
}

function extension_destination_width(operation : Semantic_operation) -> int =
  if operation == Op_EXTZW | operation == Op_EXTSW then 2
  else if operation == Op_EXTZL | operation == Op_EXTSL then 4
  else 8

function instruction_ea_width(operation : Semantic_operation, operand : Decoded_operand,
                              default_width : int) -> int =
  if operand.name == "dst"
     & (operation == Op_EXTZW | operation == Op_EXTSW | operation == Op_EXTZL
        | operation == Op_EXTSL | operation == Op_EXTZQ | operation == Op_EXTSQ)
  then extension_destination_width(operation)
  else if operand.ea_width == "B" then 1
  else if operand.ea_width == "W" then 2
  else if operand.ea_width == "L" then 4
  else if operand.ea_width == "Q" then 8
  else default_width

function evaluate_instruction_eas(operands : list(Decoded_operand), operation : Semantic_operation,
                                   image : Cpu_state, instruction_pc : bits(64),
                                   default_width : int) -> Ea_evaluation_set = match operands {
  [||] => struct { evaluations = [||], image = image },
  operand :: tail => match operand.ea {
    None() => evaluate_instruction_eas(tail, operation, image, instruction_pc, default_width),
    Some(ea) => {
      let width = instruction_ea_width(operation, operand, default_width);
      let (evaluation, next_image) = evaluate_decoded_ea(
        operand, ea, image, instruction_pc, width
      );
      let rest = evaluate_instruction_eas(
        tail, operation, next_image, instruction_pc, default_width
      );
      struct { evaluations = evaluation :: rest.evaluations, image = rest.image }
    },
  }
}

function merge_narrow(previous : bits(64), value : bits(64), width : int) -> bits(64) =
  if width == 1 then previous[63 .. 8] @ value[7 .. 0]
  else if width == 2 then previous[63 .. 16] @ value[15 .. 0]
  else if width == 4 then previous[63 .. 32] @ value[31 .. 0]
  else value

function width_mask(width : int) -> bits(64) =
  if width == 1 then 0x00000000000000FF
  else if width == 2 then 0x000000000000FFFF
  else if width == 4 then 0x00000000FFFFFFFF
  else 0xFFFFFFFFFFFFFFFF

function width_sign(value : bits(64), width : int) -> bool =
  if width == 1 then value[7] == bitone
  else if width == 2 then value[15] == bitone
  else if width == 4 then value[31] == bitone
  else value[63] == bitone

function flags_value(zero : bool, negative : bool, carry : bool, overflow : bool) -> bits(4) =
  (if zero then bitone else bitzero)
  @ (if negative then bitone else bitzero)
  @ (if carry then bitone else bitzero)
  @ (if overflow then bitone else bitzero)

function shift_result(operation : Semantic_operation, value : bits(64), raw_count : bits(64),
                      width : int) -> bits(64) = {
  let width_bits = width * 8;
  let count = tmod_int(unsigned(raw_count[5 .. 0]), width_bits);
  let masked = value & width_mask(width);
  if count == 0 then masked
  else if operation == Op_SHL then sail_shiftleft(masked, count) & width_mask(width)
  else if operation == Op_SHR then sail_shiftright(masked, count)
  else if operation == Op_SAR then {
    let signed_value : bits(64) = if width == 1 then sail_sign_extend(masked[7 .. 0], 64)
      else if width == 2 then sail_sign_extend(masked[15 .. 0], 64)
      else if width == 4 then sail_sign_extend(masked[31 .. 0], 64)
      else masked;
    sail_arith_shiftright(signed_value, count) & width_mask(width)
  }
  else if operation == Op_ROL then
    (sail_shiftleft(masked, count) | sail_shiftright(masked, width_bits - count)) & width_mask(width)
  else
    (sail_shiftright(masked, count) | sail_shiftleft(masked, width_bits - count)) & width_mask(width)
}

val route_environment : (Decoded_instruction, Cpu_state, Effect_kind, Commit_kind, bool) -> Execution_result
val start_memory_transaction : (Decoded_instruction, Cpu_state) -> option(Execution_result)

