enum Fp_compare_operation =
  FpCompareOrdered
| FpCompareMinimum
| FpCompareMaximum

function fp_compare_operation(operation : Semantic_operation)
  -> option(Fp_compare_operation) = match operation {
  Op_FCMP => Some(FpCompareOrdered),
  Op_FMIN => Some(FpCompareMinimum),
  Op_FMAX => Some(FpCompareMaximum),
  _ => None(),
}

function fp_compare_semantic_operation(operation : Fp_compare_operation)
  -> Semantic_operation = match operation {
  FpCompareOrdered => Op_FCMP,
  FpCompareMinimum => Op_FMIN,
  FpCompareMaximum => Op_FMAX,
}
