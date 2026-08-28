function clause register_result_extension(Op_SETcc) = RegisterZeroExtend

function clause repeat_semantics(Op_SETcc) = RepeatObserveDestination

function lower_SETcc_uops(instruction : Decoded_instruction) -> option(list(Uop)) =
  match operand_named(instruction, Operand_dst) {
    Some(destination_operand) => {
      let width = operation_width(instruction);
      let destination = uop_operand_lower(destination_operand, width, 0, false);
      let output = if destination.memory then uop_location_make_temporary(destination.next_temporary)
                   else destination.value;
      let operation = uop_make(UopPredicateValue(), uop_location_make_none(), uop_location_make_none(),
        output, Operand_dst, width, CommitRegisters);
      Some(uop_program_build_operation(destination.program, operation, output, destination,
        Operand_dst, width, destination.memory))
    }, None() => None(),
  }

function execute_SETcc(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
  match lower_SETcc_uops(instruction) {
    Some(program) => Some(uop_program_execute(program, instruction, state)),
    None() => Some(faulted(state, instruction.form.operation, IllegalInstruction, "SETcc could not be lowered")),
  }
