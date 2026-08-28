union clause Uop_kind = UopCommit : unit

function clause execute_uop(UopCommit(), uop, _, _, _, instruction, before, speculative) =
    completed(before, advance_pc(speculative, instruction), uop.commit_kind, [||])
