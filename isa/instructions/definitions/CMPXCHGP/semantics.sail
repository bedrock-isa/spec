function clause register_result_extension(Op_CMPXCHGP) = RegisterZeroExtend

function clause repeat_semantics(Op_CMPXCHGP) = RepeatObserveDestination

function lower_CMPXCHGP_uops(instruction : Decoded_instruction) -> option(list(Uop)) =
  match (operand_named(instruction, Operand_memory), operand_named(instruction, Operand_expected),
         operand_named(instruction, Operand_desired), operand_named(instruction, Operand_order)) {
    (Some(memory_operand), Some(expected_operand), Some(desired_operand), Some(order_operand)) => {
      let memory = uop_operand_lower(memory_operand, 16, 0, false);
      let expected_index = unsigned(expected_operand.value[2 .. 0]) * 2;
      let desired_index = unsigned(desired_operand.value[2 .. 0]) * 2;
      let expected = uop_location_make_register(expected_index);
      let desired = uop_location_make_register(desired_index);
      let response = uop_location_make_temporary(memory.next_temporary);
      let issue = {
        uop_make_ternary(UopAtomicIssue(AtomicCompareExchangePair), memory.address,
          expected, desired, response, Operand_memory, 16, CommitMemory) with
        auxiliary = uop_operand_location(order_operand),
      };
      let complete = uop_make(UopAtomicComplete(AtomicCompareExchangePair),
        response, expected, expected, Operand_expected, 16, CommitRegisters);
      Some(uop_program_build(memory.program, [|issue, complete|],
        Operand_expected, 16, CommitMemory))
    },
    _ => None(),
  }

function execute_CMPXCHGP(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
  match lower_CMPXCHGP_uops(instruction) {
    Some(program) => Some(uop_program_execute(program, instruction, state)),
    None() => Some(faulted(state, instruction.form.operation, IllegalInstruction,
                           "CMPXCHGP could not be lowered")),
  }
