union clause Uop_kind = UopRepeat : unit
union clause Uop_kind = UopEventControl : Event_control_uop_operation

function clause execute_uop(UopRepeat(), _, _, instruction, _, speculative) =
    uop_step_delegate(start_repeat_transaction(instruction, speculative))

function clause execute_uop(UopEventControl(operation), _, _, instruction, _, speculative) =
    uop_step_delegate(start_event_control(operation, instruction, speculative))
