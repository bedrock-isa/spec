enum Fp_conversion_operation =
  FpConvertSigned
| FpConvertUnsigned
| FpConvertRound
| FpConvertTruncate
| FpConvertFloor
| FpConvertCeiling

function fp_conversion_semantic_operation(operation : Fp_conversion_operation)
  -> Semantic_operation = match operation {
  FpConvertSigned => Op_FCVT,
  FpConvertUnsigned => Op_FCVTU,
  FpConvertRound => Op_FROUND,
  FpConvertTruncate => Op_FTRUNC,
  FpConvertFloor => Op_FFLOOR,
  FpConvertCeiling => Op_FCEIL,
}
