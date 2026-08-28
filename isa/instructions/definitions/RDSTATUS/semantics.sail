function clause register_result_extension(Op_RDSTATUS) = RegisterZeroExtend

function clause repeat_semantics(Op_RDSTATUS) = RepeatObserveDestination

function lower_RDSTATUS_uops(_ : Decoded_instruction) -> list(Uop) = [|
  uop_make(UopSystemState(SystemReadStatus), uop_location_make_none(), uop_location_make_none(), uop_location_make_none(), Operand_dst, 8, CommitRegisters)
|]

function execute_RDSTATUS(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
  Some(uop_program_execute(lower_RDSTATUS_uops(instruction), instruction, state))
