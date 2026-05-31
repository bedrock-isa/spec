#!/usr/bin/env python3
"""Validate the declarative ISA specification before generation."""

from __future__ import annotations

import argparse
import sys

sys.dont_write_bytecode = True

from typing import Any

from isa_spec import instruction_catalog, load_and_validate, print_result, semantic_entry_mnemonics


IEEE754_FFLAGS = {
    "NV": "invalid operation",
    "DZ": "division by zero",
    "OF": "overflow",
    "UF": "underflow",
    "NX": "inexact",
}


def catalog_mnemonic_count(spec: dict[str, Any]) -> int:
    catalog = instruction_catalog(spec)
    sections = [
        catalog.get("compact_primary_instructions"),
        catalog.get("integer_instructions"),
        catalog.get("atomic_system_cache_instructions"),
        (catalog.get("fpu") or {}).get("instructions") if isinstance(catalog.get("fpu"), dict) else None,
    ]
    names: set[str] = set()
    for section in sections:
        if not isinstance(section, dict):
            continue
        for key, body in section.items():
            if isinstance(body, dict):
                names.update(semantic_entry_mnemonics(str(key), body))
    return len(names)


def collect_fflag_names(value: Any) -> set[str]:
    if isinstance(value, str):
        return set() if value == "unchanged" else {value}
    if isinstance(value, list):
        names: set[str] = set()
        for item in value:
            names.update(collect_fflag_names(item))
        return names
    if not isinstance(value, dict):
        return set()
    names: set[str] = set()
    for key in ("update", "update_when_required"):
        if key in value:
            names.update(collect_fflag_names(value[key]))
    return names


def iter_fp_flag_specs(value: Any) -> list[Any]:
    specs: list[Any] = []
    if isinstance(value, dict):
        for key, item in value.items():
            if key == "fp_flags":
                specs.append(item)
            elif key == "fp_flags_by_mnemonic" and isinstance(item, dict):
                specs.extend(item.values())
            else:
                specs.extend(iter_fp_flag_specs(item))
    elif isinstance(value, list):
        for item in value:
            specs.extend(iter_fp_flag_specs(item))
    return specs


def validate_ieee754_fflags(spec: dict[str, Any]) -> list[str]:
    issues: list[str] = []
    notation = (((spec.get("instructions") or {}).get("operation_semantics") or {}).get("notation") or {}).get("fflags")
    if notation != IEEE754_FFLAGS:
        issues.append("operation_semantics.notation.fflags must match IEEE 754 exception flags NV/DZ/OF/UF/NX")

    allowed = set(IEEE754_FFLAGS)
    for flag_spec in iter_fp_flag_specs(spec):
        names = collect_fflag_names(flag_spec)
        unknown = sorted(names - allowed)
        if unknown:
            issues.append(f"unknown FFLAGS names: {', '.join(unknown)}")
    return issues


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("spec_dir", nargs="?", default="isa/spec")
    parser.add_argument("-v", "--verbose", action="store_true", help="show accepted intentional overlaps")
    args = parser.parse_args(argv)

    spec, result, entries = load_and_validate(args.spec_dir)
    print_result(result, verbose=args.verbose)
    if not result.ok:
        return 1
    ieee754_issues = validate_ieee754_fflags(spec)
    if ieee754_issues:
        for issue in ieee754_issues:
            print(f"IEEE 754 FFLAGS validation error: {issue}")
        return 1
    pattern_count = sum(1 for e in entries if e.kind == "instruction")
    catalog_count = catalog_mnemonic_count(spec)
    print(f"validated {pattern_count} hand-authored instruction patterns; {catalog_count} catalog mnemonics")
    print("IEEE 754 FFLAGS: NV, DZ, OF, UF, NX")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
