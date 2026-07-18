#!/usr/bin/env python3
"""Tests for reader-facing per-instruction EA summaries."""

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
)
from encoding_store import allocation_entry_dict, load_encoding_store  # noqa: E402


class InstructionEaFormsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.store = load_encoding_store(ROOT / "isa" / "defs")
        cls.model = IsaModel(
            defs_root=ROOT / "isa" / "defs",
            metadata={
                "ea": load_yaml(ROOT / "isa" / "defs" / "ea.yaml"),
                "conditions": load_yaml(ROOT / "isa" / "defs" / "conditions.yaml"),
            },
            instructions=[],
            allocation_classes=[],
            allocated_by_mnemonic={},
        )

    def instruction(self, mnemonic: str) -> InstructionDef:
        path = ROOT / "isa" / "defs" / "instructions" / mnemonic / "instruction.yaml"
        return InstructionDef(path, "base", mnemonic, load_yaml(path))

    def allocation(self, entry_id: str) -> AllocationEntry:
        located = next(item for item in self.store.encodings if item.form.id == entry_id)
        encoding_class = self.store.classes_by_name[located.form.encoding_class]
        raw = allocation_entry_dict(located)
        return AllocationEntry(
            path=located.path,
            cls=encoding_class.name,
            payload_bits=encoding_class.payload_bits,
            entry_id=entry_id,
            bits=compact_bits(str(raw["bits"])),
            text=str(raw["text"]),
            assigned=0,
            skipped=0,
            fields=raw.get("fields") or {},
            constraints=raw.get("constraints") or [],
            operands=tuple(
                {
                    "name": operand.name,
                    "type": operand.type,
                    "access": operand.access,
                    **({"field": operand.field} if operand.field else {}),
                }
                for operand in located.form.operands
            ),
            instruction_bytes=encoding_class.instruction_bytes,
        )

    def render_entry(self, mnemonic: str, entry_id: str) -> str:
        return latex_allocated_instruction_form_block(
            self.model,
            self.instruction(mnemonic),
            self.allocation(entry_id),
        )

    def test_two_ea_fields_get_separate_availability_summaries(self) -> None:
        rendered = self.render_entry("MOV", "long.mov_x_ea_s_ea_d")

        self.assertEqual(rendered.count("Effective Address field"), 2)
        self.assertEqual(rendered.count(r"\manualeasummary"), 2)

    def test_all_summaries_reconstruct_their_allowed_sets(self) -> None:
        rows = compact_ea_display_rows(self.model.metadata["ea"])
        for located in self.store.encodings:
            encoding_class = self.store.classes_by_name[located.form.encoding_class]
            raw = allocation_entry_dict(located)
            entry = AllocationEntry(
                path=located.path,
                cls=encoding_class.name,
                payload_bits=encoding_class.payload_bits,
                entry_id=str(raw["id"]),
                bits=compact_bits(str(raw["bits"])),
                text=str(raw["text"]),
                assigned=0,
                skipped=0,
                fields=raw.get("fields") or {},
                    constraints=raw.get("constraints") or [],
                    instruction_bytes=encoding_class.instruction_bytes,
                )
            for symbol, spec in entry.fields.items():
                if not isinstance(spec, dict) or spec.get("kind") != "ea7":
                    continue
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

if __name__ == "__main__":
    unittest.main()
