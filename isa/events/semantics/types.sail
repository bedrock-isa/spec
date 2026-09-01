enum Event_kind = EventNone | EventSynchronous | EventDebug | EventNmi | EventInterrupt
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
  automatic_return_rf : bool,
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
  interrupt_posted : bool,
  interrupt_identity : bits(24),
}
