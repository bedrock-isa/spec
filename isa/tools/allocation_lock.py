"""Per-instruction encoding lock extraction and verification."""

from __future__ import annotations

from typing import Any


INSTRUCTION_SECTIONS = ("compact_primary", "integer", "system", "fpu")
FAMILY_SECTION_METADATA = {"description", "notes", "category", "registers"}

PRIMARY_KEYS = (
    "id",
    "kind",
    "start_payload",
    "end_payload",
    "slots",
    "primary_bits",
    "field_layout",
    "fields",
    "primary_payloads",
    "alias_payloads",
    "alias_of",
    "alias_condition",
    "canonical_disassembly",
)

EXTENDED_KEYS = (
    "id",
    "kind",
    "extension_root",
    "extension_root_payload",
    "extension_family",
    "extended_opcode",
    "extended_opcode_start",
    "extended_opcode_end",
    "extended_opcode_slots",
    "extended_opcode_bits",
    "operand_payload_bits",
    "operand_descriptor_words",
    "operand_descriptor_spilled",
    "descriptor_layout",
    "fields",
    "alias_payloads",
    "alias_of",
    "alias_condition",
    "canonical_disassembly",
)

FIELD_KEYS = (
    "name",
    "kind",
    "source",
    "storage",
    "width",
    "low_bit",
    "high_bit",
    "range",
    "value",
    "value_label",
    "placement",
)


def allocation_lock_from_plan(plan: dict[str, Any]) -> dict[str, Any]:
    solver = plan.get("solver") if isinstance(plan.get("solver"), dict) else plan
    return {"encoding": instruction_encoding_rows_from_solver_result(solver)}


def instruction_encoding_rows_from_plan(plan: dict[str, Any]) -> list[dict[str, Any]]:
    solver = plan.get("solver") if isinstance(plan.get("solver"), dict) else plan
    return instruction_encoding_rows_from_solver_result(solver)


def instruction_encoding_rows_from_solver_result(solver_result: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    rows.extend(
        locked_row(row, PRIMARY_KEYS)
        for row in solver_result.get("primary_allocations", []) or []
        if isinstance(row, dict) and row.get("kind") != "extension_root"
    )
    rows.extend(
        locked_row(row, PRIMARY_KEYS)
        for row in solver_result.get("primary_alias_allocations", []) or []
        if isinstance(row, dict)
    )
    rows.extend(
        locked_row(row, EXTENDED_KEYS)
        for row in solver_result.get("extended_allocations", []) or []
        if isinstance(row, dict)
    )
    rows.extend(
        locked_row(row, EXTENDED_KEYS)
        for row in solver_result.get("extended_alias_allocations", []) or []
        if isinstance(row, dict)
    )
    return sorted(rows, key=instruction_row_sort_key)


def instruction_row_sort_key(row: dict[str, Any]) -> tuple[int, str, str]:
    kind_rank = {
        "compact": 0,
        "compact_alias": 1,
        "extended": 2,
        "extended_alias": 3,
    }
    return (kind_rank.get(str(row.get("kind", "")), 99), str(row.get("id", "")), str(row.get("extended_opcode", "")))


def locked_row(row: dict[str, Any], keys: tuple[str, ...]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key in keys:
        if key not in row:
            continue
        value = row[key]
        if key == "fields":
            value = [locked_field(field) for field in value if isinstance(field, dict)]
        out[key] = normalize_scalar_tree(value)
    if "kind" in keys and "kind" not in out and "extended_opcode" in out:
        out["kind"] = "extended"
    return out


def locked_field(field: dict[str, Any]) -> dict[str, Any]:
    return {
        key: normalize_scalar_tree(field[key])
        for key in FIELD_KEYS
        if key in field
    }


def normalize_scalar_tree(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(key): normalize_scalar_tree(item) for key, item in value.items()}
    if isinstance(value, list):
        return [normalize_scalar_tree(item) for item in value]
    if isinstance(value, tuple):
        return [normalize_scalar_tree(item) for item in value]
    return value


def spec_encoding_rows(spec: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    families = ((spec.get("instructions") or {}).get("families") or {})
    if not isinstance(families, dict):
        return rows
    for family in families.values():
        if not isinstance(family, dict):
            continue
        for section_name in INSTRUCTION_SECTIONS:
            section = family.get(section_name)
            if not isinstance(section, dict):
                continue
            entries = section.get("entries") if isinstance(section.get("entries"), dict) else {
                key: item
                for key, item in section.items()
                if key not in FAMILY_SECTION_METADATA
            }
            if not isinstance(entries, dict):
                continue
            for entry in entries.values():
                if not isinstance(entry, dict):
                    continue
                encoding = entry.get("encoding", []) or []
                if isinstance(encoding, list):
                    rows.extend(normalize_scalar_tree(row) for row in encoding if isinstance(row, dict))
    return sorted(rows, key=instruction_row_sort_key)


def allocation_lock_errors(expected_rows: list[dict[str, Any]], solver_result: dict[str, Any]) -> list[str]:
    if not expected_rows:
        return []
    actual_rows = instruction_encoding_rows_from_solver_result(solver_result)
    return section_errors("instruction_encoding", expected_rows, actual_rows)


def section_errors(section: str, expected_rows: list[Any], actual_rows: list[Any]) -> list[str]:
    errors: list[str] = []
    expected, expected_duplicates = rows_by_id(expected_rows)
    actual, actual_duplicates = rows_by_id(actual_rows)
    for ident in expected_duplicates:
        errors.append(f"{section}: duplicate locked id {ident}")
    for ident in actual_duplicates:
        errors.append(f"{section}: duplicate allocator id {ident}")

    expected_ids = set(expected)
    actual_ids = set(actual)
    for ident in sorted(expected_ids - actual_ids):
        errors.append(f"{section}.{ident}: locked encoding is missing from allocator output")
    for ident in sorted(actual_ids - expected_ids):
        errors.append(f"{section}.{ident}: allocator produced an unlocked encoding")

    for ident in sorted(expected_ids & actual_ids):
        errors.extend(row_errors(section, ident, expected[ident], actual[ident]))
    return errors


def rows_by_id(rows: list[Any]) -> tuple[dict[str, dict[str, Any]], list[str]]:
    out: dict[str, dict[str, Any]] = {}
    duplicates: list[str] = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        ident = str(row.get("id", ""))
        if not ident:
            continue
        if ident in out:
            duplicates.append(ident)
            continue
        out[ident] = normalize_scalar_tree(row)
    return out, duplicates


def row_errors(section: str, ident: str, expected: dict[str, Any], actual: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for key in sorted(set(expected) | set(actual)):
        if expected.get(key) == actual.get(key):
            continue
        errors.append(
            f"{section}.{ident}.{key}: expected {short_value(expected.get(key))}, got {short_value(actual.get(key))}"
        )
    return errors


def short_value(value: Any) -> str:
    text = repr(value)
    if len(text) <= 160:
        return text
    return text[:157] + "..."
