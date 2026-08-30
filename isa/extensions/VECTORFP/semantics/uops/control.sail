union clause Uop_kind = UopVectorFp : Semantic_operation

val vector_fp_uop_execute : (
        Semantic_operation,
        Uop,
        list(Uop_value),
        Decoded_instruction,
        Cpu_state,
        Cpu_state,
    ) -> Uop_step

function clause execute_uop(UopVectorFp(operation), uop, values, instruction, before, speculative) =
    vector_fp_uop_execute(operation, uop, values, instruction, before, speculative)
