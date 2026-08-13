function event_frame_control(state : Cpu_state, frame_slots : int,
                             frame_type : int, saved_level : int) -> bits(64) =
  get_slice_int(64, frame_slots, 0)
  | sail_shiftleft(get_slice_int(64, frame_type, 0), 8)
  | sail_shiftleft(get_slice_int(64, state.event_depth, 0), 12)
  | sail_shiftleft(get_slice_int(64, saved_level, 0), 16)
  | (if state.repeat_state.active then 0x0000000000040000 else 0x0000000000000000)
  | sail_shiftleft(sail_zero_extend(state.flags, 64), 32)
  | sail_shiftleft(state.status & 0x000000000000FFFF, 48)

function repeat_frame_ext1(state : Cpu_state, saved_pc : bits(64)) -> bits(64) =
  if not_bool(state.repeat_state.active) then 0x0000000000000000
  else {
    let grouped = state.repeat_state.grouped;
    let delta = if grouped then sub_bits(saved_pc, state.repeat_state.body_start)
                else 0x0000000000000000;
    sail_zero_extend(state.repeat_state.counter, 64)
    | sail_shiftleft(sail_zero_extend(state.repeat_state.condition, 64), 4)
    | (if grouped then 0x0000000000000100 else 0x0000000000000000)
    | sail_shiftleft(delta & 0x000000000000FFFF, 16)
    | sail_shiftleft(sail_zero_extend(state.repeat_state.body_bytes, 64), 32)
  }

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
  let slot7 = le64_bytes(state.segments[2]);
  let slot6 = append_bytes(le64_bytes(state.segments[1]), slot7);
  let slot5 = append_bytes(le64_bytes(state.segments[0]), slot6);
  let slot4 = append_bytes(le64_bytes(state.sp), slot5);
  let slot3 = append_bytes(le64_bytes(event.saved_pc), slot4);
  let slot2 = append_bytes(le64_bytes(repeat_frame_ext1(state, event.saved_pc)), slot3);
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

function event_requested_level(event : Event_record) -> int =
  if event.code == 0x00000018 then 3
  else if event.kind == EventInterrupt then 1
  else 2

function event_retain_stack(event : Event_record, state : Cpu_state) -> bool =
  state.status[0] == bitone & state.event_stack_level >= event_requested_level(event)

function event_stack_segment(event : Event_record, state : Cpu_state) -> bits(64) =
  if event_retain_stack(event, state) then state.segments[2]
  else if event_requested_level(event) == 1 then state.controls[17]
  else if event_requested_level(event) == 2 then state.controls[19]
  else state.controls[21]

function event_stack_top(event : Event_record, state : Cpu_state) -> bits(64) =
  if event_retain_stack(event, state) then state.sp
  else if event_requested_level(event) == 1 then state.controls[18]
  else if event_requested_level(event) == 2 then state.controls[20]
  else state.controls[22]

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
  & (top & 0x000000000000003F) == 0x0000000000000000
}

function event_frame_address_valid(event : Event_record, state : Cpu_state) -> bool = {
  let segment_image = event_stack_segment(event, state);
  let top = event_stack_top(event, state);
  let frame_bytes = event_frame_slots(event.frame_type) * 8;
  segment_point(segment_image, sub_bits(top, bits_from_int(frame_bytes))).in_bounds
}

function event_target_request(state : Cpu_state) -> Primitive_request =
  { target_probe_request(0, state.controls[13], state.controls[12]) with
    role = "event_entry_target", state_image = state }

function event_stack_range_request(event : Event_record, state : Cpu_state,
                                   ordinal : int) -> Primitive_request = {
  let segment_image = event_stack_segment(event, state);
  let top = event_stack_top(event, state);
  let frame_bytes = event_frame_slots(event.frame_type) * 8;
  let frame_start = sub_bits(top, bits_from_int(frame_bytes));
  let point = segment_point(segment_image, frame_start);
  { stack_request(StackRange, ordinal, state, frame_start, top, AccessStackWrite,
                  0x0000000000000000, false) with
    role = "event_frame_range", segment_image = segment_image,
    effective_address = frame_start, linear_address = point.linear,
    width = frame_bytes, range_length = frame_bytes, state_image = state }
}

