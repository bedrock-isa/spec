function event_test_ingress(machine_check : bool, machine_check_code : bits(32),
                            nmi : bool, nmi_source : bits(24),
                            interrupt : bool, interrupt_id : bits(24))
  -> Async_ingress = struct {
  machine_check_pending = machine_check, machine_check_code = machine_check_code,
  machine_check_error_code = 0x0000000000000000,
  machine_check_fault_ea = 0x0000000000000000,
  machine_check_fault_linear = 0x0000000000000000,
  machine_check_event_aux = 0x0000000000000000,
  nmi_pending = nmi, nmi_source = nmi_source,
  interrupt_pending = interrupt, interrupt_id = interrupt_id
}

function event_test_no_ingress() -> Async_ingress = event_test_ingress(
  false, 0x00000000, false, 0x000000, false, 0x000000
)

function event_test_response(kind : Transaction_response_kind,
                             success : bool) -> Transaction_response = struct {
  kind = kind, success = success,
  fault_kind = if success then NoFault else AccessFault,
  detail = if success then "" else "event test access fault",
  value = 0x0000000000000000, secondary_value = 0x0000000000000000,
  flags = 0x0, write_flags = false, generated_fflags = 0b00000,
  bounds_passed = success, address_type = 0, cache_policy = 0,
  atomic_store_happened = false, body_bytes = [||],
  state_image = initial_cpu(), known = success, present = success,
  fp_response = empty_fp_response()
}

function event_test_response_bytes(kind : Transaction_response_kind,
                                   bytes : list(bits(8))) -> Transaction_response =
  { event_test_response(kind, true) with body_bytes = bytes }

function event_test_entry_state() -> Cpu_state = {
  var state = initial_cpu();
  state.pc = 0x0000000000001000;
  state.sp = 0x0000000000007000;
  state.controls[2] = 0x0000000000000401;
  state.controls[12] = 0x0000000000000200;
  state.controls[13] = 0x0000000000000000;
  state.controls[14] = 0x0000000000000000;
  state.controls[17] = 0x0000000000000000;
  state.controls[18] = 0x0000000000008000;
  state.controls[19] = 0x0000000000000000;
  state.controls[20] = 0x0000000000009000;
  state.controls[21] = 0x0000000000000000;
  state.controls[22] = 0x000000000000A000;
  state.controls[23] = 0x0000000000004000;
  state
}

function event_test_finish_entry(target : Execution_result) -> Execution_result = {
  assert(target.awaiting_environment);
  assert(target.pending.phase == PhaseEventTargetProbe);
  let range = resume_transaction(
    target, event_test_response(ResponseTranslation, true)
  );
  assert(range.awaiting_environment);
  assert(range.pending.phase == PhaseEventStackProbe);
  let store = resume_transaction(
    range, event_test_response(ResponseStackRange, true)
  );
  assert(store.awaiting_environment);
  assert(store.pending.phase == PhaseEventFrameStore);
  resume_transaction(store, event_test_response(ResponseEventFrame, true))
}

function event_test_assert_double_fault(result : Execution_result,
                                        stage : int) -> unit =
  match result.pending.event {
    Some(event) => {
      let address_bits : bits(64) = if stage >= 2
        then 0x0000000003000000 else 0x0000000000000000;
      let expected : bits(64) = bits_from_int(stage)
                                  | 0x0000000004000000 | address_bits;
      assert(result.awaiting_environment);
      assert(result.pending.phase == PhaseEventTargetProbe);
      assert(result.pending.event_attempt == 1);
      assert(event.kind == EventSynchronous);
      assert(event.frame_type == EventFrameAuxiliary);
      assert(event.code == 0x00000018);
      assert(event.error_code == expected);
      assert(event.event_aux == 0x0000000000000002)
    },
    None() => assert(false),
  }

function event_test_frame(control : bits(64), event_info : bits(64),
                          ext : bits(64), saved_pc : bits(64),
                          saved_sp : bits(64), saved_cs : bits(64),
                          saved_ds : bits(64), saved_ss : bits(64))
  -> list(bits(8)) = append_bytes(
  le64_bytes(control), append_bytes(
    le64_bytes(event_info), append_bytes(
      le64_bytes(ext), append_bytes(
        le64_bytes(saved_pc), append_bytes(
          le64_bytes(saved_sp), append_bytes(
            le64_bytes(saved_cs), append_bytes(
              le64_bytes(saved_ds), le64_bytes(saved_ss)))))))
)

