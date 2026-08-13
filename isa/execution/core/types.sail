type Floating_registers = vector(16, inc, bits(64))
type Segment_registers = vector(9, inc, bits(64))
type Control_registers = vector(32, inc, bits(64))

enum Run_state = Running | Halted | Shutdown

enum Event_kind = EventNone | EventSynchronous | EventDebugTrace | EventNmi | EventInterrupt

enum Event_frame_type = EventFrameBasic | EventFrameError | EventFramePage | EventFrameAuxiliary

enum Boundary_class = BoundaryOrdinary | BoundaryRepeatIteration | BoundaryRepeatGroup
                    | BoundaryRepeatInterior | BoundaryEventEntry

struct Event_record = {
  kind : Event_kind,
  frame_type : Event_frame_type,
  code : bits(32),
  priority : int,
  saved_pc : bits(64),
  error_code : bits(64),
  fault_ea : bits(64),
  fault_linear : bits(64),
  event_aux : bits(64),
}

struct Async_ingress = {
  machine_check_pending : bool,
  machine_check_code : bits(32),
  machine_check_error_code : bits(64),
  machine_check_fault_ea : bits(64),
  machine_check_fault_linear : bits(64),
  machine_check_event_aux : bits(64),
  nmi_pending : bool,
  nmi_source : bits(24),
  interrupt_pending : bool,
  interrupt_id : bits(24),
}

struct Repeat_state = {
  active : bool,
  grouped : bool,
  counter : bits(4),
  remaining : bits(64),
  condition : bits(4),
  body_bytes : bits(16),
  body_start : bits(64),
  fixed_body : list(bits(8)),
  group_progress : int,
}

