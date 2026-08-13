function test_protocol_events_group() -> unit = {
  match decode_full_record([|0x07|]) {
    Some(instruction) => {
      var state = initial_cpu();
      state.pc = 0x0000000000001000; state.sp = 0x0000000000007000;
      state.flags = 0b1010; state.status = 0x0000000000000024;
      state.controls[2] = 0x0000000000000401;
      state.controls[12] = 0x0000000000000200;
      state.controls[19] = 0x0000000000000000;
      state.controls[20] = 0x0000000000009000;
      state.controls[21] = 0x0000000000000000;
      state.controls[22] = 0x000000000000A000;
      let target = execute_full(instruction, state);
      let range = resume_transaction(
        target, successful_response(ResponseTranslation, 0x0000000000000000, true)
      );
      let store = resume_transaction(
        range, successful_response(ResponseStackRange, 0x0000000000000000, true)
      );
      assert(store.request.range_start == 0x0000000000008FC0);
      match read_le_bits(store.request.payload_bytes, 0, 64) {
        Some(control) => assert(control == 0x0024000A00000008),
        None() => assert(false),
      };
      match read_le_bits(store.request.payload_bytes, 24, 64) {
        Some(saved_pc) => assert(saved_pc == 0x0000000000001001),
        None() => assert(false),
      };
      let df_target = resume_transaction(store, failing_response(ResponseEventFrame));
      assert(df_target.pending.phase == PhaseEventTargetProbe);
      let df_range = resume_transaction(
        df_target, successful_response(ResponseTranslation, 0x0000000000000000, true)
      );
      let df_store = resume_transaction(
        df_range, successful_response(ResponseStackRange, 0x0000000000000000, true)
      );
      assert(df_store.request.range_start == 0x0000000000009FA0);
      match (read_le_bits(df_store.request.payload_bytes, 0, 64),
             read_le_bits(df_store.request.payload_bytes, 64, 64),
             read_le_bits(df_store.request.payload_bytes, 88, 64)) {
        (Some(control), Some(error), Some(aux)) => {
          assert(control == 0x0024000A0000030C);
          assert(error == 0x0000000007000003);
          assert(aux == 0x0000000000000002)
        },
        _ => assert(false),
      }
    },
    None() => assert(false),
  };

  var repeat_image = initial_cpu();
  repeat_image.repeat_state = struct {
    active = true, grouped = true, counter = 0x3, remaining = 0x0000000000000005,
    condition = 0x0, body_bytes = 0x0034, body_start = 0x0000000000000FEE,
    fixed_body = [||], group_progress = 0
  };
  assert(repeat_frame_ext1(repeat_image, 0x0000000000001000)
         == 0x0000003400120103);

  match decode_full_record([|0xC8, 0x26, 0x80, 0x02, 0x00|]) {
    Some(prefix) => {
      var five = initial_cpu(); five.registers[0] = 0x0000000000000002;
      five.registers[1] = 0x0000000000000005;
      let fetch = execute_full(prefix, five);
      let boundary = resume_transaction(
        fetch, response_bytes(ResponseRepeatFetch, [|0x81, 0x10|])
      );
      assert(boundary.pending.boundary_class == BoundaryRepeatGroup);
      assert(not_bool(boundary.awaiting_environment));
      assert(boundary.state.registers[0] == 0x0000000000000004);
      assert(boundary.pending.after.registers[0] == 0x0000000000000004);
      var zero = initial_cpu(); zero.registers[0] = 0x0000000000000002;
      zero.registers[1] = 0x0000000000000000;
      let zero_done = resume_transaction(
        execute_full(prefix, zero), response_bytes(ResponseRepeatFetch, [|0x81, 0x10|])
      );
      assert(not_bool(zero_done.awaiting_environment));
      assert(zero_done.state.registers[0] == 0x0000000000000000);
      var one = initial_cpu(); one.registers[0] = 0x0000000000000002;
      one.registers[1] = 0x0000000000000001;
      let one_done = resume_transaction(
        execute_full(prefix, one), response_bytes(ResponseRepeatFetch, [|0x81, 0x10|])
      );
      assert(not_bool(one_done.awaiting_environment));
      assert(one_done.state.registers[0] == 0x0000000000000000)
    },
    None() => assert(false),
  };

  match decode_full_record([|0xC8, 0x26, 0x80, 0x05, 0x00|]) {
    Some(prefix) => {
      var state = initial_cpu(); state.registers[0] = 0x0000000000000005;
      let first = resume_transaction(
        execute_full(prefix, state),
        response_bytes(ResponseRepeatFetch, [|0x60, 0xC7, 0xC2, 0x20, 0x00|])
      );
      assert(first.pending.boundary_class == BoundaryRepeatInterior);
      let next = execute_boundary(prefix, first.state, no_async_ingress());
      let failed : Execution_result = match next.execution {
        Some(result) => result,
        None() => first,
      };
      assert(not_bool(failed.awaiting_environment));
      match failed.fault {
        Some(fault) => assert(fault.kind == DivideByZero),
        None() => assert(false),
      };
      assert(failed.state.registers[0] == 0x0000000000000000);
      assert(failed.state.repeat_state.active);
      assert(failed.state.repeat_state.remaining == 0x0000000000000005)
    },
    None() => assert(false),
  }
}
