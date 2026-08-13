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

