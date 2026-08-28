function clause register_result_extension(Op_PUSH) = RegisterZeroExtend

function clause repeat_semantics(Op_PUSH) = RepeatObserveSource

function lower_PUSH_uops(instruction : Decoded_instruction) -> option(list(Uop)) =
  match operand_named(instruction, Operand_reg) {
    Some(reg) => Some(uop_program_build_stack_push(uop_operand_location(reg), Operand_reg)),
    None() => None(),
  }

function execute_PUSH(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
  match lower_PUSH_uops(instruction) {
    Some(program) => Some(uop_program_execute(program, instruction, state)),
    None() => Some(faulted(state, instruction.form.operation, IllegalInstruction, "PUSH could not be lowered")),
  }
