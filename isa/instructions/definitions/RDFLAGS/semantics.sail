function clause register_result_extension(Op_RDFLAGS) = RegisterZeroExtend

function clause repeat_semantics(Op_RDFLAGS) = RepeatObserveDestination

function lower_RDFLAGS_uops(_ : Decoded_instruction) -> list(Uop) = [|
  uop_make(UopSystemState(SystemReadFlags), uop_location_make_none(), uop_location_make_none(), uop_location_make_none(), Operand_dst, 8, CommitRegisters)
|]

function execute_RDFLAGS(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
  Some(uop_program_execute(lower_RDFLAGS_uops(instruction), instruction, state))
