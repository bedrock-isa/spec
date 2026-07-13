#!/usr/bin/env python3
"""Regression tests for reclaiming immediate EA encodings from destinations."""

from __future__ import annotations

from pathlib import Path
import sys
import unittest
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
TOOL_DIR = ROOT / "isa" / "tools"
if str(TOOL_DIR) not in sys.path:
    sys.path.insert(0, str(TOOL_DIR))

from validate_alloc import (  # noqa: E402
    compact_bits,
    entry_claims,
    field_value,
    namespace_patterns,
    validate_file,
)
from validate_isa import (  # noqa: E402
    allocation_mnemonic,
    destination_ea_reclaim_status,
    load_yaml,
)


MEDIUM_ALLOC = ROOT / "isa" / "alloc" / "medium.yaml"
IMMEDIATE_EA_VALUES = range(0x6C, 0x70)


def as_names(value: Any) -> set[str]:
    if value is None or value == "none":
        return set()
    if isinstance(value, list):
        return {str(item) for item in value}
    return {str(value)}


def contains_writable_ea(value: Any, written_names: set[str]) -> bool:
    if isinstance(value, dict):
        if value.get("type") == "EA" and str(value.get("name")) in written_names:
            return True
        return any(contains_writable_ea(item, written_names) for item in value.values())
    if isinstance(value, list):
        return any(contains_writable_ea(item, written_names) for item in value)
    return False


def writable_ea_mnemonics() -> set[str]:
    result: set[str] = set()
    for path in sorted((ROOT / "isa" / "defs").glob("**/instructions/*.yaml")):
        if path.name == "_common.yaml":
            continue
        data = load_yaml(path)
        if not isinstance(data, dict) or "mnemonic" not in data:
            continue
        behavior = data.get("behavior") or {}
        written_names = as_names(behavior.get("output")) | as_names(behavior.get("input_output"))
        if contains_writable_ea(data.get("forms") or {}, written_names):
            result.add(str(data["mnemonic"]))
    return result


def form_operands(text: str) -> list[str]:
    parts = text.split(maxsplit=1)
    if len(parts) < 2:
        return []
    return [operand.strip() for operand in parts[1].split(",")]


def medium_destination_ea_entries() -> list[dict[str, Any]]:
    data = load_yaml(MEDIUM_ALLOC)
    writable = writable_ea_mnemonics()
    result: list[dict[str, Any]] = []
    for entry in data.get("entries") or []:
        mnemonic = allocation_mnemonic(str(entry.get("text", "")))
        if mnemonic not in writable:
            continue
        ea_fields = [
            name
            for name, spec in (entry.get("fields") or {}).items()
            if isinstance(spec, dict) and spec.get("kind") == "ea7"
        ]
        if not ea_fields:
            continue
        operands = form_operands(str(entry["text"]))
        if mnemonic == "XCHG" or (operands and "<ea>" in operands[-1]):
            result.append(entry)
    return result


def has_immediate_destination_reclaim(entry: dict[str, Any]) -> bool:
    return any(
        constraint.get("destination")
        and constraint.get("exclude") == "immediate"
        and constraint.get("reason") == "invalid_destination"
        for constraint in entry.get("constraints") or []
    )


def immediate_claim_count(entry_id: str) -> int:
    path = MEDIUM_ALLOC
    data = load_yaml(path)
    entry = next(item for item in data["entries"] if item["id"] == entry_id)
    pattern = compact_bits(str(entry["bits"]))
    ea_fields = [
        name
        for name, spec in (entry.get("fields") or {}).items()
        if isinstance(spec, dict) and spec.get("kind") == "ea7"
    ]
    if len(ea_fields) != 1:
        raise AssertionError(f"{entry_id}: expected one EA field, got {ea_fields}")
    claims, _ = entry_claims(
        path,
        int(data["payload_bits"]),
        namespace_patterns(int(data["payload_bits"]), data),
        entry,
    )
    result = 0
    for value, _claim in claims:
        ea_value, width = field_value(value, pattern, ea_fields[0])
        if width != 7:
            raise AssertionError(f"{entry_id}: expected a 7-bit EA field, got {width}")
        if ea_value in IMMEDIATE_EA_VALUES:
            result += 1
    return result


class DestinationEaReclaimTests(unittest.TestCase):
    def test_cross_layer_validator_covers_all_allocated_destinations(self) -> None:
        checked, missing = destination_ea_reclaim_status(
            ROOT / "isa" / "defs",
            ROOT / "isa" / "alloc",
        )

        self.assertEqual(checked, 104)
        self.assertEqual(missing, [])

    def test_every_medium_writable_ea_form_reclaims_immediates(self) -> None:
        entries = medium_destination_ea_entries()

        self.assertEqual(len(entries), 53)
        self.assertTrue(all(has_immediate_destination_reclaim(entry) for entry in entries))

    def test_medium_reclaim_slot_total(self) -> None:
        _cls, summary, skipped, overlaps = validate_file(MEDIUM_ALLOC)

        self.assertEqual(overlaps, [])
        self.assertEqual(skipped["invalid_destination"], 4_204)
        self.assertEqual(summary["allocated"], 233_653)
        self.assertEqual(summary["reserved_total"], 12_107)

    def test_read_only_and_source_eas_keep_immediate_forms(self) -> None:
        self.assertEqual(immediate_claim_count("medium.add_x_ea_e_rn_d"), 128)
        self.assertEqual(immediate_claim_count("medium.test_x_rn_s_ea_e"), 128)

    def test_both_xchg_operands_reclaim_immediate_forms(self) -> None:
        self.assertEqual(immediate_claim_count("medium.xchg_x_rn_s_ea_e"), 0)
        self.assertEqual(immediate_claim_count("medium.xchg_x_ea_e_rn_d"), 0)


if __name__ == "__main__":
    unittest.main()
