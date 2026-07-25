#!/usr/bin/env python3
"""Regression tests for the generated reference indexes and editorial contracts."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[2]
TOOL_DIR = ROOT / "isa" / "tools"
if str(TOOL_DIR) not in sys.path:
    sys.path.insert(0, str(TOOL_DIR))

from gen_architecture_tables import output_files  # noqa: E402
from gen_docs import (  # noqa: E402
    REFERENCE_NAVIGATION_PATH,
    allocation_index_rows,
    architecture_table_data,
    event_index_rows,
    feature_index_rows,
    load_model,
    load_reference_navigation,
    mnemonic_index_rows,
    state_index_rows,
    tex_code,
    tex_breakable_code,
)
from validate_reference_navigation import (  # noqa: E402
    NavigationError,
    validate_document,
    validate_path,
)


class ReferenceNavigationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.model = load_model(ROOT / "isa" / "defs")
        cls.architecture = architecture_table_data()
        cls.navigation = load_reference_navigation(REFERENCE_NAVIGATION_PATH)

    def test_navigation_source_and_canonical_names_are_valid(self) -> None:
        self.assertEqual(validate_path(), self.navigation)

    def test_unreleased_revision_must_not_claim_a_revision_number(self) -> None:
        candidate = deepcopy(self.navigation)
        candidate["revision_history"]["unreleased"]["architecture_revision"] = 1
        with self.assertRaisesRegex(NavigationError, "expected null"):
            validate_document(candidate)

    def test_released_revisions_are_strictly_increasing(self) -> None:
        candidate = deepcopy(self.navigation)
        candidate["revision_history"]["released"] = [
            {
                "architecture_revision": 2,
                "title": "second",
                "compatibility": "compatible",
                "changes": ["second"],
            },
            {
                "architecture_revision": 1,
                "title": "first",
                "compatibility": "compatible",
                "changes": ["first"],
            },
        ]
        with self.assertRaisesRegex(NavigationError, "unique and increasing"):
            validate_document(candidate)

    def test_every_instruction_form_appears_once_in_mnemonic_index(self) -> None:
        rows = mnemonic_index_rows(self.model, self.model.instructions)
        form_cells = [row[2] for row in rows if row[2] != "--"]
        expected = [
            tex_breakable_code(entry.entry_id)
            for entries in self.model.allocated_by_mnemonic.values()
            for entry in entries
        ]
        self.assertCountEqual(form_cells, expected)
        self.assertEqual(len(form_cells), len(set(form_cells)))

    def test_state_event_and_feature_indexes_have_complete_source_coverage(self) -> None:
        state_rows = state_index_rows(self.navigation, self.architecture)
        self.assertEqual(
            len(state_rows),
            len(self.navigation["state_groups"])
            + len(self.architecture["control_registers"]),
        )
        control_rows = state_rows[-len(self.architecture["control_registers"]) :]
        for control in self.architecture["control_registers"]:
            self.assertEqual(
                sum(tex_code(control["name"]) in row[0] for row in control_rows),
                1,
            )

        event_rows = event_index_rows(self.architecture, self.model.instructions)
        self.assertEqual(
            len(event_rows),
            len(self.architecture["architectural_events"]),
        )
        self.assertCountEqual(
            [row[1] for row in event_rows],
            [
                tex_breakable_code(event["name"])
                for event in self.architecture["architectural_events"]
            ],
        )

        feature_rows = feature_index_rows(
            self.model, self.model.instructions, self.architecture
        )
        optional_instructions = [
            instruction
            for instruction in self.model.instructions
            if instruction.instruction_set != "base"
        ]
        self.assertEqual(len(feature_rows), len(optional_instructions))
        for instruction in optional_instructions:
            label = f"instr:{instruction.mnemonic.lower()}"
            self.assertEqual(
                sum(f"[{label}]" in row[2] for row in feature_rows),
                1,
            )

    def test_allocation_index_covers_each_required_namespace(self) -> None:
        rows = allocation_index_rows(self.model, self.architecture)
        text = "\n".join(" ".join(row) for row in rows)
        for encoding_class in self.model.allocation_classes:
            self.assertIn(
                tex_breakable_code(f"opcode/{encoding_class.cls}"),
                text,
            )
        for namespace in (
            "effective_address/compact",
            "effective_address/EXT0",
            "operand_selector/pt_level",
            "control_register_selector",
            "base_exception_id",
            "CPUID_class_leaf_index",
        ):
            self.assertIn(tex_breakable_code(namespace), text)

    def test_generated_urctl_selector_keeps_complete_description(self) -> None:
        outputs = output_files(self.architecture)
        selector_path = next(
            path
            for path in outputs
            if path.name == "control_register_selectors.tex"
        )
        urctl_line = next(
            line for line in outputs[selector_path].splitlines() if "URCTL" in line
        )
        self.assertIn("FLAGS, STATUS, and valid state", urctl_line)


if __name__ == "__main__":
    unittest.main()
