function event_frame_control(state : Cpu_state, frame_slots : int,
                             frame_type : int) -> bits(64) =
  get_slice_int(64, frame_slots, 0)
  | sail_shiftleft(get_slice_int(64, frame_type, 0), 8)
  | (if state.current_dfa then 0x0000000000001000 else 0x0000000000000000)
  | sail_shiftleft(sail_zero_extend(state.flags, 64), 32)
  | sail_shiftleft(state.status & 0x000000000000FFFF, 36)

function event_frame_type_code(frame_type : Event_frame_type) -> int = match frame_type {
  EventFrameBasic => 0, EventFrameError => 1,
  EventFramePage => 2, EventFrameAuxiliary => 3,
}

function event_frame_slots(frame_type : Event_frame_type) -> int = match frame_type {
  EventFrameBasic => 8, EventFrameError => 10,
  EventFramePage => 12, EventFrameAuxiliary => 12,
}

function make_event(kind : Event_kind, frame_type : Event_frame_type, code : bits(32),
                    priority : int, saved_pc : bits(64)) -> Event_record = struct {
  kind = kind, frame_type = frame_type, code = code, priority = priority,
  saved_pc = saved_pc, error_code = 0x0000000000000000,
  fault_ea = 0x0000000000000000, fault_linear = 0x0000000000000000,
  event_aux = 0x0000000000000000
}

function encode_event_frame(state : Cpu_state, event : Event_record,
                            control : bits(64)) -> list(bits(8)) = {
  let slot7 = le64_bytes(0x0000000000000000);
  let slot6 = append_bytes(le64_bytes(state.segments[2]), slot7);
  let slot5 = append_bytes(le64_bytes(state.segments[1]), slot6);
  let slot4 = append_bytes(le64_bytes(state.segments[0]), slot5);
  let slot3 = append_bytes(le64_bytes(state.sp), slot4);
  let slot2 = append_bytes(le64_bytes(event.saved_pc), slot3);
  let slot1 = append_bytes(le64_bytes(sail_zero_extend(event.code, 64)), slot2);
  let basic = append_bytes(le64_bytes(control), slot1);
  if event.frame_type == EventFrameBasic then basic
  else if event.frame_type == EventFrameError then append_bytes(
    basic, append_bytes(le64_bytes(event.error_code), le64_bytes(0x0000000000000000))
  )
  else append_bytes(basic, append_bytes(
    le64_bytes(event.error_code), append_bytes(
      le64_bytes(event.fault_ea), append_bytes(
        le64_bytes(event.fault_linear), le64_bytes(event.event_aux))))
  )
}

function event_uses_user_bank(state : Cpu_state) -> bool =
  not_bool(state.supervisor) & status_event_depth(state.status) == 0

function event_payload_slots(frame_type : Event_frame_type) -> int = match frame_type {
  EventFrameBasic => 0, EventFrameError => 2,
  EventFramePage => 4, EventFrameAuxiliary => 4,
}

function event_storage_slots(event : Event_record, state : Cpu_state) -> int =
  if event_uses_user_bank(state) then event_payload_slots(event.frame_type)
  else event_frame_slots(event.frame_type)

function event_stack_segment(event : Event_record, state : Cpu_state) -> bits(64) =
  if event.code == 0x00000018 then state.controls[21]
  else if not_bool(event_uses_user_bank(state)) then state.segments[2]
  else if event.code == 0x00000020 then state.controls[15]
  else if event.kind == EventInterrupt then state.controls[17]
  else state.controls[19]

function event_stack_top(event : Event_record, state : Cpu_state) -> bits(64) =
  if event.code == 0x00000018 then state.controls[22]
  else if not_bool(event_uses_user_bank(state)) then state.sp
  else if event.code == 0x00000020 then state.controls[16]
  else if event.kind == EventInterrupt then state.controls[18]
  else state.controls[20]

