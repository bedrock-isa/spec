function test_event_boundaries() -> unit =
  match (decode_full_record([|0x01|]), decode_full_record([|0x07|]),
         decode_full_record([|0x04|]), decode_full_record([|0x0A|])) {
    (Some(nop), Some(bkpt), Some(eret), Some(rfence)) => {
      /* Machine check wins over NMI and IRQ and performs a real entry commit. */
      let all_ingress = event_test_ingress(
        true, 0xA5A55A5A, true, 0x112233, true, 0x445566
      );
      let machine_boundary = execute_boundary(
        nop, event_test_entry_state(), all_ingress
      );
      match machine_boundary.admitted {
        Some(event) => {
          assert(event.code == 0x00000019);
          assert(event.frame_type == EventFrameAuxiliary);
          assert(event.event_aux == 0x00000000A5A55A5A)
        },
        None() => assert(false),
      };
      match machine_boundary.execution {
        Some(target) => {
          assert(target.request.kind == TranslationExecuteProbe);
          let done = event_test_finish_entry(target);
          assert(not_bool(done.awaiting_environment));
          assert(done.fault == None());
          assert(done.pending.kind == CommitEvent);
          assert(done.state.pc == 0x0000000000000200);
          assert(done.state.event_depth == 1);
          assert(done.state.event_stack_level == 2);
          assert(done.state.sp == 0x0000000000008FA0);
          assert(not_bool(done.state.machine_check_pending));
          assert(done.state.controls[2][7] == bitone);
          assert(done.state.nmi_latched_source == 0x112233)
        },
        None() => assert(false),
      };

      /* NMI is latched while V=0 and is admitted after V is enabled. */
      var disabled = event_test_entry_state();
      disabled.controls[2] = 0x0000000000000400;
      let latched_boundary = execute_boundary(
        nop, disabled,
        event_test_ingress(false, 0x00000000, true, 0xABCDEF,
                           false, 0x000000)
      );
      assert(latched_boundary.admitted == None());
      match latched_boundary.execution {
        Some(executed) => {
          assert(executed.state.controls[2][7] == bitone);
          assert(executed.state.nmi_latched_source == 0xABCDEF);
          var enabled = executed.state;
          enabled.controls[2] = enabled.controls[2] | 0x0000000000000001;
          let admitted = execute_boundary(nop, enabled, event_test_no_ingress());
          match admitted.admitted {
            Some(event) => {
              assert(event.kind == EventNmi);
              assert(event.code == 0x02ABCDEF)
            },
            None() => assert(false),
          }
        },
        None() => assert(false),
      };

      /* A second observed NMI survives the first NMI's outstanding entry. */
      let first_nmi = execute_boundary(
        nop, event_test_entry_state(),
        event_test_ingress(false, 0x00000000, true, 0x010203,
                           false, 0x000000)
      );
      match first_nmi.execution {
        Some(first_target) => {
          let relatched_boundary = resume_boundary(
            first_target, first_target.state.status,
            event_test_ingress(false, 0x00000000, true, 0xA0B0C0,
                               false, 0x000000)
          );
          match relatched_boundary.execution {
            Some(rebased) => {
              assert(rebased.pending.before.nmi_relatched);
              assert(rebased.pending.before.nmi_relatched_source == 0xA0B0C0);
              let done = event_test_finish_entry(rebased);
              assert(done.state.controls[2][7] == bitone);
              assert(done.state.nmi_latched_source == 0xA0B0C0);
              assert(not_bool(done.state.nmi_relatched));
              assert(done.state.status[1] == bitone)
            },
            None() => assert(false),
          }
        },
        None() => assert(false),
      };

      /* BKPT ignores MAX_EDEPTH, but still requires V and the hard depth limit. */
      var zero_max = event_test_entry_state();
      zero_max.controls[2] = 0x0000000000000001;
      let bkpt_done = event_test_finish_entry(execute_full(bkpt, zero_max));
      assert(bkpt_done.state.event_depth == 1);
      assert(bkpt_done.state.pc == zero_max.controls[12]);
      var no_vector = event_test_entry_state();
      no_vector.controls[2] = 0x0000000000000000;
      let no_vector_result = execute_full(bkpt, no_vector);
      assert(no_vector_result.state.run_state == Shutdown);
      var full_depth = event_test_entry_state();
      full_depth.supervisor = true;
      full_depth.status = 0x0000000000000011;
      full_depth.event_depth = 15;
      full_depth.event_stack_level = 2;
      full_depth.controls[2] = 0x0000000000000001;
      let depth_result = execute_full(bkpt, full_depth);
      assert(depth_result.state.run_state == Shutdown);

      /* A lower-level nested interrupt retains the current SS:SP and stack level. */
      var nested = event_test_entry_state();
      nested.supervisor = true;
      nested.status = 0x0000000000000031;
      nested.event_depth = 1;
      nested.event_stack_level = 2;
      nested.segments[2] = 0x0000000000000000;
      nested.sp = 0x0000000000007000;
      let nested_boundary = execute_boundary(
        nop, nested,
        event_test_ingress(false, 0x00000000, false, 0x000000,
                           true, 0x123456)
      );
      match nested_boundary.execution {
        Some(target) => {
          let range = resume_transaction(
            target, event_test_response(ResponseTranslation, true)
          );
          assert(range.request.segment_image == nested.segments[2]);
          assert(range.request.range_start == 0x0000000000006FC0);
          let store = resume_transaction(
            range, event_test_response(ResponseStackRange, true)
          );
          assert(store.request.segment_image == nested.segments[2]);
          let done = resume_transaction(
            store, event_test_response(ResponseEventFrame, true)
          );
          assert(done.state.event_depth == 2);
          assert(done.state.event_stack_level == 2);
          assert(done.state.segments[2] == nested.segments[2]);
          assert(done.state.sp == 0x0000000000006FC0)
        },
        None() => assert(false),
      };

      /* Target, stack-state, stack-range, and frame-store failures encode stages 0..3. */
      let original = make_event(
        EventSynchronous, EventFrameBasic, 0x00000002, 4,
        0x0000000000001001
      );
      let stage0 = resume_transaction(
        start_admitted_event(original, event_test_entry_state()),
        event_test_response(ResponseTranslation, false)
      );
      event_test_assert_double_fault(stage0, 0);

      var bad_stack = event_test_entry_state();
      bad_stack.controls[20] = 0x0000000000009001;
      let stage1 = resume_transaction(
        start_admitted_event(original, bad_stack),
        event_test_response(ResponseTranslation, true)
      );
      event_test_assert_double_fault(stage1, 1);

      let stage2_range = resume_transaction(
        start_admitted_event(original, event_test_entry_state()),
        event_test_response(ResponseTranslation, true)
      );
      let stage2 = resume_transaction(
        stage2_range, event_test_response(ResponseStackRange, false)
      );
      event_test_assert_double_fault(stage2, 2);

      let stage3_range = resume_transaction(
        start_admitted_event(original, event_test_entry_state()),
        event_test_response(ResponseTranslation, true)
      );
      let stage3_store = resume_transaction(
        stage3_range, event_test_response(ResponseStackRange, true)
      );
      let stage3 = resume_transaction(
        stage3_store, event_test_response(ResponseEventFrame, false)
      );
      event_test_assert_double_fault(stage3, 3);

      let failed_double_fault = resume_transaction(
        stage0, event_test_response(ResponseTranslation, false)
      );
      assert(failed_double_fault.state.run_state == Shutdown);
      assert(not_bool(failed_double_fault.awaiting_environment));

      /* RF suppresses a trace, remains set while a unit is pending, and clears on success. */
      var rf_state = event_test_entry_state();
      rf_state.status = 0x000000000000000C;
      let pending_fence = execute_full(rfence, rf_state);
      let pending_boundary = resume_boundary(
        pending_fence, rf_state.status, event_test_no_ingress()
      );
      assert(pending_boundary.state.status[3] == bitone);
      assert(pending_boundary.admitted == None());
      let completed_nop = execute_full(nop, rf_state);
      let suppressed = resume_boundary(
        completed_nop, rf_state.status, event_test_no_ingress()
      );
      assert(suppressed.admitted == None());
      assert(suppressed.state.status[3] == bitzero);
      assert(suppressed.state.status[2] == bitone);
      let trace_nop = execute_full(nop, suppressed.state);
      let traced = resume_boundary(
        trace_nop, suppressed.state.status, event_test_no_ingress()
      );
      match traced.admitted {
        Some(event) => {
          assert(event.kind == EventDebugTrace);
          assert(event.code == 0x00000000)
        },
        None() => assert(false),
      };

      /* Halted wakes only when event entry commits; Shutdown never wakes asynchronously. */
      var halted = event_test_entry_state();
      halted.run_state = Halted;
      halted.halted = true;
      let sleeping = execute_boundary(nop, halted, event_test_no_ingress());
      assert(sleeping.execution == None());
      assert(sleeping.state.run_state == Halted);
      let waking = execute_boundary(
        nop, halted,
        event_test_ingress(false, 0x00000000, true, 0x0BADF0,
                           false, 0x000000)
      );
      match waking.execution {
        Some(target) => {
          assert(target.state.run_state == Halted);
          let range = resume_transaction(
            target, event_test_response(ResponseTranslation, true)
          );
          assert(range.state.run_state == Halted);
          let store = resume_transaction(
            range, event_test_response(ResponseStackRange, true)
          );
          assert(store.state.run_state == Halted);
          let awake = resume_transaction(
            store, event_test_response(ResponseEventFrame, true)
          );
          assert(awake.state.run_state == Running);
          assert(not_bool(awake.state.halted));
          let failed = resume_transaction(
            target, event_test_response(ResponseTranslation, false)
          );
          assert(failed.state.run_state == Halted)
        },
        None() => assert(false),
      };
      var shutdown = event_test_entry_state();
      shutdown.run_state = Shutdown;
      let no_wake = execute_boundary(nop, shutdown, all_ingress);
      assert(no_wake.execution == None());
      assert(no_wake.state.run_state == Shutdown);
      let reset = platform_reset(no_wake.state);
      assert(reset.run_state == Running);
      assert(not_bool(reset.halted));
      assert(reset.pc == shutdown.controls[23]);

      /* ERET validates a saved REPG interior and resumes at its saved body offset. */
      var active = event_test_entry_state();
      active.supervisor = true;
      active.status = 0x0000000000000011;
      active.event_depth = 1;
      active.event_stack_level = 2;
      active.sp = 0x0000000000006000;
      active.registers[0] = 0xA5A5A5A55A5A5A5A;
      active.registers[1] = 0x1122334455667788;
      active.registers[2] = 0xFFEEDDCCBBAA0099;
      active.registers[3] = 0x0000000000000002;
      let frame_control : bits(64) = 0x0000000000040008;
      let frame_ext1 : bits(64) = 0x0000000300010103;
      let saved_pc : bits(64) = 0x0000000000001001;
      let header = execute_full(eret, active);
      assert(header.pending.phase == PhaseEventFrameHeader);
      let frame_read = resume_transaction(
        header, event_test_response_bytes(
          ResponseEventFrame, le64_bytes(frame_control)
        )
      );
      assert(frame_read.pending.phase == PhaseEventFrame);
      let body_probe = resume_transaction(
        frame_read, event_test_response_bytes(
          ResponseEventFrame,
          event_test_frame(
            frame_control, 0x0000000000000002, frame_ext1, saved_pc,
            0x0000000000007000, 0x0000000000000000,
            0x0000000000000000, 0x0000000000000000
          )
        )
      );
      assert(body_probe.pending.phase == PhaseEventReturnBody);
      assert(body_probe.request.range_start == 0x0000000000001000);
      assert(body_probe.request.range_length == 3);
      let return_probe = resume_transaction(
        body_probe,
        event_test_response_bytes(ResponseRepeatFetch, [|0x60, 0x81, 0x12|])
      );
      assert(return_probe.pending.phase == PhaseEventReturnExecute);
      assert(return_probe.request.effective_address == saved_pc);
      let returned = resume_transaction(
        return_probe, event_test_response(ResponseTranslation, true)
      );
      assert(returned.fault == None());
      assert(returned.state.pc == saved_pc);
      assert(returned.state.repeat_state.active);
      assert(returned.state.repeat_state.grouped);
      assert(returned.state.repeat_state.body_start == 0x0000000000001000);
      assert(returned.state.repeat_state.group_progress == 1);
      let resumed = execute_boundary(
        nop, returned.state, event_test_no_ingress()
      );
      match resumed.execution {
        Some(done) => {
          assert(done.fault == None());
          assert(done.state.registers[0] == 0xA5A5A5A55A5A5A5A);
          assert(done.state.registers[2] == 0x1122334455667788);
          assert(done.state.registers[3] == 0x0000000000000001);
          assert(done.state.pc == 0x0000000000001000);
          assert(done.state.repeat_state.active)
        },
        None() => assert(false),
      }
    },
    _ => assert(false),
  }
