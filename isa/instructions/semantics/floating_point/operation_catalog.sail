enum Fp_path = FpPathR | FpPathS1 | FpPathS2 | FpPathD1 | FpPathStack

enum Fp_result_policy =
  FpResultNone
| FpResultFnByFormat
| FpResultByForm
| FpResultFn32
| FpResultFn64
| FpResultRn64
| FpResultFlags
| FpResultFlagsVOnly
| FpResultFnPairByFormat
| FpResultFnPair32
| FpResultFnPair64
| FpResultMemory32
| FpResultMemory64

struct Fp_semantics = {
  path : Fp_path,
  source_count : int,
  result_policy : Fp_result_policy,
  allowed_causes : bits(5),
  flags_mask : bits(4),
  transcendental : bool,
  contract_id : bits(16),
}

let fflags_nv : bits(5) = 0b10000
let fflags_dz : bits(5) = 0b01000
let fflags_of : bits(5) = 0b00100
let fflags_uf : bits(5) = 0b00010
let fflags_nx : bits(5) = 0b00001
let fflags_none : bits(5) = 0b00000
let fflags_all : bits(5) = 0b11111
let fflags_fptransa : bits(5) = 0b11110

let fp_flags_none : bits(4) = 0b0000
let fp_flags_all : bits(4) = 0b1111
let fp_flags_v : bits(4) = 0b0001

function fp_info(path : Fp_path, source_count : int, result_policy : Fp_result_policy,
                 allowed_causes : bits(5), flags_mask : bits(4),
                 transcendental : bool, contract_id : int) -> Fp_semantics = struct {
  path = path,
  source_count = source_count,
  result_policy = result_policy,
  allowed_causes = allowed_causes,
  flags_mask = flags_mask,
  transcendental = transcendental,
  contract_id = get_slice_int(16, contract_id, 0)
}

