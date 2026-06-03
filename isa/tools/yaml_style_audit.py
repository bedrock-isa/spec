#!/usr/bin/env python3
"""Report YAML values that look like prose or compound policy strings.

This is intentionally a style audit, not a schema validator.  The ISA spec can
still contain prose in documentation fields and p-code-like operation fields,
but machine-readable policy should avoid long sentence-like enum strings such as
``foo_bar_baz_with_qux`` when a mapping would preserve the structure better.
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any, Iterable
import re
import sys

try:
    import yaml
except ImportError as exc:  # pragma: no cover
    raise SystemExit("PyYAML is required: python3 -m pip install pyyaml") from exc


DOC_KEYS = {
    "description",
    "summary",
    "title",
    "reason",
    "rationale",
    "note",
    "notes",
    "definition",
    "text",
    "purpose",
    "example",
    "examples",
    "syntax_examples",
}

PROSE_OR_CODE_KEYS = {
    "operation",
    "operation_by_mnemonic",
    "pcode",
    "pcode_by_mnemonic",
    "expression",
    "formula",
    "calculation",
    "description_by_mnemonic",
}

ALLOW_KEYS = DOC_KEYS | PROSE_OR_CODE_KEYS

MACHINE_TOKEN_KEYS = {
    "dst_ea_set",
    "extension_family",
    "extension_requirement",
}

CODEGEN_PATHS = {
    # EA constraints reference named EA sets; validators check these strings.
    ("instruction_ea_constraints",),
    # Allocation policy is consumed by the Z3 allocator.
    ("allocation",),
    # REPG continuation fields are exact validator inputs.
    ("prefixes", "fault_behavior", "precise_at"),
    ("prefixes", "fault_behavior", "continuation_state", "saved_pc"),
}

SUSPICIOUS_WORDS = re.compile(
    r"\b(TBD|choose|optional|defined_required|hardware_or_internal_assist|"
    r"unchanged_or|false_unless|only_if|or_defined|status_result_optional)\b",
    re.IGNORECASE,
)

LONG_COMPOUND = re.compile(r"^[A-Za-z][A-Za-z0-9]*(?:_[A-Za-z0-9]+){2,}$")


def load_yaml(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as fp:
        return yaml.safe_load(fp)


def scalar_path(path: Iterable[Any]) -> str:
    parts: list[str] = []
    for item in path:
        if isinstance(item, int):
            parts[-1:] = [f"{parts[-1]}[{item}]"] if parts else [f"[{item}]"]
        else:
            parts.append(str(item))
    return ".".join(parts)


def is_allowed_context(path: list[Any]) -> bool:
    keys = {str(item) for item in path if not isinstance(item, int)}
    key_path = tuple(str(item) for item in path if not isinstance(item, int))
    for allowed in CODEGEN_PATHS:
        if len(allowed) == 1 and allowed[0] in key_path:
            return True
        if all(part in key_path for part in allowed):
            return True
    if any(key.endswith(("_description", "_summary", "_note", "_notes", "_reason")) for key in keys):
        return True
    if keys & MACHINE_TOKEN_KEYS:
        return True
    return bool(keys & ALLOW_KEYS)


def audit_scalar(file: Path, path: list[Any], value: str) -> list[tuple[str, str, str]]:
    if is_allowed_context(path):
        return []
    text = value.strip()
    if not text:
        return []
    issues: list[tuple[str, str, str]] = []
    location = f"{file}:{scalar_path(path)}"
    if SUSPICIOUS_WORDS.search(text):
        issues.append(("ambiguous-token", location, text))
    if (
        len(text) >= 18
        and LONG_COMPOUND.match(text)
        and not re.fullmatch(r"[A-Z0-9_]+", text)
        and not text.startswith("R_BEDROCK_")
    ):
        issues.append(("compound-token", location, text))
    return issues


def walk(file: Path, value: Any, path: list[Any]) -> list[tuple[str, str, str]]:
    issues: list[tuple[str, str, str]] = []
    if isinstance(value, dict):
        for key, child in value.items():
            issues.extend(walk(file, child, [*path, key]))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            issues.extend(walk(file, child, [*path, index]))
    elif isinstance(value, str):
        issues.extend(audit_scalar(file, path, value))
    return issues


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="*", default=["isa/spec"], help="YAML files or directories")
    parser.add_argument("--fail", action="store_true", help="exit non-zero when issues are found")
    args = parser.parse_args(argv)

    files: list[Path] = []
    for raw in args.paths:
        path = Path(raw)
        if path.is_dir():
            files.extend(sorted(path.glob("*.yaml")))
        elif path.suffix in {".yaml", ".yml"}:
            files.append(path)

    issues: list[tuple[str, str, str]] = []
    for file in files:
        data = load_yaml(file)
        issues.extend(walk(file, data, []))

    if not issues:
        print("YAML style audit: no suspicious scalar policy tokens")
        return 0

    print("YAML style audit: suspicious scalar policy tokens")
    for kind, location, value in issues:
        print(f"- {kind}: {location}: {value}")
    return 1 if args.fail else 0


if __name__ == "__main__":
    raise SystemExit(main())
