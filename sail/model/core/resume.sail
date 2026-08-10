function continue_with_request(previous : Execution_result, phase : Continuation_phase,
                               ordinal : int, first : bits(64), second : bits(64),
                               request : Primitive_request) -> Execution_result = struct {
  state = previous.state,
  pending = { previous.pending with phase = phase, ordinal = ordinal,
              captured_first = first, captured_second = second },
  request = request, effects = [||], fault = None(), awaiting_environment = true
}

struct Resolved_execution = {
  state : Cpu_state,
  destination_value : bits(64),
}

function register_operand_uses(index : int, operand : Decoded_operand,
                               except_name : string) -> bool =
  operand.name != except_name & operand.type_name == "Rn"
  & unsigned(operand.value[3 .. 0]) == index

function register_is_used(index : int, operands : list(Decoded_operand),
                          except_name : string) -> bool = match operands {
  [||] => false,
  operand :: tail => register_operand_uses(index, operand, except_name)
                     | register_is_used(index, tail, except_name),
}

function available_scratch(operands : list(Decoded_operand), except_name : string,
                           candidate : int) -> int =
  if candidate < 0 then 15
  else if register_is_used(candidate, operands, except_name)
       then available_scratch(operands, except_name, candidate - 1)
       else candidate

function option_operand_writes(value : option(Decoded_operand)) -> bool = match value {
  Some(operand) => operand.access == AccessWrite | operand.access == AccessReadWrite,
  None() => false,
}

function operand_access_named(name : string, operands : list(Decoded_operand)) -> Metadata_access =
  match operands {
    [||] => AccessRead,
    operand :: tail => if operand.name == name then operand.access
                       else operand_access_named(name, tail),
  }

function resolved_operand(operand : Decoded_operand, first_name : string, first_value : bits(64),
                          second_name : string, second_value : bits(64), scratch : int)
  -> Decoded_operand =
  if operand.name != first_name & operand.name != second_name then operand
  else {
    let value = if operand.name == first_name then first_value else second_value;
    if operand.access == AccessWrite | operand.access == AccessReadWrite then
      { operand with type_name = "Rn", value = get_slice_int(64, scratch, 0),
                     fixed_identity = "", ea = None() }
    else { operand with type_name = "imm64", value = value,
                        fixed_identity = "", ea = None() }
  }

function resolved_operand_list(operands : list(Decoded_operand),
                               first_name : string, first_value : bits(64),
                               second_name : string, second_value : bits(64), scratch : int)
  -> list(Decoded_operand) = match operands {
  [||] => [||],
  operand :: tail => resolved_operand(
    operand, first_name, first_value, second_name, second_value, scratch
  ) :: resolved_operand_list(tail, first_name, first_value, second_name, second_value, scratch),
}

function execute_resolved_operands(instruction : Decoded_instruction, image : Cpu_state,
                                   first_name : string, first_value : bits(64),
                                   second_name : string, second_value : bits(64))
  -> option(Resolved_execution) = {
  let destination_name = if second_name != "" then second_name else first_name;
  let scratch = available_scratch(instruction.operands, destination_name, 15);
  let destination_operand = find_operand_by_name(destination_name, instruction.operands);
  let destination_is_memory_write = option_operand_writes(destination_operand);
  var execution_image = image;
  let saved_scratch = image_register(image, scratch);
  if destination_is_memory_write then {
    let initial_value = if destination_name == first_name then first_value else second_value;
    execution_image.registers[unsigned(get_slice_int(4, scratch, 0))] = initial_value
  } else ();
  let synthetic = { instruction with operands = resolved_operand_list(
    instruction.operands, first_name, first_value, second_name, second_value, scratch
  ) };
  let result = execute_route_exact(synthetic, execution_image);
  if result.awaiting_environment | result.fault != None() then None()
  else {
    let destination_value = image_register(result.state, scratch);
    var final_state = result.state;
    if destination_is_memory_write then
      final_state.registers[unsigned(get_slice_int(4, scratch, 0))] = saved_scratch
    else ();
    Some(struct { state = final_state, destination_value = destination_value })
  }
}

function commit_response_destination(previous : Execution_result, value : bits(64),
                                     response : Transaction_response) -> Execution_result = {
  let fp_route = semantic_route(previous.pending.operation) == RouteFpu
               | semantic_route(previous.pending.operation) == RouteFpuTranscendental;
  let destination = previous.pending.destination;
  let initial_operand : Fp_operand_image = struct {
    valid = destination.kind == "Fn",
    kind = if destination.width == 4 then FpBits32 else FpBits64,
    bits = value
  };
  let post = if fp_route & destination.kind == "Fn" then fp_postprocess(
    initial_operand, previous.pending.before.fstatus,
    semantic_route(previous.pending.operation) == RouteFpuTranscendental,
    response.generated_fflags
  ) else struct { value = initial_operand, generated_causes = response.generated_fflags };
  let generated = post.generated_causes;
  if fp_route & not_bool(fp_operation_causes_valid(previous.pending.operation, generated)) then
    faulted(previous.pending.before, previous.pending.operation, InvalidControlState,
            "floating-point response reported an impossible cause")
  else if fp_route & fp_traps(previous.pending.before.fstatus, generated) then {
    let base = faulted(previous.pending.before, previous.pending.operation,
                       FloatingPointFault, "enabled floating-point exception");
    { base with fault = Some(struct {
        kind = FloatingPointFault, operation = previous.pending.operation,
        detail = "enabled floating-point exception",
        error_code = sail_zero_extend(generated, 64), bus_error = false
      }) }
  }
  else {
  var updated = previous.pending.after;
  if destination.kind == "Rn" then {
    let index = unsigned(destination.index);
    updated.registers[index] = merge_narrow(updated.registers[index], value, destination.width)
  }
  else if destination.kind == "Fn" then {
    let index = unsigned(destination.index);
    updated.floating_registers[index] = if destination.width == 4
      then 0x00000000 @ post.value.bits[31 .. 0] else post.value.bits
    ; updated.fp_component_modified = true
  }
  else if destination.kind == "SP" then
    updated.sp = merge_narrow(updated.sp, value, destination.width)
  else ();
  if response.write_flags & fp_route then match fp_semantics(previous.pending.operation) {
    Some(semantics) => updated.flags = (updated.flags & not_vec(semantics.flags_mask))
                                     | (response.flags & semantics.flags_mask),
    None() => (),
  }
  else if response.write_flags then updated.flags = response.flags else ();
  updated.fflags = updated.fflags | generated;
  if generated != 0b00000 then updated.fp_component_modified = true else ();
  completed(previous.state, updated, previous.pending.kind, [||])
  }
}

function restore_register_file(bytes : list(bits(8)), index : int, registers : Registers)
  -> option(Registers) =
  if index >= 16 then Some(registers)
  else match read_le_bits(bytes, 16 + index * 8, 64) {
    None() => None(),
    Some(value) => {
      var updated = registers;
      updated[unsigned(get_slice_int(4, index, 0))] = value;
      restore_register_file(bytes, index + 1, updated)
    },
  }

function restore_fp_file(bytes : list(bits(8)), offset : int, index : int,
                         registers : Floating_registers) -> option(Floating_registers) =
  if index >= 16 then Some(registers)
  else match read_le_bits(bytes, offset + index * 8, 64) {
    None() => None(),
    Some(value) => {
      var updated = registers;
      updated[unsigned(get_slice_int(4, index, 0))] = value;
      restore_fp_file(bytes, offset, index + 1, updated)
    },
  }

