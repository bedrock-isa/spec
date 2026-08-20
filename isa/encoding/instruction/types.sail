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
  descriptor_name : string,
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
  opcode_allocation : bits(64),
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
