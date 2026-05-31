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
    common = spec["semantics"].get("common_fields", {})
    add(
        "D register range",
        common.get("dreg") == "D0-D7" and int(registers.get("D", {}).get("count", 0)) == 8,
        f"common dreg={common.get('dreg')}, register count={registers.get('D', {}).get('count')}",
    )
    add(
        "A register range",
        common.get("areg") == "A0-A7" and int(registers.get("A", {}).get("count", 0)) == 8,
        f"common areg={common.get('areg')}, register count={registers.get('A', {}).get('count')}",
    )

    rep = {item.get("name"): item for item in spec["prefixes"].get("prefixes", []) or []}.get("REPcc", {})
    rep_syntax = rep.get("syntax", {}) if isinstance(rep, dict) else {}
    rep_condition = rep.get("condition", {}) if isinstance(rep, dict) else {}
    rep_operand = rep.get("operand", {}) if isinstance(rep, dict) else {}
    add(
        "REPcc counter and condition range",
        rep_operand.get("range") == "D0-D7"
        and rep_operand.get("field") == "d"
        and rep_condition.get("field") == "c"
        and rep_condition.get("full_set") is True
        and rep.get("pattern") == "1ccc cddd"
        and (rep_syntax.get("aliases") or {}).get("REP") == "REPT",
        (
            f"REPcc pattern={rep.get('pattern')}, condition={rep_condition.get('field')}, "
            f"range={rep_operand.get('range')}, alias REP={(rep_syntax.get('aliases') or {}).get('REP')}"
        ),
    )

    prefix_by_name = {item.get("name"): item for item in spec["prefixes"].get("prefixes", []) or []}
    repg = prefix_by_name.get("REPG", {})
    repg_syntax = repg.get("syntax", {}) if isinstance(repg, dict) else {}
    repg_operand = repg.get("operand", {}) if isinstance(repg, dict) else {}
    repg_alignment = repg.get("alignment", {}) if isinstance(repg, dict) else {}
    repg_scope = repg.get("encoding_scope", {}) if isinstance(repg, dict) else {}
    endg = prefix_by_name.get("ENDG", {})
    add(
        "REPG/ENDG group prefix",
        repg.get("pattern") == "0110 0ddd"
        and repg_operand.get("range") == "D0-D7"
        and repg_operand.get("field") == "d"
        and bool(repg_syntax.get("block"))
        and repg_syntax.get("terminator_prefix") == "ENDG"
        and int(repg_alignment.get("grouping_window_bytes", 0) or 0) == 64
        and repg_scope.get("group_termination") == "ENDG_prefix"
        and isinstance(endg, dict)
        and int(endg.get("value", -1) or -1) == 0x68
        and endg.get("group") == "repeat_boundary",
        (
            f"REPG pattern={repg.get('pattern')}, terminator={repg_syntax.get('terminator_prefix')}, "
            f"range={repg_operand.get('range')}, window={repg_alignment.get('grouping_window_bytes')}, "
            f"ENDG={endg.get('value') if isinstance(endg, dict) else None}"
        ),
    )

    raw_ea_forms = spec["ea"].get("ea_forms", []) or []
    compact_ea_forms = raw_ea_forms.get("compact", []) if isinstance(raw_ea_forms, dict) else raw_ea_forms
    raw_extended_ea_forms = spec["ea"].get("extended_ea_forms")
    if raw_extended_ea_forms is None:
        raw_extended_ea_forms = spec["ea"].get("extended_ea_word", {}).get("modes", []) or []
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
    add(
        "address-update prefix legality",
        ea_forms == {"INDIRECT"} and ext_modes == {"SEG_A"},
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
    constraints = spec["ea"].get("instruction_ea_constraints", {}) or {}
    unknown_sets = []
    for name, body in constraints.items():
        if not isinstance(body, dict):
            continue
        for key, value in body.items():
            if key.endswith("_ea_set") and str(value) not in ea_sets:
                unknown_sets.append(f"{name}.{key}={value}")
    add(
        "EA operand policy",
        bool(ea_sets) and not unknown_sets,
        f"{len(ea_sets)} EA sets, {len(constraints)} instruction constraints"
        if ea_sets and not unknown_sets
        else f"unknown EA set references={unknown_sets}",
    )

    canonical_rules = spec["opcodes"].get("canonical_rules", []) or []
    mov_rule_ok = any(
        rule.get("canonical") == "MOV_EA_TO_D"
        and rule.get("noncanonical") == "MOV_D_TO_EA"
        and rule.get("when", {}).get("source") == "DREG"
        and rule.get("when", {}).get("destination") == "DREG"
        for rule in canonical_rules
    )
    add("MOV D-to-D canonical rule", mov_rule_ok, "MOV_D_TO_D maps to MOV_EA_TO_D")

    fixed = {candidate.id: candidate.fixed_payload for candidate in candidates if candidate.fixed_payload is not None}
    add(
        "sentinel fixed payloads",
        fixed.get("HALT") == 0x000 and fixed.get("ILLEGAL") == 0xFFF,
        f"HALT={fixed.get('HALT')}, ILLEGAL={fixed.get('ILLEGAL')}",
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
