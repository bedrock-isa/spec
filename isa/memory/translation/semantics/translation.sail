function paging_format_canonical(linear : bits(64), ptcr : bits(64)) -> bool =
  if ptcr[3 .. 1] == 0b010 then
    linear[63 .. 45] == (if linear[44] == bitone
                         then 0b1111111111111111111
                         else 0b0000000000000000000)
  else if ptcr[3 .. 1] == 0b011 then
    linear[63 .. 56] == (if linear[55] == bitone then 0xFF else 0x00)
  else false

function paging_canonical(linear : bits(64), ptcr : bits(64)) -> bool =
  ptcr[0] == bitzero | paging_format_canonical(linear, ptcr)

function paging_root_level(ptcr : bits(64)) -> option(int) =
  if ptcr[3 .. 1] == 0b010 then Some(3)
  else if ptcr[3 .. 1] == 0b011 then Some(4)
  else None()

function paging_leaf_pfn_mask(ptcr : bits(64)) -> bits(64) =
  0x00FFFFFFFFFFC000

function paging_next_table_mask(ptcr : bits(64)) -> bits(64) =
  0x00FFFFFFFFFFF000

function physical_address_fits_pabits(address : bits(64)) -> bool =
  address[63 .. 56] == 0x00

function paging_level_index(linear : bits(64), level : int) -> bits(64) = match level {
  4 => sail_shiftright(linear, 45) & 0x00000000000007FF,
  3 => sail_shiftright(linear, 34) & 0x00000000000007FF,
  2 => sail_shiftright(linear, 23) & 0x00000000000007FF,
  _ => sail_shiftright(linear, 14) & 0x00000000000001FF,
}

function paging_leaf_offset_mask(level : int) -> bits(64) = match level {
  4 => 0x00001FFFFFFFFFFF,
  3 => 0x00000003FFFFFFFF,
  2 => 0x00000000007FFFFF,
  _ => 0x0000000000003FFF,
}

function paging_leaf_alignment_mask(level : int) -> bits(64) =
  paging_leaf_offset_mask(level) & 0x00FFFFFFFFFFC000

function pte_structurally_valid(pte : bits(64), level : int) -> bool =
  if pte[0] == bitzero then false
  else if (pte & 0xFC00000000000000) != 0x0000000000000000 then false
  else if pte[1] == bitone then
    level > 1 & (pte & 0x0000000000000F40) == 0x0000000000000000
      & (level == 2 | (pte & 0x0000000000003000) == 0x0000000000000000)
      & pte[4 .. 2] != 0b000
  else (pte & 0x0000000000003800) == 0x0000000000000000
    & (pte & paging_leaf_alignment_mask(level)) == 0x0000000000000000

function pte_read_request(state : Cpu_state, ptquery : bool,
                          linear : bits(64), table_base : bits(64), level : int,
                          target_level : int, ordinal : int)
  -> Primitive_request = {
  let address = add_bits(table_base, sail_shiftleft(paging_level_index(linear, level), 3));
  { empty_primitive_request() with
    kind = PhysicalPteRead, ordinal = ordinal, role = if ptquery
      then RequestRolePtqueryPte else RequestRoleVtopPte,
    domain = RequestDomainPhysicalPageTable, width = 8, range_start = address,
    range_end = add_bits(address, 0x0000000000000008), range_length = 8,
    effective_address = address, linear_address = address, access = AccessLoad,
    address_translation = false, commit_point = false, value = linear,
    selector = bits_from_int(level), expected = bits_from_int(target_level),
    auxiliary = 0x0000000000000000 }
}

function query_result(previous : Execution_result, value : bits(64), valid : bool)
  -> Execution_result = {
  var updated = pending_after(previous);
  let destination = previous.pending.destination;
  if destination.kind == DestinationRn then
    updated.registers[unsigned(destination.index)] = value
  else ();
  updated.flags = if valid then 0x1 else 0x0;
  completed(previous.state, updated, CommitControl, [||])
}

