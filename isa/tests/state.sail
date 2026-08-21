function test_state_register_local() -> unit = {
  match decode_full_record([|0xC0, 0x2D, 0x85|]) {
    Some(instruction) => {
      let result = execute_full(instruction, { initial_cpu() with flags = 0b1111 });
      assert(result.state.flags == 0b0111)
    },
    None() => assert(false),
  };
  match decode_full_record([|0xC0, 0x25, 0x8A|]) {
    Some(_) => assert(false),
    None() => (),
  };
  match decode_full_record([|0xC7, 0xEF, 0x47, 0x34|]) {
    Some(instruction) => {
      var state = initial_cpu();
      state.registers[4] = 0x0000000000000010;
      let result = execute_full(instruction, state);
      assert(result.fault != None());
      assert(result.state.flags == state.flags)
    },
    None() => assert(false),
  };
  match decode_full_record([|0xC7, 0xEF, 0x47, 0x24|]) {
    Some(instruction) => {
      let state = { initial_cpu() with flags = 0b1010 };
      let result = execute_full(instruction, state);
      assert(result.state.registers[4] == 0x000000000000000A)
    },
    None() => assert(false),
  };
  match decode_full_record([|0xCF, 0xEF, 0x47, 0x11, 0xFF, 0xFF|]) {
    Some(instruction) => {
      var state = initial_cpu();
      state.supervisor = true;
      state.status = 0x0000000000000010;
      state.registers[1] = 0x0123456789ABCDEF;
      let result = execute_full(instruction, state);
      assert(not_bool(result.awaiting_environment));
      assert(result.state.pc == state.pc);
      assert(result.state.controls == state.controls);
      match result.fault {
        Some(fault) => assert(fault.kind == InvalidControlState),
        None() => assert(false),
      }
    },
    None() => assert(false),
  };
  match decode_full_record([|0xCF, 0xEF, 0x47, 0x02, 0xFF, 0xFF|]) {
    Some(instruction) => {
      var state = initial_cpu();
      state.supervisor = true;
      state.status = 0x0000000000000010;
      state.registers[2] = 0xFEDCBA9876543210;
      let result = execute_full(instruction, state);
      assert(not_bool(result.awaiting_environment));
      assert(result.state.pc == state.pc);
      assert(result.state.registers[2] == state.registers[2]);
      match result.fault {
        Some(fault) => assert(fault.kind == InvalidControlState),
        None() => assert(false),
      }
    },
    None() => assert(false),
  };
  match decode_full_record([|0xCF, 0xEF, 0x47, 0x10, 0x02, 0x00|]) {
    Some(instruction) => {
      var reserved = initial_cpu();
      reserved.supervisor = true; reserved.status = 0x0000000000000010;
      reserved.registers[0] = 0x0000000000000002;
      let rejected_reserved = execute_full(instruction, reserved);
      assert(not_bool(rejected_reserved.awaiting_environment));
      assert(rejected_reserved.state == reserved);
      assert(rejected_reserved.fault != None());

      var preserve_pending = reserved;
      preserve_pending.controls[2] = 0x0000000000000080;
      preserve_pending.registers[0] = 0x0000000000000000;
      let preserved = execute_full(instruction, preserve_pending);
      assert(preserved.fault == None());
      assert(preserved.state.controls[2] == 0x0000000000000080);

      var ignore_input = reserved;
      ignore_input.registers[0] = 0x0000000000000080;
      let ignored = execute_full(instruction, ignore_input);
      assert(ignored.fault == None());
      assert(ignored.state.controls[2] == 0x0000000000000000);

      var valid_transition = reserved;
      valid_transition.controls[2] = 0x0000000000000080;
      valid_transition.registers[0] = 0x0000000000000001;
      let pending = execute_full(instruction, valid_transition);
      assert(pending.awaiting_environment);
      assert(pending.request.kind == ControlTransitionRequest);
      assert(pending.request.value == 0x0000000000000081);
      let enabled = resume_transaction(
        pending, successful_response(ResponseControlTransition, 0xFFFFFFFFFFFFFFFF, true)
      );
      assert(enabled.fault == None());
      assert(enabled.state.controls[2] == 0x0000000000000081);

      var invalid_transition = reserved;
      invalid_transition.registers[0] = 0x0000000000000001;
      invalid_transition.controls[12] = 0x0000000000000001;
      let rejected_bank = execute_full(instruction, invalid_transition);
      assert(not_bool(rejected_bank.awaiting_environment));
      assert(rejected_bank.state == invalid_transition);
      assert(rejected_bank.fault != None());

      var invalid_revalidation = invalid_transition;
      invalid_revalidation.controls[2] = 0x0000000000000001;
      let rejected_revalidation = execute_full(instruction, invalid_revalidation);
      assert(not_bool(rejected_revalidation.awaiting_environment));
      assert(rejected_revalidation.state == invalid_revalidation);
      assert(rejected_revalidation.fault != None())
    },
    None() => assert(false),
  }
}
