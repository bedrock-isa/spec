enum Integer_size = SizeL | SizeQ
enum Selected_operation = Clear | Move | And | Or | Xor

struct Selected_instruction = {
  operation : Selected_operation,
  size : Integer_size,
  source : bits(4),
  destination : bits(4),
}

function decode_selected(bytes : list(bits(8))) -> option(Selected_instruction) = match bytes {
  [|byte0|] =>
    if byte0[7 .. 4] == 0x6 then
      Some(struct {
        operation = Clear,
        size = SizeQ,
        source = byte0[3 .. 0],
        destination = byte0[3 .. 0]
      })
    else None(),
  [|byte0, byte1|] => {
    let operation : option(Selected_operation) = match (byte0 & 0xFE) {
      0x80 => Some(Move),
      0x88 => Some(And),
      0x8A => Some(Or),
      0x8C => Some(Xor),
      _ => None(),
    };
    match operation {
      Some(selected) => Some(struct {
        operation = selected,
        size = if byte0[0] == bitzero then SizeL else SizeQ,
        source = byte1[7 .. 4],
        destination = byte1[3 .. 0]
      }),
      None() => None(),
    }
  },
  _ => None(),
}

type Registers = vector(16, inc, bits(64))

function binary_result(operation : Selected_operation, source : bits(64), destination : bits(64)) -> bits(64) =
  match operation {
    Move => source,
    And => source & destination,
    Or => source | destination,
    Xor => xor_vec(source, destination),
    Clear => 0x0000000000000000,
  }

function execute_selected(instruction : Selected_instruction, registers : Registers) -> Registers = {
  let source = registers[unsigned(instruction.source)];
  let destination = registers[unsigned(instruction.destination)];
  let result = binary_result(instruction.operation, source, destination);
  var updated = registers;
  updated[unsigned(instruction.destination)] = match instruction.size {
    SizeL => destination[63 .. 32] @ result[31 .. 0],
    SizeQ => result,
  };
  updated
}

function decode_and_execute(bytes : list(bits(8)), registers : Registers) -> option(Registers) =
  match decode_selected(bytes) {
    Some(instruction) => Some(execute_selected(instruction, registers)),
    None() => None(),
  }
struct Decoded_field = {
  symbol : string,
  type_name : string,
  kind : Metadata_field_kind,
  role : string,
  value : int,
}

struct Decoded_ea = {
  compact_name : string,
  kind : string,
  segment : string,
  base : string,
  register_name : string,
  operand_width : string,
  ext0_name : string,
  raw : int,
  descriptor_bytes : int,
  fields : list(Decoded_field),
  payload : bits(64),
  payload_width : int,
  payload_signed : bool,
  update_target : string,
  update_mode : string,
}

struct Decoded_operand = {
  name : string,
  type_name : string,
  access : Metadata_access,
  domain : string,
  ea_role : string,
  ea_width : string,
  fixed_identity : string,
  value : bits(64),
  ea : option(Decoded_ea),
}

struct Ea_binding = {
  operand_name : string,
  ea : Decoded_ea,
}

struct Ea_parse = {
  bindings : list(Ea_binding),
  cursor : int,
}

struct Operand_parse = {
  operands : list(Decoded_operand),
  cursor : int,
}

struct Decoded_instruction = {
  form : Catalog_entry,
  payload : bits(64),
  fields : list(Decoded_field),
  operands : list(Decoded_operand),
  encoded_length : int,
  required_length : int,
  bytes : list(bits(8)),
}

struct Decode_outcome = {
  stage : Decode_stage,
  candidate_form : option(Catalog_entry),
  instruction : option(Decoded_instruction),
  detail : string,
}

function byte_at(bytes : list(bits(8)), index : int) -> option(bits(8)) = match bytes {
  [||] => None(),
  byte :: tail => if index == 0 then Some(byte) else if index > 0 then byte_at(tail, index - 1) else None(),
}

