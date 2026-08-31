function clause register_result_extension(Op_LDP) = RegisterZeroExtend
function clause repeat_semantics(Op_LDP) = RepeatObserveDestination

function lower_LDP_uops(instruction : Decoded_instruction) -> option(list(Uop)) =
  match (operand_named(instruction, Operand_memory), operand_named(instruction, Operand_pair_id)) {
    (Some(memory_operand), Some(pair_operand)) => {
      let memory = uop_operand_lower(memory_operand, 16, 0, false);
      let response = uop_location_make_temporary(memory.next_temporary);
      let first = unsigned(pair_operand.value[2 .. 0]) * 2;
      let destination = uop_location_make_register(first);
      let load = uop_make(UopMemoryLoadPair(), memory.address, uop_location_make_none(),
        response, Operand_memory, 16, CommitMemory);
      let complete = uop_make(UopMemoryLoadPairComplete(), response,
        uop_location_make_none(), destination, Operand_pair_id, 16, CommitRegisters);
      Some(uop_program_build(memory.program, [|load, complete|],
        Operand_pair_id, 16, CommitMemory))
    }, _ => None(),
  }

function execute_LDP(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
  match lower_LDP_uops(instruction) {
    Some(program) => Some(uop_program_execute(program, instruction, state)),
    None() => Some(faulted(state, instruction.form.operation, IllegalInstruction,
                           "LDP could not be lowered")),
  }
