enum Fp_conversion_operation =
  FpConvertSigned
| FpConvertUnsigned
| FpConvertRound
| FpConvertTruncate
| FpConvertFloor
| FpConvertCeiling

function fp_conversion_operation(operation : Semantic_operation)
  -> option(Fp_conversion_operation) = match operation {
  Op_FCVT => Some(FpConvertSigned),
  Op_FCVTU => Some(FpConvertUnsigned),
  Op_FROUND => Some(FpConvertRound),
  Op_FTRUNC => Some(FpConvertTruncate),
  Op_FFLOOR => Some(FpConvertFloor),
  Op_FCEIL => Some(FpConvertCeiling),
  _ => None(),
}

function fp_conversion_semantic_operation(operation : Fp_conversion_operation)
  -> Semantic_operation = match operation {
  FpConvertSigned => Op_FCVT,
  FpConvertUnsigned => Op_FCVTU,
  FpConvertRound => Op_FROUND,
  FpConvertTruncate => Op_FTRUNC,
  FpConvertFloor => Op_FFLOOR,
  FpConvertCeiling => Op_FCEIL,
}
