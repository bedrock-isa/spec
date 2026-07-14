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
    namespace_patterns,
)
from validate_isa import load_yaml  # noqa: E402


LONG_ALLOC = ROOT / "isa" / "alloc" / "long.yaml"
IMMEDIATE_EA_VALUES = set(range(0x6C, 0x70))


class ControlFlowEaReclaimTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data = load_yaml(LONG_ALLOC)
        cls.payload_bits = int(cls.data["payload_bits"])
        cls.namespaces = namespace_patterns(cls.payload_bits, cls.data)

    def entry(self, entry_id: str) -> dict[str, Any]:
        return next(item for item in self.data["entries"] if item["id"] == entry_id)

    def claims(self, entry_id: str) -> tuple[set[int], dict[str, int]]:
        claims, skipped = entry_claims(
            LONG_ALLOC,
            self.payload_bits,
            self.namespaces,
            self.entry(entry_id),
        )
        return {value for value, _claim in claims}, dict(skipped)

    def field_values(self, entry_id: str, field: str) -> set[int]:
        entry = self.entry(entry_id)
        pattern = compact_bits(str(entry["bits"]))
        claims, _skipped = self.claims(entry_id)
        return {field_value(value, pattern, field)[0] for value in claims}

    def claimed_targets(self, targets: set[int]) -> set[int]:
        result: set[int] = set()
        for entry in self.data["entries"]:
            pattern = compact_bits(str(entry["bits"]))
            if not any(matches_pattern(value, pattern) for value in targets):
                continue
            claims, _skipped = entry_claims(
                LONG_ALLOC,
                self.payload_bits,
                self.namespaces,
                entry,
            )
            result.update(value for value, _claim in claims if value in targets)
        return result

    def test_control_flow_family_uses_the_reserved_long_block(self) -> None:
        expected = {
            "long.jmp_x_ea_e": "1111001001z00000000eeeeeee",
            "long.jcc_x_ea_e": "1111001001z0000cccceeeeeee",
            "long.call_ea_e": "1111000011011100000eeeeeee",
            "long.callcc_ea_e": "111100001101110cccceeeeeee",
        }
        for entry_id, bits in expected.items():
            with self.subTest(entry=entry_id):
                self.assertEqual(compact_bits(str(self.entry(entry_id)["bits"])), bits)

    def test_immediate_ea_modes_are_reclaimed_from_every_form(self) -> None:
        for entry_id in (
            "long.jmp_x_ea_e",
            "long.jcc_x_ea_e",
            "long.call_ea_e",
            "long.callcc_ea_e",
        ):
            with self.subTest(entry=entry_id):
                self.assertTrue(self.field_values(entry_id, "e").isdisjoint(IMMEDIATE_EA_VALUES))

    def test_claim_and_reclaim_cardinalities(self) -> None:
        expected = {
            "long.jmp_x_ea_e": (248, {"canonical_form_reclaim": 8}),
            "long.jcc_x_ea_e": (
                3_472,
                {
                    "condition_true_false_reclaimed": 512,
                    "canonical_form_reclaim": 112,
                },
            ),
            "long.call_ea_e": (124, {"canonical_form_reclaim": 4}),
            "long.callcc_ea_e": (
                1_736,
                {
                    "condition_true_false_reclaimed": 256,
                    "canonical_form_reclaim": 56,
                },
            ),
        }
        for entry_id, (claim_count, skipped) in expected.items():
            with self.subTest(entry=entry_id):
                claims, actual_skipped = self.claims(entry_id)
                self.assertEqual(len(claims), claim_count)
                self.assertEqual(actual_skipped, skipped)

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

    def test_callcc_definition_declares_compact_and_ea_forms(self) -> None:
        definition = load_yaml(
            ROOT / "isa" / "defs" / "base" / "instructions" / "CALLcc" / "instruction.yaml"
        )
        forms = definition["forms"]

        self.assertEqual(forms["compact_forms"][0]["operands"][-1]["type"], "relative_imm")
        self.assertEqual(forms["extended_forms"][0]["operands"][-1]["type"], "EA")
        self.assertFalse(forms["extended_forms"][0]["compact"])
        self.assertEqual(forms["reads"], "FLAGS")


if __name__ == "__main__":
    unittest.main()
