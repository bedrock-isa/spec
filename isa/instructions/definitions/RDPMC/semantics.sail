function clause register_result_extension(Op_RDPMC) = RegisterZeroExtend

function clause repeat_semantics(Op_RDPMC) = RepeatObserveDestination

function lower_RDPMC_uops(_ : Decoded_instruction) -> list(Uop) = [|
  uop_make(UopSystemRequest(SystemPerformanceCounter), uop_location_make_none(), uop_location_make_none(), uop_location_make_none(), Operand_dst, 8, CommitControl)
|]

function execute_RDPMC(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
  Some(uop_program_execute(lower_RDPMC_uops(instruction), instruction, state))
