#!/usr/bin/env python3
"""Regression checks for the architectural extralong front-end partition."""

from __future__ import annotations

from pathlib import Path
import sys
import unittest


TOOLS_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(TOOLS_ROOT))

from decode_ir import instruction_set_name  # noqa: E402
from encoding_architecture import (  # noqa: E402
    ENCODING_CLASSES_BY_NAME,
    OPERATOR_SPACE_PREFIX_BITS,
    operator_space_from_prefix,
)
from encoding_store import load_encoding_store  # noqa: E402


DEFS_ROOT = TOOLS_ROOT.parent / "instructions" / "definitions"
class ExtralongPartitionTests(unittest.TestCase):
    def test_extralong_and_xxlong_class_grammar(self) -> None:
        xxlong = ENCODING_CLASSES_BY_NAME["xxlong"]
        extralong = ENCODING_CLASSES_BY_NAME["extralong"]
        self.assertEqual((xxlong.opcode_space_bytes, xxlong.allocation_bits), (6, 42))
        self.assertEqual(xxlong.selectors, ("11111111",))
        self.assertIn("11111110" + "?" * 26, extralong.namespace)

    def test_allocated_prefixes_determine_operator_space(self) -> None:
        """The D0 prefix identifies the instruction set before form decode."""
        store = load_encoding_store(DEFS_ROOT)
        for encoding_class in ("extralong", "xxlong"):
            for located in store.for_class(encoding_class):
                prefix = located.form.bits[:OPERATOR_SPACE_PREFIX_BITS]
                self.assertEqual(
                    operator_space_from_prefix(encoding_class, prefix),
                    instruction_set_name(DEFS_ROOT, located.path),
                    located.form.id,
                )

    def test_operator_space_resolution_is_scoped_by_encoding_class(self) -> None:
        with self.assertRaises(ValueError):
            operator_space_from_prefix("extralong", "1111111100")
        with self.assertRaises(ValueError):
            operator_space_from_prefix("xxlong", "1111110000")

        self.assertIsNone(operator_space_from_prefix("extralong", "11111110??"))
        self.assertIsNone(operator_space_from_prefix("xxlong", "1111111101"))


if __name__ == "__main__":
    unittest.main()
