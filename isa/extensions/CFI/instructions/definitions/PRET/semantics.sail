function clause register_result_extension(Op_PRET) = RegisterZeroExtend

function clause repeat_semantics(Op_PRET) = RepeatObserveDestination

function lower_PRET_uops(state : Cpu_state) -> list(Uop) =
  if link_active(state) then [|
    uop_make(UopCfiKeyGuard(), uop_location_make_none(),
      uop_location_make_none(), uop_location_make_none(), Operand_target,
      0, CommitControl),
    uop_make(UopCfiResidentAuthenticate(), uop_location_make_none(),
      uop_location_make_none(), uop_location_make_temporary(0), Operand_target,
      16, CommitControl),
    uop_make(UopControlProbe(), uop_location_make_temporary(0),
      uop_location_make_segment(0), uop_location_make_none(), Operand_target,
      8, CommitControl),
    uop_make(UopIntegerAdd(), uop_location_make_sp(),
      uop_location_make_immediate(0x0000000000000010),
      uop_location_make_sp(), Operand_target, 8, CommitControl),
    uop_make(UopLinkClear(), uop_location_make_none(),
      uop_location_make_none(), uop_location_make_none(), Operand_target,
      16, CommitControl),
    uop_make(UopControlCommit(ControlReturn), uop_location_make_temporary(0),
      uop_location_make_segment(0), uop_location_make_none(), Operand_target,
      8, CommitControl)
  |] else [|
    uop_make(UopCfiKeyGuard(), uop_location_make_none(),
      uop_location_make_none(), uop_location_make_none(), Operand_target,
      0, CommitControl),
    uop_make(UopStackRange(false), uop_location_make_sp(),
      uop_location_make_none(), uop_location_make_none(), Operand_target,
      16, CommitMemory),
    uop_make(UopCfiRecordLoad(16), uop_location_make_sp(),
      uop_location_make_none(), uop_location_make_temporary(0), Operand_target,
      16, CommitMemory),
    uop_make_pair(UopCfiRecordAuthenticate(false),
      uop_location_make_temporary(0), uop_location_make_none(),
      uop_location_make_temporary(1), uop_location_make_none(),
      Operand_target, 16, CommitControl),
    uop_make(UopControlProbe(), uop_location_make_temporary(1),
      uop_location_make_segment(0), uop_location_make_none(), Operand_target,
      8, CommitControl),
    uop_make(UopIntegerAdd(), uop_location_make_sp(),
      uop_location_make_immediate(0x0000000000000010),
      uop_location_make_sp(), Operand_target, 8, CommitControl),
    uop_make(UopControlCommit(ControlReturn), uop_location_make_temporary(1),
      uop_location_make_segment(0), uop_location_make_none(), Operand_target,
      8, CommitControl)
  |]

function execute_PRET(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) =
  Some(uop_program_execute(lower_PRET_uops(state), instruction, state))
