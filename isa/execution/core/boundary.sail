function live_event_state_valid(state : Cpu_state) -> bool =
  if state.status[0] == bitzero then
    state.event_depth == 0 & state.event_stack_level == 0
  else state.supervisor & state.status[4] == bitone
       & state.event_depth >= 1 & state.event_depth <= 15
       & state.event_stack_level >= 1 & state.event_stack_level <= 3

function fp_static_operand_relation_valid(instruction : Decoded_instruction) -> bool =
  if instruction.form.operation != Op_FSINCOSA then true
  else match (operand_named(instruction, "sin_dst"),
              operand_named(instruction, "cos_dst")) {
    (Some(sin_destination), Some(cos_destination)) =>
      sin_destination.value[3 .. 0] != cos_destination.value[3 .. 0],
    _ => false,
  }

function execute_full(instruction : Decoded_instruction, state : Cpu_state) -> Execution_result =
  if state.run_state != Running then
    completed(state, state, CommitNone, [||])
  else if state.supervisor != (state.status[4] == bitone) then
    faulted(state, instruction.form.operation, InvalidControlState,
            "supervisor and STATUS.PM disagree")
  else if not_bool(live_event_state_valid(state)) then
    faulted(state, instruction.form.operation, InvalidControlState,
            "STATUS.EA and live event state disagree")
  else if not_bool(fp_static_operand_relation_valid(instruction)) then
    faulted_with_error_code(
      state, instruction.form.operation, IllegalInstruction,
      "invalid floating-point destination relation", 0x0000000000000006
    )
  else if instruction.form.instruction_set == FpuSet & not_bool(state.fp_enabled) then
    faulted(state, instruction.form.operation, ExtensionUnavailable, "FP extension disabled")
  else if instruction.form.instruction_set == FpuTranscendentalSet
          & (not_bool(state.fp_enabled) | not_bool(state.fptrans_enabled)) then
    faulted(state, instruction.form.operation, ExtensionUnavailable, "FPTRANSA extension disabled")
  else if instruction.form.privilege == SupervisorPrivilege & not_bool(state.supervisor) then
    faulted(state, instruction.form.operation, PrivilegeFault, "supervisor instruction")
  else match architectural_state_fault(instruction, state) {
    Some(problem) => faulted(state, instruction.form.operation, problem.kind, problem.detail),
    None() =>
      if instruction.form.predicate_mode == WriteBoolean then execute_setcc(instruction, state)
      else if instruction.form.predicate_mode == AnnulOnFalse
              & not_bool(predicate_holds(instruction, state)) then
        completed(state, advance_pc(state, instruction), CommitControl, [||])
      else execute_route_exact(instruction, state),
  }

function machine_check_payload_valid(error_code : bits(64), fault_ea : bits(64),
                                     fault_linear : bits(64), event_aux : bits(64)) -> bool = {
  let source = unsigned(error_code[7 .. 0]);
  let severity = unsigned(error_code[9 .. 8]);
  let precise = error_code[10] == bitone;
  let retry_safe = error_code[11] == bitone;
  let fields_consistent = (error_code[24] == bitone | fault_ea == 0x0000000000000000)
                        & (error_code[25] == bitone | fault_linear == 0x0000000000000000)
                        & (error_code[26] == bitone | event_aux == 0x0000000000000000);
  source <= 5
  & severity <= 2
  & (error_code & 0xFFFFFFFFF8FFF000) == 0x0000000000000000
  & fields_consistent
  & (if severity == 0 then not_bool(precise) & not_bool(retry_safe)
     else if severity == 1 then precise | not_bool(retry_safe)
     else not_bool(retry_safe))
}

function latch_ingress(state : Cpu_state, ingress : Async_ingress) -> Cpu_state = {
  var updated = state;
  if ingress.nmi_pending then {
    if updated.controls[2][7] == bitzero then
      updated.nmi_latched_source = ingress.nmi_source
    else {
      updated.nmi_relatched = true;
      updated.nmi_relatched_source = ingress.nmi_source
    };
    updated.controls[2] = updated.controls[2] | 0x0000000000000080
  } else ();
  if ingress.machine_check_pending then {
    updated.machine_check_pending = true;
    updated.machine_check_payload = ingress.machine_check_code;
    updated.machine_check_error_code = if ingress.machine_check_error_code
        == 0x0000000000000000 & ingress.machine_check_code != 0x00000000
      then 0x0000000004000000 else ingress.machine_check_error_code;
    updated.machine_check_fault_ea = ingress.machine_check_fault_ea;
    updated.machine_check_fault_linear = ingress.machine_check_fault_linear;
    updated.machine_check_event_aux = if ingress.machine_check_event_aux
        == 0x0000000000000000 & ingress.machine_check_code != 0x00000000
      then sail_zero_extend(ingress.machine_check_code, 64)
      else ingress.machine_check_event_aux
  } else ();
  updated
}

