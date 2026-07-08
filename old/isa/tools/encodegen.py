#!/usr/bin/env python3
"""Generate assembler/encoder metadata from the declarative ISA spec."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True

from isa_spec import entry_dict, instruction_catalog, json_dumps, load_and_validate, print_result


def default_allocation_path(spec_dir: str) -> Path:
    return Path(spec_dir).resolve().parents[1] / "build" / "generated" / "allocation_plan.json"


def load_allocated_entries(path: Path) -> list[dict[str, object]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8") as fp:
        plan = json.load(fp)
    solver = plan.get("solver", {})
    rows = []
    rows.extend(item for item in solver.get("primary_allocations", []) if item.get("kind") == "compact")
    rows.extend(solver.get("primary_alias_allocations", []))
    rows.extend(solver.get("extended_allocations", []))
    rows.extend(solver.get("extended_alias_allocations", []))
    return rows


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("spec_dir", nargs="?", default="isa/spec")
    parser.add_argument("-o", "--output", default="build/generated/encoder_table.json")
    parser.add_argument("--allocation", help="allocation_plan.json to include allocated encoder entries")
    args = parser.parse_args(argv)

    spec, result, entries = load_and_validate(args.spec_dir)
    print_result(result)
    if not result.ok:
        return 1

    payload = {
        "canonical_rules": spec["opcodes"].get("canonical_rules", []),
        "ea_catalog": spec.get("ea", {}),
        "semantic_catalog": spec.get("semantics", {}),
        "instruction_catalog": instruction_catalog(spec),
        "allocated_encoder_entries": load_allocated_entries(
            Path(args.allocation) if args.allocation else default_allocation_path(args.spec_dir)
        ),
        "encoder_entries": [
            entry_dict(entry)
            for entry in entries
            if entry.kind == "instruction" and not entry.source.get("reserved")
        ],
    }
    text = json_dumps(payload)
    if args.output == "-":
        sys.stdout.write(text)
    else:
        path = Path(args.output)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
