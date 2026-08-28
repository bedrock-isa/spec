function clause register_result_extension(Op_DJcc) = RegisterZeroExtend

function clause repeat_semantics(Op_DJcc) = RepeatObserveDestination

function lower_DJcc_uops(instruction : Decoded_instruction) -> option(list(Uop)) =
  match operand_named(instruction, Operand_target) {
    Some(target) => {
      let lowered = uop_operand_lower(target, operation_width(instruction), 0, true);
      let result = uop_location_make_temporary(lowered.next_temporary);
      let relative = target.operand_type == OperandType_imm8s | target.operand_type == OperandType_imm16s
                   | target.operand_type == OperandType_imm32s;
      Some(uop_program_append([|uop_make(UopCountGuard(true), uop_location_make_none(), uop_location_make_none(), uop_location_make_none(),
                                  Operand_counter, 0, CommitControl)|], uop_program_append(lowered.program, [|
        uop_make(UopControlTarget(relative), lowered.value, uop_location_make_none(), result, Operand_target,
                 operation_width(instruction), CommitControl),
        uop_make(UopControlProbe(), result, uop_location_make_segment(0), uop_location_make_none(), Operand_target, 8, CommitControl),
        uop_make(UopControlCommit(ControlJump), result, uop_location_make_segment(0), uop_location_make_none(), Operand_target, 8, CommitControl)
      |])))
    }, None() => None(),
  }

function execute_DJcc(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
  match lower_DJcc_uops(instruction) {
    Some(program) => Some(uop_program_execute(program, instruction, state)),
    None() => Some(faulted(state, Op_DJcc, IllegalInstruction, "DJcc could not be lowered")),
  }
