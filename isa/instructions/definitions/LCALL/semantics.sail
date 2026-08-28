function clause register_result_extension(Op_LCALL) = RegisterZeroExtend

function clause repeat_semantics(Op_LCALL) = RepeatObserveDestination

function lower_LCALL_uops(instruction : Decoded_instruction) -> option(list(Uop)) =
  match (operand_named(instruction, Operand_target), operand_named(instruction, Operand_new_cs)) {
    (Some(target), Some(new_cs)) => {
      let lowered = uop_operand_lower(target, operation_width(instruction), 0, true);
      let target_value = uop_location_make_temporary(lowered.next_temporary);
      let return_value = uop_location_make_temporary(lowered.next_temporary + 1);
      let cs = uop_operand_location(new_cs);
      Some(uop_program_append(lowered.program, [|
        uop_make(UopControlTarget(false), lowered.value, uop_location_make_none(), target_value, Operand_target,
                 operation_width(instruction), CommitControl),
        uop_make(UopControlProbe(), target_value, cs, uop_location_make_none(), Operand_target, 8, CommitControl),
        uop_make(UopNextPc(), uop_location_make_none(), uop_location_make_none(), return_value, Operand_target, 8, CommitControl),
        uop_make(UopIntegerAdd(), uop_location_make_sp(), uop_location_make_immediate(bits_from_int(0 - 16)), uop_location_make_sp(), Operand_target, 8, CommitControl),
        uop_make(UopStackRange(true), uop_location_make_sp(), uop_location_make_none(), uop_location_make_none(), Operand_target, 16, CommitMemory),
        uop_make(UopStackStorePair(), return_value, uop_location_make_segment(0), uop_location_make_sp(), Operand_target, 16, CommitMemory),
        uop_make(UopControlCommit(ControlFarCall), target_value, cs, uop_location_make_none(), Operand_target, 8, CommitControl)
      |]))
    }, _ => None(),
  }

function execute_LCALL(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
  match lower_LCALL_uops(instruction) {
    Some(program) => Some(uop_program_execute(program, instruction, state)),
    None() => Some(faulted(state, Op_LCALL, IllegalInstruction, "LCALL could not be lowered")),
  }
