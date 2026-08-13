function resume_memory_phase(previous : Execution_result, response : Transaction_response)
  -> Execution_result = match previous.pending.phase {
    PhaseSourceRead => match previous.pending.instruction {
      None() => faulted(previous.pending.before, previous.pending.operation,
                        InvalidControlState, "missing continuation instruction"),
      Some(instruction) => {
        let width = operation_width(instruction);
        let evaluated = evaluate_instruction_eas(
          instruction.operands, instruction.form.operation,
          previous.pending.before, previous.pending.before.pc, width
        );
        match memory_evaluation_for(instruction.operands, evaluated.evaluations, false) {
          None() => {
            let source_name = evaluation_option_name(memory_evaluation_for(
              instruction.operands, evaluated.evaluations, true
            ));
            match next_memory_source(instruction.operands, evaluated.evaluations, source_name) {
              Some(second_source) => continue_with_request(
                previous, PhaseDestinationProbe, previous.pending.ordinal + 1,
                response.value, 0x0000000000000000,
                request_for_evaluation(
                  MemoryRead, previous.pending.ordinal + 1, second_source,
                  AccessLoad, 0x0000000000000000, false
                )
              ),
              None() => match execute_resolved_operands(
                instruction, evaluated.image, source_name, response.value,
                "", 0x0000000000000000
              ) {
                Some(resolved) => completed(
                  previous.pending.before, resolved.state, CommitRegisters, [||]
                ),
                None() => faulted(
                  previous.pending.before, instruction.form.operation,
                  IllegalInstruction, "unresolved memory semantic continuation"
                ),
              },
            }
          },
          Some(destination) => {
            let source = memory_evaluation_for(instruction.operands, evaluated.evaluations, true);
            let same_operand = evaluation_option_named(source, destination.operand_name);
            if same_operand & instruction.form.operation == Op_XCHG then
              match next_memory_source(
                instruction.operands, evaluated.evaluations, destination.operand_name
              ) {
                Some(second_source) => continue_with_request(
                  previous, PhaseDestinationProbe, 1, response.value,
                  0x0000000000000000,
                  request_for_evaluation(
                    MemoryRead, 1, second_source, AccessLoad,
                    0x0000000000000000, false
                  )
                ),
                None() => match execute_resolved_operands(
                  instruction, evaluated.image, destination.operand_name, response.value,
                  "", 0x0000000000000000
                ) {
                  None() => faulted(
                    previous.pending.before, Op_XCHG, IllegalInstruction,
                    "unresolved register-memory XCHG continuation"
                  ),
                  Some(resolved) => {
                    let staged = { previous with pending = {
                      previous.pending with after = resolved.state
                    } };
                    continue_with_request(
                      staged, PhaseDestinationWrite, 1,
                      resolved.destination_value, response.value,
                      request_for_evaluation(
                        MemoryStore, 1, destination, AccessStore,
                        resolved.destination_value, true
                      )
                    )
                  },
                },
              }
            else if same_operand then {
              match execute_resolved_operands(
                instruction, evaluated.image, destination.operand_name, response.value,
                "", 0x0000000000000000
              ) {
                None() => faulted(
                  previous.pending.before, instruction.form.operation,
                  IllegalInstruction, "unresolved read-modify-write semantic continuation"
                ),
                Some(resolved) => {
                  let staged = { previous with pending = {
                    previous.pending with after = resolved.state
                  } };
                  continue_with_request(
                    staged, PhaseDestinationWrite, 1,
                    resolved.destination_value, response.value,
                    request_for_evaluation(
                      MemoryStore, 1, destination, AccessStore,
                      resolved.destination_value, true
                    )
                  )
                },
              }
            }
            else continue_with_request(
              previous, PhaseDestinationProbe, 1, response.value, 0x0000000000000000,
              request_for_evaluation(
                if operand_access_named(destination.operand_name, instruction.operands) == AccessReadWrite
                then MemoryRead else MemoryProbe,
                1, destination,
                if operand_access_named(destination.operand_name, instruction.operands) == AccessReadWrite
                then AccessLoad else AccessStore,
                                     0x0000000000000000, false)
            )
          },
        }
      },
    },
    PhaseDestinationProbe => match previous.pending.instruction {
      None() => faulted(previous.pending.before, previous.pending.operation,
                        InvalidControlState, "missing destination continuation"),
      Some(instruction) => {
        let width = operation_width(instruction);
        let evaluated = evaluate_instruction_eas(
          instruction.operands, instruction.form.operation,
          previous.pending.before, previous.pending.before.pc, width
        );
        match memory_evaluation_for(instruction.operands, evaluated.evaluations, false) {
          None() => {
            let first_source = memory_evaluation_for(
              instruction.operands, evaluated.evaluations, true
            );
            let first_name = evaluation_option_name(first_source);
            match next_memory_source(instruction.operands, evaluated.evaluations, first_name) {
              None() => faulted(previous.pending.before, previous.pending.operation,
                                InvalidControlState, "missing second memory source"),
              Some(second_source) => match execute_resolved_operands(
                instruction, evaluated.image, first_name, previous.pending.captured_first,
                second_source.operand_name, response.value
              ) {
                Some(resolved) => completed(
                  previous.pending.before, resolved.state, CommitRegisters, [||]
                ),
                None() => faulted(
                  previous.pending.before, previous.pending.operation,
                  IllegalInstruction, "unresolved two-source memory continuation"
                ),
              },
            }
          },
          Some(destination) => {
            if instruction.form.operation == Op_XCHG then {
              let first_source = memory_evaluation_for(
                instruction.operands, evaluated.evaluations, true
              );
              match first_source {
                None() => faulted(
                  previous.pending.before, Op_XCHG, InvalidControlState,
                  "missing first XCHG operand"
                ),
                Some(first) => continue_with_request(
                  previous, PhaseMemoryWriteFirst, previous.pending.ordinal + 1,
                  previous.pending.captured_first, response.value,
                  request_for_evaluation(
                    MemoryStore, previous.pending.ordinal + 1, first,
                    AccessStore, response.value, false
                  )
                ),
              }
            }
            else {
            let source_name = evaluation_option_name(memory_evaluation_for(
              instruction.operands, evaluated.evaluations, true
            ));
            match execute_resolved_operands(
              instruction, evaluated.image, source_name, previous.pending.captured_first,
              destination.operand_name, response.value
            ) {
              None() => faulted(
                previous.pending.before, instruction.form.operation,
                IllegalInstruction, "unresolved memory-to-memory semantic continuation"
              ),
              Some(resolved) => {
                let staged = { previous with pending = {
                  previous.pending with after = resolved.state
                } };
                continue_with_request(
                  staged, PhaseDestinationWrite, previous.pending.ordinal + 1,
                  resolved.destination_value, response.value,
                  request_for_evaluation(
                    MemoryStore, previous.pending.ordinal + 1, destination,
                    AccessStore, resolved.destination_value, true
                  )
                )
              },
            }
            }
          },
        }
      },
    },
    PhaseDestinationWrite => completed(
      previous.pending.before, previous.pending.after, previous.pending.kind, [||]
    ),
    PhaseMemoryWriteFirst => match previous.pending.instruction {
      None() => faulted(previous.pending.before, previous.pending.operation,
                        InvalidControlState, "missing compound memory continuation"),
      Some(instruction) => {
        let evaluated = evaluate_instruction_eas(
          instruction.operands, instruction.form.operation,
          previous.pending.before, previous.pending.before.pc,
          operation_width(instruction)
        );
        let first_name = evaluation_option_name(memory_evaluation_for(
          instruction.operands, evaluated.evaluations, true
        ));
        match next_memory_source(instruction.operands, evaluated.evaluations, first_name) {
          None() => faulted(previous.pending.before, previous.pending.operation,
                            InvalidControlState, "missing compound memory destination"),
          Some(second) => continue_with_request(
            previous, PhaseMemoryWriteSecond, previous.pending.ordinal + 1,
            previous.pending.captured_first, previous.pending.captured_second,
            request_for_evaluation(
              MemoryStore, previous.pending.ordinal + 1, second,
              AccessStore, previous.pending.captured_first, true
            )
          ),
        }
      },
    },
    PhaseMemoryWriteSecond => completed(
      previous.pending.before, previous.pending.after, CommitMemory, [||]
    ),
    PhaseAtomicRmw => match previous.pending.instruction {
      None() => faulted(previous.pending.before, previous.pending.operation,
                        InvalidControlState, "missing atomic continuation"),
      Some(instruction) => {
        let width = operation_width(instruction);
        let equal = narrow_bits(response.value, width)
                  == narrow_bits(previous.pending.captured_first, width);
        if instruction.form.operation == Op_CMPXCHG
           & response.atomic_store_happened != equal then
          faulted(previous.pending.before, Op_CMPXCHG, InvalidControlState,
                  "inconsistent CMPXCHG atomic acknowledgement")
        else if instruction.form.operation != Op_CMPXCHG
                & not_bool(response.atomic_store_happened) then
          faulted(previous.pending.before, instruction.form.operation, InvalidControlState,
                  "atomic operation did not acknowledge its store")
        else {
        var updated = previous.pending.after;
        let destination = previous.pending.destination;
        if destination.kind == "Rn" then {
          let index = unsigned(destination.index);
          updated.registers[index] = merge_narrow(
            updated.registers[index], response.value, width
          )
        } else ();
        if instruction.form.operation == Op_CMPXCHG then
          updated.flags = flags_value(equal, false, false, false)
        else ();
        completed(previous.pending.before, updated, CommitMemory, [||])
        }
      },
    },
    _ => faulted(previous.pending.before, previous.pending.operation,
                 InvalidControlState, "unexpected transaction phase"),
  }
