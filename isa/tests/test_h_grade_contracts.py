#!/usr/bin/env python3
"""Regression checks for the H-grade architectural contracts."""

from __future__ import annotations

from pathlib import Path
import sys
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[2]
TOOL_DIR = ROOT / "isa" / "tools"
if str(TOOL_DIR) not in sys.path:
    sys.path.insert(0, str(TOOL_DIR))

from defs_schema import decode_encodings, decode_instruction  # noqa: E402
from gen_architecture_tables import SOURCE, load_mapping, validate_manifest  # noqa: E402
from gen_docs import (  # noqa: E402
    latex_opcode_allocation_map,
    latex_repeat_contract_table,
    load_model,
)


class HGradeContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data = load_mapping(SOURCE)
        validate_manifest(cls.data)
        cls.model = load_model(ROOT / "isa" / "defs")

    def test_reset_contract_is_complete_and_current_lp_scoped(self) -> None:
        contract = self.data["reset_contract"]
        self.assertEqual(contract["scope"], "executing logical processor")
        self.assertEqual(contract["other_logical_processors"], "unchanged")
        values = {
            state: row["value"]
            for row in self.data["reset_state"]
            for state in row["state"]
        }
        for index in range(16):
            self.assertEqual(values[f"R{index}"], "zero")
        self.assertEqual(values["SP"], "zero")
        self.assertEqual(values["PC"], "bootpc")
        self.assertEqual(values["STATUS"], "supervisor_only")
        self.assertEqual(values["BOOTPC"], "platform_supplied_cold_preserved_warm")
        self.assertEqual(values["BOOTCFG"], "platform_supplied_cold_preserved_warm")
        self.assertEqual(values["local_translation_cache"], "invalid")
        self.assertEqual(values["execution_state"], "running_at_bootpc")

    def test_cache_translation_control_and_event_manifests_are_closed(self) -> None:
        self.assertEqual(
            [(int(item["cp"]), item["name"]) for item in self.data["cache_policies"]],
            [
                (0, "CACHEABLE_WRITE_BACK"),
                (1, "COHERENT_UNCACHEABLE"),
                (2, "COHERENT_WRITE_THROUGH"),
                (3, "COHERENT_WRITE_COMBINING"),
            ],
        )
        self.assertEqual(len(self.data["translation_cache"]["shootdown"]), 9)
        self.assertEqual(
            self.data["translation_cache"]["shootdown"][0:3],
            ["PTE store", "AFENCE", "local invalidate"],
        )
        controlled = {
            register
            for rule in self.data["control_write_rules"]
            for register in rule["registers"]
        }
        self.assertEqual(
            controlled,
            {item["name"] for item in self.data["control_registers"]},
        )
        events = {item["name"]: item for item in self.data["architectural_events"]}
        self.assertEqual(events["DOUBLE_FAULT"]["priority"], 1)
        self.assertEqual(events["DEBUG_TRACE"]["priority"], 5)
        self.assertEqual(events["NMI"]["priority"], 6)
        self.assertEqual(events["INTERRUPT"]["priority"], 7)

    def test_repeat_contracts_are_structured_and_context_safe(self) -> None:
        instruction_paths = sorted(
            (ROOT / "isa" / "defs").glob("**/instructions/*/instruction.yaml")
        )
        repeat_count = 0
        for path in instruction_paths:
            raw = yaml.safe_load(path.read_text(encoding="utf-8"))
            document = decode_instruction(path, raw)
            if document.repeat is None:
                continue
            repeat_count += 1
            self.assertNotIn("REPGF", document.repeat.contexts)
            self.assertEqual(
                "REPcc" in document.repeat.contexts,
                document.repeat.observed is not None,
            )
            if "/extensions/fpu/" in path.as_posix():
                self.assertNotIn("REPcc", document.repeat.contexts)
        self.assertEqual(repeat_count, 141)

        for mnemonic in ("MOVcc", "XCHG", "PUSHP", "POPP"):
            instruction = next(
                item for item in self.model.instructions if item.mnemonic == mnemonic
            )
            contexts = instruction.data["repeat"]["contexts"]
            self.assertNotIn("REPcc", contexts)
        self.assertEqual(
            next(
                item for item in self.model.instructions if item.mnemonic == "DIVMODS"
            ).data["repeat"]["observed"],
            {"kind": "result", "operand": "quotient"},
        )
        table = latex_repeat_contract_table(self.model)
        self.assertIn("Instruction Repeat Contracts", table)
        self.assertIn(r"\hyperref[instr:movnt]{\texttt{MOVNT}}", table)
        self.assertIn(r"\texttt{source:src}", table)

    def test_destination_overlap_and_instruction_exceptions_are_structured(self) -> None:
        cases = {
            "XCHG": "same_value",
            "FXCHG": "same_value",
            "DIVMODS": "illegal_instruction",
            "DIVMODU": "illegal_instruction",
            "FSINCOSA": "illegal_instruction",
        }
        for mnemonic, expected_rule in cases.items():
            path = next(
                (ROOT / "isa" / "defs").glob(
                    f"**/instructions/{mnemonic}/encodings.yaml"
                )
            )
            document = decode_encodings(
                path, yaml.safe_load(path.read_text(encoding="utf-8"))
            )
            rules = {
                relation.rule
                for form in document.forms
                for relation in form.destination_overlap
            }
            self.assertEqual(rules, {expected_rule})

        divmods = next(
            item for item in self.model.instructions if item.mnemonic == "DIVMODS"
        )
        event_names = {item["event"] for item in divmods.data["exceptions"]}
        self.assertEqual(event_names, {"DIVIDE_ERROR", "ILLEGAL_INSTRUCTION"})

    def test_opcode_and_padding_contract_is_generated(self) -> None:
        opcode_map = latex_opcode_allocation_map(self.model)
        self.assertIn("Medium Opcode Allocation", opcode_map)
        self.assertIn("required", opcode_map)
        self.assertIn("each concrete required..18", opcode_map)
        self.assertIn(
            r"quotient=\allowbreak{}remainder:\allowbreak{}illegal\_\allowbreak{}instruction",
            opcode_map,
        )

        encoding = (
            ROOT
            / "isa"
            / "tools"
            / "latex_builder"
            / "templates"
            / "instruction_word_formats.tex"
        ).read_text(encoding="utf-8")
        for text in (
            "every byte value is valid",
            "including padding",
            r"ILLEGAL\_INSTRUCTION.INSUFFICIENT\_LENGTH",
            r"\texttt{LEN n, <instruction>}",
            "padding byte values are not preserved",
        ):
            self.assertIn(text, encoding)


if __name__ == "__main__":
    unittest.main()
