"""Markdown report rendering for opcode allocation plans."""

from __future__ import annotations

import re
from typing import Any


def compact_hex_ranges(values: list[Any]) -> str:
    ints = sorted({int(str(value), 16) for value in values})
    if not ints:
        return ""
    ranges: list[tuple[int, int]] = []
    start = previous = ints[0]
    for value in ints[1:]:
        if value == previous + 1:
            previous = value
            continue
        ranges.append((start, previous))
        start = previous = value
    ranges.append((start, previous))
    parts = []
    for start, end in ranges:
        if start == end:
            parts.append(f"`0x{start:03x}`")
        else:
            parts.append(f"`0x{start:03x}`..`0x{end:03x}`")
    return ", ".join(parts)


def primary_field_layout_table_text(layout: Any) -> str:
    text = str(layout or "").split(";", 1)[0].strip()
    if not text or text == "none":
        return "none"
    text = re.sub(r"(?:^|\s)op\[[^\]]+\]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text or "none"


def descriptor_layout_table_text(layout: Any) -> str:
    text = str(layout or "").strip()
    if not text or text == "none":
        return "none"
    return text


def compact_cost_table_text(allocation: dict[str, Any]) -> str:
    compact_cost = allocation["primary_slots_if_one_word"]
    if compact_cost is not None:
        return str(compact_cost)
    return str(allocation.get("eviction_reason", "extended-only"))


def render_markdown(plan: dict[str, Any]) -> str:
    solver = plan["solver"]
    lines = [
        "# Generated Opcode Allocation Plan",
        "",
        "Generated from `isa/spec/*.yaml`. Do not edit by hand.",
        "",
        f"- Solver status: `{solver['status']}`",
        f"- Primary target space: `{plan['target_space']['id']}`",
        f"- Extended target space: `{plan['extended_space']['id']}`",
        f"- Candidates allocated: {solver['candidate_count']}",
        f"- One-word compact encodings selected: {solver['compact_count']}",
        f"- Extended encodings selected: {solver['extended_count']}",
        f"- Primary slots used: {solver['primary_used_slot_count']} / {solver['slot_count']}",
        f"- Primary free slots: {solver['primary_free_slot_count']}",
        f"- Primary headroom target: {solver['primary_headroom_target']}",
        f"- Natural extension roots: {solver['extension_root_count']}",
        f"- Extension root primary slots: {solver['extension_root_slot_count']}",
        f"- Extended opcodes used: {solver['extended_used_opcode_count']} / {solver['extended_total_opcode_slot_count']}",
        f"- Allocator compact exclusions: {solver['compact_policy']['excluded_candidate_count']}",
        f"- Allocator compact-policy violations: {solver['compact_policy']['violation_count']}",
        "",
        "## Alignment Audit",
        "",
        "| Check | Status | Detail |",
        "| --- | --- | --- |",
    ]
    for check in plan["alignment_audit"]:
        lines.append(f"| {check['name']} | `{check['status']}` | {check['detail']} |")

    lines.extend(
        [
            "",
            "## Decode Cost Audit",
            "",
            "| Check | Status | Severity | Detail |",
            "| --- | --- | --- | --- |",
        ]
    )
    for item in solver.get("decode_cost_audit", []):
        lines.append(f"| {item['name']} | `{item['status']}` | {item['severity']} | {item['detail']} |")

    layout_model = solver.get("field_layout_model", {})
    if layout_model:
        score_model = layout_model.get("field_score_model", {})
        formula = str(score_model.get("formula", "candidate_weight_times_field_width"))
        default_multiplier = score_model.get("default_multiplier", 1)
        lines.extend(
            [
                "",
                "## Field Layout Model",
                "",
                f"- Field score formula: `{formula}`",
                f"- Default field score multiplier: `{default_multiplier}`",
                "",
                "| Rank | Signature | Width | Score |",
                "| --- | --- | --- | --- |",
            ]
        )
        for item in layout_model.get("signature_order", [])[:24]:
            lines.append(
                f"| {item['rank']} | `{item['signature']}` | {item['width']} | {item['score']} |"
            )
        subfield_affinities = layout_model.get("subfield_affinities", [])
        if subfield_affinities:
            lines.extend(
                [
                    "",
                    "| Container | Subfield | Offset | Score | Examples |",
                    "| --- | --- | --- | --- | --- |",
                ]
            )
            for item in subfield_affinities[:16]:
                examples = ", ".join(f"`{example}`" for example in item.get("examples", []))
                lines.append(
                    f"| `{item['container']}` | `{item['subfield']}` | {item['offset']} | "
                    f"{item['score']} | {examples} |"
                )
        lines.extend(
            [
                "",
                "| Operand Format | Count | Weight | Examples |",
                "| --- | --- | --- | --- |",
            ]
        )
        for item in layout_model.get("operand_format_groups", [])[:16]:
            examples = ", ".join(f"`{example}`" for example in item.get("examples", []))
            lines.append(
                f"| `{', '.join(item['format'])}` | {item['count']} | {item.get('weight', 0)} | {examples} |"
            )
        similarity = layout_model.get("operand_format_similarity", [])
        if similarity:
            lines.extend(
                [
                    "",
                    "| Similar Formats | Similarity | Shared Placement Pressure | Examples |",
                    "| --- | --- | --- | --- |",
                ]
            )
            for item in similarity[:16]:
                left = ", ".join(item.get("left", []))
                right = ", ".join(item.get("right", []))
                examples = ", ".join(
                    f"`{example}`"
                    for example in (list(item.get("left_examples", []))[:2] + list(item.get("right_examples", []))[:2])
                )
                lines.append(
                    f"| `{left}` / `{right}` | {item.get('similarity', 0)} | "
                    f"{item.get('combined_weight', 0)} | {examples} |"
                )

    family_symmetry = solver.get("compact_family_symmetry_audit", [])
    if family_symmetry:
        lines.extend(
            [
                "",
                "## Compact Family Symmetry Audit",
                "",
                "| Family | Status | Rule | Preference | Compact | Total | Detail |",
                "| --- | --- | --- | --- | --- | --- | --- |",
            ]
        )
        for item in family_symmetry:
            lines.append(
                f"| {item['family']} | `{item['status']}` | {item['rule']} | {item.get('preference', 'normal')} | "
                f"{item['compact']} | {item['total']} | {item['detail']} |"
            )

    lines.extend(
        [
            "",
            "## Primary Payload Allocations",
            "",
            "| Payload Range | Slots | Candidate | Bits | Field Layout | Operands |",
            "| --- | --- | --- | --- | --- | --- |",
        ]
    )
    for allocation in solver["primary_allocations"]:
        if allocation.get("primary_payloads"):
            payload = compact_hex_ranges(allocation.get("primary_payloads", []))
        elif allocation["start_payload"] == allocation["end_payload"]:
            payload = f"`{allocation['start_payload']}`"
        else:
            payload = f"`{allocation['start_payload']}`..`{allocation['end_payload']}`"
        operands = ", ".join(allocation["operands"])
        lines.append(
            f"| {payload} | {allocation['slots']} | `{allocation['id']}` | "
            f"{allocation['primary_bits']} | {primary_field_layout_table_text(allocation['field_layout'])} | {operands} |"
        )

    lines.extend(
        [
            "",
            "## Extension Roots",
            "",
            "| Payload Range | Root | Family | Profile | Primary Slots | Forms | Ext Slots Used | Ext Slots Free |",
            "| --- | --- | --- | --- | --- | --- | --- | --- |",
        ]
    )
    root_by_id = {root["id"]: root for root in solver["extension_roots"]}
    for item in solver["extension_root_usage"]:
        root = root_by_id[item["root"]]
        lines.append(
            f"| `{item['payload']}` | `{item['root']}` | {item['family']} | "
            f"{item['profile']} | {root['slots']} | {item['members']} | {item['used']} | {item['free']} |"
        )

    lines.extend(
        [
            "",
            "## Symmetry Audit",
            "",
            "| Check | Status | Severity | Detail |",
            "| --- | --- | --- | --- |",
        ]
    )
    for item in solver.get("symmetry_audit", []):
        lines.append(f"| {item['name']} | `{item['status']}` | {item['severity']} | {item['detail']} |")

    lines.extend(
        [
            "",
            "## Conditional Alias Audit",
            "",
            "| Check | Status | Detail |",
            "| --- | --- | --- |",
        ]
    )
    for item in solver.get("conditional_alias_audit", []):
        lines.append(f"| {item['name']} | `{item['status']}` | {item['detail']} |")

    lines.extend(
        [
            "",
            "## Canonical Alias Allocations",
            "",
            "| Alias | Alias Of | Condition | Encoding | Notes |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    for allocation in solver.get("primary_alias_allocations", []):
        payloads = ", ".join(f"`{payload}`" for payload in allocation.get("alias_payloads", []))
        lines.append(
            f"| `{allocation['id']}` | `{allocation['alias_of']}` | `{allocation['alias_condition']}` | "
            f"primary {payloads} | canonical disassembly `{allocation['canonical_disassembly']}` |"
        )
    for allocation in solver.get("extended_alias_allocations", []):
        payloads = ", ".join(f"`{payload}`" for payload in allocation.get("alias_payloads", []))
        lines.append(
            f"| `{allocation['id']}` | `{allocation['alias_of']}` | `{allocation['alias_condition']}` | "
            f"{allocation['extension_root']} @ {payloads}; ext `{allocation['extended_opcode']}` | "
            f"canonical disassembly `{allocation['canonical_disassembly']}` |"
        )

    lines.extend(
        [
            "",
            "## Extended Opcode Allocations",
            "",
            "| Root | Ext Opcode Range | Ext Slots | Candidate | Ext Field Bits | Payload Bits | Payload Words | Field Layout | Compact Cost If One-Word |",
            "| --- | --- | --- | --- | --- | --- | --- | --- | --- |",
        ]
    )
    for allocation in solver["extended_allocations"]:
        compact_cost_text = compact_cost_table_text(allocation)
        payload_bits = str(allocation["operand_payload_bits"])
        if allocation.get("operand_descriptor_spilled"):
            payload_bits += "+spill"
        lines.append(
            f"| `{allocation['extension_root']}` | "
            f"`{allocation['extended_opcode']}` | {allocation['extended_opcode_slots']} | `{allocation['id']}` | "
            f"{allocation['extended_opcode_bits']} | {payload_bits} | "
            f"{allocation['operand_descriptor_words']} | {descriptor_layout_table_text(allocation['descriptor_layout'])} | "
            f"{compact_cost_text} |"
        )

    lines.extend(
        [
            "",
            "## Compact Eviction Report",
            "",
            "| Evicted Candidate | Reason |",
            "| --- | --- |",
        ]
    )
    for item in solver["compact_evictions"]:
        lines.append(f"| `{item['evicted_instruction']}` | {item['estimated_code_size_delta']} |")

    lines.extend(
        [
            "",
            "## Primary Free Ranges",
            "",
            "| Payload Range | Count |",
            "| --- | --- |",
        ]
    )
    for item in solver["free_ranges"]:
        lines.append(f"| `{item['start_payload']}`..`{item['end_payload']}` | {item['count']} |")
    lines.append("")
    return "\n".join(lines)
