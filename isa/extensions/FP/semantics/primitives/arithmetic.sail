enum Fp_arithmetic_operation =
  FpArithmeticAbsolute
| FpArithmeticNegate
| FpArithmeticAdd
| FpArithmeticSubtract
| FpArithmeticMultiply
| FpArithmeticDivide
| FpArithmeticSquareRoot
| FpArithmeticFusedMultiplyAdd
| FpArithmeticFusedMultiplySubtract
| FpArithmeticFusedNegatedMultiplyAdd
| FpArithmeticFusedNegatedMultiplySubtract

function fp_arithmetic_operation(operation : Semantic_operation)
  -> option(Fp_arithmetic_operation) = match operation {
  Op_FABS => Some(FpArithmeticAbsolute),
  Op_FNEG => Some(FpArithmeticNegate),
  Op_FADD => Some(FpArithmeticAdd),
  Op_FSUB => Some(FpArithmeticSubtract),
  Op_FMUL => Some(FpArithmeticMultiply),
  Op_FDIV => Some(FpArithmeticDivide),
  Op_FSQRT => Some(FpArithmeticSquareRoot),
  Op_FMADD => Some(FpArithmeticFusedMultiplyAdd),
  Op_FMSUB => Some(FpArithmeticFusedMultiplySubtract),
  Op_FNMADD => Some(FpArithmeticFusedNegatedMultiplyAdd),
  Op_FNMSUB => Some(FpArithmeticFusedNegatedMultiplySubtract),
  _ => None(),
}

function fp_arithmetic_semantic_operation(operation : Fp_arithmetic_operation)
  -> Semantic_operation = match operation {
  FpArithmeticAbsolute => Op_FABS,
  FpArithmeticNegate => Op_FNEG,
  FpArithmeticAdd => Op_FADD,
  FpArithmeticSubtract => Op_FSUB,
  FpArithmeticMultiply => Op_FMUL,
  FpArithmeticDivide => Op_FDIV,
  FpArithmeticSquareRoot => Op_FSQRT,
  FpArithmeticFusedMultiplyAdd => Op_FMADD,
  FpArithmeticFusedMultiplySubtract => Op_FMSUB,
  FpArithmeticFusedNegatedMultiplyAdd => Op_FNMADD,
  FpArithmeticFusedNegatedMultiplySubtract => Op_FNMSUB,
}
