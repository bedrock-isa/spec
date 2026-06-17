#!/usr/bin/env python3
"""Generate an operand-aware ISA opcode allocation plan with Z3."""

from __future__ import annotations

from pathlib import Path
from typing import Any
import argparse
import sys

sys.dont_write_bytecode = True

from isa_spec import (
    PatternEntry,
    json_dumps,
    load_and_validate,
    print_result,
)


from alloc_candidates import (
    alias_rules_by_target,
    all_direct_d,
    allocation_params,
    allocation_rule_matches,
    canonical_alias_family_mnemonics,
    canonical_alias_rules,
    ceil_words,
    collect_candidates,
    form_name,
    operand_norm,
)
from alloc_markdown import render_markdown
from alloc_field_layout import (
    assign_field_positions,
    bit_range,
    build_field_layout_model,
    descriptor_layout_text,
    extended_field_layout_text,
    field_dict,
    field_layout_model_report,
    layout_text,
)
from alloc_validation import audit_alignment, has_alignment_failure
from alloc_model import (
    DEFAULT_COMPACT_EXCLUDE,
    DEFAULT_COMPACT_PREFER,
    EXTENDED_BITS,
    EXTENDED_SLOTS,
    EXTENDED_SPACE_ID,
    EXTENSION_FAMILY_RANK,
    EXTENSION_PROFILE_RANK,
    HIGH_PRIMARY_PAYLOAD_START,
    PRIMARY_BITS,
    PRIMARY_EXTENSION_HEADROOM_SLOTS,
    PRIMARY_SLOTS,
    PRIMARY_SPACE_ID,
    Candidate,
    Field,
    default_field_layout_policy,
    profile_candidate_id,
    profile_form_parts,
    size_tag_from_fields,
)



def normalize_compact_policy(raw_policy: dict[str, Any]) -> dict[str, Any]:
    compactness = raw_policy.get("compactness_policy", raw_policy)
    return {
        "compact_exclude": tuple(str(item) for item in compactness.get("compact_exclude", DEFAULT_COMPACT_EXCLUDE)),
        "compact_prefer": tuple(str(item) for item in compactness.get("compact_prefer", DEFAULT_COMPACT_PREFER)),
        "compact_family_symmetry": raw_policy.get("compact_family_symmetry", {}),
        "instruction_families": raw_policy.get("instruction_families", {}),
        "family_locality": raw_policy.get("family_locality", default_family_locality_policy()),
        "decode_cost_policy": raw_policy.get("decode_cost_policy", default_decode_cost_policy()),
        "extension_root_policy": raw_policy.get("extension_root_policy", default_extension_root_policy()),
        "extension_roots": raw_policy.get("extension_roots", default_extension_roots_policy()),
        "primary_clusters": raw_policy.get("primary_clusters", default_primary_clusters_policy()),
        "condition_field": raw_policy.get("condition_field", {}),
        "field_reclaim": raw_policy.get("field_reclaim", {}),
        "field_layout": raw_policy.get("field_layout", default_field_layout_policy()),
        "mnemonic_policy": raw_policy.get("mnemonic_policy", {}),
    }


def default_family_locality_policy() -> dict[str, Any]:
    return {
        "integer_alu": {
            "prefer_contiguous_roots": True,
            "roots": ["EA_TO_D", "EA_TO_A", "D_TO_EA"],
        }
    }


def default_decode_cost_policy() -> dict[str, Any]:
    return {
        "priority_order": [
            "aligned_large_ranges",
            "shared_field_layout",
            "family_locality",
            "fewer_singletons",
            "compact_hot_path",
            "visual_symmetry",
        ]
    }


def default_extension_root_policy() -> dict[str, Any]:
    return {
        "preferred_region": "high_primary_payload",
        "prefer_contiguous_family_roots": True,
        "allow_low_payload_roots": False,
    }


def default_extension_roots_policy() -> dict[str, Any]:
    return {
        "group_by": "semantic_family",
        "condition_field_in_primary": True,
    }


def default_primary_clusters_policy() -> dict[str, Any]:
    return {
        "order": ["bitmap_ops", "direct_call", "stack_ops", "core_control"],
    }


def mnemonic_policy_set(compact_policy: dict[str, Any], key: str) -> set[str]:
    policy = compact_policy.get("mnemonic_policy", {})
    if not isinstance(policy, dict):
        return set()
    values = policy.get(key, [])
    if not isinstance(values, list):
        return set()
    return {str(item).upper() for item in values}


def is_transcendental_fpu_candidate(candidate: Candidate) -> bool:
    family = str(candidate.extension_family or "").lower()
    group = str(candidate.group or "").lower()
    return family == "fpu_transcendental" or group.split(".", 1)[0] == "fpu_transcendental"



def compact_exclusion_reasons(candidate: Candidate, compact_policy: dict[str, Any]) -> list[str]:
    labels = set(compact_policy["compact_exclude"])
    reasons: list[str] = []
    mnemonic = candidate.mnemonic.upper()
    group = candidate.group.upper()
    if "FPU" in labels and candidate.category == "fpu":
        reasons.append("FPU")
    if "transcendental_fpu" in labels and is_transcendental_fpu_candidate(candidate):
        reasons.append("transcendental_fpu")
    cache_mnemonics = mnemonic_policy_set(compact_policy, "cache_management_mnemonics")
    if "cache_management" in labels and (
        mnemonic in cache_mnemonics or "CACHE" in group or mnemonic == "PREFETCH"
    ):
        reasons.append("cache_management")
    tlb_mnemonics = mnemonic_policy_set(compact_policy, "tlb_management_mnemonics")
    if "tlb_management" in labels and (
        mnemonic in tlb_mnemonics
        or "TLB" in group
        or "PAGE" in group
        or "PT" in group
        or mnemonic.startswith("PT")
    ):
        reasons.append("tlb_management")
    core_control_mnemonics = mnemonic_policy_set(compact_policy, "core_control_compact_mnemonics")
    if (
        "system_core_except_core_control" in labels
        and candidate.category == "system"
        and mnemonic not in core_control_mnemonics
    ):
        reasons.append("system_core_except_core_control")
    return reasons


def compact_allowed(candidate: Candidate, compact_policy: dict[str, Any]) -> bool:
    if candidate.must_compact:
        return True
    return not compact_exclusion_reasons(candidate, compact_policy)


def compact_preference_reasons(candidate: Candidate, compact_policy: dict[str, Any]) -> list[str]:
    labels = set(compact_policy["compact_prefer"])
    reasons: list[str] = []
    mnemonic = candidate.mnemonic
    profile = "_TO_".join(profile_form_parts(candidate.compact_fields))
    size = size_tag_from_fields(candidate.compact_fields)
    if "D_D_integer_alu" in labels and mnemonic in {"ADD", "SUB", "AND", "OR", "XOR", "CMP", "TEST"} and all_direct_d(candidate.operands):
        reasons.append("D_D_integer_alu")
    if "MOV_LQ_EA_D" in labels and mnemonic == "MOV" and profile == "EA_TO_D" and size == "LQ":
        reasons.append("MOV_LQ_EA_D")
    if "MOV_LQ_D_EA" in labels and mnemonic == "MOV" and profile == "D_TO_EA" and size == "LQ":
        reasons.append("MOV_LQ_D_EA")
    if "INC_DEC_D" in labels and mnemonic in {"INC", "DEC"} and profile == "D":
        reasons.append("INC_DEC_D")
    if "PUSH_POP" in labels and mnemonic in {"PUSH", "POP"}:
        reasons.append("PUSH_POP")
    if "Jcc" in labels and mnemonic == "Jcc":
        reasons.append("Jcc")
    for exact in ("CALL", "RET", "NOP", "SYSCALL", "BKPT", "WAIT", "YIELD"):
        if exact in labels and mnemonic == exact:
            reasons.append(exact)
    if "fences" in labels and mnemonic.upper() in mnemonic_policy_set(compact_policy, "fence_mnemonics"):
        reasons.append("fences")
    return reasons


def is_integer_minmax_d_to_d(candidate: Candidate, compact_policy: dict[str, Any]) -> bool:
    return (
        candidate.mnemonic.upper() in mnemonic_policy_set(compact_policy, "integer_minmax_order")
        and "_TO_".join(profile_form_parts(candidate.compact_fields)) == "D_TO_D"
    )


def is_integer_mul_div_d_to_d(candidate: Candidate, compact_policy: dict[str, Any]) -> bool:
    return (
        candidate.mnemonic.upper() in mnemonic_policy_set(compact_policy, "integer_mul_div_compact_order")
        and "_TO_".join(profile_form_parts(candidate.compact_fields)) == "D_TO_D"
    )


def family_locality_prefers_root(compact_policy: dict[str, Any], family: str, root: str) -> bool:
    rules = compact_policy.get("family_locality", {})
    if not isinstance(rules, dict):
        return False
    family_rule = rules.get(family, {})
    if not isinstance(family_rule, dict) or not family_rule.get("prefer_contiguous_roots"):
        return False
    roots = family_rule.get("roots", [])
    return isinstance(roots, list) and root in {str(item) for item in roots}


def extension_root_policy(compact_policy: dict[str, Any]) -> dict[str, Any]:
    policy = compact_policy.get("extension_root_policy", {})
    return policy if isinstance(policy, dict) else {}


def extension_root_region_start(compact_policy: dict[str, Any]) -> int:
    policy = extension_root_policy(compact_policy)
    if str(policy.get("preferred_region", "")).lower() == "high_primary_payload":
        return HIGH_PRIMARY_PAYLOAD_START
    return 0


def extension_roots_allow_low_payload(compact_policy: dict[str, Any]) -> bool:
    policy = extension_root_policy(compact_policy)
    return bool(policy.get("allow_low_payload_roots", True))


def extension_roots_prefer_family_contiguity(compact_policy: dict[str, Any]) -> bool:
    policy = extension_root_policy(compact_policy)
    return bool(policy.get("prefer_contiguous_family_roots", True))


def compact_family_symmetry_policy(compact_policy: dict[str, Any]) -> dict[str, Any]:
    policy = compact_policy.get("compact_family_symmetry", {})
    return policy if isinstance(policy, dict) else {}


def compact_family_symmetry_enabled(compact_policy: dict[str, Any]) -> bool:
    policy = compact_family_symmetry_policy(compact_policy)
    return (
        str(policy.get("default_rule", "")).lower() == "all_or_none"
        and bool(policy.get("apply_to_all_instruction_families", False))
    )


def instruction_family_map(compact_policy: dict[str, Any]) -> dict[str, str]:
    out: dict[str, str] = {}
    for family, members in instruction_family_members(compact_policy).items():
        for member in members:
            out[str(member).upper()] = str(family)
    return out


def instruction_family_members(compact_policy: dict[str, Any]) -> dict[str, list[str]]:
    families = compact_policy.get("instruction_families", {})
    if not isinstance(families, dict):
        return {}
    out: dict[str, list[str]] = {}
    for family, body in families.items():
        members = body.get("members", []) if isinstance(body, dict) else body
        if not isinstance(members, list):
            continue
        out[str(family)] = [str(member) for member in members]
    return out


