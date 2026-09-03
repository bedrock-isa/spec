function vector_record_size(state : Cpu_state) -> int =
  64 + 64 * tdiv_int(34 * state.vector_length_bytes + 63, 64)

function vector_record_register_bytes(registers : Vector_registers, index : int)
  -> list(bits(8)) =
  if index >= 32 then [||]
  else append_bytes(registers[unsigned(get_slice_int(5, index, 0))],
                    vector_record_register_bytes(registers, index + 1))

function vector_record_predicate_bytes(registers : Predicate_registers, index : int)
  -> list(bits(8)) =
  if index >= 16 then [||]
  else append_bytes(registers[unsigned(get_slice_int(4, index, 0))],
                    vector_record_predicate_bytes(registers, index + 1))

function vector_record_bytes(state : Cpu_state) -> list(bits(8)) = {
  let bitmap = if state.vector_state_modified then 0x0000FFFFFFFFFFFF
               else 0x0000000000000000;
  let payload = append_bytes(vector_record_register_bytes(state.vector_registers, 0),
                  vector_record_predicate_bytes(state.predicate_registers, 0));
  append_bytes(le64_bytes(bitmap), append_bytes(zero_byte_count(56),
    append_bytes(payload, zero_byte_count(vector_record_size(state)
                                          - 64 - 34 * state.vector_length_bytes))))
}

function vector_record_slot_ranges(address : Uop_value, bitmap : bits(64),
                                   bytes_per_vector : int, index : int)
  -> list(Memory_access_range) =
  if index >= 48 then [||]
  else {
    let width = if index < 32 then bytes_per_vector
                else tdiv_int(bytes_per_vector, 8);
    let offset = if index < 32 then 64 + index * bytes_per_vector
      else 64 + 32 * bytes_per_vector + (index - 32) * width;
    let tail = vector_record_slot_ranges(address, bitmap, bytes_per_vector,
                                         index + 1);
    if bitmap[unsigned(get_slice_int(6, index, 0))] == bitone
    then state_record_range(address, offset, width) :: tail else tail
  }

function vector_record_drop(bytes : list(bits(8)), count : int) -> list(bits(8)) =
  if count <= 0 then bytes
  else match bytes {
    [||] => [||],
    _head :: tail => vector_record_drop(tail, count - 1),
  }

function vector_record_take(bytes : list(bits(8)), count : int) -> list(bits(8)) =
  if count <= 0 then [||]
  else match bytes {
    [||] => [||],
    head :: tail => head :: vector_record_take(tail, count - 1),
  }

function vector_record_slice(bytes : list(bits(8)), offset : int, count : int)
  -> list(bits(8)) =
  vector_record_take(vector_record_drop(bytes, offset), count)

function vector_record_restore_vectors(bytes : list(bits(8)), bitmap : bits(64),
                                       bytes_per_vector : int, index : int,
                                       registers : Vector_registers)
  -> Vector_registers =
  if index >= 32 then registers
  else {
    var updated = registers;
    if bitmap[unsigned(get_slice_int(6, index, 0))] == bitone then
      updated[unsigned(get_slice_int(5, index, 0))] =
        vector_record_slice(bytes, 64 + index * bytes_per_vector, bytes_per_vector)
    else ();
    vector_record_restore_vectors(bytes, bitmap, bytes_per_vector, index + 1, updated)
  }

function vector_record_restore_predicates(bytes : list(bits(8)), bitmap : bits(64),
                                          bytes_per_vector : int, index : int,
                                          registers : Predicate_registers)
  -> Predicate_registers =
  if index >= 16 then registers
  else {
    let width = tdiv_int(bytes_per_vector, 8);
    var updated = registers;
    if bitmap[unsigned(get_slice_int(6, index + 32, 0))] == bitone then
      updated[unsigned(get_slice_int(4, index, 0))] = vector_record_slice(
        bytes, 64 + 32 * bytes_per_vector + index * width, width)
    else ();
    vector_record_restore_predicates(bytes, bitmap, bytes_per_vector,
                                     index + 1, updated)
  }

union clause Uop_kind = UopVectorRecordAddress : unit
union clause Uop_kind = UopVectorRecordSave : unit
union clause Uop_kind = UopVectorRecordHeaderRead : unit
union clause Uop_kind = UopVectorRecordBodyRead : unit
union clause Uop_kind = UopVectorRecordRestoreCommit : unit

function clause execute_uop(UopVectorRecordAddress(), uop, values, instruction,
                            before, speculative) =
  match uop_location_read(uop.source0, before, values) {
    Some(raw) => {
      let size = vector_record_size(before);
      let last = add_bits(raw, bits_from_int(size - 1));
      let start_point = segment_point(before.segments[1], raw);
      let last_point = segment_point(before.segments[1], last);
      if tmod_int(unsigned(raw), 64) != 0 then
        uop_step_fault(faulted(before, instruction.form.operation,
          InvalidControlState, "vector state-record address is misaligned"))
      else if unsigned(last) < unsigned(raw) | not_bool(start_point.in_bounds)
              | not_bool(last_point.in_bounds) then
        uop_step_fault(faulted(before, instruction.form.operation,
          AccessFault, "vector state-record range is outside the default data segment"))
      else {
        let address : Uop_value = {
          uop_value_empty() with value = raw, address = true, segment = 1,
          segment_image = before.segments[1], effective_address = raw,
          linear_address = start_point.linear, domain = RequestDomainCurrent,
        };
        uop_step_continue(speculative,
          uop_value_set(values, uop.destination.index, address))
      }
    },
    None() => uop_step_fault(faulted(before, instruction.form.operation,
      InvalidControlState, "vector state-record address is unavailable")),
  }

