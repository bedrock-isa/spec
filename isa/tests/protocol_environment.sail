function test_protocol_environment_group() -> unit = {
  verify_pair_stack_protocol(0);
  match decode_full_record([|0xC7, 0xD5, 0x08, 0x10|]) {
    Some(instruction) => {
      var state = initial_cpu(); state.fp_enabled = true;
      state.floating_registers[0] = 0x3FF0000000000000;
      state.registers[15] = 0x0000000000000002;
      state.repeat_state = struct {
        active = true, counter = 0xF,
        remaining = 0x0000000000000002, condition = 0x0,
        prefix_start = state.pc, body_start = state.pc,
        fixed_body = [|0xC7, 0xD5, 0x08, 0x10|]
      };
      let source = execute_full(instruction, state);
      assert(source.pending.phase == PhaseFpSourceRead);
      let parent = attach_repeat_parent(
        source, instruction, [|0xC7, 0xD5, 0x08, 0x10|]
      );
      let compute = resume_transaction(
        parent, successful_response(ResponseRead, 0x4000000000000000, true)
      );
      assert(compute.awaiting_environment);
      assert(compute.pending.phase == PhaseFpCompute);
      assert(compute.pending.repeat_parent_active);
      assert(compute.pending.repeat_body == Some(instruction));
      assert(compute.pending.repeat_bytes == [|0xC7, 0xD5, 0x08, 0x10|])
    },
    None() => assert(false),
  };
  match decode_full_record([|0xC7, 0xEF, 0x42, 0x10|]) {
    Some(instruction) => {
      var state = initial_cpu();
      state.supervisor = true; state.status = 0x0000000000000010;
      state.registers[0] = 0x0000000000000037;
      state.segments[1] = 0x0000000000001002;
      state.controls[0] = 0x0000000000001001;
      let translating = execute_full(instruction, state);
      assert(translating.pending.phase == PhaseCacheTranslate);
      assert(translating.request.linear_address == 0x0000000000001037);
      assert(not_bool(translating.request.commit_point));
      let block = resume_transaction(
        translating, { successful_response(
          ResponseAddressTranslation, 0x000000000000A07F, true
        ) with cache_policy = 7 }
      );
      assert(block.request.kind == CacheMaintenanceBlock);
      assert(block.request.range_start == 0x000000000000A040);
      assert(block.request.range_end == 0x000000000000A080);
      assert(block.request.address_translation == false);
      assert(block.request.cache_policy == 7);
    },
    None() => assert(false),
  };

  match decode_full_record([|0xC7, 0xEF, 0x48, 0x00|]) {
    Some(instruction) => {
      var state = initial_cpu();
      state.supervisor = true; state.status = 0x0000000000000010;
      state.controls[0] = 0x0000000000001001;
      state.registers[0] = 0x0000123456789ABC;
      let l4 = execute_full(instruction, state);
      assert(l4.request.kind == PhysicalPteRead);
      assert(l4.request.range_start == 0x0000000000001120);
      let l3 = resume_transaction(l4, pte_response(0x000000000000203F));
      assert(l3.request.range_start == 0x0000000000002688);
      let l2 = resume_transaction(l3, pte_response(0x000000000000303F));
      assert(l2.request.range_start == 0x0000000000003598);
      let l1 = resume_transaction(l2, pte_response(0x000000000000403F));
      assert(l1.request.range_start == 0x0000000000004C48);
      let done = resume_transaction(l1, pte_response(0x00000000ABCDE02D));
      assert(done.state.registers[0] == 0x00000000ABCDEABC);
      assert(done.state.flags == 0b0001);
      let large_l3 = resume_transaction(l3, pte_response(0x000000004000002D));
      assert(large_l3.state.registers[0] == 0x0000000056789ABC);
      assert(large_l3.state.flags == 0b0001);
      let misaligned_l3 = resume_transaction(l3, pte_response(0x000000004000102D));
      assert(misaligned_l3.state.registers[0] == 0x0000000000000000);
      assert(misaligned_l3.state.flags == 0b0000);
      let bit7_leaf = resume_transaction(l3, pte_response(0x00000000400000AD));
      assert(bit7_leaf.state.registers[0] == 0x0000000056789ABC);
      assert(bit7_leaf.state.flags == 0b0001);
      let malformed_l3 = resume_transaction(l3, pte_response(0x000000000000307F));
      assert(malformed_l3.state.registers[0] == 0x0000000000000000);
      assert(malformed_l3.state.flags == 0b0000);
      let unreadable = resume_transaction(l4, failing_response(ResponsePteRead));
      assert(unreadable.fault != None());
      assert(unreadable.state == state)
    },
    None() => assert(false),
  };

  match decode_full_record([|0xC7, 0xEF, 0x48, 0x00|]) {
    Some(instruction) => {
      var direct_state = initial_cpu();
      direct_state.supervisor = true; direct_state.status = 0x0000000000000010;
      direct_state.controls[0] = 0x0000000000000000;
      direct_state.registers[0] = 0x00FFFFFFFFFFFFFF;
      let direct = execute_full(instruction, direct_state);
      assert(not_bool(direct.awaiting_environment));
      assert(direct.request.kind == NoPrimitiveRequest);
      assert(direct.state.registers[0] == 0x00FFFFFFFFFFFFFF);
      assert(direct.state.flags == 0b0001);

      var outside_state = direct_state;
      outside_state.registers[0] = 0x0100000000000000;
      let outside = execute_full(instruction, outside_state);
      assert(not_bool(outside.awaiting_environment));
      assert(outside.request.kind == NoPrimitiveRequest);
      assert(outside.state.registers[0] == 0x0000000000000000);
      assert(outside.state.flags == 0b0000)
    },
    None() => assert(false),
  };

  match decode_full_record([|0xC7, 0xEF, 0x18, 0x00|]) {
    Some(instruction) => {
      var state = initial_cpu();
      state.supervisor = true; state.status = 0x0000000000000010;
      state.controls[0] = 0x0000000000001001;
      state.registers[0] = 0x0000123456789ABC;
      let l4 = execute_full(instruction, state);
      let l3 = resume_transaction(l4, pte_response(0x000000000000203F));
      let raw = resume_transaction(l3, pte_response(0x000000000000307F));
      assert(raw.state.registers[0] == 0x000000000000307F);
      assert(raw.state.flags == 0b0000);
      let large_leaf = resume_transaction(l3, pte_response(0x000000004000002D));
      assert(large_leaf.state.registers[0] == 0x000000004000002D);
      assert(large_leaf.state.flags == 0b0001);
      let unreadable = resume_transaction(l4, failing_response(ResponsePteRead));
      assert(unreadable.fault != None());
      assert(unreadable.state == state);
      var outside = state;
      outside.registers[0] = 0x0000000000003000;
      outside.segments[1] = 0x0000000000001003;
      let rejected_bounds = execute_full(instruction, outside);
      assert(not_bool(rejected_bounds.awaiting_environment));
      assert(rejected_bounds.fault != None());
      assert(rejected_bounds.state == outside)
    },
    None() => assert(false),
  };

  match decode_full_record([|0xC7, 0xEF, 0x10, 0x00|]) {
    Some(instruction) => {
      var state = initial_cpu();
      state.supervisor = true; state.status = 0x0000000000000010;
      state.controls[0] = 0x0000000000001001;
      state.registers[0] = 0x0000123456789ABC;
      let l4 = execute_full(instruction, state);
      let l3 = resume_transaction(l4, pte_response(0x000000000000203F));
      let blocked = resume_transaction(l3, pte_response(0x000000004000002D));
      assert(not_bool(blocked.awaiting_environment));
      assert(blocked.state.registers[0] == 0x0000000000000000);
      assert(blocked.state.flags == 0b0000)
    },
    None() => assert(false),
  };

  match decode_full_record([|0xCF, 0xEF, 0x47, 0x10, 0x01, 0x10|]) {
    Some(instruction) => {
      var state = initial_cpu();
      state.supervisor = true; state.status = 0x0000000000000010;
      state.registers[0] = 0x0123456789ABCDEF;
      let pending = execute_full(instruction, state);
      assert(pending.request.kind == ControlTransitionRequest);
      let done = resume_transaction(
        pending, successful_response(ResponseControlTransition, 0xFFFFFFFFFFFFFFFF, true)
      );
      assert(done.state.controls[24] == state.registers[0])
    },
    None() => assert(false),
  };

  match decode_full_record([|0xC0, 0x27, 0x00|]) {
    Some(instruction) => {
      var state = initial_cpu(); state.registers[0] = 0xFFFFFFFFFFFFFFFF;
      let pending = execute_full(instruction, state);
      let unknown = resume_transaction(
        pending, { successful_response(ResponseCpuidQuery, 0xDEADBEEFDEADBEEF, true) with
                   known = false }
      );
      assert(unknown.state.registers[0] == 0x0000000000000000)
    },
    None() => assert(false),
  };

  match decode_full_record([|0xCF, 0xEF, 0x47, 0xA0, 0x00, 0x00|]) {
    Some(instruction) => {
      let rejected = execute_full(instruction, initial_cpu());
      assert(not_bool(rejected.awaiting_environment));
      assert(rejected.fault != None());
      assert(rejected.state == initial_cpu())
    },
    None() => assert(false),
  };

  match decode_full_record([|0xCF, 0xEF, 0x47, 0xA0, 0x01, 0x00|]) {
    Some(instruction) => {
      var state = initial_cpu(); state.flags = 0b1010; state.fflags = 0b00001;
      let pending = execute_full(instruction, state);
      assert(pending.awaiting_environment);
      let done = resume_transaction(
        pending, { successful_response(
          ResponsePerformanceCounter, 0x0000000000001234, true
        ) with write_flags = true, flags = 0b0101, generated_fflags = 0b11110,
               state_image = { initial_cpu() with sp = 0xFFFFFFFFFFFFFFFF } }
      );
      assert(done.fault == None());
      assert(done.state.registers[0] == 0x0000000000001234);
      assert(done.state.flags == state.flags);
      assert(done.state.fflags == state.fflags);
      assert(done.state.sp == state.sp)
    },
    None() => assert(false),
  };
}