def instruction_family_rule(compact_policy: dict[str, Any], family: str) -> str:
    families = compact_policy.get("instruction_families", {})
    if isinstance(families, dict) and isinstance(families.get(family), dict):
        return str(families[family].get("compact_symmetry", "all_or_none"))
    policy = compact_family_symmetry_policy(compact_policy)
    return str(policy.get("default_rule", "all_or_none"))


def instruction_family_compact_preference(compact_policy: dict[str, Any], family: str) -> str:
    families = compact_policy.get("instruction_families", {})
    if isinstance(families, dict) and isinstance(families.get(family), dict):
        return str(families[family].get("compact_preference", "normal"))
    return "normal"


def compact_family_exception_members(compact_policy: dict[str, Any]) -> dict[str, set[str]]:
    policy = compact_family_symmetry_policy(compact_policy)
    out: dict[str, set[str]] = {}
    exceptions = policy.get("exceptions", [])
    if not isinstance(exceptions, list):
        return out
    for item in exceptions:
        if not isinstance(item, dict):
            continue
        name = str(item.get("name", ""))
        if not name:
            continue
        members = item.get("members", [])
        out[name] = {str(member).upper() for member in members} if isinstance(members, list) else set()
    return out


def compact_family_exception_for_candidate(candidate: Candidate, compact_policy: dict[str, Any]) -> str:
    exceptions = compact_family_exception_members(compact_policy)
    mnemonic = candidate.mnemonic.upper()
    if candidate.must_compact and "mandatory_compact" in exceptions:
        return "mandatory_compact"
    if mnemonic in exceptions.get("sentinel_or_control_singletons", set()):
        return "sentinel_or_control_singletons"
    alias_forms = {str(item).upper() for item in compact_policy.get("alias_form_mnemonics", [])}
    if mnemonic in alias_forms and "alias_forms" in exceptions:
        return "alias_forms"
    return ""


def compact_family_name(candidate: Candidate, compact_policy: dict[str, Any]) -> str:
    return instruction_family_map(compact_policy).get(candidate.mnemonic.upper(), "")


def compact_family_candidates(
    candidates: list[Candidate], compact_policy: dict[str, Any]
) -> dict[str, list[Candidate]]:
    grouped: dict[str, list[Candidate]] = {}
    if not compact_family_symmetry_enabled(compact_policy):
        return grouped
    for candidate in candidates:
        family = compact_family_name(candidate, compact_policy)
        if (
            not family
            or candidate.compact_slots is None
            or compact_family_exception_for_candidate(candidate, compact_policy)
            or instruction_family_rule(compact_policy, family).lower() != "all_or_none"
        ):
            continue
        grouped.setdefault(family, []).append(candidate)
    return grouped


def apply_compact_family_symmetry(
    candidates: list[Candidate], selected_compact: set[str], compact_policy: dict[str, Any]
) -> set[str]:
    if not compact_family_symmetry_enabled(compact_policy):
        return selected_compact
    selected = set(selected_compact)
    for family_members in compact_family_candidates(candidates, compact_policy).values():
        member_ids = {candidate.id for candidate in family_members}
        selected_ids = member_ids & selected
        if selected_ids and selected_ids != member_ids:
            selected -= selected_ids
    return selected


def compact_family_item_value(
    family: str, members: list[Candidate], compact_policy: dict[str, Any]
) -> int:
    preference = instruction_family_compact_preference(compact_policy, family).lower()
    if preference == "low":
        return 0
    base = sum(compact_value(candidate, compact_policy) for candidate in members)
    if preference == "high":
        return base + 2400 * len({candidate.mnemonic for candidate in members})
    return base


def compact_dp_items(
    optional: list[Candidate], compact_policy: dict[str, Any]
) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    grouped: dict[str, list[Candidate]] = {}
    grouped_ids: set[str] = set()
    if compact_family_symmetry_enabled(compact_policy):
        for candidate in optional:
            family = compact_family_name(candidate, compact_policy)
            if (
                not family
                or compact_family_exception_for_candidate(candidate, compact_policy)
                or instruction_family_rule(compact_policy, family).lower() != "all_or_none"
            ):
                continue
            grouped.setdefault(family, []).append(candidate)
            grouped_ids.add(candidate.id)
    for family, family_members in sorted(grouped.items()):
        members = sorted(family_members, key=candidate_sort_key)
        items.append(
            {
                "ids": tuple(candidate.id for candidate in members),
                "cost": sum(compact_slot_cost(candidate, compact_policy) for candidate in members),
                "value": compact_family_item_value(family, members, compact_policy),
            }
        )
    for candidate in optional:
        if candidate.id in grouped_ids:
            continue
        items.append(
            {
                "ids": (candidate.id,),
                "cost": compact_slot_cost(candidate, compact_policy),
                "value": compact_value(candidate, compact_policy),
            }
        )
    return items


def condition_reclaim_policy(compact_policy: dict[str, Any]) -> dict[str, Any]:
    policy = compact_policy.get("condition_field", {})
    if not isinstance(policy, dict):
        return {}
    reclaim = policy.get("reclaim_never_taken", {})
    return reclaim if isinstance(reclaim, dict) else {}


def reclaimed_condition_value(candidate: Candidate, compact_policy: dict[str, Any]) -> int | None:
    reclaim = condition_reclaim_policy(compact_policy)
    mnemonics = {str(item).upper() for item in reclaim.get("mnemonics", []) or []}
    if candidate.mnemonic.upper() not in mnemonics:
        return None
    value = reclaim.get("condition_value")
    if value is None:
        return None
    return int(str(value), 0)


def field_reclaim_policy(compact_policy: dict[str, Any]) -> dict[str, Any]:
    policy = compact_policy.get("field_reclaim", {})
    return policy if isinstance(policy, dict) else {}


def candidate_policy_context(candidate: Candidate) -> dict[str, str]:
    return {
        "mnemonic": candidate.mnemonic,
        "category": candidate.category,
        "semantic_family": candidate.group.split(".", 1)[0],
        "group": candidate.group,
        "profile": "_TO_".join(profile_form_parts(candidate.compact_fields)) or "NO_OPERANDS",
        "size": size_tag_from_fields(candidate.compact_fields),
    }


def compact_reclaim_filters(candidate: Candidate, compact_policy: dict[str, Any]) -> list[dict[str, Any]]:
    filters: list[dict[str, Any]] = []
    condition_value = reclaimed_condition_value(candidate, compact_policy)
    if condition_value is not None:
        filters.append(
            {
                "field_kind": "condition",
                "values": (condition_value,),
                "reason": "reclaimed condition value",
            }
        )

    policy = field_reclaim_policy(compact_policy)
    context = candidate_policy_context(candidate)
    for rule in policy.get("invalid_values", []) or []:
        if not isinstance(rule, dict) or not allocation_rule_matches(rule, context):
            continue
        values = tuple(int(str(value), 0) for value in rule.get("values", []) or [])
        if not values:
            continue
        filters.append(
            {
                "field_source": str(rule.get("field_source", "")),
                "field_name": str(rule.get("field_name", "")),
                "field_kind": str(rule.get("field_kind", "")),
                "values": values,
                "reason": str(rule.get("reason", "reclaimed invalid field value")),
            }
        )
    return filters


def field_get(field: Field | dict[str, Any], name: str, default: Any = "") -> Any:
    if isinstance(field, dict):
        return field.get(name, default)
    return getattr(field, name, default)


def field_matches_reclaim_filter(field: Field | dict[str, Any], reclaim_filter: dict[str, Any]) -> bool:
    source = str(reclaim_filter.get("field_source", ""))
    name = str(reclaim_filter.get("field_name", ""))
    kind = str(reclaim_filter.get("field_kind", ""))
    if source and str(field_get(field, "source", "")) != source:
        return False
    if name and str(field_get(field, "name", "")) != name:
        return False
    if kind and str(field_get(field, "kind", "")) != kind:
        return False
    return bool(source or name or kind)


def reclaim_filter_field_width(candidate: Candidate, reclaim_filter: dict[str, Any]) -> int:
    matches = [
        field
        for field in candidate.compact_fields
        if field.storage == "primary" and field.value is None and field_matches_reclaim_filter(field, reclaim_filter)
    ]
    if len(matches) != 1:
        return 0
    return int(matches[0].width)


def compact_slot_cost(candidate: Candidate, compact_policy: dict[str, Any]) -> int:
    slots = int(candidate.compact_slots or 0)
    if slots <= 0:
        return slots
    filters = compact_reclaim_filters(candidate, compact_policy)
    if not filters:
        return slots
    cost = slots
    seen_fields: set[tuple[str, str, str]] = set()
    for reclaim_filter in filters:
        key = (
            str(reclaim_filter.get("field_source", "")),
            str(reclaim_filter.get("field_name", "")),
            str(reclaim_filter.get("field_kind", "")),
        )
        if key in seen_fields:
            continue
        seen_fields.add(key)
        width = reclaim_filter_field_width(candidate, reclaim_filter)
        if width <= 0:
            continue
        invalid_values = {int(value) for value in reclaim_filter.get("values", ())}
        invalid_count = len([value for value in invalid_values if 0 <= value < (1 << width)])
        if invalid_count <= 0:
            continue
        cost = cost * ((1 << width) - invalid_count) // (1 << width)
    return cost


def payload_matches_reclaim_filter(payload: int, fields: list[dict[str, Any]], reclaim_filter: dict[str, Any]) -> bool:
    matches = [field for field in fields if field_matches_reclaim_filter(field, reclaim_filter)]
    if len(matches) != 1:
        return False
    field = matches[0]
    low_bit = int(field["low_bit"])
    width = int(field["width"])
    mask = (1 << width) - 1
    value = (payload >> low_bit) & mask
    return value in {int(item) for item in reclaim_filter.get("values", ())}


def candidate_sort_key(candidate: Candidate) -> tuple[int, int, int, str]:
    rank = {
        "sentinel": 0,
        "integer": 1,
        "data_movement": 2,
        "control_flow": 3,
        "system": 4,
        "fpu": 5,
        "misc": 6,
    }
    slots = candidate.compact_slots if candidate.compact_slots is not None else PRIMARY_SLOTS + 1
    return (rank.get(candidate.category, 99), -candidate.weight, slots, candidate.id)


