function test_vector_predicate_semantics() -> unit = {
  match decode_full_record([|0xC7, 0xE9, 0xC4, 0x03|]) {
    Some(instruction) => {
      assert(instruction.form.operation == Op_PTRUE);
      let result = execute_full(instruction, initial_cpu());
      assert(result.fault == None());
      assert(result.state.predicate_registers[3] == [|0x55, 0x55|])
    },
    None() => assert(false),
  };

  match decode_full_record([|0xC7, 0xE9, 0x48, 0x24|]) {
    Some(instruction) => {
      var state = initial_cpu();
      state.registers[2] = 0x0000000000000002;
      let result = execute_full(instruction, state);
      assert(result.fault == None());
      assert(result.state.predicate_registers[4] == [|0x00, 0x11|])
    },
    None() => assert(false),
  };

  match decode_full_record([|0xCF, 0xFC, 0x0A, 0x80, 0x91, 0x80|]) {
    Some(instruction) => {
      assert(instruction.form.operation == Op_PLOOP);
      var state = initial_cpu();
      state.registers[1] = 0x0000000000000014;
      state.registers[2] = 0x0000000000000002;
      state.predicate_registers[3] = [|0xAA, 0x55|];
      let chunk = execute_full(instruction, state);
      assert(not_bool(chunk.awaiting_environment));
      assert(chunk.fault == None());
      assert(chunk.state.registers[1] == 0x0000000000000006);
      assert(chunk.state.registers[2] == 0x0000000000000000);
      assert(chunk.state.predicate_registers[3] == [|0xFC, 0xFF|]);

      state.registers[1] = 0x0000000000000001;
      state.registers[2] = 0x0000000000000010;
      let range = execute_full(instruction, state);
      assert(range.state == state);
      match range.fault {
        Some(fault) => {
          assert(fault.kind == VectorRangeFault);
          assert(fault.error_code == 0x0000000000000000)
        },
        None() => assert(false),
      }
    },
    None() => assert(false),
  }
}

function test_vector_integer_semantics() -> unit = {
  match decode_full_record([|0xCB, 0xF7, 0x80, 0x00, 0x00|]) {
    Some(instruction) => {
      assert(instruction.form.operation == Op_VADD);
      var state = initial_cpu();
      state.predicate_registers[0] = [|0x01, 0x00|];
      state.vector_registers[0] =
        [|0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08,
          0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F, 0x10|];
      let result = execute_full(instruction, state);
      assert(result.fault == None());
      assert(result.state.vector_registers[0] ==
        [|0x02, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08,
          0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F, 0x10|])
    },
    None() => assert(false),
  };

  assert(decode_full_record([|0xCB, 0xF4, 0x00, 0x00, 0x00|]) == None());
  assert(decode_full_record([|0xCB, 0xF5, 0x50, 0x00, 0x00|]) == None());

  match decode_full_record([|0xCB, 0xF4, 0x08, 0x00, 0x00|]) {
    Some(instruction) => {
      assert(instruction.form.operation == Op_VCMPcc);
      var state = initial_cpu();
      state.predicate_registers[0] = [|0x05, 0x80|];
      let result = execute_full(instruction, state);
      assert(result.fault == None());
      assert(result.state.predicate_registers[0] == [|0x05, 0x80|])
    },
    None() => assert(false),
  };

  match decode_full_record([|0xCB, 0xF7, 0x98, 0x40, 0x00|]) {
    Some(instruction) => {
      assert(instruction.form.operation == Op_VEXTZW);
      var state = initial_cpu();
      state.predicate_registers[0] = [|0x01, 0x00|];
      state.vector_registers[0] =
        [|0x80, 0xAA, 0x7F, 0xBB, 0x01, 0xCC, 0x02, 0xDD,
          0x03, 0xEE, 0x04, 0xFF, 0x05, 0x11, 0x06, 0x22|];
      let result = execute_full(instruction, state);
      assert(result.fault == None());
      assert(result.state.vector_registers[0] ==
        [|0x80, 0x00, 0x7F, 0xBB, 0x01, 0xCC, 0x02, 0xDD,
          0x03, 0xEE, 0x04, 0xFF, 0x05, 0x11, 0x06, 0x22|])
    },
    None() => assert(false),
  };

  match decode_full_record([|0xCB, 0xF7, 0xAC, 0x40, 0x00|]) {
    Some(instruction) => {
      assert(instruction.form.operation == Op_VPERM);
      var state = initial_cpu();
      state.predicate_registers[0] = [|0xFF, 0xFF|];
      state.vector_registers[0] =
        [|0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
          0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00|];
      let result = execute_full(instruction, state);
      assert(result.fault == None());
      assert(result.state.vector_registers[0] ==
        [|0x00, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01,
          0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01|])
    },
    None() => assert(false),
  };

  match decode_full_record([|0xCB, 0xF7, 0xE0, 0x00, 0x00|]) {
    Some(instruction) => {
      assert(instruction.form.operation == Op_VEXTRACT);
      var state = initial_cpu();
      state.registers[0] = 0x0000000000000010;
      let result = execute_full(instruction, state);
      assert(result.state == state);
      match result.fault {
        Some(fault) => {
          assert(fault.kind == VectorRangeFault);
          assert(fault.error_code == 0x0000000000000001)
        },
        None() => assert(false),
      }
    },
    None() => assert(false),
  }
}

