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


def load_yaml(path: Path) -> Any:
    with path.open() as f:
        return yaml.safe_load(f)


def definition_mnemonics(root: Path) -> set[str]:
    manifest = load_yaml(root / "manifest.yaml")
    out: set[str] = set()
    for spec in manifest.get("instruction_sets", []):
        include = root / spec["include"]
        data = load_yaml(include)
        for item in data.get("include", []):
            path = include.parent / item
            child = load_yaml(path)
            if isinstance(child, dict) and "mnemonic" in child:
                out.add(str(child["mnemonic"]))
    return out


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

    # Missing definitions are hard errors; definitions without allocation are
    # expected while optional extensions and extralong candidates are still being
    # placed.
    return 1 if missing_defs else 0


if __name__ == "__main__":
    raise SystemExit(main())
