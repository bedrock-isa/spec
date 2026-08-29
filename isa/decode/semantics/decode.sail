function decode_operand_list(operands : list(Catalog_operand), payloads : list(Catalog_payload),
                             fields : list(Decoded_field), bindings : list(Ea_binding),
                             bytes : list(bits(8)), cursor : int) -> option(Operand_parse) =
  match operands {
    [||] => Some(struct { operands = [||], cursor = cursor }),
    operand :: tail => {
      let ea = find_ea_binding(operand.name, bindings);
      let field : option(Decoded_field) = match operand.field_symbol {
        Some(symbol) => find_decoded_field(symbol, fields),
        None() => None(),
      };
      let appended = find_payload(operand.name, payloads);
      let width : int = match ea {
        Some(item) => item.payload_width,
        None() => match appended { Some(item) => item.width, None() => 0 },
      };
      let value_result : option(bits(64)) = match (field, appended) {
        (Some(item), _) => Some(get_slice_int(64, item.value, 0)),
        (_, Some(_)) => read_le_bits(bytes, cursor, width),
        _ => if operand.has_fixed_value
             then Some(get_slice_int(64, operand.fixed_value, 0))
             else Some(0x0000000000000000),
      };
      let ea_payload_result : option(bits(64)) = match ea {
        Some(_) => read_le_bits(bytes, cursor, width),
        None() => Some(0x0000000000000000),
      };
      match (value_result, ea_payload_result) {
        (Some(value), Some(ea_payload)) => match decode_operand_list(
          tail, payloads, fields, bindings, bytes, cursor + tdiv_int(width, 8)
        ) {
          None() => None(),
          Some(parsed) => Some(struct {
            operands = struct {
              name = operand.name,
              operand_type = operand.operand_type,
              access = operand.access,
              domain = operand.domain,
              ea_role = operand.ea_role,
              ea_width = operand.ea_width,
              value = value,
              ea = match ea {
                Some(item) => Some({ item with payload = ea_payload }),
                None() => None(),
              }
            } :: parsed.operands,
            cursor = parsed.cursor
          }),
        },
        _ => None(),
      }
    },
  }

function operand_payload_failure_stage(operands : list(Catalog_operand), payloads : list(Catalog_payload),
                                       bindings : list(Ea_binding), bytes : list(bits(8)), cursor : int)
  -> Decode_stage = match operands {
  [||] => DecodeSuccess,
  operand :: tail => {
    let ea = find_ea_binding(operand.name, bindings);
    let appended = find_payload(operand.name, payloads);
    let width : int = match ea {
      Some(item) => item.payload_width,
      None() => match appended { Some(item) => item.width, None() => 0 },
    };
    let next_cursor = cursor + tdiv_int(width, 8);
    if byte_count(bytes) < next_cursor then match ea {
      Some(_) => DecodeEaPayload,
      None() => DecodeStandalonePayload,
    }
    else operand_payload_failure_stage(tail, payloads, bindings, bytes, next_cursor)
  },
}

function int_member(value : int, values : list(int)) -> bool = match values {
  [||] => false,
  item :: tail => value == item | int_member(value, tail),
}

function legal_value_or_unrestricted(value : int, values : list(int)) -> bool = match values {
  [||] => true,
  _ => int_member(value, values),
}

function operands_statically_legal(catalog : list(Catalog_operand),
                                   decoded : list(Decoded_operand)) -> bool =
  match (catalog, decoded) {
    ([||], [||]) => true,
    (expected :: expected_tail, actual :: actual_tail) => {
      let fixed_ok = not_bool(expected.has_fixed_value) | unsigned(actual.value) == expected.fixed_value;
      let enum_ok = legal_value_or_unrestricted(unsigned(actual.value), expected.legal_values);
      fixed_ok & enum_ok
      & operands_statically_legal(expected_tail, actual_tail)
    },
    _ => false,
  }

function decode_success(form : Catalog_entry, allocation : bits(64), fields : list(Decoded_field),
                        operands : Operand_parse, frame : Framed_record,
                        bytes : list(bits(8))) -> Decode_outcome = {
  let instruction : Decoded_instruction = struct {
    form = form, opcode_allocation = allocation, fields = fields, operands = operands.operands,
    encoded_length = frame.encoded_length, required_length = operands.cursor, bytes = bytes
  };
  if not_bool(operands_statically_legal(form.operands, operands.operands)) then
    struct { stage = DecodeStaticLegality, candidate_form = Some(form), instruction = None(), detail = "fixed or enum operand" }
  else if not_bool(required_bytes_sufficient(frame, operands.cursor)) then
    struct { stage = DecodeRecordLength, candidate_form = Some(form), instruction = None(), detail = "record length" }
  else struct { stage = DecodeSuccess, candidate_form = None(), instruction = Some(instruction), detail = "" }
}

function decode_full_record_execution_outcome(bytes : list(bits(8))) -> Decode_outcome =
  if byte_count(bytes) == 0 then
    struct { stage = DecodeFetch, candidate_form = None(), instruction = None(), detail = "instruction byte 0 unavailable" }
  else match frame_record(bytes) {
    None() => struct { stage = DecodeFraming, candidate_form = None(), instruction = None(), detail = "record framing" },
    Some(frame) => {
      let encoding_class = encoding_class_of_record(frame.record_class);
      match opcode_allocation(bytes, encoding_class) {
        None() => struct { stage = DecodeFetch, candidate_form = None(), instruction = None(), detail = "opcode-space bytes unavailable" },
        Some(allocation) => match find_catalog_entry(allocation, encoding_class, primary_form_catalog_for(encoding_class)) {
          None() => match find_opcode_entry(allocation, encoding_class, primary_form_catalog_for(encoding_class)) {
            None() => struct { stage = DecodeOpcode, candidate_form = None(), instruction = None(), detail = "unallocated opcode" },
            Some(opcode_form) => struct {
              stage = DecodeConstraint, candidate_form = Some(opcode_form),
              instruction = None(), detail = "catalog constraint"
            },
          },
          Some(form) => {
            let fields = decode_fields(allocation, form.fields);
            let opcode_space_bytes = class_minimum(frame.record_class);
            match parse_ea_descriptors(form.operands, fields, bytes, opcode_space_bytes) {
              None() => {
                struct {
                  stage = ea_failure_stage(form.operands, fields, bytes, opcode_space_bytes),
                  candidate_form = Some(form), instruction = None(), detail = "effective-address encoding"
                }
              },
              Some(eas) => match decode_operand_list(
                form.operands, form.appended_payloads, fields, eas.bindings, bytes, eas.cursor
              ) {
                None() => struct {
                  stage = operand_payload_failure_stage(
                    form.operands, form.appended_payloads, eas.bindings, bytes, eas.cursor
                  ), instruction = None(),
                  candidate_form = Some(form),
                  detail = "operand payload"
                },
                Some(operands) => decode_success(form, allocation, fields, operands, frame, bytes),
              },
            }
          },
        },
      }
    },
  }

function decode_full_record_outcome(bytes : list(bits(8))) -> Decode_outcome = {
  let decoded = decode_full_record_execution_outcome(bytes);
  match decoded.instruction {
    Some(instruction) => { decoded with candidate_form = Some(instruction.form) },
    None() => decoded,
  }
}

function decode_full_record(bytes : list(bits(8))) -> option(Decoded_instruction) =
  match decode_full_record_outcome(bytes).instruction {
    Some(instruction) => Some(instruction),
    None() => None(),
  }
