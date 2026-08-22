#!/usr/bin/env python3
"""Regression tests for the YAML-derived LLVM vector MC catalog."""

from __future__ import annotations

from pathlib import Path
import re
import sys
import unittest

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gen_llvm_vector_catalog  # noqa: E402


ROOT = Path(__file__).resolve().parents[2]
VECTOR_INSTRUCTIONS = (
    ROOT / "isa/instructions/definitions/extensions/vector/instructions"
)


class LLVMVectorCatalogTests(unittest.TestCase):
    def test_yaml_form_ids_are_unique_and_generated_per_source(self) -> None:
        ids_by_source = {}
        for path in sorted(VECTOR_INSTRUCTIONS.glob("*/encodings.yaml")):
            forms = (yaml.safe_load(path.read_text()) or {}).get("forms", [])
            source_ids = [form["id"] for form in forms]
            self.assertEqual(len(source_ids), len(set(source_ids)), path)
            ids_by_source[path] = set(source_ids)

        ids = set().union(*ids_by_source.values())
        self.assertEqual(
            sum(len(source_ids) for source_ids in ids_by_source.values()),
            len(ids),
        )
        generated = gen_llvm_vector_catalog._generate()
        generated_ids = set(
            re.findall(r'^  \{"([^"]+)",', generated, flags=re.MULTILINE)
        )
        generated_ids = {
            identifier for identifier in generated_ids
            if identifier.startswith(("long.", "extralong.", "xxlong."))
        }
        for path, source_ids in ids_by_source.items():
            self.assertEqual(generated_ids & source_ids, source_ids, path)
        self.assertEqual(generated_ids, ids)

    def test_vcmp_domain_constraints_are_complete(self) -> None:
        forms, _ = gen_llvm_vector_catalog._load_forms_and_sizes()
        vcmp = [form for form in forms if form["syntax"].startswith("VCMPcc")]
        legal = set()
        for form in vcmp:
            sizes = gen_llvm_vector_catalog._allowed_field_values(form, "x", 3)
            conditions = gen_llvm_vector_catalog._allowed_field_values(form, "c", 4)
            legal.update((size, condition) for size in sizes for condition in conditions)
        integer = {2, 3, 4, 5, 10, 11, 12, 13, 14, 15}
        floating = {2, 3, 8, 9, 12, 13, 14, 15}
        expected = {(size, condition) for size in range(4) for condition in integer}
        expected |= {(size, condition) for size in range(5, 8) for condition in floating}
        self.assertEqual(legal, expected)
        self.assertFalse(any(condition in {0, 1} for _, condition in legal))

    def test_repeat_table_contains_every_authoritative_vector_declaration(self) -> None:
        entries = gen_llvm_vector_catalog._load_repeat_eligibility()
        self.assertIn(("add", False, True, True), entries)

        vector_mnemonics = set()
        expected = []
        for path in sorted(VECTOR_INSTRUCTIONS.glob("*/instruction.yaml")):
            document = yaml.safe_load(path.read_text()) or {}
            mnemonic = str(document["mnemonic"])
            has_condition = mnemonic.endswith("cc")
            stem = (mnemonic[:-2] if has_condition else mnemonic).lower()
            vector_mnemonics.add(stem)
            repeat = document.get("repeat")
            if repeat:
                contexts = set(repeat.get("contexts", []))
                expected.append(
                    (stem, has_condition, "REP" in contexts, "REPcc" in contexts)
                )

        generated_vector = [
            entry for entry in entries if entry[0] in vector_mnemonics
        ]
        for entry in expected:
            with self.subTest(mnemonic=entry[0]):
                self.assertIn(entry, generated_vector)
        self.assertCountEqual(
            generated_vector,
            expected,
            "generated repeat eligibility must exactly preserve vector metadata",
        )

    def test_lane_count_helpers_and_step_memory_use_width_only_aliases(self) -> None:
        generated = gen_llvm_vector_catalog._generate()
        for form_id in (
            "long.vlcnt.v20",
            "long.vlcadd.v21",
            "xxlong.vgather1.v239",
            "xxlong.vgather1.v240",
            "xxlong.vscatter1.v248",
            "xxlong.vscatter1.v249",
        ):
            line = next(
                line for line in generated.splitlines()
                if line.startswith(f'  {{"{form_id}"')
            )
            self.assertRegex(line, r", false, true, [0-9]+,$", form_id)

if __name__ == "__main__":
    unittest.main()
