type Fp_primitive_bits8 = bits(8)
type Fp_primitive_bits2 = bits(2)
type Fp_primitive_bits64 = bits(64)

val bedrock_numeric_primitive = pure {c: "bedrock_numeric_primitive"} :
  (Semantic_operation, Fp_primitive_bits8, Fp_primitive_bits8,
   Fp_primitive_bits8, Fp_primitive_bits8,
   Fp_primitive_bits8, Fp_primitive_bits64,
   Fp_primitive_bits8, Fp_primitive_bits64,
   Fp_primitive_bits8, Fp_primitive_bits64,
   Fp_primitive_bits8, Fp_primitive_bits8) -> Fp_primitive_bits64

function fp_primitive_value_kind_code(kind : Fp_value_kind) -> bits(8) = match kind {
  FpValueNone => 0x00,
  FpBits16 => 0x06,
  FpBits32 => 0x01,
  FpBits64 => 0x02,
  FpRaw64 => 0x03,
  FpSigned64 => 0x04,
  FpUnsigned64 => 0x05,
}

function fp_primitive_result_kind_code(kind : Fp_result_kind) -> bits(8) = match kind {
  FpResultValueNone => 0x00,
  FpResultBits16 => 0x09,
  FpResultBits32 => 0x01,
  FpResultBits64 => 0x02,
  FpResultRaw64 => 0x03,
  FpResultInteger => 0x04,
  FpResultValueFlags => 0x05,
  FpResultPair32 => 0x06,
  FpResultPair64 => 0x07,
  FpResultPairRaw64 => 0x08,
}

function fp_primitive_control(rounding_mode : bits(2), ftz : bool,
                              daz : bool, dn : bool) -> bits(8) =
  0b000 @ (if dn then 0b1 else 0b0)
        @ (if daz then 0b1 else 0b0)
        @ (if ftz then 0b1 else 0b0)
        @ rounding_mode

function fp_primitive_nan_origin(raw : bits(3)) -> option(Fp_nan_origin) =
  if raw == 0b000 then Some(FpNotNan)
  else if raw == 0b001 then Some(FpNanOperand0)
  else if raw == 0b010 then Some(FpNanOperand1)
  else if raw == 0b011 then Some(FpNanOperand2)
  else if raw == 0b100 then Some(FpNanGeneratedDefault)
  else None()

struct Fp_primitive_evaluation = {
  primary : bits(64),
  secondary : bits(64),
  primary_nan_origin : Fp_nan_origin,
  secondary_nan_origin : Fp_nan_origin,
  flags_value : bits(4),
  generated_causes : bits(5),
  accuracy_mask : bits(2),
  error0_q8_8_up : bits(16),
  error1_q8_8_up : bits(16),
}

function fp_primitive_evaluate(
  operation : Semantic_operation, width : int, result_kind : bits(8),
  control : bits(8), operand_count : int,
  kind0 : bits(8), bits0 : bits(64),
  kind1 : bits(8), bits1 : bits(64),
  kind2 : bits(8), bits2 : bits(64),
  transcendental : bool
) -> option(Fp_primitive_evaluation) = {
  let width_bits = get_slice_int(8, width, 0);
  let count_bits = get_slice_int(8, operand_count, 0);
  let trans_bits : bits(8) = if transcendental then 0x01 else 0x00;
  let primary = bedrock_numeric_primitive(
    operation, width_bits, result_kind, control, count_bits,
    kind0, bits0, kind1, bits1, kind2, bits2, trans_bits, 0x00
  );
  let secondary = bedrock_numeric_primitive(
    operation, width_bits, result_kind, control, count_bits,
    kind0, bits0, kind1, bits1, kind2, bits2, trans_bits, 0x01
  );
  let metadata = bedrock_numeric_primitive(
    operation, width_bits, result_kind, control, count_bits,
    kind0, bits0, kind1, bits1, kind2, bits2, trans_bits, 0x02
  );
  match (fp_primitive_nan_origin(metadata[11 .. 9]),
         fp_primitive_nan_origin(metadata[14 .. 12])) {
    (Some(primary_origin), Some(secondary_origin)) =>
      if metadata[63] == bitzero then None()
      else Some(struct {
        primary = primary,
        secondary = secondary,
        primary_nan_origin = primary_origin,
        secondary_nan_origin = secondary_origin,
        flags_value = metadata[8 .. 5],
        generated_causes = metadata[4 .. 0],
        accuracy_mask = metadata[16 .. 15],
        error0_q8_8_up = metadata[32 .. 17],
        error1_q8_8_up = metadata[48 .. 33]
      }),
    _ => None(),
  }
}

function fp_primitive_response(request : Fp_request_image)
  -> option(Fp_response_image) = {
  match fp_primitive_evaluate(
    request.operation, request.operation_width,
    fp_primitive_result_kind_code(request.result_kind),
    fp_primitive_control(request.rounding_mode, request.ftz, request.daz, request.dn),
    request.operand_count,
    fp_primitive_value_kind_code(request.operand0.kind), request.operand0.bits,
    fp_primitive_value_kind_code(request.operand1.kind), request.operand1.bits,
    fp_primitive_value_kind_code(request.operand2.kind), request.operand2.bits,
    request.transcendental
  ) {
    Some(evaluation) => {
      let response : Fp_response_image = struct {
        valid = true,
        echo = request,
        result_kind = request.result_kind,
        primary = evaluation.primary,
        secondary = evaluation.secondary,
        primary_nan_origin = evaluation.primary_nan_origin,
        secondary_nan_origin = evaluation.secondary_nan_origin,
        flags_mask = request.flags_mask,
        flags_value = evaluation.flags_value,
        generated_causes = evaluation.generated_causes,
        accuracy_mask = evaluation.accuracy_mask,
        error0_q8_8_up = evaluation.error0_q8_8_up,
        error1_q8_8_up = evaluation.error1_q8_8_up
      };
      Some(response)
    },
    None() => None(),
  }
}
