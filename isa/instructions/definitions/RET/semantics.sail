function clause register_result_extension(Op_RET) = RegisterZeroExtend

function clause repeat_semantics(Op_RET) = RepeatObserveDestination

function lower_RET_uops(_ : Decoded_instruction, state : Cpu_state) -> list(Uop) =
  if link_active(state) then resident_RET_uops(state) else [|
    uop_make(UopStackRange(false), uop_location_make_sp(), uop_location_make_none(), uop_location_make_none(), Operand_target, 8, CommitMemory),
    uop_make(UopStackLoad(0), uop_location_make_sp(), uop_location_make_none(), uop_location_make_temporary(0), Operand_target, 8, CommitMemory),
    uop_make(UopIntegerAdd(), uop_location_make_sp(), uop_location_make_immediate(0x0000000000000008), uop_location_make_sp(), Operand_target, 8, CommitControl),
    uop_make(UopControlProbe(), uop_location_make_temporary(0), uop_location_make_segment(0), uop_location_make_none(), Operand_target, 8, CommitControl),
    uop_make(UopControlCommit(ControlReturn), uop_location_make_temporary(0), uop_location_make_segment(0), uop_location_make_none(), Operand_target, 8, CommitControl)
  |]

function execute_RET(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
  Some(uop_program_execute(lower_RET_uops(instruction, state), instruction, state))
