function fp_fstatus_rounding_mode(fstatus : bits(64)) -> bits(2) = fstatus[6 .. 5]
function fp_fstatus_exception_enables(fstatus : bits(64)) -> bits(5) = fstatus[4 .. 0]
function fp_fstatus_ftz(fstatus : bits(64)) -> bool = fstatus[7] == bitone
function fp_fstatus_daz(fstatus : bits(64)) -> bool = fstatus[8] == bitone
function fp_fstatus_dn(fstatus : bits(64)) -> bool = fstatus[9] == bitone
function fp_make_fstatus(rounding_mode : bits(2), ftz : bool, daz : bool, dn : bool,
                         exception_enables : bits(5)) -> bits(64) =
  0x00000000 @ 0b0000000000000000000000
  @ (if dn then 0b1 else 0b0)
  @ (if daz then 0b1 else 0b0)
  @ (if ftz then 0b1 else 0b0)
  @ rounding_mode @ exception_enables
function fp_fstatus_valid(fstatus : bits(64)) -> bool =
  fstatus[63 .. 32] == 0x00000000
  & fstatus[31 .. 10] == 0b0000000000000000000000

function fp_classify_raw(value : bits(64), width : int) -> option(Fp_class) =
  if width == 2 then {
    let exponent = value[14 .. 10];
    let fraction = value[9 .. 0];
    if exponent == 0b00000 then
      Some(if fraction == 0b0000000000 then FpZero else FpSubnormal)
    else if exponent != 0b11111 then Some(FpNormal)
    else if fraction == 0b0000000000 then Some(FpInfinity)
    else if fraction[9] == bitone then Some(FpQuietNan)
    else Some(FpSignalingNan)
  }
  else if width == 4 then {
    let exponent = value[30 .. 23];
    let fraction = value[22 .. 0];
    if exponent == 0x00 then
      Some(if fraction == 0b00000000000000000000000 then FpZero else FpSubnormal)
    else if exponent != 0xFF then Some(FpNormal)
    else if fraction == 0b00000000000000000000000 then Some(FpInfinity)
    else if fraction[22] == bitone then Some(FpQuietNan)
    else Some(FpSignalingNan)
  }
  else if width == 8 then {
    let exponent = value[62 .. 52];
    let fraction = value[51 .. 0];
    if exponent == 0b00000000000 then
      Some(if fraction == 0x0000000000000 then FpZero else FpSubnormal)
    else if exponent != 0b11111111111 then Some(FpNormal)
    else if fraction == 0x0000000000000 then Some(FpInfinity)
    else if fraction[51] == bitone then Some(FpQuietNan)
    else Some(FpSignalingNan)
  }
  else None()

function fp_operand_width(operand : Fp_operand_image) -> int = match operand.kind {
  FpBits32 => 4,
  FpBits64 => 8,
  _ => 0,
}

function fp_operand_class(operand : Fp_operand_image) -> option(Fp_class) =
  if not_bool(operand.valid) then None()
  else fp_classify_raw(operand.bits, fp_operand_width(operand))

function fp_class_is_nan(class : Fp_class) -> bool =
  class == FpQuietNan | class == FpSignalingNan

function fp_operand_is_class(operand : Fp_operand_image, class : Fp_class) -> bool =
  match fp_operand_class(operand) { Some(actual) => actual == class, None() => false }

function fp_signed_zero(value : bits(64), width : int) -> bits(64) =
  if width == 2 then value & 0x0000000000008000
  else if width == 4 then value & 0x0000000080000000
  else value & 0x8000000000000000

function fp_apply_daz(operand : Fp_operand_image, daz : bool) -> Fp_operand_image =
  if daz & fp_operand_is_class(operand, FpSubnormal) then
    { operand with bits = fp_signed_zero(operand.bits, fp_operand_width(operand)) }
  else operand

function fp_default_nan(width : int) -> bits(64) =
  if width == 2 then 0x0000000000007E00
  else if width == 4 then 0x000000007FC00000 else 0x7FF8000000000000

function fp_quiet_nan(value : bits(64), width : int) -> bits(64) =
  if width == 2 then (value & 0x000000000000FFFF) | 0x0000000000000200
  else if width == 4 then (value & 0x00000000FFFFFFFF) | 0x0000000000400000
  else value | 0x0008000000000000

function fp_apply_dn(value : Fp_operand_image, dn : bool) -> Fp_operand_image =
  match fp_operand_class(value) {
    Some(class) => if fp_class_is_nan(class) then
      { value with bits = if dn then fp_default_nan(fp_operand_width(value))
                          else fp_quiet_nan(value.bits, fp_operand_width(value)) }
      else value,
    None() => value,
  }

struct Fp_postprocess_result = {
  value : Fp_operand_image,
  generated_causes : bits(5),
}

