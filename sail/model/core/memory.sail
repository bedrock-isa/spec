function warm_reset_state(state : Cpu_state) -> Cpu_state = {
  var reset = initial_cpu();
  reset.fp_enabled = state.fp_enabled;
  reset.fptrans_enabled = state.fptrans_enabled;
  reset.cache_maintenance_granule = state.cache_maintenance_granule;
  reset.save_area_size = state.save_area_size;
  reset.save_fixed_size = state.save_fixed_size;
  reset.save_format = state.save_format;
  reset.save_bitmap_words = state.save_bitmap_words;
  reset.fp_component_present = state.fp_component_present;
  reset.fp_component_id = state.fp_component_id;
  reset.fp_component_bitmap_bit = state.fp_component_bitmap_bit;
  reset.fp_component_offset = state.fp_component_offset;
  reset.fp_component_size = state.fp_component_size;
  reset.fp_component_alignment = state.fp_component_alignment;
  reset.fp_component_init_policy = state.fp_component_init_policy;
  reset.controls[23] = state.controls[23];
  reset.controls[24] = state.controls[24];
  reset.pc = state.controls[23];
  reset.status = 0x0000000000000010;
  reset.supervisor = true;
  reset.halted = false;
  reset.run_state = Running;
  reset
}

function evaluation_named(name : string, evaluations : list(Ea_evaluation))
  -> option(Ea_evaluation) = match evaluations {
  [||] => None(),
  evaluation :: tail => if evaluation.operand_name == name then Some(evaluation)
                        else evaluation_named(name, tail),
}

function memory_evaluation_for(operands : list(Decoded_operand), evaluations : list(Ea_evaluation),
                               source : bool) -> option(Ea_evaluation) = match operands {
  [||] => None(),
  operand :: tail => match evaluation_named(operand.name, evaluations) {
    Some(evaluation) =>
      if evaluation.kind == "memory"
         & (if source then operand.access == AccessRead | operand.access == AccessReadWrite
            else operand.access == AccessWrite | operand.access == AccessReadWrite)
      then Some(evaluation)
      else memory_evaluation_for(tail, evaluations, source),
    None() => memory_evaluation_for(tail, evaluations, source),
  },
}

function next_memory_source(operands : list(Decoded_operand), evaluations : list(Ea_evaluation),
                            previous_name : string) -> option(Ea_evaluation) = match operands {
  [||] => None(),
  operand :: tail => match evaluation_named(operand.name, evaluations) {
    Some(evaluation) =>
      if evaluation.kind == "memory" & evaluation.operand_name != previous_name
         & (operand.access == AccessRead | operand.access == AccessReadWrite)
      then Some(evaluation)
      else next_memory_source(tail, evaluations, previous_name),
    None() => next_memory_source(tail, evaluations, previous_name),
  },
}

function evaluation_option_named(value : option(Ea_evaluation), name : string) -> bool = match value {
  Some(item) => item.operand_name == name,
  None() => false,
}

function evaluation_option_name(value : option(Ea_evaluation)) -> string = match value {
  Some(item) => item.operand_name,
  None() => "",
}

function request_for_evaluation(kind : Primitive_request_kind, ordinal : int,
                                evaluation : Ea_evaluation, access : Transaction_access,
                                value : bits(64), commit_point : bool) -> Primitive_request = struct {
  kind = kind, ordinal = ordinal, role = evaluation.role, domain = evaluation.domain,
  segment = evaluation.segment, segment_image = evaluation.segment_image,
  width = evaluation.width, range_start = evaluation.effective_address,
  range_end = add_bits(evaluation.effective_address, get_slice_int(64, evaluation.width, 0)),
  range_length = evaluation.width,
  range_wrap = unsigned(evaluation.effective_address) + evaluation.width > 18446744073709551616,
  range_end_at_modulus = unsigned(evaluation.effective_address) + evaluation.width
                         == 18446744073709551616,
  effective_address = evaluation.effective_address, linear_address = evaluation.linear_address,
  access = access, value = value, address_translation = true, commit_point = commit_point,
  memory_order = ordinal, address_type = 0, cache_policy = 0,
  suppress_fault = false, staged_updates = evaluation.staged_updates
  , selector = 0x0000000000000000, expected = 0x0000000000000000,
  desired = 0x0000000000000000, auxiliary = 0x0000000000000000, body_length = 0,
  payload_bytes = [||], fp_request = empty_fp_request(),
  state_image = initial_cpu()
}

