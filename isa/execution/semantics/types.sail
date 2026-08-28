enum Boundary_class = { BoundaryOrdinary, BoundaryRepeatIteration, BoundaryEventEntry }
struct Architectural_effect = {
  kind : Effect_kind,
  operation : Semantic_operation,
  form_id : Form_id,
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

enum Primitive_request_kind = {
    NoPrimitiveRequest,
    TranslationExecuteProbe,
    MemoryProbe,
    MemoryRead,
    MemoryStore,
    CompoundMemoryStore,
    NonTemporalStore,
    StackRange,
    SegmentBoundsPoint,
    AtomicReadModifyWrite,
    AddressTranslateRequest,
    PhysicalPteRead,
    CacheMaintenanceBlock,
    PrefetchHint,
    FenceCompletion,
    TlbInvalidateRequest,
    TranslationQueryRequest,
    ContextSwitchRequest,
    StateSaveRequest,
    StateRestoreRequest,
    RepeatBodyFetch,
    EventFrameAccess,
    CpuidQueryRequest,
    PerformanceCounterRequest,
    ControlTransitionRequest,
    ResetSerializeRequest,
    VectorMemoryRead,
    VectorMemoryWrite,
    ExternalIntegerRequest,
}

enum Transaction_access = {
    NoTransactionAccess,
    AccessLoad,
    AccessStore,
    AccessReadModifyWrite,
    AccessExecute,
    AccessStackRead,
    AccessStackWrite,
    AccessAddressOnly,
}

enum Memory_access_class = { NormalAccess, MmioAccess }
enum Physical_memory_class = { NormalPhysical, DevicePhysical }

enum Continuation_phase = {
    ContinuationNone,
    PhaseSourceAddress,
    PhaseSourceRead,
    PhaseDestinationAddress,
    PhaseDestinationProbe,
    PhaseDestinationWrite,
    PhaseMemoryWriteFirst,
    PhaseMemoryWriteSecond,
    PhaseTargetRead,
    PhaseTargetExecuteProbe,
    PhaseStackRange,
    PhaseStackReadFirst,
    PhaseStackReadSecond,
    PhaseStackWriteFirst,
    PhaseIntegerExternal,
    PhaseAtomicRmw,
    PhaseCacheTranslate,
    PhaseCacheMaintenance,
    PhaseFenceCompletion,
    PhaseTlbOperation,
    PhaseTranslationQuery,
    PhasePteRead,
    PhaseContextSwitch,
    PhaseStateSave,
    PhaseStateRestoreHeader,
    PhaseStateRestoreRange,
    PhaseStateRestore,
    PhaseRepeatFetch,
    PhaseEventFrameHeader,
    PhaseEventFrame,
    PhaseEventTargetProbe,
    PhaseEventStackProbe,
    PhaseEventFrameStore,
    PhaseEventReturnExecute,
    PhaseFpContractQuery,
    PhaseFpSourceRead,
    PhaseFpDestinationProbe,
    PhaseFpDestinationWrite,
    PhaseVectorMemoryRead,
    PhaseVectorMemoryWrite,
    PhaseVectorFpMemoryRead,
    PhaseVectorFpMemoryWrite,
    PhaseCpuidQuery,
    PhasePerformanceCounter,
    PhaseControlTransition,
    PhaseResetSerialize,
    PhaseUopMemoryRead,
    PhaseUopMemoryWrite,
}

enum Transaction_response_kind = {
    ResponseTranslation,
    ResponseProbe,
    ResponseRead,
    ResponseStoreAck,
    ResponseStackRange,
    ResponseSegmentBounds,
    ResponseIntegerExternal,
    ResponseAtomic,
    ResponseAddressTranslation,
    ResponsePteRead,
    ResponseCacheMaintenance,
    ResponseFenceCompletion,
    ResponseTlbOperation,
    ResponseTranslationQuery,
    ResponseContextSwitch,
    ResponseStateSave,
    ResponseStateRestore,
    ResponseRepeatFetch,
    ResponseEventFrame,
    ResponseVectorMemory,
    ResponseCpuidQuery,
    ResponsePerformanceCounter,
    ResponseControlTransition,
    ResponseResetSerialize,
}

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

enum Request_domain = {
    RequestDomainCurrent,
    RequestDomainUser,
    RequestDomainCode,
    RequestDomainStack,
    RequestDomainPhysicalPageTable,
}

enum Request_role = {
    RequestRoleNone,
    RequestRoleValue,
    RequestRoleAddress,
    RequestRoleControlTarget,
    RequestRoleSingle,
    RequestRoleStack,
    RequestRoleEventEntryTarget,
    RequestRoleEventFrameRange,
    RequestRoleEventFrameStore,
    RequestRoleUserReturnTarget,
    RequestRoleUserBankTarget,
    RequestRoleCacheTranslate,
    RequestRoleFpApproximationContractQuery,
    RequestRolePtqueryPte,
    RequestRoleVtopPte,
    RequestRolePhysicalPrefetch,
    RequestRolePhysicalCacheBlock,
}

enum Commit_destination_kind = { DestinationNone, DestinationRn, DestinationFn, DestinationSP }

struct Ea_evaluation = {
  operand_name : Operand_id,
  kind : Ea_kind,
  role : option(Ea_role),
  domain : option(Operand_domain),
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
  role : Request_role,
  domain : Request_domain,
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
  cache_policy : int,
  suppress_fault : bool,
  staged_updates : list(Staged_register_update),
  selector : bits(64),
  expected : bits(64),
  desired : bits(64),
  auxiliary : bits(64),
  body_length : int,
  payload_bytes : list(bits(8)),
}

struct Commit_destination = {
  kind : Commit_destination_kind,
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

scattered union Uop_kind

enum Uop_location_kind = {
    UopLocationNone,
    UopLocationRegister,
    UopLocationSp,
    UopLocationImmediate,
    UopLocationTemporary,
}

struct Uop_location = {
  kind : Uop_location_kind,
  index : int,
  immediate : bits(64),
}

struct Micro_operation = {
  kind : Uop_kind,
  source0 : Uop_location,
  source1 : Uop_location,
  destination : Uop_location,
  operand_name : Operand_id,
  width : int,
  commit_kind : Commit_kind,
}

struct Uop_value = {
  value : bits(64),
  address : bool,
  segment : int,
  segment_image : bits(64),
  effective_address : bits(64),
  linear_address : bits(64),
  domain : Request_domain,
}

struct Pending_commit = {
  kind : Commit_kind,
  operation : Semantic_operation,
  destination : Commit_destination,
  after : option(Cpu_state),
  instruction : option(Decoded_instruction),
  phase : Continuation_phase,
  ordinal : int,
  captured_first : bits(64),
  captured_second : bits(64),
  memory_writes : list(Memory_write),
  atomic : bool,
  repeat_body : option(Decoded_instruction),
  repeat_bytes : list(bits(8)),
  repeat_parent_active : bool,
  event : option(Event_record),
  event_attempt : int,
  boundary_class : Boundary_class,
  fp_pending : Fp_pending_image,
  vector_payload0 : list(bits(8)),
  vector_payload1 : list(bits(8)),
  uop_program : list(Micro_operation),
  uop_cursor : int,
  uop_values : list(Uop_value),
  uop_pending_destination : int,
}

struct Transaction_response = {
  kind : Transaction_response_kind,
  success : bool,
  fault_kind : Fault_kind,
  fault_cause : int,
  detail : string,
  value : bits(64),
  secondary_value : bits(64),
  flags : bits(4),
  write_flags : bool,
  generated_fflags : bits(5),
  bounds_passed : bool,
  cache_policy : int,
  access_class : Memory_access_class,
  physical_class : Physical_memory_class,
  atomic_store_happened : bool,
  body_bytes : list(bits(8)),
  known : bool,
  present : bool,
}

struct Execution_result = {
  state : Cpu_state,
  pending : Pending_commit,
  request : Primitive_request,
  effects : list(Architectural_effect),
  fault : option(Execution_fault),
  awaiting_environment : bool,
}

// Operation-local entries are generated after the core module.  Core
// continuations resume through this declared boundary without depending on a
// generic route dispatcher.
val execute_operation_entry : (Decoded_instruction, Cpu_state) -> Execution_result

struct Boundary_result = {
  state : Cpu_state,
  admitted : option(Event_record),
  execution : option(Execution_result),
}

struct Decode_execute_outcome = {
  decode : Decode_outcome,
  execution : option(Execution_result),
}
