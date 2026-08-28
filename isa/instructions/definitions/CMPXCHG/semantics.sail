function clause register_result_extension(Op_CMPXCHG) = RegisterZeroExtend

function clause repeat_semantics(Op_CMPXCHG) = RepeatObserveDestination

function lower_CMPXCHG_uops(instruction : Decoded_instruction) -> option(list(Uop)) =
  match (operand_named(instruction, Operand_memory), operand_named(instruction, Operand_expected),
         operand_named(instruction, Operand_desired), operand_named(instruction, Operand_order)) {
    (Some(memory_operand), Some(first_operand), Some(second_operand), Some(order_operand)) => {
      let width = operation_width(instruction);
      let memory = uop_operand_lower(memory_operand, width, 0, false);
      let first = uop_operand_location(first_operand);
      let second = uop_operand_location(second_operand);
      let order = uop_operand_location(order_operand);
      Some(uop_program_build_atomic(memory, first, second, order, AtomicCompareExchange,
        Operand_expected, width))
    }, _ => None(),
  }

function execute_CMPXCHG(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
  match lower_CMPXCHG_uops(instruction) {
    Some(program) => Some(uop_program_execute(program, instruction, state)),
    None() => Some(faulted(state, instruction.form.operation, IllegalInstruction, "CMPXCHG could not be lowered")),
  }
