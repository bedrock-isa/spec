function clause register_result_extension(Op_RDCR) = RegisterZeroExtend

function clause repeat_semantics(Op_RDCR) = RepeatObserveDestination

function lower_RDCR_uops(_ : Decoded_instruction) -> list(Uop) = [|
  uop_make(UopSystemState(SystemReadControl), uop_location_make_none(), uop_location_make_none(), uop_location_make_none(), Operand_dst, 8, CommitRegisters)
|]

function execute_RDCR(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
  Some(uop_program_execute(lower_RDCR_uops(instruction), instruction, state))
