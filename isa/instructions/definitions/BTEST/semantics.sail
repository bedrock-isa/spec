function clause register_result_extension(Op_BTEST) = RegisterZeroExtend

function clause repeat_semantics(Op_BTEST) = RepeatObserveFlags

function lower_BTEST_uops(instruction : Decoded_instruction) -> option(list(Uop)) =
  match (operand_named(instruction, Operand_bit_index), operand_named(instruction, Operand_dst)) {
    (Some(index_operand), Some(destination_operand)) => {
      let width = operation_width(instruction);
      let index = uop_operand_lower(index_operand, width, 0, true);
      let destination = uop_operand_lower(destination_operand, width, index.next_temporary, true);
      let operation = uop_make(UopIntegerBit(IntegerBitTest), destination.value,
        index.value, uop_location_make_none(), Operand_dst, width, CommitRegisters);
      Some(uop_program_build(uop_program_append(index.program, destination.program),
        [|operation|], Operand_dst, width,
        if index.memory | destination.memory then CommitMemory else CommitRegisters))
    }, _ => None(),
  }

function execute_BTEST(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
  match lower_BTEST_uops(instruction) {
    Some(program) => Some(uop_program_execute(program, instruction, state)),
    None() => Some(faulted(state, instruction.form.operation, IllegalInstruction,
                           "BTEST could not be lowered")),
  }