function waiting_transaction(before : Cpu_state, after : Cpu_state,
                             instruction : Decoded_instruction, kind : Commit_kind,
                             destination : Commit_destination, phase : Continuation_phase,
                             ordinal : int, first : bits(64), second : bits(64),
                             request : Primitive_request) -> Execution_result = struct {
  state = before,
  pending = { empty_pending(before, after, instruction.form.operation, kind) with
    destination = destination, instruction = Some(instruction), phase = phase,
    ordinal = ordinal, captured_first = first, captured_second = second },
  request = request, effects = [||], fault = None(), awaiting_environment = true
}

function source_value_for_transaction(instruction : Decoded_instruction, state : Cpu_state)
  -> bits(64) = if instruction.form.operation == Op_SET then 0x0000000000000001
  else match value_named(instruction, state, "src") {
  Some(value) => value,
  None() => match value_named(instruction, state, "reg") {
    Some(value) => value,
    None() => 0x0000000000000000,
  },
}

function start_memory_transaction(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) = {
  let width = operation_width(instruction);
  let evaluated = evaluate_instruction_eas(
    instruction.operands, instruction.form.operation, state, state.pc, width
  );
  let source = memory_evaluation_for(instruction.operands, evaluated.evaluations, true);
  let destination = memory_evaluation_for(instruction.operands, evaluated.evaluations, false);
  let after = advance_pc(evaluated.image, instruction);
  let commit_target = commit_destination_for(instruction.operands, width);
  match source {
    Some(evaluation) => Some(waiting_transaction(
      state, after, instruction, CommitMemory, commit_target, PhaseSourceRead, 0,
      0x0000000000000000, 0x0000000000000000,
      request_for_evaluation(MemoryRead, 0, evaluation, AccessLoad,
                             0x0000000000000000, false)
    )),
    None() => match destination {
      Some(evaluation) => {
        let raw_value = source_value_for_transaction(instruction, state);
        let signed_extension = instruction.form.operation == Op_EXTSW
                            | instruction.form.operation == Op_EXTSL
                            | instruction.form.operation == Op_EXTSQ;
        let extension = instruction.form.operation == Op_EXTZW
                      | instruction.form.operation == Op_EXTSW
                      | instruction.form.operation == Op_EXTZL
                      | instruction.form.operation == Op_EXTSL
                      | instruction.form.operation == Op_EXTZQ
                      | instruction.form.operation == Op_EXTSQ;
        let value = if extension then
          if signed_extension then sign_extend_width(raw_value, width)
          else narrow_bits(raw_value, width)
        else raw_value;
        Some(waiting_transaction(
          state, after, instruction, CommitMemory, commit_target, PhaseDestinationWrite, 0,
          value, 0x0000000000000000,
          request_for_evaluation(
            if instruction.form.operation == Op_MOVNT then NonTemporalStore else MemoryStore,
            0, evaluation, AccessStore, value, true
          )
        ))
      },
      None() => None(),
    },
  }
}

function atomic_selector(operation : Semantic_operation) -> bits(64) =
  if operation == Op_CMPXCHG then 0x0000000000000000
  else if operation == Op_FETCHADD then 0x0000000000000001
  else if operation == Op_FETCHAND then 0x0000000000000002
  else if operation == Op_FETCHOR then 0x0000000000000003
  else if operation == Op_FETCHSUB then 0x0000000000000004
  else 0x0000000000000005

function start_atomic_transaction(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) = {
  let width = operation_width(instruction);
  let evaluated = evaluate_instruction_eas(
    instruction.operands, instruction.form.operation, state, state.pc, width
  );
  match evaluation_named("memory", evaluated.evaluations) {
    None() => None(),
    Some(memory) => {
      let operation = instruction.form.operation;
      let order : int = match value_named(instruction, state, "order") {
        Some(value) => unsigned(value[2 .. 0]), None() => 0
      };
      let expected : bits(64) = match value_named(instruction, state, "expected") {
        Some(value) => narrow_bits(value, width), None() => 0x0000000000000000
      };
      let source : bits(64) = match value_named(instruction, state, "src") {
        Some(value) => narrow_bits(value, width), None() => 0x0000000000000000
      };
      let desired : bits(64) = match value_named(instruction, state, "desired") {
        Some(value) => narrow_bits(value, width), None() => 0x0000000000000000
      };
      let destination = if operation == Op_CMPXCHG
        then commit_destination_for([|match operand_named(instruction, "expected") {
          Some(operand) => operand,
          None() => return None(),
        }|], width)
        else commit_destination_for([|match operand_named(instruction, "src") {
          Some(operand) => operand,
          None() => return None(),
        }|], width);
      let request = { request_for_evaluation(
        AtomicReadModifyWrite, 0, memory, AccessReadModifyWrite, source, true
      ) with memory_order = order, selector = atomic_selector(operation), expected = expected,
             desired = desired, state_image = state };
      Some(waiting_transaction(
        state, advance_pc(evaluated.image, instruction), instruction, CommitMemory,
        destination, PhaseAtomicRmw, 0, expected, source, request
      ))
    },
  }
}

