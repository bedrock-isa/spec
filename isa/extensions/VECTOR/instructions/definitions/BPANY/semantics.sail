function clause register_result_extension(Op_BPANY) = RegisterZeroExtend

function clause repeat_semantics(Op_BPANY) = RepeatObserveDestination

function clause vector_semantics(Op_BPANY) = vector_default_semantics()

function lower_BPANY_uops(instruction : Decoded_instruction) -> option(list(Uop)) =
  match operand_named(instruction, Operand_target) {
    Some(target) => {
      let lowered = uop_operand_lower(target, 8, 0, true);
      let target_value = uop_location_make_temporary(lowered.next_temporary);
      let relative = target.operand_type == OperandType_imm8s | target.operand_type == OperandType_imm16s
                   | target.operand_type == OperandType_imm32s;
      Some(uop_program_append([|uop_make(UopVectorBranchGuard(VectorBranchAny), uop_location_make_none(), uop_location_make_none(), uop_location_make_none(),
                                  Operand_target, 0, CommitControl)|],
        uop_program_append(lowered.program, [|
          uop_make(UopControlTarget(relative), lowered.value, uop_location_make_none(), target_value, Operand_target, 8, CommitControl),
          uop_make(UopControlProbe(), target_value, uop_location_make_segment(0), uop_location_make_none(), Operand_target, 8, CommitControl),
          uop_make(UopControlCommit(ControlJump), target_value, uop_location_make_segment(0), uop_location_make_none(), Operand_target, 8, CommitControl)
        |])))
    }, None() => None(),
  }

function execute_BPANY(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
  match lower_BPANY_uops(instruction) {
    Some(program) => Some(uop_program_execute(program, instruction, state)),
    None() => Some(faulted(state, instruction.form.operation, IllegalInstruction, "BPANY could not be lowered")),
  }
