function ea_patterns_match(patterns : list(Ea_pattern), bytes : list(bits(8)), cursor : int) -> bool =
  match patterns {
    [||] => true,
    pattern :: tail => match byte_at(bytes, cursor) {
      Some(byte) =>
        ((sail_zero_extend(byte, 16) & pattern.mask) == pattern.value)
        & ea_patterns_match(tail, bytes, cursor + 1),
      None() => false,
    },
  }

function ea_pattern_count(patterns : list(Ea_pattern)) -> int = match patterns {
  [||] => 0,
  _ :: tail => 1 + ea_pattern_count(tail),
}

function compact_ea_matches(form : Ea_form, raw : bits(16)) -> bool = match form.patterns {
  [|pattern|] => (form.descriptor_family == "") & ((raw & pattern.mask) == pattern.value),
  _ => false,
}

function find_compact_ea(raw : bits(16), forms : list(Ea_form)) -> option(Ea_form) = match forms {
  [||] => None(),
  form :: tail => if compact_ea_matches(form, raw) then Some(form) else find_compact_ea(raw, tail),
}

function find_extended_ea(family : string, bytes : list(bits(8)), cursor : int,
                          forms : list(Ea_form)) -> option(Ea_form) =
  match forms {
    [||] => None(),
    form :: tail =>
      if (form.descriptor_family == family) & ea_patterns_match(form.patterns, bytes, cursor)
      then Some(form)
      else find_extended_ea(family, bytes, cursor, tail),
  }

val extracted_ea_field : (bits(64), list(range(0, 15)), int) -> int
val decode_ea_field_list : (bits(64), list(Ea_field)) -> list(Decoded_field)

function append_decoded_fields(left : list(Decoded_field), right : list(Decoded_field))
  -> list(Decoded_field) = match left {
  [||] => right,
  field :: tail => field :: append_decoded_fields(tail, right),
}

function decode_ea_fields(bytes : list(bits(8)), cursor : int, form : Ea_form) -> list(Decoded_field) =
  match read_be_bits(bytes, cursor, ea_pattern_count(form.patterns) * 8) {
    Some(raw) => decode_ea_field_list(raw, form.fields),
    None() => [||],
  }

function decode_ea_field_list(raw : bits(64), fields : list(Ea_field)) -> list(Decoded_field) =
  match fields {
    [||] => [||],
    field :: tail => struct {
      symbol = field.symbol,
      type_name = field.type_name,
      kind = FieldBits,
      role = field.role,
      value = extracted_ea_field(raw, field.positions, 0)
    } :: decode_ea_field_list(raw, tail),
  }

function extracted_ea_field(payload : bits(64), positions : list(range(0, 15)), accumulated : int) -> int =
  match positions {
    [||] => accumulated,
    position :: tail => extracted_ea_field(
      payload, tail, accumulated * 2 + (if payload[position] == bitone then 1 else 0)
    ),
  }