function restore_raw_image(previous : Execution_result, bytes : list(bits(8)),
                           header : bits(64), bitmap : bits(64)) -> Execution_result = {
  let state = previous.pending.before;
  let saved_status = sail_shiftright(header, 36) & 0x000000000000FFFF;
  let saved_flags = sail_shiftright(header, 20) & 0x000000000000FFFF;
  let invalid_status = state.supervisor
    & (saved_status[15 .. 6] != 0b0000000000
       | saved_status[4] != state.status[4] | saved_status[0] != state.status[0]);
  if byte_list_length(bytes) < state.save_area_size
     | saved_flags[15 .. 4] != 0x000 | invalid_status then
    faulted(state, Op_RESTORE, InvalidControlState, "invalid raw RESTORE image")
  else match restore_register_file(bytes, 0, state.registers) {
    None() => faulted(state, Op_RESTORE, InvalidControlState, "truncated RESTORE register block"),
    Some(registers) => match (
      read_le_bits(bytes, 144, 64), read_le_bits(bytes, 152, 64),
      read_le_bits(bytes, 160, 64), read_le_bits(bytes, 168, 64),
      read_le_bits(bytes, 176, 64), read_le_bits(bytes, 184, 64)
    ) {
      (Some(gs0), Some(gs1), Some(gs2), Some(gs3), Some(gs4), Some(gs5)) => {
        let invalid_segments =
          (header[4] == bitone & not_bool(segment_image_valid(gs0)))
          | (header[5] == bitone & not_bool(segment_image_valid(gs1)))
          | (header[6] == bitone & not_bool(segment_image_valid(gs2)))
          | (header[7] == bitone & not_bool(segment_image_valid(gs3)))
          | (header[8] == bitone & not_bool(segment_image_valid(gs4)))
          | (header[9] == bitone & not_bool(segment_image_valid(gs5)));
        if invalid_segments then faulted(
          state, Op_RESTORE, InvalidControlState, "invalid RESTORE segment image"
        )
        else {
          var updated = previous.pending.after;
          updated.registers = registers;
          updated.flags = saved_flags[3 .. 0];
          if state.supervisor then updated.status = saved_status else ();
          if header[4] == bitone then updated.segments[3] = gs0 else ();
          if header[5] == bitone then updated.segments[4] = gs1 else ();
          if header[6] == bitone then updated.segments[5] = gs2 else ();
          if header[7] == bitone then updated.segments[6] = gs3 else ();
          if header[8] == bitone then updated.segments[7] = gs4 else ();
          if header[9] == bitone then updated.segments[8] = gs5 else ();
          if bitmap[0] == bitzero then {
            if state.fp_component_present then {
              updated.floating_registers = zero_floating_registers();
              updated.fflags = 0b00000;
              updated.fstatus = 0x0000000000000000;
              updated.fp_component_modified = false
            } else ();
            completed(state, updated, CommitMemory, [||])
          }
          else match (
            restore_fp_file(bytes, state.fp_component_offset, 0,
                            state.floating_registers),
            read_le_bits(bytes, state.fp_component_offset + 128, 64),
            read_le_bits(bytes, state.fp_component_offset + 136, 64)
          ) {
            (Some(fp_registers), Some(fflags), Some(fstatus)) =>
              if (fflags & 0xFFFFFFFFFFFFFFE0) != 0x0000000000000000
                 | (fstatus & 0xFFFFFFFFFFFFFC00) != 0x0000000000000000 then
                faulted(state, Op_RESTORE, InvalidControlState,
                        "invalid RESTORE floating-point component")
              else {
                updated.floating_registers = fp_registers;
                updated.fflags = fflags[4 .. 0];
                updated.fstatus = fstatus;
                updated.fp_component_modified = fp_registers != zero_floating_registers()
                  | fflags != 0x0000000000000000 | fstatus != 0x0000000000000000;
                completed(state, updated, CommitMemory, [||])
              },
            _ => faulted(state, Op_RESTORE, InvalidControlState,
                         "truncated RESTORE floating-point component"),
          }
        }
      },
      _ => faulted(state, Op_RESTORE, InvalidControlState, "truncated RESTORE segment block"),
    },
  }
}

function decode_repeat_frame(control : bits(64), ext : bits(64), saved_pc : bits(64),
                             saved_cs : bits(64), state : Cpu_state) -> option(Repeat_state) =
  if control[18] == bitzero then
    if ext == 0x0000000000000000 then Some({ state.repeat_state with active = false })
    else None()
  else {
    let kind = unsigned(ext[9 .. 8]);
    let delta = sail_zero_extend(ext[31 .. 16], 64);
    let body_length = ext[47 .. 32];
    let grouped = kind == 1;
    let body_start = sub_bits(saved_pc, delta);
    let grouped_location_valid = not_bool(grouped) | (
      unsigned(delta) < unsigned(body_length)
      & unsigned(saved_pc) >= unsigned(delta)
      & segment_point(saved_cs, body_start).in_bounds
      & segment_point(saved_cs, add_bits(body_start,
          bits_from_int(unsigned(body_length) - 1))).in_bounds
    );
    if kind > 1 | ext[15 .. 10] != 0b000000 | ext[63 .. 48] != 0x0000
       | (kind == 0 & ext[7 .. 4] == 0x1)
       | (kind == 1 & ext[7 .. 4] != 0x0)
       | (not_bool(grouped) & (delta != 0x0000000000000000 | body_length != 0x0000))
       | (grouped & body_length == 0x0000)
       | not_bool(grouped_location_valid) then None()
    else {
      let counter = ext[3 .. 0];
      Some(struct {
        active = true, grouped = grouped, counter = counter,
        remaining = state.registers[unsigned(counter)], condition = ext[7 .. 4],
        body_bytes = body_length,
        body_start = if grouped then body_start else saved_pc,
        fixed_body = [||], group_progress = if grouped then unsigned(delta) else 0
      })
    }
  }

function continue_event_return(previous : Execution_result, bytes : list(bits(8)))
  -> Execution_result = match (
    read_le_bits(bytes, 0, 64), read_le_bits(bytes, 8, 64),
    read_le_bits(bytes, 16, 64), read_le_bits(bytes, 24, 64),
    read_le_bits(bytes, 32, 64), read_le_bits(bytes, 40, 64),
    read_le_bits(bytes, 48, 64), read_le_bits(bytes, 56, 64)
  ) {
    (Some(control), Some(event_info), Some(ext), Some(saved_pc), Some(saved_sp),
     Some(saved_cs), Some(saved_ds), Some(saved_ss)) => {
      let saved_flags = sail_shiftright(control, 32) & 0x000000000000FFFF;
      let saved_status = sail_shiftright(control, 48) & 0x000000000000FFFF;
      if control != previous.pending.captured_first
         | byte_list_length(bytes) < unsigned(control[7 .. 0]) * 8
         | event_info[63 .. 32] != 0x00000000
         | saved_flags[15 .. 4] != 0x000
         | saved_status[15 .. 6] != 0b0000000000
         | not_bool(segment_image_valid(saved_cs))
         | not_bool(segment_image_valid(saved_ds))
         | not_bool(segment_image_valid(saved_ss))
         | not_bool(segment_point(saved_cs, saved_pc).in_bounds)
         | not_bool(segment_point(saved_ss, saved_sp).in_bounds) then
        faulted(previous.pending.before, Op_ERET, InvalidControlState,
                "invalid raw event return frame")
      else match decode_repeat_frame(control, ext, saved_pc, saved_cs,
                                     previous.pending.before) {
        None() => faulted(previous.pending.before, Op_ERET, InvalidControlState,
                          "invalid FRAME_EXT1 repeat continuation"),
        Some(repeat_state) => {
          var candidate = previous.pending.before;
          candidate.flags = saved_flags[3 .. 0];
          candidate.status = saved_status;
          candidate.supervisor = saved_status[4] == bitone;
          candidate.pc = saved_pc;
          candidate.sp = saved_sp;
          candidate.segments[0] = saved_cs;
          candidate.segments[1] = saved_ds;
          candidate.segments[2] = saved_ss;
          candidate.event_depth = unsigned(control[15 .. 12]);
          candidate.event_stack_level = unsigned(control[17 .. 16]);
          candidate.repeat_state = repeat_state;
          candidate.halted = false;
          candidate.run_state = Running;
          let staged = { previous with pending = { previous.pending with after = candidate } };
          if repeat_state.active then {
            let fetch_length = if repeat_state.grouped
              then unsigned(repeat_state.body_bytes) else 18;
            let request = { empty_primitive_request() with
              kind = RepeatBodyFetch, ordinal = previous.pending.ordinal + 1,
              role = "eret_repeat_validate", domain = "CS", segment = 0,
              segment_image = saved_cs, width = fetch_length,
              range_start = repeat_state.body_start,
              range_end = add_bits(repeat_state.body_start, bits_from_int(fetch_length)),
              range_length = fetch_length,
              range_wrap = unsigned(add_bits(repeat_state.body_start,
                                              bits_from_int(fetch_length)))
                           < unsigned(repeat_state.body_start),
              range_end_at_modulus = add_bits(repeat_state.body_start,
                                               bits_from_int(fetch_length))
                                     == 0x0000000000000000,
              effective_address = repeat_state.body_start,
              linear_address = segment_point(saved_cs, repeat_state.body_start).linear,
              access = AccessExecute, address_translation = true,
              commit_point = false, body_length = fetch_length,
              state_image = previous.pending.before };
            continue_with_request(
              staged, PhaseEventReturnBody, previous.pending.ordinal + 1,
              saved_pc, saved_cs, request
            )
          }
          else continue_with_request(
            staged, PhaseEventReturnExecute, previous.pending.ordinal + 1,
            saved_pc, saved_cs,
            target_probe_request(previous.pending.ordinal + 1, saved_cs, saved_pc)
          )
        },
      }
    },
    _ => faulted(previous.pending.before, Op_ERET, InvalidControlState,
                 "truncated event return frame"),
  }

