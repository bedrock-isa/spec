function clause register_result_extension(Op_PTQUERY) = RegisterZeroExtend

function clause repeat_semantics(Op_PTQUERY) = RepeatObserveDestination

function lower_PTQUERY_uops(_ : Decoded_instruction) -> list(Uop) = [|
  uop_make(UopTlbContext(TlbPageTableQuery), uop_location_make_none(), uop_location_make_none(), uop_location_make_none(), Operand_dst, 8, CommitControl)
|]

function execute_PTQUERY(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
  Some(uop_program_execute(lower_PTQUERY_uops(instruction), instruction, state))
