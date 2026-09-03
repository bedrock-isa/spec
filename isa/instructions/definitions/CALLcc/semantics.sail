function clause register_result_extension(Op_CALLcc) = RegisterZeroExtend

function clause repeat_semantics(Op_CALLcc) = RepeatObserveDestination

function lower_CALLcc_uops(instruction : Decoded_instruction) -> option(list(Uop)) =
  match operand_named(instruction, Operand_target) {
    Some(target) => {
      let lowered = uop_operand_lower(target, operation_width(instruction), 0, true);
      let target_value = uop_location_make_temporary(lowered.next_temporary);
      let return_value = uop_location_make_temporary(lowered.next_temporary + 1);
      let relative = target.operand_type == OperandType_imm8s | target.operand_type == OperandType_imm16s
                   | target.operand_type == OperandType_imm32s;
      Some(uop_program_append([|
        uop_make(UopPredicateGuard(), uop_location_make_none(),
          uop_location_make_none(), uop_location_make_none(), Operand_target,
          0, CommitControl),
        uop_make(UopLinkInactiveGuard(), uop_location_make_none(),
          uop_location_make_none(), uop_location_make_none(), Operand_target,
          0, CommitControl)
      |], uop_program_append(lowered.program, [|
        uop_make(UopControlTarget(relative), lowered.value, uop_location_make_none(), target_value, Operand_target,
                 operation_width(instruction), CommitControl),
        uop_make(UopControlProbe(), target_value, uop_location_make_segment(0), uop_location_make_none(), Operand_target, 8, CommitControl),
        uop_make(UopNextPc(), uop_location_make_none(), uop_location_make_none(), return_value, Operand_target, 8, CommitControl),
        uop_make(UopIntegerAdd(), uop_location_make_sp(), uop_location_make_immediate(bits_from_int(0 - 8)), uop_location_make_sp(), Operand_target, 8, CommitControl),
        uop_make(UopStackRange(true), uop_location_make_sp(), uop_location_make_none(), uop_location_make_none(), Operand_target, 8, CommitMemory),
        uop_make(UopStackStore(), return_value, uop_location_make_sp(), uop_location_make_none(), Operand_target, 8, CommitMemory),
        uop_make(UopControlCommit(ControlCall), target_value, uop_location_make_segment(0), uop_location_make_none(), Operand_target, 8, CommitControl)
      |])))
    }, None() => None(),
  }

function execute_CALLcc(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
  match lower_CALLcc_uops(instruction) {
    Some(program) => Some(uop_program_execute(program, instruction, state)),
    None() => Some(faulted(state, Op_CALLcc, IllegalInstruction, "CALLcc could not be lowered")),
  }
