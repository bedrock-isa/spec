function clause register_result_extension(Op_REPcc) = RegisterZeroExtend

function clause repeat_semantics(Op_REPcc) = RepeatObserveDestination

function lower_REPcc_uops(_ : Decoded_instruction) -> list(Uop) = [|
  uop_make(UopRepeat(), uop_location_make_none(), uop_location_make_none(), uop_location_make_none(), Operand_counter, 0, CommitControl)
|]

function execute_REPcc(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
  Some(uop_program_execute(lower_REPcc_uops(instruction), instruction, state))
