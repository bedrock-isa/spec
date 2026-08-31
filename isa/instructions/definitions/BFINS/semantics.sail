function clause register_result_extension(Op_BFINS) = RegisterZeroExtend

function clause repeat_semantics(Op_BFINS) = RepeatObserveDestination

function lower_BFINS_uops(instruction : Decoded_instruction) -> option(list(Uop)) =
  match (operand_named(instruction, Operand_lsb), operand_named(instruction, Operand_width_minus1),
         operand_named(instruction, Operand_src), operand_named(instruction, Operand_dst)) {
    (Some(lsb), Some(width_minus1), Some(src), Some(dst)) => {
      let width = operation_width(instruction);
      let operation = uop_make_ternary(UopIntegerBitfield(IntegerBitfieldInsert),
        uop_operand_location(src), uop_operand_location(lsb), uop_operand_location(width_minus1),
        uop_operand_location(dst), Operand_dst, width, CommitRegisters);
      Some(uop_program_build([||], [|operation|], Operand_dst, width, CommitRegisters))
    },
    _ => None(),
  }

function execute_BFINS(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
  match lower_BFINS_uops(instruction) {
    Some(program) => Some(uop_program_execute(program, instruction, state)),
    None() => Some(faulted(state, instruction.form.operation, IllegalInstruction,
                           "BFINS could not be lowered")),
  }
