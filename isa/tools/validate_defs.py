#!/usr/bin/env python3
"""Strictly validate the integrated ISA definition tree and its references."""

from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path
import re
from typing import Any

from defs_loader import (
    InstructionSetDef,
    load_extension_catalog,
    extension_cpuid_requirements,
    load_architectural_event_causes,
    load_architectural_event_ids,
    load_cpuid_flags,
    load_extensions,
    load_field_types,
    load_flag_effect_definitions,
    load_instruction_sets,
    load_operation,
    load_named_values,
    load_operand_types,
    load_register_groups,
    load_semantic_conditions,
    load_size_definitions,
    load_yaml,
)
from defs_schema import DecodeError, decode_encodings, decode_yaml, verify_schema_lock
from encoding_store import load_encoding_store
from encoding_fields import resolve_encoding_form
from encoding_fields import validate_encoding_template
from artifact_overlay import resolve_source


ROOT = Path(__file__).resolve().parents[2] / "isa" / "instructions" / "definitions"
OPERATION_FILENAME = "operation.yaml"
ENCODINGS_FILENAME = "encodings.yaml"


def iter_operation_files(
    instruction_sets: list[InstructionSetDef],
) -> tuple[list[Path], list[str]]:
    errors: list[str] = []
    files: list[Path] = []
    for instruction_set in instruction_sets:
        include = instruction_set.include
        if instruction_set.introduction is not None and not instruction_set.introduction.is_file():
            errors.append(
                f"{include}: missing introduction {instruction_set.introduction.name}"
            )
        data = load_yaml(include)
        include_items = data.get("include") if isinstance(data, dict) else None
        if not isinstance(include_items, list):
            errors.append(f"{include}: include must be a list of instruction directories")
            continue
        for item in include_items:
            if not isinstance(item, str) or not item.strip():
                errors.append(f"{include}: instruction include entries must be non-empty strings")
                continue
            path = include.parent / item / OPERATION_FILENAME
            if not path.is_file():
                errors.append(f"{include}: missing operation definition {item}/{OPERATION_FILENAME}")
                continue
            files.append(path)
    return files, errors


def validate_description_tex(path: Path) -> list[str]:
    repository_root = ROOT.parents[2]
    resolved = resolve_source(path, repository_root)
    if not resolved.is_file():
        return [f"{path}: referenced TeX file does not exist"]
    text = resolved.read_text(encoding="utf-8").strip()
    errors: list[str] = []
    if not text:
        errors.append(f"{path}: referenced TeX file must not be empty")
    forbidden = (
        re.search(r"\\(?:sub)*section\s*(?!\*)\{", text)
        or re.search(r"\\addcontentsline\s*\{toc\}", text)
        or re.search(
            r"\\(?:input|include|documentclass)\b|\\begin\s*\{document\}|\\end\s*\{document\}",
            text,
        )
    )
    if forbidden:
        errors.append(f"{path}: additional description contains a forbidden document-structure command")
    return errors


