function clause register_result_extension(Op_WRSTATUS) = RegisterZeroExtend

function clause repeat_semantics(Op_WRSTATUS) = RepeatObserveDestination

function lower_WRSTATUS_uops(_ : Decoded_instruction) -> list(Uop) = [|
  uop_make(UopSystemState(SystemWriteStatus), uop_location_make_none(), uop_location_make_none(), uop_location_make_none(), Operand_src, 8, CommitRegisters)
|]

function execute_WRSTATUS(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
  Some(uop_program_execute(lower_WRSTATUS_uops(instruction), instruction, state))
