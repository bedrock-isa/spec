function start_cache_transaction(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) = {
  let operation = instruction.form.operation;
  let evaluated = evaluate_instruction_eas(
    instruction.operands, operation, state, state.pc, 8
  );
  match first_evaluation(evaluated.evaluations) {
    None() => None(),
    Some(address) => {
      let prefetch = operation == Op_PREFETCH | operation == Op_PREFETCHNT;
      let request = { request_for_evaluation(
        AddressTranslateRequest,
        0, address, AccessAddressOnly, 0x0000000000000000, false
      ) with role = "cache_translate", suppress_fault = prefetch, selector =
        if operation == Op_FLSHDCACHE then 0x0000000000000000
        else if operation == Op_INVDCACHE then 0x0000000000000001
        else if operation == Op_INVICACHE then 0x0000000000000002
        else if operation == Op_WRBKDCACHE then 0x0000000000000003
        else if operation == Op_SYNCCACHE then 0x0000000000000004
        else if operation == Op_PREFETCHNT then 0x0000000000000006
        else 0x0000000000000005,
        auxiliary = bits_from_int(state.cache_maintenance_granule), state_image = state };
      Some(waiting_transaction(
        state, advance_pc(evaluated.image, instruction), instruction, CommitControl,
        empty_destination(), PhaseCacheTranslate, 0,
        address.effective_address, 0x0000000000000000, request
      ))
    },
  }
}