function parse_one_ea(operand_name : string, operand_width : string, raw_value : int,
                      bytes : list(bits(8)), cursor : int)
  -> option((Ea_binding, int)) =
  match find_compact_ea(get_slice_int(16, raw_value, 0), effective_address_catalog()) {
    None() => None(),
    Some(compact) => {
      let descriptor_cursor = cursor;
      let descriptor_bytes = compact.descriptor_bytes;
      let descriptor = if descriptor_bytes > 0
        then find_extended_ea(compact.descriptor, bytes, descriptor_cursor,
                              effective_address_catalog())
        else None();
      let descriptor_valid = if descriptor_bytes == 0 then true else match descriptor {
        Some(_) => true,
        None() => false,
      };
      if descriptor_bytes < 0 | not_bool(descriptor_valid) then None()
      else {
        let payload_cursor = cursor + descriptor_bytes;
        match read_le_bits(bytes, payload_cursor, compact.payload_width) {
          None() => None(),
          Some(payload) => {
            let descriptor_name : string = match descriptor { Some(form) => form.name, None() => "" };
            let descriptor_fields : list(Decoded_field) = match descriptor {
              Some(form) => decode_ea_fields(bytes, descriptor_cursor, form),
              None() => [||],
            };
            let update_target : string = match descriptor { Some(form) => form.update_target, None() => "" };
            let update_mode : string = match descriptor { Some(form) => form.update_mode, None() => "" };
            let resolved_kind : string = match descriptor { Some(form) => form.kind, None() => compact.kind };
            let resolved_segment : string = match descriptor { Some(form) => form.segment, None() => compact.segment };
            let resolved_base : string = match descriptor { Some(form) => form.base, None() => compact.base };
            let resolved_register : string = match descriptor {
              Some(form) => form.register_name, None() => compact.register_name
            };
            let compact_fields = decode_ea_field_list(
              sail_zero_extend(get_slice_int(16, raw_value, 0), 64), compact.fields
            );
            Some((struct {
              operand_name = operand_name,
              ea = struct {
                compact_name = compact.name,
                kind = resolved_kind,
                segment = resolved_segment,
                base = resolved_base,
                register_name = resolved_register,
                operand_width = operand_width,
                descriptor_name = descriptor_name,
                raw = raw_value,
                descriptor_bytes = descriptor_bytes,
                fields = append_decoded_fields(compact_fields, descriptor_fields),
                payload = payload,
                payload_width = compact.payload_width,
                payload_signed = compact.payload_signed,
                update_target = update_target,
                update_mode = update_mode
              }
            }, payload_cursor + tdiv_int(compact.payload_width, 8)))
          },
        }
      }
    },
  }

function parse_ea_operands(operands : list(Catalog_operand), fields : list(Decoded_field),
                           bytes : list(bits(8)), cursor : int) -> option(Ea_parse) =
  match operands {
    [||] => Some(struct { bindings = [||], cursor = cursor }),
    operand :: tail =>
      if operand.type_name == "EA" then match find_decoded_field(operand.field_symbol, fields) {
        None() => None(),
        Some(field) => match parse_one_ea(operand.name, operand.ea_width, field.value, bytes, cursor) {
          None() => None(),
          Some((binding, next_cursor)) => match parse_ea_operands(tail, fields, bytes, next_cursor) {
            None() => None(),
            Some(parsed) => Some(struct { bindings = binding :: parsed.bindings, cursor = parsed.cursor }),
          },
        },
      }
      else parse_ea_operands(tail, fields, bytes, cursor),
  }

function ea_failure_stage(operands : list(Catalog_operand), fields : list(Decoded_field),
                          bytes : list(bits(8)), cursor : int) -> Decode_stage = match operands {
  [||] => DecodeSuccess,
  operand :: tail =>
    if operand.type_name != "EA" then ea_failure_stage(tail, fields, bytes, cursor)
    else match find_decoded_field(operand.field_symbol, fields) {
      None() => DecodeStaticLegality,
      Some(field) => match find_compact_ea(
        get_slice_int(16, field.value, 0), effective_address_catalog()
      ) {
        None() => DecodeEaDescriptor,
        Some(compact) => {
          let descriptor_bytes = compact.descriptor_bytes;
          if descriptor_bytes < 0 | byte_count(bytes) < cursor + descriptor_bytes then DecodeEaDescriptor
          else {
            let descriptor = if descriptor_bytes > 0
              then find_extended_ea(compact.descriptor, bytes, cursor, effective_address_catalog())
              else None();
            let descriptor_valid = if descriptor_bytes == 0 then true else match descriptor {
              Some(_) => true,
              None() => false,
            };
            if not_bool(descriptor_valid) then DecodeEaDescriptor
            else {
              let payload_end = cursor + descriptor_bytes + tdiv_int(compact.payload_width, 8);
              if byte_count(bytes) < payload_end then DecodeEaPayload
              else ea_failure_stage(tail, fields, bytes, payload_end)
            }
          }
        },
      },
    }
}

function find_ea_binding(name : string, bindings : list(Ea_binding)) -> option(Decoded_ea) = match bindings {
  [||] => None(),
  binding :: tail => if binding.operand_name == name then Some(binding.ea) else find_ea_binding(name, tail),
}

function find_payload(name : string, payloads : list(Catalog_payload)) -> option(Catalog_payload) =
  match payloads {
    [||] => None(),
    payload :: tail => if payload.operand_name == name then Some(payload) else find_payload(name, tail),
  }

