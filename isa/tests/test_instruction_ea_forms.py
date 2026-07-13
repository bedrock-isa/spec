#!/usr/bin/env python3
"""Tests for reader-facing per-instruction EA form tables."""

from __future__ import annotations

from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[2]
TOOL_DIR = ROOT / "isa" / "tools"
if str(TOOL_DIR) not in sys.path:
    sys.path.insert(0, str(TOOL_DIR))

from gen_docs import (  # noqa: E402
    AllocationEntry,
    InstructionDef,
    IsaModel,
    compact_bits,
    compact_ea_display_rows,
    latex_allocated_instruction_form_block,
    load_yaml,
    operand_role,
)


class InstructionEaFormsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.model = IsaModel(
            defs_root=ROOT / "isa" / "defs",
            alloc_root=ROOT / "isa" / "alloc",
            metadata={
                "ea": load_yaml(ROOT / "isa" / "defs" / "ea.yaml"),
                "conditions": load_yaml(ROOT / "isa" / "defs" / "conditions.yaml"),
            },
            instructions=[],
            allocation_classes=[],
            allocated_by_mnemonic={},
        )

    def instruction(self, mnemonic: str) -> InstructionDef:
        path = ROOT / "isa" / "defs" / "base" / "instructions" / f"{mnemonic}.yaml"
        return InstructionDef(path, "base", mnemonic, load_yaml(path))

    def allocation(self, entry_id: str) -> AllocationEntry:
        cls = entry_id.split(".", 1)[0]
        path = ROOT / "isa" / "alloc" / f"{cls}.yaml"
        data = load_yaml(path)
        raw = next(item for item in data["entries"] if item["id"] == entry_id)
        return AllocationEntry(
            path=path,
            cls=cls,
            payload_bits=int(data["payload_bits"]),
            entry_id=entry_id,
            bits=compact_bits(str(raw["bits"])),
            text=str(raw["text"]),
            assigned=0,
            skipped=0,
            fields=raw.get("fields") or {},
            constraints=raw.get("constraints") or [],
        )

    def render_entry(self, mnemonic: str, entry_id: str) -> str:
        return latex_allocated_instruction_form_block(
            self.model,
            self.instruction(mnemonic),
            self.allocation(entry_id),
        )

    def test_internal_constraint_dump_is_not_rendered(self) -> None:
        cases = (
            ("ADD", "medium.add_x_ea_e_rn_d.2"),
            ("BCHG", "long.bchg_rn_b_ea_e"),
            ("FETCHADD", "extralong.fetchadd_x_order_o_rn_s_ea_e"),
        )
        for mnemonic, entry_id in cases:
            rendered = self.render_entry(mnemonic, entry_id)
            with self.subTest(entry=entry_id):
                self.assertNotIn("field=", rendered)
                self.assertNotIn("allow=", rendered)
                self.assertNotIn("reason=", rendered)
                self.assertNotIn("_reclaimed", rendered)

    def test_reclaimed_register_forms_remain_visible_with_dashes(self) -> None:
        rendered = self.render_entry("ADD", "medium.add_x_ea_e_rn_d.2")

        self.assertIn(r"\manualinstructionformatheading", rendered)
        self.assertIn(r"\manualinstructionfieldsheading", rendered)
        self.assertIn(r"\renewcommand{\arraystretch}{1.22}", rendered)
        self.assertEqual(
            rendered.count(
                r"\begin{tabularx}{\linewidth}{|>{\raggedright\arraybackslash}X|"
            ),
            2,
        )
        self.assertEqual(
            rendered.count(r"\multicolumn{1}{|c|}{\textbf{Addressing Mode}}"),
            2,
        )
        self.assertIn(
            r"\texttt{Rn(r)} & \textemdash{} & \textemdash{}\\",
            rendered,
        )
        self.assertIn(
            r"\texttt{SP} & \textemdash{} & \textemdash{}\\",
            rendered,
        )
        self.assertIn(
            r"\texttt{[Rn(r)]} & \texttt{001} & \texttt{rrrr}\\",
            rendered,
        )
        self.assertNotIn("Following payload", rendered)
        self.assertNotIn(" & yes & ", rendered)

    def test_destination_table_marks_immediate_forms_unavailable(self) -> None:
        rendered = self.render_entry("BCHG", "long.bchg_rn_b_ea_e")

        self.assertIn(
            r"\texttt{Rn(r)} & \texttt{000} & \texttt{rrrr}\\",
            rendered,
        )
        self.assertIn(
            r"\texttt{imm8s} & \textemdash{} & \textemdash{}\\",
            rendered,
        )

    def test_memory_only_table_marks_registers_and_immediates_unavailable(self) -> None:
        rendered = self.render_entry("FETCHADD", "extralong.fetchadd_x_order_o_rn_s_ea_e")

        for syntax in ("Rn(r)", "SP", "imm8s", "imm64"):
            self.assertIn(
                rf"\texttt{{{syntax}}} & \textemdash{{}} & \textemdash{{}}\\",
                rendered,
            )
        self.assertIn(
            r"\texttt{[Rn(r)]} & \texttt{001} & \texttt{rrrr}\\",
            rendered,
        )
        self.assertIn("relaxed, acquire, release, acqrel, seqcst", rendered)

    def test_two_ea_fields_get_separate_addressing_mode_tables(self) -> None:
        rendered = self.render_entry("MOV", "long.mov_x_ea_s_ea_d")

        self.assertEqual(rendered.count("Effective Address field"), 2)
        self.assertEqual(rendered.count(r"\textbf{Addressing Mode}"), 4)
        self.assertEqual(rendered.count(r"\Needspace{2.55in}"), 2)
        self.assertEqual(rendered.count(r"\renewcommand{\arraystretch}{1.22}"), 2)
        self.assertEqual(
            rendered.count(
                r"\begin{tabularx}{\linewidth}{|>{\raggedright\arraybackslash}X|"
            ),
            4,
        )
        self.assertEqual(
            rendered.count(r"\multicolumn{1}{|c|}{\textbf{Addressing Mode}}"),
            4,
        )
        immediate_rows = [
            line
            for line in rendered.splitlines()
            if line.startswith(r"\texttt{imm8s} &")
        ]
        self.assertEqual(
            immediate_rows,
            [
                r"\texttt{imm8s} & \texttt{110} & \texttt{1100}\\\hline",
                r"\texttt{imm8s} & \textemdash{} & \textemdash{}\\\hline",
            ],
        )

    def test_single_ea_field_lists_every_valid_compact_form_once(self) -> None:
        rendered = self.render_entry("ADD", "medium.add_x_ea_e_rn_d.2")
        rows = compact_ea_display_rows(self.model.metadata["ea"])

        self.assertEqual(len(rows), 27)
        for row in rows:
            with self.subTest(syntax=row.syntax):
                self.assertEqual(rendered.count(rf"\texttt{{{row.syntax}}} &"), 1)
        self.assertNotIn("1110101..1111111", rendered)

    def test_non_ea_constraints_are_rendered_as_reader_facing_values(self) -> None:
        condition = self.render_entry("SET", "short.setcc_rn_r")
        nonzero = self.render_entry("SUB", "short.sub_q_imm8_i_sp")

        self.assertIn("EQ, NE, ULT", condition)
        self.assertNotIn("condition_true_false_reclaimed", condition)
        self.assertIn("1-255", nonzero)
        self.assertNotIn("zero_immediate_reclaimed", nonzero)

    def test_form_without_declared_fields_omits_empty_fields_heading(self) -> None:
        rendered = self.render_entry("ADD", "extrashort.add_q_8_sp")

        self.assertIn(r"\manualinstructionformatheading", rendered)
        self.assertNotIn(r"\manualinstructionfieldsheading", rendered)

    def test_three_operand_forms_use_positional_roles(self) -> None:
        self.assertEqual(
            [operand_role(index, 3) for index in range(3)],
            ["operand 1", "operand 2", "operand 3"],
        )


if __name__ == "__main__":
    unittest.main()
