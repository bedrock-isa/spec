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
  match fp_test_build_request("medium.fmovcr_x_imm16_fn_d", 8,
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

