function clause register_result_extension(Op_RESET) = RegisterZeroExtend

function clause repeat_semantics(Op_RESET) = RepeatObserveDestination

function lower_RESET_uops(_ : Decoded_instruction) -> list(Uop) = {
  let operation : Environment_uop_operation = struct {
    family = TransactionControl,
    request_kind = ResetSerializeRequest,
    effect_kind = ResetProcessor,
    commit_kind = CommitControl,
    suppress_fault = false
  };
  [|uop_make(UopEnvironment(operation), uop_location_make_none(), uop_location_make_none(), uop_location_make_none(),
             Operand_dst, 0, CommitControl)|]
}

function execute_RESET(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
  Some(uop_program_execute(lower_RESET_uops(instruction), instruction, state))
