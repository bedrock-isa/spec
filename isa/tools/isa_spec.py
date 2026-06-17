#!/usr/bin/env python3
"""Shared ISA specification loading, pattern parsing, and validation helpers."""

from __future__ import annotations

from pathlib import Path
import sys

from spec_model import (
    SPEC_FILES,
    SpecError,
    Pattern,
    PatternEntry,
    ValidationResult,
    aliases_for,
    catalog_entry_map,
    catalog_operand_schema,
    catalog_sections,
    check_overlaps,
    cleaned_pattern,
    entry_dict,
    entry_has_operand_profile,
    entry_id,
    family_section_entries,
    field_names,
    instruction_catalog,
    is_operand_spec,
    json_dumps,
    length_bounds,
    load_spec,
    load_yaml,
    load_yaml_with_includes,
    normalize_loaded_spec,
    normalized_family_catalog,
    operand_field_refs,
    operand_forms_from_value,
    overlap_allowed,
    parse_pattern,
    pattern_dict,
    patterns_overlap,
    semantic_entry_mnemonics,
    validate_spec_consistency,
)


def load_and_validate(spec_dir: str | Path) -> tuple[dict[str, object], ValidationResult, list[PatternEntry]]:
    spec = load_spec(spec_dir)
    result, entries = validate_spec_consistency(spec)
    return spec, result, entries


def print_result(result: ValidationResult, *, verbose: bool = False) -> None:
    for error in result.errors:
        print(f"error: {error}", file=sys.stderr)
    for warning in result.warnings:
        print(f"warning: {warning}", file=sys.stderr)
    if verbose:
        for info in result.infos:
            print(f"info: {info}")
