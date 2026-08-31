function clause register_result_extension(Op_FETCHXCHG) = RegisterZeroExtend

function clause repeat_semantics(Op_FETCHXCHG) = RepeatObserveDestination

function lower_FETCHXCHG_uops(instruction : Decoded_instruction) -> option(list(Uop)) =
  match (operand_named(instruction, Operand_memory), operand_named(instruction, Operand_src),
         operand_named(instruction, Operand_order)) {
    (Some(memory_operand), Some(source_operand), Some(order_operand)) => {
      let width = operation_width(instruction);
      let memory = uop_operand_lower(memory_operand, width, 0, false);
      let source = uop_operand_location(source_operand);
      let order = uop_operand_location(order_operand);
      Some(uop_program_build_atomic(memory, source, source, order, AtomicFetchExchange,
        Operand_src, width))
    },
    _ => None(),
  }

function execute_FETCHXCHG(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
  match lower_FETCHXCHG_uops(instruction) {
    Some(program) => Some(uop_program_execute(program, instruction, state)),
    None() => Some(faulted(state, instruction.form.operation, IllegalInstruction,
                           "FETCHXCHG could not be lowered")),
  }
