function clause register_result_extension(Op_XCHG) = RegisterZeroExtend

function clause repeat_semantics(Op_XCHG) = RepeatObserveDestination

function lower_XCHG_uops(instruction : Decoded_instruction) -> option(list(Uop)) =
  match (operand_named(instruction, Operand_lhs), operand_named(instruction, Operand_rhs)) {
    (Some(lhs_operand), Some(rhs_operand)) => {
      let width = operation_width(instruction);
      let lhs = uop_operand_lower(lhs_operand, width, 0, true);
      let rhs = uop_operand_lower(rhs_operand, width, lhs.next_temporary, true);
      let lhs_store = if lhs.memory then [|uop_make(UopMemoryStore(), lhs.value,
        lhs.address, uop_location_make_none(), Operand_lhs, width, CommitMemory)|] else [||];
      let rhs_store = if rhs.memory then [|uop_make(UopMemoryStore(), rhs.value,
        rhs.address, uop_location_make_none(), Operand_rhs, width, CommitMemory)|] else [||];
      let exchange = uop_make_pair(UopRegisterPairMove(), rhs.value, lhs.value,
        lhs.value, rhs.value, Operand_lhs, width, CommitRegisters);
      Some(uop_program_build(uop_program_append(lhs.program, rhs.program),
        exchange :: uop_program_append(lhs_store, rhs_store), Operand_lhs, width,
        if lhs.memory | rhs.memory then CommitMemory else CommitRegisters))
    }, _ => None(),
  }

function execute_XCHG(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
  match lower_XCHG_uops(instruction) {
    Some(program) => Some(uop_program_execute(program, instruction, state)),
    None() => Some(faulted(state, instruction.form.operation, IllegalInstruction, "XCHG could not be lowered")),
  }
