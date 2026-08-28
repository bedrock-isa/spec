function clause register_result_extension(Op_SETF) = RegisterZeroExtend

function clause repeat_semantics(Op_SETF) = RepeatObserveDestination

function lower_SETF_uops(_ : Decoded_instruction) -> list(Uop) = [|
  uop_make(UopSystemState(SystemSetFlags), uop_location_make_none(), uop_location_make_none(), uop_location_make_none(), Operand_mask, 8, CommitRegisters)
|]

function execute_SETF(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
  Some(uop_program_execute(lower_SETF_uops(instruction), instruction, state))
