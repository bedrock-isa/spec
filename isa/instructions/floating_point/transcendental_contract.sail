function fptrans_contract_operation(contract_id : bits(16)) -> option(Semantic_operation) =
  match contract_id {
    0x0001 => Some(Op_FSINA),
    0x0002 => Some(Op_FCOSA),
    0x0003 => Some(Op_FTANA),
    0x0004 => Some(Op_FSINCOSA),
    0x0011 => Some(Op_FASINA),
    0x0012 => Some(Op_FACOSA),
    0x0013 => Some(Op_FATANA),
    0x0021 => Some(Op_FSINHA),
    0x0022 => Some(Op_FCOSHA),
    0x0023 => Some(Op_FTANHA),
    0x0024 => Some(Op_FATANHA),
    0x0031 => Some(Op_FETOXA),
    0x0032 => Some(Op_FETOXM1A),
    0x0033 => Some(Op_FTWOTOXA),
    0x0034 => Some(Op_FTENTOXA),
    0x0041 => Some(Op_FLOGNA),
    0x0042 => Some(Op_FLOGNP1A),
    0x0043 => Some(Op_FLOG2A),
    0x0044 => Some(Op_FLOG10A),
    _ => None(),
  }

function fptrans_contract_id(operation : Semantic_operation) -> option(bits(16)) =
  match fp_semantics(operation) {
    Some(semantics) => if semantics.transcendental then Some(semantics.contract_id) else None(),
    None() => None(),
  }

function fptrans_contract_allowed_causes(contract_id : bits(16)) -> option(bits(5)) =
  match fptrans_contract_operation(contract_id) {
    None() => None(),
    Some(operation) => match fp_semantics(operation) {
      Some(semantics) => Some(semantics.allowed_causes),
      None() => None(),
    },
  }

enum Fptrans_contract_status =
  FptransContractUnknown
| FptransContractAbsent
| FptransContractMalformed
| FptransContractPresent

struct Fptrans_contract_lookup = {
  status : Fptrans_contract_status,
  operation : option(Semantic_operation),
  allowed_causes : bits(5),
  contract_word : bits(64),
  s_max_ulp_q8_8 : bits(16),
  d_max_ulp_q8_8 : bits(16),
}

function fptrans_contract_word_present(contract_word : bits(64)) -> bool =
  contract_word[63] == bitone

function fptrans_bound_valid(bound : bits(16)) -> bool =
  unsigned(bound) >= 1 & unsigned(bound) <= 1024

function fptrans_contract_word_valid(contract_word : bits(64)) -> bool =
  fptrans_contract_word_present(contract_word)
  & contract_word[62 .. 40] == 0b00000000000000000000000
  & contract_word[39 .. 32] == 0x01
  & fptrans_bound_valid(contract_word[15 .. 0])
  & fptrans_bound_valid(contract_word[31 .. 16])

function fptrans_selected_bound(contract_word : bits(64), width : int)
  -> option(bits(16)) =
  if not_bool(fptrans_contract_word_valid(contract_word)) then None()
  else if width == 4 then Some(contract_word[15 .. 0])
  else if width == 8 then Some(contract_word[31 .. 16])
  else None()

function fptrans_cpuid_selector(contract_id : bits(16)) -> bits(64) =
  0x000000010001 @ contract_id

function fptrans_contract_lookup(contract_id : bits(16), contract_word : bits(64))
  -> Fptrans_contract_lookup = match fptrans_contract_operation(contract_id) {
  None() => struct {
    status = FptransContractUnknown,
    operation = None(),
    allowed_causes = fflags_none,
    contract_word = contract_word,
    s_max_ulp_q8_8 = contract_word[15 .. 0],
    d_max_ulp_q8_8 = contract_word[31 .. 16]
  },
  Some(operation) => struct {
    status = if not_bool(fptrans_contract_word_present(contract_word))
             then FptransContractAbsent
             else if fptrans_contract_word_valid(contract_word)
             then FptransContractPresent
             else FptransContractMalformed,
    operation = Some(operation),
    allowed_causes = match fp_semantics(operation) {
      Some(semantics) => semantics.allowed_causes,
      None() => fflags_none,
    },
    contract_word = contract_word,
    s_max_ulp_q8_8 = contract_word[15 .. 0],
    d_max_ulp_q8_8 = contract_word[31 .. 16]
  },
}

function fp_operation_count(operations : list(Semantic_operation)) -> int = match operations {
  [||] => 0,
  operation :: tail => {
    let selected : int = match fp_semantics(operation) { Some(_) => 1, None() => 0 };
    selected + fp_operation_count(tail)
  },
}

function fp_form_count(forms : list(Catalog_entry)) -> int = match forms {
  [||] => 0,
  form :: tail => {
    let selected : int = match fp_semantics(form.operation) { Some(_) => 1, None() => 0 };
    selected + fp_form_count(tail)
  },
}

function fp_path_count(forms : list(Catalog_entry), path : Fp_path) -> int = match forms {
  [||] => 0,
  form :: tail => {
    let selected : int = match fp_form_path(form) {
      Some(form_path) => if form_path == path then 1 else 0,
      None() => 0,
    };
    selected + fp_path_count(tail, path)
  },
}

