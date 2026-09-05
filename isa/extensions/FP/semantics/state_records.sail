function fp_record_register_bytes(registers : Floating_registers, index : int)
  -> list(bits(8)) =
  if index >= 16 then [||]
  else append_bytes(le64_bytes(registers[unsigned(get_slice_int(4, index, 0))]),
                    fp_record_register_bytes(registers, index + 1))

function fp_record_bytes(state : Cpu_state) -> list(bits(8)) = {
  let present = if state.fp_state_modified then 0x000000000003FFFF
                else 0x0000000000000000;
  let state_images = 0x00000000 @ state.fstatus[15 .. 0]
                     @ 0b00000000000 @ state.fflags;
  append_bytes(le64_bytes(present),
    append_bytes(le64_bytes(state_images),
      append_bytes(fp_record_register_bytes(state.floating_registers, 0),
        zero_byte_count(48))))
}

function fp_record_slot_ranges(address : Uop_value, bitmap : bits(64), index : int)
  -> list(Memory_access_range) =
  if index >= 18 then [||]
  else {
    let offset = if index < 16 then 16 + index * 8
                 else if index == 16 then 8 else 10;
    let width = if index < 16 then 8 else 2;
    let tail = fp_record_slot_ranges(address, bitmap, index + 1);
    if bitmap[unsigned(get_slice_int(6, index, 0))] == bitone
    then state_record_range(address, offset, width) :: tail else tail
  }

function fp_record_restore_registers(bytes : list(bits(8)), bitmap : bits(64),
                                     index : int, registers : Floating_registers)
  -> option(Floating_registers) =
  if index >= 16 then Some(registers)
  else if bitmap[unsigned(get_slice_int(4, index, 0))] == bitzero then
    fp_record_restore_registers(bytes, bitmap, index + 1, registers)
  else match read_le_bits(bytes, 16 + index * 8, 64) {
    None() => None(),
    Some(value) => {
      var updated = registers;
      updated[unsigned(get_slice_int(4, index, 0))] = value;
      fp_record_restore_registers(bytes, bitmap, index + 1, updated)
    },
  }

union clause Uop_kind = UopFpRecordSave : unit
union clause Uop_kind = UopFpRecordBitmapRead : unit
union clause Uop_kind = UopFpRecordBodyRead : unit
union clause Uop_kind = UopFpRecordRestoreCommit : unit

function clause execute_uop(UopFpRecordSave(), uop, values, instruction,
                            before, _) =
  match uop_value_get(values, uop.source0.index) {
    Some(address) => uop_step_wait(0 - 1,
      state_record_request(address, Write, 192, AccessStore,
        [|state_record_range(address, 0, 192)|], 0,
        fp_record_bytes(before), true), 0x0000000000000000),
    None() => uop_step_fault(faulted(before, instruction.form.operation,
      InvalidControlState, "floating-point state-record address was not captured")),
  }

function clause execute_uop(UopFpRecordBitmapRead(), uop, values, instruction,
                            before, _) =
  match uop_value_get(values, uop.source0.index) {
    Some(address) => uop_step_wait(uop.destination.index,
      state_record_request(address, Read, 192, AccessLoad,
        [|state_record_buffer_range(address, 0, 8, 0)|], 8, [||], false),
      0x0000000000000000),
    None() => uop_step_fault(faulted(before, instruction.form.operation,
      InvalidControlState, "floating-point state-record address was not captured")),
  }

