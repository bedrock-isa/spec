enum Encoding_class = ExtraShort | Short | Medium | Long | ExtraLong

enum Constraint_kind = AllowRanges | ExcludeRnDirect | ExcludeRegDirect | ExcludeImmediate

enum Metadata_field_kind = FieldRn | FieldFreg | FieldEa | FieldCondition | FieldSize | FieldImmediate | FieldBits
enum Metadata_access = AccessRead | AccessWrite | AccessReadWrite | AccessAddress

struct Catalog_range = {
  lower : int,
  upper : int,
}

struct Catalog_constraint = {
  field_positions : list(range(0, 63)),
  kind : Constraint_kind,
  ranges : list(Catalog_range),
  reason : string,
}

struct Catalog_field = {
  symbol : string,
  type_name : string,
  kind : Metadata_field_kind,
  positions : list(range(0, 63)),
}

struct Catalog_operand = {
  name : string,
  type_name : string,
  access : Metadata_access,
  field_symbol : string,
  field_positions : list(range(0, 63)),
  domain : string,
  ea_role : string,
  ea_width : string,
  has_fixed_value : bool,
  fixed_value : int,
  fixed_identity : string,
  legal_values : list(int),
}

struct Catalog_payload = {
  operand_name : string,
  type_name : string,
  width : int,
  signed : bool,
}

struct Catalog_exception = {
  event : string,
  when_text : string,
  forms : list(string),
}

struct Catalog_overlap = {
  left : string,
  right : string,
  rule : string,
}

struct Ea_pattern = {
  width : int,
  value : bits(16),
  mask : bits(16),
}

struct Ea_field = {
  symbol : string,
  type_name : string,
  role : string,
  positions : list(range(0, 15)),
}

struct Ea_form = {
  name : string,
  descriptor_family : string,
  descriptor_bytes : int,
  patterns : list(Ea_pattern),
  kind : string,
  fields : list(Ea_field),
  segment : string,
  payload : string,
  payload_width : int,
  payload_signed : bool,
  base : string,
  register_name : string,
  descriptor : string,
  update_target : string,
  update_mode : string,
}

struct Representative_record = {
  form_id : string,
  mnemonic : string,
  bytes : list(bits(8)),
}

struct Catalog_entry = {
  form_id : string,
  mnemonic : string,
  operation : Semantic_operation,
  route : Semantic_route,
  instruction_set : Instruction_set,
  instruction_class : string,
  family : string,
  privilege : Privilege_level,
  predicate_mode : Predicate_mode,
  has_ea_operand : bool,
  repeat_rep : bool,
  repeat_repcc : bool,
  repeat_repg : bool,
  repeat_observed_kind : string,
  repeat_observed_operand : string,
  flag_effects : list(string),
  exceptions : list(Catalog_exception),
  encoding_class : Encoding_class,
  payload_width : int,
  value : bits(64),
  mask : bits(64),
  constraints : list(Catalog_constraint),
  fields : list(Catalog_field),
  operands : list(Catalog_operand),
  sizes : list(string),
  appended_payloads : list(Catalog_payload),
  overlaps : list(Catalog_overlap),
}
