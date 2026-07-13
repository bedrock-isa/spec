#!/usr/bin/env python3

from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
TEMPLATES = ROOT / "isa" / "tools" / "latex_builder" / "templates"


class ExtendedEaDiagramTests(unittest.TestCase):
    def test_two_byte_descriptor_diagram_has_explicit_byte_boundary(self) -> None:
        source = (TEMPLATES / "fragments" / "ea_field_diagrams.tex").read_text()
        section = source.split(r"\begin{manuallistedbitdiagram}{EXT0 Two-Byte", 1)[1]
        section = section.split(r"\end{manuallistedbitdiagram}", 1)[0]

        self.assertEqual(section.count(r"\manualbytepairlabels"), 2)
        self.assertEqual(section.count(r"\manualbitgap{1}"), 2)
        self.assertNotIn(r"\manualbitrow{SEG + base + index}", section)
        self.assertNotIn(r"\manualbitrow{SP/PC + index}", section)

    def test_descriptor_prose_distinguishes_stream_order_from_endianness(self) -> None:
        source = (TEMPLATES / "effective_address_modes.tex").read_text()

        self.assertIn("Multi-byte scalar EA payloads", source)
        self.assertIn("EXT0 descriptor is not a multi-byte scalar", source)
        self.assertIn("byte 0 followed by byte 1", source)

    def test_two_byte_reference_forms_name_each_byte(self) -> None:
        source = (TEMPLATES / "fragments" / "ext0_reference_blocks.tex").read_text()

        self.assertEqual(source.count(r"\textbf{Descriptor} & Byte 0"), 4)
        self.assertGreaterEqual(source.count("Byte 1 is"), 4)
        self.assertNotIn("1sss0010 bbbbiiii", source)
        self.assertNotIn("1sss1000 bbbb0000", source)


if __name__ == "__main__":
    unittest.main()