function response_matches_phase(phase : Continuation_phase, request : Primitive_request,
                                kind : Transaction_response_kind) -> bool = match phase {
  PhaseSourceRead => kind == ResponseRead,
  PhaseDestinationProbe =>
    if request.kind == MemoryRead then kind == ResponseRead
    else if request.kind == MemoryProbe then kind == ResponseProbe
    else false,
  PhaseDestinationWrite => kind == ResponseStoreAck,
  PhaseMemoryWriteFirst => kind == ResponseStoreAck,
  PhaseMemoryWriteSecond => kind == ResponseStoreAck,
  PhaseTargetRead => kind == ResponseRead,
  PhaseTargetExecuteProbe => kind == ResponseTranslation,
  PhaseStackRange => kind == ResponseStackRange,
  PhaseStackReadFirst => kind == ResponseRead,
  PhaseStackReadSecond => kind == ResponseRead,
  PhaseStackWriteFirst => kind == ResponseStoreAck,
  PhaseIntegerExternal => kind == ResponseIntegerExternal,
  PhaseAtomicRmw => kind == ResponseAtomic,
  PhaseCacheTranslate => kind == ResponseAddressTranslation,
  PhaseCacheMaintenance => kind == ResponseCacheMaintenance,
  PhaseFenceCompletion => kind == ResponseFenceCompletion,
  PhaseTlbOperation => kind == ResponseTlbOperation,
  PhaseTranslationQuery => kind == ResponseTranslationQuery,
  PhasePteRead => kind == ResponsePteRead,
  PhaseContextSwitch => kind == ResponseContextSwitch,
  PhaseStateSave => kind == ResponseStateSave,
  PhaseStateRestoreHeader => kind == ResponseStateRestore,
  PhaseStateRestoreRange => kind == ResponseStateRestore,
  PhaseStateRestore => kind == ResponseStateRestore,
  PhaseRepeatFetch => kind == ResponseRepeatFetch,
  PhaseEventFrameHeader => kind == ResponseEventFrame,
  PhaseEventFrame => kind == ResponseEventFrame,
  PhaseEventTargetProbe => kind == ResponseTranslation,
  PhaseEventStackProbe => kind == ResponseStackRange,
  PhaseEventFrameStore => kind == ResponseEventFrame,
  PhaseEventReturnBody => kind == ResponseRepeatFetch,
  PhaseEventReturnExecute => kind == ResponseTranslation,
  PhaseFpContractQuery => kind == ResponseCpuidQuery,
  PhaseFpSourceRead => kind == ResponseRead,
  PhaseFpDestinationProbe => kind == ResponseProbe,
  PhaseFpCompute => kind == ResponseFloatingPoint,
  PhaseFpDestinationWrite => kind == ResponseStoreAck,
  PhaseCpuidQuery => kind == ResponseCpuidQuery,
  PhasePerformanceCounter => kind == ResponsePerformanceCounter,
  PhaseControlTransition => kind == ResponseControlTransition,
  PhaseResetSerialize => kind == ResponseResetSerialize,
  ContinuationNone => false,
  _ => false,
}

function transaction_faulted(previous : Execution_result, kind : Fault_kind,
                             detail : string) -> Execution_result = struct {
  state = previous.pending.before,
  pending = previous.pending,
  request = previous.request,
  effects = [||],
  fault = Some(struct {
    kind = kind, operation = previous.pending.operation, detail = detail,
    error_code = if kind == AccessFault then 0x0000000047000000 else 0x0000000000000000,
    bus_error = kind == AccessFault
  }),
  awaiting_environment = false
}

