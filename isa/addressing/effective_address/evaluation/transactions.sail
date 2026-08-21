function execute_lea_transaction(instruction : Decoded_instruction, state : Cpu_state)
  -> option(Execution_result) = {
  let width = operation_width(instruction);
  let evaluated = evaluate_instruction_eas(
    instruction.operands, instruction.form.operation, state, state.pc, width
  );
  match evaluation_named("src", evaluated.evaluations) {
    None() => None(),
    Some(source) => {
      let destination = commit_destination_for(instruction.operands, 8);
      if instruction.form.operation == Op_SEGLEA then {
        let point = segment_point(source.segment_image, source.effective_address);
        var updated = advance_pc(evaluated.image, instruction);
        if point.in_bounds then {
          updated = write_local_destination(updated, destination, point.linear);
          updated.flags = flags_value(false, false, false, false)
        }
        else updated.flags = flags_value(false, false, false, true);
        Some(completed(state, updated, CommitRegisters, [||]))
      }
      else {
        let updated = write_local_destination(
          advance_pc(evaluated.image, instruction), destination, source.effective_address
        );
        Some(completed(state, updated, CommitRegisters, [||]))
      }
    },
  }
}
