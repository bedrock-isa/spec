function clause register_result_extension(Op_BIC) = RegisterZeroExtend

function clause repeat_semantics(Op_BIC) = RepeatObserveDestination

function lower_BIC_uops(instruction : Decoded_instruction) -> option(list(Uop)) =
  match (operand_named(instruction, Operand_src), operand_named(instruction, Operand_dst)) {
    (Some(source_operand), Some(destination_operand)) => {
      let width = operation_width(instruction);
      let source = uop_operand_location(source_operand);
      let destination = uop_operand_location(destination_operand);
      let complement = uop_location_make_temporary(0);
      let invert = uop_make(UopIntegerUnary(IntegerUnaryComplement), source,
        uop_location_make_none(), complement, Operand_src, width, CommitRegisters);
      let clear = uop_make(UopIntegerAlu(IntegerAluAnd), destination, complement,
        destination, Operand_dst, width, CommitRegisters);
      Some(uop_program_build([||], [|invert, clear|], Operand_dst, width, CommitRegisters))
    },
    _ => None(),
  }

function execute_BIC(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
  match lower_BIC_uops(instruction) {
    Some(program) => Some(uop_program_execute(program, instruction, state)),
    None() => Some(faulted(state, instruction.form.operation, IllegalInstruction,
                           "BIC could not be lowered")),
  }
