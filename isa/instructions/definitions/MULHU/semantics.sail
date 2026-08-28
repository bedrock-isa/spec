function clause register_result_extension(Op_MULHU) = RegisterZeroExtend

function clause repeat_semantics(Op_MULHU) = RepeatObserveDestination

function lower_MULHU_uops(instruction : Decoded_instruction) -> option(list(Uop)) =
  match (operand_named(instruction, Operand_src), operand_named(instruction, Operand_dst)) {
    (Some(source_operand), Some(destination_operand)) => {
      let width = operation_width(instruction);
      let source = uop_operand_lower(source_operand, width, 0, true);
      let destination = uop_operand_lower(destination_operand, width, source.next_temporary, true);
      let operation = uop_make(UopIntegerMath(IntegerMultiplyHighUnsigned), destination.value, source.value,
        destination.value, Operand_dst, width, CommitRegisters);
      Some(uop_program_build_operation(
        uop_program_append(source.program, destination.program), operation, destination.value, destination,
        Operand_dst, width, source.memory | destination.memory
      ))
    }, _ => None(),
  }

function execute_MULHU(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
  match lower_MULHU_uops(instruction) {
    Some(program) => Some(uop_program_execute(program, instruction, state)),
    None() => Some(faulted(state, instruction.form.operation, IllegalInstruction,
                           "MULHU could not be lowered")),
  }
