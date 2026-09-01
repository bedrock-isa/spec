function zero_registers() -> Registers = [
  0x0000000000000000, 0x0000000000000000, 0x0000000000000000, 0x0000000000000000,
  0x0000000000000000, 0x0000000000000000, 0x0000000000000000, 0x0000000000000000,
  0x0000000000000000, 0x0000000000000000, 0x0000000000000000, 0x0000000000000000,
  0x0000000000000000, 0x0000000000000000, 0x0000000000000000, 0x0000000000000000
]

function zero_floating_registers() -> Floating_registers = [
  0x0000000000000000, 0x0000000000000000, 0x0000000000000000, 0x0000000000000000,
  0x0000000000000000, 0x0000000000000000, 0x0000000000000000, 0x0000000000000000,
  0x0000000000000000, 0x0000000000000000, 0x0000000000000000, 0x0000000000000000,
  0x0000000000000000, 0x0000000000000000, 0x0000000000000000, 0x0000000000000000
]

function zero_vector_bytes(count : int) -> list(bits(8)) =
  if count <= 0 then [||] else 0x00 :: zero_vector_bytes(count - 1)

function zero_vector_registers(bytes : int) -> Vector_registers = [
  zero_vector_bytes(bytes), zero_vector_bytes(bytes), zero_vector_bytes(bytes), zero_vector_bytes(bytes),
  zero_vector_bytes(bytes), zero_vector_bytes(bytes), zero_vector_bytes(bytes), zero_vector_bytes(bytes),
  zero_vector_bytes(bytes), zero_vector_bytes(bytes), zero_vector_bytes(bytes), zero_vector_bytes(bytes),
  zero_vector_bytes(bytes), zero_vector_bytes(bytes), zero_vector_bytes(bytes), zero_vector_bytes(bytes),
  zero_vector_bytes(bytes), zero_vector_bytes(bytes), zero_vector_bytes(bytes), zero_vector_bytes(bytes),
  zero_vector_bytes(bytes), zero_vector_bytes(bytes), zero_vector_bytes(bytes), zero_vector_bytes(bytes),
  zero_vector_bytes(bytes), zero_vector_bytes(bytes), zero_vector_bytes(bytes), zero_vector_bytes(bytes),
  zero_vector_bytes(bytes), zero_vector_bytes(bytes), zero_vector_bytes(bytes), zero_vector_bytes(bytes)
]

function zero_predicate_registers(bytes : int) -> Predicate_registers = [
  zero_vector_bytes(tdiv_int(bytes, 8)), zero_vector_bytes(tdiv_int(bytes, 8)),
  zero_vector_bytes(tdiv_int(bytes, 8)), zero_vector_bytes(tdiv_int(bytes, 8)),
  zero_vector_bytes(tdiv_int(bytes, 8)), zero_vector_bytes(tdiv_int(bytes, 8)),
  zero_vector_bytes(tdiv_int(bytes, 8)), zero_vector_bytes(tdiv_int(bytes, 8)),
  zero_vector_bytes(tdiv_int(bytes, 8)), zero_vector_bytes(tdiv_int(bytes, 8)),
  zero_vector_bytes(tdiv_int(bytes, 8)), zero_vector_bytes(tdiv_int(bytes, 8)),
  zero_vector_bytes(tdiv_int(bytes, 8)), zero_vector_bytes(tdiv_int(bytes, 8)),
  zero_vector_bytes(tdiv_int(bytes, 8)), zero_vector_bytes(tdiv_int(bytes, 8))
]

function zero_segments() -> Segment_registers = [
  0x0000000000000000, 0x0000000000000000, 0x0000000000000000, 0x0000000000000000,
  0x0000000000000000, 0x0000000000000000, 0x0000000000000000, 0x0000000000000000,
  0x0000000000000000
]

function initial_cpu() -> Cpu_state = struct {
  registers = zero_registers(),
  floating_registers = zero_floating_registers(),
  vector_registers = zero_vector_registers(16),
  predicate_registers = zero_predicate_registers(16),
  segments = zero_segments(),
  controls = initial_control_state(),
  sp = 0x0000000000000000,
  pc = 0x0000000000000000,
  flags = 0x0,
  status = 0x0000000000000000,
  fflags = 0b00000,
  fstatus = 0x0000000000000000,
  supervisor = false,
  base_instruction_features = 0x0000000000000000,
  fp_enabled = false,
  fp16_convert_enabled = false,
  fptrans_enabled = false,
  vector_enabled = true,
  wait_enabled = false,
  vector_length_bytes = 16,
  halted = false,
  run_state = Running,
  current_dfa = false,
  cache_maintenance_granule = 0x0000000000000040,
  save_area_size = 960,
  save_fixed_size = 192,
  save_format = 0x0,
  save_bitmap_words = 0x0000000000000001,
  fp_component_present = true,
  fp_component_id = 0x0000000000000001,
  fp_component_bitmap_bit = 0x0000000000000000,
  fp_component_offset = 192,
  fp_component_size = 192,
  fp_component_alignment = 0x0000000000000040,
  fp_component_init_policy = 0x0000000000000001,
  fp_component_modified = false,
  vector_component_present = true,
  vector_component_id = 0x0000000000000002,
  vector_component_bitmap_bit = 0x0000000000000001,
  vector_component_offset = 384,
  vector_component_size = 576,
  vector_component_alignment = 0x0000000000000040,
  vector_component_init_policy = 0x0000000000000001,
  vector_component_modified = false,
  repeat_state = struct {
    active = false, counter = 0x0, remaining = 0x0000000000000000,
    condition = 0x0, prefix_start = 0x0000000000000000,
    body_start = 0x0000000000000000, fixed_body = [||]
  },
  nmi_latched_source = 0x000000,
  nmi_relatched = false,
  nmi_relatched_source = 0x000000,
  machine_check_pending = false,
  machine_check_payload = 0x00000000,
  machine_check_error_code = 0x0000000000000000,
  machine_check_fault_ea = 0x0000000000000000,
  machine_check_fault_linear = 0x0000000000000000,
  machine_check_event_aux = 0x0000000000000000
}

function next_pc(state : Cpu_state, instruction : Decoded_instruction) -> bits(64) =
  add_bits(state.pc, get_slice_int(64, instruction.encoded_length, 0))

function status_event_depth(status : bits(64)) -> int = unsigned(status[9 .. 6])

function status_user_origin(status : bits(64)) -> bool = status[10] == bitone

function status_with_event_state(status : bits(64), depth : int, user_origin : bool)
  -> bits(64) =
  (status & 0xFFFFFFFFFFFFF83F)
  | sail_shiftleft(get_slice_int(64, depth, 0), 6)
  | (if user_origin then 0x0000000000000400 else 0x0000000000000000)

function advance_pc(state : Cpu_state, instruction : Decoded_instruction) -> Cpu_state =
  { state with pc = next_pc(state, instruction) }
