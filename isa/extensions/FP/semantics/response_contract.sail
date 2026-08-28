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
  if fp_request_is_exact_local(request)
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
  fp_request_is_exact_local(request)
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
    match fp_approx_selected_bound(request.contract_word, width) {
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
     | (response.generated_causes & fflags_nx)
       == (response.generated_causes & fp_request_conversion_allowed_causes(request)
           & fflags_nx))
  & fp_response_unused_valid(response)
  & fp_response_upper_zero_valid(response)
  & fp_response_nan_origins_valid(request, response)
  & fp_response_signaling_nan_valid(request, response)
  & fp_response_accuracy_valid(request, response)

function fp_local_pre_dn_values(request : Fp_request_image,
                                selector : bits(64)) -> option(Fp_exchange_result) = {
  let width = fp_request_width(request);
  if request.operation == Op_FABS then match fp_exact_arithmetic(
    FpArithmeticAbsolute, request.operand0.bits, width
  ) {
    Some(value) => Some(struct { lhs = value, rhs = 0x0000000000000000 }),
    None() => None(),
  }
  else if request.operation == Op_FNEG then match fp_exact_arithmetic(
    FpArithmeticNegate, request.operand0.bits, width
  ) {
    Some(value) => Some(struct { lhs = value, rhs = 0x0000000000000000 }),
    None() => None(),
  }
  else if request.operation == Op_FCOPYSIGN then
    match fp_exact_data(
      FpDataCopySign, request.operand0.bits, request.operand1.bits, width
    ) {
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
  else if request.operation == Op_FCLASS then match fp_exact_data(
    FpDataClassify, request.operand0.bits, 0x0000000000000000, width
  ) {
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
  if not_bool(fp_request_is_exact_local(request)) then fp_primitive_response(request)
  else match fp_local_pre_dn_values(request, selector) {
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
