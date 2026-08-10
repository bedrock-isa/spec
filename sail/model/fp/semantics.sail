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
  if width == 4 then {
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
  if width == 4 then value & 0x0000000080000000
  else value & 0x8000000000000000

function fp_apply_daz(operand : Fp_operand_image, daz : bool) -> Fp_operand_image =
  if daz & fp_operand_is_class(operand, FpSubnormal) then
    { operand with bits = fp_signed_zero(operand.bits, fp_operand_width(operand)) }
  else operand

function fp_default_nan(width : int) -> bits(64) =
  if width == 4 then 0x000000007FC00000 else 0x7FF8000000000000

function fp_quiet_nan(value : bits(64), width : int) -> bits(64) =
  if width == 4 then (value & 0x00000000FFFFFFFF) | 0x0000000000400000
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

function fp_width_mask(width : int) -> option(bits(64)) =
  if width == 4 then Some(0x00000000FFFFFFFF)
  else if width == 8 then Some(0xFFFFFFFFFFFFFFFF)
  else None()

function fp_sign_mask(width : int) -> option(bits(64)) =
  if width == 4 then Some(0x0000000080000000)
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
      let negative = if width == 4 then value[31] == bitone else value[63] == bitone;
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

function fp_operation_is_exact_local(operation : Semantic_operation) -> bool =
  operation == Op_FABS | operation == Op_FNEG | operation == Op_FCOPYSIGN
  | operation == Op_FMOV | operation == Op_FMOVcc | operation == Op_FCLR
  | operation == Op_FXCHG | operation == Op_FCLASS | operation == Op_FMOVCR

function fp_operand_image_valid(operand : Fp_operand_image) -> bool =
  if operand.valid then match operand.kind {
    FpValueNone => false,
    FpBits32 => operand.bits[63 .. 32] == 0x00000000,
    _ => true,
  }
  else operand.kind == FpValueNone & operand.bits == 0x0000000000000000

function fp_operand_slot_get(slots : Fp_operand_slots,
                             index : int) -> option(Fp_operand_image) =
  if index == 0 then Some(slots.operand0)
  else if index == 1 then Some(slots.operand1)
  else if index == 2 then Some(slots.operand2)
  else None()

function fp_operand_slot_set(slots : Fp_operand_slots, index : int,
                             operand : Fp_operand_image) -> option(Fp_operand_slots) =
  if index == 0 then Some({ slots with operand0 = operand })
  else if index == 1 then Some({ slots with operand1 = operand })
  else if index == 2 then Some({ slots with operand2 = operand })
  else None()

function fp_operand_valid_bitmap(slots : Fp_operand_slots) -> bits(3) =
  (if slots.operand2.valid then 0b1 else 0b0)
  @ (if slots.operand1.valid then 0b1 else 0b0)
  @ (if slots.operand0.valid then 0b1 else 0b0)

function fp_operand_count_bitmap(count : int) -> option(bits(3)) =
  if count == 0 then Some(0b000)
  else if count == 1 then Some(0b001)
  else if count == 2 then Some(0b011)
  else if count == 3 then Some(0b111)
  else None()

function fp_operand_slots_valid(slots : Fp_operand_slots, count : int) -> bool =
  fp_operand_image_valid(slots.operand0)
  & fp_operand_image_valid(slots.operand1)
  & fp_operand_image_valid(slots.operand2)
  & (match fp_operand_count_bitmap(count) {
      Some(expected) => fp_operand_valid_bitmap(slots) == expected,
      None() => false,
    })

function fp_operand_slot_valid(operand : Fp_operand_image, used : bool) -> bool =
  fp_operand_image_valid(operand) & operand.valid == used

function fp_request_arity_valid(request : Fp_request_image) -> bool =
  request.operand_count >= 0 & request.operand_count <= 3
  & fp_operand_slot_valid(request.operand0, request.operand_count >= 1)
  & fp_operand_slot_valid(request.operand1, request.operand_count >= 2)
  & fp_operand_slot_valid(request.operand2, request.operand_count >= 3)

function fp_result_kind_width(kind : Fp_result_kind) -> int = match kind {
  FpResultBits32 => 4,
  FpResultPair32 => 4,
  FpResultBits64 => 8,
  FpResultRaw64 => 8,
  FpResultPair64 => 8,
  FpResultPairRaw64 => 8,
  _ => 0,
}

function fp_result_kind_is_pair(kind : Fp_result_kind) -> bool =
  kind == FpResultPair32 | kind == FpResultPair64 | kind == FpResultPairRaw64

function fp_result_kind_is_float(kind : Fp_result_kind) -> bool =
  kind == FpResultBits32 | kind == FpResultBits64
  | kind == FpResultPair32 | kind == FpResultPair64

function fp_fn_write_count(operands : list(Catalog_operand)) -> int = match operands {
  [||] => 0,
  operand :: tail =>
    (if operand.type_name == "Fn"
        & (operand.access == AccessWrite | operand.access == AccessReadWrite)
     then 1 else 0)
    + fp_fn_write_count(tail),
}

function fp_policy_result_kind(policy : Fp_result_policy,
                               operation : Semantic_operation) -> option(Fp_result_kind) =
  if operation == Op_FXCHG | operation == Op_FPOPP
  then Some(FpResultPairRaw64)
  else match policy {
    FpResultNone => Some(FpResultValueNone),
    FpResultFn32 => Some(FpResultBits32),
    FpResultMemory32 => Some(FpResultBits32),
    FpResultFn64 => Some(FpResultBits64),
    FpResultMemory64 => Some(FpResultBits64),
    FpResultRn64 => Some(FpResultInteger),
    FpResultFlags => Some(FpResultValueFlags),
    FpResultFlagsVOnly => Some(FpResultValueFlags),
    FpResultFnPair32 => Some(FpResultPair32),
    FpResultFnPair64 => Some(FpResultPair64),
    _ => None(),
  }

function fp_derive_result_kind(form : Catalog_entry,
                               width : int) -> option(Fp_result_kind) =
  match fp_form_result_policy(form, width) {
    Some(policy) => fp_policy_result_kind(policy, form.operation),
    None() => None(),
  }

function fp_derive_destination_kind(form : Catalog_entry) -> Fp_destination_kind =
  match fp_semantics(form.operation) {
    Some(semantics) =>
      if form.operation == Op_FXCHG | form.operation == Op_FPOPP
         | form.operation == Op_FSINCOSA
      then FpDestinationFnPair
      else if form.operation == Op_FPUSHP | fp_has_ea_write(form.operands)
      then FpDestinationMemory
      else if fp_has_rn_write(form.operands) then FpDestinationRn
      else
      if semantics.result_policy == FpResultFlags
         | semantics.result_policy == FpResultFlagsVOnly
      then FpDestinationFlags
      else if fp_fn_write_count(form.operands) > 0 then FpDestinationFn
      else FpDestinationNone,
    None() => FpDestinationNone,
  }

function fp_request_width(request : Fp_request_image) -> int = {
  let result_width = fp_result_kind_width(request.result_kind);
  if result_width != 0 then result_width
  else if request.operand_count > 0 then fp_operand_width(request.operand0)
  else 0
}

function fp_result_policy_matches(kind : Fp_result_kind, policy : Fp_result_policy,
                                  operation : Semantic_operation) -> bool =
  if operation == Op_FXCHG | operation == Op_FPOPP
  then kind == FpResultPairRaw64
  else match policy {
    FpResultNone => kind == FpResultValueNone,
    FpResultFn32 => kind == FpResultBits32,
    FpResultMemory32 => kind == FpResultBits32,
    FpResultFn64 => kind == FpResultBits64,
    FpResultMemory64 => kind == FpResultBits64,
    FpResultRn64 => kind == FpResultInteger,
    FpResultFlags => kind == FpResultValueFlags,
    FpResultFlagsVOnly => kind == FpResultValueFlags,
    FpResultFnPair32 => kind == FpResultPair32,
    FpResultFnPair64 => kind == FpResultPair64,
    _ => false,
  }

function fp_find_form(forms : list(Catalog_entry), form_id : string) -> option(Catalog_entry) =
  match forms {
    [||] => None(),
    form :: tail => if form.form_id == form_id then Some(form) else fp_find_form(tail, form_id),
  }

function fp_request_contract_valid(request : Fp_request_image,
                                   semantics : Fp_semantics) -> bool =
  if semantics.transcendental then
    request.contract_id == semantics.contract_id
    & fptrans_contract_operation(request.contract_id) == Some(request.operation)
    & fptrans_contract_word_valid(request.contract_word)
    & (request.allowed_causes & fflags_nx) == fflags_none
  else request.contract_id == 0x0000
       & request.contract_word == 0x0000000000000000

function fp_request_form_valid(request : Fp_request_image) -> bool =
  match fp_find_form(primary_form_catalog(), request.form_id) {
    None() => false,
    Some(form) => {
      let width = fp_request_width(request);
      form.operation == request.operation
      & (match fp_form_semantics(form, width) {
          Some(form_semantics) =>
            request.path == form_semantics.path
            & fp_result_policy_matches(request.result_kind,
                                       form_semantics.result_policy,
                                       request.operation),
          None() => false,
        })
    },
  }

function fp_request_valid(request : Fp_request_image) -> bool =
  request.valid & request.form_id != "" & fp_request_arity_valid(request)
  & (match fp_semantics(request.operation) {
      None() => false,
      Some(semantics) =>
        request.operand_count == semantics.source_count
        & request.allowed_causes == semantics.allowed_causes
        & request.flags_mask == semantics.flags_mask
        & request.transcendental == semantics.transcendental
        & fp_request_contract_valid(request, semantics)
        & fp_request_form_valid(request),
    })

function fp_prepare_request_operand(operation : Semantic_operation,
                                    operand : Fp_operand_image,
                                    daz : bool) -> Fp_operand_image =
  if fp_operation_is_exact_local(operation) then operand
  else fp_apply_daz(operand, daz)

function fp_build_request(operation : Semantic_operation, form : Catalog_entry,
                          path : Fp_path, result_kind : Fp_result_kind,
                          operands : Fp_operand_slots, fstatus : bits(64),
                          contract_word : bits(64)) -> option(Fp_request_image) =
  match fp_semantics(operation) {
    None() => None(),
    Some(semantics) => {
      let daz = fp_fstatus_daz(fstatus);
      let prepared : Fp_operand_slots = struct {
        operand0 = fp_prepare_request_operand(operation, operands.operand0, daz),
        operand1 = fp_prepare_request_operand(operation, operands.operand1, daz),
        operand2 = fp_prepare_request_operand(operation, operands.operand2, daz)
      };
      let request : Fp_request_image = struct {
        valid = true,
        operation = operation,
        form_id = form.form_id,
        path = path,
        result_kind = result_kind,
        operand_count = semantics.source_count,
        operand0 = prepared.operand0,
        operand1 = prepared.operand1,
        operand2 = prepared.operand2,
        rounding_mode = if semantics.transcendental then 0b00
                        else fp_fstatus_rounding_mode(fstatus),
        daz = daz,
        ftz = fp_fstatus_ftz(fstatus),
        dn = fp_fstatus_dn(fstatus),
        allowed_causes = semantics.allowed_causes,
        flags_mask = semantics.flags_mask,
        transcendental = semantics.transcendental,
        contract_id = semantics.contract_id,
        contract_word = contract_word
      };
      let metadata_valid = form.operation == operation
                           & fp_form_path(form) == Some(path)
                           & fp_derive_result_kind(form, fp_request_width(request))
                             == Some(result_kind);
      if fp_fstatus_valid(fstatus)
         & fp_operand_slots_valid(operands, semantics.source_count)
         & metadata_valid & fp_request_valid(request)
      then Some(request) else None()
    },
  }

function fp_result_primary_used(kind : Fp_result_kind) -> bool =
  kind != FpResultValueNone & kind != FpResultValueFlags

function fp_response_unused_valid(response : Fp_response_image) -> bool = {
  let primary_used = fp_result_primary_used(response.result_kind);
  let secondary_used = fp_result_kind_is_pair(response.result_kind);
  (primary_used | (response.primary == 0x0000000000000000
                   & response.primary_nan_origin == FpNotNan))
  & (secondary_used | (response.secondary == 0x0000000000000000
                       & response.secondary_nan_origin == FpNotNan))
}

function fp_response_upper_zero_valid(response : Fp_response_image) -> bool =
  if response.result_kind == FpResultBits32 then
    response.primary[63 .. 32] == 0x00000000
  else if response.result_kind == FpResultPair32 then
    response.primary[63 .. 32] == 0x00000000
    & response.secondary[63 .. 32] == 0x00000000
  else true

function fp_result_operand(kind : Fp_result_kind, bits : bits(64)) -> Fp_operand_image =
  struct {
    valid = true,
    kind = if kind == FpResultBits32 | kind == FpResultPair32
           then FpBits32 else FpBits64,
    bits = bits
  }

function fp_response_nan_origins_valid(request : Fp_request_image,
                                       response : Fp_response_image) -> bool =
  if fp_operation_is_exact_local(request.operation)
     | not_bool(fp_result_kind_is_float(response.result_kind)) then
    response.primary_nan_origin == FpNotNan
    & response.secondary_nan_origin == FpNotNan
  else {
    let primary = fp_result_operand(response.result_kind, response.primary);
    let primary_valid = fp_nan_origin_valid(request, primary,
                                            response.primary_nan_origin)
                        & fp_pre_dn_nan_payload_valid(request, primary);
    if fp_result_kind_is_pair(response.result_kind) then {
      let secondary = fp_result_operand(response.result_kind, response.secondary);
      primary_valid & fp_nan_origin_valid(request, secondary,
                                          response.secondary_nan_origin)
      & fp_pre_dn_nan_payload_valid(request, secondary)
    }
    else primary_valid & response.secondary_nan_origin == FpNotNan
  }

function fp_response_signaling_nan_valid(request : Fp_request_image,
                                         response : Fp_response_image) -> bool =
  fp_operation_is_exact_local(request.operation)
  | not_bool(fp_request_has_signaling_nan(request))
  | (response.generated_causes & fflags_nv) == fflags_nv

function fp_result_requires_accuracy(value : bits(64), width : int) -> bool =
  match fp_classify_raw(value, width) {
    Some(FpInfinity) => false,
    Some(FpQuietNan) => false,
    Some(FpSignalingNan) => false,
    Some(_) => true,
    None() => false,
  }

function fp_response_accuracy_valid(request : Fp_request_image,
                                    response : Fp_response_image) -> bool =
  if not_bool(request.transcendental) then
    response.accuracy_mask == 0b00
    & response.error0_q8_8_up == 0x0000
    & response.error1_q8_8_up == 0x0000
  else {
    let width = fp_result_kind_width(response.result_kind);
    match fptrans_selected_bound(request.contract_word, width) {
      None() => false,
      Some(bound) => {
        let primary_required = fp_result_requires_accuracy(response.primary, width);
        let secondary_used = fp_result_kind_is_pair(response.result_kind);
        let secondary_required = secondary_used
                                 & fp_result_requires_accuracy(response.secondary, width);
        let expected_mask : bits(2) =
          (if secondary_required then 0b10 else 0b00)
          | (if primary_required then 0b01 else 0b00);
        let error0_valid : bool =
          if primary_required then
            unsigned(response.error0_q8_8_up) <= unsigned(bound)
          else (response.error0_q8_8_up == 0x0000);
        let error1_valid : bool =
          if secondary_required then
            unsigned(response.error1_q8_8_up) <= unsigned(bound)
          else (response.error1_q8_8_up == 0x0000);
        response.accuracy_mask == expected_mask
        & error0_valid & error1_valid
      },
    }
  }

function fp_response_valid(request : Fp_request_image,
                           response : Fp_response_image) -> bool =
  fp_request_valid(request) & response.valid & response.echo == request
  & response.result_kind == request.result_kind
  & response.flags_mask == request.flags_mask
  & (response.flags_value & response.flags_mask) == response.flags_value
  & (response.generated_causes & request.allowed_causes) == response.generated_causes
  & (not_bool(request.transcendental)
     | (response.generated_causes & fflags_nx) == fflags_none)
  & fp_response_unused_valid(response)
  & fp_response_upper_zero_valid(response)
  & fp_response_nan_origins_valid(request, response)
  & fp_response_signaling_nan_valid(request, response)
  & fp_response_accuracy_valid(request, response)

function fp_local_pre_dn_values(request : Fp_request_image,
                                selector : bits(64)) -> option(Fp_exchange_result) = {
  let width = fp_request_width(request);
  if request.operation == Op_FABS then match fp_bitwise_fabs(request.operand0.bits, width) {
    Some(value) => Some(struct { lhs = value, rhs = 0x0000000000000000 }),
    None() => None(),
  }
  else if request.operation == Op_FNEG then match fp_bitwise_fneg(request.operand0.bits, width) {
    Some(value) => Some(struct { lhs = value, rhs = 0x0000000000000000 }),
    None() => None(),
  }
  else if request.operation == Op_FCOPYSIGN then
    match fp_bitwise_fcopysign(request.operand0.bits, request.operand1.bits, width) {
      Some(value) => Some(struct { lhs = value, rhs = 0x0000000000000000 }),
      None() => None(),
    }
  else if request.operation == Op_FMOV | request.operation == Op_FMOVcc then
    match fp_bitwise_fmov(request.operand0.bits, width) {
      Some(value) => Some(struct { lhs = value, rhs = 0x0000000000000000 }),
      None() => None(),
    }
  else if request.operation == Op_FCLR then
    Some(struct { lhs = fp_bitwise_fclr(), rhs = 0x0000000000000000 })
  else if request.operation == Op_FXCHG then
    Some(fp_bitwise_fxchg(request.operand0.bits, request.operand1.bits))
  else if request.operation == Op_FCLASS then match fp_fclass(request.operand0.bits, width) {
    Some(value) => Some(struct { lhs = value, rhs = 0x0000000000000000 }),
    None() => None(),
  }
  else if request.operation == Op_FMOVCR then match fp_fmovcr(selector[15 .. 0]) {
    Some(value) => Some(struct { lhs = value, rhs = 0x0000000000000000 }),
    None() => None(),
  }
  else None()
}

function fp_local_response(request : Fp_request_image,
                           selector : bits(64)) -> option(Fp_response_image) =
  match fp_local_pre_dn_values(request, selector) {
    None() => None(),
    Some(values) => {
      let response : Fp_response_image = struct {
        valid = true,
        echo = request,
        result_kind = request.result_kind,
        primary = values.lhs,
        secondary = values.rhs,
        primary_nan_origin = FpNotNan,
        secondary_nan_origin = FpNotNan,
        flags_mask = request.flags_mask,
        flags_value = fp_flags_none,
        generated_causes = fflags_none,
        accuracy_mask = 0b00,
        error0_q8_8_up = 0x0000,
        error1_q8_8_up = 0x0000
      };
      if fp_response_valid(request, response) then Some(response) else None()
    },
  }

struct Fp_final_values = {
  primary : bits(64),
  secondary : bits(64),
  generated_causes : bits(5),
}

struct Fp_candidate_result = {
  shape_valid : bool,
  result_kind : Fp_result_kind,
  primary : bits(64),
  secondary : bits(64),
  flags_mask : bits(4),
  flags_value : bits(4),
  generated_causes : bits(5),
  trap : bool,
  trap_errors : bits(5),
}

function empty_fp_candidate_result() -> Fp_candidate_result = struct {
  shape_valid = false,
  result_kind = FpResultValueNone,
  primary = 0x0000000000000000,
  secondary = 0x0000000000000000,
  flags_mask = fp_flags_none,
  flags_value = fp_flags_none,
  generated_causes = fflags_none,
  trap = false,
  trap_errors = fflags_none
}

function fp_request_fstatus_matches(request : Fp_request_image,
                                    fstatus : bits(64)) -> bool =
  fp_fstatus_valid(fstatus)
  & request.daz == fp_fstatus_daz(fstatus)
  & request.ftz == fp_fstatus_ftz(fstatus)
  & request.dn == fp_fstatus_dn(fstatus)
  & request.rounding_mode == (if request.transcendental then 0b00
                              else fp_fstatus_rounding_mode(fstatus))

function fp_postprocess_response_values(request : Fp_request_image,
                                        response : Fp_response_image)
  -> Fp_final_values =
  if fp_operation_is_exact_local(request.operation)
     | not_bool(fp_result_kind_is_float(response.result_kind)) then struct {
    primary = response.primary,
    secondary = response.secondary,
    generated_causes = response.generated_causes
  }
  else {
    let primary = fp_postprocess_pre_dn_response(
      fp_result_operand(response.result_kind, response.primary), request,
      response.generated_causes
    );
    if fp_result_kind_is_pair(response.result_kind) then {
      let secondary = fp_postprocess_pre_dn_response(
        fp_result_operand(response.result_kind, response.secondary), request,
        primary.generated_causes
      );
      struct {
        primary = primary.value.bits,
        secondary = secondary.value.bits,
        generated_causes = secondary.generated_causes
      }
    }
    else struct {
      primary = primary.value.bits,
      secondary = response.secondary,
      generated_causes = primary.generated_causes
    }
  }

function fp_finalize_response(request : Fp_request_image,
                              response : Fp_response_image,
                              fstatus : bits(64)) -> Fp_candidate_result =
  if not_bool(fp_request_fstatus_matches(request, fstatus)
              & fp_response_valid(request, response)) then
    empty_fp_candidate_result()
  else {
    let final_values = fp_postprocess_response_values(request, response);
    let enabled_errors = fp_enabled_causes(fstatus, final_values.generated_causes);
    struct {
      shape_valid = true,
      result_kind = response.result_kind,
      primary = final_values.primary,
      secondary = final_values.secondary,
      flags_mask = response.flags_mask,
      flags_value = response.flags_value,
      generated_causes = final_values.generated_causes,
      trap = enabled_errors != fflags_none,
      trap_errors = final_values.generated_causes
    }
  }
