#!/usr/bin/env python3
"""Validate ISA conformance manifests and exact assembler golden vectors."""

from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path
import sys
from typing import Any

import yaml

TOOL_DIR = Path(__file__).resolve().parent
if str(TOOL_DIR) not in sys.path:
    sys.path.insert(0, str(TOOL_DIR))

from encoding_architecture import ENCODING_CLASSES_BY_NAME  # noqa: E402
from encoding_store import EncodingStore, LocatedEncoding, load_encoding_store  # noqa: E402


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_GOLDEN = ROOT / "isa" / "reference" / "assembler_golden_vectors.yaml"
DEFAULT_MANIFEST = ROOT / "isa" / "reference" / "conformance_manifest.yaml"

GOLDEN_TOP_KEYS = {"schema_version", "cases"}
GOLDEN_CASE_KEYS = {
    "id",
    "assembly",
    "form_id",
    "field_values",
    "payload_bytes",
    "encoded_bytes",
    "canonical_disassembly",
    "covers",
}
REQUIRED_GOLDEN_COVERAGE = {
    "extrashort",
    "short",
    "medium",
    "long",
    "extralong",
    "register",
    "indirect",
    "displacement",
    "SP",
    "PC",
    "absolute",
    "immediate",
    "EXT0",
    "condition_size",
    "alias",
    "LEN_padding",
}

MANIFEST_TOP_KEYS = {"schema_version", "families", "implementation_defined"}
MANIFEST_FAMILY_KEYS = {"id", "source", "required_cases"}
MANIFEST_IMPLEMENTATION_KEYS = {"id", "definition", "publication"}
REQUIRED_MANIFEST_SOURCES = {
    "isa/reference/assembler_golden_vectors.yaml",
    "isa/memory_model/atomic_order_litmus.yaml",
    "isa/reference/address_translation_test_vectors.yaml",
    "isa/reference/stack_event_test_vectors.yaml",
    "isa/memory_model/validation.yaml",
    "isa/memory_model/cache_sync_litmus.yaml",
    "isa/reference/fp_common_test_vectors.yaml",
}


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


def _byte_list(value: Any, where: str) -> list[int]:
    result = _list(value, where)
    for index, byte in enumerate(result):
        if not isinstance(byte, int) or isinstance(byte, bool) or not 0 <= byte <= 0xFF:
            raise ConformanceError(f"{where}[{index}]: expected byte")
    return result


def _integer_mapping(value: Any, where: str) -> dict[str, int]:
    result = _mapping(value, where)
    for name, number in result.items():
        if not isinstance(name, str) or len(name) != 1 or not name.islower():
            raise ConformanceError(f"{where}: invalid field marker {name!r}")
        if not isinstance(number, int) or isinstance(number, bool) or number < 0:
            raise ConformanceError(f"{where}.{name}: expected nonnegative integer")
    return result


def _form_index(store: EncodingStore) -> dict[str, LocatedEncoding]:
    return {located.form.id: located for located in store.encodings}


def _substitute_fields(
    located: LocatedEncoding,
    field_values: dict[str, int],
    where: str,
) -> str:
    bits = located.form.bits
    if "?" in bits:
        raise ConformanceError(f"{where}: golden form may not contain wildcard bits")
    widths = Counter(char for char in bits if char not in "01")
    if set(field_values) != set(widths):
        missing = ", ".join(sorted(set(widths) - set(field_values))) or "-"
        extra = ", ".join(sorted(set(field_values) - set(widths))) or "-"
        raise ConformanceError(
            f"{where}.field_values: marker mismatch; missing [{missing}], extra [{extra}]"
        )

    encoded_fields: dict[str, str] = {}
    for marker, width in widths.items():
        value = field_values[marker]
        if value >= 1 << width:
            raise ConformanceError(
                f"{where}.field_values.{marker}: {value} does not fit {width} bits"
            )
        encoded_fields[marker] = f"{value:0{width}b}"

    positions = Counter()
    result: list[str] = []
    for char in bits:
        if char in "01":
            result.append(char)
            continue
        result.append(encoded_fields[char][positions[char]])
        positions[char] += 1
    return "".join(result)


def encode_golden_case(
    case: dict[str, Any],
    form_index: dict[str, LocatedEncoding],
    where: str = "case",
) -> bytes:
    """Encode one exact golden case from its form fields and appended bytes."""

    form_id = _nonempty_string(case.get("form_id"), f"{where}.form_id")
    located = form_index.get(form_id)
    if located is None:
        raise ConformanceError(f"{where}.form_id: unknown form {form_id!r}")

    field_values = _integer_mapping(case.get("field_values"), f"{where}.field_values")
    opcode_bits = _substitute_fields(located, field_values, where)
    encoding_class = ENCODING_CLASSES_BY_NAME[located.form.encoding_class]
    if len(opcode_bits) != encoding_class.payload_bits:
        raise ConformanceError(
            f"{where}: form payload has {len(opcode_bits)} bits, "
            f"expected {encoding_class.payload_bits}"
        )

    payload = _byte_list(case.get("payload_bytes"), f"{where}.payload_bytes")
    expected = _byte_list(case.get("encoded_bytes"), f"{where}.encoded_bytes")
    if located.form.encoding_class == "extrashort":
        if payload or len(expected) != 1:
            raise ConformanceError(f"{where}: extrashort form must be exactly one byte")
        record_bits = "0" + opcode_bits
    elif located.form.encoding_class == "short":
        if payload or len(expected) != 2:
            raise ConformanceError(f"{where}: short form must be exactly two bytes")
        record_bits = "10" + opcode_bits
    else:
        total_bytes = encoding_class.instruction_bytes + len(payload)
        if total_bytes != len(expected):
            raise ConformanceError(
                f"{where}: encoded length must equal class minimum plus payload bytes"
            )
        if not 3 <= total_bytes <= 18:
            raise ConformanceError(f"{where}: extended record length must be 3..18")
        record_bits = f"11{total_bytes - 3:04b}" + opcode_bits

    if len(record_bits) % 8:
        raise ConformanceError(f"{where}: internal bit packing is not byte aligned")
    record = bytes(
        int(record_bits[offset : offset + 8], 2)
        for offset in range(0, len(record_bits), 8)
    ) + bytes(payload)
    if record != bytes(expected):
        actual_text = " ".join(f"{byte:02x}" for byte in record)
        expected_text = " ".join(f"{byte:02x}" for byte in expected)
        raise ConformanceError(
            f"{where}.encoded_bytes: reconstructed [{actual_text}], "
            f"declared [{expected_text}]"
        )
    return record


