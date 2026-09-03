function clause register_result_extension(Op_PLCALL) = RegisterZeroExtend

function clause repeat_semantics(Op_PLCALL) = RepeatObserveDestination

function lower_PLCALL_uops(instruction : Decoded_instruction) -> option(list(Uop)) =
  match (operand_named(instruction, Operand_target),
         operand_named(instruction, Operand_new_cs)) {
    (Some(target), Some(new_cs)) => {
      let lowered = uop_operand_lower(target, operation_width(instruction), 0, true);
      let target_value = uop_location_make_temporary(lowered.next_temporary);
      let return_value = uop_location_make_temporary(lowered.next_temporary + 1);
      let pa = uop_location_make_temporary(lowered.next_temporary + 2);
      let cs = uop_operand_location(new_cs);
      Some(uop_program_append([|
        uop_make(UopCfiKeyGuard(), uop_location_make_none(),
          uop_location_make_none(), uop_location_make_none(), Operand_target,
          0, CommitControl),
        uop_make(UopLinkInactiveGuard(), uop_location_make_none(),
          uop_location_make_none(), uop_location_make_none(), Operand_target,
          0, CommitControl)
      |], uop_program_append(lowered.program, [|
        uop_make(UopControlTarget(false), lowered.value,
          uop_location_make_none(), target_value, Operand_target,
          operation_width(instruction), CommitControl),
        uop_make(UopControlProbe(), target_value, cs,
          uop_location_make_none(), Operand_target, 8, CommitControl),
        uop_make(UopNextPc(), uop_location_make_none(),
          uop_location_make_none(), return_value, Operand_target, 8,
          CommitControl),
        uop_make(UopIntegerAdd(), uop_location_make_sp(),
          uop_location_make_immediate(bits_from_int(0 - 24)),
          uop_location_make_sp(), Operand_target, 8, CommitControl),
        uop_make(UopStackRange(true), uop_location_make_sp(),
          uop_location_make_none(), uop_location_make_none(), Operand_target,
          24, CommitMemory),
        uop_make(UopCfiTag(true), return_value,
          uop_location_make_segment(0), pa, Operand_target, 8, CommitControl),
        uop_make_ternary(UopCfiRecordStore(true), return_value,
          uop_location_make_segment(0), pa, uop_location_make_sp(),
          Operand_target, 24, CommitMemory),
        uop_make(UopControlCommit(ControlFarCall), target_value, cs,
          uop_location_make_none(), Operand_target, 8, CommitControl)
      |])))
    },
    _ => None(),
  }

function execute_PLCALL(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) =
  match lower_PLCALL_uops(instruction) {
    Some(program) => Some(uop_program_execute(
      cfi_call_program(program, instruction, state), instruction, state
    )),
    None() => Some(faulted(
      state, Op_PLCALL, IllegalInstruction, "PLCALL could not be lowered"
    )),
  }