def solve_allocation(
    candidates: list[Candidate],
    z3: Any,
    compact_policy: dict[str, Any],
    alias_rules: list[dict[str, Any]],
) -> dict[str, Any]:
    selected_compact = select_compact_profiles(candidates, compact_policy)
    selected_compact, extended_candidates, extension_roots = enforce_symmetry_and_capacity(
        candidates, selected_compact, compact_policy
    )
    if any(not candidate.can_extend for candidate in extended_candidates):
        bad = [candidate.id for candidate in extended_candidates if not candidate.can_extend]
        return {"status": "unsat", "reason": f"non-extendable candidates not compact: {', '.join(bad)}"}
    overfull_roots = [root for root in extension_roots if len(root["members"]) > EXTENDED_SLOTS]
    if overfull_roots:
        names = ", ".join(str(root["id"]) for root in overfull_roots)
        return {"status": "unsat", "reason": f"extended roots are full: {names}"}

    solver = z3.Solver()
    compact_slot_sum = sum(
        compact_slot_cost(candidate, compact_policy) if candidate.compact_slots is not None else PRIMARY_SLOTS + 1
        for candidate in candidates
        if candidate.id in selected_compact
    )
    extension_root_slots = sum(int(root["slots"]) for root in extension_roots)
    solver.add(compact_slot_sum + extension_root_slots + PRIMARY_EXTENSION_HEADROOM_SLOTS <= PRIMARY_SLOTS)
    for root in extension_roots:
        solver.add(len(root["members"]) <= EXTENDED_SLOTS)
    status = solver.check()
    if status != z3.sat:
        return {"status": str(status), "allocations": []}

    field_layout_model = build_field_layout_model(
        candidates,
        selected_compact,
        extended_candidates,
        compact_policy,
    )
    primary_allocations, used, packed_roots = pack_primary_allocations(
        candidates, selected_compact, extension_roots, compact_policy, field_layout_model
    )
    extended_allocations = pack_extended_allocations(
        extended_candidates, packed_roots, compact_policy, field_layout_model
    )
    primary_aliases = compact_conditional_alias_allocations(primary_allocations, alias_rules)
    extended_aliases = extended_conditional_alias_allocations(extended_allocations, alias_rules)
    evictions = eviction_report(candidates, selected_compact, compact_policy)
    policy_report = compact_policy_report(candidates, selected_compact, compact_policy)
    family_symmetry = compact_family_symmetry_audit(candidates, selected_compact, compact_policy)
    symmetry = symmetry_audit(selected_compact, primary_allocations, extended_allocations, compact_policy)
    alias_audit = conditional_alias_audit(primary_aliases, extended_aliases, alias_rules)
    decode_cost = decode_cost_audit(primary_allocations, compact_policy)
    extended_used_slots = sum(int(item.get("extended_opcode_slots", 1)) for item in extended_allocations)
    extended_total_slots = len(extension_roots) * EXTENDED_SLOTS

    return {
        "status": str(status),
        "slot_count": PRIMARY_SLOTS,
        "candidate_count": len(candidates),
        "primary_used_slot_count": len(used),
        "primary_free_slot_count": PRIMARY_SLOTS - len(used),
        "primary_headroom_target": PRIMARY_EXTENSION_HEADROOM_SLOTS,
        "compact_count": sum(1 for item in primary_allocations if item["kind"] == "compact"),
        "extended_count": len(extended_allocations),
        "extension_root_count": len(extension_roots),
        "extension_root_slot_count": extension_root_slots,
        "extended_opcode_slot_count": EXTENDED_SLOTS,
        "extended_total_opcode_slot_count": extended_total_slots,
        "extended_used_opcode_count": extended_used_slots,
        "extended_free_opcode_count": extended_total_slots - extended_used_slots,
        "extension_root_usage": extension_root_usage(packed_roots, extended_allocations),
        "profile_selection": "weighted_compact_knapsack_with_z3_capacity_check",
        "compact_policy": policy_report,
        "decode_cost_audit": decode_cost,
        "field_layout_model": field_layout_model_report(field_layout_model),
        "compact_family_symmetry_audit": family_symmetry,
        "symmetry_audit": symmetry,
        "conditional_alias_audit": alias_audit,
        "free_ranges": free_ranges(used, PRIMARY_SLOTS),
        "primary_allocations": primary_allocations,
        "primary_alias_allocations": primary_aliases,
        "extension_roots": packed_roots,
        "extended_allocations": extended_allocations,
        "extended_alias_allocations": extended_aliases,
        "compact_evictions": evictions,
    }


def select_compact_profiles(candidates: list[Candidate], compact_policy: dict[str, Any]) -> set[str]:
    selected = {candidate.id for candidate in candidates if candidate.must_compact}
    fixed_slots = sum(compact_slot_cost(candidate, compact_policy) for candidate in candidates if candidate.id in selected)
    capacity = PRIMARY_SLOTS - fixed_slots - PRIMARY_EXTENSION_HEADROOM_SLOTS
    if capacity < 0:
        raise ValueError("mandatory compact candidates leave no primary headroom")

    optional = [
        candidate
        for candidate in sorted(candidates, key=candidate_sort_key)
        if candidate.id not in selected
        and candidate.compact_slots is not None
        and compact_allowed(candidate, compact_policy)
    ]
    dp: list[tuple[int, tuple[str, ...]]] = [(0, ()) for _ in range(capacity + 1)]
    for item in compact_dp_items(optional, compact_policy):
        cost = int(item["cost"])
        if cost <= 0 or cost > capacity:
            continue
        value = int(item["value"])
        ids = tuple(str(ident) for ident in item["ids"])
        for used in range(capacity, cost - 1, -1):
            old_score, old_items = dp[used]
            prev_score, prev_items = dp[used - cost]
            score = prev_score + value
            if score > old_score:
                dp[used] = (score, prev_items + ids)

    best_score = max(score for score, _items in dp)
    best_used, best_items = min(
        (used, items)
        for used, (score, items) in enumerate(dp)
        if score == best_score
    )
    _ = best_used
    return selected | set(best_items)


def enforce_symmetry_and_capacity(
    candidates: list[Candidate], selected_compact: set[str], compact_policy: dict[str, Any]
) -> tuple[set[str], list[Candidate], list[dict[str, Any]]]:
    selected = set(selected_compact)
    for _attempt in range(len(candidates) + 1):
        before = set(selected)
        selected = apply_compact_family_symmetry(candidates, selected, compact_policy)
        extended_candidates = [candidate for candidate in candidates if candidate.id not in selected]
        extension_roots = build_extension_roots(extended_candidates, compact_policy)
        selected, extended_candidates, extension_roots = enforce_primary_capacity(
            candidates, selected, extended_candidates, extension_roots, compact_policy
        )
        if selected == before:
            return selected, extended_candidates, extension_roots
    raise RuntimeError("compact family symmetry did not converge")


def enforce_primary_capacity(
    candidates: list[Candidate],
    selected_compact: set[str],
    extended_candidates: list[Candidate],
    extension_roots: list[dict[str, Any]],
    compact_policy: dict[str, Any],
) -> tuple[set[str], list[Candidate], list[dict[str, Any]]]:
    by_id = {candidate.id: candidate for candidate in candidates}
    while True:
        compact_slots = sum(
            compact_slot_cost(by_id[ident], compact_policy)
            if by_id[ident].compact_slots is not None
            else PRIMARY_SLOTS + 1
            for ident in selected_compact
        )
        root_slots = sum(int(root["slots"]) for root in extension_roots)
        if compact_slots + root_slots + PRIMARY_EXTENSION_HEADROOM_SLOTS <= PRIMARY_SLOTS:
            return selected_compact, extended_candidates, extension_roots

        eviction = choose_capacity_eviction(selected_compact, by_id, compact_policy)
        if eviction is None:
            raise ValueError("unable to fit compact forms, natural extension roots, and primary headroom")
        selected_compact.remove(eviction.id)
        extended_candidates.append(eviction)
        extension_roots = build_extension_roots(extended_candidates, compact_policy)


def choose_capacity_eviction(
    selected_compact: set[str], by_id: dict[str, Candidate], compact_policy: dict[str, Any]
) -> Candidate | None:
    optional = [
        by_id[ident]
        for ident in selected_compact
        if not by_id[ident].must_compact and by_id[ident].compact_slots is not None
    ]
    if not optional:
        return None
    return min(
        optional,
        key=lambda candidate: (
            compact_value(candidate, compact_policy) / max(1, compact_slot_cost(candidate, compact_policy)),
            compact_value(candidate, compact_policy),
            candidate.id,
        ),
    )


def compact_value(candidate: Candidate, compact_policy: dict[str, Any]) -> int:
    if candidate.compact_slots is None:
        return 0
    density_bonus = max(1, candidate.descriptor_words + 1)
    regularity_bonus = 200 if has_regular_primary_layout(candidate.compact_fields) else 0
    preference_bonus = 1600 if compact_preference_reasons(candidate, compact_policy) else 0
    return candidate.weight * density_bonus + regularity_bonus + preference_bonus


def has_regular_primary_layout(fields: tuple[Field, ...]) -> bool:
    names = {field.name for field in fields if field.storage == "primary"}
    if "e" in names:
        return True
    if "c" in names and len(names) <= 2:
        return True
    return bool(names)


def primary_cluster_name(candidate: Candidate) -> str:
    if candidate.allocation_cluster:
        return candidate.allocation_cluster
    mnemonic = candidate.mnemonic
    if mnemonic in {"PUSHM", "POPM", "MOVSETAD", "MOVSETDA", "XCHGSETAD", "XCHGSETDA"}:
        return "bitmap_ops"
    if mnemonic in {"PUSH", "POP"}:
        return "stack_ops"
    if mnemonic in {"RESET", "SYSRET", "IRET"}:
        return "core_control"
    return ""


def primary_cluster_sort_key(candidate: Candidate) -> tuple[int, str]:
    order = {
        "CALL.IMM32": -2,
        "CALL.IMM64": -1,
        "PUSHM": 0,
        "POPM": 1,
        "MOVSETAD": 2,
        "MOVSETDA": 3,
        "XCHGSETAD": 4,
        "XCHGSETDA": 5,
        "PUSH": 10,
        "POP": 20,
        "RESET": 30,
        "SYSRET": 31,
        "IRET": 32,
    }
    profile = "_TO_".join(profile_form_parts(candidate.compact_fields))
    if candidate.mnemonic in {"PUSH", "POP"} and profile == "D":
        return (order[candidate.mnemonic], candidate.id)
    if candidate.mnemonic in {"PUSH", "POP"} and profile == "A":
        return (order[candidate.mnemonic] + 1, candidate.id)
    return (order.get(candidate.id, order.get(candidate.mnemonic, 99)), candidate.id)


def primary_cluster_order(compact_policy: dict[str, Any]) -> list[str]:
    policy = compact_policy.get("primary_clusters", {})
    order = policy.get("order", []) if isinstance(policy, dict) else []
    if isinstance(order, list):
        return [str(item) for item in order]
    return default_primary_clusters_policy()["order"]


