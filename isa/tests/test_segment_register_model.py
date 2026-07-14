#!/usr/bin/env python3

from __future__ import annotations

from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[2]
SEGMENTS = ROOT / "isa" / "defs" / "segments.yaml"
TEMPLATES = ROOT / "isa" / "tools" / "latex_builder" / "templates"


def sreg_encodings() -> dict[str, int]:
    source = SEGMENTS.read_text(encoding="utf-8")
    result: dict[str, int] = {}
    for match in re.finditer(
        r"(?ms)^- name: ([A-Z][A-Z0-9]*)\n(?P<body>.*?)(?=^- name:|\Z)", source
    ):
        encoding = re.search(r"(?m)^\s+sreg_encoding:\s*(\d+)\s*$", match.group("body"))
        if encoding is not None:
            result[match.group(1)] = int(encoding.group(1))
    return result


class SegmentRegisterModelTests(unittest.TestCase):
    def test_sreg_namespace_excludes_cs_and_fills_all_three_bit_values(self) -> None:
        self.assertEqual(
            sreg_encodings(),
            {"DS": 0, "SS": 1, "GS0": 2, "GS1": 3, "GS2": 4, "GS3": 5, "GS4": 6, "GS5": 7},
        )

    def test_explicit_ea_documents_only_sreg_selectors(self) -> None:
        ea = (ROOT / "isa" / "defs" / "ea.yaml").read_text(encoding="utf-8")
        reference = (TEMPLATES / "fragments" / "ext0_reference_blocks.tex").read_text(encoding="utf-8")
        self.assertIn("explicit_segment_selector: SREG", ea)
        self.assertIn("DS, SS, or GS0..GS5", reference)
        self.assertNotIn("selects CS", reference)

    def test_sreg_reference_table_is_generated_from_metadata(self) -> None:
        register_model = (TEMPLATES / "register_model.tex").read_text(encoding="utf-8")
        generator = (ROOT / "isa" / "tools" / "gen_docs.py").read_text(encoding="utf-8")
        self.assertIn("@SREG_TABLE@", register_model)
        self.assertIn('"SREG_TABLE": latex_code_table(', generator)
        self.assertNotIn(r"\texttt{CS} & \texttt{000}", register_model)

    def test_cs_has_dedicated_read_form_without_entering_sreg_namespace(self) -> None:
        rdseg = (ROOT / "isa" / "defs" / "base" / "instructions" / "RDSEG" / "instruction.yaml").read_text(
            encoding="utf-8"
        )
        allocation = (ROOT / "isa" / "alloc" / "long.yaml").read_text(encoding="utf-8")
        register_model = (TEMPLATES / "register_model.tex").read_text(encoding="utf-8")
        self.assertIn("type: CS", rdseg)
        self.assertIn("source_only: true", rdseg)
        self.assertIn('bits: "1111101111010001111100dddd"', allocation)
        self.assertIn('text: "RDSEG CS, Rn(d)"', allocation)
        self.assertNotIn('text: "WRSEG Rn(d), CS"', allocation)
        self.assertIn(r"\texttt{RDSEG CS}", register_model)

    def test_save_restore_uses_six_gs_slots_without_growing_fixed_block(self) -> None:
        save = (ROOT / "isa" / "defs" / "base" / "instructions" / "SAVE" / "instruction.yaml").read_text(encoding="utf-8")
        restore = (ROOT / "isa" / "defs" / "base" / "instructions" / "RESTORE" / "instruction.yaml").read_text(encoding="utf-8")
        save_details = (ROOT / "isa" / "defs" / "base" / "instructions" / "SAVE" / "details.tex").read_text(encoding="utf-8")
        restore_details = (ROOT / "isa" / "defs" / "base" / "instructions" / "RESTORE" / "details.tex").read_text(encoding="utf-8")
        diagram = (TEMPLATES / "fragments" / "save_area_diagram.tex").read_text(encoding="utf-8")
        self.assertIn("GS0--GS5", save_details)
        self.assertIn("GS0--GS5", restore_details)
        self.assertNotIn("reg_v", save + restore + save_details + restore_details)
        self.assertIn(r"\manualformatfield{GSV}{6}", diagram)
        self.assertIn(r"\manualstructoptionalseries{GS}{0}{6}", diagram)
        self.assertIn(r"\manualstructtallrow{0x0c0+}", diagram)
        self.assertNotIn(r"reserved\\\texttt{0x0b8}", diagram)


if __name__ == "__main__":
    unittest.main()