function event_entry_state_valid(state : Cpu_state) -> bool =
  segment_image_valid(state.controls[13])
  & segment_image_valid(state.controls[14])
  & (state.controls[12] & 0x000000000000000F) == 0x0000000000000000
  & paging_canonical(state.controls[12], state.controls[0])
  & segment_point(state.controls[13], state.controls[12]).in_bounds

function event_stack_state_valid(event : Event_record, state : Cpu_state) -> bool = {
  let segment_image = event_stack_segment(event, state);
  let top = event_stack_top(event, state);
  segment_image_valid(segment_image)
  & (top & (if event_uses_user_bank(state) | event.code == 0x00000018
            then 0x000000000000003F
            else 0x000000000000000F)) == 0x0000000000000000
}

function event_frame_address_valid(event : Event_record, state : Cpu_state) -> bool = {
  let segment_image = event_stack_segment(event, state);
  let top = event_stack_top(event, state);
  let frame_bytes = event_storage_slots(event, state) * 8;
  segment_point(segment_image, sub_bits(top, bits_from_int(frame_bytes))).in_bounds
}

function event_target_request(state : Cpu_state) -> Primitive_request =
  { target_probe_request(0, state.controls[13], state.controls[12]) with
    role = RequestRoleEventEntryTarget }

function event_stack_range_request(event : Event_record, state : Cpu_state,
                                   ordinal : int) -> Primitive_request = {
  let segment_image = event_stack_segment(event, state);
  let top = event_stack_top(event, state);
  let frame_bytes = event_storage_slots(event, state) * 8;
  let frame_start = sub_bits(top, bits_from_int(frame_bytes));
  let point = segment_point(segment_image, frame_start);
  { stack_request(StackRange, ordinal, state, frame_start, top, AccessStackWrite,
                  0x0000000000000000, false) with
    role = RequestRoleEventFrameRange, segment_image = segment_image,
    effective_address = frame_start, linear_address = point.linear,
    width = frame_bytes, range_length = frame_bytes }
}

function event_frame_store_request(event : Event_record, state : Cpu_state,
                                   ordinal : int) -> Primitive_request = {
  let range = event_stack_range_request(event, state, ordinal);
  let control = event_frame_control(
    state, event_frame_slots(event.frame_type), event_frame_type_code(event.frame_type)
  );
  let payload = if event.frame_type == EventFrameError then
    append_bytes(le64_bytes(event.error_code), le64_bytes(0x0000000000000000))
  else if event.frame_type == EventFramePage | event.frame_type == EventFrameAuxiliary then
    append_bytes(le64_bytes(event.error_code), append_bytes(
      le64_bytes(event.fault_ea), append_bytes(
        le64_bytes(event.fault_linear), le64_bytes(event.event_aux))))
  else [||];
  { range with kind = EventFrameAccess, role = RequestRoleEventFrameStore,
    access = AccessStackWrite, commit_point = true,
    selector = sail_zero_extend(event.code, 64), value = control,
    expected = event.saved_pc,
    payload_bytes = if event_uses_user_bank(state) then payload
                    else encode_event_frame(state, event, control) }
}

function committed_event_entry(before : Cpu_state, event : Event_record,
                               new_sp : bits(64), stack_segment : bits(64)) -> Cpu_state = {
  var updated = before;
  let user_origin = event_uses_user_bank(before);
  if user_origin then {
    updated.controls[6] = event.saved_pc;
    updated.controls[7] = before.sp;
    updated.controls[8] = before.segments[0];
    updated.controls[9] = before.segments[1];
    updated.controls[10] = before.segments[2];
    updated.controls[11] = 0x0000000100000000
      | sail_shiftleft(before.status & 0x000000000000FFFF, 16)
      | sail_zero_extend(before.flags, 64);
    updated.controls[26] = sail_zero_extend(event.code, 64)
  } else ();
  updated.sp = new_sp;
  updated.pc = before.controls[12];
  updated.segments[0] = before.controls[13];
  updated.segments[1] = before.controls[14];
  updated.segments[2] = stack_segment;
  updated.status = status_with_event_state(
    (before.status & 0x0000000000000002) | 0x0000000000000011,
    status_event_depth(before.status) + 1,
    status_user_origin(before.status) | user_origin
  );
  if event.kind == EventNmi then
    updated.status = updated.status | 0x0000000000000002
  else ();
  if event.code == 0x00000018 then updated.current_dfa = true else ();
  updated.supervisor = true;
  updated.repeat_state = { updated.repeat_state with active = false };
  updated.run_state = Running;
  updated.halted = false;
  updated
}

