function stack_request(kind : Primitive_request_kind, ordinal : int, state : Cpu_state,
                       address : bits(64), range_end : bits(64), access : Transaction_access,
                       value : bits(64), commit_point : bool) -> Primitive_request = {
  let point = segment_point(state.segments[2], address);
  struct {
    kind = kind, ordinal = ordinal, role = RequestRoleStack, domain = RequestDomainStack, segment = 2,
    segment_image = state.segments[2], width = 8, range_start = address, range_end = range_end,
    range_length = unsigned(sub_bits(range_end, address)),
    range_wrap = unsigned(range_end) < unsigned(address) & range_end != 0x0000000000000000,
    range_end_at_modulus = range_end == 0x0000000000000000
                           & address != 0x0000000000000000,
    effective_address = address, linear_address = point.linear, access = access, value = value,
    address_translation = true, commit_point = commit_point, memory_order = ordinal,
    cache_policy = 0, suppress_fault = false, staged_updates = [||]
    , selector = 0x0000000000000000, expected = 0x0000000000000000,
    desired = 0x0000000000000000, auxiliary = 0x0000000000000000, body_length = 0,
    payload_bytes = [||]
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
  then match operand_named(instruction, Operand_pair_id) {
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
  else match operand_named(instruction, Operand_reg) {
    Some(reg) =>
      if reg.operand_type == OperandType_CS then (state.segments[0], 0x0000000000000000)
      else if reg.operand_type == OperandType_SREG then
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
