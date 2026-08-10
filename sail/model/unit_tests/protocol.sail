function test_protocol_audit() -> unit = {
  verify_pair_stack_protocol(0);
  match decode_full_record([|0xC7, 0xD5, 0x08, 0x10|]) {
    Some(instruction) => {
      var state = initial_cpu(); state.fp_enabled = true;
      state.floating_registers[0] = 0x3FF0000000000000;
      state.registers[15] = 0x0000000000000002;
      state.repeat_state = struct {
        active = true, grouped = false, counter = 0xF,
        remaining = 0x0000000000000002, condition = 0x0,
        body_bytes = 0x0004, body_start = state.pc,
        fixed_body = [|0xC7, 0xD5, 0x08, 0x10|], group_progress = 0
      };
      let source = execute_full(instruction, state);
      assert(source.pending.phase == PhaseFpSourceRead);
      let parent = attach_repeat_parent(
        source, instruction, [|0xC7, 0xD5, 0x08, 0x10|], [||], 0, false
      );
      let compute = resume_transaction(
        parent, successful_response(ResponseRead, 0x4000000000000000, true)
      );
      assert(compute.awaiting_environment);
      assert(compute.pending.phase == PhaseFpCompute);
      assert(compute.pending.repeat_parent_active);
      assert(not_bool(compute.pending.repeat_parent_grouped));
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
        ) with address_type = 0, cache_policy = 7 }
      );
      assert(block.request.kind == CacheMaintenanceBlock);
      assert(block.request.range_start == 0x000000000000A040);
      assert(block.request.range_end == 0x000000000000A080);
      assert(block.request.address_translation == false);
      assert(block.request.address_type == 0);
      assert(block.request.cache_policy == 7);
      let device = resume_transaction(
        translating, { successful_response(
          ResponseAddressTranslation, 0x000000000000B000, true
        ) with address_type = 1, cache_policy = 3 }
      );
      assert(not_bool(device.awaiting_environment));
      assert(device.fault == None());
      assert(device.request.kind == NoPrimitiveRequest);
      assert(device.state.pc == 0x0000000000000004)
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
      let l3 = resume_transaction(l4, pte_response(0x000000000000280F));
      assert(l3.request.range_start == 0x0000000000002688);
      let l2 = resume_transaction(l3, pte_response(0x000000000000380F));
      assert(l2.request.range_start == 0x0000000000003598);
      let l1 = resume_transaction(l2, pte_response(0x000000000000480F));
      assert(l1.request.range_start == 0x0000000000004C48);
      let done = resume_transaction(l1, pte_response(0x00000000ABCDE00F));
      assert(done.state.registers[0] == 0x00000000ABCDEABC);
      assert(done.state.flags == 0b1111);
      let malformed_l3 = resume_transaction(l3, pte_response(0x000000000000384F));
      assert(malformed_l3.state.registers[0] == 0x0000000000000000);
      assert(malformed_l3.state.flags == 0b0000);
      let unreadable = resume_transaction(l4, failing_response(ResponsePteRead));
      assert(unreadable.fault != None());
      assert(unreadable.state == state)
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
      let l3 = resume_transaction(l4, pte_response(0x000000000000280F));
      let raw = resume_transaction(l3, pte_response(0x000000000000384F));
      assert(raw.state.registers[0] == 0x000000000000384F);
      assert(raw.state.flags == 0b0000);
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

  match decode_full_record([|0x06|]) {
    Some(instruction) => {
      var state = initial_cpu();
      state.supervisor = true; state.status = 0x0000000000000010;
      state.controls[11] = 0x0000000100000000;
      state.controls[10] = 0x0000000000001003;
      state.controls[7] = 0x0000000000003000;
      let rejected = execute_full(instruction, state);
      assert(not_bool(rejected.awaiting_environment));
      assert(rejected.fault != None());
      assert(rejected.state == state)
    },
    None() => assert(false),
  };

  match decode_full_record([|0x01|]) {
    Some(instruction) => {
      var inactive = initial_cpu(); inactive.event_depth = 1;
      let rejected_inactive = execute_full(instruction, inactive);
      assert(rejected_inactive.fault != None());
      assert(rejected_inactive.state == inactive);
      var active = initial_cpu();
      active.supervisor = true; active.status = 0x0000000000000011;
      active.event_depth = 1; active.event_stack_level = 1;
      let accepted = execute_full(instruction, active);
      assert(accepted.fault == None());
      assert(accepted.state.pc == 0x0000000000000001);
      var invalid_active = active; invalid_active.event_stack_level = 0;
      let rejected_active = execute_full(instruction, invalid_active);
      assert(rejected_active.fault != None());
      assert(rejected_active.state == invalid_active)
    },
    None() => assert(false),
  };

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

