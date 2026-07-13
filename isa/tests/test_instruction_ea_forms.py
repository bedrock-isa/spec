#!/usr/bin/env python3
"""Tests for lossless reader-facing per-instruction EA summaries."""

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
    ea_availability_summary,
    ea_constraints_for_field,
    ea_value_allowed,
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

    def test_reclaimed_register_forms_are_summarized_as_an_excluded_category(self) -> None:
        rendered = self.render_entry("ADD", "medium.add_x_ea_e_rn_d.2")

        self.assertIn(r"\manualinstructionformatheading", rendered)
        self.assertIn(r"\manualinstructionfieldsheading", rendered)
        self.assertIn(r"\manualeasummary{Memory; Immediate; EXT0}{Register}", rendered)
        self.assertNotIn(r"\begin{tabular", rendered)
        self.assertNotIn("001", rendered)

    def test_destination_summary_marks_immediate_category_unavailable(self) -> None:
        rendered = self.render_entry("BCHG", "long.bchg_rn_b_ea_e")
        self.assertIn(r"\manualeasummary{Register; Memory; EXT0}{Immediate}", rendered)

    def test_memory_only_summary_marks_register_and_immediate_categories_unavailable(self) -> None:
        rendered = self.render_entry("FETCHADD", "extralong.fetchadd_x_order_o_rn_s_ea_e")
        self.assertIn(r"\manualeasummary{Memory; EXT0}{Register, Immediate}", rendered)
        self.assertIn("relaxed, acquire, release, acqrel, seqcst", rendered)

    def test_two_ea_fields_get_separate_availability_summaries(self) -> None:
        rendered = self.render_entry("MOV", "long.mov_x_ea_s_ea_d")

        self.assertEqual(rendered.count("Effective Address field"), 2)
        self.assertEqual(rendered.count(r"\manualeasummary"), 2)
        self.assertEqual(rendered.count(r"\Needspace{1.15in}"), 2)
        self.assertNotIn(r"\begin{tabular", rendered)

    def test_all_249_summaries_reconstruct_the_original_allowed_sets(self) -> None:
        rows = compact_ea_display_rows(self.model.metadata["ea"])
        self.assertEqual(len(rows), 27)
        summary_count = 0
        for path in sorted((ROOT / "isa" / "alloc").glob("*.yaml")):
            data = load_yaml(path)
            for raw in data.get("entries", []) or []:
                entry = AllocationEntry(
                    path=path,
                    cls=str(data["class"]),
                    payload_bits=int(data["payload_bits"]),
                    entry_id=str(raw["id"]),
                    bits=compact_bits(str(raw["bits"])),
                    text=str(raw["text"]),
                    assigned=0,
                    skipped=0,
                    fields=raw.get("fields") or {},
                    constraints=raw.get("constraints") or [],
                )
                for symbol, spec in entry.fields.items():
                    if not isinstance(spec, dict) or spec.get("kind") != "ea7":
                        continue
                    summary_count += 1
                    constraints = ea_constraints_for_field(entry, symbol)
                    expected = frozenset(
                        row.syntax
                        for row in rows
                        if all(ea_value_allowed(value, constraints) for value in row.values)
                    )
                    summary = ea_availability_summary(self.model, entry, symbol)
                    with self.subTest(entry=entry.entry_id, field=symbol):
                        self.assertEqual(summary.allowed_syntax, expected)
                        self.assertEqual(summary.reconstructed_allowed_syntax(), expected)
        self.assertEqual(summary_count, 249)

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
