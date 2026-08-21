val fp_start_compute : (Decoded_instruction, Cpu_state, Cpu_state,
                        Fp_pending_image, bits(64), int) -> Execution_result

function fp_commit_candidate(before : Cpu_state, after : Cpu_state,
                             instruction : Decoded_instruction,
                             candidate : Fp_candidate_result,
                             fp_pending : Fp_pending_image,
                             ordinal : int) -> Execution_result =
  if not_bool(candidate.shape_valid) then faulted(
    before, instruction.form.operation, InvalidControlState,
    "invalid floating-point response shape or echo"
  )
  else if candidate.trap then
    fp_fault_with_causes(before, instruction.form.operation, candidate.trap_errors)
  else {
    var updated = after;
    updated.fflags = updated.fflags | candidate.generated_causes;
    updated.flags = (updated.flags & not_vec(candidate.flags_mask))
                  | (candidate.flags_value & candidate.flags_mask);
    let destination_kind = fp_derive_destination_kind(instruction.form);
    if destination_kind == FpDestinationFn then match fp_writable_fn_at(
      instruction.operands, 0, 0
    ) {
      Some(destination) => {
        let index = unsigned(destination.value[3 .. 0]);
        updated.floating_registers[index] = if candidate.result_kind == FpResultBits32
          then 0x00000000 @ candidate.primary[31 .. 0] else candidate.primary;
        updated.fp_component_modified = true
      },
      None() => return faulted(before, instruction.form.operation,
                               InvalidControlState, "missing FP destination"),
    }
    else if destination_kind == FpDestinationFnPair then match (
      fp_writable_fn_at(instruction.operands, 0, 0),
      fp_writable_fn_at(instruction.operands, 1, 0)
    ) {
      (Some(first), Some(second)) => {
        updated.floating_registers[unsigned(first.value[3 .. 0])] =
          if candidate.result_kind == FpResultPair32
          then 0x00000000 @ candidate.primary[31 .. 0] else candidate.primary;
        updated.floating_registers[unsigned(second.value[3 .. 0])] =
          if candidate.result_kind == FpResultPair32
          then 0x00000000 @ candidate.secondary[31 .. 0] else candidate.secondary;
        updated.fp_component_modified = true
      },
      _ => return faulted(before, instruction.form.operation,
                          InvalidControlState, "missing FP pair destination"),
    }
    else if destination_kind == FpDestinationRn then match operand_named(instruction, "dst") {
      Some(destination) => updated.registers[unsigned(destination.value[3 .. 0])]
                         = candidate.primary,
      None() => return faulted(before, instruction.form.operation,
                               InvalidControlState, "missing integer FP destination"),
    }
    else ();
    if candidate.generated_causes != 0b00000 then updated.fp_component_modified = true else ();
    if destination_kind == FpDestinationMemory then {
      let evaluated = evaluate_instruction_eas(
        instruction.operands, instruction.form.operation, before, before.pc,
        operation_width(instruction)
      );
      match memory_evaluation_for(instruction.operands, evaluated.evaluations, false) {
        None() => faulted(before, instruction.form.operation, InvalidControlState,
                          "missing FP memory destination"),
        Some(destination) => {
          let staged_pending = { fp_pending with
            candidate0 = candidate.primary, candidate1 = candidate.secondary,
            candidate_flags = candidate.flags_value,
            candidate_causes = candidate.generated_causes };
          fp_waiting(
            before, updated, instruction, PhaseFpDestinationWrite, ordinal,
            request_for_evaluation(MemoryStore, ordinal, destination, AccessStore,
                                   candidate.primary, true), staged_pending
          )
        },
      }
    }
    else completed(before, updated, CommitRegisters, [||])
  }

function fp_start_compute(instruction : Decoded_instruction, before : Cpu_state,
                          after : Cpu_state, fp_pending : Fp_pending_image,
                          contract_word : bits(64), ordinal : int) -> Execution_result =
  match (fp_form_path(instruction.form),
         fp_derive_result_kind(instruction.form, operation_width(instruction))) {
    (Some(path), Some(result_kind)) => match fp_build_request(
      instruction.form.operation, instruction.form, path, result_kind,
      operation_width(instruction),
      fp_pending_raw_slots(fp_pending), before.fstatus, contract_word
    ) {
      None() => faulted(before, instruction.form.operation, InvalidControlState,
                        "invalid floating-point request image"),
      Some(request_image) => {
        let prepared_pending = { fp_pending with
          effective0 = request_image.operand0, effective1 = request_image.operand1,
          effective2 = request_image.operand2, result_kind = result_kind,
          flags_mask = request_image.flags_mask, contract_id = request_image.contract_id,
          contract_word = request_image.contract_word };
        let selector : bits(64) = match operand_named(instruction, "constant_id") {
          Some(value) => value.value, None() => 0x0000000000000000,
        };
        match fp_local_response(request_image, selector) {
          Some(local_response) => fp_commit_candidate(
            before, after, instruction,
            fp_finalize_response(request_image, local_response, before.fstatus),
            prepared_pending, ordinal
          ),
          None() => fp_waiting(
            before, after, instruction, PhaseFpCompute, ordinal,
            { empty_primitive_request() with
              kind = FloatingPointRequest, ordinal = ordinal,
              role = "floating_point_compute", width = operation_width(instruction),
              commit_point = false, fp_request = request_image,
              state_image = before }, prepared_pending
          ),
        }
      },
    },
    _ => faulted(before, instruction.form.operation, InvalidControlState,
                 "missing floating-point form semantics"),
  }

function fp_continue_after_sources(instruction : Decoded_instruction,
                                   before : Cpu_state, after : Cpu_state,
                                   fp_pending : Fp_pending_image,
                                   contract_word : bits(64), ordinal : int)
  -> Execution_result = {
  let evaluated = evaluate_instruction_eas(
    instruction.operands, instruction.form.operation, before, before.pc,
    operation_width(instruction)
  );
  match memory_evaluation_for(instruction.operands, evaluated.evaluations, false) {
    Some(destination) => fp_waiting(
      before, after, instruction, PhaseFpDestinationProbe, ordinal,
      request_for_evaluation(MemoryProbe, ordinal, destination, AccessStore,
                             0x0000000000000000, false), fp_pending
    ),
    None() => fp_start_compute(
      instruction, before, after, fp_pending, contract_word, ordinal
    ),
  }
}