function machine_check_event(state : Cpu_state) -> Event_record =
  { make_event(EventSynchronous, EventFrameAuxiliary, 0x00000019, 2, state.pc) with
    error_code = state.machine_check_error_code,
    fault_ea = state.machine_check_fault_ea,
    fault_linear = state.machine_check_fault_linear,
    event_aux = state.machine_check_event_aux }

function machine_check_state_valid(state : Cpu_state) -> bool =
  machine_check_payload_valid(
    state.machine_check_error_code, state.machine_check_fault_ea,
    state.machine_check_fault_linear, state.machine_check_event_aux
  )

function admitted_async_event(state : Cpu_state, ingress : Async_ingress)
  -> option(Event_record) = {
  let ecr = state.controls[2];
  let nmi = ecr[7] == bitone;
  let interrupt = ingress.interrupt_pending;
  let max_depth = unsigned(ecr[11 .. 8]);
  if state.machine_check_pending & ecr[0] == bitone & state.event_depth < 15 then
    Some(machine_check_event(state))
  else if nmi & ecr[0] == bitone & state.status[1] == bitzero & state.event_depth < 15 then
    Some(make_event(EventNmi, EventFrameBasic, 0x02 @ state.nmi_latched_source,
                    6, state.pc))
  else if interrupt & ecr[0] == bitone & state.status[5] == bitone
          & state.event_depth < max_depth & state.event_depth < 15 then
    Some(make_event(EventInterrupt, EventFrameBasic, 0x01 @ ingress.interrupt_id,
                    7, state.pc))
  else None()
}

function event_from_fault(result : Execution_result) -> Event_record = match result.fault {
  None() => make_event(EventSynchronous, EventFrameError, 0x0000000D, 3, result.state.pc),
  Some(fault) => {
    let code : bits(32) = if fault.kind == IllegalInstruction
                          | fault.kind == ExtensionUnavailable then 0x00000003
      else if fault.kind == PrivilegeFault then 0x00000008
      else if fault.kind == BoundsFault | fault.kind == AlignmentFault
           | fault.kind == TranslationFault | (fault.kind == AccessFault & not_bool(fault.bus_error))
        then 0x00000009
      else if fault.kind == DivideByZero | fault.kind == DivideOverflow then 0x0000000A
      else if fault.kind == FloatingPointFault then 0x0000000E
      else if fault.bus_error then 0x0000001A
      else 0x0000000D;
    let frame_type = if code == 0x00000008 then EventFrameBasic
      else if code == 0x00000009 then EventFramePage
      else if code == 0x0000001A then EventFrameAuxiliary
      else EventFrameError;
    var event = make_event(EventSynchronous, frame_type, code, 3, result.state.pc);
    if code == 0x00000003 | code == 0x0000000A | code == 0x0000000D
       | code == 0x0000000E then
      event.error_code = fault.error_code
    else if code == 0x00000009 then {
      event.error_code = fault.error_code;
      if result.request.kind != NoPrimitiveRequest then {
        event.fault_ea = result.request.effective_address;
        event.fault_linear = result.request.linear_address;
        event.error_code = event.error_code | 0x0000000003000000
      } else ()
    }
    else if code == 0x0000001A then {
      event.fault_ea = result.request.effective_address;
      event.fault_linear = result.request.linear_address;
      event.event_aux = result.request.range_start;
      event.error_code = fault.error_code
    }
    else event.error_code = fault.error_code;
    event
  },
}

function execute_active_repeat(state : Cpu_state) -> Execution_result =
  if state.repeat_state.grouped then
    if state.repeat_state.fixed_body == [||] then faulted(
      state, Op_REPG, InvalidControlState, "active REPG has no validated body"
    )
    else run_repeat_group_tail(
      state.repeat_state.fixed_body,
      drop_bytes(state.repeat_state.fixed_body, state.repeat_state.group_progress),
      unsigned(state.repeat_state.body_bytes) - state.repeat_state.group_progress, state
    )
  else match decode_full_record(state.repeat_state.fixed_body) {
    Some(body) => run_repeat_single(body, state.repeat_state.fixed_body, state),
    None() => faulted(state, Op_REPcc, InvalidControlState,
                      "active REPcc has no validated body"),
  }

function boundary_with_event(state : Cpu_state, event : Event_record) -> Boundary_result = {
  let execution = start_admitted_event(event, state);
  struct { state = execution.state, admitted = Some(event), execution = Some(execution) }
}

function boundary_shutdown(state : Cpu_state) -> Boundary_result = {
  let execution = event_shutdown(state);
  struct { state = execution.state, admitted = None(), execution = Some(execution) }
}

