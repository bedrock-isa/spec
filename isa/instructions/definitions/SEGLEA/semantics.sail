function clause register_result_extension(Op_SEGLEA) = RegisterZeroExtend

function clause repeat_semantics(Op_SEGLEA) = RepeatObserveBoolean

function lower_SEGLEA_uops(instruction : Decoded_instruction) -> option(list(Uop)) =
  match (operand_named(instruction, Operand_src), operand_named(instruction, Operand_dst)) {
    (Some(source_operand), Some(destination_operand)) => {
      let source = uop_operand_lower(source_operand, operation_width(instruction), 0, false);
      let destination = uop_operand_location(destination_operand);
      let operation = uop_make(UopSegmentLea(), source.address, uop_location_make_none(), destination, Operand_dst, 8, CommitRegisters);
      Some(uop_program_build(source.program, [|operation|], Operand_dst, 8,
        CommitRegisters))
    }, _ => None(),
  }

function execute_SEGLEA(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
  match lower_SEGLEA_uops(instruction) {
    Some(program) => Some(uop_program_execute(program, instruction, state)),
    None() => Some(faulted(state, instruction.form.operation, IllegalInstruction, "SEGLEA could not be lowered")),
  }
