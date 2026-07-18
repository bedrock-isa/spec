#!/usr/bin/env python3
"""Regression checks for manifest-generated target-intrinsic tables."""

from __future__ import annotations

from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[2]
TOOL_DIR = ROOT / "isa" / "tools"
if str(TOOL_DIR) not in sys.path:
    sys.path.insert(0, str(TOOL_DIR))

import gen_target_intrinsics  # noqa: E402


class TargetIntrinsicGeneratedTableTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.manifest = gen_target_intrinsics.load_manifest()

    def test_generated_fragments_are_current(self) -> None:
        rendered = gen_target_intrinsics.render_tables(self.manifest)
        self.assertEqual(len(rendered), 11)
        gen_target_intrinsics.check_tables(
            rendered,
            gen_target_intrinsics.DEFAULT_OUTPUT_DIR,
        )

    def test_document_consumes_all_generated_fragments(self) -> None:
        document = (ROOT / "isa" / "c" / "bedrock-target-intrinsics.tex").read_text(
            encoding="utf-8"
        )
        for name in gen_target_intrinsics.render_tables(self.manifest):
            self.assertIn(
                rf"\input{{isa/c/generated/target_intrinsics/{name}}}",
                document,
            )
        self.assertNotIn(r"\compilerbuiltin{", document)
        self.assertNotIn(r"\manualtablecaption{Target Intrinsic", document)

    def test_manifest_matches_family_headers_and_umbrellas(self) -> None:
        gen_target_intrinsics.validate_manifest_against_headers(self.manifest)

    def test_manifest_keeps_semantic_structure(self) -> None:
        self.assertEqual(self.manifest["interface_count"], 50)
        self.assertEqual(len(self.manifest["header_families"]), 9)
        self.assertEqual(len(self.manifest["builtin_families"]), 9)
        self.assertEqual(len(self.manifest["shared_types"]), 4)
        cpuid = self.manifest["builtin_families"][1]["builtins"][0]
        self.assertEqual(cpuid["name"], "cpuid")
        self.assertEqual(cpuid["lowering"], {"kind": "instruction", "value": "CPUID"})
        self.assertEqual(
            self.manifest["header_families"][0]["header"],
            "bedrockfarintrin.h",
        )


if __name__ == "__main__":
    unittest.main()