function first_evaluation(evaluations : list(Ea_evaluation)) -> option(Ea_evaluation) =
  match evaluations {
    [||] => None(),
    evaluation :: _ => Some(evaluation),
  }

function append_bytes(left : list(bits(8)), right : list(bits(8))) -> list(bits(8)) =
  match left {
    [||] => right,
    byte :: tail => byte :: append_bytes(tail, right),
  }

function zero_byte_count(count : int) -> list(bits(8)) =
  if count <= 0 then [||] else 0x00 :: zero_byte_count(count - 1)

function le64_bytes(value : bits(64)) -> list(bits(8)) = [|
  value[7 .. 0], value[15 .. 8], value[23 .. 16], value[31 .. 24],
  value[39 .. 32], value[47 .. 40], value[55 .. 48], value[63 .. 56]
|]

function serialize_register_file(registers : Registers, index : int) -> list(bits(8)) =
  if index >= 16 then [||]
  else append_bytes(le64_bytes(registers[unsigned(get_slice_int(4, index, 0))]),
                    serialize_register_file(registers, index + 1))

function serialize_fp_file(registers : Floating_registers, index : int) -> list(bits(8)) =
  if index >= 16 then [||]
  else append_bytes(le64_bytes(registers[unsigned(get_slice_int(4, index, 0))]),
                    serialize_fp_file(registers, index + 1))

function serialize_saved_segments(segments : Segment_registers, index : int) -> list(bits(8)) =
  if index >= 9 then [||]
  else append_bytes(le64_bytes(image_segment({ initial_cpu() with segments = segments }, index)),
                    serialize_saved_segments(segments, index + 1))

function save_layout_valid(state : Cpu_state) -> bool =
  state.save_format == 0x0
  & state.save_bitmap_words == 1
  & state.save_fixed_size == 192
  & state.save_area_size >= state.save_fixed_size
  & tmod_int(state.save_area_size, 64) == 0
  & (if state.fp_component_present then
       state.fp_component_id == 1
       & state.fp_component_bitmap_bit == 0
       & state.fp_component_offset == 192
       & state.fp_component_alignment == 64
       & state.fp_component_size == 192
       & state.fp_component_offset + state.fp_component_size <= state.save_area_size
       & state.fp_component_init_policy == 1
     else true)

function save_header(state : Cpu_state) -> bits(64) =
  sail_shiftleft(state.status & 0x000000000000FFFF, 36)
  | sail_shiftleft(sail_zero_extend(state.flags, 64), 20)
  | 0x00000000000003F0
  | sail_zero_extend(state.save_format, 64)

function fp_save_payload(state : Cpu_state) -> list(bits(8)) = {
  let raw = append_bytes(
    serialize_fp_file(state.floating_registers, 0),
    append_bytes(le64_bytes(sail_zero_extend(state.fflags, 64)), le64_bytes(state.fstatus))
  );
  append_bytes(raw, zero_byte_count(state.fp_component_size - 144))
}

function save_image_bytes(state : Cpu_state) -> list(bits(8)) = {
  let include_fp = state.fp_component_present & state.fp_enabled & state.fp_component_modified;
  let bitmap : bits(64) = if include_fp then 0x0000000000000001 else 0x0000000000000000;
  let fixed = append_bytes(
    le64_bytes(save_header(state)),
    append_bytes(le64_bytes(bitmap),
      append_bytes(serialize_register_file(state.registers, 0),
                   serialize_saved_segments(state.segments, 3)))
  );
  let to_component = append_bytes(
    fixed, zero_byte_count((if state.fp_component_present then state.fp_component_offset
                            else state.save_area_size) - state.save_fixed_size)
  );
  if state.fp_component_present then {
    let component = if include_fp then fp_save_payload(state)
                    else zero_byte_count(state.fp_component_size);
    append_bytes(
      append_bytes(to_component, component),
      zero_byte_count(state.save_area_size - state.fp_component_offset
                      - state.fp_component_size)
    )
  }
  else to_component
}

