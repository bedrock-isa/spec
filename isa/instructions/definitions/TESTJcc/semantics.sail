function clause register_result_extension(Op_TESTJcc) = RegisterZeroExtend

function clause repeat_semantics(Op_TESTJcc) = RepeatObserveDestination

function lower_TESTJcc_uops(instruction : Decoded_instruction) -> option(list(Uop)) =
  match (operand_named(instruction, Operand_src), operand_named(instruction, Operand_dst),
         operand_named(instruction, Operand_target)) {
    (Some(src), Some(dst), Some(target)) => Some([|
      uop_make_ternary(UopFusedJump(FusedTestJump), uop_operand_location(src), uop_operand_location(dst),
                uop_operand_location(target), uop_location_make_none(), Operand_target, operation_width(instruction), CommitControl)
    |]), _ => None(),
  }

function execute_TESTJcc(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
  match lower_TESTJcc_uops(instruction) {
    Some(program) => Some(uop_program_execute(program, instruction, state)),
    None() => Some(faulted(state, Op_TESTJcc, IllegalInstruction, "TESTJcc could not be lowered")),
  }
