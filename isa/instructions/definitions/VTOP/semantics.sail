function clause register_result_extension(Op_VTOP) = RegisterZeroExtend

function clause repeat_semantics(Op_VTOP) = RepeatObserveDestination

function lower_VTOP_uops(_ : Decoded_instruction) -> list(Uop) = [|
  uop_make(UopTlbContext(TlbVirtualToPhysical), uop_location_make_none(), uop_location_make_none(), uop_location_make_none(), Operand_phys, 8, CommitControl)
|]

function execute_VTOP(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
  Some(uop_program_execute(lower_VTOP_uops(instruction), instruction, state))
