#!/usr/bin/env python3
"""Tests for byte-packed instruction encoding diagrams."""

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
    allocation_opcode_bytes,
    entry_byte_segments,
    instruction_length,
    load_yaml,
    required_bytes_text,
)
from encoding_store import allocation_entry_dict, load_encoding_store  # noqa: E402
from encoding_architecture import ENCODING_CLASSES, ENCODING_CLASSES_BY_NAME  # noqa: E402


def allocation(
    cls: str,
    payload_bits: int,
    *,
    bits: str | None = None,
    fields: dict[str, object] | None = None,
) -> AllocationEntry:
    instruction_bytes = ENCODING_CLASSES_BY_NAME[cls].instruction_bytes
    return AllocationEntry(
        path=Path(f"isa/alloc/{cls}.yaml"),
        cls=cls,
        payload_bits=payload_bits,
        entry_id=f"{cls}.test",
        bits=bits or "0" * payload_bits,
        text="TEST",
        assigned=0,
        skipped=0,
        fields=fields or {},
        constraints=[],
        instruction_bytes=instruction_bytes,
    )


class InstructionBitDiagramTests(unittest.TestCase):
    def test_every_rendered_byte_has_exactly_eight_bits(self) -> None:
        for encoding_class in ENCODING_CLASSES:
            with self.subTest(cls=encoding_class.name):
                for byte in entry_byte_segments(
                    allocation(encoding_class.name, encoding_class.payload_bits)
                ):
                    self.assertEqual(sum(width for _label, width in byte), 8)

    def test_required_bytes_use_ea_metadata_instead_of_global_maximum(self) -> None:
        ea_data = load_yaml(ROOT / "isa" / "defs" / "ea.yaml")
        entry = allocation(
            "extralong",
            34,
            fields={"e": {"kind": "ea7", "width": 7}},
        )
        length = instruction_length(entry, "TEST <ea>(e)", ea_data)
        self.assertEqual(length.minimum_required_bytes, 5)
        self.assertEqual(length.maximum_required_bytes, 15)
        self.assertEqual(required_bytes_text(length), "5-15")

    def test_required_bytes_include_fixed_immediate_payload(self) -> None:
        ea_data = load_yaml(ROOT / "isa" / "defs" / "ea.yaml")
        entry = allocation("long", 26)
        self.assertEqual(required_bytes_text(instruction_length(entry, "TEST <imm8s>", ea_data)), "5")
        self.assertEqual(required_bytes_text(instruction_length(entry, "TEST <imm16>", ea_data)), "6")

    def test_all_allocations_have_valid_byte_and_required_length_models(self) -> None:
        ea_data = load_yaml(ROOT / "isa" / "defs" / "ea.yaml")
        store = load_encoding_store(ROOT / "isa" / "defs")
        for located in store.encodings:
            encoding_class = store.classes_by_name[located.form.encoding_class]
            raw = allocation_entry_dict(located)
            entry = AllocationEntry(
                path=located.path,
                cls=encoding_class.name,
                payload_bits=encoding_class.payload_bits,
                entry_id=str(raw["id"]),
                bits="".join(str(raw["bits"]).split()),
                text=str(raw.get("text", "")),
                assigned=0,
                skipped=0,
                fields=raw.get("fields") or {},
                constraints=raw.get("constraints") or [],
                instruction_bytes=encoding_class.instruction_bytes,
            )
            with self.subTest(entry=entry.entry_id):
                byte_segments = entry_byte_segments(entry)
                self.assertEqual(len(byte_segments), allocation_opcode_bytes(entry))
                self.assertTrue(all(sum(width for _label, width in byte) == 8 for byte in byte_segments))
                length = instruction_length(entry, entry.text, ea_data)
                self.assertLessEqual(length.maximum_required_bytes, 18)


if __name__ == "__main__":
    unittest.main()
