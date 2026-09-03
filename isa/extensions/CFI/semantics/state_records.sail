function cfi_supervisor_record_bytes(state : Cpu_state) -> list(bits(8)) =
  append_bytes(le64_bytes(state.lkl), le64_bytes(state.lkh))

union clause Uop_kind = UopCfiSupervisorSave : unit
union clause Uop_kind = UopCfiSupervisorRestoreRead : unit
union clause Uop_kind = UopCfiSupervisorRestoreCommit : unit

function clause execute_uop(UopCfiSupervisorSave(), uop, values, instruction,
                            before, _) =
  match uop_value_get(values, uop.source0.index) {
    Some(address) => uop_step_wait(
      0 - 1,
      state_record_request(
        address, Write, 16, AccessStore,
        [|state_record_range(address, 0, 16)|], 0,
        cfi_supervisor_record_bytes(before), true
      ),
      0x0000000000000000
    ),
    None() => uop_step_fault(faulted(
      before, instruction.form.operation, InvalidControlState,
      "CFI supervisor-state record address was not captured"
    )),
  }

function clause execute_uop(UopCfiSupervisorRestoreRead(), uop, values,
                            instruction, before, _) =
  match uop_value_get(values, uop.source0.index) {
    Some(address) => uop_step_wait(
      uop.destination.index,
      state_record_request(
        address, Read, 16, AccessLoad,
        [|state_record_range(address, 0, 16)|], 16, [||], false
      ),
      0x0000000000000000
    ),
    None() => uop_step_fault(faulted(
      before, instruction.form.operation, InvalidControlState,
      "CFI supervisor-state record address was not captured"
    )),
  }

function clause execute_uop(UopCfiSupervisorRestoreCommit(), uop, values,
                            instruction, before, speculative) =
  match uop_value_get(values, uop.source0.index) {
    None() => uop_step_fault(faulted(
      before, instruction.form.operation, InvalidControlState,
      "CFI supervisor-state record is unavailable"
    )),
    Some(record) => match (
      read_le_bits(record.body_bytes, 0, 64),
      read_le_bits(record.body_bytes, 8, 64)
    ) {
      (Some(lkl), Some(lkh)) =>
        if byte_count(record.body_bytes) != 16 then
          uop_step_fault(faulted(
            before, instruction.form.operation, InvalidControlState,
            "invalid CFI supervisor-state record"
          ))
        else {
          var updated = speculative;
          updated.lkl = lkl;
          updated.lkh = lkh;
          uop_step_continue(updated, values)
        },
      _ => uop_step_fault(faulted(
        before, instruction.form.operation, InvalidControlState,
        "invalid CFI supervisor-state record"
      )),
    },
  }

function lower_cfi_state_record_uops(instruction : Decoded_instruction,
                                     restore : bool) -> option(list(Uop)) =
  match operand_named(instruction, Operand_memory) {
    None() => None(),
    Some(memory) => {
      let address = uop_location_make_temporary(0);
      let record = uop_location_make_temporary(1);
      let capture = uop_make(
        UopStateRecordAddress(), uop_operand_location(memory),
        uop_location_make_immediate(0x0000000000000008), address,
        Operand_memory, 16, CommitNone
      );
      let transfer = if restore then [|
        uop_make(
          UopCfiSupervisorRestoreRead(), address, uop_location_make_none(),
          record, Operand_memory, 16, CommitMemory
        ),
        uop_make(
          UopCfiSupervisorRestoreCommit(), record, uop_location_make_none(),
          uop_location_make_none(), Operand_memory, 16, CommitMemory
        )
      |] else [|uop_make(
        UopCfiSupervisorSave(), address, uop_location_make_none(),
        uop_location_make_none(), Operand_memory, 16, CommitMemory
      )|];
      Some(capture :: uop_program_append(transfer, [|uop_make(
        UopCommit(), uop_location_make_none(), uop_location_make_none(),
        uop_location_make_none(), Operand_memory, 16, CommitMemory
      )|]))
    },
  }