function fp_semantics(operation : Semantic_operation) -> option(Fp_semantics) =
  match operation {
    Op_FABS => Some(fp_info(FpPathR, 1, FpResultByForm, fflags_none,
                            fp_flags_none, false, 0)),
    Op_FADD => Some(fp_info(FpPathR, 2, FpResultFnByFormat, 0b10111,
                            fp_flags_none, false, 0)),
    Op_FBNDII => Some(fp_info(FpPathR, 3, FpResultFlagsVOnly, fflags_nv,
                              fp_flags_v, false, 0)),
    Op_FBNDIX => Some(fp_info(FpPathR, 3, FpResultFlagsVOnly, fflags_nv,
                              fp_flags_v, false, 0)),
    Op_FBNDXI => Some(fp_info(FpPathR, 3, FpResultFlagsVOnly, fflags_nv,
                              fp_flags_v, false, 0)),
    Op_FBNDXX => Some(fp_info(FpPathR, 3, FpResultFlagsVOnly, fflags_nv,
                              fp_flags_v, false, 0)),
    Op_FCEIL => Some(fp_info(FpPathR, 1, FpResultByForm, 0b10001,
                             fp_flags_none, false, 0)),
    Op_FCLASS => Some(fp_info(FpPathR, 1, FpResultRn64, fflags_none,
                              fp_flags_none, false, 0)),
    Op_FCLR => Some(fp_info(FpPathR, 0, FpResultFn64, fflags_none,
                            fp_flags_none, false, 0)),
    Op_FCMP => Some(fp_info(FpPathR, 2, FpResultFlags, fflags_nv,
                            fp_flags_all, false, 0)),
    Op_FCOPYSIGN => Some(fp_info(FpPathR, 2, FpResultFnByFormat, fflags_none,
                                fp_flags_none, false, 0)),
    Op_FCVT => Some(fp_info(FpPathR, 1, FpResultByForm, 0b10111,
                            fp_flags_none, false, 0)),
    Op_FCVTU => Some(fp_info(FpPathR, 1, FpResultByForm, 0b10111,
                             fp_flags_none, false, 0)),
    Op_FDIV => Some(fp_info(FpPathR, 2, FpResultFnByFormat, fflags_all,
                            fp_flags_none, false, 0)),
    Op_FFLOOR => Some(fp_info(FpPathR, 1, FpResultByForm, 0b10001,
                              fp_flags_none, false, 0)),
    Op_FGETEXP => Some(fp_info(FpPathR, 1, FpResultFnByFormat, fflags_nv,
                              fp_flags_none, false, 0)),
    Op_FGETMAN => Some(fp_info(FpPathR, 1, FpResultFnByFormat, 0b10001,
                              fp_flags_none, false, 0)),
    Op_FINT => Some(fp_info(FpPathR, 1, FpResultByForm, 0b10001,
                            fp_flags_none, false, 0)),
    Op_FINTRZ => Some(fp_info(FpPathR, 1, FpResultByForm, 0b10001,
                              fp_flags_none, false, 0)),
    Op_FMADD => Some(fp_info(FpPathR, 3, FpResultFnByFormat, 0b10111,
                             fp_flags_none, false, 0)),
    Op_FMAX => Some(fp_info(FpPathR, 2, FpResultFnByFormat, fflags_nv,
                            fp_flags_none, false, 0)),
    Op_FMIN => Some(fp_info(FpPathR, 2, FpResultFnByFormat, fflags_nv,
                            fp_flags_none, false, 0)),
    Op_FMOD => Some(fp_info(FpPathR, 2, FpResultFnByFormat, fflags_nv,
                            fp_flags_none, false, 0)),
    Op_FMOV => Some(fp_info(FpPathR, 1, FpResultByForm, fflags_none,
                            fp_flags_none, false, 0)),
    Op_FMOVCR => Some(fp_info(FpPathR, 0, FpResultFn64, fflags_none,
                              fp_flags_none, false, 0)),
    Op_FMOVcc => Some(fp_info(FpPathR, 1, FpResultByForm, fflags_none,
                              fp_flags_none, false, 0)),
    Op_FMSUB => Some(fp_info(FpPathR, 3, FpResultFnByFormat, 0b10111,
                             fp_flags_none, false, 0)),
    Op_FMUL => Some(fp_info(FpPathR, 2, FpResultFnByFormat, 0b10111,
                            fp_flags_none, false, 0)),
    Op_FNEG => Some(fp_info(FpPathR, 1, FpResultByForm, fflags_none,
                            fp_flags_none, false, 0)),
    Op_FNMADD => Some(fp_info(FpPathR, 3, FpResultFnByFormat, 0b10111,
                              fp_flags_none, false, 0)),
    Op_FNMSUB => Some(fp_info(FpPathR, 3, FpResultFnByFormat, 0b10111,
                              fp_flags_none, false, 0)),
    Op_FPOPP => Some(fp_info(FpPathStack, 2, FpResultFnPair64, fflags_none,
                             fp_flags_none, false, 0)),
    Op_FPUSHP => Some(fp_info(FpPathStack, 2, FpResultMemory64, fflags_none,
                              fp_flags_none, false, 0)),
    Op_FREM => Some(fp_info(FpPathR, 2, FpResultFnByFormat, fflags_nv,
                            fp_flags_none, false, 0)),
    Op_FROUND => Some(fp_info(FpPathR, 1, FpResultByForm, 0b10001,
                              fp_flags_none, false, 0)),
    Op_FSCALE => Some(fp_info(FpPathR, 2, FpResultFnByFormat, 0b10111,
                              fp_flags_none, false, 0)),
    Op_FSQRT => Some(fp_info(FpPathR, 1, FpResultByForm, 0b10001,
                             fp_flags_none, false, 0)),
    Op_FSUB => Some(fp_info(FpPathR, 2, FpResultFnByFormat, 0b10111,
                            fp_flags_none, false, 0)),
    Op_FTEST => Some(fp_info(FpPathR, 1, FpResultFlags, fflags_nv,
                             fp_flags_all, false, 0)),
    Op_FTRUNC => Some(fp_info(FpPathR, 1, FpResultByForm, 0b10001,
                              fp_flags_none, false, 0)),
    Op_FXCHG => Some(fp_info(FpPathR, 2, FpResultFnPair64, fflags_none,
                             fp_flags_none, false, 0)),

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

function fp_causes_valid(semantics : Fp_semantics, generated : bits(5)) -> bool =
  (generated & semantics.allowed_causes) == generated

function fp_operation_causes_valid(operation : Semantic_operation,
                                   generated : bits(5)) -> bool =
  match fp_semantics(operation) {
    Some(semantics) => fp_causes_valid(semantics, generated),
    None() => false,
  }

function fp_enabled_causes(fstatus : bits(64), generated : bits(5)) -> bits(5) =
  fstatus[4 .. 0] & generated

function fp_traps(fstatus : bits(64), generated : bits(5)) -> bool =
  fp_enabled_causes(fstatus, generated) != fflags_none

function fp_ea_read_count(operands : list(Catalog_operand)) -> int = match operands {
  [||] => 0,
  operand :: tail =>
    (if operand.type_name == "EA" & operand.access == AccessRead then 1 else 0)
    + fp_ea_read_count(tail),
}

function fp_has_ea_write(operands : list(Catalog_operand)) -> bool = match operands {
  [||] => false,
  operand :: tail =>
    (operand.type_name == "EA"
     & (operand.access == AccessWrite | operand.access == AccessReadWrite))
    | fp_has_ea_write(tail),
}

function fp_has_rn_write(operands : list(Catalog_operand)) -> bool = match operands {
  [||] => false,
  operand :: tail =>
    (operand.type_name == "Rn"
     & (operand.access == AccessWrite | operand.access == AccessReadWrite))
    | fp_has_rn_write(tail),
}

function fp_form_path(form : Catalog_entry) -> option(Fp_path) =
  match fp_semantics(form.operation) {
    None() => None(),
    Some(_) =>
      if form.operation == Op_FPOPP | form.operation == Op_FPUSHP then Some(FpPathStack)
      else if fp_has_ea_write(form.operands) then Some(FpPathD1)
      else if fp_ea_read_count(form.operands) >= 2 then Some(FpPathS2)
      else if fp_ea_read_count(form.operands) == 1 then Some(FpPathS1)
      else Some(FpPathR),
  }

function fp_fn_result(width : int) -> Fp_result_policy =
  if width == 4 then FpResultFn32 else FpResultFn64

function fp_pair_result(width : int) -> Fp_result_policy =
  if width == 4 then FpResultFnPair32 else FpResultFnPair64

function fp_memory_result(width : int) -> Fp_result_policy =
  if width == 4 then FpResultMemory32 else FpResultMemory64

function fp_form_result_policy(form : Catalog_entry, width : int) -> option(Fp_result_policy) =
  match fp_semantics(form.operation) {
    None() => None(),
    Some(semantics) =>
      if width != 4 & width != 8 then None()
      else if form.operation == Op_FPOPP then Some(FpResultFnPair64)
      else if form.operation == Op_FPUSHP then Some(FpResultMemory64)
      else if form.operation == Op_FXCHG then Some(FpResultFnPair64)
      else if form.operation == Op_FSINCOSA then Some(fp_pair_result(width))
      else if semantics.result_policy == FpResultFlags
           | semantics.result_policy == FpResultFlagsVOnly
           | semantics.result_policy == FpResultNone
           | semantics.result_policy == FpResultRn64
        then Some(semantics.result_policy)
      else if fp_has_rn_write(form.operands) then Some(FpResultRn64)
      else if fp_has_ea_write(form.operands) then Some(fp_memory_result(width))
      else if form.operation == Op_FCLR | form.operation == Op_FMOVCR
        then Some(FpResultFn64)
      else Some(fp_fn_result(width)),
  }

function fp_form_semantics(form : Catalog_entry, width : int) -> option(Fp_semantics) =
  match (fp_semantics(form.operation), fp_form_path(form),
         fp_form_result_policy(form, width)) {
    (Some(semantics), Some(path), Some(result_policy)) =>
      Some({ semantics with path = path, result_policy = result_policy }),
    _ => None(),
  }

