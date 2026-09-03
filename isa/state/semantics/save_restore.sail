function zero_byte_count(count : int) -> list(bits(8)) =
  if count <= 0 then [||] else 0x00 :: zero_byte_count(count - 1)

function byte_range_zero(bytes : list(bits(8)), offset : int, count : int) -> bool =
  if count <= 0 then true
  else match bytes {
    [||] => false,
    head :: tail => if offset > 0 then byte_range_zero(tail, offset - 1, count)
                    else head == 0x00 & byte_range_zero(tail, 0, count - 1),
  }

function le64_bytes(value : bits(64)) -> list(bits(8)) = [|
  value[7 .. 0], value[15 .. 8], value[23 .. 16], value[31 .. 24],
  value[39 .. 32], value[47 .. 40], value[55 .. 48], value[63 .. 56]
|]

function serialize_register_file(registers : Registers, index : int) -> list(bits(8)) =
  if index >= 16 then [||]
  else append_bytes(le64_bytes(registers[unsigned(get_slice_int(4, index, 0))]),
                    serialize_register_file(registers, index + 1))

function serialize_saved_gs(segments : Segment_registers, index : int) -> list(bits(8)) =
  if index >= 6 then [||]
  else append_bytes(le64_bytes(image_segment({ initial_cpu() with segments = segments }, index + 3)),
                    serialize_saved_gs(segments, index + 1))

function restored_event_state_valid(state : Cpu_state, saved_status : bits(64),
                                    saved_dfa : bool) -> bool = {
  let privileged = saved_status[4] == bitone;
  let active = saved_status[0] == bitone;
  let depth = status_event_depth(saved_status);
  let user_origin = status_user_origin(saved_status);
  if saved_status[15 .. 11] != 0b00000 | (saved_dfa & not_bool(active)) then false
  else if privileged & active then
    depth > 0 & (not_bool(user_origin)
      | control_register_value(state, ControlRegister_BASE_UCTL)[32] == bitone)
  else if privileged then depth == 0 & not_bool(user_origin) & not_bool(saved_dfa)
  else not_bool(active) & depth == 0 & not_bool(user_origin) & not_bool(saved_dfa)
}

function state_record_range(address : Uop_value, offset : int, width : int)
  -> Memory_access_range = struct {
  effective_address = add_bits(address.effective_address, bits_from_int(offset)),
  linear_address = add_bits(address.linear_address, bits_from_int(offset)),
  width = width,
  buffer_offset = offset,
}

function state_record_buffer_range(address : Uop_value, offset : int, width : int,
                                   buffer_offset : int) -> Memory_access_range = struct {
  effective_address = add_bits(address.effective_address, bits_from_int(offset)),
  linear_address = add_bits(address.linear_address, bits_from_int(offset)),
  width = width,
  buffer_offset = buffer_offset,
}

function state_record_request(address : Uop_value, kind : Primitive_request_kind,
                              size : int, access : Transaction_access,
                              ranges : list(Memory_access_range), body_length : int,
                              payload : list(bits(8)), commit : bool)
  -> Primitive_request = {
  let request = uop_memory_request_make(
    kind, address, size, access, 0x0000000000000000, commit
  );
  { request with
    range_end = add_bits(address.effective_address, bits_from_int(size)),
    range_length = size,
    range_wrap = size > 0
      & unsigned(add_bits(address.effective_address, bits_from_int(size)))
        < unsigned(address.effective_address)
      & add_bits(address.effective_address, bits_from_int(size)) != 0x0000000000000000,
    range_end_at_modulus = size > 0
      & add_bits(address.effective_address, bits_from_int(size)) == 0x0000000000000000
      & address.effective_address != 0x0000000000000000,
    memory_ranges = ranges,
    body_length = body_length,
    payload_bytes = payload,
  }
}

union clause Uop_kind = UopStateRecordAddress : unit

