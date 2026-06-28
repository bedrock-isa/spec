"""Validation checks for generated allocation candidates."""

from __future__ import annotations

from typing import Any

from isa_spec import PatternEntry
from alloc_model import Candidate, Field

def audit_alignment(spec: dict[str, Any], entries: list[PatternEntry], candidates: list[Candidate]) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []

    def add(name: str, ok: bool, detail: str) -> None:
        checks.append({"name": name, "status": "pass" if ok else "fail", "detail": detail})

    registers = spec["registers"].get("register_classes", {})
    d_count = int(registers.get("D", {}).get("count", 0) or 0)
    a_count = int(registers.get("A", {}).get("count", 0) or 0)
    d_width = int(registers.get("D", {}).get("width", 0) or 0)
    a_width = int(registers.get("A", {}).get("width", 0) or 0)
    add(
        "D register class",
        d_count > 0 and d_width > 0,
        f"register class D count={d_count}, width={d_width}",
    )
    add(
        "A register class",
        a_count > 0 and a_width > 0,
        f"register class A count={a_count}, width={a_width}",
    )

    prefix_by_name = {item.get("name"): item for item in spec["prefixes"].get("prefixes", []) or []}
    rep = prefix_by_name.get("REPcc", {})
    rep_syntax = rep.get("syntax", {}) if isinstance(rep, dict) else {}
    rep_condition = rep.get("condition", {}) if isinstance(rep, dict) else {}
    rep_operand = rep.get("operand", {}) if isinstance(rep, dict) else {}
    add(
        "REPcc prefix metadata",
        isinstance(rep, dict)
        and bool(rep.get("pattern"))
        and bool(rep_condition.get("field"))
        and bool(rep_operand.get("field"))
        and bool(rep_syntax.get("mnemonic_template")),
        (
            f"condition field={rep_condition.get('field')}, "
            f"counter field={rep_operand.get('field')}, aliases={sorted((rep_syntax.get('aliases') or {}).keys())}"
        ),
    )

    repg = prefix_by_name.get("REPG", {})
    repg_syntax = repg.get("syntax", {}) if isinstance(repg, dict) else {}
    repg_operand = repg.get("operand", {}) if isinstance(repg, dict) else {}
    repg_alignment = repg.get("alignment", {}) if isinstance(repg, dict) else {}
    terminator = repg_syntax.get("terminator_prefix")
    terminator_prefix = prefix_by_name.get(terminator)
    try:
        grouping_window_bytes = int(repg_alignment.get("grouping_window_bytes", 0) or 0)
    except (TypeError, ValueError):
        grouping_window_bytes = 0
    add(
        "grouped repeat prefix metadata",
        isinstance(repg, dict)
        and bool(repg.get("pattern"))
        and bool(repg_operand.get("field"))
        and bool(repg_syntax.get("block"))
        and isinstance(terminator_prefix, dict)
        and grouping_window_bytes > 0,
        (
            f"terminator={repg_syntax.get('terminator_prefix')}, "
            f"counter field={repg_operand.get('field')}, grouping window={repg_alignment.get('grouping_window_bytes')} bytes"
        ),
    )

    raw_ea_forms = spec["ea"].get("ea_forms", []) or []
    compact_ea_forms = raw_ea_forms.get("compact", []) if isinstance(raw_ea_forms, dict) else raw_ea_forms
    raw_extended_ea_forms = spec["ea"].get("extended_ea_forms", []) or []
    ea_forms = {
        item.get("name")
        for item in compact_ea_forms
        if item.get("update_eligible") is True
    }
    ext_modes = {
        item.get("name")
        for item in raw_extended_ea_forms
        if item.get("update_eligible") is True
    }
    update_prefixes = [
        prefix
        for prefix in spec["prefixes"].get("prefixes", []) or []
        if isinstance(prefix, dict) and prefix.get("group") == "ea_update"
    ]
    add(
        "address-update operand coverage",
        bool(ea_forms or ext_modes)
        and all((prefix.get("requires") or {}).get("update_eligible_ea") is True for prefix in update_prefixes),
        f"compact update forms={sorted(ea_forms)}, extended update modes={sorted(ext_modes)}",
    )

    compact_names = {str(item.get("name")) for item in compact_ea_forms}
    extended_names = {str(item.get("name")) for item in raw_extended_ea_forms}
    ea_audit = spec["ea"].get("ea_coverage_audit", {}) or {}
    required_compact = {str(name) for name in ea_audit.get("required_compact_ea_forms", []) or []}
    required_extended = {str(name) for name in ea_audit.get("required_extended_ea_forms", []) or []}
    missing_compact = sorted(required_compact - compact_names)
    missing_extended = sorted(required_extended - extended_names)
    add(
        "EA compact coverage",
        not missing_compact,
        f"{len(required_compact)} required compact forms covered"
        if not missing_compact
        else f"missing compact forms={missing_compact}",
    )
    add(
        "EA extended coverage",
        not missing_extended,
        f"{len(required_extended)} required extended forms covered"
        if not missing_extended
        else f"missing extended forms={missing_extended}",
    )

    ea_policy = spec["ea"].get("ea_operand_policy", {}) or {}
    ea_sets = ea_policy.get("ea_sets", {}) or {}
    add(
        "EA operand policy",
        bool(ea_sets),
        f"{len(ea_sets)} EA sets",
    )

    canonical_rules = spec["opcodes"].get("canonical_rules", []) or []
    malformed_canonical_rules = [
        str(rule.get("id", index))
        for index, rule in enumerate(canonical_rules)
        if not isinstance(rule, dict) or not rule.get("canonical") or not rule.get("noncanonical")
    ]
    add(
        "canonical encoding rules",
        bool(canonical_rules) and not malformed_canonical_rules,
        f"{len(canonical_rules)} canonical rules"
        if canonical_rules and not malformed_canonical_rules
        else f"malformed canonical rules={malformed_canonical_rules}",
    )

    fixed = {candidate.id: candidate.fixed_payload for candidate in candidates if candidate.fixed_payload is not None}
    fixed_values = [int(value) for value in fixed.values() if value is not None]
    fixed_in_range = [value for value in fixed_values if 0 <= value < (1 << 12)]
    duplicate_fixed = sorted({value for value in fixed_values if fixed_values.count(value) > 1})
    add(
        "fixed primary payloads",
        len(fixed_in_range) == len(fixed_values) and not duplicate_fixed,
        f"fixed={fixed}"
        if len(fixed_in_range) == len(fixed_values) and not duplicate_fixed
        else f"duplicate_or_out_of_range={duplicate_fixed}",
    )

    impossible_must = [candidate.id for candidate in candidates if candidate.must_compact and candidate.compact_slots is None]
    add(
        "mandatory compact fit",
        not impossible_must,
        "all mandatory compact candidates fit primary payload"
        if not impossible_must
        else f"too wide: {', '.join(impossible_must)}",
    )

    bad_memmem = [
        candidate.id
        for candidate in candidates
        if not candidate.allow_memory_memory and count_kind(candidate.descriptor_fields, "EA") > 1
    ]
    add(
        "memory-memory restriction",
        not bad_memmem,
        "only candidates explicitly marked memory-memory-capable contain two EA operands"
        if not bad_memmem
        else f"undeclared mem-mem candidates: {', '.join(bad_memmem[:12])}",
    )

    compact_possible = sum(1 for candidate in candidates if candidate.compact_slots is not None)
    checks.append(
        {
            "name": "allocation scope",
            "status": "info",
            "detail": (
                f"{len(candidates)} candidates allocated together; "
                f"{compact_possible} have one-word field layouts."
            ),
        }
    )
    return checks


def count_kind(fields: tuple[Field, ...], kind: str) -> int:
    return sum(1 for field in fields if field.kind == kind)


def has_alignment_failure(checks: list[dict[str, Any]]) -> bool:
    return any(item["status"] == "fail" for item in checks)
