function clause register_result_extension(Op_CMPJcc) = RegisterZeroExtend

function clause repeat_semantics(Op_CMPJcc) = RepeatObserveDestination

function lower_CMPJcc_uops(instruction : Decoded_instruction) -> option(list(Uop)) =
  match (operand_named(instruction, Operand_src), operand_named(instruction, Operand_dst),
         operand_named(instruction, Operand_target)) {
    (Some(src), Some(dst), Some(target)) => Some([|
      uop_make_ternary(UopFusedJump(FusedCompareJump), uop_operand_location(src), uop_operand_location(dst),
                uop_operand_location(target), uop_location_make_none(), Operand_target, operation_width(instruction), CommitControl)
    |]), _ => None(),
  }

function execute_CMPJcc(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
  match lower_CMPJcc_uops(instruction) {
    Some(program) => Some(uop_program_execute(program, instruction, state)),
    None() => Some(faulted(state, Op_CMPJcc, IllegalInstruction, "CMPJcc could not be lowered")),
  }
