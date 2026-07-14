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
    IsaModel,
    instruction_details_tex,
    latex_instruction_constant_ids,
    latex_instruction_entry,
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
    def test_directory_contract_has_exact_instruction_and_details_sets(self) -> None:
        instruction_paths = sorted((ROOT / "isa" / "defs").glob("**/instructions/*/instruction.yaml"))
        details_paths = sorted((ROOT / "isa" / "defs").glob("**/instructions/*/details.tex"))
        self.assertEqual(len(instruction_paths), 206)
        self.assertEqual(len(details_paths), 60)

    def test_legacy_operation_text_is_preserved_as_reader_facing_details(self) -> None:
        required_phrases = {
            "EXTRACT": ("unsigned seven-bit shift count", "greater than or equal to \\(2n\\) produces zero"),
            "POP": ("segment-image validation completes before commit", "old SS"),
            "POPP": ("reverse listed order", "reverse canonical epilogue order"),
            "PUSH": ("current SS:SP", "old SS image"),
            "PUSHP": ("listed order", "canonical prologue order"),
            "REPG": ("final priority", "EVENT\\_AUX", "bitwise inclusive-or"),
            "REPcc": ("first body iteration", "terminating condition-false iteration"),
            "RESTORE": ("GS0--GS5", "User-mode RESTORE", "component offsets"),
            "SAVE": ("GS0--GS5", "architecturally clean extension blocks", "state-block bitmap"),
            "SYSCALL": ("URPC, URSP, URCS, URDS, URSS, and URCTL", "creates no stack frame"),
            "SYSRET": ("restored as one commit", "URCTL.V is cleared"),
            "FCLASS": ("negative infinity", "quiet NaN"),
            "FPOPP": ("complete two-slot stack range", "reverse listed order"),
            "FPUSHP": ("complete two-slot stack range", "listed order"),
        }
        for mnemonic, phrases in required_phrases.items():
            paths = list((ROOT / "isa" / "defs").glob(f"**/instructions/{mnemonic}/details.tex"))
            self.assertEqual(len(paths), 1, mnemonic)
            text = paths[0].read_text(encoding="utf-8")
            for phrase in phrases:
                with self.subTest(mnemonic=mnemonic, phrase=phrase):
                    self.assertIn(phrase, text)

    def test_fcvt_form_specific_meanings_are_preserved(self) -> None:
        root = ROOT / "isa" / "defs" / "extensions" / "fpu" / "instructions"
        signed = (root / "FCVT" / "details.tex").read_text(encoding="utf-8")
        unsigned = (root / "FCVTU" / "details.tex").read_text(encoding="utf-8")
        for phrase in ("Fn to Fn", "Fn to Rn", "Rn to Fn", "signed integer"):
            self.assertIn(phrase, signed)
        for phrase in ("Fn to Fn", "Fn to Rn", "Rn to Fn", "unsigned integer", "full 64-bit source range"):
            self.assertIn(phrase, unsigned)

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

    def test_reads_sibling_details_body(self) -> None:
        path = ROOT / "isa" / "defs" / "base" / "instructions" / "RDPMC" / "instruction.yaml"
        text = instruction_details_tex(InstructionDef(path, "base", "RDPMC", {}))
        self.assertIn(r"\textbf{Performance-Counter IDs}", text)

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

    def test_inserts_details_after_status_and_before_forms(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "TESTDOC" / "instruction.yaml"
            path.parent.mkdir()
            path.with_name("details.tex").write_text(r"Body-only detailed semantics.", encoding="utf-8")
            inst = instruction(path)
            model = IsaModel(
                defs_root=ROOT / "isa" / "defs",
                alloc_root=ROOT / "isa" / "alloc",
                metadata={},
                instructions=[inst],
                allocation_classes=[],
                allocated_by_mnemonic={},
            )
            rendered = latex_instruction_entry(model, inst)
            description_at = rendered.index(r"\manualinstructionfield{Description}")
            syntax_at = rendered.index(r"\manualinstructionfield{Assembler Syntax}")
            attributes_at = rendered.index(r"\manualinstructionfield{Attributes}")
            status_at = rendered.index(r"\begin{manualstatusstrip}")
            details_at = rendered.index(r"\manualinstructiondescriptionheading{Detailed Semantics}")
            forms_at = rendered.index(r"\begin{manualinstructionforms}")
            self.assertLess(description_at, syntax_at)
            self.assertLess(syntax_at, attributes_at)
            self.assertLess(attributes_at, status_at)
            self.assertLess(status_at, details_at)
            self.assertLess(details_at, forms_at)
            self.assertNotIn(r"\manualinstructionfield{Summary}", rendered)
            self.assertNotIn(r"\manualinstructionfield{Operation}", rendered)


if __name__ == "__main__":
    unittest.main()
