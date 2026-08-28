function clause register_result_extension(Op_CLR) = RegisterZeroExtend

function clause repeat_semantics(Op_CLR) = RepeatObserveDestination

function lower_CLR_uops(instruction : Decoded_instruction) -> option(list(Uop)) =
  match operand_named(instruction, Operand_dst) {
    Some(operand) => {
      let width = operation_width(instruction);
      let destination = uop_operand_lower(operand, width, 0, false);
      Some(uop_program_build_transfer(destination.program, uop_location_make_immediate(0x0000000000000000),
        destination, Operand_dst, width, destination.memory))
    }, None() => None(),
  }

function execute_CLR(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
  match lower_CLR_uops(instruction) {
    Some(program) => Some(uop_program_execute(program, instruction, state)),
    None() => Some(faulted(state, instruction.form.operation, IllegalInstruction, "CLR could not be lowered")),
  }