def validate_defs(root: Path = ROOT) -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    event_path = root.parent.parent / "system" / "events" / "architectural_events.yaml"
    try:
        verify_schema_lock()
        for path in sorted(root.rglob("*.yaml")):
            decode_yaml(path)
        catalog = load_extension_catalog(root)
        extensions = load_extensions(root, catalog)
        cpuid_flags = load_cpuid_flags(root)
        register_groups = load_register_groups(root, extensions)
        instruction_sets = load_instruction_sets(root, extensions)
        field_types = load_field_types(root, extensions)
        operand_types = load_operand_types(root, extensions)
        size_definitions = load_size_definitions(root, extensions)
        known_cpuid_flags, requirements_by_set = extension_cpuid_requirements(
            extensions, cpuid_flags
        )
        known_event_ids = load_architectural_event_ids(event_path)
        known_event_causes = load_architectural_event_causes(event_path)
        known_conditions = frozenset(load_semantic_conditions(root))
        known_named_values = frozenset(load_named_values(root))
        known_flag_effects = load_flag_effect_definitions(root)
    except (OSError, ValueError, DecodeError) as exc:
        return {}, [str(exc)]

    instruction_files, include_errors = iter_operation_files(instruction_sets)
    errors.extend(include_errors)
    listed = set(instruction_files)
    discovered = set(root.glob("**/instructions/*/operation.yaml"))
    for path in sorted(discovered - listed):
        errors.append(f"{path}: operation definition is not listed by an instructions.yaml index")
    for path in sorted(listed - discovered):
        errors.append(f"{path}: listed operation definition is outside the directory contract")

    mnemonics: dict[str, Path] = {}
    instruction_families: Counter[str] = Counter()
    used_operand_types: Counter[str] = Counter()
    details_count = 0
    encoding_count = 0

    for path in instruction_files:
        try:
            instruction_set = next(
                item
                for item in instruction_sets
                if path.is_relative_to(item.include.parent)
            )
            document = load_operation(
                path.parent,
                operand_types=operand_types,
                size_definitions=size_definitions,
                base_requirements=requirements_by_set[instruction_set.name],
                known_cpuid_flags=known_cpuid_flags,
                known_event_ids=known_event_ids,
                known_event_causes=known_event_causes,
                known_condition_ids=known_conditions,
                known_named_value_ids=known_named_values,
                known_diagram_kinds=frozenset({"vector-example"}),
                known_flag_effect_definitions=known_flag_effects,
            )
        except (OSError, ValueError, DecodeError) as exc:
            errors.append(str(exc))
            continue
        mnemonic = document.public_instruction.mnemonic
        if path.parent.name != mnemonic:
            errors.append(f"{path}: directory name must match mnemonic {mnemonic}")
        previous = mnemonics.get(mnemonic)
        if previous is not None:
            errors.append(f"duplicate mnemonic {mnemonic}: {previous} and {path}")
        mnemonics[mnemonic] = path
        instruction_families[document.execution_route or "unrouted"] += 1
        if document.artifacts is not None:
            details_count += 1
            errors.extend(validate_description_tex(path.parent / document.artifacts.description.path))

        encodings_path = path.with_name(ENCODINGS_FILENAME)
        if not encodings_path.is_file():
            errors.append(f"{path}: missing {ENCODINGS_FILENAME}")
            continue
        try:
            encodings = decode_encodings(encodings_path, load_yaml(encodings_path))
        except (OSError, ValueError, DecodeError) as exc:
            errors.append(str(exc))
            continue
        encoding_count += len(encodings.forms)
        form_ids = {form.id for form in encodings.forms}
        if document.repeat.observed is not None:
            observed_operand = getattr(document.repeat.observed, "operand", None)
            if observed_operand is not None:
                missing_forms = [
                    form.id
                    for form in encodings.forms
                    if observed_operand not in {operand.name for operand in form.operands}
                ]
                if missing_forms:
                    errors.append(
                        f"{path}: repeat observed operand {observed_operand} is absent from "
                        f"forms {', '.join(missing_forms)}"
                    )
        valid_forms = []
        for decoded_form in encodings.forms:
            try:
                validate_encoding_template(
                    decoded_form,
                    mnemonic,
                    field_types,
                    encodings_path,
                )
                form = resolve_encoding_form(decoded_form, field_types, encodings_path)
            except ValueError as exc:
                errors.append(str(exc))
                continue
            valid_forms.append(decoded_form)
            for operand in form.operands:
                used_operand_types[operand.type] += 1

    discovered_encoding_files = set(root.glob("**/instructions/*/encodings.yaml"))
    expected_encoding_files = {path.with_name(ENCODINGS_FILENAME) for path in instruction_files}
    for path in sorted(discovered_encoding_files - expected_encoding_files):
        errors.append(f"{path}: encodings file is outside a listed instruction directory")

    try:
        store = load_encoding_store(root)
        if len(store.encodings) != encoding_count:
            errors.append("global encoding store count differs from per-instruction decode count")
    except (OSError, ValueError, DecodeError) as exc:
        errors.append(str(exc))

    summary = {
        "extension_definitions": len(extensions),
        "register_groups": len(register_groups),
        "instruction_files": len(instruction_files),
        "instructions": len(mnemonics),
        "instruction_details": details_count,
        "encodings": encoding_count,
        "instruction_families": dict(sorted(instruction_families.items())),
        "operand_types": dict(sorted(used_operand_types.items())),
    }
    return summary, errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=ROOT,
        help=(
            "ISA definition root "
            "(default: repository isa/instructions/definitions)"
        ),
    )
    args = parser.parse_args()
    summary, errors = validate_defs(args.root)
    print(args.root)
    for key in (
        "extension_definitions",
        "register_groups",
        "instruction_files",
        "instructions",
        "instruction_details",
        "encodings",
    ):
        print(f"  {key}: {summary.get(key, 0)}")
    print("  instruction families:", len(summary.get("instruction_families", {})))
    print(f"  errors: {len(errors)}")
    for error in errors[:40]:
        print(f"    {error}")
    if len(errors) > 40:
        print(f"    ... {len(errors) - 40} more")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