function fp_apply_ftz(value : Fp_operand_image, ftz : bool, transcendental : bool,
                      generated_causes : bits(5)) -> Fp_postprocess_result =
  if ftz & fp_operand_is_class(value, FpSubnormal) then struct {
    value = { value with bits = fp_signed_zero(value.bits, fp_operand_width(value)) },
    generated_causes = generated_causes | fflags_uf
      | (if transcendental then fflags_none else fflags_nx)
  }
  else struct { value = value, generated_causes = generated_causes }

function fp_postprocess(value : Fp_operand_image, fstatus : bits(64),
                        transcendental : bool, generated_causes : bits(5))
  -> Fp_postprocess_result =
  fp_apply_ftz(fp_apply_dn(value, fp_fstatus_dn(fstatus)), fp_fstatus_ftz(fstatus),
               transcendental, generated_causes)

function fp_postprocess_pre_dn_response(value : Fp_operand_image,
                                        request : Fp_request_image,
                                        generated_causes : bits(5))
  -> Fp_postprocess_result =
  fp_apply_ftz(fp_apply_dn(value, request.dn), request.ftz,
               request.transcendental, generated_causes)

function fp_origin_for_index(index : int) -> Fp_nan_origin =
  if index == 0 then FpNanOperand0
  else if index == 1 then FpNanOperand1
  else FpNanOperand2

function fp_request_operand(request : Fp_request_image, index : int) -> Fp_operand_image =
  if index == 0 then request.operand0
  else if index == 1 then request.operand1
  else request.operand2

function fp_first_source_class(request : Fp_request_image, class : Fp_class,
                               index : int) -> option(Fp_nan_origin) =
  if index >= request.operand_count | index >= 3 then None()
  else if fp_operand_is_class(fp_request_operand(request, index), class)
  then Some(fp_origin_for_index(index))
  else fp_first_source_class(request, class, index + 1)

function fp_source_nan_origin(request : Fp_request_image) -> option(Fp_nan_origin) =
  match fp_first_source_class(request, FpSignalingNan, 0) {
    Some(origin) => Some(origin),
    None() => fp_first_source_class(request, FpQuietNan, 0),
  }

function fp_expected_nan_origin(request : Fp_request_image,
                                result : Fp_operand_image) -> Fp_nan_origin =
  match fp_operand_class(result) {
    Some(class) => if fp_class_is_nan(class) then
      match fp_source_nan_origin(request) {
        Some(origin) => origin,
        None() => FpNanGeneratedDefault,
      }
      else FpNotNan,
    None() => FpNotNan,
  }

function fp_nan_origin_valid(request : Fp_request_image, result : Fp_operand_image,
                             origin : Fp_nan_origin) -> bool =
  origin == fp_expected_nan_origin(request, result)

function fp_nan_source(request : Fp_request_image) -> option(Fp_operand_image) =
  match fp_source_nan_origin(request) {
    Some(FpNanOperand0) => Some(request.operand0),
    Some(FpNanOperand1) => Some(request.operand1),
    Some(FpNanOperand2) => Some(request.operand2),
    _ => None(),
  }

function fp_convert_nan_payload(value : bits(64), source_width : int,
                                result_width : int) -> option(bits(64)) = {
  let quiet = fp_quiet_nan(value, source_width);
  if source_width == result_width & (result_width == 4 | result_width == 8) then
    Some(quiet)
  else if source_width == 4 & result_width == 8 then {
    let sign = if quiet[31] == bitone then 0x8000000000000000
               else 0x0000000000000000;
    Some(sign | 0x7FF0000000000000
         | sail_shiftleft(sail_zero_extend(quiet[22 .. 0], 64), 29))
  }
  else if source_width == 8 & result_width == 4 then {
    let sign = if quiet[63] == bitone then 0x0000000080000000
               else 0x0000000000000000;
    Some(sign | 0x000000007F800000 | sail_zero_extend(quiet[51 .. 29], 64))
  }
  else None()
}

function fp_expected_pre_dn_nan(request : Fp_request_image,
                                result_width : int) -> option(bits(64)) =
  match fp_nan_source(request) {
    Some(source) => fp_convert_nan_payload(source.bits, fp_operand_width(source),
                                           result_width),
    None() => if result_width == 4 | result_width == 8
              then Some(fp_default_nan(result_width)) else None(),
  }

function fp_request_has_signaling_nan(request : Fp_request_image) -> bool =
  match fp_first_source_class(request, FpSignalingNan, 0) {
    Some(_) => true,
    None() => false,
  }

function fp_pre_dn_nan_payload_valid(request : Fp_request_image,
                                     result : Fp_operand_image) -> bool =
  match fp_operand_class(result) {
    Some(class) => if fp_class_is_nan(class) then
      match fp_expected_pre_dn_nan(request, fp_operand_width(result)) {
        Some(expected) => result.bits == expected,
        None() => false,
      }
      else true,
    None() => true,
  }
