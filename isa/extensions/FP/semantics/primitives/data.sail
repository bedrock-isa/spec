enum Fp_data_operation =
  FpDataCopySign
| FpDataClassify

function fp_data_operation(operation : Semantic_operation)
  -> option(Fp_data_operation) = match operation {
  Op_FCOPYSIGN => Some(FpDataCopySign),
  Op_FCLASS => Some(FpDataClassify),
  _ => None(),
}

function fp_data_semantic_operation(operation : Fp_data_operation)
  -> Semantic_operation = match operation {
  FpDataCopySign => Op_FCOPYSIGN,
  FpDataClassify => Op_FCLASS,
}
