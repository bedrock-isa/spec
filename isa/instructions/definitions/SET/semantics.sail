function clause register_result_extension(Op_SET) = RegisterZeroExtend

function clause repeat_semantics(Op_SET) = RepeatObserveDestination

function lower_SET_uops(instruction : Decoded_instruction) -> option(list(Uop)) =
  match operand_named(instruction, Operand_dst) {
    Some(destination_operand) => {
      let width = operation_width(instruction);
      let destination = uop_operand_lower(destination_operand, width, 0, false);
      Some(uop_program_build_transfer(destination.program, uop_location_make_immediate(0x0000000000000001),
        destination, Operand_dst, width, destination.memory))
    }, None() => None(),
  }

function execute_SET(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
  match lower_SET_uops(instruction) {
    Some(program) => Some(uop_program_execute(program, instruction, state)),
    None() => Some(faulted(state, instruction.form.operation, IllegalInstruction, "SET could not be lowered")),
  }