function start_tlb_context_transaction(tlb_operation : Tlb_context_uop_operation,
                                       instruction : Decoded_instruction, state : Cpu_state)
  -> Execution_result = {
  let operation = instruction.form.operation;
  let ptquery = tlb_operation == TlbPageTableQuery;
  let vtop = tlb_operation == TlbVirtualToPhysical;
  let swpt = tlb_operation == TlbSwitchPageTable | tlb_operation == TlbSwitchPageTableAsid;
  let swpta = tlb_operation == TlbSwitchPageTableAsid;
  let evaluated = evaluate_instruction_eas(
    instruction.operands, state, state.pc, 8
  );
  let address : Ea_evaluation = match first_evaluation(evaluated.evaluations) {
    Some(value) => value, None() => struct {
      operand_name = Operand_address, kind = EaKind_memory, role = None(), domain = None(), segment = 0,
      segment_image = 0x0000000000000000, width = 8,
      effective_address = 0x0000000000000000, linear_address = 0x0000000000000000,
      value = 0x0000000000000000, staged_updates = [||]
    }
  };
  let selector = if tlb_operation == TlbInvalidateAsid then match value_named(instruction, state, Operand_asid) {
      Some(value) => value & 0x000000000000FFFF, None() => 0x0000000000000000
    }
    else if ptquery then match value_named(instruction, state, Operand_level) {
      Some(value) => value & 0x0000000000000007, None() => 0x0000000000000000
    }
    else if swpta then match value_named(instruction, state, Operand_asid) {
      Some(value) => value & 0x000000000000FFFF, None() => 0x0000000000000000
    }
    else 0x0000000000000000;
  let value = if vtop then match value_named(instruction, state, Operand_virt) {
      Some(item) => item, None() => 0x0000000000000000
    }
    else if swpt then
      match value_named(instruction, state, Operand_new_ptcr) {
        Some(item) => item, None() => 0x0000000000000000
      }
    else address.linear_address;
  let kind = if tlb_operation == TlbInvalidateAsid | tlb_operation == TlbInvalidatePage
             | tlb_operation == TlbInvalidateAll
    then TlbInvalidateRequest
    else if ptquery | vtop then PhysicalPteRead
    else ContextSwitchRequest;
  let phase = if kind == TlbInvalidateRequest then PhaseTlbOperation
    else if kind == PhysicalPteRead then PhasePteRead
    else PhaseContextSwitch;
  let install_fault = if swpt then ptcr_image_fault(value) else None();
  let destination = commit_destination_for(instruction.operands, 8);
  let base_request = request_for_evaluation(
    kind, 0, address, AccessAddressOnly, value, true
  );
  let request = { base_request with selector = selector };
  if ptquery | vtop then {
    let linear = value;
    let target_level = if ptquery then unsigned(selector[2 .. 0]) else 1;
    let ptcr = control_register_value(state, ControlRegister_BASE_PTCR);
    if target_level < 1 | target_level > 4 then
      faulted(state, operation, InvalidControlSelectorFault, "invalid PTQUERY level")
    else if ptquery
            & not_bool(segment_point(address.segment_image,
                                     address.effective_address).in_bounds) then
      faulted(state, operation, AccessFault, "PTQUERY effective address outside segment")
    else if vtop & ptcr[0] == bitzero then {
      var direct = advance_pc(evaluated.image, instruction);
      let valid = physical_address_fits_pabits(linear);
      if destination.kind == DestinationRn then
        direct.registers[unsigned(destination.index)] =
          if valid then linear else 0x0000000000000000
      else ();
      direct.flags = if valid then 0x1 else 0x0;
      completed(state, direct, CommitControl, [||])
    }
    else match paging_root_level(ptcr) {
      None() => {
        var failed = advance_pc(evaluated.image, instruction);
        if destination.kind == DestinationRn then failed.registers[unsigned(destination.index)] = 0x0000000000000000
        else ();
        failed.flags = 0x0;
        completed(state, failed, CommitControl, [||])
      },
      Some(root_level) =>
        if not_bool(paging_format_canonical(linear, ptcr))
           | (ptquery & target_level > root_level) then {
          var failed = advance_pc(evaluated.image, instruction);
          if destination.kind == DestinationRn then failed.registers[unsigned(destination.index)] = 0x0000000000000000
          else ();
          failed.flags = 0x0;
          completed(state, failed, CommitControl, [||])
        }
        else waiting_transaction(TransactionSystem,
          state, advance_pc(evaluated.image, instruction), instruction, CommitControl,
          destination, PhasePteRead, 0, linear, bits_from_int(target_level),
          pte_read_request(state, ptquery, linear,
                           ptcr & paging_leaf_pfn_mask(ptcr),
                           root_level, target_level, 0)
        ),
    }
  }
  else match install_fault {
    Some(kind) => faulted(state, operation, kind, "invalid PTCR image"),
    None() => waiting_transaction(TransactionSystem,
      state, advance_pc(evaluated.image, instruction), instruction,
      CommitControl,
      destination,
      phase,
      0, value, selector,
      { request with auxiliary = if swpta then 0x0000000000000001 else request.auxiliary }
    ),
  }
}