def ordered_primary_variables(candidates: list[Candidate], compact_policy: dict[str, Any]) -> list[Candidate]:
    clusters = primary_cluster_order(compact_policy)
    out: list[Candidate] = []
    used: set[str] = set()
    for cluster in clusters:
        members = [candidate for candidate in candidates if primary_cluster_name(candidate) == cluster]
        members.sort(key=primary_cluster_sort_key)
        out.extend(members)
        used.update(candidate.id for candidate in members)
    extra_clusters = sorted(
        {
            primary_cluster_name(candidate)
            for candidate in candidates
            if candidate.id not in used and primary_cluster_name(candidate)
        }
    )
    for cluster in extra_clusters:
        members = [candidate for candidate in candidates if candidate.id not in used and primary_cluster_name(candidate) == cluster]
        members.sort(key=primary_cluster_sort_key)
        out.extend(members)
        used.update(candidate.id for candidate in members)

    remaining = [candidate for candidate in candidates if candidate.id not in used]
    remaining.sort(key=lambda candidate: (-(candidate.compact_slots or 0), candidate_sort_key(candidate)))
    out.extend(remaining)
    return out


def ordered_extension_root_groups(
    extension_roots: list[dict[str, Any]], compact_policy: dict[str, Any]
) -> list[list[dict[str, Any]]]:
    if not extension_roots_prefer_family_contiguity(compact_policy):
        return [[root] for root in sorted(extension_roots, key=extension_root_sort_key)]
    groups: dict[str, list[dict[str, Any]]] = {}
    for root in sorted(extension_roots, key=extension_root_sort_key):
        groups.setdefault(str(root["family"]), []).append(root)
    return [
        sorted(
            members,
            key=lambda root: (-int(root.get("slots", 1)), extension_root_sort_key(root)),
        )
        for _family, members in sorted(
            groups.items(), key=lambda item: (EXTENSION_FAMILY_RANK.get(item[0], 99), item[0])
        )
    ]


def pack_primary_allocations(
    candidates: list[Candidate],
    selected_compact: set[str],
    extension_roots: list[dict[str, Any]],
    compact_policy: dict[str, Any],
    field_layout_model: dict[str, Any],
) -> tuple[list[dict[str, Any]], set[int], list[dict[str, Any]]]:
    used: set[int] = set()
    allocations: list[dict[str, Any]] = []
    by_id = {candidate.id: candidate for candidate in candidates}

    fixed = sorted(
        [candidate for candidate in candidates if candidate.id in selected_compact and candidate.fixed_payload is not None],
        key=lambda candidate: int(candidate.fixed_payload or 0),
    )
    for candidate in fixed:
        payload = int(candidate.fixed_payload or 0)
        if payload in used:
            raise RuntimeError(f"fixed payload collision at 0x{payload:03x}")
        used.add(payload)
        allocations.append(primary_allocation_dict(candidate, payload, payload, "compact", field_layout_model))

    variable = ordered_primary_variables(
        [
            by_id[ident]
            for ident in selected_compact
            if by_id[ident].fixed_payload is None
        ],
        compact_policy,
    )
    for candidate in variable:
        span_slots = int(candidate.compact_slots or 0)
        start = find_free_range(used, span_slots, alignment=max(1, span_slots), limit=PRIMARY_SLOTS)
        end = start + span_slots - 1
        allocation = primary_allocation_dict(candidate, start, end, "compact", field_layout_model)
        exact_payloads = compact_exact_primary_payloads(candidate, allocation, compact_policy)
        if exact_payloads:
            reclaimed = sorted(set(range(start, end + 1)) - set(exact_payloads))
            allocation["primary_payloads"] = [f"0x{payload:03x}" for payload in exact_payloads]
            allocation["reclaimed_payloads"] = [f"0x{payload:03x}" for payload in reclaimed]
            allocation["slots"] = len(exact_payloads)
            if reclaimed:
                allocation["field_layout"] = f"{allocation['field_layout']} ; reclaims {len(reclaimed)} invalid payload slots"
            for payload in exact_payloads:
                used.add(payload)
        else:
            for payload in range(start, end + 1):
                used.add(payload)
        allocations.append(allocation)

    packed_roots = []
    root_cursor = extension_root_region_start(compact_policy)
    for group in ordered_extension_root_groups(extension_roots, compact_policy):
        total_slots = sum(int(root["slots"]) for root in group)
        alignment = max(1, max(int(root["slots"]) for root in group))
        try:
            start = find_free_range(used, total_slots, alignment=alignment, limit=PRIMARY_SLOTS, min_start=root_cursor)
        except RuntimeError:
            if not extension_roots_allow_low_payload(compact_policy):
                raise
            start = find_free_range(used, total_slots, alignment=alignment, limit=PRIMARY_SLOTS)
        offset = start
        for root in group:
            slots = int(root["slots"])
            end = offset + slots - 1
            for payload in range(offset, end + 1):
                used.add(payload)
            packed = dict(root)
            packed.update(
                {
                    "start_payload": f"0x{offset:03x}",
                    "end_payload": f"0x{end:03x}",
                }
            )
            packed_roots.append(packed)
            allocations.append(extension_root_allocation_dict(packed))
            offset = end + 1
        root_cursor = offset

    allocations.sort(key=lambda item: int(str(item["start_payload"]), 16))
    packed_roots.sort(key=lambda item: int(str(item["start_payload"]), 16))
    return allocations, used, packed_roots


def primary_allocation_dict(
    candidate: Candidate, start: int, end: int, kind: str, field_layout_model: dict[str, Any]
) -> dict[str, Any]:
    fields = assign_field_positions(candidate.compact_fields, PRIMARY_BITS, "primary", field_layout_model)
    return {
        "id": profile_candidate_id(candidate, candidate.compact_fields),
        "kind": kind,
        "mnemonic": candidate.mnemonic,
        "category": candidate.category,
        "group": candidate.group,
        "origin": candidate.origin,
        "operands": list(candidate.operands),
        "primary_bits": candidate.compact_bits,
        "slots": end - start + 1,
        "start_payload": f"0x{start:03x}",
        "end_payload": f"0x{end:03x}",
        "field_layout": layout_text(fields),
        "fields": fields,
        "weight": candidate.weight,
        "shape_hint": candidate.shape_hint,
        "min_words": candidate.min_words,
        "max_words": candidate.max_words,
        "privilege": candidate.privilege,
        **({"fixed_size_suffix": candidate.fixed_size_suffix} if candidate.fixed_size_suffix else {}),
    }


def compact_exact_primary_payloads(
    candidate: Candidate, allocation: dict[str, Any], compact_policy: dict[str, Any]
) -> list[int]:
    filters = compact_reclaim_filters(candidate, compact_policy)
    if not filters:
        return []
    start = int(str(allocation["start_payload"]), 16)
    end = int(str(allocation["end_payload"]), 16)
    fields = list(allocation.get("fields", []) or [])
    return [
        payload
        for payload in range(start, end + 1)
        if not any(payload_matches_reclaim_filter(payload, fields, reclaim_filter) for reclaim_filter in filters)
    ]



def build_extension_roots(candidates: list[Candidate], compact_policy: dict[str, Any]) -> list[dict[str, Any]]:
    roots: dict[str, dict[str, Any]] = {}
    for candidate in candidates:
        key = extension_root_key(candidate, compact_policy)
        if key not in roots:
            roots[key] = extension_root_dict(key, candidate, compact_policy)
        roots[key]["members"].append(profile_candidate_id(candidate, candidate.descriptor_fields))
    return sorted(roots.values(), key=extension_root_sort_key)


def extension_root_key(candidate: Candidate, compact_policy: dict[str, Any]) -> str:
    family = extension_family_name(candidate)
    root_policy = compact_policy.get("extension_roots", {})
    group_by = str(root_policy.get("group_by", "semantic_family")) if isinstance(root_policy, dict) else "semantic_family"
    condition_in_primary = bool(root_policy.get("condition_field_in_primary", True)) if isinstance(root_policy, dict) else True
    carries_condition = any(field.kind == "condition" for field in candidate.descriptor_fields)
    if group_by == "semantic_family":
        if condition_in_primary and carries_condition:
            return f"{family}.cc"
        return family
    profile = "_TO_".join(profile_form_parts(candidate.descriptor_fields)) or "NO_OPERANDS"
    size = size_tag_from_fields(candidate.descriptor_fields)
    if size and size not in {"Q", "LQ"}:
        return f"{family}.{profile}.{size}"
    return f"{family}.{profile}"


def extension_root_dict(key: str, candidate: Candidate, compact_policy: dict[str, Any]) -> dict[str, Any]:
    carries_condition = any(field.kind == "condition" for field in candidate.descriptor_fields)
    root_policy = compact_policy.get("extension_roots", {})
    condition_in_primary = bool(root_policy.get("condition_field_in_primary", True)) if isinstance(root_policy, dict) else True
    slots = 16 if carries_condition and condition_in_primary else 1
    primary_bits = 4 if carries_condition and condition_in_primary else 0
    layout = (
        "c[3:0] subop/operands in following word"
        if carries_condition and condition_in_primary
        else "subop/operands in following word"
    )
    return {
        "id": f"EXT.{key}",
        "key": key,
        "family": extension_family_name(candidate),
        "profile": "_TO_".join(profile_form_parts(candidate.descriptor_fields)) or "NO_OPERANDS",
        "size": size_tag_from_fields(candidate.descriptor_fields),
        "slots": slots,
        "primary_bits": primary_bits,
        "field_layout": layout,
        "members": [],
        "opcode_capacity": EXTENDED_SLOTS,
    }


def extension_family_name(candidate: Candidate) -> str:
    if candidate.extension_family:
        return candidate.extension_family
    group = candidate.group.upper()
    mnemonic = candidate.mnemonic.upper()
    if mnemonic in {"LEA", "SEGLEA", "TESTCANON"}:
        return "ea_utility"
    if mnemonic == "PREFETCH":
        return "cache_hint"
    if candidate.category == "data_movement":
        return "data_movement"
    if any(field.kind == "condition" for field in candidate.descriptor_fields):
        return "conditional_control"
    if candidate.category == "control_flow":
        return "control_flow"
    if candidate.category == "fpu":
        if is_transcendental_fpu_candidate(candidate):
            return "fpu_transcendental"
        if any(key in mnemonic for key in ("MOV", "CMP", "TEST", "CLASS", "CVT")):
            return "fpu_move_compare"
        return "fpu_arithmetic"
    if mnemonic.startswith("FETCH") or mnemonic == "CMPXCHG":
        return "atomic_memory"
    if any(key in group or key in mnemonic for key in ("TLB", "CACHE", "PAGE", "PT", "VTOP")):
        return "tlb_cache"
    if candidate.category == "system":
        return "system_core"
    if any(key in group for key in ("MULTIPLY", "DIV", "MOD", "CARRYLESS")):
        return "integer_mul_div"
    if any(key in group for key in ("BIT", "SHIFT")):
        return "integer_bitfield"
    if candidate.category == "integer":
        return "integer_alu"
    return "misc"


def extension_root_sort_key(root: dict[str, Any]) -> tuple[int, int, int, str]:
    family = str(root["family"])
    profile = str(root["profile"])
    profile_rank = EXTENSION_PROFILE_RANK.get(family, {}).get(profile, 99)
    return (EXTENSION_FAMILY_RANK.get(family, 99), profile_rank, -len(root["members"]), str(root["key"]))


