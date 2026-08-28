function clause register_result_extension(Op_BCLR) = RegisterZeroExtend

function clause repeat_semantics(Op_BCLR) = RepeatObserveFlags

function lower_BCLR_uops(instruction : Decoded_instruction) -> option(list(Uop)) =
  match (operand_named(instruction, Operand_bit_index), operand_named(instruction, Operand_dst)) {
    (Some(index_operand), Some(destination_operand)) => {
      let width = operation_width(instruction);
      let index = uop_operand_lower(index_operand, width, 0, true);
      let destination = uop_operand_lower(destination_operand, width, index.next_temporary, true);
      let operation = uop_make(UopIntegerBit(IntegerBitClear), destination.value,
        index.value, destination.value, Operand_dst, width, CommitRegisters);
      Some(uop_program_build_operation(
        uop_program_append(index.program, destination.program), operation, destination.value, destination,
        Operand_dst, width, index.memory | destination.memory
      ))
    }, _ => None(),
  }

function execute_BCLR(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
  match lower_BCLR_uops(instruction) {
    Some(program) => Some(uop_program_execute(program, instruction, state)),
    None() => Some(faulted(state, instruction.form.operation, IllegalInstruction,
                           "BCLR could not be lowered")),
  }
