function clause register_result_extension(Op_INVTLB) = RegisterZeroExtend

function clause repeat_semantics(Op_INVTLB) = RepeatObserveDestination

function lower_INVTLB_uops(_ : Decoded_instruction) -> list(Uop) = [|
  uop_make(UopTlbContext(TlbInvalidateAll), uop_location_make_none(), uop_location_make_none(), uop_location_make_none(), Operand_dst, 8, CommitControl)
|]

function execute_INVTLB(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
  Some(uop_program_execute(lower_INVTLB_uops(instruction), instruction, state))
