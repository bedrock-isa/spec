#!/usr/bin/env python3
"""Regression checks for decisions preserved by the integrated migration."""

from __future__ import annotations

from pathlib import Path
import sys
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[2]
TOOL_DIR = ROOT / "isa" / "tools"
if str(TOOL_DIR) not in sys.path:
    sys.path.insert(0, str(TOOL_DIR))

from encoding_store import load_encoding_store  # noqa: E402


class IntegratedMigrationInvariantTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.defs = ROOT / "isa" / "defs"
        cls.store = load_encoding_store(cls.defs)

    def test_instruction_encoding_and_operand_projection_counts(self) -> None:
        instructions = list(self.defs.glob("**/instructions/*/instruction.yaml"))
        operands = [
            operand
            for located in self.store.encodings
            for operand in located.form.operands
        ]
        self.assertEqual(len(instructions), 205)
        self.assertEqual(len(self.store.encodings), 402)
        self.assertEqual(len(operands), 762)
        self.assertEqual(sum(operand.domain == "user" for operand in operands), 4)
        self.assertFalse(any("reserved" in located.form.id.lower() for located in self.store.encodings))

    def test_removed_unallocated_forms_have_no_backlog(self) -> None:
        self.assertFalse((ROOT / "isa" / "pending_instruction_forms.yaml").exists())

    def test_privilege_cache_and_fpu_ownership_decisions_remain(self) -> None:
        for mnemonic in ("RDPMC", "RDSEG", "WRSEG", "WAIT"):
            instruction = yaml.safe_load(
                (self.defs / "instructions" / mnemonic / "instruction.yaml").read_text(
                    encoding="utf-8"
                )
            )
            self.assertEqual(instruction["attributes"]["privilege"], "unprivileged")

        for mnemonic in (
            "PREFETCH",
            "PREFETCHNT",
            "FLSHDCACHE",
            "INVDCACHE",
            "INVICACHE",
            "SYNCCACHE",
            "WRBKDCACHE",
        ):
            forms = yaml.safe_load(
                (self.defs / "instructions" / mnemonic / "encodings.yaml").read_text(
                    encoding="utf-8"
                )
            )["forms"]
            self.assertTrue(
                all(
                    any(
                        constraint.get("exclude") == "reg_direct"
                        for constraint in form.get("constraints", [])
                    )
                    for form in forms
                ),
                mnemonic,
            )

        for mnemonic in ("RDFFLAGS", "RDFSTATUS", "WRFFLAGS", "WRFSTATUS"):
            self.assertFalse((self.defs / "instructions" / mnemonic).exists())
            self.assertTrue(
                (self.defs / "extensions" / "fpu" / "instructions" / mnemonic).is_dir()
            )

    def test_extension_cpuid_positions_are_exact(self) -> None:
        fpu = yaml.safe_load(
            (self.defs / "extensions" / "fpu" / "extension.yaml").read_text(
                encoding="utf-8"
            )
        )
        fptransa = yaml.safe_load(
            (
                self.defs
                / "extensions"
                / "fpu"
                / "extensions"
                / "transcendental_approx"
                / "extension.yaml"
            ).read_text(encoding="utf-8")
        )
        self.assertEqual(
            fpu["availability"]["cpuid"],
            {"feature": "FP", "class": 1, "leaf": 0, "index": 1, "bit": 0},
        )
        self.assertEqual(
            fptransa["availability"]["cpuid"],
            {"feature": "FPTRANSA", "class": 1, "leaf": 0, "index": 1, "bit": 1},
        )


if __name__ == "__main__":
    unittest.main()