def _validate_round_trip(
    case: dict[str, Any],
    located: LocatedEncoding,
    record: bytes,
    where: str,
) -> None:
    """Recover the selected form fields from the encoded opcode payload."""

    encoding_class = ENCODING_CLASSES_BY_NAME[located.form.encoding_class]
    bits = "".join(f"{byte:08b}" for byte in record)
    if located.form.encoding_class == "extrashort":
        if bits[0] != "0":
            raise ConformanceError(f"{where}: invalid extrashort header")
        opcode = bits[1 : 1 + encoding_class.payload_bits]
    elif located.form.encoding_class == "short":
        if bits[:2] != "10":
            raise ConformanceError(f"{where}: invalid short header")
        opcode = bits[2 : 2 + encoding_class.payload_bits]
    else:
        if bits[:2] != "11" or int(bits[2:6], 2) + 3 != len(record):
            raise ConformanceError(f"{where}: invalid extended length header")
        opcode = bits[6 : 6 + encoding_class.payload_bits]

    recovered: dict[str, list[str]] = {}
    for pattern_bit, encoded_bit in zip(located.form.bits, opcode, strict=True):
        if pattern_bit in "01":
            if pattern_bit != encoded_bit:
                raise ConformanceError(f"{where}: encoded opcode does not match form")
        elif pattern_bit == "?":
            raise ConformanceError(f"{where}: golden form may not contain wildcard bits")
        else:
            recovered.setdefault(pattern_bit, []).append(encoded_bit)
    values = {name: int("".join(value), 2) for name, value in recovered.items()}
    if values != case["field_values"]:
        raise ConformanceError(
            f"{where}: decoded fields {values!r} do not match {case['field_values']!r}"
        )


def validate_golden_document(raw: Any, store: EncodingStore) -> None:
    document = _mapping(raw, "assembler golden vectors")
    _exact_keys(document, GOLDEN_TOP_KEYS, "assembler golden vectors")
    if document["schema_version"] != 0:
        raise ConformanceError("assembler golden vectors.schema_version: expected 0")

    cases = _list(document["cases"], "assembler golden vectors.cases")
    if not cases:
        raise ConformanceError("assembler golden vectors.cases: expected non-empty list")
    index = _form_index(store)
    ids: set[str] = set()
    coverage: set[str] = set()
    for case_index, raw_case in enumerate(cases):
        where = f"assembler golden vectors.cases[{case_index}]"
        case = _mapping(raw_case, where)
        _exact_keys(case, GOLDEN_CASE_KEYS, where)
        case_id = _nonempty_string(case["id"], f"{where}.id")
        if case_id in ids:
            raise ConformanceError(f"{where}.id: duplicate {case_id!r}")
        ids.add(case_id)
        assembly = _nonempty_string(case["assembly"], f"{where}.assembly")
        canonical = _nonempty_string(
            case["canonical_disassembly"], f"{where}.canonical_disassembly"
        )
        covers = _list(case["covers"], f"{where}.covers")
        if not covers or any(not isinstance(item, str) or not item for item in covers):
            raise ConformanceError(f"{where}.covers: expected non-empty string list")
        if len(covers) != len(set(covers)):
            raise ConformanceError(f"{where}.covers: duplicate tag")
        coverage.update(covers)
        if "alias" not in covers and assembly != canonical:
            raise ConformanceError(
                f"{where}: non-alias assembly must equal canonical disassembly"
            )

        form_id = _nonempty_string(case["form_id"], f"{where}.form_id")
        located = index.get(form_id)
        if located is None:
            raise ConformanceError(f"{where}.form_id: unknown form {form_id!r}")
        record = encode_golden_case(case, index, where)
        _validate_round_trip(case, located, record, where)

    missing_coverage = REQUIRED_GOLDEN_COVERAGE - coverage
    if missing_coverage:
        raise ConformanceError(
            "assembler golden vectors: missing coverage "
            + ", ".join(sorted(missing_coverage))
        )


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
    sources: set[str] = set()
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
        sources.add(source)

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

    missing_sources = REQUIRED_MANIFEST_SOURCES - sources
    if missing_sources:
        raise ConformanceError(
            "conformance manifest: missing required sources "
            + ", ".join(sorted(missing_sources))
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
    golden_path: Path = DEFAULT_GOLDEN,
    manifest_path: Path = DEFAULT_MANIFEST,
    root: Path = ROOT,
) -> None:
    store = load_encoding_store(root / "isa" / "defs")
    validate_golden_document(_load_yaml(golden_path), store)
    validate_manifest_document(_load_yaml(manifest_path), root)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--golden", type=Path, default=DEFAULT_GOLDEN)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    args = parser.parse_args()
    try:
        validate_paths(args.golden, args.manifest)
    except (ConformanceError, ValueError) as exc:
        print(f"conformance validation failed: {exc}", file=sys.stderr)
        return 1
    print("conformance manifest and assembler golden vectors are valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
