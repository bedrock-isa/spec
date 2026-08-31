function clause register_result_extension(Op_MOVREL) = RegisterZeroExtend

function clause repeat_semantics(Op_MOVREL) = RepeatObserveSource

function lower_MOVREL_uops(instruction : Decoded_instruction) -> option(list(Uop)) =
  match (operand_named(instruction, Operand_src), operand_named(instruction, Operand_memory)) {
    (Some(source_operand), Some(memory_operand)) => {
      let width = operation_width(instruction);
      let memory = uop_operand_lower(memory_operand, width, 0, false);
      let store = uop_make(UopMemoryStoreRelease(), uop_operand_location(source_operand),
        memory.address, uop_location_make_none(), Operand_memory, width, CommitMemory);
      Some(uop_program_build(memory.program, [|store|], Operand_memory, width, CommitMemory))
    },
    _ => None(),
  }

function execute_MOVREL(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
  match lower_MOVREL_uops(instruction) {
    Some(program) => Some(uop_program_execute(program, instruction, state)),
    None() => Some(faulted(state, instruction.form.operation, IllegalInstruction,
                           "MOVREL could not be lowered")),
  }