function event_frame_store_request(event : Event_record, state : Cpu_state,
                                   ordinal : int) -> Primitive_request = {
  let range = event_stack_range_request(event, state, ordinal);
  let control = event_frame_control(
    state, event_frame_slots(event.frame_type), event_frame_type_code(event.frame_type),
    state.event_stack_level
  );
  { range with kind = EventFrameAccess, role = "event_frame_store",
    access = AccessStackWrite, commit_point = true,
    selector = sail_zero_extend(event.code, 64), value = control,
    expected = event.saved_pc, auxiliary = bits_from_int(event_requested_level(event)),
    payload_bytes = encode_event_frame(state, event, control) }
}

function waiting_event_transaction(state : Cpu_state, event : Event_record, attempt : int,
                                   phase : Continuation_phase, ordinal : int,
                                   request : Primitive_request) -> Execution_result = struct {
  state = state,
  pending = { empty_pending(state, state, Op_NOP, CommitEvent) with
    phase = phase, ordinal = ordinal, event = Some(event), event_attempt = attempt,
    boundary_class = BoundaryEventEntry },
  request = request, effects = [||], fault = None(), awaiting_environment = true
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
  if state.controls[2][0] == bitzero | state.event_depth >= 15 then event_shutdown(state)
  else if not_bool(event_entry_state_valid(state)) then
    if attempt >= 1 then event_shutdown(state)
    else start_event_attempt(double_fault_event(event, 0), state, 1)
  else waiting_event_transaction(
    state, event, attempt, PhaseEventTargetProbe, 0, event_target_request(state)
  )

function start_admitted_event(event : Event_record, state : Cpu_state) -> Execution_result =
  start_event_attempt(event, state, 0)

function event_delivery_failed(previous : Execution_result, stage : int) -> Execution_result =
  match previous.pending.event {
    None() => event_shutdown(previous.pending.before),
    Some(event) => {
      var failed = event;
      if stage >= 2 then {
        failed.fault_ea = previous.request.effective_address;
        failed.fault_linear = previous.request.linear_address
      } else ();
      if previous.pending.event_attempt >= 1 | previous.pending.before.event_depth >= 15 then
        event_shutdown(previous.pending.before)
      else start_event_attempt(double_fault_event(failed, stage), previous.pending.before, 1)
    },
  }

function start_event_control(instruction : Decoded_instruction, state : Cpu_state)
  -> Execution_result = {
  if instruction.form.operation == Op_BKPT then
    start_admitted_event(
      make_event(EventSynchronous, EventFrameBasic, 0x00000002, 4,
                 next_pc(state, instruction)), state
    )
  else if instruction.form.operation == Op_ERET then
    if state.status[0] == bitzero then faulted(
      state, Op_ERET, InvalidControlState, "ERET outside event-active state"
    )
    else {
      let request = { stack_request(
        EventFrameAccess, 0, state, state.sp, add_bits(state.sp, 0x0000000000000008),
        AccessStackRead, 0x0000000000000000, false
      ) with selector = 0x0000000000000000, state_image = state };
      waiting_transaction(
        state, state, instruction, CommitEvent, empty_destination(), PhaseEventFrameHeader,
        0, 0x0000000000000000, 0x0000000000000000, request
      )
    }
  else faulted(state, instruction.form.operation, IllegalInstruction,
               "unsupported event-control operation")
}

function valid_frame_control(control : bits(64), state : Cpu_state) -> bool = {
  let slots = unsigned(control[7 .. 0]);
  let frame_type = unsigned(control[11 .. 8]);
  let saved_depth = unsigned(control[15 .. 12]);
  let saved_level = unsigned(control[17 .. 16]);
  let shape = (frame_type == 0 & slots == 8) | (frame_type == 1 & slots == 10)
            | ((frame_type == 2 | frame_type == 3) & slots == 12);
  shape & control[31 .. 19] == 0b0000000000000 & saved_depth + 1 == state.event_depth
  & saved_level <= state.event_stack_level
  & (if control[48] == bitzero then saved_depth == 0 & saved_level == 0
     else saved_depth >= 1 & saved_level >= 1)
}

function start_syscall_transition(instruction : Decoded_instruction, state : Cpu_state)
  -> Execution_result = {
  let operation = instruction.form.operation;
  if operation == Op_SYSCALL then
    if state.supervisor | state.status[0] == bitone
       | state.controls[11][32] == bitone
       | not_bool(segment_image_valid(state.controls[4]))
       | not_bool(segment_image_valid(state.controls[5]))
       | not_bool(segment_image_valid(state.controls[15]))
       | not_bool(segment_point(state.controls[15], state.controls[16]).in_bounds)
       | (state.controls[3] & 0x000000000000000F) != 0x0000000000000000
       | (state.controls[16] & 0x000000000000003F) != 0x0000000000000000
    then faulted(state, operation, InvalidControlState, "invalid SYSCALL entry bank")
    else {
      var after = state;
      after.controls[6] = next_pc(state, instruction);
      after.controls[7] = state.sp;
      after.controls[8] = state.segments[0];
      after.controls[9] = state.segments[1];
      after.controls[10] = state.segments[2];
      after.controls[11] = 0x0000000100000000
                         | sail_shiftleft(state.status & 0x000000000000FFFF, 16)
                         | sail_zero_extend(state.flags, 64);
      after.pc = state.controls[3];
      after.sp = state.controls[16];
      after.segments[0] = state.controls[4];
      after.segments[1] = state.controls[5];
      after.segments[2] = state.controls[15];
      after.status = state.status | 0x0000000000000010;
      after.supervisor = true;
      let request = { target_probe_request(0, state.controls[4], state.controls[3]) with
        kind = ControlTransitionRequest, role = "syscall_entry", commit_point = true,
        state_image = state };
      waiting_transaction(
        state, after, instruction, CommitControl, empty_destination(), PhaseControlTransition,
        0, state.controls[3], 0x0000000000000000, request
      )
    }
  else {
    let urctl = state.controls[11];
    let saved_status = sail_shiftright(urctl, 16) & 0x000000000000FFFF;
    let saved_flags = urctl & 0x000000000000FFFF;
    if not_bool(state.supervisor) | state.status[0] == bitone | urctl[32] == bitzero
       | (urctl & 0xFFFFFFFE00000000) != 0x0000000000000000
       | (saved_status & 0xFFFFFFFFFFFFFFC0) != 0x0000000000000000
       | (saved_status & 0x0000000000000011) != 0x0000000000000000
       | (saved_flags & 0xFFFFFFFFFFFFFFF0) != 0x0000000000000000
       | not_bool(segment_image_valid(state.controls[8]))
       | not_bool(segment_image_valid(state.controls[9]))
       | not_bool(segment_image_valid(state.controls[10]))
       | not_bool(segment_point(state.controls[10], state.controls[7]).in_bounds)
    then faulted(state, operation, InvalidControlState, "invalid SYSRET return bank")
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
      after.controls[11] = urctl & 0xFFFFFFFEFFFFFFFF;
      let request = { target_probe_request(0, state.controls[8], state.controls[6]) with
        kind = ControlTransitionRequest, role = "sysret_target", commit_point = true,
        state_image = state };
      waiting_transaction(
        state, after, instruction, CommitControl, empty_destination(), PhaseControlTransition,
        0, state.controls[6], 0x0000000000000000, request
      )
    }
  }
}