function clause execute_uop(UopStateRecordAddress(), uop, values, instruction,
                            before, speculative) =
  match (uop_location_read(uop.source0, before, values),
         uop_location_read(uop.source1, before, values)) {
    (Some(raw), Some(alignment)) => {
      let last = add_bits(raw, bits_from_int(uop.width - 1));
      let start_point = segment_point(before.segments[1], raw);
      let last_point = segment_point(before.segments[1], last);
      if alignment == 0x0000000000000000
         | tmod_int(unsigned(raw), unsigned(alignment)) != 0 then
        uop_step_fault(faulted(before, instruction.form.operation,
          InvalidControlState, "state-record address is misaligned"))
      else if uop.width <= 0 | unsigned(last) < unsigned(raw)
              | not_bool(start_point.in_bounds) | not_bool(last_point.in_bounds) then
        uop_step_fault(faulted(before, instruction.form.operation,
          AccessFault, "state-record range is outside the default data segment"))
      else {
        let address : Uop_value = {
          uop_value_empty() with
          value = raw,
          address = true,
          segment = 1,
          segment_image = before.segments[1],
          effective_address = raw,
          linear_address = start_point.linear,
          domain = RequestDomainCurrent,
        };
        uop_step_continue(speculative,
          uop_value_set(values, uop.destination.index, address))
      }
    },
    _ => uop_step_fault(faulted(before, instruction.form.operation,
      InvalidControlState, "state-record address is unavailable")),
  }

function base_user_record_bytes(state : Cpu_state) -> list(bits(8)) =
  append_bytes(
    serialize_register_file(state.registers, 0),
    append_bytes(serialize_saved_gs(state.segments, 0),
                 le64_bytes(sail_zero_extend(state.flags, 64)))
  )

function restore_base_registers(bytes : list(bits(8)), index : int,
                                registers : Registers) -> option(Registers) =
  if index >= 16 then Some(registers)
  else match read_le_bits(bytes, index * 8, 64) {
    None() => None(),
    Some(value) => {
      var updated = registers;
      updated[unsigned(get_slice_int(4, index, 0))] = value;
      restore_base_registers(bytes, index + 1, updated)
    },
  }

function restore_base_gs(bytes : list(bits(8)), index : int,
                         segments : Segment_registers) -> option(Segment_registers) =
  if index >= 6 then Some(segments)
  else match read_le_bits(bytes, 128 + index * 8, 64) {
    None() => None(),
    Some(value) => if not_bool(segment_image_valid(value)) then None()
    else {
      var updated = segments;
      if index == 0 then updated[3] = value
      else if index == 1 then updated[4] = value
      else if index == 2 then updated[5] = value
      else if index == 3 then updated[6] = value
      else if index == 4 then updated[7] = value
      else updated[8] = value;
      restore_base_gs(bytes, index + 1, updated)
    },
  }

function base_supervisor_record_bytes(state : Cpu_state) -> list(bits(8)) =
  le64_bytes((state.status & 0x000000000000FFFF)
    | (if state.current_dfa then 0x0000000000010000 else 0x0000000000000000))

union clause Uop_kind = UopBaseUserSave : unit
union clause Uop_kind = UopBaseUserRestoreRead : unit
union clause Uop_kind = UopBaseUserRestoreCommit : unit
union clause Uop_kind = UopBaseSupervisorSave : unit
union clause Uop_kind = UopBaseSupervisorRestoreRead : unit
union clause Uop_kind = UopBaseSupervisorRestoreCommit : unit

function base_record_save_step(uop : Uop, values : list(Uop_value),
                               instruction : Decoded_instruction, before : Cpu_state,
                               payload : list(bits(8))) -> Uop_step =
  match uop_value_get(values, uop.source0.index) {
    Some(address) => uop_step_wait(0 - 1,
      state_record_request(address, Write, uop.width, AccessStore,
        [|state_record_range(address, 0, uop.width)|], 0, payload, true),
      0x0000000000000000),
    None() => uop_step_fault(faulted(before, instruction.form.operation,
      InvalidControlState, "state-record address was not captured")),
  }

function base_record_read_step(uop : Uop, values : list(Uop_value),
                               instruction : Decoded_instruction, before : Cpu_state)
  -> Uop_step =
  match uop_value_get(values, uop.source0.index) {
    Some(address) => uop_step_wait(uop.destination.index,
      state_record_request(address, Read, uop.width, AccessLoad,
        [|state_record_range(address, 0, uop.width)|], uop.width, [||], false),
      0x0000000000000000),
    None() => uop_step_fault(faulted(before, instruction.form.operation,
      InvalidControlState, "state-record address was not captured")),
  }

function clause execute_uop(UopBaseUserSave(), uop, values, instruction,
                            before, _) =
  base_record_save_step(uop, values, instruction, before,
                        base_user_record_bytes(before))

function clause execute_uop(UopBaseSupervisorSave(), uop, values, instruction,
                            before, _) =
  base_record_save_step(uop, values, instruction, before,
                        base_supervisor_record_bytes(before))

function clause execute_uop(UopBaseUserRestoreRead(), uop, values, instruction,
                            before, _) =
  base_record_read_step(uop, values, instruction, before)

