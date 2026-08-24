#!/usr/bin/env python3
"""Validate joins and generic safety rules in integrated ISA definitions."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

from defs_loader import (
    extension_cpuid_requirements, load_architectural_event_causes,
    load_architectural_event_ids, load_operation, load_cpuid_flags, load_extensions,
    load_flag_effect_definitions, load_instruction_sets, load_named_values,
    load_operand_types, load_semantic_conditions, load_size_definitions, load_yaml,
)
from encoding_store import EncodingStore, LocatedEncoding, load_encoding_store


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
DEF_ROOT = REPOSITORY_ROOT / "isa" / "instructions" / "definitions"


def definition_payloads(root: Path) -> dict[str, dict]:
    extensions = load_extensions(root)
    cpuid_flags = load_cpuid_flags(root)
    operand_types = load_operand_types(root, extensions)
    size_definitions = load_size_definitions(root, extensions)
    known_cpuid_flags, requirements_by_set = extension_cpuid_requirements(
        extensions, cpuid_flags
    )
    event_path = REPOSITORY_ROOT / "isa" / "conformance" / "architecture_tables.yaml"
    known_events = load_architectural_event_ids(event_path)
    known_causes = load_architectural_event_causes(event_path)
    known_conditions = frozenset(load_semantic_conditions(root))
    known_values = frozenset(load_named_values(root))
    flag_definitions = load_flag_effect_definitions(root)
    out: dict[str, dict] = {}
    for instruction_set in load_instruction_sets(root, extensions):
        index = load_yaml(instruction_set.include)
        for item in index.get("include", []):
            bundle = instruction_set.include.parent / item
            operation = load_operation(
                bundle, operand_types=operand_types, size_definitions=size_definitions,
                base_requirements=requirements_by_set[instruction_set.name],
                known_cpuid_flags=known_cpuid_flags, known_event_ids=known_events,
                known_event_causes=known_causes, known_condition_ids=known_conditions,
                known_named_value_ids=known_values,
                known_diagram_kinds=frozenset({"vector-example"}),
                known_flag_effect_definitions=flag_definitions,
            )
            mnemonic = operation.public_instruction.mnemonic
            if mnemonic in out:
                raise ValueError(f"{bundle}: duplicate mnemonic {mnemonic}")
            out[mnemonic] = {"operation": operation.id}
    return out


def definition_mnemonics(root: Path) -> set[str]:
    return set(definition_payloads(root))


def allocation_mnemonic(text: str) -> str | None:
    if not text:
        return None
    head = text.split(";", 1)[0].strip().split()[0]
    head = re.split(r"[./(]", head)[0]
    return head if re.fullmatch(r"[A-Za-z][A-Za-z0-9]*", head) else None


def encoding_mnemonics(store: EncodingStore) -> set[str]:
    return {located.mnemonic for located in store.encodings}


def has_immediate_exclusion(located: LocatedEncoding, field: str) -> bool:
    return any(
        constraint.field == field and constraint.exclude == "immediate"
        for constraint in located.form.constraints
    )


def writable_ea_reclaim_status(store: EncodingStore) -> tuple[int, list[str]]:
    checked = 0
    missing: list[str] = []
    for located in store.encodings:
        for operand in located.form.operands:
            if operand.type not in {"EA", "FEA", "VEA"} or operand.access not in {
                "write",
                "read_write",
            }:
                continue
            checked += 1
            if operand.field is None or not has_immediate_exclusion(located, operand.field):
                missing.append(located.form.id)
    return checked, missing


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--defs",
        type=Path,
        default=DEF_ROOT,
        help=(
            "ISA definition root "
            "(default: repository isa/instructions/definitions)"
        ),
    )
    args = parser.parse_args()

    definitions = definition_mnemonics(args.defs)
    store = load_encoding_store(args.defs)
    encoded = encoding_mnemonics(store)
    missing_defs = sorted(encoded - definitions)
    unallocated_defs = sorted(definitions - encoded)
    checked, missing_reclaims = writable_ea_reclaim_status(store)

    print("ISA definition/encoding join")
    print(f"  definition mnemonics: {len(definitions)}")
    print(f"  encoded mnemonics:    {len(encoded)}")
    print(f"  encoded without definition: {len(missing_defs)}")
    if missing_defs:
        print("    " + " ".join(missing_defs))
    print(f"  definitions without encoding: {len(unallocated_defs)}")
    if unallocated_defs:
        print("    " + " ".join(unallocated_defs))
    print(f"  writable EA operands: {checked}")
    print(f"  writable EA operands without immediate reclaim: {len(missing_reclaims)}")
    if missing_reclaims:
        print("    " + " ".join(missing_reclaims))
    return 1 if missing_defs or missing_reclaims else 0


if __name__ == "__main__":
    raise SystemExit(main())
