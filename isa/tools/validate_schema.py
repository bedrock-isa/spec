#!/usr/bin/env python3
"""Strictly decode every YAML document in the repository."""

from __future__ import annotations

import argparse
from pathlib import Path

from defs_schema import DecodeError, decode_yaml, verify_schema_lock


ROOT = Path(__file__).resolve().parents[2]


def document_paths(root: Path) -> list[Path]:
    paths = sorted((root / "isa" / "instructions" / "definitions").rglob("*.yaml"))
    paths.extend(
        (
            root / "isa" / "addressing" / "effective_address" / "definition.yaml",
            root / "isa" / "interfaces" / "abi" / "plt_conformance_vectors.yaml",
            root / "isa" / "memory" / "ordering" / "formal" / "validation.yaml",
        )
    )
    return paths


def validate_schema(root: Path = ROOT) -> tuple[int, list[str]]:
    errors: list[str] = []
    try:
        verify_schema_lock(
            root / "isa" / "instructions" / "definitions" / "schema.lock"
        )
    except DecodeError as exc:
        errors.append(str(exc))
        return 0, errors
    count = 0
    for path in document_paths(root):
        if not path.is_file():
            errors.append(f"{path}: required schema document does not exist")
            continue
        try:
            decode_yaml(path)
            count += 1
        except DecodeError as exc:
            errors.append(str(exc))
    return count, errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=ROOT,
        help="repository root containing schema documents",
    )
    args = parser.parse_args()
    count, errors = validate_schema(args.root.resolve())
    print(f"decoded documents: {count}")
    print(f"errors: {len(errors)}")
    for error in errors:
        print(f"  {error}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
