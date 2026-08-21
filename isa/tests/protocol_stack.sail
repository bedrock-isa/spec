function test_protocol_stack_group() -> unit = {
  match decode_full_record([|0x10|]) {
    Some(instruction) => {
      var state = initial_cpu(); state.sp = 0x0000000000001000;
      state.registers[0] = 0x1111111111111111;
      state.registers[1] = 0x2222222222222222;
      let range = execute_full(instruction, state);
      let store = resume_transaction(
        range, successful_response(ResponseStackRange, 0x0000000000000000, true)
      );
      assert(store.request.kind == CompoundMemoryStore);
      assert(store.request.value == state.registers[1]);
      assert(store.request.desired == state.registers[0]);
      let failed = resume_transaction(store, failing_response(ResponseStoreAck));
      assert(failed.state == state);
      let done = resume_transaction(
        store, successful_response(ResponseStoreAck, 0x0000000000000000, true)
      );
      assert(done.state.sp == 0x0000000000000FF0)
    },
    None() => assert(false),
  };

  match decode_full_record([|0x18|]) {
    Some(instruction) => {
      var state = initial_cpu(); state.sp = 0x0000000000001000;
      let range = execute_full(instruction, state);
      let low_read = resume_transaction(
        range, successful_response(ResponseStackRange, 0x0000000000000000, true)
      );
      assert(low_read.request.kind == MemoryRead);
      assert(low_read.request.range_start == state.sp);
      let high_read = resume_transaction(
        low_read, successful_response(ResponseRead, 0x2222222222222222, true)
      );
      assert(high_read.request.kind == MemoryRead);
      assert(high_read.request.range_start == 0x0000000000001008);
      let done = resume_transaction(
        high_read, successful_response(ResponseRead, 0x1111111111111111, true)
      );
      assert(done.state.registers[0] == 0x1111111111111111);
      assert(done.state.registers[1] == 0x2222222222222222);
      assert(done.state.sp == 0x0000000000001010)
    },
    None() => assert(false),
  };

  match decode_full_record([|0x1F|]) {
    Some(instruction) => {
      var state = initial_cpu(); state.sp = 0x0000000000002000;
      let range = execute_full(instruction, state);
      let low_read = resume_transaction(
        range, successful_response(ResponseStackRange, 0x0000000000000000, true)
      );
      let high_read = resume_transaction(
        low_read, successful_response(ResponseRead, 0x4444444444444444, true)
      );
      let done = resume_transaction(
        high_read, successful_response(ResponseRead, 0x3333333333333333, true)
      );
      assert(done.state.registers[14] == 0x3333333333333333);
      assert(done.state.registers[15] == 0x4444444444444444);
      assert(done.state.sp == 0x0000000000002010)
    },
    None() => assert(false),
  };

  match decode_full_record([|0x70|]) {
    Some(instruction) => {
      var state = initial_cpu(); state.fp_enabled = true;
      state.sp = 0x0000000000003000;
      state.floating_registers[0] = 0x1111111111111111;
      state.floating_registers[1] = 0x2222222222222222;
      let range = execute_full(instruction, state);
      assert(range.request.range_length == 16);
      let store = resume_transaction(
        range, successful_response(ResponseStackRange, 0x0000000000000000, true)
      );
      assert(store.request.kind == CompoundMemoryStore);
      assert(store.request.value == state.floating_registers[1]);
      assert(store.request.desired == state.floating_registers[0]);
      let done = resume_transaction(
        store, successful_response(ResponseStoreAck, 0x0000000000000000, true)
      );
      assert(done.state.sp == 0x0000000000002FF0)
    },
    None() => assert(false),
  };

  match decode_full_record([|0x7F|]) {
    Some(instruction) => {
      var state = initial_cpu(); state.fp_enabled = true;
      state.sp = 0x0000000000003000;
      let range = execute_full(instruction, state);
      let low_read = resume_transaction(
        range, successful_response(ResponseStackRange, 0x0000000000000000, true)
      );
      let high_read = resume_transaction(
        low_read, successful_response(ResponseRead, 0x4444444444444444, true)
      );
      let done = resume_transaction(
        high_read, successful_response(ResponseRead, 0x3333333333333333, true)
      );
      assert(done.state.floating_registers[14] == 0x3333333333333333);
      assert(done.state.floating_registers[15] == 0x4444444444444444);
      assert(done.state.sp == 0x0000000000003010);
      assert(done.state.fp_component_modified)
    },
    None() => assert(false),
  };

  match decode_full_record([|0x03|]) {
    Some(instruction) => {
      var state = initial_cpu(); state.sp = 0x0000000000002000;
      state.segments[0] = 0x0000000000000000;
      let range = execute_full(instruction, state);
      assert(range.request.kind == StackRange);
      assert(range.request.range_length == 16);
      let failed_range = resume_transaction(range, failing_response(ResponseStackRange));
      assert(failed_range.state == state);
      let first_read = resume_transaction(
        range, successful_response(ResponseStackRange, 0x0000000000000000, true)
      );
      assert(first_read.request.kind == MemoryRead);
      let failed_first = resume_transaction(first_read, failing_response(ResponseRead));
      assert(failed_first.state == state);
      let second_read = resume_transaction(
        first_read, successful_response(ResponseRead, 0x0000000000001200, true)
      );
      assert(second_read.request.kind == MemoryRead);
      assert(second_read.request.range_start == 0x0000000000002008);
      let failed_second = resume_transaction(second_read, failing_response(ResponseRead));
      assert(failed_second.state == state);
      let probe = resume_transaction(
        second_read, successful_response(ResponseRead, 0x0000000000001003, true)
      );
      assert(probe.pending.phase == PhaseTargetExecuteProbe);
      assert(probe.request.kind == TranslationExecuteProbe);
      assert(probe.request.segment_image == 0x0000000000001003);
      let failed_probe = resume_transaction(probe, failing_response(ResponseTranslation));
      assert(failed_probe.state == state);
      let done = resume_transaction(
        probe, successful_response(ResponseTranslation, 0x0000000000000000, true)
      );
      assert(done.fault == None());
      assert(done.state.pc == 0x0000000000001200);
      assert(done.state.segments[0] == 0x0000000000001003);
      assert(done.state.sp == 0x0000000000002010);

      var wrapping = state; wrapping.sp = 0xFFFFFFFFFFFFFFF8;
      let wrapped = execute_full(instruction, wrapping);
      assert(wrapped.request.range_end == 0x0000000000000008);
      assert(wrapped.request.range_length == 16);
      assert(wrapped.request.range_wrap)
    },
    None() => assert(false),
  };

  match decode_full_record([|0x02|]) {
    Some(instruction) => {
      let state = { initial_cpu() with sp = 0xFFFFFFFFFFFFFFF8 };
      let wrapped = execute_full(instruction, state);
      assert(wrapped.request.range_end == 0x0000000000000000);
      assert(wrapped.request.range_length == 8);
      assert(wrapped.request.range_end_at_modulus)
    },
    None() => assert(false),
  };

  match decode_full_record([|0x05|]) {
    Some(instruction) => {
      var state = initial_cpu();
      state.controls[3] = 0x0000000000002000;
      state.controls[15] = 0x0000000000001003;
      state.controls[16] = 0x0000000000003000;
      let rejected = execute_full(instruction, state);
      assert(not_bool(rejected.awaiting_environment));
      assert(rejected.fault != None());
      assert(rejected.state == state)
    },
    None() => assert(false),
  };

  assert(decode_full_record([|0x06|]) == None());

  match decode_full_record([|0x01|]) {
    Some(instruction) => {
      var inactive = initial_cpu(); inactive.status = status_with_event_state(inactive.status, 1, false);
      let rejected_inactive = execute_full(instruction, inactive);
      assert(rejected_inactive.fault != None());
      assert(rejected_inactive.state == inactive);
      var active = initial_cpu();
      active.supervisor = true; active.status = 0x0000000000000011;
      active.status = status_with_event_state(active.status, 1, false);
      let accepted = execute_full(instruction, active);
      assert(accepted.fault == None());
      assert(accepted.state.pc == 0x0000000000000001);
      var invalid_active = active; invalid_active.status = status_with_event_state(active.status, 0, false);
      let rejected_active = execute_full(instruction, invalid_active);
      assert(rejected_active.fault != None());
      assert(rejected_active.state == invalid_active)
    },
    None() => assert(false),
  };
}
