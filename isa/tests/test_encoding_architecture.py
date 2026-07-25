#!/usr/bin/env python3
"""Regression tests for the fixed instruction encoding grammar."""

from __future__ import annotations

from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[2]
TOOL_DIR = ROOT / "isa" / "tools"
if str(TOOL_DIR) not in sys.path:
    sys.path.insert(0, str(TOOL_DIR))

from encoding_architecture import (  # noqa: E402
    ENCODING_CLASSES,
    extended_record_is_sufficient,
    extended_instruction_lengths,
    extended_length_byte0_pattern,
)
from gen_docs import encoding_architecture_template_values  # noqa: E402


class EncodingArchitectureTests(unittest.TestCase):
    def test_class_order_widths_and_selectors_are_architectural(self) -> None:
        self.assertEqual(
            [
                (
                    encoding_class.name,
                    encoding_class.instruction_bytes,
                    encoding_class.payload_bits,
                    encoding_class.selectors,
                )
                for encoding_class in ENCODING_CLASSES
            ],
            [
                ("extrashort", 1, 7, ()),
                ("short", 2, 14, ()),
                (
                    "medium",
                    3,
                    18,
                    ("0xxxxx", "10xxxx", "110xxx", "1110xx"),
                ),
                ("long", 4, 26, ("11110x", "111110")),
                ("extralong", 5, 34, ("111111",)),
            ],
        )

    def test_length_and_opcode_tables_are_derived_from_the_grammar(self) -> None:
        self.assertEqual(list(extended_instruction_lengths()), list(range(3, 19)))
        self.assertEqual(extended_length_byte0_pattern(3), "110000oo")
        self.assertEqual(extended_length_byte0_pattern(18), "111111oo")

        values = encoding_architecture_template_values()
        self.assertEqual(
            len(values["INSTRUCTION_LENGTH_TRUTH_TABLE_ROWS"].splitlines()),
            18,
        )
        self.assertEqual(
            len(values["ENCODING_CLASS_SUMMARY_ROWS"].splitlines()),
            5,
        )
        self.assertEqual(
            len(values["OPCODE_PAYLOAD_NAMESPACE_ROWS"].split(r"\manualbitrow")) - 1,
            9,
        )

    def test_extended_padding_values_do_not_change_length_validity(self) -> None:
        for required in extended_instruction_lengths():
            for encoded in extended_instruction_lengths():
                payloads = (
                    bytes(encoded),
                    bytes([0xFF]) * encoded,
                    bytes(0x00 if index % 2 == 0 else 0xA5 for index in range(encoded)),
                )
                for record in payloads:
                    self.assertEqual(
                        extended_record_is_sufficient(required, record),
                        encoded >= required,
                    )


if __name__ == "__main__":
    unittest.main()