function waiting_event_transaction(state : Cpu_state, event : Event_record, attempt : int,
                                   phase : Continuation_phase, ordinal : int,
                                   request : Primitive_request) -> Execution_result = struct {
  state = state,
  pending = { empty_pending(Some(state), Op_NOP, CommitEvent) with
    continuation = PendingEvent(struct {
      transaction = {
        empty_transaction_continuation() with
        phase = phase, ordinal = ordinal
      },
      event = event,
      attempt = attempt
    }),
    boundary_class = BoundaryEventEntry },
  request = request, effects = [||], fault = None(), awaiting_environment = true
}

function pending_event_record(pending : Pending_commit) -> option(Event_record) =
  match pending.continuation {
    PendingEvent(continuation) => Some(continuation.event),
    _ => None(),
  }

function pending_event_attempt(pending : Pending_commit) -> int =
  match pending.continuation {
    PendingEvent(continuation) => continuation.attempt,
    _ => 0,
  }

val start_event_attempt : (Event_record, Cpu_state, int) -> Execution_result

function double_fault_event(failed : Event_record, stage : int) -> Event_record = {
  let address_valid = stage >= 2;
  { make_event(EventSynchronous, EventFrameAuxiliary, 0x00000018, 1, failed.saved_pc) with
    error_code = bits_from_int(stage)
      | 0x0000000004000000
      | (if address_valid then 0x0000000003000000 else 0x0000000000000000),
    fault_ea = if address_valid then failed.fault_ea else 0x0000000000000000,
    fault_linear = if address_valid then failed.fault_linear else 0x0000000000000000,
    event_aux = sail_zero_extend(failed.code, 64) }
}

function event_shutdown(state : Cpu_state) -> Execution_result = completed(
  state, { state with run_state = Shutdown, halted = false }, CommitEvent, [||]
)

function start_event_attempt(event : Event_record, state : Cpu_state,
                             attempt : int) -> Execution_result =
  if state.controls[2][0] == bitzero | status_event_depth(state.status) >= 15 then event_shutdown(state)
  else if not_bool(event_entry_state_valid(state)) then
    if attempt >= 1 then event_shutdown(state)
    else start_event_attempt(double_fault_event(event, 0), state, 1)
  else waiting_event_transaction(
    state, event, attempt, PhaseEventTargetProbe, 0, event_target_request(state)
  )

function start_admitted_event(event : Event_record, state : Cpu_state) -> Execution_result =
  start_event_attempt(event, state, 0)

function event_delivery_failed(previous : Execution_result, stage : int) -> Execution_result =
  match pending_event_record(previous.pending) {
    None() => event_shutdown(previous.state),
    Some(event) => {
      var failed = event;
      if stage >= 2 then {
        failed.fault_ea = previous.request.effective_address;
        failed.fault_linear = previous.request.linear_address
      } else ();
      if pending_event_attempt(previous.pending) >= 1 | previous.state.current_dfa
         | status_event_depth(previous.state.status) >= 15 then
        event_shutdown(previous.state)
      else start_event_attempt(double_fault_event(failed, stage), previous.state, 1)
    },
  }

val start_user_return : (Decoded_instruction, Cpu_state) -> Execution_result

