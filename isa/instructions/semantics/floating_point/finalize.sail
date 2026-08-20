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
