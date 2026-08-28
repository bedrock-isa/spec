function clause register_result_extension(Op_INVPAGE) = RegisterZeroExtend

function clause repeat_semantics(Op_INVPAGE) = RepeatObserveDestination

function lower_INVPAGE_uops(_ : Decoded_instruction) -> list(Uop) = [|
  uop_make(UopTlbContext(TlbInvalidatePage), uop_location_make_none(), uop_location_make_none(), uop_location_make_none(), Operand_dst, 8, CommitControl)
|]

function execute_INVPAGE(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
  Some(uop_program_execute(lower_INVPAGE_uops(instruction), instruction, state))