function start_cache_transaction(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) = {
  let operation = instruction.form.operation;
  let evaluated = evaluate_instruction_eas(
    instruction.operands, operation, state, state.pc, 8
  );
  match first_evaluation(evaluated.evaluations) {
    None() => None(),
    Some(address) => {
      let prefetch = operation == Op_PREFETCH | operation == Op_PREFETCHNT;
      let request = { request_for_evaluation(
        AddressTranslateRequest,
        0, address, AccessAddressOnly, 0x0000000000000000, false
      ) with role = "cache_translate", suppress_fault = prefetch, selector =
        if operation == Op_FLSHDCACHE then 0x0000000000000000
        else if operation == Op_INVDCACHE then 0x0000000000000001
        else if operation == Op_INVICACHE then 0x0000000000000002
        else if operation == Op_WRBKDCACHE then 0x0000000000000003
        else if operation == Op_SYNCCACHE then 0x0000000000000004
        else if operation == Op_PREFETCHNT then 0x0000000000000006
        else 0x0000000000000005,
        auxiliary = bits_from_int(state.cache_maintenance_granule), state_image = state };
      Some(waiting_transaction(
        state, advance_pc(evaluated.image, instruction), instruction, CommitControl,
        empty_destination(), PhaseCacheTranslate, 0,
        address.effective_address, 0x0000000000000000, request
      ))
    },
  }
}

function paging_canonical(linear : bits(64), ptcr : bits(64)) -> bool =
  if ptcr[7] == bitone then
    linear[63 .. 57] == (if linear[56] == bitone then 0b1111111 else 0b0000000)
  else linear[63 .. 48] == (if linear[47] == bitone then 0xFFFF else 0x0000)

function paging_pfn_mask(ptcr : bits(64)) -> bits(64) =
  if ptcr[11 .. 8] == 0x1 then 0x00FFFFFFFFFFF000 else 0x0000FFFFFFFFF000

function paging_level_index(linear : bits(64), level : int) -> bits(64) = match level {
  5 => sail_shiftright(linear, 48) & 0x00000000000001FF,
  4 => sail_shiftright(linear, 39) & 0x00000000000001FF,
  3 => sail_shiftright(linear, 30) & 0x00000000000001FF,
  2 => sail_shiftright(linear, 21) & 0x00000000000001FF,
  _ => sail_shiftright(linear, 12) & 0x00000000000001FF,
}

function pte_permission_bits(pte : bits(64)) -> bits(64) =
  (if pte[3] == bitone then 0x0000000000000001 else 0x0000000000000000)
  | (if pte[1] == bitone then 0x0000000000000002 else 0x0000000000000000)
  | (if pte[2] == bitone then 0x0000000000000004 else 0x0000000000000000)

function pte_structurally_valid(pte : bits(64), level : int) -> bool =
  if pte[0] == bitzero then false
  else if level > 1 then
    pte[11] == bitone & pte[6] == bitzero & pte[4] == bitzero & pte[7] == bitzero
  else {
    let slot = pte[7] == bitone;
    pte[11] == bitzero
    & (if slot then pte[9 .. 8] == 0b01 & pte[2] == bitzero
                    & pte[5] == bitone & pte[6] == bitone
       else true)
  }

function pte_read_request(state : Cpu_state, instruction : Decoded_instruction,
                          linear : bits(64), table_base : bits(64), level : int,
                          target_level : int, permissions : bits(64), ordinal : int)
  -> Primitive_request = {
  let address = add_bits(table_base, sail_shiftleft(paging_level_index(linear, level), 3));
  { empty_primitive_request() with
    kind = PhysicalPteRead, ordinal = ordinal, role = if instruction.form.operation == Op_PTQUERY
      then "ptquery_pte" else "vtop_pte",
    domain = "physical_page_table", width = 8, range_start = address,
    range_end = add_bits(address, 0x0000000000000008), range_length = 8,
    effective_address = address, linear_address = address, access = AccessLoad,
    address_translation = false, commit_point = false, value = linear,
    selector = bits_from_int(level), expected = bits_from_int(target_level),
    auxiliary = permissions, state_image = state }
}

function query_result(previous : Execution_result, value : bits(64), valid : bool,
                      permissions : bits(64)) -> Execution_result = {
  var updated = previous.pending.after;
  let destination = previous.pending.destination;
  if destination.kind == "Rn" then
    updated.registers[unsigned(destination.index)] = value
  else ();
  updated.flags = if valid then
    flags_value(true, permissions[0] == bitone, permissions[1] == bitone,
                permissions[2] == bitone)
  else 0x0;
  completed(previous.pending.before, updated, CommitControl, [||])
}

