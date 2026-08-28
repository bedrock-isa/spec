function clause register_result_extension(Op_LJMP) = RegisterZeroExtend

function clause repeat_semantics(Op_LJMP) = RepeatObserveDestination

function lower_LJMP_uops(instruction : Decoded_instruction) -> option(list(Uop)) =
  match (operand_named(instruction, Operand_target), operand_named(instruction, Operand_new_cs)) {
    (Some(target), Some(new_cs)) => {
      let lowered = uop_operand_lower(target, operation_width(instruction), 0, true);
      let target_value = uop_location_make_temporary(lowered.next_temporary);
      let cs = uop_operand_location(new_cs);
      Some(uop_program_append(lowered.program, [|
        uop_make(UopControlTarget(false), lowered.value, uop_location_make_none(), target_value, Operand_target,
                 operation_width(instruction), CommitControl),
        uop_make(UopControlProbe(), target_value, cs, uop_location_make_none(), Operand_target, 8, CommitControl),
        uop_make(UopControlCommit(ControlFarJump), target_value, cs, uop_location_make_none(), Operand_target, 8, CommitControl)
      |]))
    }, _ => None(),
  }

function execute_LJMP(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
  match lower_LJMP_uops(instruction) {
    Some(program) => Some(uop_program_execute(program, instruction, state)),
    None() => Some(faulted(state, Op_LJMP, IllegalInstruction, "LJMP could not be lowered")),
  }
