#!/usr/bin/env python3
"""Regression checks for ISA, ABI, and toolchain document ownership."""

from __future__ import annotations

from pathlib import Path
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[2]


class DocumentOwnershipTests(unittest.TestCase):
    def test_draft_sources_do_not_claim_a_release_version(self) -> None:
        public_documents = (
            ROOT / "isa" / "abi" / "bedrock-c-abi.tex",
            ROOT / "isa" / "abi" / "bedrock-elf-abi.tex",
            ROOT / "isa" / "c" / "bedrock-c-far-extensions.tex",
            ROOT / "isa" / "c" / "bedrock-target-intrinsics.tex",
            ROOT / "isa" / "guides" / "bedrock-programming-toolchain-guide.tex",
            ROOT
            / "isa"
            / "tools"
            / "latex_builder"
            / "templates"
            / "cpuid_feature_discovery.tex",
        )
        major = str(1)
        release_labels = (f"version {major}.0", f"revision {major}")
        for path in public_documents:
            text = path.read_text(encoding="utf-8").lower()
            for label in release_labels:
                self.assertNotIn(label, text, path)

        self.assertTrue((ROOT / "isa" / "memory_model" / "validation.yaml").exists())

    def test_gs_metadata_and_segment_instructions_are_abi_neutral(self) -> None:
        register_groups = yaml.safe_load(
            (ROOT / "isa" / "defs" / "registers.yaml").read_text(encoding="utf-8")
        )["registers"]
        segments = register_groups["segment"]["entries"]
        gs_registers = [entry for entry in segments if entry["name"].startswith("GS")]
        self.assertEqual(
            [entry["description"] for entry in gs_registers],
            [f"general segment register {index}" for index in range(6)],
        )

        for mnemonic in ("RDSEG", "WRSEG"):
            definition = yaml.safe_load(
                (
                    ROOT
                    / "isa"
                    / "defs"
                    / "instructions"
                    / mnemonic
                    / "instruction.yaml"
                ).read_text(encoding="utf-8")
            )
            description = definition["description"].lower()
            self.assertNotIn("tls", description)
            self.assertNotIn("far-pointer", description)
            self.assertNotIn("profile_access", definition["attributes"])

    def test_language_and_elf_address_meanings_stay_out_of_isa_terminology(self) -> None:
        terminology = (
            ROOT / "isa" / "tools" / "latex_builder" / "templates" / "terminology.tex"
        ).read_text(encoding="utf-8")
        for phrase in ("ABI-visible", "Ordinary pointers", "ELF symbol values"):
            self.assertNotIn(phrase, terminology)

        c_abi = (ROOT / "isa" / "abi" / "bedrock-c-abi.tex").read_text(encoding="utf-8")
        elf_abi = (ROOT / "isa" / "abi" / "bedrock-elf-abi.tex").read_text(
            encoding="utf-8"
        )
        self.assertIn("An ordinary object or function pointer is a 64-bit", c_abi)
        self.assertIn("address value used by ELF symbols", elf_abi)

    def test_isa_memory_model_contains_only_architectural_ordering(self) -> None:
        memory_model = (
            ROOT / "isa" / "tools" / "latex_builder" / "templates" / "memory_model.tex"
        ).read_text(encoding="utf-8")
        for phrase in (
            "C-language",
            "compiler mappings",
            "architecture freeze",
            "Memory-Model Validation Gate",
        ):
            self.assertNotIn(phrase, memory_model)
        self.assertIn(
            "contributes no write and therefore creates no release sequence",
            memory_model,
        )

        c_abi = (ROOT / "isa" / "abi" / "bedrock-c-abi.tex").read_text(encoding="utf-8")
        closure = (ROOT / "isa" / "memory_model" / "validation.yaml").read_text(
            encoding="utf-8"
        )
        self.assertIn("release sequence", c_abi)
        self.assertIn("failed-compare-exchange", closure)

    def test_compiler_policy_stays_out_of_architecture_text(self) -> None:
        templates = ROOT / "isa" / "tools" / "latex_builder" / "templates"
        cpuid = (templates / "cpuid_feature_discovery.tex").read_text(encoding="utf-8")
        fptransa = (
            ROOT
            / "isa"
            / "defs"
            / "extensions"
            / "fpu"
            / "extensions"
            / "transcendental_approx"
            / "introduction.tex"
        ).read_text(encoding="utf-8")
        self.assertNotIn("compiler intrinsic", cpuid.lower())
        for term in ("compiler mode", "intrinsic", "libm"):
            self.assertNotIn(term, fptransa.lower())

        intrinsics = (ROOT / "isa" / "c" / "bedrock-target-intrinsics.tex").read_text(
            encoding="utf-8"
        )
        self.assertIn("Approximate Transcendental Lowering Policy", intrinsics)

    def test_c_and_runtime_examples_are_a_separate_nonnormative_guide(self) -> None:
        templates = ROOT / "isa" / "tools" / "latex_builder" / "templates"
        document = (templates / "document.tex").read_text(encoding="utf-8")
        self.assertNotIn("C Library Instruction Examples", document)
        self.assertNotIn("c_library_instruction_examples.tex", document)
        self.assertNotIn("runtime_instruction_examples.tex", document)
        self.assertFalse((templates / "c_library_instruction_examples.tex").exists())
        self.assertFalse((templates / "runtime_instruction_examples.tex").exists())

        guide = (
            ROOT / "isa" / "guides" / "bedrock-programming-toolchain-guide.tex"
        ).read_text(encoding="utf-8")
        self.assertIn("This guide is non-normative", guide)
        self.assertIn(r"\input{isa/guides/c_library_instruction_examples.tex}", guide)
        self.assertIn(r"\input{isa/guides/runtime_instruction_examples.tex}", guide)


if __name__ == "__main__":
    unittest.main()
