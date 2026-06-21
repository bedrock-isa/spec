#!/usr/bin/env python3
"""Generate Markdown opcode tables from the declarative ISA spec."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any

sys.dont_write_bytecode = True

from isa_spec import PatternEntry, load_and_validate, print_result


def operand_text(entry: PatternEntry) -> str:
    parts: list[str] = []
    for operand in entry.source.get("operands", []) or []:
        if not isinstance(operand, dict):
            continue
        name = operand.get("name")
        typ = operand.get("type", "?")
        field = operand.get("field")
        text = str(typ)
        if field:
            text += f"({field})"
        if name:
            text = f"{name}:{text}"
        parts.append(text)
    return ", ".join(parts)


def length_text(entry: PatternEntry) -> str:
    length = entry.source.get("length") or {}
    if isinstance(length, int):
        return str(length)
    if isinstance(length, dict):
        return f"{length.get('min_words', '?')}..{length.get('max_words', '?')}"
    return "?"


def primary_sort_key(entry: PatternEntry) -> tuple[int, int, int, int, str]:
    shift = max(0, entry.pattern.width - 16)
    primary_value = entry.pattern.value >> shift
    return (primary_value, entry.pattern.word_count, entry.pattern.value, -entry.pattern.fixed_bits, entry.id)


def allocation_sort_key(item: dict[str, Any]) -> tuple[int, int, str]:
    if item.get("kind") in {"compact", "compact_alias"}:
        return (int(str(item["start_payload"]), 16), -1, str(item["id"]))
    root = str(item.get("extension_root_payload", "0x000")).split("..", 1)[0]
    opcode = str(item.get("extended_opcode_start", item.get("extended_opcode", "0x0000"))).split("..", 1)[0]
    return (int(root, 16), int(opcode, 16), str(item["id"]))


def hex_digits(value: Any, width: int) -> str:
    if isinstance(value, int):
        return f"{value:0{width}x}"
    return f"{int(str(value), 16):0{width}x}"


def short_payload(value: Any) -> str:
    text = str(value)
    if ".." not in text:
        return hex_digits(text, 3)
    start, end = text.split("..", 1)
    return f"{hex_digits(start, 3)}-{hex_digits(end, 3)}"


def short_extended_opcode(item: dict[str, Any]) -> str:
    start = item.get("extended_opcode_start")
    end = item.get("extended_opcode_end")
    if start is not None and end is not None:
        left = hex_digits(start, 4)
        right = hex_digits(end, 4)
        return left if left == right else f"{left}-{right}"
    text = str(item.get("extended_opcode", "0x0000"))
    if ".." not in text:
        return hex_digits(text, 4)
    left, right = text.split("..", 1)
    return f"{hex_digits(left, 4)}-{hex_digits(right, 4)}"


def short_payload_range(start: Any, end: Any) -> str:
    left = hex_digits(start, 3)
    right = hex_digits(end, 3)
    return left if left == right else f"{left}-{right}"


def short_payload_list(values: list[Any]) -> str:
    return ",".join(short_payload(value) for value in values)


def allocation_encoding(item: dict[str, Any]) -> str:
    kind = item.get("kind")
    if kind == "compact":
        return f"P:{short_payload_range(item['start_payload'], item['end_payload'])}"
    if kind == "compact_alias":
        payloads = short_payload_list(item.get("alias_payloads", []))
        return f"A:{item['alias_of']}/{item.get('alias_condition', 'T')} P:{payloads}"
    if kind == "extended_alias":
        payloads = short_payload_list(item.get("alias_payloads", []))
        return f"A:{item['alias_of']}/{item.get('alias_condition', 'T')} E:{payloads}/{short_extended_opcode(item)}"
    return f"E:{short_payload(item['extension_root_payload'])}/{short_extended_opcode(item)}"


def allocation_words(item: dict[str, Any]) -> str:
    if item.get("kind") in {"compact", "compact_alias"}:
        if "min_words" in item and "max_words" in item:
            return f"{item['min_words']}..{item['max_words']}"
        return "1..8"
    words = 2 + int(item.get("operand_descriptor_words", 0))
    if "min_words" in item:
        words = max(words, int(item["min_words"]))
    return f"{words}..{item.get('max_words', 8)}"


SELECTOR_SOURCES = {"count", "bit_index", "offset", "width"}


def operand_kind_label(source: str, kind: str) -> str:
    if kind == "small_selector" and source.lower() in SELECTOR_SOURCES:
        return "Dreg|imm"
    if kind == "selector6" and source.lower() in SELECTOR_SOURCES:
        return "imm6"
    return kind


def allocation_operands(item: dict[str, Any]) -> str:
    operands = [str(operand) for operand in item.get("operands", [])]
    fields_by_source: dict[str, list[str]] = {}
    for field in item.get("fields", []) or []:
        source = str(field.get("source", ""))
        kind = str(field.get("kind", ""))
        if not source or source == "size":
            continue
        fields_by_source.setdefault(source, []).append(kind)
    parts = []
    for operand in operands:
        if ":" in operand:
            source, declared = operand.split(":", 1)
        else:
            source, declared = operand, ""
        kinds = fields_by_source.get(source, [])
        if kinds:
            labels = [operand_kind_label(source, kind) for kind in kinds]
            parts.append(f"{source}:{'/'.join(labels)}")
        elif declared:
            parts.append(f"{source}:{declared}")
        else:
            parts.append(source)
    return ", ".join(parts)


def allocation_fields(item: dict[str, Any]) -> str:
    if item.get("kind") in {"compact", "compact_alias"}:
        return str(item.get("field_layout", ""))
    return str(item.get("descriptor_layout", ""))


def allocation_rows(plan: dict[str, Any]) -> list[dict[str, Any]]:
    solver = plan.get("solver", {})
    rows = [
        item for item in solver.get("primary_allocations", []) if item.get("kind") == "compact"
    ]
    rows += list(solver.get("primary_alias_allocations", []))
    rows += list(solver.get("extended_allocations", []))
    rows += list(solver.get("extended_alias_allocations", []))
    return sorted(rows, key=allocation_sort_key)


def load_allocation(path: Path | None) -> dict[str, Any] | None:
    if path is None or not path.exists():
        return None
    with path.open("r", encoding="utf-8") as fp:
        return json.load(fp)


def default_allocation_path(spec_dir: str | Path) -> Path:
    return Path(spec_dir).resolve().parents[1] / "build" / "generated" / "allocation_plan.json"


def render(entries: list[PatternEntry], allocation: dict[str, Any] | None = None) -> str:
    extensions = [entry for entry in entries if entry.kind == "extension_space"]
    reserved = [entry for entry in entries if entry.kind == "reserved"]

    lines = [
        "# Generated Opcode Table",
        "",
        "Generated from `isa/spec/*.yaml`. Do not edit by hand.",
        "",
    ]

    if allocation is not None:
        lines.extend(
            [
                "",
                "## Allocated Instruction Forms",
                "",
                "This table is generated from `build/generated/allocation_plan.json` and includes instruction-catalog forms allocated by the Z3 allocator.",
                "",
                "| Mnemonic | Form | Encoding | Words | Operands / Addressing Mode | Fields | Source |",
                "| --- | --- | --- | --- | --- | --- | --- |",
            ]
        )
        for item in allocation_rows(allocation):
            lines.append(
                f"| `{item['mnemonic']}` | `{item['id']}` | `{allocation_encoding(item)}` | "
                f"{allocation_words(item)} | {allocation_operands(item)} | "
                f"{allocation_fields(item)} | {item.get('origin', '')} |"
            )

    if extensions:
        lines.extend(
            [
                "",
                "## Extension Spaces",
                "",
                "| Mnemonic | ID | Pattern | Purpose |",
                "| --- | --- | --- | --- |",
            ]
        )
        for entry in extensions:
            lines.append(f"| `{entry.mnemonic}` | `{entry.id}` | `{entry.pattern.raw}` | {entry.source.get('purpose', '')} |")

    if reserved:
        lines.extend(
            [
                "",
                "## Reserved Primary Patterns",
                "",
                "| Mnemonic | ID | Pattern | Purpose |",
                "| --- | --- | --- | --- |",
            ]
        )
        for entry in reserved:
            lines.append(f"| `{entry.mnemonic}` | `{entry.id}` | `{entry.pattern.raw}` | {entry.source.get('purpose', '')} |")
    lines.append("")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("spec_dir", nargs="?", default="isa/spec")
    parser.add_argument("-o", "--output", help="write table to this file")
    parser.add_argument(
        "--allocation",
        help="allocation_plan.json to include generated instruction-catalog forms; defaults to build/generated/allocation_plan.json when present",
    )
    args = parser.parse_args(argv)

    _spec, result, entries = load_and_validate(args.spec_dir)
    print_result(result)
    if not result.ok:
        return 1

    allocation_path = Path(args.allocation) if args.allocation else default_allocation_path(args.spec_dir)
    text = render(entries, load_allocation(allocation_path))
    if args.output:
        path = Path(args.output)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    else:
        sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
