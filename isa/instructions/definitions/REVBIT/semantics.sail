function clause register_result_extension(Op_REVBIT) = RegisterZeroExtend

function clause repeat_semantics(Op_REVBIT) = RepeatObserveDestination

function lower_REVBIT_uops(instruction : Decoded_instruction) -> option(list(Uop)) =
  match operand_named(instruction, Operand_dst) {
    Some(dst) => {
      let width = operation_width(instruction);
      let location = uop_operand_location(dst);
      let operation = uop_make(UopIntegerCount(IntegerReverseBits), location,
        uop_location_make_none(), location, Operand_dst, width, CommitRegisters);
      Some(uop_program_build([||], [|operation|], Operand_dst, width, CommitRegisters))
    },
    None() => None(),
  }

function execute_REVBIT(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
  match lower_REVBIT_uops(instruction) {
    Some(program) => Some(uop_program_execute(program, instruction, state)),
    None() => Some(faulted(state, instruction.form.operation, IllegalInstruction,
                           "REVBIT could not be lowered")),
  }
