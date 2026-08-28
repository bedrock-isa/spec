enum Fp_approx_contract_status =
  FpApproxContractUnknown
| FpApproxContractAbsent
| FpApproxContractMalformed
| FpApproxContractPresent

struct Fp_approx_contract_lookup = {
  status : Fp_approx_contract_status,
  operation : option(Semantic_operation),
  allowed_causes : bits(5),
  contract_word : bits(64),
  s_max_ulp_q8_8 : bits(16),
  d_max_ulp_q8_8 : bits(16),
}

val fp_approx_contract_operation : bits(16) -> option(Semantic_operation)
val fp_approx_contract_id : Semantic_operation -> option(bits(16))
val fp_approx_contract_allowed_causes : bits(16) -> option(bits(5))
val fp_approx_contract_word_present : bits(64) -> bool
val fp_approx_bound_valid : bits(16) -> bool
val fp_approx_contract_word_valid : bits(64) -> bool
val fp_approx_selected_bound : (bits(64), int) -> option(bits(16))
val fp_approx_cpuid_selector : bits(16) -> bits(64)
val fp_approx_contract_lookup : (bits(16), bits(64)) -> Fp_approx_contract_lookup
