type Registers = vector(16, inc, bits(64))

type Floating_registers = vector(16, inc, bits(64))
type Vector_registers = vector(32, inc, list(bits(8)))
type Predicate_registers = vector(16, inc, list(bits(8)))
type Segment_registers = vector(9, inc, bits(64))

enum Run_state = Running | Halted | Shutdown
struct Repeat_state = {
  active : bool,
  counter : bits(4),
  remaining : bits(64),
  condition : bits(4),
  prefix_start : bits(64),
  body_start : bits(64),
  fixed_body : list(bits(8)),
}

struct Cpu_state = {
  registers : Registers,
  floating_registers : Floating_registers,
  vector_registers : Vector_registers,
  predicate_registers : Predicate_registers,
  segments : Segment_registers,
  controls : Control_state,
  time : Time_state,
  sp : bits(64),
  pc : bits(64),
  lpc : bits(64),
  lpa : bits(64),
  lkl : bits(64),
  lkh : bits(64),
  flags : bits(4),
  status : bits(64),
  fflags : bits(5),
  fstatus : bits(64),
  vstatus : bits(64),
  supervisor : bool,
  base_instruction_features : bits(64),
  fp_enabled : bool,
  fp16_convert_enabled : bool,
  fptrans_enabled : bool,
  vector_enabled : bool,
  wait_enabled : bool,
  max_vector_length_bytes : int,
  halted : bool,
  run_state : Run_state,
  current_dfa : bool,
  cache_maintenance_granule : bits(64),
  fp_state_modified : bool,
  vector_state_modified : bool,
  repeat_state : Repeat_state,
  nmi_latched_source : bits(24),
  nmi_relatched : bool,
  nmi_relatched_source : bits(24),
  machine_check_pending : bool,
  machine_check_payload : bits(32),
  machine_check_error_code : bits(64),
  machine_check_fault_ea : bits(64),
  machine_check_fault_linear : bits(64),
  machine_check_event_aux : bits(64),
}
