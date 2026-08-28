function clause register_result_extension(Op_POP) = RegisterZeroExtend

function clause repeat_semantics(Op_POP) = RepeatObserveDestination

function lower_POP_uops(instruction : Decoded_instruction) -> option(list(Uop)) =
  match operand_named(instruction, Operand_reg) {
    Some(reg) => Some(uop_program_build_stack_pop(uop_operand_location(reg), Operand_reg)),
    None() => None(),
  }

function execute_POP(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
  match lower_POP_uops(instruction) {
    Some(program) => Some(uop_program_execute(program, instruction, state)),
    None() => Some(faulted(state, instruction.form.operation, IllegalInstruction, "POP could not be lowered")),
  }
