#!/usr/bin/env python3
"""Tests for Markdown heading normalization after Pandoc conversion."""

from __future__ import annotations

from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[2]
TOOL_DIR = ROOT / "isa" / "tools"
if str(TOOL_DIR) not in sys.path:
    sys.path.insert(0, str(TOOL_DIR))

from latex_to_markdown import normalize_part_heading_levels  # noqa: E402


class PartHeadingNormalizationTests(unittest.TestCase):
    def test_collapses_only_the_unused_chapter_level(self) -> None:
        source = "# Part\n\n### Chapter\n\n#### Subsection\n\n## Existing H2\n"
        expected = "# Part\n\n## Chapter\n\n### Subsection\n\n## Existing H2\n"
        self.assertEqual(normalize_part_heading_levels(source, has_parts=True), expected)

    def test_leaves_markdown_without_parts_unchanged(self) -> None:
        source = "### Chapter\n#### Subsection\n"
        self.assertEqual(normalize_part_heading_levels(source, has_parts=False), source)

    def test_does_not_rewrite_fenced_code(self) -> None:
        source = "### Chapter\n```text\n### code heading\n```\n~~~~\n#### more code\n~~~~\n"
        expected = "## Chapter\n```text\n### code heading\n```\n~~~~\n#### more code\n~~~~\n"
        self.assertEqual(normalize_part_heading_levels(source, has_parts=True), expected)


if __name__ == "__main__":
    unittest.main()