function resume_transaction_inner(previous : Execution_result, response : Transaction_response)
  -> Execution_result =
  if not_bool(previous.awaiting_environment) then previous
  else if not_bool(response_matches_phase(previous.pending.phase, previous.request,
                                          response.kind)) then
    faulted(previous.pending.before, previous.pending.operation,
            InvalidControlState, "transaction response kind mismatch")
  else if not_bool(response.success) & previous.pending.phase == PhaseEventTargetProbe then
    event_delivery_failed(previous, 0)
  else if not_bool(response.success) & previous.pending.phase == PhaseEventStackProbe then
    event_delivery_failed(previous, 2)
  else if not_bool(response.success) & previous.pending.phase == PhaseEventFrameStore then
    event_delivery_failed(previous, 3)
  else if not_bool(response.success) & previous.request.suppress_fault then
    completed(previous.pending.before, previous.pending.after, previous.pending.kind, [||])
  else if not_bool(response.success) then
    transaction_faulted(previous, response.fault_kind, response.detail)
  else match previous.pending.phase {
    PhaseSourceRead => match previous.pending.instruction {
      None() => faulted(previous.pending.before, previous.pending.operation,
                        InvalidControlState, "missing continuation instruction"),
      Some(instruction) => {
        let width = operation_width(instruction);
        let evaluated = evaluate_instruction_eas(
          instruction.operands, instruction.form.operation,
          previous.pending.before, previous.pending.before.pc, width
        );
        match memory_evaluation_for(instruction.operands, evaluated.evaluations, false) {
          None() => {
            let source_name = evaluation_option_name(memory_evaluation_for(
              instruction.operands, evaluated.evaluations, true
            ));
            match next_memory_source(instruction.operands, evaluated.evaluations, source_name) {
              Some(second_source) => continue_with_request(
                previous, PhaseDestinationProbe, previous.pending.ordinal + 1,
                response.value, 0x0000000000000000,
                request_for_evaluation(
                  MemoryRead, previous.pending.ordinal + 1, second_source,
                  AccessLoad, 0x0000000000000000, false
                )
              ),
              None() => match execute_resolved_operands(
                instruction, evaluated.image, source_name, response.value,
                "", 0x0000000000000000
              ) {
                Some(resolved) => completed(
                  previous.pending.before, resolved.state, CommitRegisters, [||]
                ),
                None() => faulted(
                  previous.pending.before, instruction.form.operation,
                  IllegalInstruction, "unresolved memory semantic continuation"
                ),
              },
            }
          },
          Some(destination) => {
            let source = memory_evaluation_for(instruction.operands, evaluated.evaluations, true);
            let same_operand = evaluation_option_named(source, destination.operand_name);
            if same_operand & instruction.form.operation == Op_XCHG then
              match next_memory_source(
                instruction.operands, evaluated.evaluations, destination.operand_name
              ) {
                Some(second_source) => continue_with_request(
                  previous, PhaseDestinationProbe, 1, response.value,
                  0x0000000000000000,
                  request_for_evaluation(
                    MemoryRead, 1, second_source, AccessLoad,
                    0x0000000000000000, false
                  )
                ),
                None() => match execute_resolved_operands(
                  instruction, evaluated.image, destination.operand_name, response.value,
                  "", 0x0000000000000000
                ) {
                  None() => faulted(
                    previous.pending.before, Op_XCHG, IllegalInstruction,
                    "unresolved register-memory XCHG continuation"
                  ),
                  Some(resolved) => {
                    let staged = { previous with pending = {
                      previous.pending with after = resolved.state
                    } };
                    continue_with_request(
                      staged, PhaseDestinationWrite, 1,
                      resolved.destination_value, response.value,
                      request_for_evaluation(
                        MemoryStore, 1, destination, AccessStore,
                        resolved.destination_value, true
                      )
                    )
                  },
                },
              }
            else if same_operand then {
              match execute_resolved_operands(
                instruction, evaluated.image, destination.operand_name, response.value,
                "", 0x0000000000000000
              ) {
                None() => faulted(
                  previous.pending.before, instruction.form.operation,
                  IllegalInstruction, "unresolved read-modify-write semantic continuation"
                ),
                Some(resolved) => {
                  let staged = { previous with pending = {
                    previous.pending with after = resolved.state
                  } };
                  continue_with_request(
                    staged, PhaseDestinationWrite, 1,
                    resolved.destination_value, response.value,
                    request_for_evaluation(
                      MemoryStore, 1, destination, AccessStore,
                      resolved.destination_value, true
                    )
                  )
                },
              }
            }
            else continue_with_request(
              previous, PhaseDestinationProbe, 1, response.value, 0x0000000000000000,
              request_for_evaluation(
                if operand_access_named(destination.operand_name, instruction.operands) == AccessReadWrite
                then MemoryRead else MemoryProbe,
                1, destination,
                if operand_access_named(destination.operand_name, instruction.operands) == AccessReadWrite
                then AccessLoad else AccessStore,
                                     0x0000000000000000, false)
            )
          },
        }
      },
    },
    PhaseDestinationProbe => match previous.pending.instruction {
      None() => faulted(previous.pending.before, previous.pending.operation,
                        InvalidControlState, "missing destination continuation"),
      Some(instruction) => {
        let width = operation_width(instruction);
        let evaluated = evaluate_instruction_eas(
          instruction.operands, instruction.form.operation,
          previous.pending.before, previous.pending.before.pc, width
        );
        match memory_evaluation_for(instruction.operands, evaluated.evaluations, false) {
          None() => {
            let first_source = memory_evaluation_for(
              instruction.operands, evaluated.evaluations, true
            );
            let first_name = evaluation_option_name(first_source);
            match next_memory_source(instruction.operands, evaluated.evaluations, first_name) {
              None() => faulted(previous.pending.before, previous.pending.operation,
                                InvalidControlState, "missing second memory source"),
              Some(second_source) => match execute_resolved_operands(
                instruction, evaluated.image, first_name, previous.pending.captured_first,
                second_source.operand_name, response.value
              ) {
                Some(resolved) => completed(
                  previous.pending.before, resolved.state, CommitRegisters, [||]
                ),
                None() => faulted(
                  previous.pending.before, previous.pending.operation,
                  IllegalInstruction, "unresolved two-source memory continuation"
                ),
              },
            }
          },
          Some(destination) => {
            if instruction.form.operation == Op_XCHG then {
              let first_source = memory_evaluation_for(
                instruction.operands, evaluated.evaluations, true
              );
              match first_source {
                None() => faulted(
                  previous.pending.before, Op_XCHG, InvalidControlState,
                  "missing first XCHG operand"
                ),
                Some(first) => continue_with_request(
                  previous, PhaseMemoryWriteFirst, previous.pending.ordinal + 1,
                  previous.pending.captured_first, response.value,
                  request_for_evaluation(
                    MemoryStore, previous.pending.ordinal + 1, first,
                    AccessStore, response.value, false
                  )
                ),
              }
            }
            else {
            let source_name = evaluation_option_name(memory_evaluation_for(
              instruction.operands, evaluated.evaluations, true
            ));
            match execute_resolved_operands(
              instruction, evaluated.image, source_name, previous.pending.captured_first,
              destination.operand_name, response.value
            ) {
              None() => faulted(
                previous.pending.before, instruction.form.operation,
                IllegalInstruction, "unresolved memory-to-memory semantic continuation"
              ),
              Some(resolved) => {
                let staged = { previous with pending = {
                  previous.pending with after = resolved.state
                } };
                continue_with_request(
                  staged, PhaseDestinationWrite, previous.pending.ordinal + 1,
                  resolved.destination_value, response.value,
                  request_for_evaluation(
                    MemoryStore, previous.pending.ordinal + 1, destination,
                    AccessStore, resolved.destination_value, true
                  )
                )
              },
            }
            }
          },
        }
      },
    },
    PhaseDestinationWrite => completed(
      previous.pending.before, previous.pending.after, previous.pending.kind, [||]
    ),
    PhaseMemoryWriteFirst => match previous.pending.instruction {
      None() => faulted(previous.pending.before, previous.pending.operation,
                        InvalidControlState, "missing compound memory continuation"),
      Some(instruction) => {
        let evaluated = evaluate_instruction_eas(
          instruction.operands, instruction.form.operation,
          previous.pending.before, previous.pending.before.pc,
          operation_width(instruction)
        );
        let first_name = evaluation_option_name(memory_evaluation_for(
          instruction.operands, evaluated.evaluations, true
        ));
        match next_memory_source(instruction.operands, evaluated.evaluations, first_name) {
          None() => faulted(previous.pending.before, previous.pending.operation,
                            InvalidControlState, "missing compound memory destination"),
          Some(second) => continue_with_request(
            previous, PhaseMemoryWriteSecond, previous.pending.ordinal + 1,
            previous.pending.captured_first, previous.pending.captured_second,
            request_for_evaluation(
              MemoryStore, previous.pending.ordinal + 1, second,
              AccessStore, previous.pending.captured_first, true
            )
          ),
        }
      },
    },
    PhaseMemoryWriteSecond => completed(
      previous.pending.before, previous.pending.after, CommitMemory, [||]
    ),
    PhaseTargetRead => match previous.pending.instruction {
      None() => faulted(previous.pending.before, previous.pending.operation,
                        InvalidControlState, "missing target continuation"),
      Some(instruction) => {
        let cs_image = if instruction.form.operation == Op_LCALL | instruction.form.operation == Op_LJMP
          then match value_named(instruction, previous.pending.before, "new_cs") {
            Some(value) => value, None() => previous.pending.before.segments[0]
          } else previous.pending.before.segments[0];
        if not_bool(segment_image_valid(cs_image)) then faulted(
          previous.pending.before, instruction.form.operation,
          InvalidControlState, "invalid target code segment"
        )
        else continue_with_request(
          previous, PhaseTargetExecuteProbe, previous.pending.ordinal + 1,
          response.value, cs_image,
          target_probe_request(previous.pending.ordinal + 1, cs_image, response.value)
        )
      },
    },
    PhaseTargetExecuteProbe => match previous.pending.instruction {
      None() => faulted(previous.pending.before, previous.pending.operation,
                        InvalidControlState, "missing control continuation"),
      Some(instruction) => {
        let operation = instruction.form.operation;
        if operation == Op_CALL | operation == Op_CALLcc | operation == Op_LCALL then {
          let far = operation == Op_LCALL;
          let bytes = if far then 16 else 8;
          let stack_start = sub_bits(previous.pending.before.sp, get_slice_int(64, bytes, 0));
          var after = previous.pending.after;
          after.sp = stack_start; after.pc = previous.pending.captured_first;
          if far then after.segments[0] = previous.pending.captured_second else ();
          let staged = { previous with pending = { previous.pending with after = after } };
          continue_with_request(
            staged, PhaseStackRange, previous.pending.ordinal + 1,
            previous.pending.captured_first, previous.pending.captured_second,
            stack_request(StackRange, previous.pending.ordinal + 1, previous.pending.before,
                          stack_start, previous.pending.before.sp, AccessStackWrite,
                          0x0000000000000000, false)
          )
        }
        else {
          var updated = previous.pending.after;
          updated.pc = previous.pending.captured_first;
          if operation == Op_LJMP | operation == Op_LRET then
            updated.segments[0] = previous.pending.captured_second
          else ();
          completed(previous.pending.before, updated, CommitControl, [||])
        }
      },
    },
    PhaseStackRange => match previous.pending.instruction {
      None() => faulted(previous.pending.before, previous.pending.operation,
                        InvalidControlState, "missing stack continuation"),
      Some(instruction) => {
        let operation = instruction.form.operation;
        let ordinal = previous.pending.ordinal + 1;
        if operation == Op_PUSH then continue_with_request(
          previous, PhaseStackWriteFirst, ordinal,
          previous.pending.captured_first, previous.pending.captured_second,
          stack_request(MemoryStore, ordinal, previous.pending.before,
                        sub_bits(previous.pending.before.sp, 0x0000000000000008),
                        previous.pending.before.sp, AccessStackWrite,
                        previous.pending.captured_first, true)
        )
        else if operation == Op_PUSHP | operation == Op_FPUSHP then continue_with_request(
          previous, PhaseStackWriteFirst, ordinal,
          previous.pending.captured_first, previous.pending.captured_second,
          compound_stack_store(
            ordinal, previous.pending.before,
            sub_bits(previous.pending.before.sp, 0x0000000000000010),
            previous.pending.captured_second, previous.pending.captured_first
          )
        )
        else if operation == Op_CALL | operation == Op_CALLcc then continue_with_request(
          previous, PhaseStackWriteFirst, ordinal,
          previous.pending.captured_first, previous.pending.captured_second,
          stack_request(MemoryStore, ordinal, previous.pending.before,
                        sub_bits(previous.pending.before.sp, 0x0000000000000008),
                        previous.pending.before.sp, AccessStackWrite,
                        next_pc(previous.pending.before, instruction), true)
        )
        else if operation == Op_LCALL then continue_with_request(
          previous, PhaseStackWriteFirst, ordinal,
          next_pc(previous.pending.before, instruction), previous.pending.before.segments[0],
          compound_stack_store(
            ordinal, previous.pending.before,
            sub_bits(previous.pending.before.sp, 0x0000000000000010),
            next_pc(previous.pending.before, instruction), previous.pending.before.segments[0]
          )
        )
        else continue_with_request(
          previous, PhaseStackReadFirst, ordinal,
          0x0000000000000000, 0x0000000000000000,
          stack_request(MemoryRead, ordinal, previous.pending.before,
                        previous.pending.before.sp,
                        add_bits(previous.pending.before.sp, 0x0000000000000008),
                        AccessStackRead, 0x0000000000000000, false)
        )
      },
    },
    PhaseStackWriteFirst => completed(
      previous.pending.before, previous.pending.after, previous.pending.kind, [||]
    ),
    PhaseStackReadFirst => match previous.pending.instruction {
      None() => faulted(previous.pending.before, previous.pending.operation,
                        InvalidControlState, "missing stack read"),
      Some(instruction) => {
        let operation = instruction.form.operation;
        let ordinal = previous.pending.ordinal + 1;
        if operation == Op_POP then {
          var updated = previous.pending.after;
          match operand_named(instruction, "reg") {
            Some(reg) =>
              if reg.type_name == "SREG" then {
                let index = unsigned(reg.value[2 .. 0]) + 1;
                if segment_image_valid(response.value) then updated.segments[index] = response.value
                else return faulted(previous.pending.before, operation,
                                    InvalidControlState, "invalid popped segment")
              }
              else {
                let index = unsigned(reg.value[3 .. 0]); updated.registers[index] = response.value
              },
            None() => (),
          };
          completed(previous.pending.before, updated, CommitRegisters, [||])
        }
        else if operation == Op_RET then continue_with_request(
          previous, PhaseTargetExecuteProbe, ordinal, response.value,
          previous.pending.before.segments[0],
          target_probe_request(ordinal, previous.pending.before.segments[0], response.value)
        )
        else continue_with_request(
          previous, PhaseStackReadSecond, ordinal, response.value,
          0x0000000000000000,
          stack_request(MemoryRead, ordinal, previous.pending.before,
                        add_bits(previous.pending.before.sp, 0x0000000000000008),
                        add_bits(previous.pending.before.sp, 0x0000000000000010),
                        AccessStackRead, 0x0000000000000000, false)
        )
      },
    },
    PhaseStackReadSecond => match previous.pending.instruction {
      None() => faulted(previous.pending.before, previous.pending.operation,
                        InvalidControlState, "missing paired stack read"),
      Some(instruction) =>
        if instruction.form.operation == Op_LRET then
          if not_bool(segment_image_valid(response.value)) then faulted(
            previous.pending.before, Op_LRET, InvalidControlState, "invalid return code segment"
          )
          else continue_with_request(
            previous, PhaseTargetExecuteProbe, previous.pending.ordinal + 1,
            previous.pending.captured_first, response.value,
            target_probe_request(previous.pending.ordinal + 1, response.value,
                                 previous.pending.captured_first)
          )
        else {
          var updated = previous.pending.after;
          match operand_named(instruction, "pair_id") {
            Some(pair) => {
              let first = pair_first_index(unsigned(pair.value[2 .. 0]));
              let first_index = unsigned(get_slice_int(4, first, 0));
              let second_index = unsigned(get_slice_int(4, first + 1, 0));
              if instruction.form.operation == Op_FPOPP then {
                updated.floating_registers[first_index] = response.value;
                updated.floating_registers[second_index] = previous.pending.captured_first;
                updated.fp_component_modified = true
              }
              else {
                updated.registers[first_index] = response.value;
                updated.registers[second_index] = previous.pending.captured_first
              }
            },
            None() => (),
          };
          completed(previous.pending.before, updated, CommitRegisters, [||])
        },
    },
    PhaseAtomicRmw => match previous.pending.instruction {
      None() => faulted(previous.pending.before, previous.pending.operation,
                        InvalidControlState, "missing atomic continuation"),
      Some(instruction) => {
        let width = operation_width(instruction);
        let equal = narrow_bits(response.value, width)
                  == narrow_bits(previous.pending.captured_first, width);
        if instruction.form.operation == Op_CMPXCHG
           & response.atomic_store_happened != equal then
          faulted(previous.pending.before, Op_CMPXCHG, InvalidControlState,
                  "inconsistent CMPXCHG atomic acknowledgement")
        else if instruction.form.operation != Op_CMPXCHG
                & not_bool(response.atomic_store_happened) then
          faulted(previous.pending.before, instruction.form.operation, InvalidControlState,
                  "atomic operation did not acknowledge its store")
        else {
        var updated = previous.pending.after;
        let destination = previous.pending.destination;
        if destination.kind == "Rn" then {
          let index = unsigned(destination.index);
          updated.registers[index] = merge_narrow(
            updated.registers[index], response.value, width
          )
        } else ();
        if instruction.form.operation == Op_CMPXCHG then
          updated.flags = flags_value(equal, false, false, false)
        else ();
        completed(previous.pending.before, updated, CommitMemory, [||])
        }
      },
    },
    PhaseCacheTranslate => match previous.pending.instruction {
      None() => faulted(previous.pending.before, previous.pending.operation,
                        InvalidControlState, "missing cache translation continuation"),
      Some(instruction) => {
        if response.address_type == 1 then completed(
          previous.pending.before, previous.pending.after, previous.pending.kind, [||]
        )
        else {
          let granule = unsigned(previous.request.auxiliary);
          let prefetch = instruction.form.operation == Op_PREFETCH
                       | instruction.form.operation == Op_PREFETCHNT;
          let physical = response.value;
          let block_start = physical & not_vec(bits_from_int(granule - 1));
          let request = { previous.request with
            kind = if prefetch then PrefetchHint else CacheMaintenanceBlock,
            role = if prefetch then "physical_prefetch" else "physical_cache_block",
            ordinal = previous.pending.ordinal + 1, address_translation = false,
            effective_address = physical, linear_address = physical,
            range_start = if prefetch then physical else block_start,
            range_end = if prefetch then add_bits(physical, 0x0000000000000001)
                        else add_bits(block_start, bits_from_int(granule)),
            range_length = if prefetch then 1 else granule,
            address_type = response.address_type, cache_policy = response.cache_policy,
            commit_point = true };
          continue_with_request(
            previous, PhaseCacheMaintenance, previous.pending.ordinal + 1,
            physical, previous.pending.captured_second, request
          )
        }
      },
    },
    PhaseCacheMaintenance => completed(
      previous.pending.before, previous.pending.after, previous.pending.kind, [||]
    ),
    PhaseFenceCompletion => completed(
      previous.pending.before, previous.pending.after, previous.pending.kind, [||]
    ),
    PhaseTlbOperation => completed(
      previous.pending.before, previous.pending.after, previous.pending.kind, [||]
    ),
    PhaseTranslationQuery => faulted(
      previous.pending.before, previous.pending.operation, InvalidControlState,
      "opaque translation-query response is not accepted"
    ),
    PhasePteRead => match previous.pending.instruction {
      None() => faulted(previous.pending.before, previous.pending.operation,
                        InvalidControlState, "missing PTE-walk continuation"),
      Some(instruction) => {
        let level = unsigned(previous.request.selector);
        let target_level = unsigned(previous.request.expected);
        let raw = response.value;
        let permissions = previous.request.auxiliary & pte_permission_bits(raw);
        let valid = pte_structurally_valid(raw, level);
        if instruction.form.operation == Op_PTQUERY & level == target_level then
          query_result(previous, raw, valid, permissions)
        else if not_bool(valid) then query_result(
          previous, 0x0000000000000000, false, 0x0000000000000000
        )
        else if level == 1 then {
          let physical = (raw & paging_pfn_mask(previous.pending.before.controls[0]))
                       | (previous.request.value & 0x0000000000000FFF);
          query_result(previous, physical, true, permissions)
        }
        else {
          let next_level = level - 1;
          let table = raw & paging_pfn_mask(previous.pending.before.controls[0]);
          continue_with_request(
            previous, PhasePteRead, previous.pending.ordinal + 1,
            previous.pending.captured_first, previous.pending.captured_second,
            pte_read_request(previous.pending.before, instruction, previous.request.value,
                             table, next_level, target_level, permissions,
                             previous.pending.ordinal + 1)
          )
        }
      },
    },
    PhaseContextSwitch => match previous.pending.instruction {
      None() => faulted(previous.pending.before, previous.pending.operation,
                        InvalidControlState, "missing context-switch continuation"),
      Some(instruction) => {
        var updated = previous.pending.after;
        updated.controls[0] = previous.pending.captured_first;
        updated.controls[1] = if instruction.form.operation == Op_SWPTA
          then sail_shiftleft(previous.pending.captured_second & 0x000000000000FFFF, 16)
               | 0x0000000000000001
          else 0x0000000000000000;
        completed(previous.pending.before, updated, CommitControl, [||])
      },
    },
    PhaseStateSave => completed(
      previous.pending.before, previous.pending.after, CommitMemory, [||]
    ),
    PhaseStateRestoreHeader => {
      let header : bits(64) = match read_le_bits(response.body_bytes, 0, 64) {
        Some(value) => value,
        None() => 0x0000000000000000,
      };
      let bitmap : bits(64) = match read_le_bits(response.body_bytes, 8, 64) {
        Some(value) => value,
        None() => 0x0000000000000000,
      };
      if byte_list_length(response.body_bytes) < 16
         | header[3 .. 0] != previous.pending.before.save_format
         | header[19 .. 10] != 0b0000000000
         | header[63 .. 52] != 0x000
         | (bitmap & 0xFFFFFFFFFFFFFFFE) != 0x0000000000000000
         | (bitmap[0] == bitone & not_bool(previous.pending.before.fp_component_present))
      then faulted(previous.pending.before, Op_RESTORE,
                   InvalidControlState, "invalid RESTORE header or component bitmap")
      else {
        let size = previous.pending.before.save_area_size;
        let request = { previous.request with
          selector = 0x0000000000000001, access = AccessAddressOnly,
          range_end = add_bits(previous.request.range_start, bits_from_int(size)),
          range_length = size,
          range_wrap = size > 0
            & unsigned(add_bits(previous.request.range_start, bits_from_int(size)))
              < unsigned(previous.request.range_start)
            & add_bits(previous.request.range_start, bits_from_int(size))
              != 0x0000000000000000,
          range_end_at_modulus = size > 0
            & add_bits(previous.request.range_start, bits_from_int(size))
              == 0x0000000000000000
            & previous.request.range_start != 0x0000000000000000,
          body_length = size, commit_point = false };
        continue_with_request(
          previous, PhaseStateRestoreRange, previous.pending.ordinal + 1,
          header, bitmap, request
        )
      }
    },
    PhaseStateRestoreRange => {
      let request = { previous.request with
        selector = 0x0000000000000002, access = AccessLoad, commit_point = true,
        expected = previous.pending.captured_first,
        desired = previous.pending.captured_second,
        range_length = previous.pending.before.save_area_size,
        body_length = previous.pending.before.save_area_size };
      continue_with_request(
        previous, PhaseStateRestore, previous.pending.ordinal + 1,
        previous.pending.captured_first, previous.pending.captured_second, request
      )
    },
    PhaseStateRestore => {
      let image_header : bits(64) = match read_le_bits(response.body_bytes, 0, 64) {
        Some(value) => value,
        None() => 0x0000000000000000,
      };
      let image_bitmap : bits(64) = match read_le_bits(response.body_bytes, 8, 64) {
        Some(value) => value,
        None() => 0x0000000000000000,
      };
      if byte_list_length(response.body_bytes) < 16
         | image_header != previous.pending.captured_first
         | image_bitmap != previous.pending.captured_second then
        faulted(previous.pending.before, Op_RESTORE, InvalidControlState,
                "RESTORE image changed after header validation")
      else restore_raw_image(previous, response.body_bytes, image_header, image_bitmap)
    },
    PhaseRepeatFetch => match previous.pending.instruction {
      None() => faulted(previous.pending.before, previous.pending.operation,
                        InvalidControlState, "missing repeat continuation"),
      Some(prefix) => {
        let repeat_context = previous.pending.after.repeat_state;
        let bytes = if response.body_bytes == [||] then repeat_context.fixed_body
                    else response.body_bytes;
        let same_body = repeat_context.fixed_body == [||] | bytes == repeat_context.fixed_body;
        if not_bool(same_body) then faulted(
          previous.pending.before, prefix.form.operation,
          InvalidControlState, "repeat body changed after entry"
        )
        else if repeat_context.grouped then {
          let length = unsigned(repeat_context.body_bytes);
          if length == 0 | byte_list_length(bytes) != length
             | not_bool(valid_repg_body(bytes, length, previous.pending.before))
          then faulted(previous.pending.before, Op_REPG,
                       IllegalInstruction, "invalid REPG body boundary or eligibility")
          else if repeat_context.remaining == 0x0000000000000000 then {
            var updated = previous.pending.after;
            updated.repeat_state = { repeat_context with active = false, fixed_body = bytes };
            updated.pc = add_bits(repeat_context.body_start, bits_from_int(length));
            let done = completed(previous.pending.before, updated, CommitControl, [||]);
            { done with pending = { done.pending with boundary_class = BoundaryRepeatGroup } }
          }
          else {
            var iteration_state = previous.pending.after;
            iteration_state.pc = repeat_context.body_start;
            iteration_state.repeat_state = { repeat_context with fixed_body = bytes };
            run_repeat_group_tail(bytes, bytes, length, iteration_state)
          }
        }
        else match decode_full_record(bytes) {
          None() => faulted(previous.pending.before, Op_REPcc,
                            IllegalInstruction, "malformed REPcc body"),
          Some(body) =>
            if not_bool(if unsigned(repeat_context.condition) == 0
                        then body.form.repeat_rep else body.form.repeat_repcc)
               | not_bool(repeat_body_available(body, previous.pending.before))
               | repeat_body_control_forbidden(body)
            then faulted(previous.pending.before, Op_REPcc,
                         IllegalInstruction, "ineligible REPcc body")
            else if byte_list_length(bytes) != body.encoded_length then faulted(
              previous.pending.before, Op_REPcc, IllegalInstruction,
              "REPcc body fetch must contain exactly one record"
            )
            else if repeat_context.remaining == 0x0000000000000000 then {
              var updated = previous.pending.after;
              updated.repeat_state = { repeat_context with active = false, fixed_body = bytes };
              updated.pc = add_bits(repeat_context.body_start, bits_from_int(body.encoded_length));
              let done = completed(previous.pending.before, updated, CommitControl, [||]);
              { done with pending = {
                  done.pending with boundary_class = BoundaryRepeatIteration } }
            }
            else {
              var iteration_state = previous.pending.after;
              iteration_state.pc = repeat_context.body_start;
              iteration_state.repeat_state = { repeat_context with fixed_body = bytes };
              run_repeat_single(body, bytes, iteration_state)
            },
        }
      },
    },
    PhaseCpuidQuery => commit_response_destination(
      previous, if response.known then response.value else 0x0000000000000000,
      { response with write_flags = false, generated_fflags = 0b00000,
                      state_image = initial_cpu() }
    ),
    PhasePerformanceCounter =>
      if previous.request.selector == 0x0000000000000000
         | not_bool(response.known) | not_bool(response.present) then
        faulted(previous.pending.before, Op_RDPMC, InvalidControlState,
                "RDPMC counter is absent or selector zero")
      else commit_response_destination(
        previous, response.value,
        { response with write_flags = false, generated_fflags = 0b00000,
                        state_image = initial_cpu() }
      ),
    PhaseControlTransition => match previous.pending.instruction {
      None() => faulted(previous.pending.before, previous.pending.operation,
                        InvalidControlState, "missing control-register continuation"),
      Some(instruction) =>
        if instruction.form.operation == Op_SYSCALL | instruction.form.operation == Op_SYSRET
        then completed(
          previous.pending.before, previous.pending.after, CommitControl, [||]
        )
        else match control_index(unsigned(previous.pending.captured_first[15 .. 0])) {
        None() => faulted(previous.pending.before, Op_WRCR,
                          InvalidControlState, "unknown control-register selector"),
        Some(index) => {
          var updated = previous.pending.after;
          updated.controls[unsigned(index)] = previous.pending.captured_second;
          completed(previous.pending.before, updated, CommitControl, [||])
        },
        },
    },
    PhaseResetSerialize => completed(
      previous.pending.before, warm_reset_state(previous.pending.before), CommitControl, [||]
    ),
    PhaseEventTargetProbe => match previous.pending.event {
      None() => event_shutdown(previous.pending.before),
      Some(event) =>
        if not_bool(event_stack_state_valid(event, previous.pending.before)) then
          event_delivery_failed(previous, 1)
        else if not_bool(event_frame_address_valid(event, previous.pending.before)) then {
          let request = event_stack_range_request(
            event, previous.pending.before, previous.pending.ordinal + 1
          );
          event_delivery_failed({ previous with request = request }, 2)
        }
        else continue_with_request(
          previous, PhaseEventStackProbe, previous.pending.ordinal + 1,
          previous.pending.captured_first, previous.pending.captured_second,
          event_stack_range_request(event, previous.pending.before,
                                    previous.pending.ordinal + 1)
        ),
    },
    PhaseEventStackProbe => match previous.pending.event {
      None() => event_shutdown(previous.pending.before),
      Some(event) => continue_with_request(
        previous, PhaseEventFrameStore, previous.pending.ordinal + 1,
        previous.pending.captured_first, previous.pending.captured_second,
        event_frame_store_request(event, previous.pending.before,
                                  previous.pending.ordinal + 1)
      ),
    },
    PhaseEventFrameStore => match previous.pending.event {
      None() => event_shutdown(previous.pending.before),
      Some(event) => {
        var updated = previous.pending.before;
        updated.sp = previous.request.range_start;
        updated.pc = previous.pending.before.controls[12];
        updated.segments[0] = previous.pending.before.controls[13];
        updated.segments[1] = previous.pending.before.controls[14];
        updated.segments[2] = previous.request.segment_image;
        updated.status = (previous.pending.before.status & 0x0000000000000002)
                       | 0x0000000000000011;
        if event.kind == EventNmi then {
          updated.status = updated.status | 0x0000000000000002;
          if previous.pending.before.nmi_relatched then {
            updated.controls[2] = updated.controls[2] | 0x0000000000000080;
            updated.nmi_latched_source = previous.pending.before.nmi_relatched_source
          }
          else {
            updated.controls[2] = updated.controls[2] & 0xFFFFFFFFFFFFFF7F;
            updated.nmi_latched_source = 0x000000
          };
          updated.nmi_relatched = false;
          updated.nmi_relatched_source = 0x000000
        } else ();
        if event.code == 0x00000019 then {
          updated.machine_check_pending = false;
          updated.machine_check_payload = 0x00000000;
          updated.machine_check_error_code = 0x0000000000000000;
          updated.machine_check_fault_ea = 0x0000000000000000;
          updated.machine_check_fault_linear = 0x0000000000000000;
          updated.machine_check_event_aux = 0x0000000000000000
        } else ();
        updated.supervisor = true;
        updated.event_depth = previous.pending.before.event_depth + 1;
        updated.event_stack_level = if event_retain_stack(event, previous.pending.before)
          then previous.pending.before.event_stack_level else event_requested_level(event);
        updated.repeat_state = { updated.repeat_state with active = false };
        updated.run_state = Running;
        updated.halted = false;
        let done = completed(previous.pending.before, updated, CommitEvent, [||]);
        { done with pending = { done.pending with boundary_class = BoundaryEventEntry } }
      },
    },
    PhaseEventFrameHeader =>
      let control : bits(64) = match read_le_bits(response.body_bytes, 0, 64) {
        Some(value) => value,
        None() => 0x0000000000000000,
      } in
      if byte_list_length(response.body_bytes) < 8
         | not_bool(valid_frame_control(control, previous.pending.before)) then faulted(
        previous.pending.before, Op_ERET, InvalidControlState, "invalid FRAME_CONTROL"
      )
      else {
        let frame_bytes = unsigned(control[7 .. 0]) * 8;
        let request = { stack_request(
          EventFrameAccess, previous.pending.ordinal + 1, previous.pending.before,
          previous.pending.before.sp,
          add_bits(previous.pending.before.sp, bits_from_int(frame_bytes)),
          AccessStackRead, 0x0000000000000000, false
        ) with selector = 0x0000000000000001, expected = control,
               width = frame_bytes, range_length = frame_bytes,
               state_image = previous.pending.before };
        continue_with_request(
          previous, PhaseEventFrame, previous.pending.ordinal + 1,
          control, 0x0000000000000000, request
        )
      },
    PhaseEventFrame => continue_event_return(previous, response.body_bytes),
    PhaseEventReturnBody => {
      let repeat_state = previous.pending.after.repeat_state;
      let bytes = if repeat_state.grouped then response.body_bytes
                  else match decode_next_record(response.body_bytes) {
                    Some(body) => take_bytes(response.body_bytes, body.encoded_length),
                    None() => [||],
                  };
      let valid : bool = if repeat_state.grouped then
        if byte_list_length(bytes) != unsigned(repeat_state.body_bytes) then false
        else if not_bool(valid_repg_body(
          bytes, unsigned(repeat_state.body_bytes), previous.pending.after
        )) then false
        else repg_offset_is_boundary(bytes, repeat_state.group_progress)
      else match decode_full_record(bytes) {
        Some(body) => {
          let eligible : bool = if unsigned(repeat_state.condition) == 0
            then body.form.repeat_rep else body.form.repeat_repcc;
          if not_bool(eligible) then false
          else if not_bool(repeat_body_available(body, previous.pending.after)) then false
          else not_bool(repeat_body_control_forbidden(body))
        },
        None() => false,
      };
      if not_bool(valid) then faulted(
        previous.pending.before, Op_ERET, InvalidControlState,
        "invalid restored repeat body"
      )
      else {
        var candidate = previous.pending.after;
        candidate.repeat_state = { repeat_state with fixed_body = bytes };
        let staged = { previous with pending = { previous.pending with after = candidate } };
        continue_with_request(
          staged, PhaseEventReturnExecute, previous.pending.ordinal + 1,
          previous.pending.captured_first, previous.pending.captured_second,
          target_probe_request(previous.pending.ordinal + 1,
                               previous.pending.captured_second,
                               previous.pending.captured_first)
        )
      }
    },
    PhaseEventReturnExecute => completed(
      previous.pending.before, previous.pending.after, CommitEvent, [||]
    ),
    PhaseFpContractQuery => fp_preserve_repeat_parent(previous, match previous.pending.instruction {
      None() => faulted(previous.pending.before, previous.pending.operation,
                        InvalidControlState, "missing FPTRANSA contract continuation"),
      Some(instruction) => match fp_semantics(instruction.form.operation) {
        None() => faulted(previous.pending.before, instruction.form.operation,
                          InvalidControlState, "missing FPTRANSA semantics"),
        Some(semantics) => {
          let lookup = fptrans_contract_lookup(semantics.contract_id, response.value);
          if not_bool(response.known) | lookup.status == FptransContractUnknown
             | not_bool(response.present) | lookup.status == FptransContractAbsent then
            faulted_with_error_code(
              previous.pending.before, instruction.form.operation,
              IllegalInstruction, "FPTRANSA contract absent or unknown",
              0x0000000000000003
            )
          else if lookup.status == FptransContractMalformed then
            faulted(previous.pending.before, instruction.form.operation,
                    InvalidControlState, "FPTRANSA contract malformed")
          else fp_start_operands(instruction, previous.pending.before, response.value)
        },
      },
    }),
    PhaseFpSourceRead => fp_preserve_repeat_parent(previous, match previous.pending.instruction {
      None() => faulted(previous.pending.before, previous.pending.operation,
                        InvalidControlState, "missing FP source continuation"),
      Some(instruction) => match fp_semantics(instruction.form.operation) {
        None() => faulted(previous.pending.before, instruction.form.operation,
                          InvalidControlState, "missing FP source semantics"),
        Some(semantics) => {
          let source_index = previous.pending.fp_pending.next_source;
          match fp_source_at(instruction.operands, source_index, 0) {
            None() => faulted(previous.pending.before, instruction.form.operation,
                              InvalidControlState, "missing FP source operand"),
            Some(source) => {
              let captured_kind = fp_operand_kind_for(
                instruction, source, operation_width(instruction)
              );
              let captured : Fp_operand_image = struct {
                valid = true,
                kind = captured_kind,
                bits = if captured_kind == FpBits32
                  then 0x00000000 @ response.value[31 .. 0] else response.value
              };
              match fp_operand_slot_set(
                fp_pending_raw_slots(previous.pending.fp_pending),
                source_index, captured
              ) {
                None() => faulted(previous.pending.before, instruction.form.operation,
                                  InvalidControlState, "invalid FP source slot"),
                Some(slots) => {
                  let missing = fp_first_missing_source(slots, semantics.source_count, 0);
                  let next_pending = { fp_pending_with_slots(
                    previous.pending.fp_pending, slots
                  ) with next_source = missing };
                  if missing < semantics.source_count then {
                    let evaluated = evaluate_instruction_eas(
                      instruction.operands, instruction.form.operation,
                      previous.pending.before, previous.pending.before.pc,
                      operation_width(instruction)
                    );
                    match fp_source_at(instruction.operands, missing, 0) {
                      Some(next_source) => match evaluation_named(
                        next_source.name, evaluated.evaluations
                      ) {
                        Some(evaluation) => fp_waiting(
                          previous.pending.before, previous.pending.after, instruction,
                          PhaseFpSourceRead, previous.pending.ordinal + 1,
                          request_for_evaluation(
                            MemoryRead, previous.pending.ordinal + 1, evaluation,
                            AccessLoad, 0x0000000000000000, false
                          ), next_pending
                        ),
                        None() => faulted(previous.pending.before,
                                          instruction.form.operation,
                                          InvalidControlState,
                                          "missing next FP source evaluation"),
                      },
                      None() => faulted(previous.pending.before,
                                        instruction.form.operation,
                                        InvalidControlState,
                                        "missing next FP source operand"),
                    }
                  }
                  else fp_continue_after_sources(
                    instruction, previous.pending.before, previous.pending.after,
                    next_pending, previous.pending.fp_pending.contract_word,
                    previous.pending.ordinal + 1
                  )
                },
              }
            },
          }
        },
      },
    }),
    PhaseFpDestinationProbe => fp_preserve_repeat_parent(previous, match previous.pending.instruction {
      None() => faulted(previous.pending.before, previous.pending.operation,
                        InvalidControlState, "missing FP destination continuation"),
      Some(instruction) => fp_start_compute(
        instruction, previous.pending.before, previous.pending.after,
        previous.pending.fp_pending, previous.pending.fp_pending.contract_word,
        previous.pending.ordinal + 1
      ),
    }),
    PhaseFpCompute => fp_preserve_repeat_parent(previous, match previous.pending.instruction {
      None() => faulted(previous.pending.before, previous.pending.operation,
                        InvalidControlState, "missing FP compute continuation"),
      Some(instruction) => fp_commit_candidate(
        previous.pending.before, previous.pending.after, instruction,
        fp_finalize_response(previous.request.fp_request, response.fp_response,
                             previous.pending.before.fstatus),
        previous.pending.fp_pending, previous.pending.ordinal + 1
      ),
    }),
    PhaseFpDestinationWrite => completed(
      previous.pending.before, previous.pending.after, CommitMemory, [||]
    ),
    PhaseIntegerExternal => commit_response_destination(previous, response.value, response),
    _ => faulted(previous.pending.before, previous.pending.operation,
                 InvalidControlState, "unexpected transaction phase"),
  }

function resume_transaction(previous : Execution_result, response : Transaction_response)
  -> Execution_result = {
  let result = resume_transaction_inner(previous, response);
  if result.awaiting_environment | result.fault != None() then result
  else if previous.pending.repeat_parent_active then
    match previous.pending.repeat_body {
      None() => faulted(previous.pending.before, previous.pending.operation,
                        InvalidControlState, "missing repeat parent body"),
      Some(body) =>
        if previous.pending.repeat_parent_grouped then finish_repeat_group_step(
          previous.pending.repeat_bytes, previous.pending.repeat_tail_length,
          previous.pending.before, result
        )
        else finish_repeat_single(
          body, previous.pending.repeat_bytes, previous.pending.before,
          result.state, previous.pending.captured_first
        ),
    }
  else result
}

