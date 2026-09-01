function debug_trigger_slot_get(
  slots : list(Debug_trigger_slot), index : int
) -> option(Debug_trigger_slot) = match slots {
  [||] => None(),
  slot :: tail => if index <= 0 then Some(slot)
                  else debug_trigger_slot_get(tail, index - 1),
}

function debug_trigger_slot_set(
  slots : list(Debug_trigger_slot), index : int, replacement : Debug_trigger_slot
) -> list(Debug_trigger_slot) = match slots {
  [||] => [||],
  slot :: tail => if index <= 0 then replacement :: tail
                  else slot :: debug_trigger_slot_set(tail, index - 1, replacement),
}

function debug_trigger_selected_slot(file : Debug_trigger_file) -> int =
  unsigned(file.selector[15 .. 0])

function debug_trigger_selected_bank(file : Debug_trigger_file) -> int =
  unsigned(file.selector[17 .. 16])

function debug_trigger_selection_valid(file : Debug_trigger_file) -> bool =
  debug_trigger_selected_slot(file) >= 0
  & debug_trigger_selected_slot(file) < file.slot_count
  & debug_trigger_selected_bank(file) < 3

function debug_trigger_selected_value(file : Debug_trigger_file) -> bits(64) =
  match debug_trigger_slot_get(file.slots, debug_trigger_selected_slot(file)) {
    None() => 0x0000000000000000,
    Some(slot) => {
      let bank = debug_trigger_selected_bank(file);
      if bank == 0 then slot.settings
      else if bank == 1 then slot.low
      else if bank == 2 then slot.high
      else 0x0000000000000000
    },
  }

function debug_trigger_slot_configuration_valid(slot : Debug_trigger_slot) -> bool =
  slot.settings[0] == bitone
  & slot.settings[3 .. 1] != 0b000
  & slot.settings[5 .. 4] != 0b00
  & unsigned(slot.low) < unsigned(slot.high)

function debug_trigger_selected_write_fault(
  file : Debug_trigger_file, source : bits(64)
) -> option(Fault_kind) =
  if not_bool(debug_trigger_selection_valid(file)) then
    Some(InvalidControlSelectorFault)
  else match debug_trigger_slot_get(file.slots, debug_trigger_selected_slot(file)) {
    None() => Some(InvalidControlSelectorFault),
    Some(slot) => {
      let bank = debug_trigger_selected_bank(file);
      let active = slot.settings[0] == bitone;
      if bank == 0 & (source & 0xFFFFFFFFFFFFFFC0) != 0x0000000000000000 then
        Some(ReservedControlBitsFault)
      else if active & (bank != 0
                        | source != (slot.settings & 0xFFFFFFFFFFFFFFFE)) then
        Some(InvalidControlTransitionFault)
      else if not_bool(active) & bank == 0 & source[0] == bitone then {
        let candidate = { slot with settings = source };
        if debug_trigger_slot_configuration_valid(candidate) then None()
        else Some(InvalidControlImageFault)
      }
      else None()
    },
  }

function debug_trigger_file_with_selected_value(
  file : Debug_trigger_file, source : bits(64)
) -> Debug_trigger_file =
  match debug_trigger_slot_get(file.slots, debug_trigger_selected_slot(file)) {
    None() => file,
    Some(slot) => {
      let bank = debug_trigger_selected_bank(file);
      let replacement = if bank == 0 then { slot with settings = source }
        else if bank == 1 then { slot with low = source }
        else if bank == 2 then { slot with high = source }
        else slot;
      { file with slots = debug_trigger_slot_set(
          file.slots, debug_trigger_selected_slot(file), replacement) }
    },
  }

function debug_trigger_request_user_domain(
  state : Cpu_state, request : Primitive_request
) -> bool =
  request.domain == RequestDomainUser
  | ((request.domain == RequestDomainCurrent | request.domain == RequestDomainStack)
     & not_bool(state.supervisor))

function debug_trigger_domain_matches(settings : bits(64), user_domain : bool) -> bool =
  if user_domain then settings[4] == bitone else settings[5] == bitone

function debug_trigger_request_read(request : Primitive_request) -> bool =
  request.kind == Read

function debug_trigger_request_write(request : Primitive_request) -> bool =
  request.kind == Write

function debug_trigger_request_atomic(request : Primitive_request) -> bool =
  request.kind == Atomic

function debug_trigger_memory_request(request : Primitive_request) -> bool =
  debug_trigger_request_read(request) | debug_trigger_request_write(request)
  | debug_trigger_request_atomic(request)