function read_le_int(bytes : list(bits(8)), cursor : int, remaining : int,
                     factor : int, accumulated : int) -> option(int) =
  if remaining == 0 then Some(accumulated)
  else match byte_at(bytes, cursor) {
    Some(byte) => read_le_int(bytes, cursor + 1, remaining - 1,
                             factor * 256, accumulated + unsigned(byte) * factor),
    None() => None(),
  }

function read_le_bits(bytes : list(bits(8)), cursor : int, width : int) -> option(bits(64)) =
  if (width == 0) | (width == 8) | (width == 16) | (width == 24)
     | (width == 32) | (width == 40) | (width == 48) | (width == 56) | (width == 64) then
    match read_le_int(bytes, cursor, tdiv_int(width, 8), 1, 0) {
      Some(value) => Some(get_slice_int(64, value, 0)),
      None() => None(),
    }
  else None()

function read_be_int(bytes : list(bits(8)), cursor : int, remaining : int,
                     accumulated : int) -> option(int) =
  if remaining == 0 then Some(accumulated)
  else match byte_at(bytes, cursor) {
    Some(byte) => read_be_int(bytes, cursor + 1, remaining - 1,
                             accumulated * 256 + unsigned(byte)),
    None() => None(),
  }

function read_be_bits(bytes : list(bits(8)), cursor : int, width : int) -> option(bits(64)) =
  match read_be_int(bytes, cursor, tdiv_int(width, 8), 0) {
    Some(value) => Some(get_slice_int(64, value, 0)),
    None() => None(),
  }

function opcode_payload(bytes : list(bits(8)), encoding_class : Encoding_class) -> option(bits(64)) =
  match (encoding_class, bytes) {
    (ExtraShort, byte0 :: _) => Some(sail_zero_extend(byte0[6 .. 0], 64)),
    (Short, byte0 :: byte1 :: _) => Some(sail_zero_extend(byte0[5 .. 0] @ byte1, 64)),
    (Medium, byte0 :: byte1 :: byte2 :: _) =>
      Some(sail_zero_extend(byte0[1 .. 0] @ byte1 @ byte2, 64)),
    (Long, byte0 :: byte1 :: byte2 :: byte3 :: _) =>
      Some(sail_zero_extend(byte0[1 .. 0] @ byte1 @ byte2 @ byte3, 64)),
    (ExtraLong, byte0 :: byte1 :: byte2 :: byte3 :: byte4 :: _) =>
      Some(sail_zero_extend(byte0[1 .. 0] @ byte1 @ byte2 @ byte3 @ byte4, 64)),
    _ => None(),
  }

function encoding_class_of_record(record_class : Record_class) -> Encoding_class = match record_class {
  FixedExtraShort => ExtraShort,
  FixedShort => Short,
  ExtendedMedium => Medium,
  ExtendedLong => Long,
  ExtendedExtraLong => ExtraLong,
}

function find_catalog_entry(payload : bits(64), encoding_class : Encoding_class,
                            entries : list(Catalog_entry)) -> option(Catalog_entry) =
  match entries {
    [||] => None(),
    entry :: tail =>
      if entry.encoding_class == encoding_class & catalog_entry_matches(payload, entry)
      then Some(entry)
      else find_catalog_entry(payload, encoding_class, tail),
  }

function find_opcode_entry(payload : bits(64), encoding_class : Encoding_class,
                           entries : list(Catalog_entry)) -> option(Catalog_entry) =
  match entries {
    [||] => None(),
    entry :: tail =>
      if entry.encoding_class == encoding_class & ((payload & entry.mask) == entry.value)
      then Some(entry)
      else find_opcode_entry(payload, encoding_class, tail),
  }

function decode_fields(payload : bits(64), fields : list(Catalog_field)) -> list(Decoded_field) =
  match fields {
    [||] => [||],
    field :: tail => struct {
      symbol = field.symbol,
      type_name = field.type_name,
      kind = field.kind,
      role = "",
      value = extracted_field(payload, field.positions, 0)
    } :: decode_fields(payload, tail),
  }

function find_decoded_field(symbol : string, fields : list(Decoded_field)) -> option(Decoded_field) =
  match fields {
    [||] => None(),
    field :: tail => if field.symbol == symbol then Some(field) else find_decoded_field(symbol, tail),
  }

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
  [|pattern|] => not_bool(form.ext0) & ((raw & pattern.mask) == pattern.value),
  _ => false,
}

