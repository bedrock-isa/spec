function execute_core_exact(instruction : Decoded_instruction, state : Cpu_state)
  -> Execution_result = match instruction.form.operation {
  Op_ILLEGAL => faulted(state, Op_ILLEGAL, IllegalInstruction, "explicit ILLEGAL"),
  Op_HALT => completed(
    state, { advance_pc(state, instruction) with halted = true, run_state = Halted }, CommitControl,
    [|typed_effect(HaltProcessor, instruction, state, 0x0000000000000000,
                   0x0000000000000000, 0, 0, false)|]
  ),
  Op_RESET => route_environment(instruction, state, ResetProcessor, CommitControl, false),
  Op_BKPT => start_event_control(instruction, state),
  Op_ERET => start_event_control(instruction, state),
  Op_SYSCALL => start_event_control(instruction, state),
  Op_NOP => completed(state, advance_pc(state, instruction), CommitControl, [||]),
  Op_WAIT => completed(
    state, advance_pc(state, instruction), CommitControl,
    [|typed_effect(NoEffect, instruction, state, 0x0000000000000000,
                   0x0000000000000000, 0, 0, false)|]
  ),
  Op_YIELD => completed(
    state, advance_pc(state, instruction), CommitControl,
    [|typed_effect(NoEffect, instruction, state, 0x0000000000000000,
                   0x0000000000000000, 0, 0, false)|]
  ),
  Op_RFENCE => route_environment(instruction, state, FenceOperation, CommitControl, false),
  Op_WFENCE => route_environment(instruction, state, FenceOperation, CommitControl, false),
  Op_AFENCE => route_environment(instruction, state, FenceOperation, CommitControl, false),
  _ => faulted(state, instruction.form.operation, IllegalInstruction,
               "unhandled core-control operation"),
}

function execute_control_exact(instruction : Decoded_instruction, state : Cpu_state)
  -> Execution_result = match instruction.form.operation {
  Op_SET => match execute_set_local(instruction, state) {
    Some(result) => result,
    None() => match start_memory_transaction(instruction, state) {
      Some(result) => result,
      None() => route_environment(instruction, state, IntegerCompute, CommitMemory, false),
    },
  },
  Op_MOVcc => match execute_data_local(instruction, state) {
    Some(result) => result,
    None() => match start_memory_transaction(instruction, state) {
      Some(result) => result,
      None() => route_environment(instruction, state, IntegerCompute, CommitMemory, false),
    },
  },
  Op_JMP => match start_control_transaction(instruction, state) {
    Some(result) => result, None() => faulted(state, Op_JMP, IllegalInstruction, "missing JMP target")
  },
  Op_Jcc => match start_control_transaction(instruction, state) {
    Some(result) => result, None() => faulted(state, Op_Jcc, IllegalInstruction, "missing Jcc target")
  },
  Op_CALL => match start_control_transaction(instruction, state) {
    Some(result) => result, None() => faulted(state, Op_CALL, IllegalInstruction, "missing CALL target")
  },
  Op_CALLcc => match start_control_transaction(instruction, state) {
    Some(result) => result, None() => faulted(state, Op_CALLcc, IllegalInstruction, "missing CALLcc target")
  },
  Op_RET => match start_control_transaction(instruction, state) {
    Some(result) => result, None() => faulted(state, Op_RET, IllegalInstruction, "invalid RET form")
  },
  Op_LCALL => match start_control_transaction(instruction, state) {
    Some(result) => result, None() => faulted(state, Op_LCALL, IllegalInstruction, "missing LCALL target")
  },
  Op_LJMP => match start_control_transaction(instruction, state) {
    Some(result) => result, None() => faulted(state, Op_LJMP, IllegalInstruction, "missing LJMP target")
  },
  Op_LRET => match start_control_transaction(instruction, state) {
    Some(result) => result, None() => faulted(state, Op_LRET, IllegalInstruction, "invalid LRET form")
  },
  Op_CMPJcc => match execute_compare_jump_local(instruction, state) {
    Some(result) => result,
    None() => faulted(state, Op_CMPJcc, IllegalInstruction, "CMPJcc local operands"),
  },
  Op_TESTJcc => match execute_compare_jump_local(instruction, state) {
    Some(result) => result,
    None() => faulted(state, Op_TESTJcc, IllegalInstruction, "TESTJcc local operands"),
  },
  Op_DJcc => execute_count_jump(instruction, state),
  Op_IJcc => execute_count_jump(instruction, state),
  Op_REPcc => start_repeat_transaction(instruction, state),
  Op_TRACE => completed(
    state, advance_pc(state, instruction), CommitControl,
    [|typed_effect(TraceMarker, instruction, state, state.pc,
                   match value_named(instruction, state, "marker") {
                     Some(value) => value, None() => 0x0000000000000000
                   }, 2, 0, false)|]
  ),
  _ => faulted(state, instruction.form.operation, IllegalInstruction,
               "unhandled control-flow operation"),
}
