function clause register_result_extension(Op_MSUB) = RegisterZeroExtend

function clause repeat_semantics(Op_MSUB) = RepeatObserveDestination

function lower_MSUB_uops(instruction : Decoded_instruction) -> option(list(Uop)) =
  match (operand_named(instruction, Operand_lhs), operand_named(instruction, Operand_rhs),
         operand_named(instruction, Operand_dst)) {
    (Some(lhs), Some(rhs), Some(dst)) => {
      let width = operation_width(instruction);
      let product = uop_location_make_temporary(0);
      let destination = uop_operand_location(dst);
      let multiply = uop_make(UopIntegerMath(IntegerMultiplyLow),
        uop_operand_location(lhs), uop_operand_location(rhs), product,
        Operand_dst, width, CommitRegisters);
      let subtract = uop_make(UopIntegerAlu(IntegerAluSubtract), destination, product,
        destination, Operand_dst, width, CommitRegisters);
      Some(uop_program_build([||], [|multiply, subtract|], Operand_dst, width, CommitRegisters))
    },
    _ => None(),
  }

function execute_MSUB(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
  match lower_MSUB_uops(instruction) {
    Some(program) => Some(uop_program_execute(program, instruction, state)),
    None() => Some(faulted(state, instruction.form.operation, IllegalInstruction,
                           "MSUB could not be lowered")),
  }
