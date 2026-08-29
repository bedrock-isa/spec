function vector_special_compute(kind : Vector_special_operation, instruction : Decoded_instruction, state : Cpu_state)
    -> option(Vector_compute_result) = match kind {
        VectorSpecialPredicateCount => vector_special_pcount_compute(instruction, state),
        VectorSpecialPredicateFalse => vector_special_pfalse_compute(instruction, state),
        VectorSpecialPredicateFirst => vector_special_pfirst_compute(instruction, state),
        VectorSpecialPredicateHead => vector_special_phead_compute(instruction, state),
        VectorSpecialPredicateLast => vector_special_plast_compute(instruction, state),
        VectorSpecialPredicateNot => vector_special_pnot_compute(instruction, state),
        VectorSpecialPredicatePackHigh => vector_special_ppackhi_compute(instruction, state),
        VectorSpecialPredicatePackLow => vector_special_ppacklo_compute(instruction, state),
        VectorSpecialPredicatePermute => vector_special_pperm_compute(instruction, state),
        VectorSpecialPredicateSelect => vector_special_psel_compute(instruction, state),
        VectorSpecialPredicateTail => vector_special_ptail_compute(instruction, state),
        VectorSpecialPredicateTrue => vector_special_ptrue_compute(instruction, state),
        VectorSpecialPredicateUnpackHigh => vector_special_punpkhi_compute(instruction, state),
        VectorSpecialPredicateUnpackLow => vector_special_punpklo_compute(instruction, state),
        VectorSpecialClear => vector_special_vclr_compute(instruction, state),
        VectorSpecialDuplicate => vector_special_vdup_compute(instruction, state),
        VectorSpecialExtract => vector_special_vextract_compute(instruction, state),
        VectorSpecialIndex => vector_special_vindex_compute(instruction, state),
        VectorSpecialInsert => vector_special_vinsert_compute(instruction, state),
        VectorSpecialLaneCountAdd => vector_special_vlcadd_compute(instruction, state),
        VectorSpecialLaneCount => vector_special_vlcnt_compute(instruction, state),
        VectorSpecialMove => vector_special_vmov_compute(instruction, state),
    }

function vector_register_compute_result(
    operation : Semantic_operation,
    instruction : Decoded_instruction,
    state : Cpu_state,
) -> option(Vector_compute_result) = {
    let semantics = vector_semantics(operation);
    if semantics.integer_binary != None() then vector_integer_binary_compute(instruction, state)
    else if semantics.integer_unary != None() then vector_integer_unary_compute(instruction, state)
    else if semantics.integer_reduction != None() then vector_integer_reduction_compute(instruction, state)
    else if semantics.shift != None() then vector_shift_compute(instruction, state)
    else if semantics.integer_compare != None() then vector_integer_compare_compute(instruction, state)
    else if semantics.width_change != None() then vector_width_change_compute(instruction, state)
    else if semantics.permute != None() then vector_permute_compute(instruction, state)
    else if semantics.predicate_binary != None() then vector_predicate_binary_compute(instruction, state)
    else if semantics.predicate_slide != None() then vector_predicate_slide_compute(instruction, state)
    else if semantics.predicate_pair != None() then vector_predicate_pair_compute(instruction, state)
    else match semantics.special {
        Some(kind) => vector_special_compute(kind, instruction, state),
        None() => None(),
    }
}
