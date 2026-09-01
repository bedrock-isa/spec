function interrupt_identity_present(identities : list(bits(24)), identity : bits(24))
  -> bool = match identities {
  [||] => false,
  head :: tail => head == identity | interrupt_identity_present(tail, identity),
}

function interrupt_identities_with(identities : list(bits(24)), identity : bits(24))
  -> list(bits(24)) =
  if interrupt_identity_present(identities, identity) then identities
  else identity :: identities

function interrupt_identities_without(identities : list(bits(24)), identity : bits(24))
  -> list(bits(24)) = match identities {
  [||] => [||],
  head :: tail =>
    if head == identity then interrupt_identities_without(tail, identity)
    else head :: interrupt_identities_without(tail, identity),
}

function interrupt_identity_implemented(file : Interrupt_file, identity : bits(24))
  -> bool = identity != 0x000000 & unsigned(identity) <= unsigned(file.max_id)

function interrupt_file_post(file : Interrupt_file, identity : bits(24))
  -> Interrupt_file =
  if not_bool(interrupt_identity_implemented(file, identity)) then file
  else { file with pending = interrupt_identities_with(file.pending, identity) }

function post_interrupt(state : Cpu_state, identity : bits(24)) -> Cpu_state = {
  var updated = state;
  updated.controls.interrupt_file = interrupt_file_post(
    state.controls.interrupt_file, identity
  );
  updated
}

function interrupt_identity_eligible(file : Interrupt_file, identity : bits(24))
  -> bool =
  interrupt_identity_present(file.enabled, identity)
  & (file.threshold == 0x000000
     | unsigned(identity) < unsigned(file.threshold))

function interrupt_top_from(file : Interrupt_file, pending : list(bits(24)),
                            selected : bits(24)) -> bits(24) = match pending {
  [||] => selected,
  identity :: tail => {
    let eligible = interrupt_identity_eligible(file, identity);
    let next = if eligible
      & (selected == 0x000000 | unsigned(identity) < unsigned(selected))
      then identity else selected;
    interrupt_top_from(file, tail, next)
  },
}

function interrupt_top(file : Interrupt_file) -> bits(24) =
  interrupt_top_from(file, file.pending, 0x000000)

function interrupt_identity_word(identity : bits(24)) -> int =
  tdiv_int(unsigned(identity), 64)

function interrupt_identity_bit(identity : bits(24)) -> int =
  tmod_int(unsigned(identity), 64)

function interrupt_selected_word(file : Interrupt_file) -> int =
  unsigned(file.selector[17 .. 0])

function interrupt_selected_bank(file : Interrupt_file) -> int =
  unsigned(file.selector[19 .. 18])

function interrupt_word_valid(file : Interrupt_file, word : int) -> bool =
  word >= 0 & word <= tdiv_int(unsigned(file.max_id), 64)

function interrupt_identities_word(identities : list(bits(24)), word : int)
  -> bits(64) = match identities {
  [||] => 0x0000000000000000,
  identity :: tail => {
    let remainder = interrupt_identities_word(tail, word);
    if interrupt_identity_word(identity) != word then remainder
    else remainder
      | sail_shiftleft(0x0000000000000001, interrupt_identity_bit(identity))
  },
}

function interrupt_idata_value(file : Interrupt_file) -> bits(64) = {
  let word = interrupt_selected_word(file);
  let bank = interrupt_selected_bank(file);
  if bank == 0 then interrupt_identities_word(file.pending, word)
  else if bank == 3 then interrupt_identities_word(file.enabled, word)
  else 0x0000000000000000
}

function interrupt_word_source_has_reserved_bit(
  file : Interrupt_file, word : int, source : bits(64), bit : int
) -> bool =
  if bit >= 64 then false
  else {
    let identity = get_slice_int(24, word * 64 + bit, 0);
    (sail_shiftright(source, bit)[0] == bitone
     & not_bool(interrupt_identity_implemented(file, identity)))
    | interrupt_word_source_has_reserved_bit(file, word, source, bit + 1)
  }

function interrupt_identities_write_word(
  file : Interrupt_file, identities : list(bits(24)), word : int,
  source : bits(64), bit : int, replace : bool
) -> list(bits(24)) =
  if bit >= 64 then identities
  else {
    let identity = get_slice_int(24, word * 64 + bit, 0);
    let implemented = interrupt_identity_implemented(file, identity);
    let selected = sail_shiftright(source, bit)[0] == bitone;
    let updated = if not_bool(implemented) then identities
      else if selected then interrupt_identities_with(identities, identity)
      else if replace then interrupt_identities_without(identities, identity)
      else identities;
    interrupt_identities_write_word(file, updated, word, source, bit + 1, replace)
  }

function interrupt_identities_clear_word(
  file : Interrupt_file, identities : list(bits(24)), word : int,
  source : bits(64), bit : int
) -> list(bits(24)) =
  if bit >= 64 then identities
  else {
    let identity = get_slice_int(24, word * 64 + bit, 0);
    let updated = if interrupt_identity_implemented(file, identity)
      & sail_shiftright(source, bit)[0] == bitone
      then interrupt_identities_without(identities, identity)
      else identities;
    interrupt_identities_clear_word(file, updated, word, source, bit + 1)
  }

function interrupt_file_with_idata(file : Interrupt_file, source : bits(64))
  -> Interrupt_file = {
  let word = interrupt_selected_word(file);
  let bank = interrupt_selected_bank(file);
  if bank == 1 then { file with pending = interrupt_identities_write_word(
    file, file.pending, word, source, 0, false
  ) }
  else if bank == 2 then { file with pending = interrupt_identities_clear_word(
    file, file.pending, word, source, 0
  ) }
  else if bank == 3 then { file with enabled = interrupt_identities_write_word(
    file, file.enabled, word, source, 0, true
  ) }
  else file
}

function interrupt_file_clear(file : Interrupt_file, identity : bits(24))
  -> Interrupt_file =
  { file with pending = interrupt_identities_without(file.pending, identity) }
