union clause Uop_kind = UopTlbContext : Tlb_context_uop_operation

function clause execute_uop(UopTlbContext(operation), _, _, instruction, _, speculative) =
    uop_step_delegate(start_tlb_context_transaction(operation, instruction, speculative))