function clause execute_uop(UopVectorRecordSave(), uop, values, instruction,
                            before, _) =
  match uop_value_get(values, uop.source0.index) {
    Some(address) => {
      let size = vector_record_size(before);
      uop_step_wait(0 - 1, state_record_request(address, Write, size, AccessStore,
        [|state_record_range(address, 0, size)|], 0,
        vector_record_bytes(before), true), 0x0000000000000000)
    },
    None() => uop_step_fault(faulted(before, instruction.form.operation,
      InvalidControlState, "vector state-record address was not captured")),
  }

function clause execute_uop(UopVectorRecordHeaderRead(), uop, values, instruction,
                            before, _) =
  match uop_value_get(values, uop.source0.index) {
    Some(address) => uop_step_wait(uop.destination.index,
      state_record_request(address, Read, vector_record_size(before), AccessLoad,
        [|state_record_range(address, 0, 64)|], 64, [||], false),
      0x0000000000000000),
    None() => uop_step_fault(faulted(before, instruction.form.operation,
      InvalidControlState, "vector state-record address was not captured")),
  }

function clause execute_uop(UopVectorRecordBodyRead(), uop, values, instruction,
                            before, _) =
  match (uop_value_get(values, uop.source0.index),
         uop_value_get(values, uop.source1.index)) {
    (Some(address), Some(header)) => {
      let bitmap = header.value;
      let size = vector_record_size(before);
      if byte_count(header.body_bytes) != 64
         | (bitmap & 0xFFFF000000000000) != 0x0000000000000000
         | not_bool(byte_range_zero(header.body_bytes, 8, 56)) then
        uop_step_fault(faulted(before, instruction.form.operation,
          InvalidControlState, "invalid vector state-record header"))
      else uop_step_wait(uop.destination.index,
        state_record_request(address, Read, size, AccessLoad,
          state_record_range(address, 0, 64)
          :: state_record_range(address, 64 + 34 * before.vector_length_bytes,
                                size - 64 - 34 * before.vector_length_bytes)
          :: vector_record_slot_ranges(address, bitmap,
                                       before.vector_length_bytes, 0),
          size, [||], false), bitmap)
    },
    _ => uop_step_fault(faulted(before, instruction.form.operation,
      InvalidControlState, "vector state-record metadata is unavailable")),
  }

function clause execute_uop(UopVectorRecordRestoreCommit(), uop, values,
                            instruction, before, speculative) =
  match (uop_value_get(values, uop.source0.index),
         uop_value_get(values, uop.source1.index)) {
    (Some(record), Some(header)) => match read_le_bits(record.body_bytes, 0, 64) {
      Some(bitmap) =>
        if byte_count(record.body_bytes) != vector_record_size(before)
           | bitmap != header.value
           | (bitmap & 0xFFFF000000000000) != 0x0000000000000000
           | not_bool(byte_range_zero(record.body_bytes, 8, 56))
           | not_bool(byte_range_zero(
               record.body_bytes, 64 + 34 * before.vector_length_bytes,
               vector_record_size(before) - 64 - 34 * before.vector_length_bytes)) then
          uop_step_fault(faulted(before, instruction.form.operation,
            InvalidControlState, "invalid vector state record"))
        else {
          var updated = speculative;
          updated.vector_registers = vector_record_restore_vectors(
            record.body_bytes, bitmap, before.vector_length_bytes, 0,
            zero_vector_registers(before.vector_length_bytes));
          updated.predicate_registers = vector_record_restore_predicates(
            record.body_bytes, bitmap, before.vector_length_bytes, 0,
            zero_predicate_registers(before.vector_length_bytes));
          updated.vector_state_modified = bitmap != 0x0000000000000000;
          uop_step_continue(updated, values)
        },
      None() => uop_step_fault(faulted(before, instruction.form.operation,
        InvalidControlState, "invalid vector state record")),
    },
    _ => uop_step_fault(faulted(before, instruction.form.operation,
      InvalidControlState, "vector state record is unavailable")),
  }

function lower_vector_state_record_uops(instruction : Decoded_instruction,
                                        restore : bool) -> option(list(Uop)) =
  match operand_named(instruction, Operand_memory) {
    None() => None(),
    Some(memory) => {
      let address = uop_location_make_temporary(0);
      let header = uop_location_make_temporary(1);
      let body = uop_location_make_temporary(2);
      let capture = uop_make(UopVectorRecordAddress(), uop_operand_location(memory),
        uop_location_make_none(), address, Operand_memory, 0, CommitNone);
      let transfer = if restore then [|
        uop_make(UopVectorRecordHeaderRead(), address, uop_location_make_none(),
          header, Operand_memory, 0, CommitMemory),
        uop_make(UopVectorRecordBodyRead(), address, header, body,
          Operand_memory, 0, CommitMemory),
        uop_make(UopVectorRecordRestoreCommit(), body, header,
          uop_location_make_none(), Operand_memory, 0, CommitMemory)
      |] else [|uop_make(UopVectorRecordSave(), address, uop_location_make_none(),
        uop_location_make_none(), Operand_memory, 0, CommitMemory)|];
      Some(capture :: uop_program_append(transfer, [|uop_make(
        UopCommit(), uop_location_make_none(), uop_location_make_none(),
        uop_location_make_none(), Operand_memory, 0, CommitMemory)|]))
    },
  }
