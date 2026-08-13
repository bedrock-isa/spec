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

