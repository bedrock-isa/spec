enum Predicate_binary_kind = { PredicateBinaryAnd, PredicateBinaryOr, PredicateBinaryXor }

enum Vector_integer_binary_kind = {
    VectorIntegerAdd,
    VectorIntegerSubtract,
    VectorIntegerAnd,
    VectorIntegerOr,
    VectorIntegerXor,
    VectorIntegerMinimumSigned,
    VectorIntegerMinimumUnsigned,
    VectorIntegerMaximumSigned,
    VectorIntegerMaximumUnsigned,
    VectorIntegerMultiplyLow,
    VectorIntegerMultiplyHighSigned,
    VectorIntegerMultiplyHighUnsigned,
    VectorIntegerMultiplyHighSignedUnsigned,
}

enum Vector_integer_reduction_kind = {
    VectorReduceAdd,
    VectorReduceAnd,
    VectorReduceOr,
    VectorReduceXor,
    VectorReduceMinimumSigned,
    VectorReduceMinimumUnsigned,
    VectorReduceMaximumSigned,
    VectorReduceMaximumUnsigned,
}

enum Vector_integer_unary_kind = {
    VectorUnaryNegate,
    VectorUnaryAbsolute,
    VectorUnaryNot,
    VectorUnaryCountLeadingZeros,
    VectorUnaryCountTrailingZeros,
    VectorUnaryCountLeadingSign,
    VectorUnaryCountTrailingSign,
    VectorUnaryPopulationCount,
    VectorUnaryReverseBytes,
}

enum Vector_integer_compare_kind = { VectorCompareCondition, VectorTestZero, VectorTestNonzero }

enum Predicate_slide_kind = { PredicateSlideUp, PredicateSlideDown, PredicateSlice }

enum Predicate_pair_kind = {
    PredicateZipLow,
    PredicateZipHigh,
    PredicateUnzipLow,
    PredicateUnzipHigh,
    PredicateTransposeLow,
    PredicateTransposeHigh,
}

enum Vector_permute_kind = {
    VectorPermuteIndexed,
    VectorSlideUp,
    VectorSlideDown,
    VectorSlice,
    VectorZipLow,
    VectorZipHigh,
    VectorUnzipLow,
    VectorUnzipHigh,
    VectorTransposeLow,
    VectorTransposeHigh,
}

enum Vector_width_change_kind = { VectorExtendZero, VectorExtendSigned, VectorTruncate }

enum Vector_fp_exact_kind = { VectorFpNegate, VectorFpAbsolute, VectorFpCopySign, VectorFpClassify }

enum Vector_fp_reduction_identity = {
    VectorFpReductionZero,
    VectorFpReductionPositiveInfinity,
    VectorFpReductionNegativeInfinity,
}

enum Vector_memory_kind = { VectorPredicateMove, VectorMoveMerge, VectorMoveReplace, VectorGather, VectorScatter }

enum Vector_special_operation = {
    VectorSpecialPredicateCount,
    VectorSpecialPredicateFalse,
    VectorSpecialPredicateFirst,
    VectorSpecialPredicateHead,
    VectorSpecialPredicateLast,
    VectorSpecialPredicateNot,
    VectorSpecialPredicatePackHigh,
    VectorSpecialPredicatePackLow,
    VectorSpecialPredicatePermute,
    VectorSpecialPredicateSelect,
    VectorSpecialPredicateTail,
    VectorSpecialPredicateTrue,
    VectorSpecialPredicateUnpackHigh,
    VectorSpecialPredicateUnpackLow,
    VectorSpecialClear,
    VectorSpecialDuplicate,
    VectorSpecialExtract,
    VectorSpecialIndex,
    VectorSpecialInsert,
    VectorSpecialLaneCountAdd,
    VectorSpecialLaneCount,
    VectorSpecialMove,
}

union Vector_compute_result = {
    VectorComputeState : Cpu_state,
    VectorComputeFault : Execution_result,
}

struct Vector_semantics = {
  predicate_binary : option(Predicate_binary_kind),
  integer_binary : option(Vector_integer_binary_kind),
  integer_reduction : option(Vector_integer_reduction_kind),
  integer_unary : option(Vector_integer_unary_kind),
  shift : option(Shift_kind),
  integer_compare : option(Vector_integer_compare_kind),
  predicate_slide : option(Predicate_slide_kind),
  predicate_pair : option(Predicate_pair_kind),
  permute : option(Vector_permute_kind),
  width_change : option(Vector_width_change_kind),
  width_change_destination_bytes : int,
  fp_basic : bool,
  fp_conversion : bool,
  reduction : bool,
  fp_primitive : bool,
  fp_exact : option(Vector_fp_exact_kind),
  fp_compare : bool,
  fp_scalar_operation : option(Semantic_operation),
  fp_arity : int,
  fp_conversion_destination_bytes : int,
  fp_conversion_destination_fp : bool,
  fp_conversion_unsigned : bool,
  fp_reduction_operation : option(Semantic_operation),
  fp_reduction_identity : Vector_fp_reduction_identity,
  fp_allowed_causes : bits(5),
  memory : option(Vector_memory_kind),
  special : option(Vector_special_operation),
}

function vector_default_semantics() -> Vector_semantics = struct {
    predicate_binary = None(),
    integer_binary = None(),
    integer_reduction = None(),
    integer_unary = None(),
    shift = None(),
    integer_compare = None(),
    predicate_slide = None(),
    predicate_pair = None(),
    permute = None(),
    width_change = None(),
    width_change_destination_bytes = 1,
    fp_basic = false,
    fp_conversion = false,
    reduction = false,
    fp_primitive = false,
    fp_exact = None(),
    fp_compare = false,
    fp_scalar_operation = None(),
    fp_arity = 2,
    fp_conversion_destination_bytes = 8,
    fp_conversion_destination_fp = false,
    fp_conversion_unsigned = false,
    fp_reduction_operation = None(),
    fp_reduction_identity = VectorFpReductionZero,
    fp_allowed_causes = 0b10111,
    memory = None(),
    special = None(),
}

val vector_semantics : Semantic_operation -> Vector_semantics

scattered function vector_semantics


function clause vector_semantics(operation if semantic_route(operation) != RouteVector) =
    vector_default_semantics()
