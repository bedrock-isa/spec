union clause Uop_kind = UopCommit : unit

function clause execute_uop(UopCommit(), uop, _, _, _, speculative) =
    uop_step_complete(speculative, uop.commit_kind)