function expect_vector_step_address(bytes : list(bits(8)), state : Cpu_state,
                                    lane : int, expected : bits(64)) -> unit =
  match decode_full_record(bytes) {
    None() => assert(false),
    Some(instruction) => match vector_step_address(
      instruction, state, lane, operation_width(instruction)
    ) {
      Some(address) => assert(address == expected), None() => assert(false),
    },
  }

function test_vector_lane_count_and_step_semantics() -> unit = {
  match decode_full_record([|0xC7, 0xE9, 0x88, 0x11|]) {
    None() => assert(false),
    Some(instruction) => {
      assert(instruction.form.operation == Op_VLCNT);
      var state = initial_cpu();
      state.flags = 0b1010;
      let result = execute_full(instruction, state);
      assert(result.fault == None());
      assert(result.state.registers[1] == 0x0000000000000004);
      assert(result.state.flags == 0b1010)
    },
  };

  match decode_full_record([|0xCB, 0xE9, 0x8C, 0x21, 0xFF|]) {
    None() => assert(false),
    Some(instruction) => {
      assert(instruction.form.operation == Op_VLCADD);
      var state = initial_cpu();
      state.registers[1] = 0x0000000000000001;
      state.flags = 0b0101;
      let result = execute_full(instruction, state);
      assert(result.fault == None());
      assert(result.state.registers[1] == 0xFFFFFFFFFFFFFFFF);
      assert(result.state.flags == 0b0101)
    },
  };

  var address_state = initial_cpu();
  address_state.registers[2] = 0x0000000000000002;
  address_state.registers[3] = 0x0000000000000100;
  address_state.registers[4] = 0xFFFFFFFFFFFFFFFD;
  expect_vector_step_address(
    [|0xCF, 0xFC, 0x10, 0x86, 0x04, 0x82|], address_state, 2,
    0x00000000000000FA
  );

  address_state.vector_registers[1] =
    [|0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
      0xFC, 0xFF, 0xFF, 0xFF, 0x00, 0x00, 0x00, 0x00|];
  expect_vector_step_address(
    [|0xCF, 0xFC, 0x11, 0x00, 0x08, 0x41|], address_state, 2,
    0x00000000FFFFFFFC
  );
  expect_vector_step_address(
    [|0xCF, 0xFC, 0x12, 0x8C, 0x08, 0x41|], address_state, 2,
    0x00000000000000FC
  );

  address_state.vector_registers[1] =
    [|0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
      0xF0, 0xDE, 0xBC, 0x9A, 0x78, 0x56, 0x34, 0x12|];
  expect_vector_step_address(
    [|0xCF, 0xFC, 0x11, 0x04, 0x04, 0x41|], address_state, 1,
    0x123456789ABCDEF0
  );

  address_state.vector_registers[1] =
    [|0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
      0x03, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00|];
  expect_vector_step_address(
    [|0xCF, 0xFC, 0x13, 0x8C, 0x08, 0x41|], address_state, 2,
    0x000000000000010C
  );
  expect_vector_step_address(
    [|0xD3, 0xFC, 0x14, 0x8C, 0x08, 0x41, 0xFE|], address_state, 2,
    0x000000000000010A
  );
  expect_vector_step_address(
    [|0xD7, 0xFC, 0x15, 0x8C, 0x08, 0x41, 0xFE, 0xFF|], address_state, 2,
    0x000000000000010A
  );
  expect_vector_step_address(
    [|0xDF, 0xFC, 0x16, 0x8C, 0x08, 0x41, 0xFE, 0xFF, 0xFF, 0xFF|],
    address_state, 2, 0x000000000000010A
  );
  expect_vector_step_address(
    [|0xEF, 0xFC, 0x17, 0x8C, 0x08, 0x41,
      0xFE, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF|],
    address_state, 2, 0x000000000000010A
  );

  match decode_full_record([|0xCF, 0xFC, 0x13, 0x8C, 0x08, 0x41|]) {
    None() => assert(false),
    Some(instruction) => {
      var state = address_state;
      state.predicate_registers[0] = [|0x00, 0x01|];
      state.vector_registers[2] =
        [|0xAA, 0xAA, 0xAA, 0xAA, 0xAA, 0xAA, 0xAA, 0xAA,
          0xAA, 0xAA, 0xAA, 0xAA, 0xAA, 0xAA, 0xAA, 0xAA|];
      state.flags = 0b1010;
      let started = execute_full(instruction, state);
      assert(started.awaiting_environment);
      assert(started.request.kind == VectorMemoryRead);
      assert(started.request.segment == 1);
      assert(started.request.range_start == 0x000000000000010C);
      assert(started.request.range_length == 4);
      assert(started.request.body_length == 4);
      assert(started.request.payload_bytes == [|0x01|]);
      let gathered = resume_transaction(
        started, response_bytes(ResponseVectorMemory, [|0x11, 0x22, 0x33, 0x44|])
      );
      assert(gathered.fault == None());
      assert(gathered.state.registers[2] == 0x0000000000000003);
      assert(gathered.state.vector_registers[2] ==
        [|0xAA, 0xAA, 0xAA, 0xAA, 0xAA, 0xAA, 0xAA, 0xAA,
          0x11, 0x22, 0x33, 0x44, 0xAA, 0xAA, 0xAA, 0xAA|]);
      assert(gathered.state.flags == 0b1010);
      let failed = resume_transaction(started, failing_response(ResponseVectorMemory));
      assert(failed.state == state);

      var inactive = state;
      inactive.registers[2] = 0x0000000000000001;
      inactive.predicate_registers[0] = [|0x00, 0x00|];
      let annulled = execute_full(instruction, inactive);
      assert(not_bool(annulled.awaiting_environment));
      assert(annulled.fault == None());
      assert(annulled.state.registers[2] == 0x0000000000000002);
      assert(annulled.state.vector_registers[2] == inactive.vector_registers[2]);

      var out_of_range = inactive;
      out_of_range.registers[2] = 0x0000000000000004;
      let ranged = execute_full(instruction, out_of_range);
      assert(ranged.state == out_of_range);
      match ranged.fault {
        Some(fault) => {
          assert(fault.kind == VectorRangeFault);
          assert(fault.error_code == 0x0000000000000001)
        },
        None() => assert(false),
      }
    },
  };

  match decode_full_record([|0xCF, 0xFC, 0x18, 0x86, 0x04, 0x82|]) {
    None() => assert(false),
    Some(instruction) => {
      var state = initial_cpu();
      state.registers[2] = 0x0000000000000001;
      state.registers[3] = 0x0000000000000100;
      state.registers[4] = 0xFFFFFFFFFFFFFFFC;
      state.predicate_registers[0] = [|0x10, 0x00|];
      state.vector_registers[2] =
        [|0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07,
          0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F|];
      let started = execute_full(instruction, state);
      assert(started.awaiting_environment);
      assert(started.request.kind == VectorMemoryWrite);
      assert(started.request.range_start == 0x00000000000000FC);
      assert(started.request.range_length == 4);
      assert(started.request.payload_bytes == [|0x01, 0x04, 0x05, 0x06, 0x07|]);
      let stored = resume_transaction(
        started, response_bytes(ResponseVectorMemory, [||])
      );
      assert(stored.fault == None());
      assert(stored.state.registers[2] == 0x0000000000000002);
      let failed = resume_transaction(started, failing_response(ResponseVectorMemory));
      assert(failed.state == state)
    },
  };

  match decode_full_record([|0xCF, 0xFC, 0x10, 0x84, 0x04, 0x82|]) {
    Some(instruction) => {
      let result = execute_full(instruction, initial_cpu());
      assert(result.state == initial_cpu());
      match result.fault {
        Some(fault) => assert(fault.kind == IllegalInstruction), None() => assert(false),
      }
    },
    None() => assert(false),
  };
  match decode_full_record([|0xCF, 0xFC, 0x10, 0x86, 0x04, 0x42|]) {
    Some(instruction) => {
      let result = execute_full(instruction, initial_cpu());
      match result.fault {
        Some(fault) => assert(fault.kind == IllegalInstruction), None() => assert(false),
      }
    },
    None() => assert(false),
  }
}

