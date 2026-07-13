#!/usr/bin/env python3
"""Regression tests for compact FP pairs and SREG stack forms."""

from __future__ import annotations

from pathlib import Path
import sys
import unittest
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
TOOL_DIR = ROOT / "isa" / "tools"
if str(TOOL_DIR) not in sys.path:
    sys.path.insert(0, str(TOOL_DIR))

from validate_alloc import compact_bits, entry_claims, namespace_patterns  # noqa: E402
from validate_isa import load_yaml  # noqa: E402


class StackPairInstructionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.allocations = {
            name: load_yaml(ROOT / "isa" / "alloc" / f"{name}.yaml")
            for name in ("extrashort", "short", "long")
        }
        cls.fpu_dir = ROOT / "isa" / "defs" / "extensions" / "fpu"
        cls.base_dir = ROOT / "isa" / "defs" / "base" / "instructions"

    def allocation_entry(self, allocation_class: str, entry_id: str) -> dict[str, Any]:
        return next(
            entry
            for entry in self.allocations[allocation_class]["entries"]
            if entry["id"] == entry_id
        )

    def claim_count(self, allocation_class: str, entry_id: str) -> tuple[int, dict[str, int]]:
        data = self.allocations[allocation_class]
        path = ROOT / "isa" / "alloc" / f"{allocation_class}.yaml"
        payload_bits = int(data["payload_bits"])
        claims, skipped = entry_claims(
            path,
            payload_bits,
            namespace_patterns(payload_bits, data),
            self.allocation_entry(allocation_class, entry_id),
        )
        return len(claims), dict(skipped)

    def test_compact_stack_allocations_have_exact_patterns_and_cardinality(self) -> None:
        expected = {
            ("extrashort", "extrashort.fpushp_imm3_i"): (
                "1110iii",
                "FPUSHP imm3(i)",
                {"i": {"kind": "immediate", "width": 3}},
                8,
                (0x70, 0x77),
            ),
            ("extrashort", "extrashort.fpopp_imm3_i"): (
                "1111iii",
                "FPOPP imm3(i)",
                {"i": {"kind": "immediate", "width": 3}},
                8,
                (0x78, 0x7F),
            ),
            ("short", "short.push_sreg_s"): (
                "10001010000sss",
                "PUSH SREG(s)",
                {"s": {"kind": "bits", "width": 3}},
                8,
                (0xA280, 0xA287),
            ),
            ("short", "short.pop_sreg_s"): (
                "10001010001sss",
                "POP SREG(s)",
                {"s": {"kind": "bits", "width": 3}},
                8,
                (0xA288, 0xA28F),
            ),
            ("extrashort", "extrashort.push_cs"): (
                "0001101",
                "PUSH CS",
                {},
                1,
                (0x0D, 0x0D),
            ),
        }

        for (allocation_class, entry_id), (bits, text, fields, count, encoded_range) in expected.items():
            with self.subTest(entry=entry_id):
                entry = self.allocation_entry(allocation_class, entry_id)
                self.assertEqual(compact_bits(str(entry["bits"])), bits)
                self.assertEqual(entry["text"], text)
                self.assertEqual(entry.get("fields", {}), fields)
                self.assertEqual(self.claim_count(allocation_class, entry_id), (count, {}))

                payload_bits = int(self.allocations[allocation_class]["payload_bits"])
                claims, _ = entry_claims(
                    ROOT / "isa" / "alloc" / f"{allocation_class}.yaml",
                    payload_bits,
                    namespace_patterns(payload_bits, self.allocations[allocation_class]),
                    entry,
                )
                payload_values = [value for value, _claim in claims]
                framing = 0 if allocation_class == "extrashort" else 0x8000
                self.assertEqual(
                    (framing | min(payload_values), framing | max(payload_values)),
                    encoded_range,
                )

    def test_bitmap_forms_are_removed_without_compatibility_aliases(self) -> None:
        long_ids = {entry["id"] for entry in self.allocations["long"]["entries"]}
        self.assertNotIn("long.fpushm_imm16_bitmap", long_ids)
        self.assertNotIn("long.fpopm_imm16_bitmap", long_ids)
        self.assertFalse((self.fpu_dir / "instructions" / "FPUSHM.yaml").exists())
        self.assertFalse((self.fpu_dir / "instructions" / "FPOPM.yaml").exists())

        manifest = load_yaml(self.fpu_dir / "instructions.yaml")["include"]
        self.assertIn("instructions/FPUSHP.yaml", manifest)
        self.assertIn("instructions/FPOPP.yaml", manifest)
        self.assertNotIn("instructions/FPUSHM.yaml", manifest)
        self.assertNotIn("instructions/FPOPM.yaml", manifest)

    def test_fp_pair_mapping_and_stack_order_match_gpr_pairs(self) -> None:
        expected_pairs = [
            {"index": 0, "registers": ["F14", "F15"]},
            {"index": 1, "registers": ["F12", "F13"]},
            {"index": 2, "registers": ["F10", "F11"]},
            {"index": 3, "registers": ["F8", "F9"]},
            {"index": 4, "registers": ["F6", "F7"]},
            {"index": 5, "registers": ["F4", "F5"]},
            {"index": 6, "registers": ["F2", "F3"]},
            {"index": 7, "registers": ["F0", "F1"]},
        ]
        expected_repeat = {"rep": True, "repcc": True, "repg": True}
        fpushp = load_yaml(self.fpu_dir / "instructions" / "FPUSHP.yaml")
        fpopp = load_yaml(self.fpu_dir / "instructions" / "FPOPP.yaml")
        gpr_pairs = load_yaml(self.base_dir / "PUSHP.yaml")["forms"]["canonical_pairs"]

        self.assertEqual(
            [[int(register[1:]) for register in pair["registers"]] for pair in expected_pairs],
            [[int(register[1:]) for register in pair["registers"]] for pair in gpr_pairs],
        )

        for definition in (fpushp, fpopp):
            self.assertEqual(definition["forms"]["canonical_pairs"], expected_pairs)
            self.assertEqual(definition["forms"]["operands"], [{"name": "pair_index", "type": "imm3"}])
            self.assertEqual(definition["attributes"]["privilege"], "unprivileged")
            self.assertEqual(definition["attributes"]["repeatable"], expected_repeat)

        push_ops = fpushp["behavior"]["operation"]
        self.assertLess(push_ops.index("*:8 SP = first_value_v;"), push_ops.index("*:8 SP = second_value_v;"))
        pop_ops = fpopp["behavior"]["operation"]
        self.assertLess(
            pop_ops.index("local second_value_v = *:8 SP;"),
            pop_ops.index("local first_value_v = *:8 (SP + 8);"),
        )
        self.assertLess(
            pop_ops.index("F[second_reg_v] = second_value_v;"),
            pop_ops.index("F[first_reg_v] = first_value_v;"),
        )

    def test_sreg_forms_cover_all_three_bit_selectors_and_exclude_cs(self) -> None:
        segments = load_yaml(ROOT / "isa" / "defs" / "segments.yaml")["segment_registers"]
        sreg_encodings = {
            segment["name"]: segment["sreg_encoding"]
            for segment in segments
            if "sreg_encoding" in segment
        }
        self.assertEqual(
            sreg_encodings,
            {"DS": 0, "SS": 1, "GS0": 2, "GS1": 3, "GS2": 4, "GS3": 5, "GS4": 6, "GS5": 7},
        )

        expected_operands = [
            [{"name": "reg", "type": "Rn"}],
            [{"name": "reg", "type": "SREG"}],
        ]
        for mnemonic in ("PUSH", "POP"):
            definition = load_yaml(self.base_dir / f"{mnemonic}.yaml")
            if mnemonic == "PUSH":
                self.assertEqual(
                    definition["forms"]["operands"],
                    expected_operands + [[{"name": "reg", "type": "CS"}]],
                )
                self.assertTrue(definition["forms"]["cs_form"]["source_only"])
            else:
                self.assertEqual(definition["forms"]["operands"], expected_operands)
            self.assertEqual(definition["attributes"]["privilege"], "unprivileged")
            self.assertEqual(
                definition["forms"]["sreg_form"]["selectors"],
                ["DS", "SS", "GS0", "GS1", "GS2", "GS3", "GS4", "GS5"],
            )
            self.assertFalse(definition["forms"]["sreg_form"]["cs_allowed"])

        pop = load_yaml(self.base_dir / "POP.yaml")
        validation = pop["forms"]["sreg_form"]["segment_image_validation"]
        self.assertEqual(validation["invalid_image_exception"], "INVALID_CONTROL_STATE")
        self.assertTrue(validation["before_commit"])
        self.assertTrue(validation["atomic_destination_and_sp_update"])
        self.assertIn("old SS", pop["doc"]["description"])
        compact_texts = {
            entry["text"]
            for allocation_class in ("extrashort", "short")
            for entry in self.allocations[allocation_class]["entries"]
        }
        self.assertIn("PUSH CS", compact_texts)
        self.assertNotIn("POP CS", compact_texts)

    def test_c_abi_uses_pair_instructions_and_order(self) -> None:
        abi = (ROOT / "isa" / "abi" / "bedrock-c-abi.tex").read_text(encoding="utf-8")
        self.assertIn(r"\texttt{FPUSHP}", abi)
        self.assertIn(r"\texttt{FPOPP}", abi)
        self.assertIn("increasing pair-index order", abi)
        self.assertIn("decreasing pair-index order", abi)
        self.assertNotIn(r"\texttt{FPUSHM}", abi)
        self.assertNotIn(r"\texttt{FPOPM}", abi)


if __name__ == "__main__":
    unittest.main()
