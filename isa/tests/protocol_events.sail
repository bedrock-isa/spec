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
      assert(target.pending.phase == PhaseEventTargetProbe);
      let done = resume_transaction(
        target, successful_response(ResponseTranslation, 0x0000000000000000, true)
      );
      assert(not_bool(done.awaiting_environment));
      assert(done.fault == None());
      assert(done.state.controls[6] == 0x0000000000001001);
      assert(done.state.controls[7] == 0x0000000000007000);
      assert(done.state.controls[8] == state.segments[0]);
      assert(done.state.controls[9] == state.segments[1]);
      assert(done.state.controls[10] == state.segments[2]);
      assert(done.state.controls[11] == 0x000000010024000A);
      assert(done.state.controls[26] == 0x0000000000000002);
      assert(done.state.sp == 0x0000000000009000);
      assert(status_event_depth(done.state.status) == 1);
      assert(status_user_origin(done.state.status))
    },
    None() => assert(false),
  }
}