function test_vector_memory_protocol() -> unit = {
  match decode_full_record([|0xCF, 0xFC, 0x08, 0x00, 0x00, 0x00|]) {
    Some(instruction) => {
      assert(instruction.form.operation == Op_VMOV);
      var state = initial_cpu();
      state.registers[0] = 0x0000000000000080;
      state.predicate_registers[0] = [|0x05, 0x00|];
      state.vector_registers[0] =
        [|0xAA, 0xAA, 0xAA, 0xAA, 0xAA, 0xAA, 0xAA, 0xAA,
          0xAA, 0xAA, 0xAA, 0xAA, 0xAA, 0xAA, 0xAA, 0xAA|];
      let started = execute_full(instruction, state);
      assert(started.awaiting_environment);
      assert(started.request.kind == VectorMemoryRead);
      assert(started.request.access == AccessLoad);
      assert(started.request.commit_point);
      assert(started.request.range_start == 0x0000000000000080);
      assert(started.request.range_length == 16);
      assert(started.request.auxiliary == 0x0000000000000001);
      assert(started.request.payload_bytes == [|0x05, 0x00|]);
      let resumed = resume_transaction(started, response_bytes(
        ResponseVectorMemory,
        [|0x10, 0x20, 0x30, 0x40, 0x50, 0x60, 0x70, 0x80,
          0x90, 0xA0, 0xB0, 0xC0, 0xD0, 0xE0, 0xF0, 0x00|]
      ));
      assert(not_bool(resumed.awaiting_environment));
      assert(resumed.fault == None());
      assert(resumed.state.vector_registers[0] ==
        [|0x10, 0xAA, 0x30, 0xAA, 0xAA, 0xAA, 0xAA, 0xAA,
          0xAA, 0xAA, 0xAA, 0xAA, 0xAA, 0xAA, 0xAA, 0xAA|]);

      let failed = resume_transaction(started, failing_response(ResponseVectorMemory));
      assert(failed.state == state);
      assert(failed.fault != None())
    },
    None() => assert(false),
  };

  match decode_full_record([|0xD3, 0xFC, 0x08, 0x00, 0x00, 0x63, 0xAC|]) {
    Some(instruction) => {
      var state = initial_cpu();
      state.registers[5] = 0x0000000000000100;
      state.predicate_registers[0] = [|0x01, 0x00|];
      let started = execute_full(instruction, state);
      assert(started.awaiting_environment);
      assert(started.request.effective_address == 0x0000000000000100);
      assert(started.pending.after.registers[5] == 0x0000000000000110)
    },
    None() => assert(false),
  }
}

