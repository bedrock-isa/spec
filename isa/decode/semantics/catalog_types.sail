enum Encoding_class = ExtraShort | Short | Medium | Long | ExtraLong | Xxlong

enum Constraint_kind = AllowRanges | ExcludeImmediate

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
  symbol : Field_id,
  operand_type : Operand_type,
  kind : Metadata_field_kind,
  positions : list(range(0, 63)),
}

struct Catalog_operand = {
  name : Operand_id,
  operand_type : Operand_type,
  access : Metadata_access,
  field_symbol : option(Field_id),
  field_positions : list(range(0, 63)),
  domain : option(Operand_domain),
  ea_role : option(Ea_role),
  ea_width : option(Ea_width),
  ea_profile : option(Ea_profile),
  has_fixed_value : bool,
  fixed_value : int,
  legal_values : list(int),
}

struct Catalog_payload = {
  operand_name : Operand_id,
  operand_type : Operand_type,
  width : int,
  signed : bool,
}

struct Ea_pattern = {
  width : int,
  value : bits(16),
  mask : bits(16),
}

struct Ea_field = {
  symbol : Field_id,
  operand_type : Operand_type,
  role : Ea_role,
  positions : list(range(0, 15)),
}

struct Ea_form = {
  name : Ea_form_id,
  profile : option(Ea_profile),
  descriptor_family : option(Ea_descriptor_family),
  descriptor_bytes : int,
  patterns : list(Ea_pattern),
  kind : Ea_kind,
  fields : list(Ea_field),
  segment : option(Ea_segment),
  payload_width : int,
  payload_signed : bool,
  base : option(Ea_base),
  descriptor : option(Ea_descriptor_family),
  update_target : option(Ea_update_target),
  update_mode : option(Ea_update_mode),
  update_difference : option(Ea_update_difference),
}

struct Representative_record = {
  form_id : Form_id,
  bytes : list(bits(8)),
}

struct Catalog_entry = {
  form_id : Form_id,
  operation : Semantic_operation,
  route : Semantic_route,
  instruction_set : Instruction_set,
  privilege : Privilege_level,
  predicate_mode : Predicate_mode,
  repeat_rep : bool,
  repeat_repcc : bool,
  encoding_class : Encoding_class,
  value : bits(64),
  mask : bits(64),
  constraints : list(Catalog_constraint),
  fields : list(Catalog_field),
  operands : list(Catalog_operand),
  sizes : list(Size_code),
  appended_payloads : list(Catalog_payload),
  required_cpuid_flags : list(Cpuid_flag),
}