function find_compact_ea(raw : bits(16), forms : list(Ea_form)) -> option(Ea_form) = match forms {
  [||] => None(),
  form :: tail => if compact_ea_matches(form, raw) then Some(form) else find_compact_ea(raw, tail),
}

function find_ext0_ea(bytes : list(bits(8)), cursor : int, forms : list(Ea_form)) -> option(Ea_form) =
  match forms {
    [||] => None(),
    form :: tail =>
      if form.ext0 & ea_patterns_match(form.patterns, bytes, cursor)
      then Some(form)
      else find_ext0_ea(bytes, cursor, tail),
  }

function selected_descriptor_bytes(selected : option(Ea_form), required : bool) -> int =
  match selected {
    Some(form) => ea_pattern_count(form.patterns),
    None() => if required then -1 else 0,
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
      let ext0 = if compact.descriptor == "ext0"
        then find_ext0_ea(bytes, descriptor_cursor, effective_address_catalog())
        else None();
      let descriptor_bytes : int = match ext0 {
        Some(form) => ea_pattern_count(form.patterns),
        None() => if compact.descriptor == "ext0" then -1 else 0,
      };
      if descriptor_bytes < 0 then None()
      else {
        let payload_cursor = cursor + descriptor_bytes;
        match read_le_bits(bytes, payload_cursor, compact.payload_width) {
          None() => None(),
          Some(payload) => {
            let ext0_name : string = match ext0 { Some(form) => form.name, None() => "" };
            let ext0_fields : list(Decoded_field) = match ext0 {
              Some(form) => decode_ea_fields(bytes, descriptor_cursor, form),
              None() => [||],
            };
            let update_target : string = match ext0 { Some(form) => form.update_target, None() => "" };
            let update_mode : string = match ext0 { Some(form) => form.update_mode, None() => "" };
            let resolved_kind : string = match ext0 { Some(form) => form.kind, None() => compact.kind };
            let resolved_segment : string = match ext0 { Some(form) => form.segment, None() => compact.segment };
            let resolved_base : string = match ext0 { Some(form) => form.base, None() => compact.base };
            let resolved_register : string = match ext0 {
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
                ext0_name = ext0_name,
                raw = raw_value,
                descriptor_bytes = descriptor_bytes,
                fields = append_decoded_fields(compact_fields, ext0_fields),
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
          let ext0 = if compact.descriptor == "ext0"
            then find_ext0_ea(bytes, cursor, effective_address_catalog()) else None();
          let descriptor_bytes = selected_descriptor_bytes(ext0, compact.descriptor == "ext0");
          if descriptor_bytes < 0 | byte_count(bytes) < cursor + descriptor_bytes then DecodeEaDescriptor
          else {
            let payload_end = cursor + descriptor_bytes + tdiv_int(compact.payload_width, 8);
            if byte_count(bytes) < payload_end then DecodeEaPayload
            else ea_failure_stage(tail, fields, bytes, payload_end)
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

function decode_operand_list(operands : list(Catalog_operand), payloads : list(Catalog_payload),
                             fields : list(Decoded_field), bindings : list(Ea_binding),
                             bytes : list(bits(8)), cursor : int) -> option(Operand_parse) =
  match operands {
    [||] => Some(struct { operands = [||], cursor = cursor }),
    operand :: tail => {
      let ea = find_ea_binding(operand.name, bindings);
      let field = if operand.field_symbol == "" then None()
                  else find_decoded_field(operand.field_symbol, fields);
      let appended = find_payload(operand.name, payloads);
      let width : int = match appended { Some(item) => item.width, None() => 0 };
      let value_result : option(bits(64)) = match (field, appended) {
        (Some(item), _) => Some(get_slice_int(64, item.value, 0)),
        (_, Some(_)) => read_le_bits(bytes, cursor, width),
        _ => if operand.has_fixed_value
             then Some(get_slice_int(64, operand.fixed_value, 0))
             else Some(0x0000000000000000),
      };
      match value_result {
        None() => None(),
        Some(value) => match decode_operand_list(
          tail, payloads, fields, bindings, bytes, cursor + tdiv_int(width, 8)
        ) {
          None() => None(),
          Some(parsed) => Some(struct {
            operands = struct {
              name = operand.name,
              type_name = operand.type_name,
              access = operand.access,
              domain = operand.domain,
              ea_role = operand.ea_role,
              ea_width = operand.ea_width,
              fixed_identity = operand.fixed_identity,
              value = value,
              ea = ea
            } :: parsed.operands,
            cursor = parsed.cursor
          }),
        },
      }
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
      let identity_ok = expected.fixed_identity == actual.fixed_identity;
      fixed_ok & enum_ok & identity_ok
      & operands_statically_legal(expected_tail, actual_tail)
    },
    _ => false,
  }

function decode_success(form : Catalog_entry, payload : bits(64), fields : list(Decoded_field),
                        operands : Operand_parse, frame : Framed_record,
                        bytes : list(bits(8))) -> Decode_outcome = {
  let instruction : Decoded_instruction = struct {
    form = form, payload = payload, fields = fields, operands = operands.operands,
    encoded_length = frame.encoded_length, required_length = operands.cursor, bytes = bytes
  };
  if not_bool(operands_statically_legal(form.operands, operands.operands)) then
    struct { stage = DecodeStaticLegality, candidate_form = Some(form), instruction = None(), detail = "fixed or enum operand" }
  else if not_bool(required_bytes_sufficient(frame, operands.cursor)) then
    struct { stage = DecodeRecordLength, candidate_form = Some(form), instruction = None(), detail = "record length" }
  else struct { stage = DecodeSuccess, candidate_form = Some(form), instruction = Some(instruction), detail = "" }
}

function decode_full_record_outcome(bytes : list(bits(8))) -> Decode_outcome =
  if byte_count(bytes) == 0 then
    struct { stage = DecodeFetch, candidate_form = None(), instruction = None(), detail = "instruction byte 0 unavailable" }
  else match frame_record(bytes) {
    None() => struct { stage = DecodeFraming, candidate_form = None(), instruction = None(), detail = "record framing" },
    Some(frame) => {
      let encoding_class = encoding_class_of_record(frame.record_class);
      match opcode_payload(bytes, encoding_class) {
        None() => struct { stage = DecodeFetch, candidate_form = None(), instruction = None(), detail = "opcode bytes unavailable" },
        Some(payload) => match find_opcode_entry(payload, encoding_class, primary_form_catalog()) {
          None() => struct { stage = DecodeOpcode, candidate_form = None(), instruction = None(), detail = "unallocated opcode" },
          Some(opcode_form) => match find_catalog_entry(payload, encoding_class, primary_form_catalog()) {
              None() => struct { stage = DecodeConstraint, candidate_form = Some(opcode_form), instruction = None(), detail = "catalog constraint" },
              Some(form) => {
                let fields = decode_fields(payload, form.fields);
                let opcode_bytes = class_minimum(frame.record_class);
                match parse_ea_operands(form.operands, fields, bytes, opcode_bytes) {
                  None() => {
                    struct {
                      stage = ea_failure_stage(form.operands, fields, bytes, opcode_bytes),
                      candidate_form = Some(form), instruction = None(), detail = "effective-address encoding"
                    }
                  },
                  Some(eas) => match decode_operand_list(
                    form.operands, form.appended_payloads, fields, eas.bindings, bytes, eas.cursor
                  ) {
                    None() => struct {
                      stage = DecodeStandalonePayload, instruction = None(),
                      candidate_form = Some(form),
                      detail = "standalone operand payload"
                    },
                    Some(operands) => decode_success(form, payload, fields, operands, frame, bytes),
                  },
                }
              },
            },
        },
      }
    },
  }

function decode_full_record(bytes : list(bits(8))) -> option(Decoded_instruction) =
  match decode_full_record_outcome(bytes).instruction {
    Some(instruction) => Some(instruction),
    None() => None(),
  }
