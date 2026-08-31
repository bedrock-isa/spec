function clause register_result_extension(Op_MOVACQ) = RegisterZeroExtend

function clause repeat_semantics(Op_MOVACQ) = RepeatObserveDestination

function lower_MOVACQ_uops(instruction : Decoded_instruction) -> option(list(Uop)) =
  match (operand_named(instruction, Operand_memory), operand_named(instruction, Operand_dst)) {
    (Some(memory_operand), Some(destination_operand)) => {
      let width = operation_width(instruction);
      let memory = uop_operand_lower(memory_operand, width, 0, false);
      let result = uop_location_make_temporary(memory.next_temporary);
      let load = uop_make(UopMemoryLoadAcquire(), memory.address,
        uop_location_make_none(), result, Operand_memory, width, CommitMemory);
      let move = uop_make(UopMove(), result, uop_location_make_none(),
        uop_operand_location(destination_operand), Operand_dst, width, CommitRegisters);
      Some(uop_program_build(memory.program, [|load, move|], Operand_dst, width, CommitMemory))
    },
    _ => None(),
  }

function execute_MOVACQ(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
  match lower_MOVACQ_uops(instruction) {
    Some(program) => Some(uop_program_execute(program, instruction, state)),
    None() => Some(faulted(state, instruction.form.operation, IllegalInstruction,
                           "MOVACQ could not be lowered")),
  }