struct Cpu_state = {
  registers : Registers,
  floating_registers : Floating_registers,
  segments : Segment_registers,
  controls : Control_registers,
  sp : bits(64),
  pc : bits(64),
  flags : bits(4),
  status : bits(64),
  fflags : bits(5),
  fstatus : bits(64),
  supervisor : bool,
  fp_enabled : bool,
  fptrans_enabled : bool,
  halted : bool,
  run_state : Run_state,
  event_depth : int,
  event_stack_level : int,
  cache_maintenance_granule : int,
  save_area_size : int,
  save_fixed_size : int,
  save_format : bits(4),
  save_bitmap_words : int,
  fp_component_present : bool,
  fp_component_id : int,
  fp_component_bitmap_bit : int,
  fp_component_offset : int,
  fp_component_size : int,
  fp_component_alignment : int,
  fp_component_init_policy : int,
  fp_component_modified : bool,
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

struct Architectural_effect = {
  kind : Effect_kind,
  operation : Semantic_operation,
  form_id : string,
  operands : list(Decoded_operand),
  pc : bits(64),
  status : bits(64),
  flags : bits(4),
  fstatus : bits(64),
  fflags : bits(5),
  address : bits(64),
  value : bits(64),
  width : int,
  order : int,
  suppress_fault : bool,
}

enum Primitive_request_kind =
  NoPrimitiveRequest
| TranslationExecuteProbe
| MemoryProbe
| MemoryRead
| MemoryStore
| CompoundMemoryStore
| NonTemporalStore
| StackRange
| SegmentBoundsPoint
| AtomicReadModifyWrite
| AddressTranslateRequest
| PhysicalPteRead
| CacheMaintenanceBlock
| PrefetchHint
| FenceCompletion
| TlbInvalidateRequest
| TranslationQueryRequest
| ContextSwitchRequest
| StateSaveRequest
| StateRestoreRequest
| RepeatBodyFetch
| EventFrameAccess
| CpuidQueryRequest
| PerformanceCounterRequest
| ControlTransitionRequest
| ResetSerializeRequest
| FloatingPointRequest
| ExternalIntegerRequest

enum Transaction_access =
  NoTransactionAccess
| AccessLoad
| AccessStore
| AccessReadModifyWrite
| AccessExecute
| AccessStackRead
| AccessStackWrite
| AccessAddressOnly

enum Continuation_phase =
  ContinuationNone
| PhaseSourceAddress
| PhaseSourceRead
| PhaseDestinationAddress
| PhaseDestinationProbe
| PhaseDestinationWrite
| PhaseMemoryWriteFirst
| PhaseMemoryWriteSecond
| PhaseTargetRead
| PhaseTargetExecuteProbe
| PhaseStackRange
| PhaseStackReadFirst
| PhaseStackReadSecond
| PhaseStackWriteFirst
| PhaseIntegerExternal
| PhaseAtomicRmw
| PhaseCacheTranslate
| PhaseCacheMaintenance
| PhaseFenceCompletion
| PhaseTlbOperation
| PhaseTranslationQuery
| PhasePteRead
| PhaseContextSwitch
| PhaseStateSave
| PhaseStateRestoreHeader
| PhaseStateRestoreRange
| PhaseStateRestore
| PhaseRepeatFetch
| PhaseEventFrameHeader
| PhaseEventFrame
| PhaseEventTargetProbe
| PhaseEventStackProbe
| PhaseEventFrameStore
| PhaseEventReturnBody
| PhaseEventReturnExecute
| PhaseFpContractQuery
| PhaseFpSourceRead
| PhaseFpDestinationProbe
| PhaseFpCompute
| PhaseFpDestinationWrite
| PhaseCpuidQuery
| PhasePerformanceCounter
| PhaseControlTransition
| PhaseResetSerialize

enum Transaction_response_kind =
  ResponseTranslation
| ResponseProbe
| ResponseRead
| ResponseStoreAck
| ResponseStackRange
| ResponseSegmentBounds
| ResponseIntegerExternal
| ResponseAtomic
| ResponseAddressTranslation
| ResponsePteRead
| ResponseCacheMaintenance
| ResponseFenceCompletion
| ResponseTlbOperation
| ResponseTranslationQuery
| ResponseContextSwitch
| ResponseStateSave
| ResponseStateRestore
| ResponseRepeatFetch
| ResponseEventFrame
| ResponseFloatingPoint
| ResponseCpuidQuery
| ResponsePerformanceCounter
| ResponseControlTransition
| ResponseResetSerialize

struct Staged_register_update = {
  index : bits(4),
  value : bits(64),
}

struct Memory_write = {
  linear_address : bits(64),
  effective_address : bits(64),
  segment : int,
  width : int,
  value : bits(64),
  slot : int,
}

struct Ea_evaluation = {
  operand_name : string,
  kind : string,
  role : string,
  domain : string,
  segment : int,
  segment_image : bits(64),
  width : int,
  effective_address : bits(64),
  linear_address : bits(64),
  value : bits(64),
  staged_updates : list(Staged_register_update),
}

struct Ea_evaluation_set = {
  evaluations : list(Ea_evaluation),
  image : Cpu_state,
}

struct Primitive_request = {
  kind : Primitive_request_kind,
  ordinal : int,
  role : string,
  domain : string,
  segment : int,
  segment_image : bits(64),
  width : int,
  range_start : bits(64),
  range_end : bits(64),
  range_length : int,
  range_wrap : bool,
  range_end_at_modulus : bool,
  effective_address : bits(64),
  linear_address : bits(64),
  access : Transaction_access,
  value : bits(64),
  address_translation : bool,
  commit_point : bool,
  memory_order : int,
  address_type : int,
  cache_policy : int,
  suppress_fault : bool,
  staged_updates : list(Staged_register_update),
  selector : bits(64),
  expected : bits(64),
  desired : bits(64),
  auxiliary : bits(64),
  body_length : int,
  payload_bytes : list(bits(8)),
  fp_request : Fp_request_image,
  state_image : Cpu_state,
}

struct Commit_destination = {
  kind : string,
  index : bits(4),
  width : int,
}

struct Execution_fault = {
  kind : Fault_kind,
  operation : Semantic_operation,
  detail : string,
  error_code : bits(64),
  bus_error : bool,
}

struct Pending_commit = {
  kind : Commit_kind,
  operation : Semantic_operation,
  destination : Commit_destination,
  before : Cpu_state,
  after : Cpu_state,
  instruction : option(Decoded_instruction),
  phase : Continuation_phase,
  ordinal : int,
  captured_first : bits(64),
  captured_second : bits(64),
  memory_writes : list(Memory_write),
  atomic : bool,
  repeat_prefix : option(Decoded_instruction),
  repeat_body : option(Decoded_instruction),
  repeat_bytes : list(bits(8)),
  repeat_tail : list(bits(8)),
  repeat_tail_length : int,
  repeat_parent_active : bool,
  repeat_parent_grouped : bool,
  event : option(Event_record),
  event_attempt : int,
  boundary_class : Boundary_class,
  fp_pending : Fp_pending_image,
}

struct Transaction_response = {
  kind : Transaction_response_kind,
  success : bool,
  fault_kind : Fault_kind,
  detail : string,
  value : bits(64),
  secondary_value : bits(64),
  flags : bits(4),
  write_flags : bool,
  generated_fflags : bits(5),
  bounds_passed : bool,
  address_type : int,
  cache_policy : int,
  atomic_store_happened : bool,
  body_bytes : list(bits(8)),
  state_image : Cpu_state,
  known : bool,
  present : bool,
  fp_response : Fp_response_image,
}

struct Execution_result = {
  state : Cpu_state,
  pending : Pending_commit,
  request : Primitive_request,
  effects : list(Architectural_effect),
  fault : option(Execution_fault),
  awaiting_environment : bool,
}

struct Boundary_result = {
  state : Cpu_state,
  admitted : option(Event_record),
  execution : option(Execution_result),
}

struct Decode_execute_outcome = {
  decode : Decode_outcome,
  execution : option(Execution_result),
}

