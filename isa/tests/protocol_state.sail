function test_protocol_state_group() -> unit = {
  match decode_full_record([|0xC7, 0xEF, 0x44, 0x80|]) {
    Some(instruction) => {
      var state = initial_cpu(); state.registers[0] = 0x0000000000001000;
      state.supervisor = true; state.status = 0x0000000000000034; state.flags = 0b1010;
      state.fp_enabled = true; state.fp_component_modified = true;
      state.floating_registers[0] = 0x0123456789ABCDEF;
      state.fflags = 0b10101; state.fstatus = 0x0000000000000155;
      state.vector_component_modified = true;
      state.vector_registers[0] = 0xAB :: zero_vector_bytes(15);
      state.predicate_registers[0] = [|0x5A, 0xA5|];
      let pending = execute_full(instruction, state);
      assert(pending.request.kind == StateSaveRequest);
      assert(pending.request.range_length == 960);
      assert(byte_list_length(pending.request.payload_bytes) == 960);
      match (read_le_bits(pending.request.payload_bytes, 0, 64),
             read_le_bits(pending.request.payload_bytes, 8, 64),
             read_le_bits(pending.request.payload_bytes, 192, 64),
             read_le_bits(pending.request.payload_bytes, 384, 64),
             read_le_bits(pending.request.payload_bytes, 896, 16)) {
        (Some(header), Some(bitmap), Some(f0), Some(v0), Some(p0)) => {
          assert(header == 0x0000034000A003F0);
          assert(bitmap == 0x0000000000000003);
          assert(f0 == state.floating_registers[0]);
          assert(v0 == 0x00000000000000AB);
          assert(p0 == 0x000000000000A55A)
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
      // valid_vector_length_bytes owns the 256-byte maximum at this SAVE boundary.
      var maximum_vlen = state;
      maximum_vlen.vector_length_bytes = 256;
      maximum_vlen.vector_registers = zero_vector_registers(256);
      maximum_vlen.predicate_registers = zero_predicate_registers(256);
      maximum_vlen.vector_component_size =
        tdiv_int(34 * maximum_vlen.vector_length_bytes + 63, 64) * 64;
      maximum_vlen.save_area_size =
        maximum_vlen.vector_component_offset + maximum_vlen.vector_component_size;
      let accepted_maximum_vlen = execute_full(instruction, maximum_vlen);
      assert(accepted_maximum_vlen.awaiting_environment);
      assert(accepted_maximum_vlen.fault == None());
      assert(accepted_maximum_vlen.request.kind == StateSaveRequest);
      assert(accepted_maximum_vlen.request.range_length == maximum_vlen.save_area_size);
      assert(byte_list_length(accepted_maximum_vlen.request.payload_bytes)
             == maximum_vlen.save_area_size);
      var excessive_vlen = maximum_vlen;
      excessive_vlen.vector_length_bytes = 512;
      excessive_vlen.vector_registers = zero_vector_registers(512);
      excessive_vlen.predicate_registers = zero_predicate_registers(512);
      excessive_vlen.vector_component_size =
        tdiv_int(34 * excessive_vlen.vector_length_bytes + 63, 64) * 64;
      excessive_vlen.save_area_size =
        excessive_vlen.vector_component_offset + excessive_vlen.vector_component_size;
      let rejected_excessive_vlen = execute_full(instruction, excessive_vlen);
      assert(not_bool(rejected_excessive_vlen.awaiting_environment));
      assert(rejected_excessive_vlen.state == excessive_vlen);
      assert(rejected_excessive_vlen.fault != None());
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
      image_state.vector_component_modified = true;
      image_state.vector_registers[0] = 0xCD :: zero_vector_bytes(15);
      image_state.predicate_registers[0] = [|0x96, 0x69|];
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
      assert(done.state.vector_registers[0] == image_state.vector_registers[0]);
      assert(done.state.predicate_registers[0] == image_state.predicate_registers[0]);
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
