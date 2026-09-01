function live_event_state_valid(state : Cpu_state) -> bool =
  if state.status[0] == bitzero then
    status_event_depth(state.status) == 0 & not_bool(status_user_origin(state.status))
  else state.supervisor & state.status[4] == bitone
       & status_event_depth(state.status) >= 1 & status_event_depth(state.status) <= 15
       & (not_bool(status_user_origin(state.status))
          | control_register_value(state, ControlRegister_BASE_UCTL)[32] == bitone)

function instruction_execution_breakpoint(
    instruction : Decoded_instruction, state : Cpu_state
) -> option(Debug_stop) =
  if state.run_state != Running
     | state.supervisor != (state.status[4] == bitone)
     | not_bool(live_event_state_valid(state))
     | not_bool(instruction_available(instruction, state))
     | (instruction.form.privilege == SupervisorPrivilege & not_bool(state.supervisor)) then None()
  else match architectural_state_fault(instruction, state) {
    Some(_) => None(),
    None() => debug_trigger_execution_stop(state),
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
  else if not_bool(instruction_available(instruction, state)) then
    faulted(
      state, instruction.form.operation, ExtensionUnavailable,
      "required CPUID flag disabled"
    )
  else if instruction.form.privilege == SupervisorPrivilege & not_bool(state.supervisor) then
    faulted(state, instruction.form.operation, PrivilegeFault, "supervisor instruction")
  else match architectural_state_fault(instruction, state) {
    Some(problem) => faulted(state, instruction.form.operation, problem.kind, problem.detail),
    None() => match debug_trigger_execution_stop(state) {
      Some(stop) => debug_stopped(state, instruction.form.operation, stop),
      None() =>
        if instruction.form.predicate_mode == AnnulOnFalse
                & not_bool(predicate_holds(instruction, state)) then
          completed(state, advance_pc(state, instruction), CommitControl, [||])
        else execute_operation_entry(instruction, state),
    },
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
  if ingress.interrupt_posted then
    updated = post_interrupt(updated, ingress.interrupt_identity)
  else ();
  if ingress.nmi_pending then {
    if control_register_value(updated, ControlRegister_BASE_ECR)[7] == bitzero then
      updated.nmi_latched_source = ingress.nmi_source
    else {
      updated.nmi_relatched = true;
      updated.nmi_relatched_source = ingress.nmi_source
    };
    updated = control_register_with_value(
      updated, ControlRegister_BASE_ECR,
      control_register_value(updated, ControlRegister_BASE_ECR)
      | 0x0000000000000080)
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

function admitted_async_event(state : Cpu_state) -> option(Event_record) = {
  let ecr = control_register_value(state, ControlRegister_BASE_ECR);
  let nmi = ecr[7] == bitone;
  let top = interrupt_top(state.controls.interrupt_file);
  let interrupt = top != 0x000000;
  let max_depth = unsigned(ecr[11 .. 8]);
  if state.machine_check_pending & ecr[0] == bitone & status_event_depth(state.status) < 15 then
    Some(machine_check_event(state))
  else if nmi & ecr[0] == bitone & state.status[1] == bitzero
          & status_event_depth(state.status) < 15 then
    Some(make_event(EventNmi, EventFrameBasic, 0x02 @ state.nmi_latched_source,
                    6, state.pc))
  else if interrupt & ecr[0] == bitone & state.status[5] == bitone
          & status_event_depth(state.status) < max_depth
          & status_event_depth(state.status) < 15 then
    Some(make_event(EventInterrupt, EventFrameBasic, 0x01 @ top,
                    7, state.pc))
  else None()
}

function execute_active_repeat(state : Cpu_state) -> Execution_result =
  match decode_full_record(state.repeat_state.fixed_body) {
    Some(body) => run_repeat_single(body, state.repeat_state.fixed_body, state),
    None() => faulted(state, Op_REPcc, InvalidControlState,
                      "active REPcc has no validated body"),
  }

function boundary_with_event(state : Cpu_state, event : Event_record) -> Boundary_result = {
  let admitted = if state.repeat_state.active
    then { event with saved_pc = state.repeat_state.prefix_start }
    else event;
  let execution = start_admitted_event(admitted, state);
  struct { state = execution.state, admitted = Some(admitted), execution = Some(execution) }
}

function boundary_shutdown(state : Cpu_state) -> Boundary_result = {
  let execution = event_shutdown(state);
  struct { state = execution.state, admitted = None(), execution = Some(execution) }
}

function boundary_execution_breakpoint(
    instruction : Decoded_instruction, state : Cpu_state
) -> option((Semantic_operation, Debug_stop)) =
  if state.repeat_state.active then match decode_full_record(state.repeat_state.fixed_body) {
    None() => None(),
    Some(body) => {
      var iteration = state;
      iteration.pc = state.repeat_state.body_start;
      match instruction_execution_breakpoint(body, iteration) {
        Some(stop) => Some((body.form.operation, stop)),
        None() => None(),
      }
    },
  }
  else match instruction_execution_breakpoint(instruction, state) {
    Some(stop) => Some((instruction.form.operation, stop)),
    None() => None(),
  }

function execute_boundary(instruction : Decoded_instruction, state : Cpu_state,
                          ingress : Async_ingress) -> Boundary_result = {
  let latched = latch_ingress(state, ingress);
  if latched.run_state == Shutdown then
    struct { state = latched, admitted = None(), execution = None() }
  else if latched.machine_check_pending & not_bool(machine_check_state_valid(latched)) then
    boundary_shutdown(latched)
  else if latched.machine_check_pending
          & (control_register_value(latched, ControlRegister_BASE_ECR)[0] == bitzero
             | status_event_depth(latched.status) >= 15) then
    boundary_shutdown(latched)
  else if latched.machine_check_pending then
    boundary_with_event(latched, machine_check_event(latched))
  else match boundary_execution_breakpoint(instruction, latched) {
    Some((operation, stop)) => {
      let execution = debug_stopped(latched, operation, stop);
      struct { state = execution.state, admitted = None(), execution = Some(execution) }
    },
    None() => match admitted_async_event(latched) {
      Some(event) => boundary_with_event(latched, event),
      None() =>
        if control_register_value(latched, ControlRegister_BASE_ECR)[7] == bitone
           & control_register_value(latched, ControlRegister_BASE_ECR)[0] == bitone
           & latched.status[1] == bitzero
           & status_event_depth(latched.status) >= 15 then
          boundary_shutdown(latched)
        else if latched.run_state == Halted then
          struct { state = latched, admitted = None(), execution = None() }
        else {
          let execution = if latched.repeat_state.active then execute_active_repeat(latched)
                          else execute_full(instruction, latched);
          struct { state = execution.state, admitted = None(), execution = Some(execution) }
        },
    },
  }
}

function rebase_awaiting_ingress(result : Execution_result, ingress : Async_ingress)
  -> Execution_result = {
  let state = latch_ingress(result.state, ingress);
  let after = latch_ingress(pending_after(result), ingress);
  { result with state = state, pending = { result.pending with after = Some(after) } }
}

function result_with_state(result : Execution_result, state : Cpu_state) -> Execution_result =
  { result with state = state }

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
       & (control_register_value(latched, ControlRegister_BASE_ECR)[0] == bitzero
          | status_event_depth(latched.status) >= 15) then
      boundary_shutdown(latched)
    else if latched.machine_check_pending then boundary_with_event(latched, machine_check_event(latched))
    else match result.fault {
      Some(_) => boundary_with_event(latched, event_from_fault(result_with_state(result, latched))),
      None() => match result.debug_stop {
        Some(stop) => boundary_with_event(latched, event_from_debug_stop(latched, stop)),
        None() => {
        let trace_unit = result.pending.boundary_class != BoundaryEventEntry
                       & result.pending.boundary_class != BoundaryVectorLane;
        if trace_unit & sampled_status[2] == bitone & sampled_status[3] == bitzero then
          boundary_with_event(
            latched, make_event(
              EventDebug, architectural_event_frame(Event_SINGLE_STEP),
              architectural_event_code(Event_SINGLE_STEP), 5, latched.pc)
          )
        else {
          var after_rf = latched;
          if trace_unit & sampled_status[3] == bitone then
            after_rf.status = after_rf.status & 0xFFFFFFFFFFFFFFF7
          else ();
          match admitted_async_event(after_rf) {
            Some(event) => boundary_with_event(after_rf, event),
            None() => {
              let updated_result = result_with_state(result, after_rf);
              struct { state = after_rf, admitted = None(), execution = Some(updated_result) }
            },
          }
        }
        },
      },
    }
  }
}

function platform_reset(state : Cpu_state) -> Cpu_state = warm_reset_state(state)

function decode_and_execute_full_outcome(bytes : list(bits(8)), state : Cpu_state)
  -> Decode_execute_outcome = {
  let decoded = decode_full_record_execution_outcome(bytes);
  match decoded.instruction {
    Some(instruction) => struct {
      decode = { decoded with candidate_form = Some(instruction.form) },
      execution = Some(execute_full(instruction, state))
    },
    None() => match decoded.candidate_form {
      None() => struct { decode = decoded, execution = None() },
      Some(form) =>
        if not_bool(candidate_form_available(form, state)) then
          struct { decode = decoded, execution = Some(faulted(
            state, form.operation, ExtensionUnavailable, "required CPUID flag disabled"
          )) }
        else struct { decode = decoded, execution = Some(faulted(
          state, form.operation, IllegalInstruction, decoded.detail
        )) },
    },
  }
}

function decode_and_execute_full(bytes : list(bits(8)), state : Cpu_state) -> option(Execution_result) = {
  let decoded = decode_full_record_execution_outcome(bytes);
  match decoded.instruction {
    Some(instruction) => Some(execute_full(instruction, state)),
    None() => match decoded.candidate_form {
      None() => None(),
      Some(form) =>
        if not_bool(candidate_form_available(form, state)) then
          Some(faulted(state, form.operation, ExtensionUnavailable,
                       "required CPUID flag disabled"))
        else Some(faulted(state, form.operation, IllegalInstruction, decoded.detail)),
    },
  }
}
