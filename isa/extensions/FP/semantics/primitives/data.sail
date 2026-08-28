enum Fp_data_operation =
  FpDataCopySign
| FpDataClassify

function fp_data_semantic_operation(operation : Fp_data_operation)
  -> Semantic_operation = match operation {
  FpDataCopySign => Op_FCOPYSIGN,
  FpDataClassify => Op_FCLASS,
}
