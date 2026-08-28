function fptransa_semantics(operation : Semantic_operation) -> option(Fp_semantics) =
  match operation {
    Op_FACOSA => Some(fp_info(FpPathR, 1, FpResultFnByFormat, 0b10010,
                              fp_flags_none, true, 18)),
    Op_FASINA => Some(fp_info(FpPathR, 1, FpResultFnByFormat, 0b10010,
                              fp_flags_none, true, 17)),
    Op_FATANA => Some(fp_info(FpPathR, 1, FpResultFnByFormat, 0b10010,
                              fp_flags_none, true, 19)),
    Op_FATANHA => Some(fp_info(FpPathR, 1, FpResultFnByFormat, 0b11010,
                               fp_flags_none, true, 36)),
    Op_FCOSA => Some(fp_info(FpPathR, 1, FpResultFnByFormat, fflags_nv,
                             fp_flags_none, true, 2)),
    Op_FCOSHA => Some(fp_info(FpPathR, 1, FpResultFnByFormat, 0b10100,
                              fp_flags_none, true, 34)),
    Op_FETOXA => Some(fp_info(FpPathR, 1, FpResultFnByFormat, 0b10110,
                              fp_flags_none, true, 49)),
    Op_FETOXM1A => Some(fp_info(FpPathR, 1, FpResultFnByFormat, 0b10110,
                                fp_flags_none, true, 50)),
    Op_FLOG10A => Some(fp_info(FpPathR, 1, FpResultFnByFormat, 0b11010,
                               fp_flags_none, true, 68)),
    Op_FLOG2A => Some(fp_info(FpPathR, 1, FpResultFnByFormat, 0b11010,
                              fp_flags_none, true, 67)),
    Op_FLOGNA => Some(fp_info(FpPathR, 1, FpResultFnByFormat, 0b11010,
                              fp_flags_none, true, 65)),
    Op_FLOGNP1A => Some(fp_info(FpPathR, 1, FpResultFnByFormat, 0b11010,
                                fp_flags_none, true, 66)),
    Op_FSINA => Some(fp_info(FpPathR, 1, FpResultFnByFormat, 0b10010,
                             fp_flags_none, true, 1)),
    Op_FSINCOSA => Some(fp_info(FpPathR, 1, FpResultFnPairByFormat, 0b10010,
                                fp_flags_none, true, 4)),
    Op_FSINHA => Some(fp_info(FpPathR, 1, FpResultFnByFormat, 0b10110,
                              fp_flags_none, true, 33)),
    Op_FTANA => Some(fp_info(FpPathR, 1, FpResultFnByFormat, 0b10010,
                             fp_flags_none, true, 3)),
    Op_FTANHA => Some(fp_info(FpPathR, 1, FpResultFnByFormat, 0b10010,
                              fp_flags_none, true, 35)),
    Op_FTENTOXA => Some(fp_info(FpPathR, 1, FpResultFnByFormat, 0b10110,
                                fp_flags_none, true, 52)),
    Op_FTWOTOXA => Some(fp_info(FpPathR, 1, FpResultFnByFormat, 0b10110,
                                fp_flags_none, true, 51)),
    _ => None(),
  }

function fptransa_is_operation(operation : Semantic_operation) -> bool =
  match fptransa_semantics(operation) {
    Some(_) => true,
    None() => false,
  }

function clause fp_semantics (operation if fptransa_is_operation(operation)) =
  fptransa_semantics(operation)

function clause fp_semantics _ = None()
