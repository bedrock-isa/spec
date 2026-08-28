function clause register_result_extension(Op_INVASID) = RegisterZeroExtend

function clause repeat_semantics(Op_INVASID) = RepeatObserveDestination

function lower_INVASID_uops(_ : Decoded_instruction) -> list(Uop) = [|
  uop_make(UopTlbContext(TlbInvalidateAsid), uop_location_make_none(), uop_location_make_none(), uop_location_make_none(), Operand_dst, 8, CommitControl)
|]

function execute_INVASID(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
  Some(uop_program_execute(lower_INVASID_uops(instruction), instruction, state))
