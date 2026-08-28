function fp_width_mask(width : int) -> option(bits(64)) =
  if width == 2 then Some(0x000000000000FFFF)
  else if width == 4 then Some(0x00000000FFFFFFFF)
  else if width == 8 then Some(0xFFFFFFFFFFFFFFFF)
  else None()

function fp_sign_mask(width : int) -> option(bits(64)) =
  if width == 2 then Some(0x0000000000008000)
  else if width == 4 then Some(0x0000000080000000)
  else if width == 8 then Some(0x8000000000000000)
  else None()

function fp_bitwise_fmov(value : bits(64), width : int) -> option(bits(64)) =
  match fp_width_mask(width) {
    Some(mask) => Some(value & mask),
    None() => None(),
  }

function fp_bitwise_fabs(value : bits(64), width : int) -> option(bits(64)) =
  match (fp_width_mask(width), fp_sign_mask(width)) {
    (Some(width_mask), Some(sign_mask)) => Some((value & width_mask) & not_vec(sign_mask)),
    _ => None(),
  }

function fp_bitwise_fneg(value : bits(64), width : int) -> option(bits(64)) =
  match (fp_width_mask(width), fp_sign_mask(width)) {
    (Some(width_mask), Some(sign_mask)) => Some(xor_vec(value & width_mask, sign_mask)),
    _ => None(),
  }

function fp_bitwise_fcopysign(sign_source : bits(64), magnitude_source : bits(64),
                              width : int) -> option(bits(64)) =
  match (fp_width_mask(width), fp_sign_mask(width)) {
    (Some(width_mask), Some(sign_mask)) =>
      Some(((magnitude_source & width_mask) & not_vec(sign_mask))
           | (sign_source & sign_mask)),
    _ => None(),
  }

function fp_exact_arithmetic(operation : Fp_arithmetic_operation,
                             value : bits(64), width : int) -> option(bits(64)) =
  match operation {
    FpArithmeticAbsolute => fp_bitwise_fabs(value, width),
    FpArithmeticNegate => fp_bitwise_fneg(value, width),
    _ => None(),
  }

function fp_bitwise_fclr() -> bits(64) = 0x0000000000000000

struct Fp_exchange_result = {
  lhs : bits(64),
  rhs : bits(64),
}

function fp_bitwise_fxchg(lhs : bits(64), rhs : bits(64)) -> Fp_exchange_result =
  struct { lhs = rhs, rhs = lhs }

function fp_fclass(value : bits(64), width : int) -> option(bits(64)) =
  match fp_classify_raw(value, width) {
    None() => None(),
    Some(class) => {
      let negative = if width == 2 then value[15] == bitone
                     else if width == 4 then value[31] == bitone
                     else value[63] == bitone;
      Some(match class {
        FpInfinity => if negative then 0x0000000000000001 else 0x0000000000000080,
        FpNormal => if negative then 0x0000000000000002 else 0x0000000000000040,
        FpSubnormal => if negative then 0x0000000000000004 else 0x0000000000000020,
        FpZero => if negative then 0x0000000000000008 else 0x0000000000000010,
        FpSignalingNan => 0x0000000000000100,
        FpQuietNan => 0x0000000000000200,
      })
    },
  }

function fp_exact_data(operation : Fp_data_operation, operand0 : bits(64),
                       operand1 : bits(64), width : int) -> option(bits(64)) =
  match operation {
    FpDataCopySign => fp_bitwise_fcopysign(operand0, operand1, width),
    FpDataClassify => fp_fclass(operand0, width),
  }

function fp_fmovcr(constant_id : bits(16)) -> option(bits(64)) = match constant_id {
  0x0000 => Some(0x0000000000000000),
  0x0001 => Some(0x8000000000000000),
  0x0002 => Some(0x3FF0000000000000),
  0x0003 => Some(0xBFF0000000000000),
  0x0004 => Some(0x3FE0000000000000),
  0x0005 => Some(0xBFE0000000000000),
  0x0006 => Some(0x4000000000000000),
  0x0007 => Some(0xC000000000000000),
  0x0008 => Some(0x4024000000000000),
  0x0009 => Some(0xC024000000000000),
  0x0010 => Some(0x400921FB54442D18),
  0x0011 => Some(0x3FF921FB54442D18),
  0x0012 => Some(0x3FE921FB54442D18),
  0x0013 => Some(0x401921FB54442D18),
  0x0014 => Some(0x3FD45F306DC9C883),
  0x0015 => Some(0x3FE45F306DC9C883),
  0x0016 => Some(0x3FF6A09E667F3BCD),
  0x0017 => Some(0x3FE6A09E667F3BCC),
  0x0020 => Some(0x4005BF0A8B145769),
  0x0021 => Some(0x3FF71547652B82FE),
  0x0022 => Some(0x3FDBCB7B1526E50E),
  0x0023 => Some(0x3FE62E42FEFA39EF),
  0x0024 => Some(0x40026BB1BBB55516),
  0x0025 => Some(0x400A934F0979A371),
  0x0026 => Some(0x3FD34413509F79FF),
  0x0100 => Some(0x7FF0000000000000),
  0x0101 => Some(0xFFF0000000000000),
  0x0102 => Some(0x7FF8000000000000),
  0x0103 => Some(0xFFF8000000000000),
  0x0104 => Some(0x7FF0000000000001),
  0x0105 => Some(0xFFF0000000000001),
  0x0110 => Some(0x7FEFFFFFFFFFFFFF),
  0x0111 => Some(0xFFEFFFFFFFFFFFFF),
  0x0112 => Some(0x0010000000000000),
  0x0113 => Some(0x8010000000000000),
  0x0114 => Some(0x0000000000000001),
  0x0115 => Some(0x8000000000000001),
  0x0116 => Some(0x3CB0000000000000),
  0x0117 => Some(0x000FFFFFFFFFFFFF),
  0x0118 => Some(0x800FFFFFFFFFFFFF),
  _ => None(),
}
