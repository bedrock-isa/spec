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
        form.operation, form, path, result_kind, operands, fstatus, contract_word
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

function test_fp_metadata() -> unit = {
  assert(fp_operation_count(all_semantic_operations()) == 60);
  assert(fp_form_count(primary_form_catalog()) == 115);
  assert(fp_path_count(primary_form_catalog(), FpPathR) == 62);
  assert(fp_path_count(primary_form_catalog(), FpPathS1) == 36);
  assert(fp_path_count(primary_form_catalog(), FpPathS2) == 4);
  assert(fp_path_count(primary_form_catalog(), FpPathD1) == 11);
  assert(fp_path_count(primary_form_catalog(), FpPathStack) == 2);
  assert(fp_test_derived_form_count(primary_form_catalog()) == 115);

  match fp_find_form(primary_form_catalog(), "long.fclass_x_fn_s_rn_d") {
    Some(form) => {
      assert(fp_derive_result_kind(form, 4) == Some(FpResultInteger));
      assert(fp_derive_destination_kind(form) == FpDestinationRn)
    },
    None() => assert(false),
  };
  match fp_find_form(primary_form_catalog(),
                     "extralong.fsincosa_x_fn_s_fn_d_fn_c") {
    Some(form) => {
      assert(fp_derive_result_kind(form, 4) == Some(FpResultPair32));
      assert(fp_derive_result_kind(form, 8) == Some(FpResultPair64));
      assert(fp_derive_destination_kind(form) == FpDestinationFnPair)
    },
    None() => assert(false),
  };
  match fp_find_form(primary_form_catalog(), "medium.fxchg_fn_l_fn_r") {
    Some(form) => {
      assert(fp_derive_result_kind(form, 8) == Some(FpResultPairRaw64));
      assert(fp_derive_destination_kind(form) == FpDestinationFnPair)
    },
    None() => assert(false),
  }
}

function test_fp_operand_slots() -> unit = {
  let first = fp_test_operand32(0x000000003F800000);
  let second = fp_test_operand64(0x4000000000000000);
  let third = fp_test_raw64(0x1122334455667788);
  let empty = empty_fp_operand_slots();
  assert(fp_operand_valid_bitmap(empty) == 0b000);
  assert(fp_operand_slots_valid(empty, 0));
  match fp_operand_slot_set(empty, 0, first) {
    None() => assert(false),
    Some(one) => {
      assert(fp_operand_valid_bitmap(one) == 0b001);
      assert(fp_operand_slots_valid(one, 1));
      assert(fp_operand_slot_get(one, 0) == Some(first));
      match fp_operand_slot_set(one, 1, second) {
        None() => assert(false),
        Some(two) => {
          assert(fp_operand_valid_bitmap(two) == 0b011);
          assert(fp_operand_slots_valid(two, 2));
          match fp_operand_slot_set(two, 2, third) {
            Some(three) => {
              assert(fp_operand_valid_bitmap(three) == 0b111);
              assert(fp_operand_slots_valid(three, 3));
              assert(fp_operand_slot_get(three, 2) == Some(third))
            },
            None() => assert(false),
          }
        },
      }
    },
  };
  let hole : Fp_operand_slots = struct {
    operand0 = empty_fp_operand(), operand1 = second,
    operand2 = empty_fp_operand()
  };
  assert(fp_operand_valid_bitmap(hole) == 0b010);
  assert(not_bool(fp_operand_slots_valid(hole, 1)));
  assert(fp_operand_slot_get(empty, 3) == None());
  assert(fp_operand_slot_set(empty, -1, first) == None())
}

