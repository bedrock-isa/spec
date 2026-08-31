function cfi_control_index(selector : int) -> option(int) =
  if selector == 4608 then Some(27)
  else if selector == 4609 then Some(28)
  else if selector == 4610 then Some(29)
  else None()

function cfi_indirect_target(instruction : Decoded_instruction) -> bool =
  match operand_named(instruction, Operand_target) {
    Some(target) =>
      target.operand_type != OperandType_imm8s
      & target.operand_type != OperandType_imm16s
      & target.operand_type != OperandType_imm32s,
    None() => false,
  }

function cfi_call_program(program : list(Uop), instruction : Decoded_instruction,
                          state : Cpu_state) -> list(Uop) = {
  let shadowed = if cfi_shadow_enabled(state)
    then cfi_with_shadow_push(program) else program;
  if cfi_landing_enabled(state) & cfi_indirect_target(instruction)
  then cfi_with_landing_check(shadowed) else shadowed
}

function cfi_jump_program(program : list(Uop), instruction : Decoded_instruction,
                          state : Cpu_state) -> list(Uop) =
  if cfi_landing_enabled(state) & cfi_indirect_target(instruction)
  then cfi_with_landing_check(program) else program

function cfi_return_program(program : list(Uop), state : Cpu_state) -> list(Uop) =
  if cfi_shadow_enabled(state) then cfi_with_shadow_return(program) else program

function cfi_execute_optional_call(program : option(list(Uop)),
                                   instruction : Decoded_instruction,
                                   state : Cpu_state) -> Execution_result =
  match program {
    Some(selected) => uop_program_execute(
      cfi_call_program(selected, instruction, state), instruction, state
    ),
    None() => faulted(
      state, instruction.form.operation, IllegalInstruction,
      "CFI could not lower call operation"
    ),
  }

function cfi_execute_optional_jump(program : option(list(Uop)),
                                   instruction : Decoded_instruction,
                                   state : Cpu_state) -> Execution_result =
  match program {
    Some(selected) => uop_program_execute(
      cfi_jump_program(selected, instruction, state), instruction, state
    ),
    None() => faulted(
      state, instruction.form.operation, IllegalInstruction,
      "CFI could not lower jump operation"
    ),
  }

function cfi_try_read_control(instruction : Decoded_instruction,
                              state : Cpu_state) -> option(Execution_result) =
  match value_named(instruction, state, Operand_cr) {
    None() => None(),
    Some(raw) => match cfi_control_index(unsigned(raw[15 .. 0])) {
      None() => None(),
      Some(index) => Some(read_state_register(
        instruction, state, state.controls[unsigned(get_slice_int(5, index, 0))]
      )),
    },
  }

function cfi_control_write_valid(selector : int, value : bits(64),
                                 candidate : Cpu_state) -> bool =
  if selector == 4608 then
    (value & 0xFFFFFFFFFFFFFFFC) == 0x0000000000000000
    & (value[1] == bitzero | cfi_shadow_push_state_valid(candidate))
  else if selector == 4609 then
    segment_image_valid(value)
    & (not_bool(cfi_shadow_enabled(candidate))
       | cfi_shadow_push_state_valid(candidate))
  else if selector == 4610 then
    (value & 0x000000000000000F) == 0x0000000000000000
    & (not_bool(cfi_shadow_enabled(candidate))
       | cfi_shadow_push_state_valid(candidate))
  else false

function cfi_try_write_control(instruction : Decoded_instruction,
                               state : Cpu_state) -> option(Execution_result) =
  match (value_named(instruction, state, Operand_cr),
         value_named(instruction, state, Operand_src)) {
    (Some(raw), Some(value)) => {
      let selector = unsigned(raw[15 .. 0]);
      match cfi_control_index(selector) {
        None() => None(),
        Some(index) => {
          var candidate = state;
          candidate.controls[unsigned(get_slice_int(5, index, 0))] = value;
          if cfi_control_write_valid(selector, value, candidate) then
            Some(local_result(state, instruction, candidate, CommitControl))
          else Some(faulted(
            state, instruction.form.operation, InvalidControlState,
            "invalid CFI control-register image"
          ))
        },
      }
    },
    _ => None(),
  }

function cpuid_flag_enabled(flag : Cpuid_flag, state : Cpu_state) -> bool =
  if flag == CpuidFlag_CFI then true else base_cpuid_flag_enabled(flag, state)

function execute_operation_entry(instruction : Decoded_instruction, state : Cpu_state)
  -> Execution_result =
  match instruction.form.operation {
    Op_CALL => cfi_execute_optional_call(lower_CALL_uops(instruction), instruction, state),
    Op_CALLcc => cfi_execute_optional_call(lower_CALLcc_uops(instruction), instruction, state),
    Op_LCALL => cfi_execute_optional_call(lower_LCALL_uops(instruction), instruction, state),
    Op_JMP => cfi_execute_optional_jump(lower_JMP_uops(instruction), instruction, state),
    Op_LJMP => cfi_execute_optional_jump(lower_LJMP_uops(instruction), instruction, state),
    Op_IJcc => cfi_execute_optional_jump(lower_IJcc_uops(instruction), instruction, state),
    Op_DJcc => cfi_execute_optional_jump(lower_DJcc_uops(instruction), instruction, state),
    Op_RET => uop_program_execute(
      cfi_return_program(lower_RET_uops(instruction), state), instruction, state
    ),
    Op_LRET => uop_program_execute(
      cfi_return_program(lower_LRET_uops(instruction), state), instruction, state
    ),
    Op_RDCR => match cfi_try_read_control(instruction, state) {
      Some(result) => result,
      None() => execute_base_operation_entry(instruction, state),
    },
    Op_WRCR => match cfi_try_write_control(instruction, state) {
      Some(result) => result,
      None() => execute_base_operation_entry(instruction, state),
    },
    _ => execute_base_operation_entry(instruction, state),
  }

function event_from_fault(result : Execution_result) -> Event_record =
  match result.fault {
    Some(fault) =>
      if fault.kind == CfiViolationFault then {
        var event = make_event(
          EventSynchronous, EventFrameError, 0x00000044, 3, result.state.pc
        );
        event.error_code = fault.error_code;
        event
      }
      else base_event_from_fault(result),
    None() => base_event_from_fault(result),
  }
