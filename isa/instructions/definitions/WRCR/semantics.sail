function clause register_result_extension(Op_WRCR) = RegisterZeroExtend

function clause repeat_semantics(Op_WRCR) = RepeatObserveDestination

function lower_WRCR_uops(_ : Decoded_instruction) -> list(Uop) = [|
  uop_make(UopSystemState(SystemWriteControlLocal), uop_location_make_none(), uop_location_make_none(), uop_location_make_none(), Operand_src, 8, CommitControl)
|]

function execute_WRCR(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
  Some(uop_program_execute(lower_WRCR_uops(instruction), instruction, state))