function start_tlb_context_transaction(instruction : Decoded_instruction, state : Cpu_state)
  -> Execution_result = {
  let operation = instruction.form.operation;
  let evaluated = evaluate_instruction_eas(
    instruction.operands, operation, state, state.pc, 8
  );
  let address : Ea_evaluation = match first_evaluation(evaluated.evaluations) {
    Some(value) => value, None() => struct {
      operand_name = "", kind = "", role = "", domain = "", segment = 0,
      segment_image = 0x0000000000000000, width = 8,
      effective_address = 0x0000000000000000, linear_address = 0x0000000000000000,
      value = 0x0000000000000000, staged_updates = [||]
    }
  };
  let selector = if operation == Op_INVASID then match value_named(instruction, state, "asid") {
      Some(value) => value & 0x000000000000FFFF, None() => 0x0000000000000000
    }
    else if operation == Op_PTQUERY then match value_named(instruction, state, "level") {
      Some(value) => value & 0x0000000000000007, None() => 0x0000000000000000
    }
    else if operation == Op_SWPTA then match value_named(instruction, state, "asid") {
      Some(value) => value & 0x000000000000FFFF, None() => 0x0000000000000000
    }
    else 0x0000000000000000;
  let value = if operation == Op_VTOP then match value_named(instruction, state, "virt") {
      Some(item) => item, None() => 0x0000000000000000
    }
    else if operation == Op_SWPT | operation == Op_SWPTA then
      match value_named(instruction, state, "new_ptcr") {
        Some(item) => item, None() => 0x0000000000000000
      }
    else address.linear_address;
  let kind = if operation == Op_INVASID | operation == Op_INVPAGE | operation == Op_INVTLB
    then TlbInvalidateRequest
    else if operation == Op_PTQUERY | operation == Op_VTOP then PhysicalPteRead
    else if operation == Op_SAVE then StateSaveRequest
    else if operation == Op_RESTORE then StateRestoreRequest
    else ContextSwitchRequest;
  let phase = if kind == TlbInvalidateRequest then PhaseTlbOperation
    else if kind == PhysicalPteRead then PhasePteRead
    else if kind == StateSaveRequest then PhaseStateSave
    else if kind == StateRestoreRequest then PhaseStateRestore
    else PhaseContextSwitch;
  let destination = commit_destination_for(instruction.operands, 8);
  let save_range = operation == Op_SAVE | operation == Op_RESTORE;
  let save_size = state.save_area_size;
  let save_end = add_bits(address.effective_address, bits_from_int(save_size));
  let base_request = request_for_evaluation(
    kind, 0, address,
    if operation == Op_SAVE then AccessStore
    else if operation == Op_RESTORE then AccessLoad
    else AccessAddressOnly,
    value, operation != Op_RESTORE
  );
  let request = { base_request with selector = selector, state_image = state,
         range_length = if save_range then save_size else address.width,
         range_end = if save_range then save_end
                     else address.linear_address,
         range_wrap = if save_range then
           save_size > 0 & unsigned(save_end) < unsigned(address.effective_address)
                         & save_end != 0x0000000000000000
           else base_request.range_wrap,
         range_end_at_modulus = if save_range then
           save_size > 0 & save_end == 0x0000000000000000
                         & address.effective_address != 0x0000000000000000
           else base_request.range_end_at_modulus,
         body_length = if save_range then save_size else 0 };
  if operation == Op_PTQUERY | operation == Op_VTOP then {
    let linear = value;
    let target_level = if operation == Op_PTQUERY then unsigned(selector[2 .. 0]) else 1;
    let root_level = if state.controls[0][7] == bitone then 5 else 4;
    if target_level < 1 | target_level > 5 then
      faulted(state, operation, IllegalInstruction, "invalid PTQUERY level")
    else if operation == Op_PTQUERY
            & not_bool(segment_point(address.segment_image,
                                     address.effective_address).in_bounds) then
      faulted(state, operation, AccessFault, "PTQUERY effective address outside segment")
    else if not_bool(paging_canonical(linear, state.controls[0]))
         | (operation == Op_PTQUERY & target_level == 5 & root_level == 4) then {
      var failed = advance_pc(evaluated.image, instruction);
      if destination.kind == "Rn" then failed.registers[unsigned(destination.index)] = 0x0000000000000000
      else ();
      failed.flags = 0x0;
      completed(state, failed, CommitControl, [||])
    }
    else waiting_transaction(
      state, advance_pc(evaluated.image, instruction), instruction, CommitControl,
      destination, PhasePteRead, 0, linear, bits_from_int(target_level),
      pte_read_request(state, instruction, linear,
                       state.controls[0] & paging_pfn_mask(state.controls[0]),
                       root_level, target_level, 0x0000000000000007, 0)
    )
  }
  else if save_range & not_bool(save_layout_valid(state)) then
    faulted(state, operation, InvalidControlState, "invalid CPUID SAVE-area layout")
  else if save_range & (address.effective_address & 0x0000000000000FFF)
                  != 0x0000000000000000 then
    faulted(state, operation, InvalidControlState, "SAVE/RESTORE base is not 4-KiB aligned")
  else waiting_transaction(
    state, advance_pc(evaluated.image, instruction), instruction,
    if operation == Op_SAVE | operation == Op_RESTORE then CommitMemory else CommitControl,
    destination,
    if operation == Op_RESTORE then PhaseStateRestoreHeader else phase,
    0, value, selector,
    if operation == Op_SAVE then { request with
      payload_bytes = save_image_bytes(state), body_length = save_size
    }
    else if operation == Op_RESTORE then { request with
      range_end = add_bits(address.effective_address, 0x0000000000000010),
      range_length = 16,
      range_wrap = unsigned(add_bits(address.effective_address, 0x0000000000000010))
                   < unsigned(address.effective_address),
      range_end_at_modulus = add_bits(address.effective_address, 0x0000000000000010)
                             == 0x0000000000000000
                             & address.effective_address != 0x0000000000000000,
      body_length = 16, selector = 0x0000000000000000, commit_point = false
    } else request
  )
}