function test_fp_environment() -> unit = {
  let s_positive_subnormal = fp_test_operand32(0x0000000000000001);
  let s_negative_subnormal = fp_test_operand32(0x0000000080000001);
  let d_positive_subnormal = fp_test_operand64(0x0000000000000001);
  let d_negative_subnormal = fp_test_operand64(0x8000000000000001);
  assert(fp_apply_daz(s_positive_subnormal, true).bits == 0x0000000000000000);
  assert(fp_apply_daz(s_negative_subnormal, true).bits == 0x0000000080000000);
  assert(fp_apply_daz(d_positive_subnormal, true).bits == 0x0000000000000000);
  assert(fp_apply_daz(d_negative_subnormal, true).bits == 0x8000000000000000);
  assert(fp_apply_daz(s_positive_subnormal, false) == s_positive_subnormal);

  assert(fp_apply_dn(fp_test_operand32(0x000000007FC12345), true).bits
         == 0x000000007FC00000);
  assert(fp_apply_dn(fp_test_operand64(0xFFF8000000001234), true).bits
         == 0x7FF8000000000000);
  assert(fp_apply_dn(fp_test_operand32(0x000000007F812345), false).bits
         == 0x000000007FC12345);
  assert(fp_apply_dn(fp_test_operand64(0xFFF0000000001234), false).bits
         == 0xFFF8000000001234);

  let ordinary_s = fp_apply_ftz(s_negative_subnormal, true, false, fflags_nv);
  assert(ordinary_s.value.bits == 0x0000000080000000);
  assert(ordinary_s.generated_causes == (fflags_nv | fflags_uf | fflags_nx));
  let ordinary_d = fp_apply_ftz(d_positive_subnormal, true, false, fflags_none);
  assert(ordinary_d.value.bits == 0x0000000000000000);
  assert(ordinary_d.generated_causes == (fflags_uf | fflags_nx));
  let trans = fp_apply_ftz(s_positive_subnormal, true, true, fflags_dz);
  assert(trans.generated_causes == (fflags_dz | fflags_uf));
  assert((trans.generated_causes & fflags_nx) == fflags_none)
}

function fp_test_nan_request(first : Fp_operand_image, second : Fp_operand_image,
                             third : Fp_operand_image, count : int) -> Fp_request_image =
  { empty_fp_request() with valid = true, operation = Op_FMADD,
    operand_count = count, operand0 = first, operand1 = second, operand2 = third }

function test_fp_nan_order() -> unit = {
  let qnan0 = fp_test_operand64(0x7FF8000000000011);
  let snan1 = fp_test_operand64(0xFFF0000000000022);
  let snan2 = fp_test_operand64(0x7FF0000000000033);
  let request = fp_test_nan_request(qnan0, snan1, snan2, 3);
  assert(fp_source_nan_origin(request) == Some(FpNanOperand1));
  assert(fp_nan_source(request) == Some(snan1));
  assert(fp_expected_pre_dn_nan(request, 8) == Some(0xFFF8000000000022));
  assert(fp_expected_pre_dn_nan(request, 4) == Some(0x00000000FFC00000));

  let first_snan = fp_test_nan_request(snan2, snan1, qnan0, 3);
  assert(fp_source_nan_origin(first_snan) == Some(FpNanOperand0));
  assert(fp_expected_pre_dn_nan(first_snan, 8) == Some(0x7FF8000000000033));

  let qnan_only = fp_test_nan_request(qnan0, fp_test_operand64(0x3FF0000000000000),
                                      empty_fp_operand(), 2);
  assert(fp_source_nan_origin(qnan_only) == Some(FpNanOperand0));
  assert(fp_expected_pre_dn_nan(qnan_only, 8) == Some(qnan0.bits));

  let generated = fp_test_nan_request(fp_test_operand64(0x3FF0000000000000),
                                      empty_fp_operand(), empty_fp_operand(), 1);
  assert(fp_source_nan_origin(generated) == None());
  assert(fp_expected_pre_dn_nan(generated, 4) == Some(0x000000007FC00000));
  assert(fp_expected_pre_dn_nan(generated, 8) == Some(0x7FF8000000000000))
}