def extension_root_allocation_dict(root: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": root["id"],
        "kind": "extension_root",
        "mnemonic": "EXT",
        "category": "extended",
        "group": root["family"],
        "operands": [],
        "primary_bits": root["primary_bits"],
        "slots": root["slots"],
        "start_payload": root["start_payload"],
        "end_payload": root["end_payload"],
        "field_layout": root["field_layout"],
        "member_count": len(root["members"]),
        "origin": "allocator",
        "weight": 0,
    }


FPU_COMPARE_PAIR_MNEMONICS = {"FCMP", "FTEST"}


def fpu_compare_source_operand(operands: list[Any] | tuple[Any, ...]) -> str:
    parsed = [(str(operand).split(":", 1)[0].lower(), str(operand)) for operand in operands]
    for source, operand in parsed:
        if source == "src":
            return operand
    for source, operand in parsed:
        if source != "dst":
            return operand
    return parsed[0][1] if parsed else ""


def fpu_compare_source_profile(operands: list[Any] | tuple[Any, ...]) -> str:
    source = fpu_compare_source_operand(operands)
    return form_name((source,)) or "NO_SOURCE"


def fpu_compare_source_rank(profile: str) -> int:
    return {"F": 0, "EA": 1}.get(profile, 99)


def extended_pair_profile(candidate: Candidate) -> str:
    if candidate.mnemonic in FPU_COMPARE_PAIR_MNEMONICS:
        return f"FCMP_FTEST.{fpu_compare_source_profile(candidate.operands)}"
    return candidate.id


def extended_pair_rank(candidate: Candidate) -> tuple[int, int, str, int, str]:
    if candidate.mnemonic in FPU_COMPARE_PAIR_MNEMONICS:
        source_profile = fpu_compare_source_profile(candidate.operands)
        return (
            0,
            fpu_compare_source_rank(source_profile),
            f"FCMP_FTEST.{source_profile}",
            0 if candidate.mnemonic == "FCMP" else 1,
            candidate.id,
        )
    order = {
        "FMOV": 2,
        "RDCR": 10,
        "WRCR": 11,
        "RDSEG": 12,
        "WRSEG": 13,
        "RDFLAGS": 14,
        "WRFLAGS": 15,
        "RDSTATUS": 16,
        "WRSTATUS": 17,
        "SAVE": 20,
        "RESTORE": 21,
        "INVTLB": 30,
        "INVPAGE": 31,
        "INVASID": 32,
        "SWPT": 40,
        "SWPTA": 41,
        "INVDCACHE": 60,
        "WRBKDCACHE": 61,
        "FLSHDCACHE": 62,
        "INVICACHE": 63,
        "SYNCCACHE": 64,
    }
    return (order.get(candidate.mnemonic, 100), 0, candidate.id, 0, candidate.id)


def extended_pair_min_start(
    candidate: Candidate,
    root_id: str,
    packed_allocations: list[dict[str, Any]],
    window_start: int,
) -> int:
    if candidate.mnemonic != "FTEST":
        return window_start
    source_profile = fpu_compare_source_profile(candidate.operands)
    predecessors = [
        item
        for item in packed_allocations
        if item.get("extension_root") == root_id
        and item.get("mnemonic") == "FCMP"
        and fpu_compare_source_profile(item.get("operands", []) or []) == source_profile
    ]
    if not predecessors:
        return window_start
    predecessor_end = max(extended_opcode_range(item)[1] for item in predecessors)
    return max(window_start, predecessor_end + 1)


def extended_candidate_sort_key(
    candidate: Candidate, compact_policy: dict[str, Any]
) -> tuple[int, str, tuple[int, int, str, int, str], tuple[int, int, int, str]]:
    family = extension_family_name(candidate)
    return (
        EXTENSION_FAMILY_RANK.get(family, 99),
        extension_root_key(candidate, compact_policy),
        extended_pair_rank(candidate),
        candidate_sort_key(candidate),
    )


def pack_extended_allocations(
    candidates: list[Candidate],
    extension_roots: list[dict[str, Any]],
    compact_policy: dict[str, Any],
    field_layout_model: dict[str, Any],
) -> list[dict[str, Any]]:
    out = []
    root_by_key = {str(root["key"]): root for root in extension_roots}
    opcode_plans = build_extended_opcode_plans(candidates, compact_policy)
    used_by_root = {str(root["key"]): set() for root in extension_roots}
    for candidate in sorted(candidates, key=lambda item: extended_candidate_sort_key(item, compact_policy)):
        root_key = extension_root_key(candidate, compact_policy)
        root = root_by_key[root_key]
        opcode_plan = opcode_plans[candidate.id]
        slots = int(opcode_plan["slots"])
        window_start, window_end = fixed_high_field_window(candidate)
        min_start = extended_pair_min_start(candidate, str(root["id"]), out, window_start)
        opcode_start = find_free_range(
            used_by_root[root_key],
            slots,
            alignment=max(1, slots),
            limit=window_end + 1,
            min_start=min_start,
        )
        opcode_end = opcode_start + slots - 1
        if opcode_end > window_end:
            raise RuntimeError(f"unable to pack {candidate.id} inside fixed-field extension window")
        for opcode in range(opcode_start, opcode_end + 1):
            used_by_root[root_key].add(opcode)
        descriptor_layout = extended_field_layout_text(
            candidate.descriptor_fields,
            field_layout_model,
            bool(opcode_plan["spilled"]),
        )
        out.append(
            {
                "extension_root": root["id"],
                "extension_root_payload": root_payload_text(root),
                "extension_family": root["family"],
                "extended_opcode": extended_opcode_text(opcode_start, opcode_end),
                "extended_opcode_start": f"0x{opcode_start:04x}",
                "extended_opcode_end": f"0x{opcode_end:04x}",
                "extended_opcode_slots": slots,
                "extended_opcode_bits": int(opcode_plan["opcode_bits"]),
                "operand_payload_bits": int(opcode_plan["payload_bits"]),
                "operand_descriptor_spilled": bool(opcode_plan["spilled"]),
                "extended_selector": f"{root['id']}:{extended_opcode_text(opcode_start, opcode_end)}",
                "id": profile_candidate_id(candidate, candidate.descriptor_fields),
                "mnemonic": candidate.mnemonic,
                "category": candidate.category,
                "group": candidate.group,
                "origin": candidate.origin,
                "operands": list(candidate.operands),
                "operand_descriptor_bits": candidate.descriptor_bits,
                "operand_descriptor_words": ceil_words(int(opcode_plan["payload_bits"])),
                "descriptor_layout": descriptor_layout,
                "fields": [field_dict(field) for field in candidate.descriptor_fields],
                "weight": candidate.weight,
                "compact_bits_if_one_word": candidate.compact_bits,
                "primary_slots_if_one_word": candidate.compact_slots,
                "eviction_reason": eviction_reason(candidate),
                "shape_hint": candidate.shape_hint,
                "min_words": candidate.min_words,
                "max_words": candidate.max_words,
                "privilege": candidate.privilege,
                **({"fixed_size_suffix": candidate.fixed_size_suffix} if candidate.fixed_size_suffix else {}),
            }
        )
    return sorted(
        out,
        key=lambda item: (
            int(str(item["extension_root_payload"]).split("..", 1)[0], 16),
            int(str(item["extended_opcode_start"]), 16),
            str(item["id"]),
        ),
    )


def fixed_high_field_window(candidate: Candidate) -> tuple[int, int]:
    prefix = 0
    prefix_bits = 0
    for field in fixed_high_fields(candidate):
        prefix = (prefix << field.width) | int(field.value or 0)
        prefix_bits += field.width
    remaining = EXTENDED_BITS - prefix_bits
    start = prefix << remaining
    return start, start + (1 << remaining) - 1


def fixed_high_fields(candidate: Candidate) -> list[Field]:
    return [
        field
        for field in candidate.descriptor_fields
        if field.storage == "descriptor" and field.value is not None and field.placement == "high"
    ]


def fixed_high_field_layout(candidate: Candidate) -> str:
    parts = []
    high = EXTENDED_BITS - 1
    for field in fixed_high_fields(candidate):
        low = high - field.width + 1
        label = field.value_label or str(field.value)
        parts.append(f"{field.name}:{field.kind}={label}{bit_range(high, low)}")
        high = low - 1
    return ", ".join(parts)


def build_extended_opcode_plans(
    candidates: list[Candidate], compact_policy: dict[str, Any]
) -> dict[str, dict[str, int | bool]]:
    grouped: dict[str, list[Candidate]] = {}
    for candidate in candidates:
        grouped.setdefault(extension_root_key(candidate, compact_policy), []).append(candidate)

    plans: dict[str, dict[str, int | bool]] = {}
    for root_key, members in grouped.items():
        spilled: set[str] = set()
        while True:
            total = 0
            impossible: list[Candidate] = []
            for candidate in members:
                bits = extended_opcode_bits(candidate, candidate.id in spilled)
                if bits > EXTENDED_BITS:
                    impossible.append(candidate)
                    continue
                total += 1 << bits
            if not impossible and total <= EXTENDED_SLOTS:
                break
            spill = choose_extended_spill_candidate(members, spilled)
            if spill is None:
                raise RuntimeError(f"extension root {root_key} is full")
            spilled.add(spill.id)

        for candidate in members:
            is_spilled = candidate.id in spilled
            opcode_bits = extended_opcode_bits(candidate, is_spilled)
            payload_bits = extended_payload_bits(candidate, is_spilled)
            plans[candidate.id] = {
                "opcode_bits": opcode_bits,
                "payload_bits": payload_bits,
                "slots": 1 << opcode_bits,
                "spilled": is_spilled,
            }
    return plans


def choose_extended_spill_candidate(members: list[Candidate], spilled: set[str]) -> Candidate | None:
    candidates = [candidate for candidate in members if candidate.id not in spilled]
    if not candidates:
        return None

    def spill_key(candidate: Candidate) -> tuple[float, int, int, str]:
        bits = extended_opcode_bits(candidate, spilled=False)
        savings = max(1, (1 << min(bits, EXTENDED_BITS + 1)) - 1)
        return (
            candidate.weight / savings,
            candidate.weight,
            -bits,
            candidate.id,
        )

    return min(candidates, key=spill_key)


def extended_opcode_bits(candidate: Candidate, spilled: bool) -> int:
    if spilled:
        return 0
    return sum(
        field.width
        for field in candidate.descriptor_fields
        if field.storage == "descriptor" and field.kind != "condition" and field.value is None
    )


def extended_payload_bits(candidate: Candidate, spilled: bool) -> int:
    payload = sum(field.width for field in candidate.descriptor_fields if field.storage == "payload")
    if spilled:
        payload += sum(
            field.width
            for field in candidate.descriptor_fields
            if field.storage == "descriptor" and field.kind != "condition" and field.value is None
        )
    return payload


