function execute_setcc(instruction : Decoded_instruction, state : Cpu_state) -> Execution_result =
  match find_operand_by_name("dst", instruction.operands) {
    Some(dst) =>
      if dst.type_name == "Rn" then {
        let selected = predicate_holds(instruction, state);
        let value : bits(64) = if selected then 0x0000000000000001 else 0x0000000000000000;
        var updated = advance_pc(state, instruction);
        let index = unsigned(dst.value[3 .. 0]);
        updated.registers[index] = merge_narrow(state.registers[index], value, operation_width(instruction));
        completed(state, updated, CommitRegisters, [||])
      }
      else match start_memory_transaction(instruction, state) {
        Some(result) => result,
        None() => faulted(state, instruction.form.operation, IllegalInstruction,
                          "missing SETcc memory destination"),
      },
    None() => faulted(state, instruction.form.operation, IllegalInstruction, "SETcc destination"),
  }

function route_environment(instruction : Decoded_instruction, state : Cpu_state,
                           effect_kind : Effect_kind, commit_kind : Commit_kind,
                           suppress_fault : bool) -> Execution_result = {
  let address : bits(64) = match first_ea_operand(instruction.operands) {
    Some(operand) => operand.value,
    None() => 0x0000000000000000,
  };
  let width = operation_width(instruction);
  let operation = instruction.form.operation;
  let kind = if operation == Op_RFENCE | operation == Op_WFENCE | operation == Op_AFENCE
    then FenceCompletion
    else if instruction.form.route == RouteAtomics then AtomicReadModifyWrite
    else if instruction.form.route == RouteCache then
      if operation == Op_PREFETCH | operation == Op_PREFETCHNT then PrefetchHint
      else CacheMaintenanceBlock
    else if instruction.form.route == RouteTlbContext then
      if operation == Op_INVASID | operation == Op_INVPAGE | operation == Op_INVTLB
        then TlbInvalidateRequest
      else if operation == Op_PTQUERY | operation == Op_VTOP then TranslationQueryRequest
      else if operation == Op_SAVE then StateSaveRequest
      else if operation == Op_RESTORE then StateRestoreRequest
      else ContextSwitchRequest
    else if operation == Op_REPcc | operation == Op_REPG then RepeatBodyFetch
    else if operation == Op_CPUID then CpuidQueryRequest
    else if operation == Op_RDPMC then PerformanceCounterRequest
    else if operation == Op_WRCR then ControlTransitionRequest
    else if operation == Op_RESET then ResetSerializeRequest
    else ExternalIntegerRequest;
  let phase = if kind == AtomicReadModifyWrite then PhaseAtomicRmw
    else if kind == CacheMaintenanceBlock | kind == PrefetchHint then PhaseCacheMaintenance
    else if kind == FenceCompletion then PhaseFenceCompletion
    else if kind == TlbInvalidateRequest then PhaseTlbOperation
    else if kind == TranslationQueryRequest then PhaseTranslationQuery
    else if kind == ContextSwitchRequest then PhaseContextSwitch
    else if kind == StateSaveRequest then PhaseStateSave
    else if kind == StateRestoreRequest then PhaseStateRestore
    else if kind == RepeatBodyFetch then PhaseRepeatFetch
    else if kind == CpuidQueryRequest then PhaseCpuidQuery
    else if kind == PerformanceCounterRequest then PhasePerformanceCounter
    else if kind == ControlTransitionRequest then PhaseControlTransition
    else if kind == ResetSerializeRequest then PhaseResetSerialize
    else PhaseIntegerExternal;
  struct {
    state = state,
    pending = { empty_pending(state, advance_pc(state, instruction),
                              instruction.form.operation, commit_kind) with
      destination = commit_destination_for(instruction.operands, width),
      instruction = Some(instruction), phase = phase },
    request = { empty_primitive_request() with
      kind = kind, role = instruction.form.family, width = width,
      access = NoTransactionAccess, commit_point = true, suppress_fault = suppress_fault,
      selector = if operation == Op_RESET then 0x000000000000003F
                 else 0x0000000000000000,
      expected = if operation == Op_RESET then state.controls[23]
                 else 0x0000000000000000,
      state_image = state },
    effects = [|typed_effect(effect_kind, instruction, state, address, 0x0000000000000000,
                            width, 0, suppress_fault)|],
    fault = None(),
    awaiting_environment = true
  }
}

val start_control_transaction : (Decoded_instruction, Cpu_state) -> option(Execution_result)

function execute_count_jump(instruction : Decoded_instruction, state : Cpu_state)
  -> Execution_result = {
  let condition : int = match condition_field(instruction.fields) {
    Some(value) => value, None() => 0
  };
  if instruction.form.operation == Op_DJcc then match operand_named(instruction, "counter") {
    None() => faulted(state, Op_DJcc, IllegalInstruction, "missing DJcc counter"),
    Some(counter_operand) => {
      let index = unsigned(counter_operand.value[3 .. 0]);
      let count = sub_bits(state.registers[index], 0x0000000000000001);
      var staged = state;
      staged.registers[index] = count;
      if count != 0x0000000000000000 & condition_holds(condition, state.flags) then
        match start_control_transaction(instruction, staged) {
          Some(result) => { result with state = state,
            pending = { result.pending with before = state } },
          None() => faulted(state, Op_DJcc, IllegalInstruction, "missing DJcc target"),
        }
      else completed(state, { staged with pc = next_pc(state, instruction) }, CommitControl, [||])
    },
  }
  else match (operand_named(instruction, "index"), operand_named(instruction, "bound")) {
    (Some(index_operand), Some(bound_operand)) => {
      let index = unsigned(index_operand.value[3 .. 0]);
      let bound = unsigned(bound_operand.value[3 .. 0]);
      let index_value = add_bits(state.registers[index], 0x0000000000000001);
      var staged = state;
      staged.registers[index] = index_value;
      if index_value != state.registers[bound] & condition_holds(condition, state.flags) then
        match start_control_transaction(instruction, staged) {
          Some(result) => { result with state = state,
            pending = { result.pending with before = state } },
          None() => faulted(state, Op_IJcc, IllegalInstruction, "missing IJcc target"),
        }
      else completed(state, { staged with pc = next_pc(state, instruction) }, CommitControl, [||])
    },
    _ => faulted(state, Op_IJcc, IllegalInstruction, "missing IJcc operands"),
  }
}