function test_fp_exact_local_bits() -> unit = {
  assert(fp_bitwise_fabs(0x00000000FFC00001, 4) == Some(0x000000007FC00001));
  assert(fp_bitwise_fabs(0xBFF0000000000000, 8) == Some(0x3FF0000000000000));
  assert(fp_bitwise_fneg(0x000000003F800000, 4) == Some(0x00000000BF800000));
  assert(fp_bitwise_fneg(0xBFF0000000000000, 8) == Some(0x3FF0000000000000));
  assert(fp_bitwise_fcopysign(0x8000000000000000, 0x3FF0000000000000, 8)
         == Some(0xBFF0000000000000));
  assert(fp_bitwise_fcopysign(0x0000000080000000, 0x000000003F800000, 4)
         == Some(0x00000000BF800000));
  assert(fp_bitwise_fmov(0xFFFFFFFF3F800000, 4) == Some(0x000000003F800000));
  assert(fp_bitwise_fmov(0x1122334455667788, 8) == Some(0x1122334455667788));
  assert(fp_bitwise_fclr() == 0x0000000000000000);
  let exchanged = fp_bitwise_fxchg(0x1111111111111111, 0x2222222222222222);
  assert(exchanged.lhs == 0x2222222222222222);
  assert(exchanged.rhs == 0x1111111111111111);

  assert(fp_fclass(0xFFF0000000000000, 8) == Some(0x0000000000000001));
  assert(fp_fclass(0xBFF0000000000000, 8) == Some(0x0000000000000002));
  assert(fp_fclass(0x8000000000000001, 8) == Some(0x0000000000000004));
  assert(fp_fclass(0x8000000000000000, 8) == Some(0x0000000000000008));
  assert(fp_fclass(0x0000000000000000, 8) == Some(0x0000000000000010));
  assert(fp_fclass(0x0000000000000001, 8) == Some(0x0000000000000020));
  assert(fp_fclass(0x3FF0000000000000, 8) == Some(0x0000000000000040));
  assert(fp_fclass(0x7FF0000000000000, 8) == Some(0x0000000000000080));
  assert(fp_fclass(0x7FF0000000000001, 8) == Some(0x0000000000000100));
  assert(fp_fclass(0x7FF8000000000000, 8) == Some(0x0000000000000200));
  assert(fp_fclass(0x00000000FF800001, 4) == Some(0x0000000000000100));

  assert(fp_fmovcr(0x0000) == Some(0x0000000000000000));
  assert(fp_fmovcr(0x0010) == Some(0x400921FB54442D18));
  assert(fp_fmovcr(0x0104) == Some(0x7FF0000000000001));
  assert(fp_fmovcr(0x0118) == Some(0x800FFFFFFFFFFFFF));
  assert(fp_fmovcr(0xFFFF) == None())
}

function test_fp_local_response() -> unit = {
  let ordinary = fp_make_fstatus(0b11, true, true, true, fflags_all);
  match fp_test_build_request("medium.fabs_x_fn_s_fn_d", 4,
                              fp_test_slots1(fp_test_operand32(0x00000000FFC00001)),
                              ordinary, 0x0000000000000000) {
    None() => assert(false),
    Some(request) => match fp_local_response(request, 0x0000000000000000) {
      Some(response) => {
        assert(response.primary == 0x000000007FC00001);
        assert(response.generated_causes == fflags_none);
        assert(response.primary_nan_origin == FpNotNan);
        let candidate = fp_finalize_response(request, response, ordinary);
        assert(candidate.shape_valid);
        assert(candidate.primary == 0x000000007FC00001);
        assert(candidate.generated_causes == fflags_none)
      },
      None() => assert(false),
    },
  };
  match fp_test_build_request("medium.fxchg_fn_l_fn_r", 8,
                              fp_test_slots2(fp_test_operand64(0x1111111111111111),
                                             fp_test_operand64(0x2222222222222222)),
                              ordinary, 0x0000000000000000) {
    Some(request) => match fp_local_response(request, 0x0000000000000000) {
      Some(response) => {
        assert(response.result_kind == FpResultPairRaw64);
        assert(response.primary == 0x2222222222222222);
        assert(response.secondary == 0x1111111111111111)
      },
      None() => assert(false),
    },
    None() => assert(false),
  };
  match fp_test_build_request("long.fmovcr_x_imm16_fn_d", 8,
                              empty_fp_operand_slots(), ordinary,
                              0x0000000000000000) {
    Some(request) => match fp_local_response(request, 0x0000000000000010) {
      Some(response) => assert(response.primary == 0x400921FB54442D18),
      None() => assert(false),
    },
    None() => assert(false),
  }
}