def extended_opcode_text(start: int, end: int) -> str:
    if start == end:
        return f"0x{start:04x}"
    return f"0x{start:04x}..0x{end:04x}"


def compact_conditional_alias_allocations(
    primary_allocations: list[dict[str, Any]], alias_rules: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    aliases: list[dict[str, Any]] = []
    rules_by_target = alias_rules_by_target(alias_rules)
    for allocation in primary_allocations:
        rule = rules_by_target.get(str(allocation.get("mnemonic")))
        if not rule or allocation.get("kind") != "compact":
            continue
        payloads = alias_payloads(
            int(str(allocation["start_payload"]), 16),
            int(str(allocation["end_payload"]), 16),
            int(rule["condition_value"]),
        )
        if not payloads:
            continue
        alias_mnemonic = str(rule["alias"])
        fields = [field for field in allocation.get("fields", []) if field.get("kind") != "condition"]
        operands = [operand for operand in allocation.get("operands", []) if operand_norm(str(operand)) != "CONDITION"]
        alias = {
            **allocation,
            "id": alias_id(str(allocation["id"]), alias_mnemonic, str(rule["target"])),
            "kind": "compact_alias",
            "mnemonic": alias_mnemonic,
            "operands": operands,
            "primary_bits": sum(int(field.get("width", 0)) for field in fields),
            "slots": 0,
            "start_payload": f"0x{payloads[0]:03x}",
            "end_payload": f"0x{payloads[-1]:03x}",
            "alias_payloads": [f"0x{payload:03x}" for payload in payloads],
            "alias_of": allocation["id"],
            "alias_condition": rule["condition"],
            "canonical_disassembly": alias_mnemonic,
            "field_layout": alias_field_layout(allocation.get("fields", []), rule),
            "fields": fields,
        }
        aliases.append(alias)
    return sorted(aliases, key=allocation_start)


def extended_conditional_alias_allocations(
    extended_allocations: list[dict[str, Any]], alias_rules: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    aliases: list[dict[str, Any]] = []
    rules_by_target = alias_rules_by_target(alias_rules)
    for allocation in extended_allocations:
        rule = rules_by_target.get(str(allocation.get("mnemonic")))
        if not rule:
            continue
        fields = [field for field in allocation.get("fields", []) if field.get("kind") != "condition"]
        if len(fields) == len(allocation.get("fields", [])):
            continue
        root_start, root_end = parse_payload_range(str(allocation["extension_root_payload"]))
        payloads = alias_payloads(root_start, root_end, int(rule["condition_value"]))
        if not payloads:
            continue
        alias_mnemonic = str(rule["alias"])
        operands = [operand for operand in allocation.get("operands", []) if operand_norm(str(operand)) != "CONDITION"]
        alias = {
            **allocation,
            "id": alias_id(str(allocation["id"]), alias_mnemonic, str(rule["target"])),
            "kind": "extended_alias",
            "mnemonic": alias_mnemonic,
            "operands": operands,
            "operand_descriptor_bits": sum(
                int(field.get("width", 0))
                for field in fields
                if field.get("storage") in {"descriptor", "payload"} and field.get("kind") != "condition"
            ),
            "descriptor_layout": alias_descriptor_layout(allocation.get("fields", []), rule),
            "fields": fields,
            "extension_root_payload": (
                f"0x{payloads[0]:03x}" if len(payloads) == 1 else f"0x{payloads[0]:03x}..0x{payloads[-1]:03x}"
            ),
            "alias_payloads": [f"0x{payload:03x}" for payload in payloads],
            "alias_of": allocation["id"],
            "alias_condition": rule["condition"],
            "canonical_disassembly": alias_mnemonic,
        }
        aliases.append(alias)
    return sorted(
        aliases,
        key=lambda item: (
            int(str(item["extension_root_payload"]).split("..", 1)[0], 16),
            int(str(item.get("extended_opcode_start", item["extended_opcode"]).split("..", 1)[0]), 16),
            str(item["id"]),
        ),
    )


def alias_payloads(start: int, end: int, condition_value: int) -> list[int]:
    return [payload for payload in range(start, end + 1) if (payload & 0xF) == condition_value]


def parse_payload_range(text: str) -> tuple[int, int]:
    if ".." not in text:
        value = int(text, 16)
        return value, value
    start, end = text.split("..", 1)
    return int(start, 16), int(end, 16)


def alias_id(target_id: str, alias_mnemonic: str, target_mnemonic: str) -> str:
    if target_id == target_mnemonic:
        return alias_mnemonic
    if target_id.startswith(f"{target_mnemonic}."):
        return alias_mnemonic + target_id.removeprefix(target_mnemonic)
    return alias_mnemonic


def alias_field_layout(fields: list[dict[str, Any]], rule: dict[str, Any]) -> str:
    layout_fields = [field for field in fields if field.get("kind") != "condition"]
    condition_high = max(
        (int(field.get("high_bit", -1)) for field in fields if field.get("kind") == "condition"),
        default=-1,
    )
    parts = [f"c={rule['condition_value']}({rule['condition']})"]
    parts.extend(
        f"{field['name']}{field['range']}"
        for field in sorted(layout_fields, key=lambda item: int(item.get("low_bit", 0)))
    )
    highest = max([condition_high] + [int(field.get("high_bit", -1)) for field in layout_fields])
    if highest + 1 < PRIMARY_BITS:
        parts.append(f"op[{PRIMARY_BITS - 1}:{highest + 1}]")
    return " ".join(parts)


def alias_descriptor_layout(fields: list[dict[str, Any]], rule: dict[str, Any]) -> str:
    condition_text = f"c={rule['condition_value']}({rule['condition']})"
    parts = [f"{condition_text}@root"]
    for field in fields:
        if field.get("kind") == "condition":
            continue
        storage = "payload" if field.get("storage") == "payload" else "ext"
        parts.append(f"{field['name']}:{field['kind']}/{field['width']}@{storage}")
    return ", ".join(parts)


def root_payload_text(root: dict[str, Any]) -> str:
    if root["start_payload"] == root["end_payload"]:
        return str(root["start_payload"])
    return f"{root['start_payload']}..{root['end_payload']}"


def extension_root_usage(
    roots: list[dict[str, Any]], allocations: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    counts = {str(root["id"]): 0 for root in roots}
    members = {str(root["id"]): 0 for root in roots}
    for allocation in allocations:
        root = str(allocation["extension_root"])
        counts[root] += int(allocation.get("extended_opcode_slots", 1))
        members[root] += 1
    return [
        {
            "root": root["id"],
            "payload": root_payload_text(root),
            "family": root["family"],
            "profile": root["profile"],
            "members": members[str(root["id"])],
            "used": counts[str(root["id"])],
            "capacity": EXTENDED_SLOTS,
            "free": EXTENDED_SLOTS - counts[str(root["id"])],
        }
        for root in roots
    ]


def compact_policy_report(
    candidates: list[Candidate], selected_compact: set[str], compact_policy: dict[str, tuple[str, ...]]
) -> dict[str, Any]:
    by_id = {candidate.id: candidate for candidate in candidates}
    selected = [by_id[ident] for ident in selected_compact]
    excluded = [
        candidate
        for candidate in candidates
        if candidate.compact_slots is not None and compact_exclusion_reasons(candidate, compact_policy)
    ]
    violations = [
        {
            "id": profile_candidate_id(candidate, candidate.compact_fields),
            "reasons": compact_exclusion_reasons(candidate, compact_policy),
        }
        for candidate in selected
        if not candidate.must_compact and compact_exclusion_reasons(candidate, compact_policy)
    ]
    preferred_selected = [
        candidate for candidate in selected if compact_preference_reasons(candidate, compact_policy)
    ]
    return {
        "compact_exclude": list(compact_policy["compact_exclude"]),
        "compact_prefer": list(compact_policy["compact_prefer"]),
        "excluded_candidate_count": len(excluded),
        "selected_preferred_count": len(preferred_selected),
        "selected_nonpreferred_count": len(selected) - len(preferred_selected),
        "violation_count": len(violations),
        "violations": violations,
    }


def allocation_start(allocation: dict[str, Any]) -> int:
    return int(str(allocation["start_payload"]), 16)


def allocation_end(allocation: dict[str, Any]) -> int:
    return int(str(allocation["end_payload"]), 16)


def primary_cluster_span(primary_allocations: list[dict[str, Any]], mnemonics: set[str]) -> dict[str, Any]:
    items = [item for item in primary_allocations if item.get("mnemonic") in mnemonics and item.get("kind") == "compact"]
    if not items:
        return {"count": 0, "span": 0, "slots": 0}
    start = min(allocation_start(item) for item in items)
    end = max(allocation_end(item) for item in items)
    slots = sum(int(item["slots"]) for item in items)
    return {"count": len(items), "span": end - start + 1, "slots": slots}


def extension_root_profile(root_id: str, family: str) -> str:
    prefix = f"EXT.{family}."
    if not root_id.startswith(prefix):
        return ""
    return root_id.removeprefix(prefix).split(".")[0]


def extension_root_cluster_span(
    primary_allocations: list[dict[str, Any]], family: str, profiles: tuple[str, ...]
) -> dict[str, Any]:
    expected = set(profiles)
    items = [
        item
        for item in primary_allocations
        if item.get("kind") == "extension_root"
        and item.get("group") == family
        and extension_root_profile(str(item.get("id", "")), family) in expected
    ]
    if not items:
        return {"count": 0, "span": 0, "slots": 0, "profiles": [], "payloads": []}
    items.sort(key=allocation_start)
    start = min(allocation_start(item) for item in items)
    end = max(allocation_end(item) for item in items)
    slots = sum(int(item["slots"]) for item in items)
    return {
        "count": len(items),
        "span": end - start + 1,
        "slots": slots,
        "profiles": [extension_root_profile(str(item["id"]), family) for item in items],
        "payloads": [root_payload_text(item) for item in items],
    }


def extended_by_id(extended_allocations: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {str(item["id"]): item for item in extended_allocations}


def root_opcode_values(extended_allocations: list[dict[str, Any]], root: str, mnemonics: set[str]) -> list[int]:
    values = []
    for item in extended_allocations:
        if item.get("extension_root") != root or item.get("mnemonic") not in mnemonics:
            continue
        values.append(int(str(item.get("extended_opcode_start", item["extended_opcode"])).split("..", 1)[0], 16))
    return sorted(values)


def extended_opcode_range(allocation: dict[str, Any]) -> tuple[int, int]:
    start = allocation.get("extended_opcode_start")
    end = allocation.get("extended_opcode_end")
    if start is not None and end is not None:
        return int(str(start), 16), int(str(end), 16)
    text = str(allocation.get("extended_opcode", "0x0000"))
    if ".." not in text:
        value = int(text, 16)
        return value, value
    left, right = text.split("..", 1)
    return int(left, 16), int(right, 16)


def opcode_ranges_touch(left: dict[str, Any], right: dict[str, Any]) -> bool:
    left_start, left_end = extended_opcode_range(left)
    right_start, right_end = extended_opcode_range(right)
    return left_end + 1 == right_start or right_end + 1 == left_start


def opcode_range_text(allocation: dict[str, Any]) -> str:
    start, end = extended_opcode_range(allocation)
    return f"0x{start:04x}" if start == end else f"0x{start:04x}..0x{end:04x}"


def alias_form_prefix(mnemonic: str, form_types: list[str]) -> str:
    profile = form_name(tuple(form_types))
    return mnemonic if not profile else f"{mnemonic}.{profile}"


def conditional_alias_audit(
    primary_aliases: list[dict[str, Any]],
    extended_aliases: list[dict[str, Any]],
    alias_rules: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    aliases = primary_aliases + extended_aliases

    def has_alias(alias_prefix: str, target_prefix: str, condition: str) -> bool:
        return any(
            (
                str(item.get("id", "")) == alias_prefix
                or str(item.get("id", "")).startswith(f"{alias_prefix}.")
            )
            and str(item.get("alias_of", "")).startswith(target_prefix)
            and str(item.get("alias_condition", "")) == condition
            for item in aliases
        )

    checks: list[dict[str, Any]] = []
    for rule in alias_rules:
        alias_mnemonic = str(rule["alias"])
        target_mnemonic = str(rule["target"])
        condition = str(rule["condition"])
        forms = rule.get("required_target_forms", []) or [[]]
        missing = []
        for form_types in forms:
            alias_prefix = alias_form_prefix(alias_mnemonic, [str(item) for item in form_types])
            target_prefix = alias_form_prefix(target_mnemonic, [str(item) for item in form_types])
            if not has_alias(alias_prefix, target_prefix, condition):
                missing.append(f"{alias_prefix}->{target_prefix}")
        alias_ids = sorted(str(item["id"]) for item in aliases if item.get("mnemonic") == alias_mnemonic)
        checks.append(
            {
                "name": f"{alias_mnemonic}_aliases_{target_mnemonic}_{condition}",
                "status": "pass" if not missing else "fail",
                "detail": f"aliases={alias_ids if alias_ids else 'none'}"
                if not missing
                else f"missing={missing}; aliases={alias_ids if alias_ids else 'none'}",
            }
        )
    return checks


def decode_cost_audit(
    primary_allocations: list[dict[str, Any]], compact_policy: dict[str, Any]
) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []

    def add(name: str, ok: bool, detail: str, severity: str = "medium") -> None:
        checks.append({"name": name, "status": "pass" if ok else "fail", "severity": severity, "detail": detail})

    decode_policy = compact_policy.get("decode_cost_policy", {})
    if isinstance(decode_policy, dict):
        priority = [str(item) for item in decode_policy.get("priority_order", []) or []]
        if priority:
            checks.append(
                {
                    "name": "decode_cost_priority_order",
                    "status": "info",
                    "severity": "info",
                    "detail": " > ".join(priority),
                }
            )

    large_ranges = [
        item
        for item in primary_allocations
        if item.get("kind") == "compact" and int(item.get("slots", 0)) > 1
    ]

    def allocation_alignment_span(item: dict[str, Any]) -> int:
        if item.get("primary_payloads"):
            return allocation_end(item) - allocation_start(item) + 1
        return int(item["slots"])

    misaligned = [
        f"{item['id']}@{item['start_payload']}/{allocation_alignment_span(item)}"
        for item in large_ranges
        if allocation_start(item) % allocation_alignment_span(item) != 0
    ]
    add(
        "aligned_large_ranges",
        not misaligned,
        "all multi-slot compact ranges start on their range-size alignment"
        if not misaligned
        else f"misaligned={misaligned}",
    )

    roots = [item for item in primary_allocations if item.get("kind") == "extension_root"]
    min_start = extension_root_region_start(compact_policy)
    low_roots = [
        f"{item['id']}@{item['start_payload']}"
        for item in roots
        if allocation_start(item) < min_start
    ]
    allow_low = extension_roots_allow_low_payload(compact_policy)
    add(
        "extension_roots_high_primary_payload",
        allow_low or not low_roots,
        f"min_payload=0x{min_start:03x}, low_roots={low_roots if low_roots else 'none'}",
        severity="high",
    )

    family_breaks = []
    roots_by_family: dict[str, list[dict[str, Any]]] = {}
    for root in roots:
        roots_by_family.setdefault(str(root.get("group", "")), []).append(root)
    for family, family_roots in roots_by_family.items():
        if len(family_roots) <= 1:
            continue
        start = min(allocation_start(root) for root in family_roots)
        end = max(allocation_end(root) for root in family_roots)
        slots = sum(int(root["slots"]) for root in family_roots)
        if end - start + 1 != slots:
            family_breaks.append(f"{family}:span={end - start + 1},slots={slots}")
    add(
        "extension_family_root_contiguity",
        not family_breaks,
        "extension roots are contiguous within each family" if not family_breaks else f"breaks={family_breaks}",
    )

    compact_singletons = [
        item for item in primary_allocations if item.get("kind") == "compact" and int(item.get("slots", 0)) == 1
    ]
    checks.append(
        {
            "name": "compact_singleton_count",
            "status": "info",
            "severity": "low",
            "detail": f"{len(compact_singletons)} one-slot compact patterns after family clustering",
        }
    )
    return checks


def compact_family_symmetry_audit(
    candidates: list[Candidate], selected_compact: set[str], compact_policy: dict[str, Any]
) -> list[dict[str, Any]]:
    policy = compact_family_symmetry_policy(compact_policy)
    if not policy:
        return []
    report_all = bool((policy.get("audit") or {}).get("report_all_families", False)) if isinstance(policy.get("audit"), dict) else False
    report_exceptions = bool((policy.get("audit") or {}).get("report_exceptions", False)) if isinstance(policy.get("audit"), dict) else False
    checks: list[dict[str, Any]] = []

    if report_exceptions:
        exception_names = [str(item.get("name", "")) for item in policy.get("exceptions", []) or [] if isinstance(item, dict)]
        for name in exception_names:
            matched = [
                candidate
                for candidate in candidates
                if compact_family_exception_for_candidate(candidate, compact_policy) == name
            ]
            mnemonics = sorted({candidate.mnemonic for candidate in matched})
            checks.append(
                {
                    "family": f"exception:{name}",
                    "status": "info",
                    "rule": "exception",
                    "preference": "exception",
                    "compact": sum(1 for candidate in matched if candidate.id in selected_compact),
                    "total": len(matched),
                    "detail": f"mnemonics={mnemonics if mnemonics else 'none'}",
                }
            )

    grouped = compact_family_candidates(candidates, compact_policy)
    family_names = list(grouped)
    if report_all:
        families = compact_policy.get("instruction_families", {})
        if isinstance(families, dict):
            family_names = list(dict.fromkeys(list(families) + family_names))

    for family in family_names:
        members = grouped.get(family, [])
        selected = [candidate for candidate in members if candidate.id in selected_compact]
        compact_ids = [profile_candidate_id(candidate, candidate.compact_fields) for candidate in selected]
        if not members:
            status = "info"
            detail = "no non-exception candidates in this family"
        elif not selected:
            status = "pass"
            detail = "all extended"
        elif len(selected) == len(members):
            status = "pass"
            detail = "all compact"
        else:
            status = "fail"
            detail = f"partial compact={compact_ids}"
        checks.append(
            {
                "family": family,
                "status": status,
                "rule": instruction_family_rule(compact_policy, family),
                "preference": instruction_family_compact_preference(compact_policy, family),
                "compact": len(selected),
                "total": len(members),
                "detail": detail,
            }
        )
    return checks


def symmetry_audit(
    selected_compact: set[str],
    primary_allocations: list[dict[str, Any]],
    extended_allocations: list[dict[str, Any]],
    compact_policy: dict[str, Any],
) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []

    def add(name: str, ok: bool, detail: str, severity: str = "medium") -> None:
        checks.append({"name": name, "status": "pass" if ok else "fail", "severity": severity, "detail": detail})

    _ = selected_compact
    minmax_mnemonics = mnemonic_policy_set(compact_policy, "integer_minmax_order")
    minmax_selected = sorted(
        str(item["id"])
        for item in primary_allocations
        if str(item.get("mnemonic")).upper() in minmax_mnemonics and str(item.get("id", "")).endswith(".D_TO_D")
    )
    add(
        "integer_minmax_all_or_none",
        len(minmax_selected) in {0, len(minmax_mnemonics)},
        "no integer min/max D_TO_D forms selected compact"
        if not minmax_selected
        else f"compact min/max forms={minmax_selected}",
    )

    mul_div_mnemonics = mnemonic_policy_set(compact_policy, "integer_mul_div_compact_order")
    mul_div_selected = sorted(
        str(item["id"])
        for item in primary_allocations
        if str(item.get("mnemonic")).upper() in mul_div_mnemonics
        and str(item.get("id", "")).endswith(".D_TO_D")
    )
    add(
        "integer_mul_div_compact_recommended_none",
        len(mul_div_selected) == 0,
        "no integer MUL/DIV/MOD D_TO_D forms selected compact"
        if not mul_div_selected
        else f"compact MUL/DIV/MOD forms={mul_div_selected}",
    )

    stack = primary_cluster_span(primary_allocations, {"PUSH", "POP"})
    add(
        "stack_push_pop_nearby",
        stack["count"] == 4 and stack["span"] == stack["slots"],
        f"span={stack['span']} slots={stack['slots']} count={stack['count']}",
    )

    direct_call = primary_cluster_span(primary_allocations, {"CALL"})
    add(
        "direct_call_immediates_clustered",
        direct_call["count"] == 2 and direct_call["span"] == direct_call["slots"],
        f"span={direct_call['span']} slots={direct_call['slots']} count={direct_call['count']}",
        severity="low",
    )

    bitmap = primary_cluster_span(primary_allocations, {"PUSHM", "POPM", "MOVSETAD", "MOVSETDA", "XCHGSETAD", "XCHGSETDA"})
    add(
        "bitmap_ops_clustered",
        bitmap["count"] == 6 and bitmap["span"] == bitmap["slots"],
        f"span={bitmap['span']} slots={bitmap['slots']} count={bitmap['count']}",
    )

    by_id = extended_by_id(extended_allocations)
    prefetch = by_id.get("PREFETCH.EA")
    prefetch_root = str(prefetch.get("extension_root", "")) if prefetch else ""
    add(
        "cache_hint_family",
        prefetch is not None and prefetch_root.startswith("EXT.cache_hint"),
        f"PREFETCH root={prefetch_root if prefetch else 'missing'}",
    )

    utility_ids = ["LEA.EA_TO_A", "SEGLEA.EA_TO_A", "TESTCANON.EA"]
    primary_by_id = {str(item["id"]): item for item in primary_allocations}
    compact_utility = sorted(item for item in utility_ids if item in primary_by_id)
    utility_roots = {str(by_id[item]["extension_root"]) for item in utility_ids if item in by_id}
    add(
        "ea_utility_family",
        bool(compact_utility)
        or (len(utility_roots) > 0 and all(root.startswith("EXT.ea_utility") for root in utility_roots)),
        f"compact={compact_utility if compact_utility else 'none'} roots={sorted(utility_roots)}",
    )

    extension_roots = [item for item in primary_allocations if item.get("kind") == "extension_root"]
    integer_alu_family_roots = [item for item in extension_roots if item.get("group") == "integer_alu"]
    integer_alu = extension_root_cluster_span(primary_allocations, "integer_alu", ("EA_TO_D", "EA_TO_A", "D_TO_EA"))
    integer_alu_ok = (
        len(integer_alu_family_roots) == 1
        and str(integer_alu_family_roots[0].get("id")) == "EXT.integer_alu"
    ) or (
        integer_alu["profiles"] == ["EA_TO_D", "EA_TO_A", "D_TO_EA"]
        and integer_alu["span"] == integer_alu["slots"]
    )
    add(
        "integer_alu_root_locality",
        integer_alu_ok,
        (
            f"family_roots={[item.get('id') for item in integer_alu_family_roots]} "
            f"profiles={integer_alu['profiles']} payloads={integer_alu['payloads']} "
            f"span={integer_alu['span']} slots={integer_alu['slots']}"
        ),
    )

    for root in sorted(
        {
            str(item["extension_root"])
            for item in extended_allocations
            if item.get("mnemonic") in FPU_COMPARE_PAIR_MNEMONICS
        }
    ):
        pairs = []
        ok = True
        tests_by_source: dict[str, list[dict[str, Any]]] = {}
        for test_item in extended_allocations:
            if test_item.get("extension_root") != root or test_item.get("mnemonic") != "FTEST":
                continue
            source_profile = fpu_compare_source_profile(test_item.get("operands", []) or [])
            tests_by_source.setdefault(source_profile, []).append(test_item)
        for items in tests_by_source.values():
            items.sort(key=lambda item: str(item["id"]))
        for cmp_item in sorted(
            (item for item in extended_allocations if item.get("extension_root") == root and item.get("mnemonic") == "FCMP"),
            key=lambda item: (
                fpu_compare_source_rank(fpu_compare_source_profile(item.get("operands", []) or [])),
                str(item["id"]),
            ),
        ):
            source_profile = fpu_compare_source_profile(cmp_item.get("operands", []) or [])
            candidates = tests_by_source.get(source_profile, [])
            test_item = next((item for item in candidates if opcode_ranges_touch(cmp_item, item)), None)
            if test_item is None and candidates:
                test_item = candidates[0]
            test_id = str(test_item["id"]) if test_item else f"FTEST.{source_profile}"
            pair_ok = test_item is not None and opcode_ranges_touch(cmp_item, test_item)
            ok = ok and pair_ok
            pairs.append(
                f"{cmp_item['id']}[{source_profile}]={opcode_range_text(cmp_item)} "
                f"{test_id}={opcode_range_text(test_item) if test_item else 'missing'}"
            )
        add(
            f"fpu_compare_pair_{root}",
            ok,
            "; ".join(pairs),
            severity="low",
        )

    return checks


def eviction_report(
    candidates: list[Candidate], selected_compact: set[str], compact_policy: dict[str, tuple[str, ...]]
) -> list[dict[str, Any]]:
    evicted = [
        candidate
        for candidate in candidates
        if candidate.id not in selected_compact and candidate.compact_slots is not None and candidate.can_extend
    ]
    evicted.sort(key=lambda candidate: (-compact_value(candidate, compact_policy), candidate.id))
    return [
        {
            "evicted_instruction": profile_candidate_id(candidate, candidate.descriptor_fields),
            "replacement_instruction": "higher weighted compact set",
            "estimated_frequency_delta": candidate.weight,
            "estimated_code_size_delta": f"compact would require {candidate.compact_slots} primary slots",
            "decode_complexity_delta": "moved to extended opcode word with generated operand descriptor",
            "affected_instruction_families": [candidate.group],
        }
        for candidate in evicted[:32]
    ]


def eviction_reason(candidate: Candidate) -> str:
    if candidate.compact_slots is None:
        if candidate.compact_bits <= PRIMARY_BITS:
            return "compact form disabled by allocation policy"
        return f"requires {candidate.compact_bits} one-word field bits, exceeding {PRIMARY_BITS}"
    return f"compact form costs {candidate.compact_slots} primary slots; lower weighted than selected compact set"


def find_free_range(used: set[int], slots: int, *, alignment: int, limit: int, min_start: int = 0) -> int:
    if slots <= 0:
        raise ValueError("slot count must be positive")
    start = min_start
    while start + slots <= limit:
        if alignment > 1:
            remainder = start % alignment
            if remainder:
                start += alignment - remainder
                continue
        if all(payload not in used for payload in range(start, start + slots)):
            return start
        start += 1
    raise RuntimeError(f"unable to pack {slots} slots")



def free_ranges(used_slots: set[int], limit: int) -> list[dict[str, Any]]:
    ranges = []
    start: int | None = None
    previous: int | None = None
    for slot in range(limit):
        if slot in used_slots:
            if start is not None and previous is not None:
                ranges.append(range_dict(start, previous))
            start = None
            previous = None
            continue
        if start is None:
            start = slot
        previous = slot
    if start is not None and previous is not None:
        ranges.append(range_dict(start, previous))
    return ranges


def range_dict(start: int, end: int) -> dict[str, Any]:
    return {
        "start_slot": start,
        "end_slot": end,
        "count": end - start + 1,
        "start_payload": f"0x{start:03x}",
        "end_payload": f"0x{end:03x}",
    }


def write_text(path: str | None, text: str) -> None:
    if not path or path == "-":
        sys.stdout.write(text)
        return
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(text, encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("spec_dir", nargs="?", default="isa/spec")
    parser.add_argument("-o", "--output", default="build/generated/allocation_plan.json")
    parser.add_argument("--md-output", default="build/generated/opcode_allocation.md")
    args = parser.parse_args(argv)

    spec, result, entries = load_and_validate(args.spec_dir)
    print_result(result)
    if not result.ok:
        return 1

    try:
        import z3  # type: ignore
    except ImportError:
        print("Z3 is not installed; allocation inputs validated but no solve was run.")
        print("Install z3-solver to enable opcode-space exploration.")
        return 1

    candidates = collect_candidates(spec, entries)
    alignment = audit_alignment(spec, entries, candidates)
    for check in alignment:
        print(f"{check['status']}: {check['name']}: {check['detail']}")
    if has_alignment_failure(alignment):
        print("Alignment audit failed; allocation solve was not run.", file=sys.stderr)
        return 1

    allocation = allocation_params(spec)
    compact_policy = normalize_compact_policy(allocation)
    root_policy = allocation.get("extension_roots", {}) if isinstance(allocation, dict) else {}
    if isinstance(root_policy, dict):
        compact_policy["extension_roots"] = {
            **compact_policy.get("extension_roots", {}),
            **root_policy,
        }
        extension_policy = dict(compact_policy.get("extension_root_policy", {}))
        if "preferred_region" in root_policy:
            extension_policy["preferred_region"] = root_policy["preferred_region"]
        if "allow_low_payload_roots" in root_policy:
            extension_policy["allow_low_payload_roots"] = root_policy["allow_low_payload_roots"]
        compact_policy["extension_root_policy"] = extension_policy
    field_layout_policy = allocation.get("field_layout", {}) if isinstance(allocation, dict) else {}
    if isinstance(field_layout_policy, dict):
        compact_policy["field_layout"] = field_layout_policy
    condition_field_policy = allocation.get("condition_field", {}) if isinstance(allocation, dict) else {}
    if isinstance(condition_field_policy, dict):
        compact_policy["condition_field"] = condition_field_policy
    field_reclaim_policy_value = allocation.get("field_reclaim", {}) if isinstance(allocation, dict) else {}
    if isinstance(field_reclaim_policy_value, dict):
        compact_policy["field_reclaim"] = field_reclaim_policy_value
    primary_clusters_policy = allocation.get("primary_clusters", {}) if isinstance(allocation, dict) else {}
    if isinstance(primary_clusters_policy, dict):
        compact_policy["primary_clusters"] = {
            **compact_policy.get("primary_clusters", {}),
            **primary_clusters_policy,
        }
    alias_rules = canonical_alias_rules(spec)
    compact_policy["alias_form_mnemonics"] = canonical_alias_family_mnemonics(spec)
    solver_result = solve_allocation(candidates, z3, compact_policy, alias_rules)
    if solver_result["status"] != "sat":
        print(f"Z3 allocation failed: {solver_result.get('reason', solver_result['status'])}", file=sys.stderr)
        return 1
    failed_alias_checks = [
        item for item in solver_result.get("conditional_alias_audit", []) if item.get("status") != "pass"
    ]
    if failed_alias_checks:
        for item in failed_alias_checks:
            print(
                f"Conditional alias audit failed: {item.get('name')}: {item.get('detail')}",
                file=sys.stderr,
            )
        return 1

    plan = {
        "z3_version": z3.get_version_string(),
        "target_space": {
            "id": PRIMARY_SPACE_ID,
            "bits": PRIMARY_BITS,
            "payload_range": "0x000..0xfff",
            "reserved_unallocated_headroom_slots": PRIMARY_EXTENSION_HEADROOM_SLOTS,
        },
        "extended_space": {
            "id": EXTENDED_SPACE_ID,
            "bits": EXTENDED_BITS,
            "root_model": "natural_family_roots",
            "opcode_range": "0x0000..0xffff",
        },
        "all_candidates_same_allocation_pool": True,
        "objectives": [
            "generate_operand_field_layouts_from_semantic_operands",
            "maximize_weighted_one_word_encodings",
            "report_extended_opcode_and_operand_descriptor_costs",
            "preserve_regular_operand_field_positions_from_layout_similarity",
        ],
        "allocation_policy_source": "instructions.yaml allocation model plus declarative instruction/EA/opcode catalogs",
        "alignment_audit": alignment,
        "solver": solver_result,
        "primary_allocations": solver_result["primary_allocations"],
        "primary_alias_allocations": solver_result["primary_alias_allocations"],
        "extended_allocations": solver_result["extended_allocations"],
        "extended_alias_allocations": solver_result["extended_alias_allocations"],
    }
    write_text(args.output, json_dumps(plan))
    if args.md_output:
        write_text(args.md_output, render_markdown(plan))

    print(
        "Z3 "
        f"{z3.get_version_string()} allocated {solver_result['candidate_count']} candidates; "
        f"{solver_result['compact_count']} one-word compact profiles and "
        f"{solver_result['extended_count']} extended profiles selected."
    )
    print(f"Wrote {args.output} and {args.md_output}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
