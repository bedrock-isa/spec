function paging_canonical(linear : bits(64), ptcr : bits(64)) -> bool =
  if ptcr[7] == bitone then
    linear[63 .. 57] == (if linear[56] == bitone then 0b1111111 else 0b0000000)
  else linear[63 .. 48] == (if linear[47] == bitone then 0xFFFF else 0x0000)

function paging_pfn_mask(ptcr : bits(64)) -> bits(64) =
  0x00FFFFFFFFFFF000

function physical_address_fits_pabits(address : bits(64)) -> bool =
  address[63 .. 56] == 0x00

function paging_level_index(linear : bits(64), level : int) -> bits(64) = match level {
  5 => sail_shiftright(linear, 48) & 0x00000000000001FF,
  4 => sail_shiftright(linear, 39) & 0x00000000000001FF,
  3 => sail_shiftright(linear, 30) & 0x00000000000001FF,
  2 => sail_shiftright(linear, 21) & 0x00000000000001FF,
  _ => sail_shiftright(linear, 12) & 0x00000000000001FF,
}

function paging_leaf_offset_mask(level : int) -> bits(64) = match level {
  5 => 0x0000FFFFFFFFFFFF,
  4 => 0x0000007FFFFFFFFF,
  3 => 0x000000003FFFFFFF,
  2 => 0x00000000001FFFFF,
  _ => 0x0000000000000FFF,
}

function paging_leaf_alignment_mask(level : int) -> bits(64) =
  paging_leaf_offset_mask(level) & 0xFFFFFFFFFFFFF000

function pte_structurally_valid(pte : bits(64), level : int) -> bool =
  if pte[0] == bitzero then false
  else if (pte & 0xFC00000000000000) != 0x0000000000000000 then false
  else if pte[1] == bitone then
    level > 1 & (pte & 0x0000000000000F40) == 0x0000000000000000
      & pte[4 .. 2] != 0b000
  else (pte & 0x0000000000000800) == 0x0000000000000000
    & (pte & paging_leaf_alignment_mask(level)) == 0x0000000000000000

function pte_read_request(state : Cpu_state, instruction : Decoded_instruction,
                          linear : bits(64), table_base : bits(64), level : int,
                          target_level : int, ordinal : int)
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
    auxiliary = 0x0000000000000000, state_image = state }
}

function query_result(previous : Execution_result, value : bits(64), valid : bool)
  -> Execution_result = {
  var updated = previous.pending.after;
  let destination = previous.pending.destination;
  if destination.kind == "Rn" then
    updated.registers[unsigned(destination.index)] = value
  else ();
  updated.flags = if valid then 0x1 else 0x0;
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
    else if operation == Op_VTOP & state.controls[0][0] == bitzero then {
      var direct = advance_pc(evaluated.image, instruction);
      let valid = physical_address_fits_pabits(linear);
      if destination.kind == "Rn" then
        direct.registers[unsigned(destination.index)] =
          if valid then linear else 0x0000000000000000
      else ();
      direct.flags = if valid then 0x1 else 0x0;
      completed(state, direct, CommitControl, [||])
    }
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
                       root_level, target_level, 0)
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
