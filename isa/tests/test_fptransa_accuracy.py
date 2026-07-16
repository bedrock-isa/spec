#!/usr/bin/env python3
"""Regression tests for the FPTRANSA accuracy-contract model."""

from __future__ import annotations

from fractions import Fraction
import math
from pathlib import Path
import sys
import unittest


TOOL_DIR = Path(__file__).resolve().parents[1] / "tools"
if str(TOOL_DIR) not in sys.path:
    sys.path.insert(0, str(TOOL_DIR))

from fp_accuracy import (  # noqa: E402
    FPTRANSA_CONTRACT_IDS,
    FPTRANSA_MAX_ASSIGNED_CONTRACT_ID,
    compose_accuracy_result,
    cpuid_selector,
    parse_accuracy_result,
    q8_8_ceiling,
    q8_8_value,
    reference_ulp,
)


class FptransaAccuracyTests(unittest.TestCase):
    def test_q8_8_examples_and_upward_quantization(self) -> None:
        cases = {
            Fraction(1, 2): 0x0080,
            1: 0x0100,
            Fraction(3, 2): 0x0180,
            2: 0x0200,
            4: 0x0400,
            "1.5001": 0x0181,
        }
        for value, expected in cases.items():
            with self.subTest(value=value):
                self.assertEqual(q8_8_ceiling(value), expected)
                self.assertGreaterEqual(q8_8_value(expected), Fraction(str(value)))

    def test_cpuid_selector_and_documented_result(self) -> None:
        self.assertEqual(cpuid_selector(FPTRANSA_CONTRACT_IDS["FSINA"]), 0x0000000100010001)
        self.assertEqual(cpuid_selector(FPTRANSA_CONTRACT_IDS["FLOG2A"]), 0x0000000100010043)
        with self.assertRaises(ValueError):
            cpuid_selector(0)
        result = compose_accuracy_result(
            present=True,
            s_max_ulp_q8_8=0x0180,
            d_max_ulp_q8_8=0x0200,
        )
        self.assertEqual(result, 0x8000000102000180)
        parsed = parse_accuracy_result(result)
        self.assertTrue(parsed.present)
        self.assertEqual(parsed.revision, 1)
        self.assertEqual(parsed.s_max_ulp_q8_8, 0x0180)
        self.assertEqual(parsed.d_max_ulp_q8_8, 0x0200)
        self.assertEqual(compose_accuracy_result(present=False), 0)
        self.assertEqual(
            parse_accuracy_result(0),
            parse_accuracy_result(compose_accuracy_result(present=False)),
        )

    def test_assigned_contract_ids_leave_family_zero_selectors_unassigned(self) -> None:
        self.assertEqual(max(FPTRANSA_CONTRACT_IDS.values()), FPTRANSA_MAX_ASSIGNED_CONTRACT_ID)
        self.assertEqual(len(FPTRANSA_CONTRACT_IDS), len(set(FPTRANSA_CONTRACT_IDS.values())))
        self.assertTrue(all(contract_id & 0xF for contract_id in FPTRANSA_CONTRACT_IDS.values()))

    def test_present_contract_requires_both_formats_within_four_ulp(self) -> None:
        for s_bound, d_bound in ((0, 0x100), (0x100, 0), (0x401, 0x100), (0x100, 0x401)):
            with self.subTest(s=s_bound, d=d_bound), self.assertRaises(ValueError):
                compose_accuracy_result(
                    present=True,
                    s_max_ulp_q8_8=s_bound,
                    d_max_ulp_q8_8=d_bound,
                )

    def test_ulp_quantum_at_zero_normal_and_subnormal_boundaries(self) -> None:
        self.assertEqual(reference_ulp(0.0, "S"), math.ldexp(1.0, -149))
        self.assertEqual(reference_ulp(1.0, "S"), math.ldexp(1.0, -23))
        self.assertEqual(reference_ulp(math.ldexp(1.0, -126), "S"), math.ldexp(1.0, -149))
        self.assertEqual(reference_ulp(0.0, "D"), math.ldexp(1.0, -1074))
        self.assertEqual(reference_ulp(1.0, "D"), math.ldexp(1.0, -52))
        self.assertEqual(reference_ulp(math.ldexp(1.0, -1022), "D"), math.ldexp(1.0, -1074))
        self.assertEqual(reference_ulp(math.nextafter(1.0, 0.0), "S"), math.ldexp(1.0, -24))
        self.assertEqual(reference_ulp(1.0, "S"), math.ldexp(1.0, -23))
        self.assertEqual(reference_ulp(math.nextafter(1.0, 0.0), "D"), math.ldexp(1.0, -53))
        self.assertEqual(reference_ulp(1.0, "D"), math.ldexp(1.0, -52))


if __name__ == "__main__":
    unittest.main()
