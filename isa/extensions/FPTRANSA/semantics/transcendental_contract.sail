function fp_approx_contract_operation(contract_id : bits(16)) -> option(Semantic_operation) =
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

function fp_approx_contract_id(operation : Semantic_operation) -> option(bits(16)) =
  match fptransa_semantics(operation) {
    Some(semantics) => Some(semantics.contract_id),
    None() => None(),
  }

function fp_approx_contract_allowed_causes(contract_id : bits(16)) -> option(bits(5)) =
  match fp_approx_contract_operation(contract_id) {
    None() => None(),
    Some(operation) => match fptransa_semantics(operation) {
      Some(semantics) => Some(semantics.allowed_causes),
      None() => None(),
    },
  }

function fp_approx_contract_word_present(contract_word : bits(64)) -> bool =
  contract_word[63] == bitone

function fp_approx_bound_valid(bound : bits(16)) -> bool =
  unsigned(bound) >= 1 & unsigned(bound) <= 1024

function fp_approx_contract_word_valid(contract_word : bits(64)) -> bool =
  fp_approx_contract_word_present(contract_word)
  & contract_word[62 .. 40] == 0b00000000000000000000000
  & contract_word[39 .. 32] == 0x01
  & fp_approx_bound_valid(contract_word[15 .. 0])
  & fp_approx_bound_valid(contract_word[31 .. 16])

function fp_approx_selected_bound(contract_word : bits(64), width : int)
  -> option(bits(16)) =
  if not_bool(fp_approx_contract_word_valid(contract_word)) then None()
  else if width == 4 then Some(contract_word[15 .. 0])
  else if width == 8 then Some(contract_word[31 .. 16])
  else None()

function fp_approx_cpuid_selector(contract_id : bits(16)) -> bits(64) =
  0x000000010001 @ contract_id

function fp_approx_contract_lookup(contract_id : bits(16), contract_word : bits(64))
  -> Fp_approx_contract_lookup = match fp_approx_contract_operation(contract_id) {
  None() => struct {
    status = FpApproxContractUnknown,
    operation = None(),
    allowed_causes = fflags_none,
    contract_word = contract_word,
    s_max_ulp_q8_8 = contract_word[15 .. 0],
    d_max_ulp_q8_8 = contract_word[31 .. 16]
  },
  Some(operation) => struct {
    status = if not_bool(fp_approx_contract_word_present(contract_word))
             then FpApproxContractAbsent
             else if fp_approx_contract_word_valid(contract_word)
             then FpApproxContractPresent
             else FpApproxContractMalformed,
    operation = Some(operation),
    allowed_causes = match fptransa_semantics(operation) {
      Some(semantics) => semantics.allowed_causes,
      None() => fflags_none,
    },
    contract_word = contract_word,
    s_max_ulp_q8_8 = contract_word[15 .. 0],
    d_max_ulp_q8_8 = contract_word[31 .. 16]
  },
}
