#!/usr/bin/env python3
"""Tests for full-width instruction description TeX fragments."""

from __future__ import annotations

from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[2]
TOOL_DIR = ROOT / "isa" / "tools"
if str(TOOL_DIR) not in sys.path:
    sys.path.insert(0, str(TOOL_DIR))

from gen_docs import (  # noqa: E402
    InstructionDef,
    IsaModel,
    instruction_description_tex,
    latex_instruction_entry,
)


def instruction(description_tex: object) -> InstructionDef:
    return InstructionDef(
        path=Path("isa/defs/base/instructions/TESTDOC.yaml"),
        instruction_set="base",
        mnemonic="TESTDOC",
        data={
            "doc": {
                "title": "Description Fragment Test",
                "summary": "Tests description fragment placement.",
                "description_tex": description_tex,
                "instruction_family": "test",
                "instruction_class": "test",
            },
            "attributes": {
                "privilege": "unprivileged",
                "flags": {"Z": "result is zero"},
            },
            "forms": {"operands": []},
        },
    )


class InstructionDescriptionTexTests(unittest.TestCase):
    def test_instruction_without_fragment_has_no_description_tex_output(self) -> None:
        inst = instruction("instruction_description_intro.tex")
        del inst.data["doc"]["description_tex"]
        self.assertEqual(instruction_description_tex(inst), "")

    def test_reads_safe_relative_tex_fragment(self) -> None:
        text = instruction_description_tex(instruction("instruction_description_intro.tex"))
        self.assertIn("Reading an Instruction Description", text)

    def test_rejects_unsafe_or_invalid_paths(self) -> None:
        for value in (
            "../outside.tex",
            "/absolute/path.tex",
            "instruction_description_intro.md",
            "missing-fragment.tex",
            "",
            1,
        ):
            with self.subTest(value=value), self.assertRaises(ValueError):
                instruction_description_tex(instruction(value))

    def test_inserts_fragment_after_status_and_before_forms(self) -> None:
        inst = instruction("instruction_description_intro.tex")
        model = IsaModel(
            defs_root=ROOT / "isa" / "defs",
            alloc_root=ROOT / "isa" / "alloc",
            metadata={},
            instructions=[inst],
            allocation_classes=[],
            allocated_by_mnemonic={},
        )
        rendered = latex_instruction_entry(model, inst)
        status_at = rendered.index(r"\manualinstructionstatus{Condition Codes}")
        fragment_at = rendered.index(r"\subsection{Reading an Instruction Description}")
        forms_at = rendered.index(r"\begin{manualinstructionforms}")
        self.assertLess(status_at, fragment_at)
        self.assertLess(fragment_at, forms_at)


if __name__ == "__main__":
    unittest.main()
