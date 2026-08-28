function ea_field_role(role : Ea_role, fields : list(Decoded_field)) -> option(int) = match fields {
  [||] => None(),
  field :: tail => if field.role == Some(role) then Some(field.value) else ea_field_role(role, tail),
}

function ea_segment_index(ea : Decoded_ea) -> int = match ea.segment {
  Some(EaSegment_CS) => 0,
  Some(EaSegment_SS) => 2,
  Some(EaSegment_explicit) => match ea_field_role(EaRole_segment, ea.fields) {
    Some(index) => index + 1,
    None() => 1,
  },
  _ => 1,
}

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

function ea_width_shift(width : int) -> int =
  if width <= 1 then 0 else 1 + ea_width_shift(tdiv_int(width, 2))

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
  let base_index = ea_field_role(EaRole_base, ea.fields);
  let index_index = ea_field_role(EaRole_index, ea.fields);
  var base_value : bits(64) = if ea.base == Some(EaBase_SP) then image.sp
    else if ea.base == Some(EaBase_PC) then instruction_pc
    else if ea.base == Some(EaBase_zero) then 0x0000000000000000
    else match base_index {
      Some(index) => image_register(image, index),
      None() => 0x0000000000000000,
    };
  if ea.update_target == Some(EaUpdateTarget_b) & ea.update_mode == Some(EaUpdateMode_predecrement) then match base_index {
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
  if ea.update_target == Some(EaUpdateTarget_i) & ea.update_mode == Some(EaUpdateMode_predecrement) then match index_index {
    Some(index) => {
      let reg_index = unsigned(get_slice_int(4, index, 0));
      let changed = sub_bits(image.registers[reg_index], 0x0000000000000001);
      staged.registers[reg_index] = changed; index_value = changed;
      updates = staged_register(index, changed)
    },
    None() => (),
  } else ();
  let scaled_index = sail_shiftleft(index_value, ea_width_shift(width));
  let offset = add_bits(add_bits(base_value, scaled_index), ea_signed_payload(ea));
  if ea.update_target == Some(EaUpdateTarget_b) & ea.update_mode == Some(EaUpdateMode_postincrement) then match base_index {
    Some(index) => {
      let reg_index = unsigned(get_slice_int(4, index, 0));
      let changed = add_bits(image.registers[reg_index], get_slice_int(64, width, 0));
      staged.registers[reg_index] = changed; updates = staged_register(index, changed)
    },
    None() => (),
  } else if ea.update_target == Some(EaUpdateTarget_i) & ea.update_mode == Some(EaUpdateMode_postincrement) then match index_index {
    Some(index) => {
      let reg_index = unsigned(get_slice_int(4, index, 0));
      let changed = add_bits(image.registers[reg_index], 0x0000000000000001);
      staged.registers[reg_index] = changed; updates = staged_register(index, changed)
    },
    None() => (),
  } else ();
  let direct_value = if ea.kind == EaKind_immediate then ea_signed_payload(ea)
    else if ea.kind == EaKind_float_immediate then ea.payload else offset;
  let point = if ea.kind == EaKind_immediate | ea.kind == EaKind_float_immediate
              then direct_value else offset;
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

function evaluate_decoded_vector_ea(operand : Decoded_operand, ea : Decoded_ea,
                                    image : Cpu_state, instruction_pc : bits(64),
                                    width : int) -> (Ea_evaluation, Cpu_state) = {
  var staged = image;
  var updates : list(Staged_register_update) = [||];
  let base_index = ea_field_role(EaRole_base, ea.fields);
  let index_index = ea_field_role(EaRole_index, ea.fields);
  var base_value : bits(64) = if ea.base == Some(EaBase_SP) then image.sp
    else if ea.base == Some(EaBase_PC) then instruction_pc
    else if ea.base == Some(EaBase_zero) then 0x0000000000000000
    else match base_index {
      Some(index) => image_register(image, index), None() => 0x0000000000000000,
    };
  let base_amount = get_slice_int(64, image.vector_length_bytes, 0);
  let index_amount = get_slice_int(64, tdiv_int(image.vector_length_bytes, width), 0);
  if ea.update_target == Some(EaUpdateTarget_b) & ea.update_mode == Some(EaUpdateMode_predecrement) then match base_index {
    Some(index) => {
      let reg_index = unsigned(get_slice_int(4, index, 0));
      let changed = sub_bits(image.registers[reg_index], base_amount);
      staged.registers[reg_index] = changed; base_value = changed;
      updates = staged_register(index, changed)
    },
    None() => (),
  } else ();
  var index_value : bits(64) = match index_index {
    Some(index) => image_register(image, index), None() => 0x0000000000000000,
  };
  if ea.update_target == Some(EaUpdateTarget_i) & ea.update_mode == Some(EaUpdateMode_predecrement) then match index_index {
    Some(index) => {
      let reg_index = unsigned(get_slice_int(4, index, 0));
      let changed = sub_bits(image.registers[reg_index], index_amount);
      staged.registers[reg_index] = changed; index_value = changed;
      updates = staged_register(index, changed)
    },
    None() => (),
  } else ();
  let scaled_index = sail_shiftleft(index_value, ea_width_shift(width));
  let offset = add_bits(add_bits(base_value, scaled_index), ea_signed_payload(ea));
  if ea.update_target == Some(EaUpdateTarget_b) & ea.update_mode == Some(EaUpdateMode_postincrement) then match base_index {
    Some(index) => {
      let reg_index = unsigned(get_slice_int(4, index, 0));
      let changed = add_bits(image.registers[reg_index], base_amount);
      staged.registers[reg_index] = changed; updates = staged_register(index, changed)
    },
    None() => (),
  } else if ea.update_target == Some(EaUpdateTarget_i) & ea.update_mode == Some(EaUpdateMode_postincrement) then match index_index {
    Some(index) => {
      let reg_index = unsigned(get_slice_int(4, index, 0));
      let changed = add_bits(image.registers[reg_index], index_amount);
      staged.registers[reg_index] = changed; updates = staged_register(index, changed)
    },
    None() => (),
  } else ();
  let segment = ea_segment_index(ea);
  let selected_segment = image_segment(image, segment);
  let translated = segment_point(selected_segment, offset);
  (struct {
    operand_name = operand.name, kind = EaKind_memory, role = operand.ea_role,
    domain = operand.domain, segment = segment, segment_image = selected_segment, width = width,
    effective_address = offset, linear_address = translated.linear, value = offset,
    staged_updates = updates
  }, staged)
}

function evaluate_vector_instruction_ea(operands : list(Decoded_operand), image : Cpu_state,
                                        instruction_pc : bits(64), width : int)
  -> option((Ea_evaluation, Cpu_state)) = match operands {
  [||] => None(),
  operand :: tail => match operand.ea {
    Some(ea) => Some(evaluate_decoded_vector_ea(operand, ea, image, instruction_pc, width)),
    None() => evaluate_vector_instruction_ea(tail, image, instruction_pc, width),
  }
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

function instruction_ea_width(operand : Decoded_operand, default_width : int) -> int =
  if operand.ea_width == Some(EaWidth_B) then 1
  else if operand.ea_width == Some(EaWidth_W) then 2
  else if operand.ea_width == Some(EaWidth_L) then 4
  else if operand.ea_width == Some(EaWidth_Q) then 8
  else default_width

function evaluate_instruction_eas(operands : list(Decoded_operand),
                                   image : Cpu_state, instruction_pc : bits(64),
                                   default_width : int) -> Ea_evaluation_set = match operands {
  [||] => struct { evaluations = [||], image = image },
  operand :: tail => match operand.ea {
    None() => evaluate_instruction_eas(tail, image, instruction_pc, default_width),
    Some(ea) => {
      let width = instruction_ea_width(operand, default_width);
      let (evaluation, next_image) = evaluate_decoded_ea(
        operand, ea, image, instruction_pc, width
      );
      let rest = evaluate_instruction_eas(
        tail, next_image, instruction_pc, default_width
      );
      struct { evaluations = evaluation :: rest.evaluations, image = rest.image }
    },
  }
}
