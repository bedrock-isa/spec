function clause register_result_extension(Op_WRFLAGS) = RegisterZeroExtend

function clause repeat_semantics(Op_WRFLAGS) = RepeatObserveDestination

function lower_WRFLAGS_uops(_ : Decoded_instruction) -> list(Uop) = [|
  uop_make(UopSystemState(SystemWriteFlags), uop_location_make_none(), uop_location_make_none(), uop_location_make_none(), Operand_src, 8, CommitRegisters)
|]

function execute_WRFLAGS(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
  Some(uop_program_execute(lower_WRFLAGS_uops(instruction), instruction, state))
