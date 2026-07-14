#!/usr/bin/env python3
"""Validate consistency between instruction definitions and allocation tables."""

from __future__ import annotations

import argparse
import re
from pathlib import Path
import sys
from typing import Any

try:
    import yaml
except ImportError as exc:  # pragma: no cover - environment error path
    raise SystemExit("PyYAML is required to validate ISA YAML files") from exc


DEF_ROOT = Path("isa/defs")
ALLOC_ROOT = Path("isa/alloc")
INSTRUCTION_FILENAME = "instruction.yaml"


def load_yaml(path: Path) -> Any:
    with path.open() as f:
        return yaml.safe_load(f)


def definition_payloads(root: Path) -> dict[str, dict[str, Any]]:
    manifest = load_yaml(root / "manifest.yaml")
    out: dict[str, dict[str, Any]] = {}
    for spec in manifest.get("instruction_sets", []):
        include = root / spec["include"]
        data = load_yaml(include)
        for item in data.get("include", []):
            path = include.parent / item / INSTRUCTION_FILENAME
            child = load_yaml(path)
            if isinstance(child, dict) and "mnemonic" in child:
                out[str(child["mnemonic"])] = child
    return out


def definition_mnemonics(root: Path) -> set[str]:
    return set(definition_payloads(root))


def allocation_mnemonic(text: str) -> str | None:
    if not text or text.startswith("reserved") or text.startswith("long/") or text.startswith("long encoding"):
        return None
    head = text.split(";", 1)[0].strip().split()[0]
    head = head.split("(", 1)[0]
    head = head.split("/", 1)[0]
    head = head.split(".", 1)[0]
    if not head or not re.match(r"^[A-Za-z][A-Za-z0-9]*$", head):
        return None
    return head


def allocation_mnemonics(root: Path) -> set[str]:
    out: set[str] = set()
    for path in sorted(root.glob("*.yaml")):
        data = load_yaml(path)
        for entry in data.get("entries") or []:
            mnemonic = allocation_mnemonic(str(entry.get("text", "")))
            if mnemonic:
                out.add(mnemonic)
    return out


def as_names(value: Any) -> set[str]:
    if value is None or value == "none":
        return set()
    if isinstance(value, list):
        return {str(item) for item in value}
    return {str(value)}


def contains_writable_ea(value: Any, written_names: set[str]) -> bool:
    if isinstance(value, dict):
        if value.get("type") == "EA" and str(value.get("name")) in written_names:
            return True
        return any(contains_writable_ea(item, written_names) for item in value.values())
    if isinstance(value, list):
        return any(contains_writable_ea(item, written_names) for item in value)
    return False


def instruction_has_writable_ea(data: dict[str, Any]) -> bool:
    behavior = data.get("behavior") or {}
    written_names = as_names(behavior.get("output")) | as_names(behavior.get("input_output"))
    forms = data.get("forms") or {}
    return bool(forms.get("dst_ea_set")) or contains_writable_ea(forms, written_names)


def allocation_form_operands(text: str) -> list[str]:
    parts = text.split(";", 1)[0].strip().split(maxsplit=1)
    if len(parts) < 2:
        return []
    return [operand.strip() for operand in parts[1].split(",")]


def destination_ea_field(entry: dict[str, Any], mnemonic: str) -> str | None:
    fields = entry.get("fields") or {}
    ea_fields = [
        name
        for name, spec in fields.items()
        if isinstance(spec, dict) and spec.get("kind") == "ea7"
    ]
    if not ea_fields:
        return None

    operands = allocation_form_operands(str(entry.get("text", "")))
    # XCHG writes both operands; all other current writable-EA forms write the
    # final explicit operand in allocation syntax.
    candidate_operands = operands if mnemonic == "XCHG" else operands[-1:]
    for operand in candidate_operands:
        if "<ea>" not in operand:
            continue
        marker = re.search(r"<ea>\(([A-Za-z])\)", operand)
        if marker:
            return marker.group(1)
        if len(ea_fields) == 1:
            return ea_fields[0]
    return None


def has_immediate_exclusion(entry: dict[str, Any], field: str) -> bool:
    return any(
        constraint.get("exclude") == "immediate"
        and (constraint.get("destination") or constraint.get("field") == field)
        for constraint in entry.get("constraints") or []
    )


def destination_ea_reclaim_status(
    defs_root: Path,
    alloc_root: Path,
) -> tuple[int, list[str]]:
    definitions = definition_payloads(defs_root)
    writable = {
        mnemonic
        for mnemonic, data in definitions.items()
        if instruction_has_writable_ea(data)
    }
    checked = 0
    missing: list[str] = []
    for path in sorted(alloc_root.glob("*.yaml")):
        data = load_yaml(path)
        for entry in data.get("entries") or []:
            mnemonic = allocation_mnemonic(str(entry.get("text", "")))
            if mnemonic not in writable:
                continue
            field = destination_ea_field(entry, mnemonic)
            if field is None:
                continue
            checked += 1
            if not has_immediate_exclusion(entry, field):
                missing.append(str(entry["id"]))
    return checked, missing


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--defs", type=Path, default=DEF_ROOT)
    parser.add_argument("--alloc", type=Path, default=ALLOC_ROOT)
    args = parser.parse_args()

    defs = definition_mnemonics(args.defs)
    alloc = allocation_mnemonics(args.alloc)

    missing_defs = sorted(alloc - defs)
    unallocated_defs = sorted(defs - alloc)

    print("ISA definition/allocation join")
    print(f"  definition mnemonics: {len(defs)}")
    print(f"  allocated mnemonics:  {len(alloc)}")
    print(f"  allocated without definition: {len(missing_defs)}")
    if missing_defs:
        print("    " + " ".join(missing_defs))
    print(f"  definitions without allocation: {len(unallocated_defs)}")
    if unallocated_defs:
        print("    " + " ".join(unallocated_defs[:80]))
        if len(unallocated_defs) > 80:
            print(f"    ... {len(unallocated_defs) - 80} more")

    checked_destinations, missing_destination_reclaims = destination_ea_reclaim_status(
        args.defs,
        args.alloc,
    )
    print(f"  writable EA allocation forms: {checked_destinations}")
    print(f"  writable EA forms without immediate reclaim: {len(missing_destination_reclaims)}")
    if missing_destination_reclaims:
        print("    " + " ".join(missing_destination_reclaims))

    # Missing definitions and writable EA forms that still claim immediate
    # destinations are hard errors. Definitions without allocation are expected
    # while optional extensions and extralong candidates are still being placed.
    return 1 if missing_defs or missing_destination_reclaims else 0


if __name__ == "__main__":
    raise SystemExit(main())
