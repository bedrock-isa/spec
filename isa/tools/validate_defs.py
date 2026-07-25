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
    load_extensions,
    load_instruction_sets,
    load_operand_types,
    load_register_groups,
    load_size_definitions,
    load_yaml,
)
from defs_schema import (
    DecodeError,
    decode_encodings,
    decode_instruction,
    decode_yaml,
    verify_schema_lock,
)
from encoding_store import load_encoding_store


ROOT = Path("isa/defs")
INSTRUCTION_FILENAME = "instruction.yaml"
ENCODINGS_FILENAME = "encodings.yaml"


def iter_instruction_files(
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
            path = include.parent / item / INSTRUCTION_FILENAME
            if not path.is_file():
                errors.append(f"{include}: missing instruction definition {item}/{INSTRUCTION_FILENAME}")
                continue
            files.append(path)
    return files, errors


def normalized_sentence(value: str) -> str:
    return " ".join(re.sub(r"[^A-Za-z0-9]+", " ", value).lower().split())


def validate_description_tex(path: Path) -> list[str]:
    if not path.is_file():
        return [f"{path}: referenced TeX file does not exist"]
    text = path.read_text(encoding="utf-8").strip()
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
    architecture_path = root.parent / "reference" / "architecture_tables.yaml"
    try:
        architecture = load_yaml(architecture_path) if architecture_path.is_file() else {}
        event_names = {
            str(item["name"])
            for item in architecture.get("architectural_events", [])
            if isinstance(item, dict) and "name" in item
        }
    except (OSError, ValueError, KeyError, TypeError) as exc:
        event_names = set()
        errors.append(f"{architecture_path}: cannot load architectural event names: {exc}")
    try:
        verify_schema_lock()
        for path in sorted(root.rglob("*.yaml")):
            decode_yaml(path)
        catalog = load_extension_catalog(root)
        extensions = load_extensions(root, catalog)
        register_groups = load_register_groups(root, extensions)
        instruction_sets = load_instruction_sets(root, extensions)
        operand_types = load_operand_types(root, extensions)
        sizes = load_size_definitions(root, extensions)
    except (OSError, ValueError, DecodeError) as exc:
        return {}, [str(exc)]

    cpuid_positions: dict[tuple[int, int, int, int], str] = {}
    cpuid_features: dict[str, str] = {}
    for name, extension in extensions.items():
        availability = extension.data.get("availability")
        cpuid = availability.get("cpuid") if isinstance(availability, dict) else None
        if not isinstance(cpuid, dict):
            continue
        position = (
            int(cpuid["class"]),
            int(cpuid["leaf"]),
            int(cpuid["index"]),
            int(cpuid["bit"]),
        )
        if any(value < 0 for value in position[:3]) or not 0 <= position[3] < 64:
            errors.append(f"{extension.path}: invalid CPUID feature position {position}")
        previous = cpuid_positions.get(position)
        if previous is not None:
            errors.append(
                f"{extension.path}: CPUID position {position} duplicates extension {previous}"
            )
        cpuid_positions[position] = name
        feature = str(cpuid["feature"])
        previous = cpuid_features.get(feature)
        if previous is not None:
            errors.append(
                f"{extension.path}: CPUID feature {feature} duplicates extension {previous}"
            )
        cpuid_features[feature] = name

    instruction_files, include_errors = iter_instruction_files(instruction_sets)
    errors.extend(include_errors)
    listed = set(instruction_files)
    discovered = set(root.glob("**/instructions/*/instruction.yaml"))
    for path in sorted(discovered - listed):
        errors.append(f"{path}: instruction definition is not listed by an instructions.yaml index")
    for path in sorted(listed - discovered):
        errors.append(f"{path}: listed instruction definition is outside the directory contract")

    known_operand_types = set(operand_types)
    known_sizes = set((sizes.get("size_codes") or {}).keys())
    known_field_types = known_operand_types | {"size"}
    mnemonics: dict[str, Path] = {}
    instruction_families: Counter[str] = Counter()
    used_operand_types: Counter[str] = Counter()
    details_count = 0
    encoding_count = 0

    for path in instruction_files:
        try:
            document = decode_instruction(path, load_yaml(path))
        except (OSError, ValueError, DecodeError) as exc:
            errors.append(str(exc))
            continue
        mnemonic = document.mnemonic
        if path.parent.name != mnemonic:
            errors.append(f"{path}: directory name must match mnemonic {mnemonic}")
        previous = mnemonics.get(mnemonic)
        if previous is not None:
            errors.append(f"duplicate mnemonic {mnemonic}: {previous} and {path}")
        mnemonics[mnemonic] = path
        instruction_families[document.attributes.family] += 1

        summary = " ".join(document.summary.split())
        if len(summary) > 120:
            errors.append(f"{path}: summary exceeds 120 characters")
        if len(re.findall(r"[.!?](?:\s|$)", summary)) != 1:
            errors.append(f"{path}: summary must contain exactly one sentence")
        if "\n\n" in document.description.strip():
            errors.append(f"{path}: description must be a single paragraph")
        if normalized_sentence(document.description).startswith(normalized_sentence(summary)):
            errors.append(f"{path}: description repeats summary as its opening sentence")

        if document.additional_description is not None:
            details_count += 1
            errors.extend(validate_description_tex(path.parent / document.additional_description))

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
        if document.repeat is not None and document.repeat.observed is not None:
            observed_operand = document.repeat.observed.operand
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
        for exception in document.exceptions:
            if exception.event not in event_names:
                errors.append(
                    f"{path}: exception references unknown event {exception.event}"
                )
            unknown_forms = set(exception.forms) - form_ids
            if unknown_forms:
                errors.append(
                    f"{path}: exception {exception.event} references unknown forms "
                    f"{', '.join(sorted(unknown_forms))}"
                )
        for form in encodings.forms:
            head = re.split(r"[./(]", form.syntax.split()[0])[0]
            if head != mnemonic:
                errors.append(
                    f"{encodings_path}: form {form.id} syntax names {head}, expected {mnemonic}"
                )
            for operand in form.operands:
                used_operand_types[operand.type] += 1
                if operand.type not in known_operand_types:
                    errors.append(
                        f"{encodings_path}: form {form.id} uses unknown operand type {operand.type}"
                    )
                elif operand.field is not None:
                    expected_width = int(operand_types[operand.type]["field_width"])
                    actual_width = form.bits.count(operand.field)
                    if actual_width != expected_width:
                        errors.append(
                            f"{encodings_path}: form {form.id} operand {operand.name} "
                            f"has {actual_width}-bit field, but {operand.type} requires {expected_width}"
                        )
            for marker, field in form.fields.items():
                if field.type not in known_field_types:
                    errors.append(
                        f"{encodings_path}: form {form.id} field {marker} uses unknown type {field.type}"
                    )
                elif field.type != "size":
                    expected_width = int(operand_types[field.type]["field_width"])
                    actual_width = form.bits.count(marker)
                    if actual_width != expected_width:
                        errors.append(
                            f"{encodings_path}: form {form.id} selector {marker} "
                            f"has {actual_width} bits, but {field.type} requires {expected_width}"
                        )
            for size in form.sizes:
                if size not in known_sizes:
                    errors.append(
                        f"{encodings_path}: form {form.id} uses unknown size {size}"
                    )

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
    parser.add_argument("--root", type=Path, default=ROOT)
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
