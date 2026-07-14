#!/usr/bin/env python3
"""Regression tests for FPU forms with expanded size or destination fields."""

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


class FpuAllocationShapeTests(unittest.TestCase):
    FPTRANSA_PATTERNS = {
        "long.facosa_x_fn_s_fn_d": "1111011100z0000dddd000ssss",
        "long.fasina_x_fn_s_fn_d": "1111011100z0000dddd001ssss",
        "long.fatana_x_fn_s_fn_d": "1111011100z0000dddd010ssss",
        "long.fatanha_x_fn_s_fn_d": "1111011100z0000dddd011ssss",
        "long.fcosa_x_fn_s_fn_d": "1111011100z0000dddd100ssss",
        "long.fcosha_x_fn_s_fn_d": "1111011100z0000dddd101ssss",
        "long.fetoxa_x_fn_s_fn_d": "1111011100z0000dddd110ssss",
        "long.fetoxm1a_x_fn_s_fn_d": "1111011100z0000dddd111ssss",
        "long.flog10a_x_fn_s_fn_d": "1111011100z0001dddd000ssss",
        "long.flog2a_x_fn_s_fn_d": "1111011100z0001dddd001ssss",
        "long.flogna_x_fn_s_fn_d": "1111011100z0001dddd010ssss",
        "long.flognp1a_x_fn_s_fn_d": "1111011100z0001dddd011ssss",
        "long.fsina_x_fn_s_fn_d": "1111011100z0001dddd100ssss",
        "long.fsinha_x_fn_s_fn_d": "1111011100z0001dddd110ssss",
        "long.ftana_x_fn_s_fn_d": "1111011100z0001dddd111ssss",
        "long.ftanha_x_fn_s_fn_d": "1111011100z0010dddd000ssss",
        "long.ftentoxa_x_fn_s_fn_d": "1111011100z0010dddd001ssss",
        "long.ftwotoxa_x_fn_s_fn_d": "1111011100z0010dddd010ssss",
        "extralong.fsincosa_x_fn_s_fn_d_fn_c": "1111110000001z01ssss000dddd000cccc",
    }

    @classmethod
    def setUpClass(cls) -> None:
        cls.long_path = ROOT / "isa" / "alloc" / "long.yaml"
        cls.extralong_path = ROOT / "isa" / "alloc" / "extralong.yaml"
        cls.long_data = load_yaml(cls.long_path)
        cls.extralong_data = load_yaml(cls.extralong_path)

    def entry(self, data: dict[str, Any], entry_id: str) -> dict[str, Any]:
        return next(item for item in data["entries"] if item["id"] == entry_id)

    def claim_count(self, path: Path, data: dict[str, Any], entry_id: str) -> tuple[int, dict[str, int]]:
        payload_bits = int(data["payload_bits"])
        claims, skipped = entry_claims(
            path,
            payload_bits,
            namespace_patterns(payload_bits, data),
            self.entry(data, entry_id),
        )
        return len(claims), dict(skipped)

    def test_fmovcr_uses_the_common_long_fpu_size_position(self) -> None:
        entry = self.entry(self.long_data, "long.fmovcr_x_imm16_fn_d")
        pattern = compact_bits(str(entry["bits"]))

        self.assertEqual(pattern, "1111010110z01100010000dddd")
        self.assertEqual(pattern.index("z"), 10)
        self.assertEqual(entry["fields"]["z"], {"kind": "size", "width": 1})
        self.assertEqual(self.claim_count(self.long_path, self.long_data, entry["id"]), (32, {}))

    def test_fsincosa_uses_the_requested_extralong_fpu_layout(self) -> None:
        entry = self.entry(self.extralong_data, "extralong.fsincosa_x_fn_s_fn_d_fn_c")
        pattern = compact_bits(str(entry["bits"]))
        fma_pattern = compact_bits(
            str(self.entry(self.extralong_data, "extralong.fmadd_x_ea_l_fn_r_fn_d")["bits"])
        )

        self.assertEqual(pattern, "1111110000001z01ssss000dddd000cccc")
        self.assertEqual(pattern.index("z"), fma_pattern.index("z"))
        self.assertEqual(entry["fields"]["c"], {"kind": "freg", "width": 4})
        self.assertEqual(self.claim_count(self.extralong_path, self.extralong_data, entry["id"]), (8_192, {}))
        self.assertFalse(any(item["id"].startswith("long.fsincosa") for item in self.long_data["entries"]))

    def test_all_fptransa_renames_preserve_the_allocated_bit_patterns_and_cardinality(self) -> None:
        entries = {
            entry["id"]: entry
            for data in (self.long_data, self.extralong_data)
            for entry in data["entries"]
            if entry["id"] in self.FPTRANSA_PATTERNS
        }
        self.assertEqual(set(entries), set(self.FPTRANSA_PATTERNS))
        for entry_id, expected_pattern in self.FPTRANSA_PATTERNS.items():
            with self.subTest(entry=entry_id):
                self.assertEqual(compact_bits(str(entries[entry_id]["bits"])), expected_pattern)

        long_claims = sum(
            self.claim_count(self.long_path, self.long_data, entry_id)[0]
            for entry_id in self.FPTRANSA_PATTERNS
            if entry_id.startswith("long.")
        )
        extralong_claims = self.claim_count(
            self.extralong_path,
            self.extralong_data,
            "extralong.fsincosa_x_fn_s_fn_d_fn_c",
        )[0]
        self.assertEqual((long_claims, extralong_claims), (18 * 512, 8_192))

    def test_instruction_definitions_match_the_expanded_forms(self) -> None:
        fmovcr = load_yaml(
            ROOT / "isa" / "defs" / "extensions" / "fpu" / "instructions" / "FMOVCR" / "instruction.yaml"
        )
        fsincosa = load_yaml(
            ROOT
            / "isa"
            / "defs"
            / "extensions"
            / "fpu_transcendental_approx"
            / "instructions"
            / "FSINCOSA"
            / "instruction.yaml"
        )

        self.assertEqual(fmovcr["forms"]["size"], "S_D")
        self.assertEqual(fsincosa["behavior"]["output"], ["sin_dst", "cos_dst"])
        self.assertEqual(
            [operand["name"] for operand in fsincosa["forms"]["operands"]],
            ["src", "sin_dst", "cos_dst"],
        )


if __name__ == "__main__":
    unittest.main()
