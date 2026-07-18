#!/usr/bin/env python3
"""Regression checks for manifest-generated ABI quick-reference tables."""

from __future__ import annotations

from pathlib import Path
import re
import sys
import unittest


ROOT = Path(__file__).resolve().parents[2]
TOOL_DIR = ROOT / "isa" / "tools"
if str(TOOL_DIR) not in sys.path:
    sys.path.insert(0, str(TOOL_DIR))

import gen_abi_tables  # noqa: E402


class AbiGeneratedTableTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.manifest = gen_abi_tables.load_manifest()

    def test_generated_fragments_are_current(self) -> None:
        self.assertEqual(gen_abi_tables.check_fragments(self.manifest), [])
        self.assertEqual(
            set(gen_abi_tables.render_fragments(self.manifest)),
            set(gen_abi_tables.FRAGMENT_NAMES),
        )

    def test_c_and_elf_documents_consume_all_generated_fragments(self) -> None:
        c_abi = (ROOT / "isa" / "abi" / "bedrock-c-abi.tex").read_text(encoding="utf-8")
        elf_abi = (ROOT / "isa" / "abi" / "bedrock-elf-abi.tex").read_text(encoding="utf-8")
        for name in gen_abi_tables.FRAGMENT_NAMES[:4]:
            self.assertIn(rf"\input{{isa/abi/generated/{name}}}", c_abi)
        for name in gen_abi_tables.FRAGMENT_NAMES[4:]:
            self.assertIn(rf"\input{{isa/abi/generated/{name}}}", elf_abi)

        self.assertNotIn(r"Direct C call & \texttt", c_abi)
        self.assertNotIn(r"Aligned 1/2/4/8-byte load or store &", c_abi)
        self.assertNotIn(r"\texttt{.got.far} &", elf_abi)
        self.assertNotIn(r"local-exec & \begin{tabular}", elf_abi)

    def test_manifest_relocations_exist_in_normative_elf_table(self) -> None:
        elf_abi = (ROOT / "isa" / "abi" / "bedrock-elf-abi.tex").read_text(encoding="utf-8")
        normalized = (
            elf_abi.replace(r"\_\allowbreak{}", "_")
            .replace(r"\_", "_")
            .replace(r"\allowbreak{}", "")
        )
        defined = {
            name
            for name in re.findall(
                r"(?m)^\d+\s*&\s*\\texttt\{(R_BEDROCK_[A-Z0-9_]+)\}",
                normalized,
            )
        }
        self.assertTrue(defined)
        gen_abi_tables.validate_relocation_relationships(self.manifest, defined)

    def test_manifest_keeps_semantic_structure(self) -> None:
        c_abi = self.manifest["c_abi"]
        elf_abi = self.manifest["elf_abi"]
        aligned = c_abi["ordinary_access_guarantees"][0]["access"]
        self.assertEqual(aligned["widths_bytes"], [1, 2, 4, 8])
        self.assertEqual(aligned["operations"], ["load", "store"])
        self.assertEqual(
            elf_abi["bedrock_specific_sections"][0]["attributes"],
            ["alloc", "read", "write"],
        )
        self.assertEqual(
            elf_abi["tls_relocation_families"][0]["model"],
            "local_exec",
        )


if __name__ == "__main__":
    unittest.main()