function test_fp_response_validation() -> unit = {
  let fstatus = fp_make_fstatus(0b10, false, false, false, fflags_none);
  let slots = fp_test_slots2(fp_test_operand32(0x000000003F800000),
                             fp_test_operand32(0x0000000040000000));
  match fp_test_build_request("medium.fadd_x_fn_s_fn_d", 4, slots, fstatus,
                              0x0000000000000000) {
    None() => assert(false),
    Some(request) => {
      let valid = fp_test_response(request, 0x0000000040400000,
                                   0x0000000000000000, FpNotNan, FpNotNan,
                                   fflags_none, 0b00, 0x0000, 0x0000);
      assert(fp_response_valid(request, valid));
      assert(not_bool(fp_response_valid(
        request, { valid with echo = empty_fp_request() }
      )));
      assert(not_bool(fp_response_valid(
        request, { valid with primary = 0xFFFFFFFF40400000 }
      )));
      assert(not_bool(fp_response_valid(
        request, { valid with generated_causes = fflags_dz }
      )));
      assert(not_bool(fp_response_valid(
        request, { valid with flags_mask = fp_flags_all }
      )))
    },
  };

  let nan_slots = fp_test_slots2(fp_test_operand32(0x000000007FC00011),
                                 fp_test_operand32(0x000000007F800022));
  match fp_test_build_request("medium.fadd_x_fn_s_fn_d", 4, nan_slots, fstatus,
                              0x0000000000000000) {
    None() => assert(false),
    Some(request) => {
      assert(fp_source_nan_origin(request) == Some(FpNanOperand1));
      let valid_nan = fp_test_response(request, 0x000000007FC00022,
                                       0x0000000000000000, FpNanOperand1, FpNotNan,
                                       fflags_nv, 0b00, 0x0000, 0x0000);
      assert(fp_response_valid(request, valid_nan));
      assert(not_bool(fp_response_valid(
        request, { valid_nan with generated_causes = fflags_none }
      )));
      assert(not_bool(fp_response_valid(
        request, { valid_nan with primary = 0x000000007FC00011,
                                  primary_nan_origin = FpNanOperand0 }
      )))
    },
  }
}

function test_fp_finalize_trap_and_dn() -> unit = {
  let trap_status = fp_make_fstatus(0b00, true, false, false, fflags_nv);
  let slots = fp_test_slots2(fp_test_operand32(0x000000003F800000),
                             fp_test_operand32(0x00000000BF800000));
  match fp_test_build_request("medium.fadd_x_fn_s_fn_d", 4, slots, trap_status,
                              0x0000000000000000) {
    None() => assert(false),
    Some(request) => {
      let response = fp_test_response(request, 0x0000000000000001,
                                      0x0000000000000000, FpNotNan, FpNotNan,
                                      fflags_nv, 0b00, 0x0000, 0x0000);
      let candidate = fp_finalize_response(request, response, trap_status);
      assert(candidate.shape_valid);
      assert(candidate.primary == 0x0000000000000000);
      assert(candidate.generated_causes == (fflags_nv | fflags_uf | fflags_nx));
      assert(candidate.trap);
      assert(candidate.trap_errors == (fflags_nv | fflags_uf | fflags_nx))
    },
  };

  let dn_status = fp_make_fstatus(0b00, false, false, true, fflags_none);
  let nan_slots = fp_test_slots2(fp_test_operand64(0xFFF8000000000042),
                                 fp_test_operand64(0x3FF0000000000000));
  match fp_test_build_request("medium.fadd_x_fn_s_fn_d", 8, nan_slots, dn_status,
                              0x0000000000000000) {
    None() => assert(false),
    Some(request) => {
      let response = fp_test_response(request, 0xFFF8000000000042,
                                      0x0000000000000000, FpNanOperand0, FpNotNan,
                                      fflags_none, 0b00, 0x0000, 0x0000);
      let candidate = fp_finalize_response(request, response, dn_status);
      assert(candidate.shape_valid);
      assert(candidate.primary == 0x7FF8000000000000);
      assert(not_bool(candidate.trap))
    },
  }
}

