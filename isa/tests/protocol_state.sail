function test_protocol_state_group() -> unit = {
  match decode_full_record([|0xC7, 0xEF, 0x44, 0x80|]) {
    Some(instruction) => {
      var state = initial_cpu(); state.registers[0] = 0x0000000000001000;
      state.supervisor = true; state.status = 0x0000000000000034; state.flags = 0b1010;
      state.fp_enabled = true; state.fp_component_modified = true;
      state.floating_registers[0] = 0x0123456789ABCDEF;
      state.fflags = 0b10101; state.fstatus = 0x0000000000000155;
      let pending = execute_full(instruction, state);
      assert(pending.request.kind == StateSaveRequest);
      assert(pending.request.range_length == 384);
      assert(byte_list_length(pending.request.payload_bytes) == 384);
      match (read_le_bits(pending.request.payload_bytes, 0, 64),
             read_le_bits(pending.request.payload_bytes, 8, 64),
             read_le_bits(pending.request.payload_bytes, 192, 64)) {
        (Some(header), Some(bitmap), Some(f0)) => {
          assert(header == 0x0000034000A003F0);
          assert(bitmap == 0x0000000000000001);
          assert(f0 == state.floating_registers[0])
        },
        _ => assert(false),
      };
      var wrong_offset = state;
      wrong_offset.save_area_size = 512;
      wrong_offset.fp_component_offset = 256;
      let rejected_offset = execute_full(instruction, wrong_offset);
      assert(not_bool(rejected_offset.awaiting_environment));
      assert(rejected_offset.state == wrong_offset);
      assert(rejected_offset.fault != None());
      var wrong_size = state;
      wrong_size.save_area_size = 448;
      wrong_size.fp_component_size = 256;
      let rejected_size = execute_full(instruction, wrong_size);
      assert(not_bool(rejected_size.awaiting_environment));
      assert(rejected_size.state == wrong_size);
      assert(rejected_size.fault != None());
      var zero_alignment = state;
      zero_alignment.fp_component_alignment = 0;
      let rejected_alignment = execute_full(instruction, zero_alignment);
      assert(not_bool(rejected_alignment.awaiting_environment));
      assert(rejected_alignment.state == zero_alignment);
      assert(rejected_alignment.fault != None());
      var wrapping = state;
      wrapping.registers[0] = 0xFFFFFFFFFFFFF000;
      wrapping.save_area_size = 4096;
      let wrapped = execute_full(instruction, wrapping);
      assert(wrapped.request.range_end == 0x0000000000000000);
      assert(wrapped.request.range_length == 4096);
      assert(not_bool(wrapped.request.range_wrap));
      assert(wrapped.request.range_end_at_modulus)
    },
    None() => assert(false),
  };

  match decode_full_record([|0xC7, 0xEF, 0x45, 0x00|]) {
    Some(instruction) => {
      var image_state = initial_cpu();
      image_state.registers[0] = 0x1111222233334444;
      image_state.status = 0x000000000000003F;
      image_state.fp_enabled = true; image_state.fp_component_modified = true;
      image_state.floating_registers[0] = 0x9999888877776666;
      let image = save_image_bytes(image_state);
      var state = initial_cpu(); state.registers[0] = 0x0000000000001000;
      let header = execute_full(instruction, state);
      assert(not_bool(header.request.commit_point));
      let range = resume_transaction(header, response_bytes(ResponseStateRestore, image));
      assert(range.pending.phase == PhaseStateRestoreRange);
      assert(not_bool(range.request.commit_point));
      let payload = resume_transaction(
        range, successful_response(ResponseStateRestore, 0x0000000000000000, true)
      );
      let poison = { initial_cpu() with sp = 0xFFFFFFFFFFFFFFFF };
      let done = resume_transaction(
        payload, { response_bytes(ResponseStateRestore, image) with state_image = poison }
      );
      assert(done.state.registers[0] == image_state.registers[0]);
      assert(done.state.status == state.status);
      assert(done.state.floating_registers[0] == image_state.floating_registers[0]);
      assert(done.state.sp == state.sp);

      var wrapping = state;
      wrapping.registers[0] = 0xFFFFFFFFFFFFF000;
      wrapping.save_area_size = 4096;
      let wrapping_image = save_image_bytes(wrapping);
      let wrapping_header = execute_full(instruction, wrapping);
      let wrapping_range = resume_transaction(
        wrapping_header, response_bytes(ResponseStateRestore, wrapping_image)
      );
      assert(wrapping_range.request.range_end == 0x0000000000000000);
      assert(wrapping_range.request.range_length == 4096);
      assert(not_bool(wrapping_range.request.range_wrap));
      assert(wrapping_range.request.range_end_at_modulus);

      var absent_image = initial_cpu();
      absent_image.fp_component_present = false;
      let absent_bytes = save_image_bytes(absent_image);
      var latent = absent_image;
      latent.registers[0] = 0x0000000000001000;
      latent.floating_registers[0] = 0x0123456789ABCDEF;
      latent.fflags = 0b10101;
      latent.fstatus = 0x0000000000000155;
      latent.fp_component_modified = true;
      let latent_header = execute_full(instruction, latent);
      let latent_range = resume_transaction(
        latent_header, response_bytes(ResponseStateRestore, absent_bytes)
      );
      let latent_payload = resume_transaction(
        latent_range, successful_response(ResponseStateRestore, 0x0000000000000000, true)
      );
      let latent_done = resume_transaction(
        latent_payload, response_bytes(ResponseStateRestore, absent_bytes)
      );
      assert(latent_done.fault == None());
      assert(latent_done.state.floating_registers[0] == latent.floating_registers[0]);
      assert(latent_done.state.fflags == latent.fflags);
      assert(latent_done.state.fstatus == latent.fstatus);
      assert(latent_done.state.fp_component_modified)
    },
    None() => assert(false),
  };
}
