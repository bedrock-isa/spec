function clause register_result_extension(Op_MADD) = RegisterZeroExtend

function clause repeat_semantics(Op_MADD) = RepeatObserveDestination

function lower_MADD_uops(instruction : Decoded_instruction) -> option(list(Uop)) =
  match (operand_named(instruction, Operand_lhs), operand_named(instruction, Operand_rhs),
         operand_named(instruction, Operand_dst)) {
    (Some(lhs), Some(rhs), Some(dst)) => {
      let width = operation_width(instruction);
      let product = uop_location_make_temporary(0);
      let destination = uop_operand_location(dst);
      let multiply = uop_make(UopIntegerMath(IntegerMultiplyLow),
        uop_operand_location(lhs), uop_operand_location(rhs), product,
        Operand_dst, width, CommitRegisters);
      let add = uop_make(UopIntegerAdd(), destination, product, destination,
        Operand_dst, width, CommitRegisters);
      Some(uop_program_build([||], [|multiply, add|], Operand_dst, width, CommitRegisters))
    },
    _ => None(),
  }

function execute_MADD(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
  match lower_MADD_uops(instruction) {
    Some(program) => Some(uop_program_execute(program, instruction, state)),
    None() => Some(faulted(state, instruction.form.operation, IllegalInstruction,
                           "MADD could not be lowered")),
  }
