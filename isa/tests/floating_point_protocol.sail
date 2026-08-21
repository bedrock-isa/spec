function test_fptrans_contract() -> unit = {
  let contract_word : bits(64) = 0x8000000101000100;
  let fstatus = fp_make_fstatus(0b11, false, false, false, fflags_all);
  let slots = fp_test_slots1(fp_test_operand32(0x000000003F800000));
  match fp_test_build_request("long.fsincosa_x_fn_s_fn_d_fn_c", 4,
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
  assert(fp_test_build_request("long.fsincosa_x_fn_s_fn_d_fn_c", 4,
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

function fp_test_representative_bytes(form_id : string,
                                      records : list(Representative_record))
  -> option(list(bits(8))) =
  match records {
    [||] => None(),
    record :: tail => if record.form_id == form_id then Some(record.bytes)
                      else fp_test_representative_bytes(form_id, tail),
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
  match fp_test_representative_bytes(
          "medium.fabs_x_fn_s_fn_d", representative_form_records()
        ) {
    None() => assert(false),
    Some(bytes) => match decode_full_record(bytes) {
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
