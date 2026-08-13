function resume_fp_phase(previous : Execution_result, response : Transaction_response)
  -> Execution_result = match previous.pending.phase {
    PhaseFpContractQuery => fp_preserve_repeat_parent(previous, match previous.pending.instruction {
      None() => faulted(previous.pending.before, previous.pending.operation,
                        InvalidControlState, "missing FPTRANSA contract continuation"),
      Some(instruction) => match fp_semantics(instruction.form.operation) {
        None() => faulted(previous.pending.before, instruction.form.operation,
                          InvalidControlState, "missing FPTRANSA semantics"),
        Some(semantics) => {
          let lookup = fptrans_contract_lookup(semantics.contract_id, response.value);
          if not_bool(response.known) | lookup.status == FptransContractUnknown
             | not_bool(response.present) | lookup.status == FptransContractAbsent then
            faulted_with_error_code(
              previous.pending.before, instruction.form.operation,
              IllegalInstruction, "FPTRANSA contract absent or unknown",
              0x0000000000000003
            )
          else if lookup.status == FptransContractMalformed then
            faulted(previous.pending.before, instruction.form.operation,
                    InvalidControlState, "FPTRANSA contract malformed")
          else fp_start_operands(instruction, previous.pending.before, response.value)
        },
      },
    }),
    PhaseFpSourceRead => fp_preserve_repeat_parent(previous, match previous.pending.instruction {
      None() => faulted(previous.pending.before, previous.pending.operation,
                        InvalidControlState, "missing FP source continuation"),
      Some(instruction) => match fp_semantics(instruction.form.operation) {
        None() => faulted(previous.pending.before, instruction.form.operation,
                          InvalidControlState, "missing FP source semantics"),
        Some(semantics) => {
          let source_index = previous.pending.fp_pending.next_source;
          match fp_source_at(instruction.operands, source_index, 0) {
            None() => faulted(previous.pending.before, instruction.form.operation,
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
                None() => faulted(previous.pending.before, instruction.form.operation,
                                  InvalidControlState, "invalid FP source slot"),
                Some(slots) => {
                  let missing = fp_first_missing_source(slots, semantics.source_count, 0);
                  let next_pending = { fp_pending_with_slots(
                    previous.pending.fp_pending, slots
                  ) with next_source = missing };
                  if missing < semantics.source_count then {
                    let evaluated = evaluate_instruction_eas(
                      instruction.operands, instruction.form.operation,
                      previous.pending.before, previous.pending.before.pc,
                      operation_width(instruction)
                    );
                    match fp_source_at(instruction.operands, missing, 0) {
                      Some(next_source) => match evaluation_named(
                        next_source.name, evaluated.evaluations
                      ) {
                        Some(evaluation) => fp_waiting(
                          previous.pending.before, previous.pending.after, instruction,
                          PhaseFpSourceRead, previous.pending.ordinal + 1,
                          request_for_evaluation(
                            MemoryRead, previous.pending.ordinal + 1, evaluation,
                            AccessLoad, 0x0000000000000000, false
                          ), next_pending
                        ),
                        None() => faulted(previous.pending.before,
                                          instruction.form.operation,
                                          InvalidControlState,
                                          "missing next FP source evaluation"),
                      },
                      None() => faulted(previous.pending.before,
                                        instruction.form.operation,
                                        InvalidControlState,
                                        "missing next FP source operand"),
                    }
                  }
                  else fp_continue_after_sources(
                    instruction, previous.pending.before, previous.pending.after,
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
      None() => faulted(previous.pending.before, previous.pending.operation,
                        InvalidControlState, "missing FP destination continuation"),
      Some(instruction) => fp_start_compute(
        instruction, previous.pending.before, previous.pending.after,
        previous.pending.fp_pending, previous.pending.fp_pending.contract_word,
        previous.pending.ordinal + 1
      ),
    }),
    PhaseFpCompute => fp_preserve_repeat_parent(previous, match previous.pending.instruction {
      None() => faulted(previous.pending.before, previous.pending.operation,
                        InvalidControlState, "missing FP compute continuation"),
      Some(instruction) => fp_commit_candidate(
        previous.pending.before, previous.pending.after, instruction,
        fp_finalize_response(previous.request.fp_request, response.fp_response,
                             previous.pending.before.fstatus),
        previous.pending.fp_pending, previous.pending.ordinal + 1
      ),
    }),
    PhaseFpDestinationWrite => completed(
      previous.pending.before, previous.pending.after, CommitMemory, [||]
    ),
    _ => faulted(previous.pending.before, previous.pending.operation,
                 InvalidControlState, "unexpected transaction phase"),
  }
