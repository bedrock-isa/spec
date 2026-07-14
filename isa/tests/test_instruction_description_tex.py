#!/usr/bin/env python3
"""Tests for sibling instruction Detailed Semantics TeX bodies."""

from __future__ import annotations

from pathlib import Path
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[2]
TOOL_DIR = ROOT / "isa" / "tools"
if str(TOOL_DIR) not in sys.path:
    sys.path.insert(0, str(TOOL_DIR))

from gen_docs import (  # noqa: E402
    InstructionDef,
    instruction_details_tex,
    latex_instruction_constant_ids,
)


def instruction(path: Path) -> InstructionDef:
    return InstructionDef(
        path=path,
        instruction_set="base",
        mnemonic="TESTDOC",
        data={
            "doc": {
                "title": "Details Body Test",
                "summary": "Tests detailed semantics placement.",
                "description": "Defines the normative behavior used by this synthetic instruction entry.",
                "instruction_family": "test",
                "instruction_class": "test",
            },
            "behavior": {},
            "attributes": {
                "privilege": "unprivileged",
                "flags": {"Z": "result is zero"},
            },
            "forms": {"operands": []},
        },
    )


class InstructionDetailsTexTests(unittest.TestCase):
    def test_renders_constant_ids_from_instruction_forms(self) -> None:
        inst = instruction(Path("isa/defs/base/instructions/TESTDOC/instruction.yaml"))
        inst.data["forms"]["result_format"] = "IEEE-754 binary64"
        inst.data["forms"]["constant_ids"] = [
            {"id": "0x0010", "name": "pi", "value_bits": "0x400921fb54442d18"},
            {"id": "0x0100", "name": "positive_infinity", "value_bits": "0x7ff0000000000000"},
        ]
        rendered = latex_instruction_constant_ids(inst)
        self.assertIn("TESTDOC Constant IDs (IEEE-754 binary64)", rendered)
        self.assertIn(r"\texttt{0x0010}", rendered)
        self.assertIn("positive infinity", rendered)
        self.assertIn(r"\texttt{0x7ff0000000000000}", rendered)

    def test_rejects_duplicate_constant_ids(self) -> None:
        inst = instruction(Path("isa/defs/base/instructions/TESTDOC/instruction.yaml"))
        inst.data["forms"]["constant_ids"] = [
            {"id": "0x0000", "name": "zero", "value_bits": "0x0"},
            {"id": "0x0000", "name": "other_zero", "value_bits": "0x0"},
        ]
        with self.assertRaisesRegex(ValueError, "duplicate constant ID"):
            latex_instruction_constant_ids(inst)

    def test_instruction_without_sibling_body_has_no_details_output(self) -> None:
        inst = instruction(Path("isa/defs/base/instructions/TESTDOC/instruction.yaml"))
        self.assertEqual(instruction_details_tex(inst), "")

    def test_rejects_forbidden_document_structure(self) -> None:
        for body in (
            r"\section{Numbered}",
            r"\addcontentsline{toc}{section}{Listed}",
            r"\input{other.tex}",
            r"\include{other.tex}",
            r"\documentclass{article}",
            r"\begin{document}text\end{document}",
        ):
            with self.subTest(body=body), tempfile.TemporaryDirectory() as directory:
                path = Path(directory) / "TESTDOC" / "instruction.yaml"
                path.parent.mkdir()
                path.with_name("details.tex").write_text(body, encoding="utf-8")
                with self.assertRaisesRegex(ValueError, "forbidden document-structure"):
                    instruction_details_tex(instruction(path))

    def test_rejects_empty_details_body(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "TESTDOC" / "instruction.yaml"
            path.parent.mkdir()
            path.with_name("details.tex").write_text("\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "must not be empty"):
                instruction_details_tex(instruction(path))

if __name__ == "__main__":
    unittest.main()
