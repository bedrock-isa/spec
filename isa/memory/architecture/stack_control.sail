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