function test_fptrans_contract() -> unit = {
  let contract_word : bits(64) = 0x8000000101000100;
  let fstatus = fp_make_fstatus(0b11, false, false, false, fflags_all);
  let slots = fp_test_slots1(fp_test_operand32(0x000000003F800000));
  match fp_test_build_request("extralong.fsincosa_x_fn_s_fn_d_fn_c", 4,
                              slots, fstatus, contract_word) {
    None() => assert(false),
    Some(request) => {
      assert(request.transcendental);
      assert(request.rounding_mode == 0b00);
      assert(request.contract_id == 0x0004);
      assert(request.result_kind == FpResultPair32);
      let response = fp_test_response(request, 0x000000003F576AA4,
                                      0x000000003F0A5140, FpNotNan, FpNotNan,
                                      fflags_none, 0b11, 0x0100, 0x00FF);
      assert(fp_response_valid(request, response));
      assert(fp_finalize_response(request, response, fstatus).shape_valid);
      assert(not_bool(fp_response_valid(
        request, { response with generated_causes = fflags_nx }
      )));
      assert(not_bool(fp_response_valid(
        request, { response with error0_q8_8_up = 0x0101 }
      )));
      assert(not_bool(fp_response_valid(
        request, { response with accuracy_mask = 0b01,
                                  error1_q8_8_up = 0x0000 }
      )))
    },
  };
  assert(fp_test_build_request("extralong.fsincosa_x_fn_s_fn_d_fn_c", 4,
                               slots, fstatus, 0x0000000000000000) == None())
}

function fp_test_pair_mapping(pair_id : int) -> unit =
  if pair_id >= 8 then ()
  else {
    let encoded = get_slice_int(3, pair_id, 0);
    assert(unsigned(fpair_low(encoded)) == pair_id * 2);
    assert(unsigned(fpair_high(encoded)) == pair_id * 2 + 1);
    fp_test_pair_mapping(pair_id + 1)
  }

function test_fp_architecture_protocol_shape() -> unit = {
  let primitive = empty_primitive_request();
  assert(primitive.fp_request == empty_fp_request());
  let state = initial_cpu();
  let pending = empty_pending(state, state, Op_FADD, CommitNone);
  assert(pending.fp_pending == empty_fp_pending());
  assert(PhaseFpCompute != ContinuationNone);
  assert(ResponseFloatingPoint != ResponseRead)
}

function fp_test_fault_kind(result : Execution_result, kind : Fault_kind) -> bool =
  match result.fault {
    Some(fault) => fault.kind == kind,
    None() => false,
  }

function fp_test_fp_response(request : Fp_request_image, primary : bits(64),
                             secondary : bits(64), causes : bits(5),
                             accuracy_mask : bits(2), error0 : bits(16),
                             error1 : bits(16)) -> Transaction_response =
  { successful_response(ResponseFloatingPoint, 0x0000000000000000, true) with
    fp_response = fp_test_response(
      request, primary, secondary, FpNotNan, FpNotNan, causes,
      accuracy_mask, error0, error1
    ) }

function test_fp_architecture_local_commit() -> unit =
  match decode_full_record([|0xC2, 0x50, 0x30|]) {
    None() => assert(false),
    Some(instruction) => {
      assert(operation_width(instruction) == 4);
      var state = initial_cpu();
      state.fp_enabled = true;
      state.floating_registers[0] = 0xDEADBEEFBF800000;
      state.fstatus = fp_make_fstatus(0b11, true, true, true, fflags_all);
      let result = execute_full(instruction, state);
      assert(not_bool(result.awaiting_environment));
      assert(result.fault == None());
      assert(result.state.floating_registers[0] == 0x000000003F800000);
      assert(result.state.fflags == fflags_none);
      assert(result.state.pc == 0x0000000000000003)
    },
  }