function clause execute_uop(UopFpRecordBodyRead(), uop, values, instruction,
                            before, _) =
  match (uop_value_get(values, uop.source0.index),
         uop_value_get(values, uop.source1.index)) {
    (Some(address), Some(bitmap_value)) => {
      let bitmap = bitmap_value.value;
      if (bitmap & 0xFFFFFFFFFFFC0000) != 0x0000000000000000 then
        uop_step_fault(faulted(before, instruction.form.operation,
          InvalidControlState, "floating-point state-record bitmap has reserved bits set"))
      else uop_step_wait(uop.destination.index,
        state_record_request(address, Read, 192, AccessLoad,
          state_record_range(address, 0, 8)
          :: state_record_range(address, 12, 4)
          :: state_record_range(address, 144, 48)
          :: fp_record_slot_ranges(address, bitmap, 0),
          192, [||], false), bitmap)
    },
    _ => uop_step_fault(faulted(before, instruction.form.operation,
      InvalidControlState, "floating-point state-record metadata is unavailable")),
  }

function clause execute_uop(UopFpRecordRestoreCommit(), uop, values,
                            instruction, before, speculative) =
  match (uop_value_get(values, uop.source0.index),
         uop_value_get(values, uop.source1.index)) {
    (Some(record), Some(bitmap_value)) => match (
      read_le_bits(record.body_bytes, 0, 64),
      fp_record_restore_registers(record.body_bytes, bitmap_value.value, 0,
                                  zero_floating_registers()),
      read_le_bits(record.body_bytes, 8, 64)
    ) {
      (Some(bitmap), Some(registers), Some(state_images)) =>
        if byte_count(record.body_bytes) != 192
           | bitmap != bitmap_value.value
           | not_bool(byte_range_zero(record.body_bytes, 144, 48))
           | (state_images & 0xFFFFFFFF00000000) != 0x0000000000000000
           | (bitmap[16] == bitone
              & (state_images & 0x000000000000FFE0) != 0x0000000000000000)
           | (bitmap[17] == bitone
              & (state_images & 0x00000000FC000000) != 0x0000000000000000) then
          uop_step_fault(faulted(before, instruction.form.operation,
            InvalidControlState, "invalid floating-point state record"))
        else {
          var updated = speculative;
          updated.floating_registers = registers;
          updated.fflags = if bitmap[16] == bitone then state_images[4 .. 0]
                           else 0b00000;
          updated.fstatus = if bitmap[17] == bitone
                            then 0x000000000000 @ state_images[31 .. 16]
                            else 0x0000000000000000;
          updated.fp_state_modified = bitmap != 0x0000000000000000;
          uop_step_continue(updated, values)
        },
      _ => uop_step_fault(faulted(before, instruction.form.operation,
        InvalidControlState, "invalid floating-point state record")),
    },
    _ => uop_step_fault(faulted(before, instruction.form.operation,
      InvalidControlState, "floating-point state record is unavailable")),
  }

function lower_fp_state_record_uops(instruction : Decoded_instruction, restore : bool)
  -> option(list(Uop)) =
  match operand_named(instruction, Operand_memory) {
    None() => None(),
    Some(memory) => {
      let address = uop_location_make_temporary(0);
      let bitmap = uop_location_make_temporary(1);
      let body = uop_location_make_temporary(2);
      let capture = uop_make(UopStateRecordAddress(), uop_operand_location(memory),
        uop_location_make_immediate(0x0000000000000040), address,
        Operand_memory, 192, CommitNone);
      let transfer = if restore then [|
        uop_make(UopFpRecordBitmapRead(), address, uop_location_make_none(),
          bitmap, Operand_memory, 192, CommitMemory),
        uop_make(UopFpRecordBodyRead(), address, bitmap, body,
          Operand_memory, 192, CommitMemory),
        uop_make(UopFpRecordRestoreCommit(), body, bitmap,
          uop_location_make_none(), Operand_memory, 192, CommitMemory)
      |] else [|uop_make(UopFpRecordSave(), address, uop_location_make_none(),
        uop_location_make_none(), Operand_memory, 192, CommitMemory)|];
      Some(capture :: uop_program_append(transfer, [|uop_make(
        UopCommit(), uop_location_make_none(), uop_location_make_none(),
        uop_location_make_none(), Operand_memory, 192, CommitMemory)|]))
    },
  }