function test_vector_fp_and_reduction_semantics() -> unit = {
  match decode_full_record([|0xCB, 0xF7, 0x96, 0xC0, 0x00|]) {
    None() => assert(false),
    Some(instruction) => {
      assert(instruction.form.operation == Op_VDIV);
      assert(operation_width(instruction) == 2);

      let disabled = execute_full(instruction, initial_cpu());
      match disabled.fault {
        Some(fault) => assert(fault.kind == ExtensionUnavailable),
        None() => assert(false),
      };

      var state = initial_cpu();
      state.fp_enabled = true;
      state.predicate_registers[0] = [|0x01, 0x00|];
      state.vector_registers[0] =
        [|0x00, 0x3C, 0x00, 0x40, 0x00, 0x42, 0x00, 0x44,
          0x00, 0x45, 0x00, 0x46, 0x00, 0x47, 0x00, 0x48|];
      let waiting = execute_full(instruction, state);
      assert(waiting.awaiting_environment);
      assert(waiting.pending.phase == PhaseVectorFpCompute);
      assert(waiting.request.kind == VectorFloatingPointRequest);
      assert(waiting.request.width == 2);
      assert(waiting.request.selector == 0x0000000000000001);
      assert(waiting.request.expected == state.fstatus);
      assert(waiting.request.body_length == 16);
      assert(byte_count(waiting.request.payload_bytes) == 34);
      assert(vector_byte_at(waiting.request.payload_bytes, 0) == 0x01);
      assert(vector_byte_at(waiting.request.payload_bytes, 2) == 0x00);
      assert(vector_byte_at(waiting.request.payload_bytes, 3) == 0x3C);
      assert(vector_byte_at(waiting.request.payload_bytes, 18) == 0x00);
      assert(vector_byte_at(waiting.request.payload_bytes, 19) == 0x3C);

      let computed =
        [|0x00, 0x38, 0x00, 0x40, 0x00, 0x42, 0x00, 0x44,
          0x00, 0x45, 0x00, 0x46, 0x00, 0x47, 0x00, 0x48|];
      let completed_result = resume_transaction(
        waiting, response_bytes(ResponseVectorFloatingPoint, computed)
      );
      assert(completed_result.fault == None());
      assert(completed_result.state.vector_registers[0] == computed);
      assert(completed_result.state.fflags == fflags_none);
      assert(completed_result.state.pc == 0x0000000000000005);

      var trap_state = state;
      trap_state.fstatus = fp_make_fstatus(0b00, false, false, false, fflags_dz);
      trap_state.fflags = fflags_nx;
      let trap_waiting = execute_full(instruction, trap_state);
      let trapped = resume_transaction(
        trap_waiting,
        { response_bytes(ResponseVectorFloatingPoint, computed) with
          generated_fflags = fflags_dz }
      );
      assert(trapped.state == trap_state);
      match trapped.fault {
        Some(fault) => assert(fault.kind == FloatingPointFault),
        None() => assert(false),
      }
    },
  };

  match decode_full_record([|0xCB, 0xF7, 0x80, 0x00, 0x00|]) {
    None() => assert(false),
    Some(instruction) => {
      let integer_without_fp = execute_full(instruction, initial_cpu());
      assert(integer_without_fp.fault == None())
    },
  };

  match decode_full_record([|0xCB, 0xF7, 0xE8, 0x00, 0x00|]) {
    None() => assert(false),
    Some(instruction) => {
      var state = initial_cpu();
      state.predicate_registers[0] = [|0x05, 0x00|];
      state.vector_registers[0] =
        [|0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08,
          0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F, 0x10|];
      let reduced = execute_full(instruction, state);
      assert(reduced.fault == None());
      assert(reduced.state.registers[0] == 0x0000000000000004)
    },
  };

  match decode_full_record([|0xCB, 0xF7, 0xEA, 0x20, 0x00|]) {
    None() => assert(false),
    Some(instruction) => {
      let reduced = execute_full(instruction, initial_cpu());
      assert(reduced.fault == None());
      assert(reduced.state.registers[0] == 0x00000000000000FF)
    },
  }
}
