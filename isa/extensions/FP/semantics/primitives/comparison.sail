enum Fp_compare_operation =
  FpCompareOrdered
| FpCompareMinimum
| FpCompareMaximum

function fp_compare_semantic_operation(operation : Fp_compare_operation)
  -> Semantic_operation = match operation {
  FpCompareOrdered => Op_FCMP,
  FpCompareMinimum => Op_FMIN,
  FpCompareMaximum => Op_FMAX,
}
