#!/usr/bin/env python3
"""Regression tests for near CALL/JMP effective-address encodings."""

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
    expand_pattern,
    field_value,
    matches_pattern,
)
from encoding_store import allocation_entry_dict, load_encoding_store  # noqa: E402


DEFS_ROOT = ROOT / "isa" / "defs"
IMMEDIATE_EA_VALUES = set(range(0x6C, 0x70))


class ControlFlowEaReclaimTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        store = load_encoding_store(DEFS_ROOT)
        encoding_class = store.classes_by_name["long"]
        cls.payload_bits = encoding_class.payload_bits
        cls.namespaces = list(encoding_class.namespace)
        cls.entries = [allocation_entry_dict(item) for item in store.for_class("long")]

    def entry(self, entry_id: str) -> dict[str, Any]:
        return next(item for item in self.entries if item["id"] == entry_id)

    def claims(self, entry_id: str) -> tuple[set[int], dict[str, int]]:
        entry = self.entry(entry_id)
        claims, skipped = entry_claims(
            Path(str(entry["source_path"])),
            self.payload_bits,
            self.namespaces,
            entry,
        )
        return {value for value, _claim in claims}, dict(skipped)

    def field_values(self, entry_id: str, field: str) -> set[int]:
        entry = self.entry(entry_id)
        pattern = compact_bits(str(entry["bits"]))
        claims, _skipped = self.claims(entry_id)
        return {field_value(value, pattern, field)[0] for value in claims}

    def claimed_targets(self, targets: set[int]) -> set[int]:
        result: set[int] = set()
        for entry in self.entries:
            pattern = compact_bits(str(entry["bits"]))
            if not any(matches_pattern(value, pattern) for value in targets):
                continue
            claims, _skipped = entry_claims(
                Path(str(entry["source_path"])),
                self.payload_bits,
                self.namespaces,
                entry,
            )
            result.update(value for value, _claim in claims if value in targets)
        return result

    def test_immediate_ea_modes_are_reclaimed_from_every_form(self) -> None:
        for entry_id in (
            "long.jmp_x_ea_e",
            "long.jcc_x_ea_e",
            "long.call_ea_e",
            "long.callcc_ea_e",
        ):
            with self.subTest(entry=entry_id):
                self.assertTrue(self.field_values(entry_id, "e").isdisjoint(IMMEDIATE_EA_VALUES))

    def test_unconditional_forms_are_the_true_condition_rows(self) -> None:
        pairs = (
            ("long.jmp_x_ea_e", "long.jcc_x_ea_e"),
            ("long.call_ea_e", "long.callcc_ea_e"),
        )
        for unconditional_id, conditional_id in pairs:
            conditional_pattern = compact_bits(str(self.entry(conditional_id)["bits"]))
            unconditional_claims, _skipped = self.claims(unconditional_id)
            with self.subTest(entry=unconditional_id):
                self.assertTrue(
                    all(field_value(value, conditional_pattern, "c")[0] == 0 for value in unconditional_claims)
                )

        self.assertEqual(self.field_values("long.jcc_x_ea_e", "c"), set(range(0x2, 0x10)))
        self.assertEqual(self.field_values("long.callcc_ea_e", "c"), set(range(0x2, 0x10)))

    def test_false_condition_rows_remain_unassigned(self) -> None:
        for entry_id in ("long.jcc_x_ea_e", "long.callcc_ea_e"):
            pattern = compact_bits(str(self.entry(entry_id)["bits"])).replace("cccc", "0001")
            targets = set(expand_pattern(pattern))
            with self.subTest(entry=entry_id):
                self.assertEqual(self.claimed_targets(targets), set())

if __name__ == "__main__":
    unittest.main()
