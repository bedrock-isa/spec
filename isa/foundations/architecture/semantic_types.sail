enum Semantic_route =
  RouteAtomics
| RouteBounds
| RouteCache
| RouteControlFlow
| RouteCoreControl
| RouteDataMovement
| RouteEaUtility
| RouteFpu
| RouteFpuTranscendental
| RouteIntegerAlu
| RouteIntegerBitfield
| RouteIntegerMulDiv
| RouteIntegerUnary
| RouteSystemRegisters
| RouteTlbContext

enum Instruction_set = BaseSet | FpuSet | FpuTranscendentalSet
enum Privilege_level = UserPrivilege | SupervisorPrivilege | AnyPrivilege

enum Predicate_mode =
  PredicateNone
| AnnulOnFalse
| Temporary
| CounterAndCondition
| WriteBoolean

enum Decode_stage =
  DecodeSuccess
| DecodeFetch
| DecodeFraming
| DecodeOpcode
| DecodeConstraint
| DecodeEaDescriptor
| DecodeEaPayload
| DecodeStandalonePayload
| DecodeRecordLength
| DecodeStaticLegality

enum Fault_kind =
  NoFault
| IllegalInstruction
| PrivilegeFault
| ExtensionUnavailable
| InvalidControlState
| DivideByZero
| DivideOverflow
| BoundsFault
| AlignmentFault
| TranslationFault
| AccessFault
| FloatingPointFault
| EventFault

enum Effect_kind =
  NoEffect
| ReadMemory
| WriteMemory
| AtomicMemory
| TranslateAddress
| CacheOperation
| TlbOperation
| ControlRegisterAccess
| EventDelivery
| TraceMarker
| HaltProcessor
| ResetProcessor
| FloatingPointCompute
| TranscendentalCompute
| RepeatBody
| FenceOperation
| IntegerCompute

enum Commit_kind = CommitNone | CommitRegisters | CommitMemory | CommitControl | CommitEvent
