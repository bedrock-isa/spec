function fp_test_operand32(value : bits(64)) -> Fp_operand_image = struct {
  valid = true, kind = FpBits32, bits = value & 0x00000000FFFFFFFF
}

function fp_test_operand64(value : bits(64)) -> Fp_operand_image = struct {
  valid = true, kind = FpBits64, bits = value
}

function fp_test_raw64(value : bits(64)) -> Fp_operand_image = struct {
  valid = true, kind = FpRaw64, bits = value
}

function fp_test_slots1(first : Fp_operand_image) -> Fp_operand_slots = struct {
  operand0 = first,
  operand1 = empty_fp_operand(),
  operand2 = empty_fp_operand()
}

function fp_test_slots2(first : Fp_operand_image,
                        second : Fp_operand_image) -> Fp_operand_slots = struct {
  operand0 = first,
  operand1 = second,
  operand2 = empty_fp_operand()
}

function fp_test_slots3(first : Fp_operand_image, second : Fp_operand_image,
                        third : Fp_operand_image) -> Fp_operand_slots = struct {
  operand0 = first,
  operand1 = second,
  operand2 = third
}

function fp_test_form_width(form : Catalog_entry) -> int =
  if form.operation == Op_FCLR | form.operation == Op_FMOVCR
     | form.operation == Op_FXCHG | form.operation == Op_FPOPP
     | form.operation == Op_FPUSHP
  then 8 else 4

function fp_test_derived_form_count(forms : list(Catalog_entry)) -> int = match forms {
  [||] => 0,
  form :: tail => match fp_semantics(form.operation) {
    None() => fp_test_derived_form_count(tail),
    Some(_) => {
      let width = fp_test_form_width(form);
      assert(fp_form_path(form) != None());
      assert(fp_derive_result_kind(form, width) != None());
      assert(fp_derive_destination_kind(form) != FpDestinationNone);
      1 + fp_test_derived_form_count(tail)
    },
  },
}

function fp_test_build_request(form_id : string, width : int,
                               operands : Fp_operand_slots, fstatus : bits(64),
                               contract_word : bits(64)) -> option(Fp_request_image) =
  match fp_find_form(primary_form_catalog(), form_id) {
    None() => None(),
    Some(form) => match (fp_form_path(form), fp_derive_result_kind(form, width)) {
      (Some(path), Some(result_kind)) => fp_build_request(
        form.operation, form, path, result_kind, width, operands, fstatus, contract_word
      ),
      _ => None(),
    },
  }

function fp_test_response(request : Fp_request_image, primary : bits(64),
                          secondary : bits(64), primary_origin : Fp_nan_origin,
                          secondary_origin : Fp_nan_origin, causes : bits(5),
                          accuracy_mask : bits(2), error0 : bits(16),
                          error1 : bits(16)) -> Fp_response_image = struct {
  valid = true,
  echo = request,
  result_kind = request.result_kind,
  primary = primary,
  secondary = secondary,
  primary_nan_origin = primary_origin,
  secondary_nan_origin = secondary_origin,
  flags_mask = request.flags_mask,
  flags_value = fp_flags_none,
  generated_causes = causes,
  accuracy_mask = accuracy_mask,
  error0_q8_8_up = error0,
  error1_q8_8_up = error1
}
