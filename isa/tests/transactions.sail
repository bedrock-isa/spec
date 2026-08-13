function test_non_fp_typed_families() -> unit = {
  match decode_full_record([|0xCB, 0xF1, 0x44, 0x00, 0x10|]) {
    Some(instruction) => {
      var state = initial_cpu();
      state.registers[0] = 0x1122334455667788;
      let pending = execute_full(instruction, state);
      assert(pending.request.kind == AtomicReadModifyWrite);
      assert(pending.pending.phase == PhaseAtomicRmw);
      assert(pending.request.expected == 0x0000000000000088);
      let failed = resume_transaction(pending, failing_response(ResponseAtomic));
      assert(failed.state == state);
      let response = { successful_response(
        ResponseAtomic, 0x0000000000000088, true
      ) with atomic_store_happened = true, state_image = { initial_cpu() with
        sp = 0xFFFFFFFFFFFFFFFF
      } };
      let done = resume_transaction(pending, response);
      assert(done.state.registers[0] == 0x1122334455667788);
      assert(done.state.flags == 0b1000);
      assert(done.state.sp == state.sp);
      let unequal = resume_transaction(
        pending, { successful_response(ResponseAtomic, 0x0000000000000042, true) with
                   atomic_store_happened = false }
      );
      assert(unequal.state.registers[0] == 0x1122334455667742);
      assert(unequal.state.flags == 0b0000);
      let poison_equal = resume_transaction(
        pending, { successful_response(ResponseAtomic, 0x0000000000000088, true) with
                   atomic_store_happened = false }
      );
      assert(poison_equal.state == state);
      assert(poison_equal.fault != None());
      let poison_unequal = resume_transaction(
        pending, { successful_response(ResponseAtomic, 0x0000000000000042, true) with
                   atomic_store_happened = true }
      );
      assert(poison_unequal.state == state);
      assert(poison_unequal.fault != None())
    },
    None() => assert(false),
  };

  match decode_full_record([|0xCB, 0xF1, 0x40, 0x00, 0x10|]) {
    Some(instruction) => {
      var state = initial_cpu(); state.registers[0] = 0x0000000000000007;
      let pending = execute_full(instruction, state);
      assert(pending.request.kind == AtomicReadModifyWrite);
      let unacknowledged = resume_transaction(
        pending, successful_response(ResponseAtomic, 0x000000000000002A, true)
      );
      assert(unacknowledged.state == state);
      assert(unacknowledged.fault != None());
      let acknowledged = resume_transaction(
        pending, { successful_response(ResponseAtomic, 0x000000000000002A, true) with
                   atomic_store_happened = true }
      );
      assert(acknowledged.fault == None());
      assert(acknowledged.state.registers[0] == 0x000000000000002A)
    },
    None() => assert(false),
  };

  match decode_full_record([|0xC7, 0xC8, 0x00, 0x10|]) {
    Some(instruction) => {
      var state = initial_cpu(); state.registers[0] = 0x0000000000002000;
      let pending = execute_full(instruction, state);
      assert(pending.request.kind == NonTemporalStore);
      assert(pending.pending.phase == PhaseDestinationWrite)
    },
    None() => assert(false),
  };
  match decode_full_record([|0xC7, 0xEF, 0x43, 0x10|]) {
    Some(instruction) => {
      var state = initial_cpu(); state.registers[0] = 0x0000000000000037;
      state.segments[1] = 0x0000000000001002;
      state.controls[0] = 0x0000000000001001;
      state.cache_maintenance_granule = 64;
      let translating = execute_full(instruction, state);
      assert(translating.request.kind == AddressTranslateRequest);
      assert(translating.pending.phase == PhaseCacheTranslate);
      assert(translating.request.effective_address == 0x0000000000000037);
      assert(translating.request.linear_address == 0x0000000000001037);
      assert(translating.request.state_image.controls[0] == state.controls[0]);
      let pending = resume_transaction(
        translating, successful_response(ResponseAddressTranslation, 0x0000000000005037, true)
      );
      assert(pending.request.kind == PrefetchHint);
      assert(pending.request.suppress_fault);
      assert(pending.request.range_start == 0x0000000000005037);
      let ignored = resume_transaction(pending, failing_response(ResponseCacheMaintenance));
      assert(ignored.fault == None());
      assert(ignored.state.pc == 0x0000000000000004)
    },
    None() => assert(false),
  };
  match decode_full_record([|0xC7, 0xEF, 0x46, 0x01|]) {
    Some(instruction) => {
      let state = { initial_cpu() with supervisor = true, status = 0x0000000000000010 };
      let pending = execute_full(instruction, state);
      assert(pending.request.kind == TlbInvalidateRequest);
      let mismatch = resume_transaction(
        pending, successful_response(ResponseTranslationQuery, 0x0000000000000000, true)
      );
      assert(mismatch.state == state);
      assert(mismatch.fault != None())
    },
    None() => assert(false),
  };
  match decode_full_record([|0xC0, 0x27, 0x00|]) {
    Some(instruction) => {
      var state = initial_cpu(); state.registers[0] = 0x0000000200040000;
      let pending = execute_full(instruction, state);
      assert(pending.request.kind == CpuidQueryRequest);
      assert(pending.request.selector == state.registers[0]);
      let done = resume_transaction(
        pending, { successful_response(
          ResponseCpuidQuery, 0x123456789ABCDEF0, true
        ) with write_flags = true, flags = 0b1111, generated_fflags = 0b11111,
               state_image = { initial_cpu() with sp = 0xFFFFFFFFFFFFFFFF } }
      );
      assert(done.state.registers[0] == 0x123456789ABCDEF0);
      assert(done.state.flags == state.flags);
      assert(done.state.fflags == state.fflags);
      assert(done.state.sp == state.sp)
    },
    None() => assert(false),
  };
  match decode_full_record([|0x0A|]) {
    Some(instruction) => {
      let pending = execute_full(instruction, initial_cpu());
      assert(pending.request.kind == FenceCompletion);
      assert(pending.pending.phase == PhaseFenceCompletion)
    },
    None() => assert(false),
  };
  match decode_full_record([|0xA0, 0x4E|]) {
    Some(instruction) => {
      var state = initial_cpu(); state.supervisor = true;
      state.status = 0x0000000000000010;
      state.controls[23] = 0x0000000000004000;
      state.controls[24] = 0xABCDEF0123456789;
      state.registers[1] = 0xFFFFFFFFFFFFFFFF;
      state.fp_enabled = true; state.fptrans_enabled = true;
      state.floating_registers[0] = 0x0123456789ABCDEF;
      state.fflags = 0b10101; state.fstatus = 0x0000000000000155;
      let pending = execute_full(instruction, state);
      assert(pending.request.kind == ResetSerializeRequest);
      let done = resume_transaction(
        pending, successful_response(ResponseResetSerialize, 0x0000000000000000, true)
      );
      assert(done.state.pc == state.controls[23]);
      assert(done.state.controls[23] == state.controls[23]);
      assert(done.state.controls[24] == state.controls[24]);
      assert(done.state.registers[1] == 0x0000000000000000);
      assert(done.state.status == 0x0000000000000010);
      assert(done.state.fp_enabled);
      assert(done.state.fptrans_enabled);
      assert(done.state.floating_registers[0] == 0x0000000000000000);
      assert(done.state.fflags == 0b00000);
      assert(done.state.fstatus == 0x0000000000000000)
    },
    None() => assert(false),
  };
  match decode_full_record([|0x07|]) {
    Some(instruction) => {
      var state = initial_cpu();
      state.controls[2] = 0x0000000000000401;
      state.controls[12] = 0x0000000000000200;
      state.controls[19] = 0x0000000000000000;
      state.controls[20] = 0x0000000000001000;
      let target = execute_full(instruction, state);
      assert(target.pending.phase == PhaseEventTargetProbe);
      let range = resume_transaction(
        target, successful_response(ResponseTranslation, 0x0000000000000000, true)
      );
      assert(range.pending.phase == PhaseEventStackProbe);
      assert(range.request.range_length == 64);
      let store = resume_transaction(
        range, successful_response(ResponseStackRange, 0x0000000000000000, true)
      );
      assert(store.request.kind == EventFrameAccess);
      assert(store.pending.phase == PhaseEventFrameStore);
      let done = resume_transaction(
        store, successful_response(ResponseEventFrame, 0x0000000000000000, true)
      );
      assert(done.state.pc == state.controls[12]);
      assert(done.state.status[4] == bitone);
      assert(done.state.status[0] == bitone);
      assert(done.state.event_depth == 1)
    },
    None() => assert(false),
  };
  match decode_full_record([|0xC2, 0x40, 0x00|]) {
    Some(instruction) => {
      var state = initial_cpu(); state.registers[0] = 0x0000000000000003;
      let pending = execute_full(instruction, state);
      assert(pending.request.kind == RepeatBodyFetch);
      let response = { successful_response(ResponseRepeatFetch, 0x0000000000000000, true) with
        body_bytes = [|0x60|] };
      let first = resume_transaction(pending, response);
      assert(first.pending.boundary_class == BoundaryRepeatIteration);
      let second_boundary = execute_boundary(instruction, first.state, no_async_ingress());
      let second : Execution_result = match second_boundary.execution {
        Some(result) => result,
        None() => first,
      };
      let final_boundary = execute_boundary(instruction, second.state, no_async_ingress());
      let done : Execution_result = match final_boundary.execution {
        Some(result) => result,
        None() => second,
      };
      assert(not_bool(done.awaiting_environment));
      assert(done.state.registers[0] == 0x0000000000000000);
      assert(done.state.pc == 0x0000000000000004);
      assert(not_bool(done.state.repeat_state.active))
    },
    None() => assert(false),
  };
  match decode_full_record([|0xC2, 0x20, 0x68|]) {
    Some(instruction) => {
      var state = initial_cpu(); state.sp = 0x1122334455667788;
      state.registers[0] = 0xAABBCCDDEEFF0011;
      let done = execute_full(instruction, state);
      assert(done.state.sp == 0x1122334455667711);
      assert(done.state.registers[0] == 0xAABBCCDDEEFF0088)
    },
    None() => assert(false),
  };
  match decode_full_record([|0xC3, 0x40, 0x10|]) {
    Some(instruction) => {
      var state = initial_cpu(); state.registers[0] = 0xFFFFFFFFFFFFFF80;
      let pending = execute_full(instruction, state);
      assert(pending.request.kind == MemoryStore);
      assert(pending.request.width == 2);
      assert(pending.request.value == 0x0000000000000080)
    },
    None() => assert(false),
  }
}

