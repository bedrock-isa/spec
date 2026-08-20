enum Record_class = FixedExtraShort | FixedShort | ExtendedMedium | ExtendedLong | ExtendedExtraLong

function extracted_field(payload : bits(64), positions : list(range(0, 63)), accumulated : int) -> int =
  match positions {
    [||] => accumulated,
    position :: tail => extracted_field(
      payload,
      tail,
      accumulated * 2 + (if payload[position] == bitone then 1 else 0)
    ),
  }

function value_in_ranges(value : int, ranges : list(Catalog_range)) -> bool = match ranges {
  [||] => false,
  allowed :: tail =>
    (allowed.lower <= value & value <= allowed.upper) | value_in_ranges(value, tail),
}

function constraint_matches(payload : bits(64), item : Catalog_constraint) -> bool = {
  let value = extracted_field(payload, item.field_positions, 0);
  match item.kind {
    AllowRanges => value_in_ranges(value, item.ranges),
    ExcludeImmediate => not_bool(91 <= value & value <= 94),
  }
}

function constraints_match(payload : bits(64), constraints : list(Catalog_constraint)) -> bool =
  match constraints {
    [||] => true,
    item :: tail => constraint_matches(payload, item) & constraints_match(payload, tail),
  }

function catalog_entry_matches(payload : bits(64), entry : Catalog_entry) -> bool =
  (payload & entry.mask) == entry.value & constraints_match(payload, entry.constraints)

function recognize_in_catalog(payload : bits(64), encoding_class : Encoding_class,
                              entries : list(Catalog_entry)) -> option(string) =
  match entries {
    [||] => None(),
    entry :: tail =>
      if entry.encoding_class == encoding_class & catalog_entry_matches(payload, entry)
      then Some(entry.form_id)
      else recognize_in_catalog(payload, encoding_class, tail),
  }

function recognize_primary_form(payload : bits(64), encoding_class : Encoding_class) -> option(string) =
  recognize_in_catalog(payload, encoding_class, primary_form_catalog())

struct Framed_record = {
  record_class : Record_class,
  encoded_length : int,
}

function byte_count(bytes : list(bits(8))) -> int = match bytes {
  [||] => 0,
  _ :: tail => 1 + byte_count(tail),
}

function class_minimum(record_class : Record_class) -> int = match record_class {
  FixedExtraShort => 1,
  FixedShort => 2,
  ExtendedMedium => 3,
  ExtendedLong => 4,
  ExtendedExtraLong => 5,
}

function extended_class(selector : int) -> Record_class =
  if selector <= 59 then ExtendedMedium
  else if selector <= 62 then ExtendedLong
  else ExtendedExtraLong

function frame_record(bytes : list(bits(8))) -> option(Framed_record) = match bytes {
  [|byte0|] =>
    if byte0[7] == bitzero then
      Some(struct { record_class = FixedExtraShort, encoded_length = 1 })
    else None(),
  [|byte0, _|] =>
    if byte0[7 .. 6] == 0b10 then
      Some(struct { record_class = FixedShort, encoded_length = 2 })
    else None(),
  byte0 :: byte1 :: _ :: _ => {
    let actual = byte_count(bytes);
    let encoded = 3 + unsigned(byte0[5 .. 2]);
    let selector = unsigned(byte0[1 .. 0] @ byte1[7 .. 4]);
    let record_class = extended_class(selector);
    if byte0[7 .. 6] == 0b11
       & actual == encoded
       & actual >= class_minimum(record_class)
    then Some(struct { record_class = record_class, encoded_length = encoded })
    else None()
  },
  _ => None(),
}

function required_bytes_sufficient(frame : Framed_record, required_bytes : int) -> bool =
  required_bytes >= class_minimum(frame.record_class)
  & required_bytes <= frame.encoded_length
  & required_bytes <= 18

function zero_bytes(bytes : list(bits(8))) -> list(bits(8)) = match bytes {
  [||] => [||],
  _ :: tail => 0x00 :: zero_bytes(tail),
}

function zero_after(bytes : list(bits(8)), keep : int) -> list(bits(8)) = match bytes {
  [||] => [||],
  byte :: tail =>
    if keep > 0 then byte :: zero_after(tail, keep - 1)
    else 0x00 :: zero_bytes(tail),
}

function canonical_zero_padding(bytes : list(bits(8)), required_bytes : int) -> option(list(bits(8))) =
  match frame_record(bytes) {
    Some(frame) =>
      if required_bytes_sufficient(frame, required_bytes)
      then Some(zero_after(bytes, required_bytes))
      else None(),
    None() => None(),
  }
