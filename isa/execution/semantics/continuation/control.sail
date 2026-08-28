function resume_control_phase(previous : Execution_result, response : Transaction_response)
  -> Execution_result = match previous.pending.phase {
    PhaseTargetRead => match previous.pending.instruction {
      None() => faulted(previous.state, previous.pending.operation,
                        InvalidControlState, "missing target continuation"),
      Some(instruction) => {
        let cs_image = if instruction.form.operation == Op_LCALL | instruction.form.operation == Op_LJMP
          then match value_named(instruction, previous.state, Operand_new_cs) {
            Some(value) => value, None() => previous.state.segments[0]
          } else previous.state.segments[0];
        if not_bool(segment_image_valid(cs_image)) then faulted(
          previous.state, instruction.form.operation,
          InvalidControlState, "invalid target code segment"
        )
        else continue_with_request(
          previous, PhaseTargetExecuteProbe, previous.pending.ordinal + 1,
          response.value, cs_image,
          target_probe_request(previous.pending.ordinal + 1, cs_image, response.value)
        )
      },
    },
    PhaseTargetExecuteProbe => match previous.pending.instruction {
      None() => faulted(previous.state, previous.pending.operation,
                        InvalidControlState, "missing control continuation"),
      Some(instruction) => {
        let operation = instruction.form.operation;
        if operation == Op_CALL | operation == Op_CALLcc | operation == Op_LCALL then {
          let far = operation == Op_LCALL;
          let bytes = if far then 16 else 8;
          let stack_start = sub_bits(previous.state.sp, get_slice_int(64, bytes, 0));
          var after = pending_after(previous);
          after.sp = stack_start; after.pc = previous.pending.captured_first;
          if far then after.segments[0] = previous.pending.captured_second else ();
          let staged = { previous with pending = { previous.pending with after = Some(after) } };
          continue_with_request(
            staged, PhaseStackRange, previous.pending.ordinal + 1,
            previous.pending.captured_first, previous.pending.captured_second,
            stack_request(StackRange, previous.pending.ordinal + 1, previous.state,
                          stack_start, previous.state.sp, AccessStackWrite,
                          0x0000000000000000, false)
          )
        }
        else {
          var updated = pending_after(previous);
          updated.pc = previous.pending.captured_first;
          if operation == Op_LJMP | operation == Op_LRET then
            updated.segments[0] = previous.pending.captured_second
          else ();
          completed(previous.state, updated, CommitControl, [||])
        }
      },
    },
    PhaseStackRange => match previous.pending.instruction {
      None() => faulted(previous.state, previous.pending.operation,
                        InvalidControlState, "missing stack continuation"),
      Some(instruction) => {
        let operation = instruction.form.operation;
        let ordinal = previous.pending.ordinal + 1;
        if operation == Op_PUSH then continue_with_request(
          previous, PhaseStackWriteFirst, ordinal,
          previous.pending.captured_first, previous.pending.captured_second,
          stack_request(MemoryStore, ordinal, previous.state,
                        sub_bits(previous.state.sp, 0x0000000000000008),
                        previous.state.sp, AccessStackWrite,
                        previous.pending.captured_first, true)
        )
        else if operation == Op_PUSHP | operation == Op_FPUSHP then continue_with_request(
          previous, PhaseStackWriteFirst, ordinal,
          previous.pending.captured_first, previous.pending.captured_second,
          compound_stack_store(
            ordinal, previous.state,
            sub_bits(previous.state.sp, 0x0000000000000010),
            previous.pending.captured_second, previous.pending.captured_first
          )
        )
        else if operation == Op_CALL | operation == Op_CALLcc then continue_with_request(
          previous, PhaseStackWriteFirst, ordinal,
          previous.pending.captured_first, previous.pending.captured_second,
          stack_request(MemoryStore, ordinal, previous.state,
                        sub_bits(previous.state.sp, 0x0000000000000008),
                        previous.state.sp, AccessStackWrite,
                        next_pc(previous.state, instruction), true)
        )
        else if operation == Op_LCALL then continue_with_request(
          previous, PhaseStackWriteFirst, ordinal,
          next_pc(previous.state, instruction), previous.state.segments[0],
          compound_stack_store(
            ordinal, previous.state,
            sub_bits(previous.state.sp, 0x0000000000000010),
            next_pc(previous.state, instruction), previous.state.segments[0]
          )
        )
        else continue_with_request(
          previous, PhaseStackReadFirst, ordinal,
          0x0000000000000000, 0x0000000000000000,
          stack_request(MemoryRead, ordinal, previous.state,
                        previous.state.sp,
                        add_bits(previous.state.sp, 0x0000000000000008),
                        AccessStackRead, 0x0000000000000000, false)
        )
      },
    },
    PhaseStackWriteFirst => completed(
      previous.state, pending_after(previous), previous.pending.kind, [||]
    ),
    PhaseStackReadFirst => match previous.pending.instruction {
      None() => faulted(previous.state, previous.pending.operation,
                        InvalidControlState, "missing stack read"),
      Some(instruction) => {
        let operation = instruction.form.operation;
        let ordinal = previous.pending.ordinal + 1;
        if operation == Op_POP then {
          var updated = pending_after(previous);
          match operand_named(instruction, Operand_reg) {
            Some(reg) =>
              if reg.operand_type == OperandType_SREG then {
                let index = unsigned(reg.value[2 .. 0]) + 1;
                if segment_image_valid(response.value) then updated.segments[index] = response.value
                else return faulted(previous.state, operation,
                                    InvalidControlState, "invalid popped segment")
              }
              else {
                let index = unsigned(reg.value[3 .. 0]); updated.registers[index] = response.value
              },
            None() => (),
          };
          completed(previous.state, updated, CommitRegisters, [||])
        }
        else if operation == Op_RET then continue_with_request(
          previous, PhaseTargetExecuteProbe, ordinal, response.value,
          previous.state.segments[0],
          target_probe_request(ordinal, previous.state.segments[0], response.value)
        )
        else continue_with_request(
          previous, PhaseStackReadSecond, ordinal, response.value,
          0x0000000000000000,
          stack_request(MemoryRead, ordinal, previous.state,
                        add_bits(previous.state.sp, 0x0000000000000008),
                        add_bits(previous.state.sp, 0x0000000000000010),
                        AccessStackRead, 0x0000000000000000, false)
        )
      },
    },
    PhaseStackReadSecond => match previous.pending.instruction {
      None() => faulted(previous.state, previous.pending.operation,
                        InvalidControlState, "missing paired stack read"),
      Some(instruction) =>
        if instruction.form.operation == Op_LRET then
          if not_bool(segment_image_valid(response.value)) then faulted(
            previous.state, Op_LRET, InvalidControlState, "invalid return code segment"
          )
          else continue_with_request(
            previous, PhaseTargetExecuteProbe, previous.pending.ordinal + 1,
            previous.pending.captured_first, response.value,
            target_probe_request(previous.pending.ordinal + 1, response.value,
                                 previous.pending.captured_first)
          )
        else {
          var updated = pending_after(previous);
          match operand_named(instruction, Operand_pair_id) {
            Some(pair) => {
              let first = pair_first_index(unsigned(pair.value[2 .. 0]));
              let first_index = unsigned(get_slice_int(4, first, 0));
              let second_index = unsigned(get_slice_int(4, first + 1, 0));
              if instruction.form.operation == Op_FPOPP then {
                updated.floating_registers[first_index] = response.value;
                updated.floating_registers[second_index] = previous.pending.captured_first;
                updated.fp_component_modified = true
              }
              else {
                updated.registers[first_index] = response.value;
                updated.registers[second_index] = previous.pending.captured_first
              }
            },
            None() => (),
          };
          completed(previous.state, updated, CommitRegisters, [||])
        },
    },
    PhaseCpuidQuery => commit_response_destination(
      previous, if response.known then response.value else 0x0000000000000000,
      { response with write_flags = false, generated_fflags = 0b00000 }
    ),
    PhasePerformanceCounter =>
      if previous.request.selector == 0x0000000000000000
         | not_bool(response.known) | not_bool(response.present) then
        faulted(previous.state, Op_RDPMC, InvalidControlState,
                "RDPMC counter is absent or selector zero")
      else commit_response_destination(
        previous, response.value,
        { response with write_flags = false, generated_fflags = 0b00000 }
      ),
    PhaseControlTransition => match previous.pending.instruction {
      None() => faulted(previous.state, previous.pending.operation,
                        InvalidControlState, "missing control-register continuation"),
      Some(instruction) =>
        if instruction.form.operation == Op_ERET
        then completed(
          previous.state, pending_after(previous), CommitControl, [||]
        )
        else match control_index(unsigned(previous.pending.captured_first[15 .. 0])) {
        None() => faulted(previous.state, Op_WRCR,
                          InvalidControlState, "unknown control-register selector"),
        Some(index) => {
          var updated = pending_after(previous);
          updated.controls[unsigned(index)] = previous.pending.captured_second;
          completed(previous.state, updated, CommitControl, [||])
        },
        },
    },
    PhaseResetSerialize => completed(
      previous.state, warm_reset_state(previous.state), CommitControl, [||]
    ),
    PhaseIntegerExternal => commit_response_destination(previous, response.value, response),
    _ => faulted(previous.state, previous.pending.operation,
                 InvalidControlState, "unexpected transaction phase"),
  }
