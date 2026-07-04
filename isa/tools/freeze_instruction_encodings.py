#!/usr/bin/env python3
"""Update per-instruction frozen encoding entries from an allocation plan."""

from __future__ import annotations

from collections import defaultdict
from pathlib import Path
from typing import Any
import argparse
import json
import re
import sys

sys.dont_write_bytecode = True

try:
    import yaml
except ImportError as exc:  # pragma: no cover - exercised only on incomplete hosts
    raise SystemExit("PyYAML is required: python3 -m pip install pyyaml") from exc

from allocation_lock import EXTENDED_KEYS, PRIMARY_KEYS, instruction_row_sort_key, locked_row


INSTRUCTION_GLOBS = (
    "base/instructions/*.yaml",
    "extensions/*/instructions/*.yaml",
)


def rows_by_mnemonic(plan: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    solver = plan.get("solver") if isinstance(plan.get("solver"), dict) else plan
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)

    def add(rows: list[Any], keys: tuple[str, ...], *, skip_extension_roots: bool = False) -> None:
        for row in rows:
            if not isinstance(row, dict):
                continue
            if skip_extension_roots and row.get("kind") == "extension_root":
                continue
            mnemonic = str(row.get("mnemonic") or "").strip()
            if not mnemonic:
                ident = str(row.get("id") or "")
                mnemonic = ident.split(".", 1)[0]
            if not mnemonic:
                continue
            grouped[mnemonic].append(locked_row(row, keys))

    add(solver.get("primary_allocations", []) or [], PRIMARY_KEYS, skip_extension_roots=True)
    add(solver.get("primary_alias_allocations", []) or [], PRIMARY_KEYS)
    add(solver.get("extended_allocations", []) or [], EXTENDED_KEYS)
    add(solver.get("extended_alias_allocations", []) or [], EXTENDED_KEYS)
    return {mnemonic: sorted(rows, key=instruction_row_sort_key) for mnemonic, rows in grouped.items()}


def mnemonic_files(spec_dir: Path) -> dict[str, Path]:
    out: dict[str, Path] = {}
    for pattern in INSTRUCTION_GLOBS:
        for path in sorted(spec_dir.glob(pattern)):
            if path.name == "_common.yaml":
                continue
            data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
            if not isinstance(data, dict):
                continue
            mnemonic = str(data.get("mnemonic") or "").strip()
            if mnemonic:
                out[mnemonic] = path
    return out


def encoding_block(rows: list[dict[str, Any]]) -> list[str]:
    text = yaml.safe_dump({"encoding": rows}, sort_keys=False, width=120)
    return [f"  {line}" if line.strip() else line for line in text.splitlines()]


def update_instruction_file(path: Path, rows: list[dict[str, Any]]) -> bool:
    original_lines = path.read_text(encoding="utf-8").splitlines()
    lines = list(original_lines)
    allocation_start = next((index for index, line in enumerate(lines) if line == "allocation:"), None)
    if allocation_start is None:
        raise ValueError(f"{path}: no allocation block")
    allocation_end = len(lines)
    for index in range(allocation_start + 1, len(lines)):
        if lines[index] and not lines[index].startswith(" "):
            allocation_end = index
            break

    lines = remove_existing_encoding(lines, allocation_start, allocation_end)
    allocation_end = len(lines)
    for index in range(allocation_start + 1, len(lines)):
        if lines[index] and not lines[index].startswith(" "):
            allocation_end = index
            break

    block = encoding_block(rows)
    updated = lines[:allocation_end] + block + lines[allocation_end:]
    if updated == original_lines:
        return False
    path.write_text("\n".join(updated) + "\n", encoding="utf-8")
    return True


def remove_existing_encoding(lines: list[str], allocation_start: int, allocation_end: int) -> list[str]:
    start = None
    for index in range(allocation_start + 1, allocation_end):
        if lines[index] == "  encoding:":
            start = index
            break
    if start is None:
        return lines
    end = allocation_end
    key_pattern = re.compile(r"^  [A-Za-z0-9_]+:")
    for index in range(start + 1, allocation_end):
        if key_pattern.match(lines[index]):
            end = index
            break
    return lines[:start] + lines[end:]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("allocation_plan", help="allocation_plan.json to freeze")
    parser.add_argument("spec_dir", nargs="?", default="isa/spec")
    args = parser.parse_args(argv)

    with Path(args.allocation_plan).open("r", encoding="utf-8") as fp:
        plan = json.load(fp)
    grouped = rows_by_mnemonic(plan)
    paths = mnemonic_files(Path(args.spec_dir))

    missing = sorted(set(grouped) - set(paths))
    if missing:
        raise SystemExit("missing instruction YAML files for: " + ", ".join(missing))

    changed = []
    for mnemonic, rows in sorted(grouped.items()):
        path = paths[mnemonic]
        if update_instruction_file(path, rows):
            changed.append(path)

    print(f"updated {len(changed)} instruction files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