function start_system_request(instruction : Decoded_instruction, state : Cpu_state)
  -> Execution_result = {
  let operation = instruction.form.operation;
  let kind = if operation == Op_CPUID then CpuidQueryRequest
    else if operation == Op_RDPMC then PerformanceCounterRequest
    else ControlTransitionRequest;
  let phase = if operation == Op_CPUID then PhaseCpuidQuery
    else if operation == Op_RDPMC then PhasePerformanceCounter
    else PhaseControlTransition;
  let selector : bits(64) = if operation == Op_CPUID then match value_named(instruction, state, "reg") {
      Some(value) => value, None() => 0x0000000000000000
    }
    else if operation == Op_RDPMC then match value_named(instruction, state, "counter_id") {
      Some(value) => value & 0x000000000000FFFF, None() => 0x0000000000000000
    }
    else match value_named(instruction, state, "cr") {
      Some(value) => value & 0x000000000000FFFF, None() => 0x0000000000000000
    };
  let value : bits(64) = if operation == Op_WRCR then match value_named(instruction, state, "src") {
      Some(item) => item, None() => 0x0000000000000000
    } else 0x0000000000000000;
  let wrcr_selector = unsigned(selector[15 .. 0]);
  let ptcr_invalid = operation == Op_WRCR & wrcr_selector == 0
    & ((value[11 .. 8] != 0x0 & value[11 .. 8] != 0x1)
       | value[6 .. 1] != 0b000000
       | (value[11 .. 8] == 0x0 & value[63 .. 48] != 0x0000)
       | (value[11 .. 8] == 0x1 & value[63 .. 56] != 0x00));
  let ascr_invalid = operation == Op_WRCR & wrcr_selector == 1
    & (value[63 .. 32] != 0x00000000 | value[15 .. 1] != 0b000000000000000);
  let entry_invalid = operation == Op_WRCR & (wrcr_selector == 256 | wrcr_selector == 272)
    & (value & 0x000000000000000F) != 0x0000000000000000;
  let urctl_invalid = operation == Op_WRCR & wrcr_selector == 269
    & ((value & 0xFFFFFFFE00000000) != 0x0000000000000000
       | value[31 .. 22] != 0b0000000000 | value[20] == bitone | value[16] == bitone
       | value[15 .. 4] != 0x000
       | not_bool(segment_image_valid(state.controls[8]))
       | not_bool(segment_image_valid(state.controls[9]))
       | not_bool(segment_image_valid(state.controls[10])));
  let ecr_invalid = operation == Op_WRCR & wrcr_selector == 2
    & ((value & 0xFFFFFFFFFFFFF07E) != 0x0000000000000000
       | (value[0] == bitone & not_bool(event_control_bank_valid(state))));
  let request = { empty_primitive_request() with
    kind = kind, role = instruction.form.family, selector = selector,
    value = if operation == Op_WRCR & wrcr_selector == 2 then
      (value & 0x0000000000000F01) | (state.controls[2] & 0x0000000000000080)
      else value,
    access = if operation == Op_WRCR then AccessStore else AccessLoad,
    commit_point = true, state_image = state };
  if operation == Op_RDPMC & selector == 0x0000000000000000 then faulted(
    state, operation, InvalidControlState, "RDPMC selector zero"
  )
  else if ptcr_invalid | ascr_invalid | entry_invalid | urctl_invalid | ecr_invalid then faulted(
    state, operation, InvalidControlState, "invalid control-register transition image"
  )
  else waiting_transaction(
    state, advance_pc(state, instruction), instruction, CommitControl,
    commit_destination_for(instruction.operands, 8), phase, 0, selector, request.value, request
  )
}

