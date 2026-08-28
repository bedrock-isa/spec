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

function operand_at(ordinal : int, operands : list(Decoded_operand)) -> option(Decoded_operand) =
  match operands {
    [||] => None(),
    operand :: tail => if ordinal == 0 then Some(operand) else operand_at(ordinal - 1, tail),
  }

function find_operand_by_name(name : Operand_id, operands : list(Decoded_operand)) -> option(Decoded_operand) =
  match operands {
    [||] => None(),
    operand :: tail => if operand.name == name then Some(operand) else find_operand_by_name(name, tail),
  }

function availability_int_contains(values : list(int), value : int) -> bool =
  match values {
    [||] => false,
    item :: tail => item == value | availability_int_contains(tail, value),
  }

function availability_operand_type_contains(
  values : list(Operand_type), value : Operand_type
) -> bool =
  match values {
    [||] => false,
    item :: tail => item == value | availability_operand_type_contains(tail, value),
  }

function availability_selector_matches(
  selector : Catalog_availability_selector,
  fields : list(Decoded_field)
) -> bool =
  match find_decoded_field(selector.field_symbol, fields) {
    Some(field) => availability_int_contains(selector.values, field.value),
    None() => false,
  }

function availability_selectors_match(
  selectors : list(Catalog_availability_selector),
  fields : list(Decoded_field)
) -> bool =
  match selectors {
    [||] => true,
    selector :: tail =>
      availability_selector_matches(selector, fields)
      & availability_selectors_match(tail, fields),
  }

function availability_operand_profile_matches(
  profile : Catalog_availability_operand_profile,
  operands : list(Decoded_operand)
) -> bool =
  match operand_at(profile.operand_ordinal, operands) {
    Some(operand) => availability_operand_type_contains(
      profile.operand_types, operand.operand_type
    ),
    None() => false,
  }

function availability_operand_profiles_match(
  profiles : list(Catalog_availability_operand_profile),
  operands : list(Decoded_operand)
) -> bool =
  match profiles {
    [||] => true,
    profile :: tail =>
      availability_operand_profile_matches(profile, operands)
      & availability_operand_profiles_match(tail, operands),
  }

function cpuid_flag_enabled(flag : Cpuid_flag, state : Cpu_state) -> bool =
  match flag {
    CpuidFlag_FP => state.fp_enabled,
    CpuidFlag_FPTRANSA => state.fptrans_enabled,
    CpuidFlag_VECTOR => state.vector_enabled,
  }

function cpuid_flags_available(flags : list(Cpuid_flag), state : Cpu_state) -> bool =
  match flags {
    [||] => true,
    flag :: tail => cpuid_flag_enabled(flag, state)
                   & cpuid_flags_available(tail, state),
  }

function matching_availability_flags(
  rules : list(Catalog_availability_rule),
  fields : list(Decoded_field),
  operands : list(Decoded_operand)
) -> option(list(Cpuid_flag)) =
  match rules {
    [||] => None(),
    rule :: tail =>
      if availability_selectors_match(rule.selectors, fields)
          & availability_operand_profiles_match(rule.operand_profiles, operands)
      then Some(rule.required_flags)
      else matching_availability_flags(tail, fields, operands),
  }

function instruction_available(instruction : Decoded_instruction, state : Cpu_state) -> bool =
  match matching_availability_flags(
    instruction.form.availability_rules, instruction.fields, instruction.operands
  ) {
    Some(flags) => cpuid_flags_available(flags, state),
    None() => false,
  }

function candidate_form_available(form : Catalog_entry, state : Cpu_state) -> bool =
  cpuid_flags_available(form.common_required_cpuid_flags, state)

function first_ea_operand(operands : list(Decoded_operand)) -> option(Decoded_operand) = match operands {
  [||] => None(),
  operand :: tail => match operand.ea { Some(_) => Some(operand), None() => first_ea_operand(tail) },
}

function commit_destination_for(operands : list(Decoded_operand), width : int) -> Commit_destination =
  match operands {
    [||] => empty_destination(),
    operand :: tail =>
      if operand.access == AccessWrite | operand.access == AccessReadWrite then
        if operand.operand_type == OperandType_Rn then struct {
          kind = DestinationRn, index = operand.value[3 .. 0], width = width
        }
        else if operand.operand_type == OperandType_Fn then struct {
          kind = DestinationFn, index = operand.value[3 .. 0], width = width
        }
        else if operand.operand_type == OperandType_SP then struct {
          kind = DestinationSP, index = 0x0, width = width
        }
        else commit_destination_for(tail, width)
      else commit_destination_for(tail, width),
  }

function size_code_bytes(code : Size_code) -> int = match code {
  Size_B => 1,
  Size_W => 2,
  Size_S => 4,
  Size_L => 4,
  _ => 8,
}

function size_list_count(items : list(Size_code)) -> int = match items {
  [||] => 0,
  _ :: tail => 1 + size_list_count(tail),
}

function size_at(items : list(Size_code), index : int) -> Size_code = match items {
  [||] => Size_Q,
  item :: tail => if index <= 0 then item else size_at(tail, index - 1),
}

val condition_size_field : list(Decoded_field) -> option(int)

function operation_width(instruction : Decoded_instruction) -> int =
  match condition_size_field(instruction.fields) {
    Some(selector) => {
      if instruction.form.instruction_set == VectorSet then
        if selector == 0 then 1
        else if selector == 1 | selector == 5 then 2
        else if selector == 2 | selector == 6 then 4
        else 8
      else {
      let count = size_list_count(instruction.form.sizes);
      let index = if count == 3 then selector - 1 else selector;
      size_code_bytes(size_at(instruction.form.sizes, index))
      }
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

function vector_operand_type_present(operands : list(Decoded_operand), operand_type : Operand_type) -> bool =
  match operands {
    [||] => false,
    operand :: tail => operand.operand_type == operand_type
                       | vector_operand_type_present(tail, operand_type),
  }

function vector_fp_arithmetic_operation(operation : Semantic_operation) -> bool =
  operation == Op_VMIN | operation == Op_VMAX | operation == Op_VDIV
  | operation == Op_VMADD | operation == Op_VMSUB | operation == Op_VNMADD
  | operation == Op_VNMSUB | operation == Op_VSQRT | operation == Op_VCOPYSIGN

function vector_fp_unary_operation(operation : Semantic_operation) -> bool =
  operation == Op_VROUND | operation == Op_VTRUNC | operation == Op_VFLOOR
  | operation == Op_VCEIL | operation == Op_VCLASS

function vector_fp_conversion_operation(operation : Semantic_operation) -> bool =
  operation == Op_VCVTH | operation == Op_VCVTUH | operation == Op_VCVTS
  | operation == Op_VCVTUS | operation == Op_VCVTD | operation == Op_VCVTUD
  | operation == Op_VCVTL | operation == Op_VCVTUL | operation == Op_VCVTQ
  | operation == Op_VCVTUQ

function vector_instruction_requires_fp(instruction : Decoded_instruction) -> bool = {
  let operation = instruction.form.operation;
  let typed_fp : bool = match condition_size_field(instruction.fields) {
    Some(selector) => selector >= 5,
    None() => false,
  };
  typed_fp | vector_operand_type_present(instruction.operands, OperandType_Fn)
  | vector_fp_arithmetic_operation(operation)
  | vector_fp_unary_operation(operation)
  | vector_fp_conversion_operation(operation)
  | operation == Op_VREDMIN | operation == Op_VREDMAX
}
