#!/usr/bin/env python3
"""Regression tests for the LA48 and LA57 page-walk reference."""

from __future__ import annotations

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]
TEMPLATE_ROOT = ROOT / "isa" / "tools" / "latex_builder" / "templates"
FRAGMENT_ROOT = TEMPLATE_ROOT / "fragments"


class PageWalkReferenceTests(unittest.TestCase):
    def test_memory_translation_includes_page_walk_reference(self) -> None:
        text = (TEMPLATE_ROOT / "memory_address_translation.tex").read_text(encoding="utf-8")
        self.assertIn(
            r"\input{isa/tools/latex_builder/templates/fragments/page_walk_reference.tex}",
            text,
        )

    def test_page_walk_reference_includes_both_modes_and_figures(self) -> None:
        text = (FRAGMENT_ROOT / "page_walk_reference.tex").read_text(encoding="utf-8")
        for heading, figure in (
            ("LA48 Four-Level Paging", "la48_page_walk_figure.tex"),
            ("LA57 Five-Level Paging", "la57_page_walk_figure.tex"),
        ):
            with self.subTest(mode=heading):
                self.assertIn(rf"\subsection{{{heading}}}", text)
                self.assertIn(
                    rf"\input{{isa/tools/latex_builder/templates/fragments/{figure}}}",
                    text,
                )
        self.assertIn("512 64-bit entries in a 4-KiB table page", text)
        self.assertIn(r"\mathit{leaf\_PFN} \ll 12", text)

    def test_page_walk_figures_preserve_address_fields_and_captions(self) -> None:
        expected = {
            "la48_page_walk_figure.tex": (
                "LA48 Four-Level Page Walk",
                ("bits 47..39", "bits 38..30", "bits 29..21", "bits 20..12"),
            ),
            "la57_page_walk_figure.tex": (
                "LA57 Five-Level Page Walk",
                ("bits 56..48", "bits 47..39", "bits 38..30", "bits 29..21", "bits 20..12"),
            ),
        }
        for filename, (caption, bit_ranges) in expected.items():
            text = (FRAGMENT_ROOT / filename).read_text(encoding="utf-8")
            with self.subTest(figure=filename):
                self.assertIn(rf"\manualfigurecaption{{{caption}}}", text)
                self.assertIn("canonical", text)
                self.assertIn(r"physical\\address", text)
                for bit_range in bit_ranges:
                    self.assertIn(bit_range, text)


if __name__ == "__main__":
    unittest.main()
