function clause register_result_extension(Op_WFENCE) = RegisterZeroExtend

function clause repeat_semantics(Op_WFENCE) = RepeatObserveDestination

function lower_WFENCE_uops(_ : Decoded_instruction) -> list(Uop) = {
  let operation : Environment_uop_operation = struct {
    family = TransactionSystem,
    request_kind = FenceCompletion,
    effect_kind = FenceOperation,
    commit_kind = CommitControl,
    suppress_fault = false
  };
  [|uop_make(UopEnvironment(operation), uop_location_make_none(), uop_location_make_none(), uop_location_make_none(),
             Operand_dst, 0, CommitControl)|]
}

function execute_WFENCE(instruction : Decoded_instruction, state : Cpu_state) -> option(Execution_result) =
  Some(uop_program_execute(lower_WFENCE_uops(instruction), instruction, state))