function set_overflow_flag(flags : bits(4), value : bool) -> bits(4) =
  flags[3 .. 1] @ (if value then bitone else bitzero)

function execute_lea_transaction(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) = {
  let width = operation_width(instruction);
  let evaluated = evaluate_instruction_eas(
    instruction.operands, instruction.form.operation, state, state.pc, width
  );
  match evaluation_named("src", evaluated.evaluations) {
    None() => None(),
    Some(source) => {
      let destination = commit_destination_for(instruction.operands, 8);
      if instruction.form.operation == Op_SEGLEA then {
        let point = segment_point(source.segment_image, source.effective_address);
        var updated = advance_pc(evaluated.image, instruction);
        if point.in_bounds then {
          updated = write_local_destination(updated, destination, point.linear);
          updated.flags = set_overflow_flag(updated.flags, false)
        }
        else updated.flags = set_overflow_flag(updated.flags, true);
        Some(completed(state, updated, CommitRegisters, [||]))
      }
      else {
        let updated = write_local_destination(
          advance_pc(evaluated.image, instruction), destination, source.effective_address
        );
        Some(completed(state, updated, CommitRegisters, [||]))
      }
    },
  }
}

function stack_request(kind : Primitive_request_kind, ordinal : int, state : Cpu_state,
                       address : bits(64), range_end : bits(64), access : Transaction_access,
                       value : bits(64), commit_point : bool) -> Primitive_request = {
  let point = segment_point(state.segments[2], address);
  struct {
    kind = kind, ordinal = ordinal, role = "stack", domain = "SS", segment = 2,
    segment_image = state.segments[2], width = 8, range_start = address, range_end = range_end,
    range_length = unsigned(sub_bits(range_end, address)),
    range_wrap = unsigned(range_end) < unsigned(address) & range_end != 0x0000000000000000,
    range_end_at_modulus = range_end == 0x0000000000000000
                           & address != 0x0000000000000000,
    effective_address = address, linear_address = point.linear, access = access, value = value,
    address_translation = true, commit_point = commit_point, memory_order = ordinal,
    address_type = 0, cache_policy = 0, suppress_fault = false, staged_updates = [||]
    , selector = 0x0000000000000000, expected = 0x0000000000000000,
    desired = 0x0000000000000000, auxiliary = 0x0000000000000000, body_length = 0,
    payload_bytes = [||], fp_request = empty_fp_request(),
    state_image = initial_cpu()
  }
}

function compound_stack_store(ordinal : int, state : Cpu_state, low_address : bits(64),
                              low_value : bits(64), high_value : bits(64))
  -> Primitive_request = {
  let high_address = add_bits(low_address, 0x0000000000000008);
  let point = segment_point(state.segments[2], low_address);
  { stack_request(CompoundMemoryStore, ordinal, state, low_address,
                  add_bits(low_address, 0x0000000000000010), AccessStackWrite,
                  low_value, true) with
    linear_address = point.linear, width = 16, range_length = 16,
    desired = high_value, auxiliary = high_address }
}

function pair_first_index(pair_id : int) -> int = pair_id * 2

function push_source_values(instruction : Decoded_instruction, state : Cpu_state)
  -> (bits(64), bits(64)) =
  if instruction.form.operation == Op_PUSHP | instruction.form.operation == Op_FPUSHP
  then match operand_named(instruction, "pair_id") {
    Some(pair) => {
      let first = pair_first_index(unsigned(pair.value[2 .. 0]));
      let first_index = unsigned(get_slice_int(4, first, 0));
      let second_index = unsigned(get_slice_int(4, first + 1, 0));
      if instruction.form.operation == Op_FPUSHP then
        (state.floating_registers[first_index], state.floating_registers[second_index])
      else (image_register(state, first), image_register(state, first + 1))
    },
    None() => (0x0000000000000000, 0x0000000000000000),
  }
  else match operand_named(instruction, "reg") {
    Some(reg) =>
      if reg.fixed_identity == "CS" then (state.segments[0], 0x0000000000000000)
      else if reg.type_name == "SREG" then
        (image_segment(state, unsigned(reg.value[2 .. 0]) + 1), 0x0000000000000000)
      else (image_register(state, unsigned(reg.value[3 .. 0])), 0x0000000000000000),
    None() => (0x0000000000000000, 0x0000000000000000),
  }

