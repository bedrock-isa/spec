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

// Legacy stack dispatch removed; typed stack uops own stack assembly.
