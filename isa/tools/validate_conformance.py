#!/usr/bin/env python3
"""Validate the ISA conformance manifest and its referenced case families."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_MANIFEST = ROOT / "isa" / "reference" / "conformance_manifest.yaml"

MANIFEST_TOP_KEYS = {"schema_version", "families", "implementation_defined"}
MANIFEST_FAMILY_KEYS = {"id", "source", "required_cases"}
MANIFEST_IMPLEMENTATION_KEYS = {"id", "definition", "publication"}


class ConformanceError(ValueError):
    """A conformance source violates its repository contract."""


def _load_yaml(path: Path) -> Any:
    with path.open(encoding="utf-8") as stream:
        return yaml.safe_load(stream)


def _mapping(value: Any, where: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ConformanceError(f"{where}: expected mapping")
    return value


def _list(value: Any, where: str) -> list[Any]:
    if not isinstance(value, list):
        raise ConformanceError(f"{where}: expected list")
    return value


def _exact_keys(value: dict[str, Any], expected: set[str], where: str) -> None:
    actual = set(value)
    if actual != expected:
        missing = ", ".join(sorted(expected - actual)) or "-"
        extra = ", ".join(sorted(actual - expected)) or "-"
        raise ConformanceError(
            f"{where}: key mismatch; missing [{missing}], extra [{extra}]"
        )


def _nonempty_string(value: Any, where: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ConformanceError(f"{where}: expected non-empty string")
    return value


def _collect_ids(value: Any) -> set[str]:
    result: set[str] = set()
    if isinstance(value, dict):
        identifier = value.get("id")
        if isinstance(identifier, str):
            result.add(identifier)
        for child in value.values():
            result.update(_collect_ids(child))
    elif isinstance(value, list):
        for child in value:
            result.update(_collect_ids(child))
    return result


def validate_manifest_document(raw: Any, root: Path = ROOT) -> None:
    document = _mapping(raw, "conformance manifest")
    _exact_keys(document, MANIFEST_TOP_KEYS, "conformance manifest")
    if document["schema_version"] != 0:
        raise ConformanceError("conformance manifest.schema_version: expected 0")

    family_ids: set[str] = set()
    for index, raw_family in enumerate(
        _list(document["families"], "conformance manifest.families")
    ):
        where = f"conformance manifest.families[{index}]"
        family = _mapping(raw_family, where)
        _exact_keys(family, MANIFEST_FAMILY_KEYS, where)
        family_id = _nonempty_string(family["id"], f"{where}.id")
        if family_id in family_ids:
            raise ConformanceError(f"{where}.id: duplicate {family_id!r}")
        family_ids.add(family_id)

        source = _nonempty_string(family["source"], f"{where}.source")
        source_path = Path(source)
        if source_path.is_absolute() or ".." in source_path.parts:
            raise ConformanceError(f"{where}.source: expected repository-relative path")
        resolved = root / source_path
        if not resolved.is_file() or resolved.suffix not in {".yaml", ".yml"}:
            raise ConformanceError(f"{where}.source: expected existing YAML file")
        required_cases = _list(family["required_cases"], f"{where}.required_cases")
        if (
            not required_cases
            or any(not isinstance(item, str) or not item for item in required_cases)
            or len(required_cases) != len(set(required_cases))
        ):
            raise ConformanceError(
                f"{where}.required_cases: expected unique non-empty strings"
            )
        available_ids = _collect_ids(_load_yaml(resolved))
        missing = set(required_cases) - available_ids
        if missing:
            raise ConformanceError(
                f"{where}.required_cases: absent from {source}: "
                + ", ".join(sorted(missing))
            )

    implementation_ids: set[str] = set()
    implementation_items = _list(
        document["implementation_defined"],
        "conformance manifest.implementation_defined",
    )
    for index, raw_item in enumerate(implementation_items):
        where = f"conformance manifest.implementation_defined[{index}]"
        item = _mapping(raw_item, where)
        _exact_keys(item, MANIFEST_IMPLEMENTATION_KEYS, where)
        identifier = _nonempty_string(item["id"], f"{where}.id")
        if identifier in implementation_ids:
            raise ConformanceError(f"{where}.id: duplicate {identifier!r}")
        implementation_ids.add(identifier)
        _nonempty_string(item["definition"], f"{where}.definition")
        _nonempty_string(item["publication"], f"{where}.publication")


def validate_paths(
    manifest_path: Path = DEFAULT_MANIFEST,
    root: Path = ROOT,
) -> None:
    validate_manifest_document(_load_yaml(manifest_path), root)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    args = parser.parse_args()
    try:
        validate_paths(args.manifest)
    except (ConformanceError, ValueError) as exc:
        print(f"conformance validation failed: {exc}", file=sys.stderr)
        return 1
    print("conformance manifest is valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
