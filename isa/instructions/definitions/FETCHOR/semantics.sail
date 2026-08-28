function clause register_result_extension(Op_FETCHOR) = RegisterZeroExtend

function clause repeat_semantics(Op_FETCHOR) = RepeatObserveDestination

function lower_FETCHOR_uops(instruction : Decoded_instruction) -> option(list(Uop)) =
  match (operand_named(instruction, Operand_memory), operand_named(instruction, Operand_src),
         operand_named(instruction, Operand_src), operand_named(instruction, Operand_order)) {
    (Some(memory_operand), Some(first_operand), Some(second_operand), Some(order_operand)) => {
      let width = operation_width(instruction);
      let memory = uop_operand_lower(memory_operand, width, 0, false);
      let first = uop_operand_location(first_operand);
      let second = uop_operand_location(second_operand);
      let order = uop_operand_location(order_operand);
      Some(uop_program_build_atomic(memory, first, second, order, AtomicFetchOr,
        Operand_src, width))
    }, _ => None(),
  }

function execute_FETCHOR(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
  match lower_FETCHOR_uops(instruction) {
    Some(program) => Some(uop_program_execute(program, instruction, state)),
    None() => Some(faulted(state, instruction.form.operation, IllegalInstruction, "FETCHOR could not be lowered")),
  }
