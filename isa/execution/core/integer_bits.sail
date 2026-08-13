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