function test_fp_architecture_compute_and_trap() -> unit =
  match decode_full_record([|0xC2, 0x48, 0x70|]) {
    None() => assert(false),
    Some(instruction) => {
      assert(operation_width(instruction) == 8);
      var state = initial_cpu();
      state.fp_enabled = true;
      state.floating_registers[0] = 0x3FF0000000000000;
      state.fstatus = fp_make_fstatus(0b00, false, false, false, fflags_none);
      let waiting = execute_full(instruction, state);
      assert(waiting.awaiting_environment);
      assert(waiting.pending.phase == PhaseFpCompute);
      assert(waiting.request.kind == FloatingPointRequest);
      assert(waiting.request.fp_request.valid);
      assert(waiting.request.fp_request.operation == Op_FADD);
      let done = resume_transaction(
        waiting, fp_test_fp_response(
          waiting.request.fp_request, 0x4000000000000000,
          0x0000000000000000, fflags_none, 0b00, 0x0000, 0x0000
        )
      );
      assert(not_bool(done.awaiting_environment));
      assert(done.fault == None());
      assert(done.state.floating_registers[0] == 0x4000000000000000);

      let wrong_echo = fp_test_fp_response(
        waiting.request.fp_request, 0x4000000000000000,
        0x0000000000000000, fflags_none, 0b00, 0x0000, 0x0000
      );
      let rejected = resume_transaction(
        waiting, { wrong_echo with fp_response = {
          wrong_echo.fp_response with echo = empty_fp_request()
        } }
      );
      assert(fp_test_fault_kind(rejected, InvalidControlState));
      assert(rejected.state == state);

      var trap_state = state;
      trap_state.fstatus = fp_make_fstatus(0b00, true, false, false, fflags_nv);
      let trap_waiting = execute_full(instruction, trap_state);
      assert(trap_waiting.pending.phase == PhaseFpCompute);
      let trapped = resume_transaction(
        trap_waiting, fp_test_fp_response(
          trap_waiting.request.fp_request, 0x0000000000000001,
          0x0000000000000000, fflags_nv | fflags_of,
          0b00, 0x0000, 0x0000
        )
      );
      assert(fp_test_fault_kind(trapped, FloatingPointFault));
      match trapped.fault {
        Some(fault) => assert(fault.error_code == 0x0000000000000017),
        None() => assert(false),
      };
      assert(trapped.state == trap_state)
    },
  }

function fp_test_contract_response(value : bits(64), known : bool,
                                   present : bool) -> Transaction_response =
  { successful_response(ResponseCpuidQuery, value, true) with
    known = known, present = present }

function test_fptrans_architecture_sequence() -> unit =
  match decode_full_record([|0xC7, 0xDC, 0x08, 0x40|]) {
    None() => assert(false),
    Some(instruction) => {
      var state = initial_cpu();
      state.fp_enabled = true;
      state.fptrans_enabled = true;
      state.floating_registers[0] = 0x000000003F800000;
      state.fstatus = fp_make_fstatus(0b11, false, false, false, fflags_all);
      let query = execute_full(instruction, state);
      assert(query.awaiting_environment);
      assert(query.pending.phase == PhaseFpContractQuery);
      assert(query.request.kind == CpuidQueryRequest);
      assert(query.request.selector == fptrans_cpuid_selector(0x0001));
      assert(query.state == state);

      let absent = resume_transaction(
        query, fp_test_contract_response(0x0000000000000000, true, false)
      );
      assert(fp_test_fault_kind(absent, IllegalInstruction));
      assert(absent.state == state);

      let present_zero = resume_transaction(
        query, fp_test_contract_response(0x0000000000000000, true, true)
      );
      assert(fp_test_fault_kind(present_zero, IllegalInstruction));
      assert(present_zero.state == state);

      let unknown = resume_transaction(
        query, fp_test_contract_response(0x0000000000000000, false, true)
      );
      assert(fp_test_fault_kind(unknown, IllegalInstruction));
      assert(unknown.state == state);

      let malformed = resume_transaction(
        query, fp_test_contract_response(0x8000000000000000, true, true)
      );
      assert(fp_test_fault_kind(malformed, InvalidControlState));
      assert(malformed.state == state);

      let contract_word : bits(64) = 0x8000000101000100;
      let compute = resume_transaction(
        query, fp_test_contract_response(contract_word, true, true)
      );
      assert(compute.awaiting_environment);
      assert(compute.pending.phase == PhaseFpCompute);
      assert(compute.request.kind == FloatingPointRequest);
      assert(compute.request.fp_request.operation == Op_FSINA);
      assert(compute.request.fp_request.contract_id == 0x0001);
      assert(compute.request.fp_request.contract_word == contract_word);
      assert(compute.request.fp_request.rounding_mode == 0b00);
      let finished = resume_transaction(
        compute, fp_test_fp_response(
          compute.request.fp_request, 0x000000003F576AA4,
          0x0000000000000000, fflags_none, 0b01, 0x0100, 0x0000
        )
      );
      assert(not_bool(finished.awaiting_environment));
      assert(finished.fault == None());
      assert(finished.state.floating_registers[0] == 0x000000003F576AA4)
    },
  }

