struct Cfi_mac_state = {
  v0 : bits(64),
  v1 : bits(64),
  v2 : bits(64),
  v3 : bits(64),
}

function cfi_key_configured(state : Cpu_state) -> bool =
  state.lkl != 0x0000000000000000 | state.lkh != 0x0000000000000000

function cfi_rotate_left(value : bits(64), count : int) -> bits(64) =
  sail_shiftleft(value, count) | sail_shiftright(value, 64 - count)

function cfi_mac_round(state : Cfi_mac_state) -> Cfi_mac_state = {
  var mixed = state;
  mixed.v0 = add_bits(mixed.v0, mixed.v1);
  mixed.v1 = xor_vec(cfi_rotate_left(mixed.v1, 13), mixed.v0);
  mixed.v0 = cfi_rotate_left(mixed.v0, 32);
  mixed.v2 = add_bits(mixed.v2, mixed.v3);
  mixed.v3 = xor_vec(cfi_rotate_left(mixed.v3, 16), mixed.v2);
  mixed.v0 = add_bits(mixed.v0, mixed.v3);
  mixed.v3 = xor_vec(cfi_rotate_left(mixed.v3, 21), mixed.v0);
  mixed.v2 = add_bits(mixed.v2, mixed.v1);
  mixed.v1 = xor_vec(cfi_rotate_left(mixed.v1, 17), mixed.v2);
  mixed.v2 = cfi_rotate_left(mixed.v2, 32);
  mixed
}

function cfi_mac_rounds(state : Cfi_mac_state, count : int) -> Cfi_mac_state =
  if count <= 0 then state else cfi_mac_rounds(cfi_mac_round(state), count - 1)

function cfi_mac_absorb(state : Cfi_mac_state, word : bits(64))
  -> Cfi_mac_state = {
  var mixed = state;
  mixed.v3 = xor_vec(mixed.v3, word);
  mixed = cfi_mac_rounds(mixed, 2);
  mixed.v0 = xor_vec(mixed.v0, word);
  mixed
}

function cfi_mac_absorb_words(state : Cfi_mac_state, words : list(bits(64)))
  -> Cfi_mac_state =
  match words {
    [||] => state,
    word :: tail => cfi_mac_absorb_words(cfi_mac_absorb(state, word), tail),
  }

function cfi_reference_mac(state : Cpu_state, domain : bits(64),
                           continuation_pc : bits(64),
                           continuation_cs : bits(64), slot_sp : bits(64))
  -> bits(64) = {
  let initial : Cfi_mac_state = struct {
    v0 = xor_vec(0x736F6D6570736575, state.lkl),
    v1 = xor_vec(0x646F72616E646F6D, state.lkh),
    v2 = xor_vec(0x6C7967656E657261, state.lkl),
    v3 = xor_vec(0x7465646279746573, state.lkh),
  };
  var mixed = cfi_mac_absorb_words(initial, [|
    domain, continuation_pc, continuation_cs, state.segments[2], slot_sp
  |]);
  mixed.v2 = xor_vec(mixed.v2, 0x00000000000000FF);
  mixed = cfi_mac_rounds(mixed, 4);
  xor_vec(xor_vec(mixed.v0, mixed.v1), xor_vec(mixed.v2, mixed.v3))
}

function cfi_pointer_authentication(state : Cpu_state, long_return : bool,
                                    continuation_pc : bits(64),
                                    continuation_cs : bits(64)) -> bits(64) = {
  let domain = if long_return then 0x4C4F4E475F504131
               else 0x4E4541525F504131;
  let cs = if long_return then continuation_cs else 0x0000000000000000;
  let truncated = cfi_reference_mac(
    state, domain, continuation_pc, cs, state.sp
  ) & 0x7FFFFFFFFFFFFFFF;
  if truncated == 0x0000000000000000 then 0x7FFFFFFFFFFFFFFF
  else truncated
}
