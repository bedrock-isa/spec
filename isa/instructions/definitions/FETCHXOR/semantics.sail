function clause register_result_extension(Op_FETCHXOR) = RegisterZeroExtend

function clause repeat_semantics(Op_FETCHXOR) = RepeatObserveDestination

function lower_FETCHXOR_uops(instruction : Decoded_instruction) -> option(list(Uop)) =
  match (operand_named(instruction, Operand_memory), operand_named(instruction, Operand_src),
         operand_named(instruction, Operand_src), operand_named(instruction, Operand_order)) {
    (Some(memory_operand), Some(first_operand), Some(second_operand), Some(order_operand)) => {
      let width = operation_width(instruction);
      let memory = uop_operand_lower(memory_operand, width, 0, false);
      let first = uop_operand_location(first_operand);
      let second = uop_operand_location(second_operand);
      let order = uop_operand_location(order_operand);
      Some(uop_program_build_atomic(memory, first, second, order, AtomicFetchXor,
        Operand_src, width))
    }, _ => None(),
  }

function execute_FETCHXOR(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
  match lower_FETCHXOR_uops(instruction) {
    Some(program) => Some(uop_program_execute(program, instruction, state)),
    None() => Some(faulted(state, instruction.form.operation, IllegalInstruction, "FETCHXOR could not be lowered")),
  }