function fp_test_conversion_request(bytes : list(bits(8)),
                                    expected_operation : Semantic_operation,
                                    expected_source : Fp_value_kind,
                                    expected_result : Fp_result_kind) -> unit =
  match decode_full_record(bytes) {
    None() => assert(false),
    Some(instruction) => {
      var state = initial_cpu();
      state.fp_enabled = true;
      state.floating_registers[0] = 0x3FF000003F800000;
      let waiting = execute_full(instruction, state);
      assert(waiting.awaiting_environment);
      assert(waiting.pending.phase == PhaseFpCompute);
      assert(waiting.request.fp_request.operation == expected_operation);
      assert(waiting.request.fp_request.operand0.kind == expected_source);
      assert(waiting.request.fp_request.result_kind == expected_result)
    },
  }

function test_fp_conversion_width_protocol() -> unit = {
  fp_test_conversion_request(
    [|0xC7, 0xD7, 0x08, 0x20|], Op_FCVT, FpBits64, FpResultBits32
  );
  fp_test_conversion_request(
    [|0xC7, 0xD7, 0x88, 0x20|], Op_FCVT, FpBits32, FpResultBits64
  );
  fp_test_conversion_request(
    [|0xC7, 0xD7, 0x10, 0x20|], Op_FCVTU, FpBits64, FpResultBits32
  );
  fp_test_conversion_request(
    [|0xC7, 0xD7, 0x90, 0x20|], Op_FCVTU, FpBits32, FpResultBits64
  )
}

function test_fp_fmovcr_s_full_width() -> unit =
  match decode_full_record([|0xCF, 0xD6, 0x31, 0x00, 0x10, 0x00|]) {
    None() => assert(false),
    Some(instruction) => {
      var state = initial_cpu();
      state.fp_enabled = true;
      state.floating_registers[0] = 0xAAAAAAAAAAAAAAAA;
      let result = execute_full(instruction, state);
      assert(not_bool(result.awaiting_environment));
      assert(result.fault == None());
      assert(result.state.floating_registers[0] == 0x400921FB54442D18)
    },
  }

function test_fp_fmovcc_false_annul() -> unit =
  match decode_full_record([|0xC7, 0xDA, 0x08, 0x10|]) {
    None() => assert(false),
    Some(instruction) => {
      assert(instruction.form.operation == Op_FMOVcc);
      var state = initial_cpu();
      state.fp_enabled = true;
      state.fstatus = 0x8000000000000000;
      state.floating_registers[0] = 0x1122334455667788;
      let result = execute_full(instruction, state);
      assert(not_bool(result.awaiting_environment));
      assert(result.fault == None());
      assert(result.request.kind == NoPrimitiveRequest);
      assert(result.effects == [||]);
      assert(result.state.floating_registers == state.floating_registers);
      assert(result.state.fstatus == state.fstatus);
      assert(result.state.fflags == state.fflags);
      assert(not_bool(result.state.fp_component_modified));
      assert(result.state.pc == state.pc + 4)
    },
  }

function test_fsincosa_alias_precedes_fp_access() -> unit =
  match decode_full_record([|0xCB, 0xF0, 0x24, 0x00, 0x00|]) {
    None() => assert(false),
    Some(instruction) => {
      var state = initial_cpu();
      state.fp_enabled = false;
      state.fptrans_enabled = false;
      state.fstatus = 0x8000000000000000;
      let result = execute_full(instruction, state);
      assert(not_bool(result.awaiting_environment));
      assert(fp_test_fault_kind(result, IllegalInstruction));
      match result.fault {
        Some(fault) => assert(fault.error_code == 0x0000000000000006),
        None() => assert(false),
      };
      assert(result.request.kind == NoPrimitiveRequest);
      assert(result.state == state)
    },
  }

function test_fp_semantics() -> unit = {
  test_fp_metadata();
  test_fp_operand_slots();
  test_fp_environment();
  test_fp_nan_order();
  test_fp_exact_local_bits();
  test_fp_local_response();
  test_fp_response_validation();
  test_fp_finalize_trap_and_dn();
  test_fptrans_contract();
  fp_test_pair_mapping(0);
  test_fp_architecture_protocol_shape();
  test_fp_architecture_local_commit();
  test_fp_architecture_compute_and_trap();
  test_fptrans_architecture_sequence();
  test_fp_conversion_width_protocol();
  test_fp_fmovcr_s_full_width();
  test_fp_fmovcc_false_annul();
  test_fsincosa_alias_precedes_fp_access()
}
