struct Fp_pair = {
  low : bits(4),
  high : bits(4),
}

function fpair_low(pair_id : bits(3)) -> bits(4) = match pair_id {
  0b000 => 0x0,
  0b001 => 0x2,
  0b010 => 0x4,
  0b011 => 0x6,
  0b100 => 0x8,
  0b101 => 0xA,
  0b110 => 0xC,
  0b111 => 0xE,
}

function fpair_high(pair_id : bits(3)) -> bits(4) = match pair_id {
  0b000 => 0x1,
  0b001 => 0x3,
  0b010 => 0x5,
  0b011 => 0x7,
  0b100 => 0x9,
  0b101 => 0xB,
  0b110 => 0xD,
  0b111 => 0xF,
}

function fpair(pair_id : bits(3)) -> Fp_pair = struct {
  low = fpair_low(pair_id),
  high = fpair_high(pair_id)
}

