#!/usr/bin/env python3
"""Regression checks for the architectural extralong front-end partition."""

from __future__ import annotations

from pathlib import Path
import sys
import unittest


TOOLS_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(TOOLS_ROOT))

from encoding_architecture import ENCODING_CLASSES_BY_NAME  # noqa: E402
from encoding_store import load_encoding_store  # noqa: E402


DEFS_ROOT = TOOLS_ROOT.parent / "instructions" / "definitions"
EXTRALONG_SELECTOR = "11111100"
COMMON_BANK = "00"
FIRST_WINDOW_ALLOCATION_BITS = 10
PARTITION = {
    ("integer", 0): "00",
    ("integer", 1): "01",
    ("fpu", 1): "10",
    ("fpu", 2): "11",
}


class ExtralongPartitionTests(unittest.TestCase):
    def test_xxlong_is_six_byte_space_and_custom_prefix_is_extralong(self) -> None:
        xxlong = ENCODING_CLASSES_BY_NAME["xxlong"]
        extralong = ENCODING_CLASSES_BY_NAME["extralong"]
        self.assertEqual((xxlong.opcode_space_bytes, xxlong.allocation_bits), (6, 42))
        self.assertEqual(xxlong.selectors, ("11111111",))
        self.assertIn("11111110" + "?" * 26, extralong.namespace)
        forms = load_encoding_store(DEFS_ROOT).for_class("xxlong")
        self.assertEqual(len(forms), 102)
        self.assertTrue(all(form.form.bits.startswith("11111111") for form in forms))
        self.assertTrue(all(len(form.form.bits) == 42 for form in forms))

    def test_first_sixteen_bits_determine_family_and_ea_count(self) -> None:
        """The eight selector bits plus this ten-bit prefix are the D0 window."""
        store = load_encoding_store(DEFS_ROOT)
        contracts_by_prefix: dict[str, set[tuple[str, int]]] = {}

        for located in store.for_class("extralong"):
            family = (
                "fpu"
                if "/extensions/fpu/" in located.path.as_posix()
                else "integer"
            )
            ea_count = sum(
                operand.type in {"EA", "FEA", "VEA"}
                for operand in located.form.operands
            )
            contract = (family, ea_count)
            expected_prefix = (
                EXTRALONG_SELECTOR + PARTITION[contract]
            )
            actual_prefix = located.form.bits[:FIRST_WINDOW_ALLOCATION_BITS]

            self.assertEqual(actual_prefix, expected_prefix, located.form.id)
            contracts_by_prefix.setdefault(actual_prefix, set()).add(contract)

        self.assertTrue(contracts_by_prefix)
        self.assertTrue(
            all(len(contracts) == 1 for contracts in contracts_by_prefix.values())
        )
        self.assertEqual(
            {prefix[6:8] for prefix in contracts_by_prefix},
            {COMMON_BANK},
        )


if __name__ == "__main__":
    unittest.main()
