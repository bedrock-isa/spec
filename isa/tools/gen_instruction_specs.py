#!/usr/bin/env python3
"""Generate per-instruction semantic and encoding reference documentation."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any
import argparse
import json
import sys

import yaml

sys.dont_write_bytecode = True

from gen_instruction_tables import (
    allocation_sort_key,
    default_words,
    encoding_line,
    encoding_text,
    entry_lengths,
    field_layout_text,
    operand_types_text,
    syntax_text,
    set_active_spec as set_instruction_table_spec,
)
from isa_spec import load_and_validate, print_result
from spec_model.encoding import fflag_meanings as spec_fflag_meanings, fflag_names as spec_fflag_names


FAMILY_SECTIONS = ("compact_primary", "integer", "system", "fpu")
ENTRY_METADATA = {"description", "notes", "category", "registers"}
FRONT_MATTER_KEYS = (
    "compact_forms",
    "extended_forms",
    "operands",
    "size",
    "D_size",
    "A_size",
    "source_size",
    "destination_size",
    "flags",
    "fp_flags",
    "effects",
    "effect",
    "performs",
    "computes",
    "result",
    "reads",
    "writes",
    "updates",
    "returns",
    "traps",
    "privilege",
)
ACTIVE_SPEC: dict[str, Any] | None = None


def set_active_spec(spec: dict[str, Any]) -> None:
    global ACTIVE_SPEC
    ACTIVE_SPEC = spec
    set_instruction_table_spec(spec)


def active_spec() -> dict[str, Any]:
    if ACTIVE_SPEC is None:
        raise RuntimeError("active ISA spec is not set")
    return ACTIVE_SPEC


def md(text: Any) -> str:
    return str(text).replace("|", "\\|").replace("\n", " ")


def markdown_value(key: str, value: Any) -> str:
    if key == "fp_flags":
        return fp_flags_markdown(value)
    return str(value)


def fp_flags_markdown(value: Any) -> str:
    if isinstance(value, dict):
        if "description" in value:
            return str(value["description"])
        if "update" in value:
            return "update: " + fflags_list_text(value["update"])
        if "update_when_required" in value:
            return "update when required: " + fflags_list_text(value["update_when_required"])
        if value.get("unchanged") is True:
            return "FFLAGS unchanged"
    if isinstance(value, str) and value == "unchanged":
        return "FFLAGS unchanged"
    if isinstance(value, str) and value == "update_FFLAGS":
        return "update: " + fflags_list_text(spec_fflag_names(active_spec()))
    if isinstance(value, str) and value == "update_when_conversion_or_compare_requires":
        return "update when required: " + fflags_list_text(spec_fflag_names(active_spec()))
    return str(value)


def fflags_list_text(flags: Any) -> str:
    if isinstance(flags, dict):
        names = list(flags)
    elif isinstance(flags, str):
        names = [flags]
    else:
        names = [str(flag) for flag in flags]
    meanings = spec_fflag_meanings(active_spec())
    return ", ".join(f"FFLAGS.{name} ({meanings.get(name, name)})" for name in names)


def anchor(text: str) -> str:
    return "".join(ch.lower() if ch.isalnum() else "-" for ch in text).strip("-")


def load_allocation(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as fp:
        return json.load(fp)


def allocation_items(plan: dict[str, Any]) -> list[dict[str, Any]]:
    solver = plan.get("solver", plan)
    items: list[dict[str, Any]] = []
    items.extend(item for item in solver.get("primary_allocations", []) if item.get("kind") == "compact")
    items.extend(solver.get("primary_alias_allocations", []))
    items.extend(solver.get("extended_allocations", []))
    items.extend(solver.get("extended_alias_allocations", []))
    return sorted((dict(item) for item in items), key=allocation_sort_key)


def mnemonic_list(entry_key: str, entry: dict[str, Any]) -> list[str]:
    if isinstance(entry.get("mnemonics"), list):
        return [str(name) for name in entry["mnemonics"]]
    return [str(entry_key)]


def resolve_mnemonic_specific_values(entry: dict[str, Any], mnemonic: str) -> dict[str, Any]:
    resolved = deepcopy(entry)
    for key in ("operands", "flags", "fp_flags", "effects", "effect", "result", "privilege"):
        value = resolved.get(key)
        if isinstance(value, dict) and mnemonic in value:
            resolved[key] = value[mnemonic]
    for key, value in list(resolved.items()):
        if not key.endswith("_by_mnemonic"):
            continue
        resolved.pop(key, None)
        base_key = key[: -len("_by_mnemonic")]
        if isinstance(value, dict) and mnemonic in value:
            resolved[base_key] = value[mnemonic]
    return resolved


def semantic_records(spec: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    instructions = spec.get("instructions") or {}
    families = instructions.get("families") or {}
    by_mnemonic: dict[str, list[dict[str, Any]]] = {}
    for family_name, family in families.items():
        if not isinstance(family, dict):
            continue
        category = str(family.get("category", ""))
        for section_name in FAMILY_SECTIONS:
            section = family.get(section_name)
            if not isinstance(section, dict):
                continue
            raw_entries = section.get("entries") if isinstance(section.get("entries"), dict) else section
            if not isinstance(raw_entries, dict):
                continue
            for entry_key, raw_entry in raw_entries.items():
                if entry_key in ENTRY_METADATA or not isinstance(raw_entry, dict):
                    continue
                for mnemonic in mnemonic_list(str(entry_key), raw_entry):
                    entry = resolve_mnemonic_specific_values(raw_entry, mnemonic)
                    entry.pop("mnemonics", None)
                    by_mnemonic.setdefault(mnemonic, []).append(
                        {
                            "family": str(family_name),
                            "category": category,
                            "section": section_name,
                            "group": str(entry_key),
                            "spec": entry,
                        }
                    )
    return by_mnemonic


def operation_records(spec: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    instructions = spec.get("instructions") or {}
    operation_semantics = instructions.get("operation_semantics") or {}
    by_mnemonic: dict[str, list[dict[str, Any]]] = {}

    def add_record(mnemonic: str, group_name: str, raw: dict[str, Any]) -> None:
        record = deepcopy(raw)
        record.pop("members", None)
        resolved: dict[str, Any] = {}
        for key, value in list(record.items()):
            if not key.endswith("_by_mnemonic"):
                continue
            record.pop(key, None)
            base_key = key[: -len("_by_mnemonic")]
            if isinstance(value, dict) and mnemonic in value:
                resolved[base_key] = value[mnemonic]
        record.update(resolved)
        by_mnemonic.setdefault(mnemonic, []).append({"group": group_name, "spec": record})

    for group_name, raw_group in (operation_semantics.get("groups") or {}).items():
        if not isinstance(raw_group, dict):
            continue
        for mnemonic in raw_group.get("members", []) or []:
            add_record(str(mnemonic), str(group_name), raw_group)

    for mnemonic, raw_entry in (operation_semantics.get("instructions") or {}).items():
        if isinstance(raw_entry, dict):
            by_mnemonic.setdefault(str(mnemonic), []).append({"group": "instruction_override", "spec": deepcopy(raw_entry)})
    return by_mnemonic


def aliases_by_mnemonic(spec: dict[str, Any], items: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    out: dict[str, list[dict[str, Any]]] = {}
    instructions = spec.get("instructions") or {}
    for alias in instructions.get("canonical_aliases", []) or []:
        if not isinstance(alias, dict):
            continue
        alias_name = str(alias.get("alias", ""))
        target = str(alias.get("target", ""))
        condition = str(alias.get("condition", ""))
        row = {
            "kind": "canonical_alias",
            "alias": alias_name,
            "target": target,
            "condition": condition,
            "canonical_disassembly": alias.get("canonical_disassembly", ""),
        }
        out.setdefault(alias_name, []).append(row)
        if target:
            out.setdefault(target, []).append(row)
    for item in items:
        if "alias_of" not in item:
            continue
        mnemonic = str(item.get("mnemonic", ""))
        out.setdefault(mnemonic, []).append(
            {
                "kind": "allocated_alias",
                "alias": mnemonic,
                "target": item.get("alias_of", ""),
                "condition": item.get("alias_condition", ""),
                "canonical_disassembly": "",
            }
        )
    return out


def render_alias_table(aliases: list[dict[str, Any]]) -> list[str]:
    if not aliases:
        return []
    rows = [
        "| Kind | Alias | Target | Condition | Canonical Disassembly |",
        "| --- | --- | --- | --- | --- |",
    ]
    seen: set[tuple[str, str, str, str, str]] = set()
    for alias in aliases:
        key = (
            str(alias.get("kind", "")),
            str(alias.get("alias", "")),
            str(alias.get("target", "")),
            str(alias.get("condition", "")),
            str(alias.get("canonical_disassembly", "")),
        )
        if key in seen:
            continue
        seen.add(key)
        rows.append(
            f"| `{md(alias.get('kind', ''))}` | `{md(alias.get('alias', ''))}` | "
            f"`{md(alias.get('target', ''))}` | `{md(alias.get('condition', ''))}` | "
            f"`{md(alias.get('canonical_disassembly', ''))}` |"
        )
    return rows


def compact_yaml(value: Any) -> str:
    return yaml.safe_dump(value, sort_keys=False, allow_unicode=False).strip()


def semantic_summary(record: dict[str, Any]) -> str:
    spec = record["spec"]
    lines = [
        f"- Family: `{record['family']}`",
        f"- Category: `{record['category'] or '-'}`",
        f"- Catalog section: `{record['section']}`",
        f"- Source group: `{record['group']}`",
    ]
    for key in FRONT_MATTER_KEYS:
        if key not in spec:
            continue
        value = spec[key]
        if isinstance(value, (dict, list)):
            if key == "fp_flags":
                lines.append(f"- {key}: `{markdown_value(key, value)}`")
            else:
                lines.append(f"- {key}:")
                dumped = compact_yaml(value)
                lines.extend(f"  {line}" for line in dumped.splitlines())
        else:
            lines.append(f"- {key}: `{markdown_value(key, value)}`")
    return "\n".join(lines)


def remaining_semantics(record: dict[str, Any]) -> dict[str, Any]:
    spec = deepcopy(record["spec"])
    for key in FRONT_MATTER_KEYS:
        spec.pop(key, None)
    spec.pop("semantic_family", None)
    spec.pop("semantic_category", None)
    return spec


def render_operation_records(records: list[dict[str, Any]]) -> list[str]:
    if not records:
        return ["Operation detail: not specified."]
    lines = ["Operation detail:"]
    for index, record in enumerate(records, 1):
        if len(records) > 1:
            lines.append(f"Entry {index}:")
        lines.append(f"- Operation group: `{record['group']}`")
        for key, value in record["spec"].items():
            if isinstance(value, (dict, list)):
                if key == "fp_flags":
                    lines.append(f"- {key}: `{markdown_value(key, value)}`")
                else:
                    lines.append(f"- {key}:")
                    dumped = compact_yaml(value)
                    lines.extend(f"  {line}" for line in dumped.splitlines())
            else:
                lines.append(f"- {key}: `{markdown_value(key, value)}`")
        lines.append("")
    return lines


def render_form_table(items: list[dict[str, Any]], lengths: dict[tuple[str, str], tuple[int, int]]) -> list[str]:
    if not items:
        return ["No allocated forms."]
    lines = [
        "| Form | Encoding | Syntax | Words | Operands | Fields | Notes |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for item in items:
        min_words, max_words, note = default_words(item, lengths)
        lines.append(
            f"| `{md(item['id'])}` | `{md(encoding_text(item))}` | `{md(syntax_text(item))}` | "
            f"{min_words}..{max_words} | {md(operand_types_text(item))} | `{md(field_layout_text(item))}` | {md(note)} |"
        )
    return lines


def render_encoding_lines(items: list[dict[str, Any]]) -> list[str]:
    if not items:
        return []
    lines = ["", "Encoding patterns:"]
    previous_space = ""
    for item in items:
        space = "primary" if item.get("kind") in {"compact", "compact_alias"} else str(item.get("extension_root", "extended"))
        if previous_space and space != previous_space:
            lines.append("")
        previous_space = space
        lines.append(encoding_line(item))
    return lines


def render_instruction(
    mnemonic: str,
    records: list[dict[str, Any]],
    operations: list[dict[str, Any]],
    items: list[dict[str, Any]],
    aliases: list[dict[str, Any]],
    lengths: dict[tuple[str, str], tuple[int, int]],
) -> str:
    lines = [f"## {mnemonic}", ""]
    if aliases:
        lines.append("Aliases:")
        lines.extend(render_alias_table(aliases))
        lines.append("")
    lines.extend(render_operation_records(operations))
    if records:
        lines.append("Semantic spec:")
        for index, record in enumerate(records, 1):
            if len(records) > 1:
                lines.append(f"Entry {index}:")
            lines.append(semantic_summary(record))
            remaining = remaining_semantics(record)
            if remaining:
                lines.append("")
                lines.append("Additional catalog data:")
                lines.append("```yaml")
                lines.append(compact_yaml(remaining))
                lines.append("```")
            lines.append("")
    else:
        lines.append("Semantic spec: not found in `instructions.yaml`.")
        lines.append("")
    lines.append("Allocated forms:")
    lines.extend(render_form_table(items, lengths))
    lines.extend(render_encoding_lines(items))
    lines.append("")
    return "\n".join(lines)


def render(plan: dict[str, Any], spec: dict[str, Any], lengths: dict[tuple[str, str], tuple[int, int]]) -> str:
    set_active_spec(spec)
    items = allocation_items(plan)
    items_by_mnemonic: dict[str, list[dict[str, Any]]] = {}
    for item in items:
        items_by_mnemonic.setdefault(str(item.get("mnemonic", item.get("id", ""))), []).append(item)
    records = semantic_records(spec)
    operations = operation_records(spec)
    aliases = aliases_by_mnemonic(spec, items)
    mnemonics = sorted(set(records) | set(operations) | set(items_by_mnemonic) | set(aliases))
    operation_coverage = len([mnemonic for mnemonic in mnemonics if operations.get(mnemonic)])

    lines = [
        "# Generated Instruction Specifications",
        "",
        "Generated from `isa/spec/instructions.yaml` and `build/generated/allocation_plan.json`. Do not edit by hand.",
        "",
        f"- Instruction mnemonics: {len(mnemonics)}",
        f"- Allocated forms: {len(items)}",
        f"- Operation detail coverage: {operation_coverage}/{len(mnemonics)}",
        f"- Solver status: `{plan.get('solver', {}).get('status', 'unknown')}`",
        "",
        "## Index",
        "",
    ]
    for mnemonic in mnemonics:
        form_count = len(items_by_mnemonic.get(mnemonic, []))
        family_names = sorted({record["family"] for record in records.get(mnemonic, [])})
        family_text = ", ".join(family_names) if family_names else "-"
        lines.append(f"- [{mnemonic}](#{anchor(mnemonic)}) — {form_count} form(s), {family_text}")
    lines.append("")
    for mnemonic in mnemonics:
        lines.append(
            render_instruction(
                mnemonic,
                records.get(mnemonic, []),
                operations.get(mnemonic, []),
                items_by_mnemonic.get(mnemonic, []),
                aliases.get(mnemonic, []),
                lengths,
            )
        )
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("spec_dir", nargs="?", default="isa/spec")
    parser.add_argument("--allocation", default="build/generated/allocation_plan.json")
    parser.add_argument("-o", "--output", default="build/generated/instruction_specs.md")
    args = parser.parse_args(argv)

    spec, result, entries = load_and_validate(args.spec_dir)
    print_result(result)
    if not result.ok:
        return 1

    plan = load_allocation(Path(args.allocation))
    text = render(plan, spec, entry_lengths(entries))
    if args.output == "-":
        sys.stdout.write(text)
    else:
        path = Path(args.output)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