function start_stack_transaction(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) = {
  let operation = instruction.form.operation;
  let pair = operation == Op_PUSHP | operation == Op_POPP
           | operation == Op_FPUSHP | operation == Op_FPOPP;
  let push = operation == Op_PUSH | operation == Op_PUSHP | operation == Op_FPUSHP;
  let pop = operation == Op_POP | operation == Op_POPP | operation == Op_FPOPP;
  if not_bool(push | pop) then None()
  else {
    let bytes = if pair then 16 else 8;
    let start = if push then sub_bits(state.sp, get_slice_int(64, bytes, 0)) else state.sp;
    let end_address = if push then state.sp else add_bits(state.sp, get_slice_int(64, bytes, 0));
    let (first, second) = push_source_values(instruction, state);
    var after = advance_pc(state, instruction);
    after.sp = if push then start else end_address;
    Some(waiting_transaction(
      state, after, instruction, CommitMemory,
      commit_destination_for(instruction.operands, 8), PhaseStackRange, 0, first, second,
      stack_request(StackRange, 0, state, start, end_address,
                    if push then AccessStackWrite else AccessStackRead,
                    0x0000000000000000, false)
    ))
  }
}

function target_probe_request(ordinal : int, segment_image : bits(64), target : bits(64))
  -> Primitive_request = {
  let point = segment_point(segment_image, target);
  struct {
    kind = TranslationExecuteProbe, ordinal = ordinal, role = "control_target", domain = "CS",
    segment = 0, segment_image = segment_image, width = 1, range_start = target,
    range_end = add_bits(target, 0x0000000000000001), effective_address = target,
    range_length = 1, range_wrap = false,
    range_end_at_modulus = target == 0xFFFFFFFFFFFFFFFF,
    linear_address = point.linear, access = AccessExecute, value = 0x0000000000000000,
    address_translation = true, commit_point = false, memory_order = ordinal,
    address_type = 0, cache_policy = 0, suppress_fault = false, staged_updates = [||]
    , selector = 0x0000000000000000, expected = 0x0000000000000000,
    desired = 0x0000000000000000, auxiliary = 0x0000000000000000, body_length = 0,
    payload_bytes = [||], fp_request = empty_fp_request(),
    state_image = initial_cpu()
  }
}

function start_control_transaction(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) = {
  let operation = instruction.form.operation;
  let far_jump = operation == Op_LCALL | operation == Op_LJMP;
  let proposed_cs = if far_jump then match value_named(instruction, state, "new_cs") {
    Some(value) => value, None() => state.segments[0]
  } else state.segments[0];
  if operation == Op_RET | operation == Op_LRET then {
    let bytes = if operation == Op_LRET then 16 else 8;
    let end_address = add_bits(state.sp, get_slice_int(64, bytes, 0));
    var after = state; after.sp = end_address;
    Some(waiting_transaction(
      state, after, instruction, CommitControl, empty_destination(), PhaseStackRange, 0,
      0x0000000000000000, 0x0000000000000000,
      stack_request(StackRange, 0, state, state.sp, end_address, AccessStackRead,
                    0x0000000000000000, false)
    ))
  }
  else {
    let evaluated = evaluate_instruction_eas(
      instruction.operands, instruction.form.operation, state, state.pc, 8
    );
    match evaluation_named("target", evaluated.evaluations) {
      Some(target_ea) =>
        if target_ea.kind == "memory" then Some(waiting_transaction(
          state, evaluated.image, instruction, CommitControl, empty_destination(), PhaseTargetRead, 0,
          0x0000000000000000, 0x0000000000000000,
          request_for_evaluation(MemoryRead, 0, target_ea, AccessLoad,
                                 0x0000000000000000, false)
        ))
        else if far_jump & not_bool(segment_image_valid(proposed_cs)) then Some(faulted(
          state, operation, InvalidControlState, "invalid target code segment"
        ))
        else {
          let cs_image = proposed_cs;
          Some(waiting_transaction(
            state, evaluated.image, instruction, CommitControl, empty_destination(),
            PhaseTargetExecuteProbe, 0, target_ea.value, cs_image,
            target_probe_request(0, cs_image, target_ea.value)
          ))
        },
      None() => match control_target_local(instruction, state) {
        Some(target) =>
          if far_jump & not_bool(segment_image_valid(proposed_cs)) then Some(faulted(
            state, operation, InvalidControlState, "invalid target code segment"
          ))
          else Some(waiting_transaction(
            state, state, instruction, CommitControl, empty_destination(), PhaseTargetExecuteProbe, 0,
            target, proposed_cs, target_probe_request(0, proposed_cs, target)
          )),
        None() => None(),
      },
    }
  }
}

