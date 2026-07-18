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
    AllocationEntry,
    InstructionDef,
    IsaModel,
    instruction_details_tex,
    latex_instruction_flag_effects,
    latex_instruction_operand_value_tables,
    load_instructions,
)


def instruction(
    path: Path,
    *,
    details: bool = False,
    flag_effects: dict[str, dict[str, str]] | None = None,
) -> InstructionDef:
    return InstructionDef(
        path=path,
        instruction_set="base",
        mnemonic="TESTDOC",
        data={
            "mnemonic": "TESTDOC",
            "title": "Details Body Test",
            "summary": "Tests detailed semantics placement.",
            "description": "Defines the normative behavior used by this synthetic instruction entry.",
            "attributes": {
                "class": "test",
                "family": "test",
                "privilege": "unprivileged",
            },
            **({"flag_effects": flag_effects} if flag_effects else {}),
            **({"additional_description": "details.tex"} if details else {}),
        },
    )


def model(constants: list[dict[str, str]]) -> IsaModel:
    entry = AllocationEntry(
        path=Path("isa/defs/instructions/TESTDOC/encodings.yaml"),
        cls="medium",
        payload_bits=18,
        entry_id="medium.testdoc",
        bits="0" * 18,
        text="TESTDOC fconst_id(i)",
        assigned=1,
        skipped=0,
        fields={"i": {"kind": "immediate", "width": 16}},
        constraints=[],
        operands=({"name": "constant_id", "type": "fconst_id", "access": "read", "field": "i"},),
        instruction_bytes=3,
    )
    return IsaModel(
        defs_root=ROOT / "isa" / "defs",
        metadata={
            "operand_types": {
                "fconst_id": {
                    "kind": "enum",
                    "field_width": 16,
                    "result_bits_format": "IEEE-754 binary64",
                    "values": constants,
                }
            }
        },
        instructions=[],
        allocation_classes=[],
        allocated_by_mnemonic={"TESTDOC": [entry]},
    )


class InstructionDetailsTexTests(unittest.TestCase):
    def test_flag_effect_metadata_uses_table_and_inline_thresholds(self) -> None:
        inline = instruction(
            Path("instruction.yaml"),
            flag_effects={"FFLAGS": {"NV": "may accrue", "NX": "may accrue"}},
        )
        inline_tex = latex_instruction_flag_effects(inline)
        self.assertIn(r"\manualinstructionfield{FFLAGS}", inline_tex)
        self.assertNotIn("manualflageffects", inline_tex)

        table = instruction(
            Path("instruction.yaml"),
            flag_effects={
                "FLAGS": {"Z": "result == 0", "N": "result sign", "C": "carry"}
            },
        )
        table_tex = latex_instruction_flag_effects(table)
        self.assertIn(r"\begin{manualflageffects}{FLAGS}", table_tex)
        self.assertIn(r"\manualflageffect{Z}{result == 0}", table_tex)

    def test_repository_flag_effect_split_and_ownership(self) -> None:
        banks = [
            effects
            for inst in load_instructions(ROOT / "isa" / "defs")
            for effects in inst.flag_effects.values()
        ]
        self.assertEqual(len(banks), 71)
        self.assertEqual(sum(len(effects) >= 3 for effects in banks), 36)
        self.assertEqual(sum(len(effects) <= 2 for effects in banks), 35)
        for path in (ROOT / "isa" / "defs").glob("**/instructions/*/details.tex"):
            self.assertNotIn("manualflageffects", path.read_text(encoding="utf-8"))

    def test_renders_rich_enum_values_from_encoding_operands(self) -> None:
        inst = instruction(Path("isa/defs/instructions/TESTDOC/instruction.yaml"))
        constants = [
            {"value": "0x0010", "name": "pi", "value_bits": "0x400921fb54442d18"},
            {"value": "0x0100", "name": "positive_infinity", "value_bits": "0x7ff0000000000000"},
        ]
        rendered = latex_instruction_operand_value_tables(model(constants), inst)
        self.assertIn("TESTDOC Constant IDs (IEEE-754 binary64)", rendered)
        self.assertIn(r"\texttt{0x0010}", rendered)
        self.assertIn("positive infinity", rendered)
        self.assertIn(r"\texttt{0x7ff0000000000000}", rendered)

    def test_rejects_duplicate_constant_ids(self) -> None:
        inst = instruction(Path("isa/defs/instructions/TESTDOC/instruction.yaml"))
        constants = [
            {"value": "0x0000", "name": "zero", "value_bits": "0x0"},
            {"value": "0x0000", "name": "other_zero", "value_bits": "0x0"},
        ]
        with self.assertRaisesRegex(ValueError, "duplicate fconst_id value"):
            latex_instruction_operand_value_tables(model(constants), inst)

    def test_instruction_without_sibling_body_has_no_details_output(self) -> None:
        inst = instruction(Path("isa/defs/instructions/TESTDOC/instruction.yaml"))
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
                    instruction_details_tex(instruction(path, details=True))

    def test_rejects_empty_details_body(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "TESTDOC" / "instruction.yaml"
            path.parent.mkdir()
            path.with_name("details.tex").write_text("\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "must not be empty"):
                instruction_details_tex(instruction(path, details=True))

if __name__ == "__main__":
    unittest.main()
