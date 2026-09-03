function clause register_result_extension(Op_LRET) = RegisterZeroExtend

function clause repeat_semantics(Op_LRET) = RepeatObserveDestination

function lower_LRET_uops(_ : Decoded_instruction) -> list(Uop) = [|
  uop_make(UopLinkInactiveGuard(), uop_location_make_none(), uop_location_make_none(), uop_location_make_none(), Operand_target, 0, CommitControl),
  uop_make(UopStackRange(false), uop_location_make_sp(), uop_location_make_none(), uop_location_make_none(), Operand_target, 16, CommitMemory),
  uop_make(UopStackLoad(0), uop_location_make_sp(), uop_location_make_none(), uop_location_make_temporary(0), Operand_target, 8, CommitMemory),
  uop_make(UopStackLoad(8), uop_location_make_sp(), uop_location_make_none(), uop_location_make_temporary(1), Operand_new_cs, 8, CommitMemory),
  uop_make(UopIntegerAdd(), uop_location_make_sp(), uop_location_make_immediate(0x0000000000000010), uop_location_make_sp(), Operand_target, 8, CommitControl),
  uop_make(UopControlProbe(), uop_location_make_temporary(0), uop_location_make_temporary(1), uop_location_make_none(), Operand_target, 8, CommitControl),
  uop_make(UopControlCommit(ControlFarReturn), uop_location_make_temporary(0), uop_location_make_temporary(1), uop_location_make_none(), Operand_target, 8, CommitControl)
|]

function execute_LRET(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
  Some(uop_program_execute(lower_LRET_uops(instruction), instruction, state))