function debug_trigger_access_matches(
  settings : bits(64), request : Primitive_request
) -> bool =
  if debug_trigger_request_atomic(request) then
    settings[2] == bitone | settings[3] == bitone
  else if debug_trigger_request_read(request) then settings[2] == bitone
  else if debug_trigger_request_write(request) then settings[3] == bitone
  else false

function debug_access_range_overlap(
  accessed : Memory_access_range, low : bits(64), high : bits(64)
) -> bool =
  accessed.width > 0
  & unsigned(accessed.effective_address) < unsigned(high)
  & unsigned(low) < unsigned(accessed.effective_address) + accessed.width

function first_overlapping_debug_range(
  ranges : list(Memory_access_range), low : bits(64), high : bits(64)
) -> option(Memory_access_range) = match ranges {
  [||] => None(),
  accessed :: tail => if debug_access_range_overlap(accessed, low, high)
                      then Some(accessed)
                      else first_overlapping_debug_range(tail, low, high),
}

function debug_trigger_find_memory(
  slots : list(Debug_trigger_slot), index : int, user_domain : bool,
  request : Primitive_request
) -> option(Debug_trigger_match) = match slots {
  [||] => None(),
  slot :: tail => if slot.settings[0] == bitone
                     & debug_trigger_domain_matches(slot.settings, user_domain)
                     & debug_trigger_access_matches(slot.settings, request) then
    match first_overlapping_debug_range(request.memory_ranges, slot.low, slot.high) {
      Some(accessed) => Some(struct { slot = index, accessed = accessed }),
      None() => debug_trigger_find_memory(tail, index + 1, user_domain, request),
    }
  else debug_trigger_find_memory(tail, index + 1, user_domain, request),
}

function debug_trigger_memory_match(
  state : Cpu_state, request : Primitive_request
) -> option(Debug_trigger_match) =
  if state.status[3] == bitone | not_bool(debug_trigger_memory_request(request)) then None()
  else debug_trigger_find_memory(
    state.controls.debug_trigger_file.slots, 0,
    debug_trigger_request_user_domain(state, request), request)

function debug_trigger_prepare_request(
  state : Cpu_state, request : Primitive_request
) -> Primitive_request =
  if request.debug_validated | request.debug_validation then request
  else match debug_trigger_memory_match(state, request) {
    Some(_) => { request with debug_validation = true },
    None() => request,
  }

function debug_trigger_validated_request(
  request : Primitive_request, physical_address : bits(64)
) -> Primitive_request =
  { request with debug_validation = false, debug_validated = true,
    physical_address = physical_address, address_translation = false }

function debug_trigger_memory_stop(
  state : Cpu_state, request : Primitive_request, access_class : Memory_access_class
) -> option(Debug_stop) = match debug_trigger_memory_match(state, request) {
  None() => None(),
  Some(winner) => Some(struct {
    kind = if debug_trigger_request_atomic(request) then DebugStopAtomicMemory
           else if debug_trigger_request_write(request) then DebugStopMemoryWrite
           else DebugStopMemoryRead,
    slot = winner.slot,
    operand = request.operand,
    access_size = winner.accessed.width,
    effective_address = winner.accessed.effective_address,
    linear_address = winner.accessed.linear_address,
    linear_valid = true,
    user_domain = debug_trigger_request_user_domain(state, request),
    access_class = access_class,
  }),
}

function debug_trigger_find_execution(
  slots : list(Debug_trigger_slot), index : int, pc : bits(64), user_domain : bool
) -> option(int) = match slots {
  [||] => None(),
  slot :: tail => if slot.settings[0] == bitone & slot.settings[1] == bitone
                     & debug_trigger_domain_matches(slot.settings, user_domain)
                     & unsigned(slot.low) <= unsigned(pc)
                     & unsigned(pc) < unsigned(slot.high)
                  then Some(index)
                  else debug_trigger_find_execution(tail, index + 1, pc, user_domain),
}

function debug_trigger_execution_stop(state : Cpu_state) -> option(Debug_stop) =
  if state.status[3] == bitone then None()
  else match debug_trigger_find_execution(
    state.controls.debug_trigger_file.slots, 0, state.pc, not_bool(state.supervisor)) {
    None() => None(),
    Some(slot) => Some(struct {
      kind = DebugStopExecution,
      slot = slot,
      operand = 255,
      access_size = 0,
      effective_address = state.pc,
      linear_address = 0x0000000000000000,
      linear_valid = false,
      user_domain = not_bool(state.supervisor),
      access_class = NormalAccess,
    }),
  }
