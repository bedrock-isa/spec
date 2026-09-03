function clause register_result_extension(Op_PLRET) = RegisterZeroExtend

function clause repeat_semantics(Op_PLRET) = RepeatObserveDestination

function lower_PLRET_uops(_ : Decoded_instruction) -> list(Uop) = [|
  uop_make(UopCfiKeyGuard(), uop_location_make_none(),
    uop_location_make_none(), uop_location_make_none(), Operand_target,
    0, CommitControl),
  uop_make(UopLinkInactiveGuard(), uop_location_make_none(),
    uop_location_make_none(), uop_location_make_none(), Operand_target,
    0, CommitControl),
  uop_make(UopStackRange(false), uop_location_make_sp(),
    uop_location_make_none(), uop_location_make_none(), Operand_target,
    24, CommitMemory),
  uop_make(UopCfiRecordLoad(24), uop_location_make_sp(),
    uop_location_make_none(), uop_location_make_temporary(0), Operand_target,
    24, CommitMemory),
  uop_make_pair(UopCfiRecordAuthenticate(true),
    uop_location_make_temporary(0), uop_location_make_none(),
    uop_location_make_temporary(1), uop_location_make_temporary(2),
    Operand_target, 24, CommitControl),
  uop_make(UopControlProbe(), uop_location_make_temporary(1),
    uop_location_make_temporary(2), uop_location_make_none(), Operand_target,
    8, CommitControl),
  uop_make(UopIntegerAdd(), uop_location_make_sp(),
    uop_location_make_immediate(0x0000000000000018),
    uop_location_make_sp(), Operand_target, 8, CommitControl),
  uop_make(UopControlCommit(ControlFarReturn),
    uop_location_make_temporary(1), uop_location_make_temporary(2),
    uop_location_make_none(), Operand_target, 8, CommitControl)
|]

function execute_PLRET(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) =
  Some(uop_program_execute(lower_PLRET_uops(instruction), instruction, state))
