enum Fp_value_kind = { FpValueNone, FpBits32, FpBits64, FpRaw64, FpSigned64, FpUnsigned64 }

enum Fp_result_kind = {
    FpResultValueNone,
    FpResultBits32,
    FpResultBits64,
    FpResultRaw64,
    FpResultInteger,
    FpResultValueFlags,
    FpResultPair32,
    FpResultPair64,
    FpResultPairRaw64,
}

enum Fp_destination_kind = {
    FpDestinationNone,
    FpDestinationFn,
    FpDestinationRn,
    FpDestinationMemory,
    FpDestinationFlags,
    FpDestinationFnPair,
}

enum Fp_nan_origin = { FpNotNan, FpNanOperand0, FpNanOperand1, FpNanOperand2, FpNanGeneratedDefault }

enum Fp_class = { FpZero, FpSubnormal, FpNormal, FpInfinity, FpQuietNan, FpSignalingNan }

struct Fp_operand_image = {
  valid : bool,
  kind : Fp_value_kind,
  bits : bits(64),
}

struct Fp_operand_slots = {
  operand0 : Fp_operand_image,
  operand1 : Fp_operand_image,
  operand2 : Fp_operand_image,
}

struct Fp_request_image = {
  valid : bool,
  operation : Semantic_operation,
  form_id : Form_id,
  path : Fp_path,
  operation_width : int,
  result_kind : Fp_result_kind,
  operand_count : int,
  operand0 : Fp_operand_image,
  operand1 : Fp_operand_image,
  operand2 : Fp_operand_image,
  rounding_mode : bits(2),
  daz : bool,
  ftz : bool,
  dn : bool,
  allowed_causes : bits(5),
  flags_mask : bits(4),
  transcendental : bool,
  contract_id : bits(16),
  contract_word : bits(64),
}

struct Fp_response_image = {
  valid : bool,
  echo : Fp_request_image,
  result_kind : Fp_result_kind,
  primary : bits(64),
  secondary : bits(64),
  primary_nan_origin : Fp_nan_origin,
  secondary_nan_origin : Fp_nan_origin,
  flags_mask : bits(4),
  flags_value : bits(4),
  generated_causes : bits(5),
  accuracy_mask : bits(2),
  error0_q8_8_up : bits(16),
  error1_q8_8_up : bits(16),
}

function empty_fp_operand() -> Fp_operand_image = struct {
    valid = false,
    kind = FpValueNone,
    bits = 0x0000000000000000,
}

function empty_fp_operand_slots() -> Fp_operand_slots = struct {
    operand0 = empty_fp_operand(),
    operand1 = empty_fp_operand(),
    operand2 = empty_fp_operand(),
}

function empty_fp_request() -> Fp_request_image = struct {
    valid = false,
    operation = Op_ILLEGAL,
    form_id = Form_invalid,
    path = FpPathR,
    operation_width = 0,
    result_kind = FpResultValueNone,
    operand_count = 0,
    operand0 = empty_fp_operand(),
    operand1 = empty_fp_operand(),
    operand2 = empty_fp_operand(),
    rounding_mode = 0b00,
    daz = false,
    ftz = false,
    dn = false,
    allowed_causes = fflags_none,
    flags_mask = fp_flags_none,
    transcendental = false,
    contract_id = 0x0000,
    contract_word = 0x0000000000000000,
}

function empty_fp_response() -> Fp_response_image = struct {
    valid = false,
    echo = empty_fp_request(),
    result_kind = FpResultValueNone,
    primary = 0x0000000000000000,
    secondary = 0x0000000000000000,
    primary_nan_origin = FpNotNan,
    secondary_nan_origin = FpNotNan,
    flags_mask = fp_flags_none,
    flags_value = fp_flags_none,
    generated_causes = fflags_none,
    accuracy_mask = 0b00,
    error0_q8_8_up = 0x0000,
    error1_q8_8_up = 0x0000,
}
enum Fp_state_uop_operation = {
    FpStateReadFlags,
    FpStateReadStatus,
    FpStateWriteFlags,
    FpStateWriteStatus,
}
