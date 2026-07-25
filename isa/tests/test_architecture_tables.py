#!/usr/bin/env python3
"""Regression tests for generated ISA-reference architecture tables."""

from __future__ import annotations

from pathlib import Path
import sys
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[2]
TOOL_DIR = ROOT / "isa" / "tools"
if str(TOOL_DIR) not in sys.path:
    sys.path.insert(0, str(TOOL_DIR))

from gen_architecture_tables import (  # noqa: E402
    SOURCE,
    generate,
    load_mapping,
    output_files,
    validate_manifest,
)


EXPECTED_CAPTIONS = {
    "Standard Performance Counters",
    "Reserved Field Defaults",
    "CPUID Class and Leaf Directory",
    "Cache-Maintenance Properties",
    "Cache-Topology Descriptor",
    "SAVE-AREA-LAYOUT Indexes",
    "SAVE Component Descriptor A",
    "SAVE Component Descriptor B",
    "Floating-Point SAVE Component",
    "Control-Register Selectors",
    r"PAGE\_FAULT Causes",
    r"ILLEGAL\_INSTRUCTION Causes",
    r"INVALID\_CONTROL\_STATE Causes",
    "FPTRANSA Accuracy Contracts",
    "Architectural Event Frame Types and Sizes",
    "Event-to-Frame-Type Assignment",
    "Immediate Operand Interpretation",
    "Architectural Reset State",
    "Atomic Memory-Order Selectors",
    "Warm RESET Contract",
    "Normal-Memory Cache Policies",
    "Translation-Cache Entry Identity",
    "Local Translation-Cache Transitions",
    "Remote Translation Shootdown Protocol",
    "WRCR Selector Rules",
    "Architectural Event Producers and Delivery State",
    "Architectural Event Boundaries and Priority",
}


class ArchitectureTableTests(unittest.TestCase):
    def test_manifest_is_valid_and_generated_files_are_current(self) -> None:
        self.assertEqual(generate(check=True), [])

    def test_generator_owns_exactly_the_derived_table_set(self) -> None:
        data = load_mapping(SOURCE)
        validate_manifest(data)
        rendered = "\n".join(output_files(data).values())
        captions = {
            line.removeprefix(r"\manualtablecaption{").removesuffix("}")
            for line in rendered.splitlines()
            if line.startswith(r"\manualtablecaption{")
        }
        self.assertEqual(captions, EXPECTED_CAPTIONS)

    def test_manifest_contains_semantic_data_not_raw_tex_rows(self) -> None:
        data = yaml.safe_load(SOURCE.read_text(encoding="utf-8"))

        def strings(value: object):
            if isinstance(value, str):
                yield value
            elif isinstance(value, dict):
                for key, child in value.items():
                    yield from strings(key)
                    yield from strings(child)
            elif isinstance(value, list):
                for child in value:
                    yield from strings(child)

        self.assertFalse(any("\\" in value for value in strings(data)))
        self.assertFalse(any(" & " in value or value.endswith(r"\\") for value in strings(data)))


if __name__ == "__main__":
    unittest.main()
