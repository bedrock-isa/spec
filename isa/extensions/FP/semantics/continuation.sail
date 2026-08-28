function resume_fp_phase(previous : Execution_result, response : Transaction_response)
  -> Execution_result = match previous.pending.phase {
    PhaseFpContractQuery => fp_preserve_repeat_parent(previous, match previous.pending.instruction {
      None() => faulted(previous.state, previous.pending.operation,
                        InvalidControlState, "missing FP approximation contract continuation"),
      Some(instruction) => match fp_semantics(instruction.form.operation) {
        None() => faulted(previous.state, instruction.form.operation,
                          InvalidControlState, "missing FP approximation semantics"),
        Some(semantics) => {
          let lookup = fp_approx_contract_lookup(semantics.contract_id, response.value);
          if not_bool(response.known) | lookup.status == FpApproxContractUnknown
             | not_bool(response.present) | lookup.status == FpApproxContractAbsent then
            faulted_with_error_code(
              previous.state, instruction.form.operation,
              IllegalInstruction, "FP approximation contract absent or unknown",
              0x0000000000000003
            )
          else if lookup.status == FpApproxContractMalformed then
            faulted(previous.state, instruction.form.operation,
                    InvalidControlState, "FP approximation contract malformed")
          else fp_start_operands(instruction, previous.state, response.value)
        },
      },
    }),
    PhaseFpSourceRead => fp_preserve_repeat_parent(previous, match previous.pending.instruction {
      None() => faulted(previous.state, previous.pending.operation,
                        InvalidControlState, "missing FP source continuation"),
      Some(instruction) => match fp_semantics(instruction.form.operation) {
        None() => faulted(previous.state, instruction.form.operation,
                          InvalidControlState, "missing FP source semantics"),
        Some(semantics) => {
          let source_index = previous.pending.fp_pending.next_source;
          match fp_source_at(instruction.operands, source_index, 0) {
            None() => faulted(previous.state, instruction.form.operation,
                              InvalidControlState, "missing FP source operand"),
            Some(source) => {
              let captured_kind = fp_operand_kind_for(
                instruction, source, operation_width(instruction)
              );
              let captured : Fp_operand_image = struct {
                valid = true,
                kind = captured_kind,
                bits = if captured_kind == FpBits32
                  then 0x00000000 @ response.value[31 .. 0] else response.value
              };
              match fp_operand_slot_set(
                fp_pending_raw_slots(previous.pending.fp_pending),
                source_index, captured
              ) {
                None() => faulted(previous.state, instruction.form.operation,
                                  InvalidControlState, "invalid FP source slot"),
                Some(slots) => {
                  let missing = fp_first_missing_source(slots, semantics.source_count, 0);
                  let next_pending = { fp_pending_with_slots(
                    previous.pending.fp_pending, slots
                  ) with next_source = missing };
                  if missing < semantics.source_count then {
                    let evaluated = evaluate_instruction_eas(
                      instruction.operands, instruction.form.operation,
                      previous.state, previous.state.pc,
                      operation_width(instruction)
                    );
                    match fp_source_at(instruction.operands, missing, 0) {
                      Some(next_source) => match evaluation_named(
                        next_source.name, evaluated.evaluations
                      ) {
                        Some(evaluation) => fp_waiting(
                          previous.state, pending_after(previous), instruction,
                          PhaseFpSourceRead, previous.pending.ordinal + 1,
                          request_for_evaluation(
                            MemoryRead, previous.pending.ordinal + 1, evaluation,
                            AccessLoad, 0x0000000000000000, false
                          ), next_pending
                        ),
                        None() => faulted(previous.state,
                                          instruction.form.operation,
                                          InvalidControlState,
                                          "missing next FP source evaluation"),
                      },
                      None() => faulted(previous.state,
                                        instruction.form.operation,
                                        InvalidControlState,
                                        "missing next FP source operand"),
                    }
                  }
                  else fp_continue_after_sources(
                    instruction, previous.state, pending_after(previous),
                    next_pending, previous.pending.fp_pending.contract_word,
                    previous.pending.ordinal + 1
                  )
                },
              }
            },
          }
        },
      },
    }),
    PhaseFpDestinationProbe => fp_preserve_repeat_parent(previous, match previous.pending.instruction {
      None() => faulted(previous.state, previous.pending.operation,
                        InvalidControlState, "missing FP destination continuation"),
      Some(instruction) => fp_start_compute(
        instruction, previous.state, pending_after(previous),
        previous.pending.fp_pending, previous.pending.fp_pending.contract_word,
        previous.pending.ordinal + 1
      ),
    }),
    PhaseFpDestinationWrite => completed(
      previous.state, pending_after(previous), CommitMemory, [||]
    ),
    _ => faulted(previous.state, previous.pending.operation,
                 InvalidControlState, "unexpected transaction phase"),
  }
