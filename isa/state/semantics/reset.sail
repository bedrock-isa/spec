function warm_reset_state(state : Cpu_state) -> Cpu_state = {
  var reset = initial_cpu();
  reset.base_instruction_features = state.base_instruction_features;
  reset.fp_enabled = state.fp_enabled;
  reset.fp16_convert_enabled = state.fp16_convert_enabled;
  reset.fptrans_enabled = state.fptrans_enabled;
  reset.vector_enabled = state.vector_enabled;
  reset.wait_enabled = state.wait_enabled;
  reset.max_vector_length_bytes = state.max_vector_length_bytes;
  reset.vector_registers = zero_vector_registers(state.max_vector_length_bytes);
  reset.predicate_registers = zero_predicate_registers(state.max_vector_length_bytes);
  reset.cache_maintenance_granule = state.cache_maintenance_granule;
  reset.controls.interrupt_file.max_id = state.controls.interrupt_file.max_id;
  reset.time.value = state.time.value;
  reset.time.ticks_per_second = state.time.ticks_per_second;
  reset = control_register_with_value(
    reset, ControlRegister_BASE_BOOTPC,
    control_register_value(state, ControlRegister_BASE_BOOTPC));
  reset = control_register_with_value(
    reset, ControlRegister_BASE_BOOTCFG,
    control_register_value(state, ControlRegister_BASE_BOOTCFG));
  reset.pc = control_register_value(state, ControlRegister_BASE_BOOTPC);
  reset.status = 0x0000000000000010;
  reset.supervisor = true;
  reset.halted = false;
  reset.run_state = Running;
  reset
}