function clause execute_uop(UopBaseSupervisorRestoreRead(), uop, values,
                            instruction, before, _) =
  base_record_read_step(uop, values, instruction, before)

function clause execute_uop(UopBaseUserRestoreCommit(), uop, values, instruction,
                            before, speculative) =
  match uop_value_get(values, uop.source0.index) {
    None() => uop_step_fault(faulted(before, instruction.form.operation,
      InvalidControlState, "base user-state record is unavailable")),
    Some(record) => match (
      restore_base_registers(record.body_bytes, 0, speculative.registers),
      restore_base_gs(record.body_bytes, 0, speculative.segments),
      read_le_bits(record.body_bytes, 176, 64)
    ) {
      (Some(registers), Some(segments), Some(flags)) =>
        if byte_count(record.body_bytes) != 184
           | (flags & 0xFFFFFFFFFFFFFFF0) != 0x0000000000000000 then
          uop_step_fault(faulted(before, instruction.form.operation,
            InvalidControlState, "invalid base user-state record"))
        else {
          var updated = speculative;
          updated.registers = registers;
          updated.segments = segments;
          updated.flags = flags[3 .. 0];
          uop_step_continue(updated, values)
        },
      _ => uop_step_fault(faulted(before, instruction.form.operation,
        InvalidControlState, "invalid base user-state record")),
    },
  }

function clause execute_uop(UopBaseSupervisorRestoreCommit(), uop, values,
                            instruction, before, speculative) =
  match uop_value_get(values, uop.source0.index) {
    None() => uop_step_fault(faulted(before, instruction.form.operation,
      InvalidControlState, "base supervisor-state record is unavailable")),
    Some(record) => match read_le_bits(record.body_bytes, 0, 64) {
      None() => uop_step_fault(faulted(before, instruction.form.operation,
        InvalidControlState, "invalid base supervisor-state record")),
      Some(image) => {
        let saved_status = image & 0x000000000000FFFF;
        let saved_dfa = image[16] == bitone;
        if byte_count(record.body_bytes) != 8
           | (image & 0xFFFFFFFFFFFE0000) != 0x0000000000000000
           | saved_status[4] != bitone
           | not_bool(restored_event_state_valid(before, saved_status, saved_dfa)) then
          uop_step_fault(faulted(before, instruction.form.operation,
            InvalidControlState, "invalid base supervisor-state record"))
        else {
          var updated = speculative;
          updated.status = saved_status;
          updated.supervisor = true;
          updated.current_dfa = saved_dfa;
          uop_step_continue(updated, values)
        }
      },
    },
  }

function lower_base_state_record_uops(instruction : Decoded_instruction,
                                      supervisor_record : bool, restore : bool)
  -> option(list(Uop)) =
  match operand_named(instruction, Operand_memory) {
    None() => None(),
    Some(memory) => {
      let size = if supervisor_record then 8 else 184;
      let captured = uop_location_make_temporary(0);
      let response = uop_location_make_temporary(1);
      let capture = uop_make(
        UopStateRecordAddress(), uop_operand_location(memory),
        uop_location_make_immediate(0x0000000000000008), captured,
        Operand_memory, size, CommitNone
      );
      let transfer = if supervisor_record then
        if restore then uop_make(UopBaseSupervisorRestoreRead(), captured,
          uop_location_make_none(), response, Operand_memory, size, CommitMemory)
        else uop_make(UopBaseSupervisorSave(), captured,
          uop_location_make_none(), uop_location_make_none(), Operand_memory,
          size, CommitMemory)
      else if restore then uop_make(UopBaseUserRestoreRead(), captured,
        uop_location_make_none(), response, Operand_memory, size, CommitMemory)
      else uop_make(UopBaseUserSave(), captured,
        uop_location_make_none(), uop_location_make_none(), Operand_memory,
        size, CommitMemory);
      let install = if not_bool(restore) then [||]
        else if supervisor_record then [|uop_make(
          UopBaseSupervisorRestoreCommit(), response, uop_location_make_none(),
          uop_location_make_none(), Operand_memory, size, CommitMemory)|]
        else [|uop_make(UopBaseUserRestoreCommit(), response,
          uop_location_make_none(), uop_location_make_none(), Operand_memory,
          size, CommitMemory)|];
      Some(capture :: transfer :: uop_program_append(install, [|uop_make(
        UopCommit(), uop_location_make_none(), uop_location_make_none(),
        uop_location_make_none(), Operand_memory, size, CommitMemory)|]))
    },
  }
