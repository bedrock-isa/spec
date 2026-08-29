union clause Uop_kind = UopEnvironment : Environment_uop_operation
union clause Uop_kind = UopSystemRequest : System_request_uop_operation

function clause execute_uop(UopEnvironment(operation), _, _, instruction, _, speculative) =
    uop_step_delegate(route_environment(instruction, speculative, operation.family,
        operation.request_kind, operation.effect_kind, operation.commit_kind,
        operation.suppress_fault))

function clause execute_uop(UopSystemRequest(operation), _, _, instruction, _, speculative) =
    uop_step_delegate(start_system_request(operation, instruction, speculative))
