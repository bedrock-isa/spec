function clause register_result_extension(Op_STP) = RegisterZeroExtend
function clause repeat_semantics(Op_STP) = RepeatObserveSource

function lower_STP_uops(instruction : Decoded_instruction) -> option(list(Uop)) =
  match (operand_named(instruction, Operand_pair_id), operand_named(instruction, Operand_memory)) {
    (Some(pair_operand), Some(memory_operand)) => {
      let memory = uop_operand_lower(memory_operand, 16, 0, false);
      let first = unsigned(pair_operand.value[2 .. 0]) * 2;
      let store = uop_make_ternary(UopMemoryStorePair(),
        uop_location_make_register(first), uop_location_make_register(first + 1),
        memory.address, uop_location_make_none(), Operand_memory, 16, CommitMemory);
      Some(uop_program_build(memory.program, [|store|], Operand_memory, 16, CommitMemory))
    }, _ => None(),
  }

function execute_STP(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
  match lower_STP_uops(instruction) {
    Some(program) => Some(uop_program_execute(program, instruction, state)),
    None() => Some(faulted(state, instruction.form.operation, IllegalInstruction,
                           "STP could not be lowered")),
  }
