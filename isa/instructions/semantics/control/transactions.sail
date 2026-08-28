function start_control_transaction(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) = {
  let operation = instruction.form.operation;
  let far_jump = operation == Op_LCALL | operation == Op_LJMP;
  let proposed_cs = if far_jump then match value_named(instruction, state, Operand_new_cs) {
    Some(value) => value, None() => state.segments[0]
  } else state.segments[0];
  if operation == Op_RET | operation == Op_LRET then {
    let bytes = if operation == Op_LRET then 16 else 8;
    let end_address = add_bits(state.sp, get_slice_int(64, bytes, 0));
    var after = state; after.sp = end_address;
    Some(waiting_transaction(
      state, after, instruction, CommitControl, empty_destination(), PhaseStackRange, 0,
      0x0000000000000000, 0x0000000000000000,
      stack_request(StackRange, 0, state, state.sp, end_address, AccessStackRead,
                    0x0000000000000000, false)
    ))
  }
  else {
    let evaluated = evaluate_instruction_eas(
      instruction.operands, instruction.form.operation, state, state.pc, 8
    );
    match evaluation_named(Operand_target, evaluated.evaluations) {
      Some(target_ea) =>
        if target_ea.kind == EaKind_memory then Some(waiting_transaction(
          state, evaluated.image, instruction, CommitControl, empty_destination(), PhaseTargetRead, 0,
          0x0000000000000000, 0x0000000000000000,
          request_for_evaluation(MemoryRead, 0, target_ea, AccessLoad,
                                 0x0000000000000000, false)
        ))
        else if far_jump & not_bool(segment_image_valid(proposed_cs)) then Some(faulted(
          state, operation, InvalidControlState, "invalid target code segment"
        ))
        else {
          let cs_image = proposed_cs;
          Some(waiting_transaction(
            state, evaluated.image, instruction, CommitControl, empty_destination(),
            PhaseTargetExecuteProbe, 0, target_ea.value, cs_image,
            target_probe_request(0, cs_image, target_ea.value)
          ))
        },
      None() => match control_target_local(instruction, state) {
        Some(target) =>
          if far_jump & not_bool(segment_image_valid(proposed_cs)) then Some(faulted(
            state, operation, InvalidControlState, "invalid target code segment"
          ))
          else Some(waiting_transaction(
            state, state, instruction, CommitControl, empty_destination(), PhaseTargetExecuteProbe, 0,
            target, proposed_cs, target_probe_request(0, proposed_cs, target)
          )),
        None() => None(),
      },
    }
  }
}