function start_event_control(operation : Event_control_uop_operation,
                             instruction : Decoded_instruction, state : Cpu_state)
  -> Execution_result = {
  if operation == EventControlBreakpoint then
    start_admitted_event(
      make_event(EventSynchronous, EventFrameBasic, 0x00000002, 4,
                 next_pc(state, instruction)), state
    )
  else if operation == EventControlSyscall then
    if state.supervisor | state.status[0] == bitone
       | status_event_depth(state.status) != 0
       | state.controls[11][32] == bitone then
      faulted(state, Op_SYSCALL, InvalidControlState, "invalid SYSCALL source state")
    else start_admitted_event(
      make_event(EventSynchronous, EventFrameBasic, 0x00000020, 4,
                 next_pc(state, instruction)), state
    )
  else {
    let direct = state.supervisor & state.status[0] == bitzero
      & status_event_depth(state.status) == 0
      & not_bool(status_user_origin(state.status)) & state.controls[11][32] == bitone;
    let outer = state.supervisor & state.status[0] == bitone
      & status_event_depth(state.status) == 1
      & status_user_origin(state.status) & state.controls[11][32] == bitone;
    if status_user_origin(state.status) & state.controls[11][32] == bitzero then
      faulted(state, Op_ERET, InvalidControlState, "invalid live user-origin chain")
    else if direct | outer then start_user_return(instruction, state)
    else if state.supervisor & state.status[0] == bitone
            & status_event_depth(state.status) > 0 then {
      let request = { stack_request(
        EventFrameAccess, 0, state, state.sp, add_bits(state.sp, 0x0000000000000008),
        AccessStackRead, 0x0000000000000000, false
      ) with selector = 0x0000000000000000 };
      waiting_transaction(TransactionEventReturn,
        state, state, instruction, CommitEvent, empty_destination(), PhaseEventFrameHeader,
        0, 0x0000000000000000, 0x0000000000000000, request
      )
    } else faulted(state, Op_ERET, InvalidControlState, "invalid ERET source state")
  }
}

function valid_frame_control(control : bits(64), state : Cpu_state) -> bool = {
  let slots = unsigned(control[7 .. 0]);
  let frame_type = unsigned(control[11 .. 8]);
  let saved_status = sail_shiftright(control, 36) & 0x000000000000FFFF;
  let shape = (frame_type == 0 & slots == 8) | (frame_type == 1 & slots == 10)
            | ((frame_type == 2 | frame_type == 3) & slots == 12);
  shape & control[31 .. 13] == 0b0000000000000000000
  & control[63 .. 52] == 0x000
  & saved_status[4] == bitone
  & ((saved_status[0] == bitone & status_event_depth(saved_status) > 0)
     | (saved_status[0] == bitzero & status_event_depth(saved_status) == 0))
  & (control[12] == bitzero | saved_status[0] == bitone)
  & status_event_depth(saved_status) + 1 == status_event_depth(state.status)
  & status_user_origin(saved_status) == status_user_origin(state.status)
}

function start_user_return(instruction : Decoded_instruction, state : Cpu_state)
  -> Execution_result = {
    let uctl = state.controls[11];
    let saved_status = sail_shiftright(uctl, 16) & 0x000000000000FFFF;
    let saved_flags = uctl & 0x000000000000FFFF;
    if not_bool(state.supervisor) | not_bool(user_return_bank_image_valid(state))
    then faulted(state, Op_ERET, InvalidControlState, "invalid user-return bank")
    else {
      var after = state;
      after.pc = state.controls[6];
      after.sp = state.controls[7];
      after.segments[0] = state.controls[8];
      after.segments[1] = state.controls[9];
      after.segments[2] = state.controls[10];
      after.flags = saved_flags[3 .. 0];
      after.status = saved_status;
      after.supervisor = false;
      after.current_dfa = false;
      after.controls[11] = uctl & 0xFFFFFFFEFFFFFFFF;
      let request = { target_probe_request(0, state.controls[8], state.controls[6]) with
        kind = ControlTransitionRequest, role = RequestRoleUserReturnTarget, commit_point = true };
      waiting_transaction(TransactionControl,
        state, after, instruction, CommitControl, empty_destination(), PhaseControlTransition,
        0, state.controls[6], 0x0000000000000000, request
      )
    }
}