function test_typed_decode_and_transactions() -> unit = {
  assert(decode_full_record_outcome([||]).stage == DecodeFetch);
  assert(decode_full_record_outcome([|0x80|]).stage == DecodeFraming);
  let disabled_fpu_bad_ea = decode_and_execute_full_outcome(
    [|0xCB, 0xD5, 0x08, 0x74, 0xFF|], initial_cpu()
  );
  assert(disabled_fpu_bad_ea.decode.stage == DecodeEaDescriptor);
  match disabled_fpu_bad_ea.execution {
    Some(result) => match result.fault {
      Some(fault) => assert(fault.kind == ExtensionUnavailable),
      None() => assert(false),
    },
    None() => assert(false),
  };
  let jcc = decode_and_execute_full_outcome([|0xB2, 0x00|], initial_cpu());
  match jcc.execution {
    Some(result) => {
      assert(not_bool(result.awaiting_environment));
      assert(result.request.kind == NoPrimitiveRequest)
    },
    None() => assert(false),
  };
  var invalid_control = initial_cpu();
  invalid_control.segments[0] = 0xFFFFFFFFFFFFFFFF;
  let state_before_predicate = decode_and_execute_full_outcome([|0xB2, 0x00|], invalid_control);
  match state_before_predicate.execution {
    Some(result) => match result.fault {
      Some(fault) => assert(fault.kind == InvalidControlState),
      None() => assert(false),
    },
    None() => assert(false),
  };
  match decode_full_record([|0xC0, 0x10, 0x00|]) {
    Some(instruction) => {
      var state = initial_cpu(); state.registers[0] = 0x0000000000001234;
      let evaluated = evaluate_ea_operands_in_order(instruction.operands, state, state.pc, 1);
      match evaluation_named("src", evaluated.evaluations) {
        Some(source) => assert(source.effective_address == 0x0000000000001234),
        None() => assert(false),
      }
    },
    None() => assert(false),
  };
  match (decode_full_record([|0xCD, 0xE4, 0x05, 0x90, 0x22, 0x7F|]),
         decode_full_record([|0xCD, 0xE4, 0x05, 0x91, 0x22, 0x7F|])) {
    (Some(post_instruction), Some(pre_instruction)) => {
      var state = initial_cpu(); state.registers[2] = 0x000000000000000A;
      let post = evaluate_ea_operands_in_order(
        post_instruction.operands, state, state.pc, operation_width(post_instruction)
      );
      let pre = evaluate_ea_operands_in_order(
        pre_instruction.operands, state, state.pc, operation_width(pre_instruction)
      );
      match (evaluation_named("dst", post.evaluations), evaluation_named("dst", pre.evaluations)) {
        (Some(post_ea), Some(pre_ea)) => {
          assert(post_ea.effective_address == 0x0000000000000093);
          assert(pre_ea.effective_address == 0x0000000000000092);
          assert(post.image.registers[2] == 0x000000000000000B);
          assert(pre.image.registers[2] == 0x0000000000000009)
        },
        _ => assert(false),
      }
    },
    _ => assert(false),
  };
  match decode_full_record([|0xC7, 0xC6, 0x00, 0x00|]) {
    Some(instruction) => {
      var state = initial_cpu(); state.registers[0] = 0x0000000000004567;
      let result = execute_full(instruction, state);
      assert(not_bool(result.awaiting_environment));
      assert(result.state.registers[0] == 0x0000000000004567);
      assert(not_bool(flag_v(result.state.flags)))
    },
    None() => assert(false),
  };
  match decode_full_record([|0xC7, 0xC6, 0x00, 0x00|]) {
    Some(instruction) => {
      var state = initial_cpu(); state.segments[1] = 0x0000000000000002;
      state.registers[0] = 0x0000000000001000;
      let result = execute_full(instruction, state);
      assert(result.state.registers[0] == 0x0000000000001000);
      assert(flag_v(result.state.flags));
      assert(result.state.pc == 0x0000000000000004)
    },
    None() => assert(false),
  };
  match decode_full_record([|0x20|]) {
    Some(instruction) => {
      var state = initial_cpu(); state.sp = 0x0000000000000100;
      state.registers[0] = 0x1122334455667788;
      let range = execute_full(instruction, state);
      assert(range.request.kind == StackRange);
      assert(range.request.range_start == 0x00000000000000F8);
      let mismatch = resume_transaction(range, successful_response(
        ResponseStoreAck, 0x0000000000000000, true
      ));
      assert(mismatch.state == state);
      match mismatch.fault {
        Some(fault) => assert(fault.kind == InvalidControlState),
        None() => assert(false),
      };
      let failed = resume_transaction(range, failing_response(ResponseStackRange));
      assert(failed.state == state);
      let store = resume_transaction(range, successful_response(
        ResponseStackRange, 0x0000000000000000, true
      ));
      assert(store.request.kind == MemoryStore);
      assert(store.request.value == state.registers[0]);
      let done = resume_transaction(store, successful_response(
        ResponseStoreAck, 0x0000000000000000, true
      ));
      assert(done.state.sp == 0x00000000000000F8)
    },
    None() => assert(false),
  }
}