function execute_boundary(instruction : Decoded_instruction, state : Cpu_state,
                          ingress : Async_ingress) -> Boundary_result = {
  let latched = latch_ingress(state, ingress);
  if latched.run_state == Shutdown then
    struct { state = latched, admitted = None(), execution = None() }
  else if latched.machine_check_pending & not_bool(machine_check_state_valid(latched)) then
    boundary_shutdown(latched)
  else if latched.machine_check_pending
          & (latched.controls[2][0] == bitzero | latched.event_depth >= 15) then
    boundary_shutdown(latched)
  else match admitted_async_event(latched, ingress) {
    Some(event) => boundary_with_event(latched, event),
    None() =>
      if latched.controls[2][7] == bitone & latched.controls[2][0] == bitone
         & latched.status[1] == bitzero & latched.event_depth >= 15 then
        boundary_shutdown(latched)
      else if latched.run_state == Halted then
        struct { state = latched, admitted = None(), execution = None() }
      else {
        let execution = if latched.repeat_state.active then execute_active_repeat(latched)
                        else execute_full(instruction, latched);
        struct { state = execution.state, admitted = None(), execution = Some(execution) }
      },
  }
}

function rebase_awaiting_ingress(result : Execution_result, ingress : Async_ingress)
  -> Execution_result = {
  let state = latch_ingress(result.state, ingress);
  let before = latch_ingress(result.pending.before, ingress);
  let after = latch_ingress(result.pending.after, ingress);
  let request_state = latch_ingress(result.request.state_image, ingress);
  { result with state = state, pending = { result.pending with before = before, after = after },
                request = { result.request with state_image = request_state } }
}

function result_with_state(result : Execution_result, state : Cpu_state) -> Execution_result =
  { result with state = state, pending = { result.pending with after = state } }

function resume_boundary(result : Execution_result, sampled_status : bits(64),
                         ingress : Async_ingress) -> Boundary_result = {
  if result.awaiting_environment then {
    let rebased = rebase_awaiting_ingress(result, ingress);
    struct { state = rebased.state, admitted = None(), execution = Some(rebased) }
  }
  else {
    let latched = latch_ingress(result.state, ingress);
    if latched.machine_check_pending & not_bool(machine_check_state_valid(latched)) then
      boundary_shutdown(latched)
    else if latched.machine_check_pending
       & (latched.controls[2][0] == bitzero | latched.event_depth >= 15) then
      boundary_shutdown(latched)
    else if latched.machine_check_pending then boundary_with_event(latched, machine_check_event(latched))
    else match result.fault {
      Some(_) => boundary_with_event(latched, event_from_fault(result_with_state(result, latched))),
      None() => {
        let trace_unit = result.pending.boundary_class != BoundaryEventEntry
                       & result.pending.boundary_class != BoundaryRepeatInterior;
        if trace_unit & sampled_status[2] == bitone & sampled_status[3] == bitzero then
          boundary_with_event(
            latched, make_event(EventDebugTrace, EventFrameBasic, 0x00000000, 5, latched.pc)
          )
        else {
          var after_rf = latched;
          if trace_unit & sampled_status[3] == bitone then
            after_rf.status = after_rf.status & 0xFFFFFFFFFFFFFFF7
          else ();
          match admitted_async_event(after_rf, ingress) {
            Some(event) => boundary_with_event(after_rf, event),
            None() => {
              let updated_result = result_with_state(result, after_rf);
              struct { state = after_rf, admitted = None(), execution = Some(updated_result) }
            },
          }
        }
      },
    }
  }
}

function platform_reset(state : Cpu_state) -> Cpu_state = warm_reset_state(state)

function decode_and_execute_full_outcome(bytes : list(bits(8)), state : Cpu_state)
  -> Decode_execute_outcome = {
  let decoded = decode_full_record_outcome(bytes);
  match decoded.candidate_form {
    None() => struct { decode = decoded, execution = None() },
    Some(form) => match decoded.instruction {
      Some(instruction) => struct {
        decode = decoded, execution = Some(execute_full(instruction, state))
      },
      None() =>
        if form.instruction_set == FpuSet & not_bool(state.fp_enabled) then
          struct { decode = decoded, execution = Some(faulted(
            state, form.operation, ExtensionUnavailable, "FP extension disabled"
          )) }
        else if form.instruction_set == FpuTranscendentalSet
                & (not_bool(state.fp_enabled) | not_bool(state.fptrans_enabled)) then
          struct { decode = decoded, execution = Some(faulted(
            state, form.operation, ExtensionUnavailable, "FPTRANSA extension disabled"
          )) }
        else struct { decode = decoded, execution = Some(faulted(
          state, form.operation, IllegalInstruction, decoded.detail
        )) },
    },
  }
}

function decode_and_execute_full(bytes : list(bits(8)), state : Cpu_state) -> option(Execution_result) =
  match decode_and_execute_full_outcome(bytes, state).execution {
    Some(result) => Some(result),
    None() => None(),
  }
