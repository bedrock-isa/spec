function resume_control_phase(previous : Execution_result, response : Transaction_response)
  -> Execution_result = match previous.pending.phase {
    PhaseTargetRead => match previous.pending.instruction {
      None() => faulted(previous.pending.before, previous.pending.operation,
                        InvalidControlState, "missing target continuation"),
      Some(instruction) => {
        let cs_image = if instruction.form.operation == Op_LCALL | instruction.form.operation == Op_LJMP
          then match value_named(instruction, previous.pending.before, "new_cs") {
            Some(value) => value, None() => previous.pending.before.segments[0]
          } else previous.pending.before.segments[0];
        if not_bool(segment_image_valid(cs_image)) then faulted(
          previous.pending.before, instruction.form.operation,
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
      None() => faulted(previous.pending.before, previous.pending.operation,
                        InvalidControlState, "missing control continuation"),
      Some(instruction) => {
        let operation = instruction.form.operation;
        if operation == Op_CALL | operation == Op_CALLcc | operation == Op_LCALL then {
          let far = operation == Op_LCALL;
          let bytes = if far then 16 else 8;
          let stack_start = sub_bits(previous.pending.before.sp, get_slice_int(64, bytes, 0));
          var after = previous.pending.after;
          after.sp = stack_start; after.pc = previous.pending.captured_first;
          if far then after.segments[0] = previous.pending.captured_second else ();
          let staged = { previous with pending = { previous.pending with after = after } };
          continue_with_request(
            staged, PhaseStackRange, previous.pending.ordinal + 1,
            previous.pending.captured_first, previous.pending.captured_second,
            stack_request(StackRange, previous.pending.ordinal + 1, previous.pending.before,
                          stack_start, previous.pending.before.sp, AccessStackWrite,
                          0x0000000000000000, false)
          )
        }
        else {
          var updated = previous.pending.after;
          updated.pc = previous.pending.captured_first;
          if operation == Op_LJMP | operation == Op_LRET then
            updated.segments[0] = previous.pending.captured_second
          else ();
          completed(previous.pending.before, updated, CommitControl, [||])
        }
      },
    },
    PhaseStackRange => match previous.pending.instruction {
      None() => faulted(previous.pending.before, previous.pending.operation,
                        InvalidControlState, "missing stack continuation"),
      Some(instruction) => {
        let operation = instruction.form.operation;
        let ordinal = previous.pending.ordinal + 1;
        if operation == Op_PUSH then continue_with_request(
          previous, PhaseStackWriteFirst, ordinal,
          previous.pending.captured_first, previous.pending.captured_second,
          stack_request(MemoryStore, ordinal, previous.pending.before,
                        sub_bits(previous.pending.before.sp, 0x0000000000000008),
                        previous.pending.before.sp, AccessStackWrite,
                        previous.pending.captured_first, true)
        )
        else if operation == Op_PUSHP | operation == Op_FPUSHP then continue_with_request(
          previous, PhaseStackWriteFirst, ordinal,
          previous.pending.captured_first, previous.pending.captured_second,
          compound_stack_store(
            ordinal, previous.pending.before,
            sub_bits(previous.pending.before.sp, 0x0000000000000010),
            previous.pending.captured_second, previous.pending.captured_first
          )
        )
        else if operation == Op_CALL | operation == Op_CALLcc then continue_with_request(
          previous, PhaseStackWriteFirst, ordinal,
          previous.pending.captured_first, previous.pending.captured_second,
          stack_request(MemoryStore, ordinal, previous.pending.before,
                        sub_bits(previous.pending.before.sp, 0x0000000000000008),
                        previous.pending.before.sp, AccessStackWrite,
                        next_pc(previous.pending.before, instruction), true)
        )
        else if operation == Op_LCALL then continue_with_request(
          previous, PhaseStackWriteFirst, ordinal,
          next_pc(previous.pending.before, instruction), previous.pending.before.segments[0],
          compound_stack_store(
            ordinal, previous.pending.before,
            sub_bits(previous.pending.before.sp, 0x0000000000000010),
            next_pc(previous.pending.before, instruction), previous.pending.before.segments[0]
          )
        )
        else continue_with_request(
          previous, PhaseStackReadFirst, ordinal,
          0x0000000000000000, 0x0000000000000000,
          stack_request(MemoryRead, ordinal, previous.pending.before,
                        previous.pending.before.sp,
                        add_bits(previous.pending.before.sp, 0x0000000000000008),
                        AccessStackRead, 0x0000000000000000, false)
        )
      },
    },
    PhaseStackWriteFirst => completed(
      previous.pending.before, previous.pending.after, previous.pending.kind, [||]
    ),
    PhaseStackReadFirst => match previous.pending.instruction {
      None() => faulted(previous.pending.before, previous.pending.operation,
                        InvalidControlState, "missing stack read"),
      Some(instruction) => {
        let operation = instruction.form.operation;
        let ordinal = previous.pending.ordinal + 1;
        if operation == Op_POP then {
          var updated = previous.pending.after;
          match operand_named(instruction, "reg") {
            Some(reg) =>
              if reg.type_name == "SREG" then {
                let index = unsigned(reg.value[2 .. 0]) + 1;
                if segment_image_valid(response.value) then updated.segments[index] = response.value
                else return faulted(previous.pending.before, operation,
                                    InvalidControlState, "invalid popped segment")
              }
              else {
                let index = unsigned(reg.value[3 .. 0]); updated.registers[index] = response.value
              },
            None() => (),
          };
          completed(previous.pending.before, updated, CommitRegisters, [||])
        }
        else if operation == Op_RET then continue_with_request(
          previous, PhaseTargetExecuteProbe, ordinal, response.value,
          previous.pending.before.segments[0],
          target_probe_request(ordinal, previous.pending.before.segments[0], response.value)
        )
        else continue_with_request(
          previous, PhaseStackReadSecond, ordinal, response.value,
          0x0000000000000000,
          stack_request(MemoryRead, ordinal, previous.pending.before,
                        add_bits(previous.pending.before.sp, 0x0000000000000008),
                        add_bits(previous.pending.before.sp, 0x0000000000000010),
                        AccessStackRead, 0x0000000000000000, false)
        )
      },
    },
    PhaseStackReadSecond => match previous.pending.instruction {
      None() => faulted(previous.pending.before, previous.pending.operation,
                        InvalidControlState, "missing paired stack read"),
      Some(instruction) =>
        if instruction.form.operation == Op_LRET then
          if not_bool(segment_image_valid(response.value)) then faulted(
            previous.pending.before, Op_LRET, InvalidControlState, "invalid return code segment"
          )
          else continue_with_request(
            previous, PhaseTargetExecuteProbe, previous.pending.ordinal + 1,
            previous.pending.captured_first, response.value,
            target_probe_request(previous.pending.ordinal + 1, response.value,
                                 previous.pending.captured_first)
          )
        else {
          var updated = previous.pending.after;
          match operand_named(instruction, "pair_id") {
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
          completed(previous.pending.before, updated, CommitRegisters, [||])
        },
    },
    PhaseCpuidQuery => commit_response_destination(
      previous, if response.known then response.value else 0x0000000000000000,
      { response with write_flags = false, generated_fflags = 0b00000,
                      state_image = initial_cpu() }
    ),
    PhasePerformanceCounter =>
      if previous.request.selector == 0x0000000000000000
         | not_bool(response.known) | not_bool(response.present) then
        faulted(previous.pending.before, Op_RDPMC, InvalidControlState,
                "RDPMC counter is absent or selector zero")
      else commit_response_destination(
        previous, response.value,
        { response with write_flags = false, generated_fflags = 0b00000,
                        state_image = initial_cpu() }
      ),
    PhaseControlTransition => match previous.pending.instruction {
      None() => faulted(previous.pending.before, previous.pending.operation,
                        InvalidControlState, "missing control-register continuation"),
      Some(instruction) =>
        if instruction.form.operation == Op_ERET
        then completed(
          previous.pending.before, previous.pending.after, CommitControl, [||]
        )
        else match control_index(unsigned(previous.pending.captured_first[15 .. 0])) {
        None() => faulted(previous.pending.before, Op_WRCR,
                          InvalidControlState, "unknown control-register selector"),
        Some(index) => {
          var updated = previous.pending.after;
          updated.controls[unsigned(index)] = previous.pending.captured_second;
          completed(previous.pending.before, updated, CommitControl, [||])
        },
        },
    },
    PhaseResetSerialize => completed(
      previous.pending.before, warm_reset_state(previous.pending.before), CommitControl, [||]
    ),
    PhaseIntegerExternal => commit_response_destination(previous, response.value, response),
    _ => faulted(previous.pending.before, previous.pending.operation,
                 InvalidControlState, "unexpected transaction phase"),
  }
