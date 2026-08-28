function clause register_result_extension(Op_DIVU) = RegisterZeroExtend

function clause repeat_semantics(Op_DIVU) = RepeatObserveDestination

function lower_DIVU_uops(instruction : Decoded_instruction) -> option(list(Uop)) =
  match (operand_named(instruction, Operand_src), operand_named(instruction, Operand_dst)) {
    (Some(source_operand), Some(destination_operand)) => {
      let width = operation_width(instruction);
      let source = uop_operand_lower(source_operand, width, 0, true);
      let destination = uop_operand_location(destination_operand);
      let operation = uop_make(UopIntegerDivide(IntegerDivideUnsigned), destination, source.value, destination,
                 Operand_dst, width, CommitRegisters);
      Some(uop_program_build(source.program, [|operation|], Operand_dst, width,
        if source.memory then CommitMemory else CommitRegisters))
    }, _ => None(),
  }

function execute_DIVU(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
  match lower_DIVU_uops(instruction) {
    Some(program) => Some(uop_program_execute(program, instruction, state)),
    None() => Some(faulted(state, instruction.form.operation, IllegalInstruction, "DIVU could not be lowered")),
  }
