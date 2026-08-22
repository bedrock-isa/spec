#!/usr/bin/env python3
"""Regression tests for the YAML-derived LLVM vector MC catalog."""

from __future__ import annotations

from collections import Counter
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
    def test_normalized_form_count_and_generated_id_set(self) -> None:
        forms = []
        for path in sorted(VECTOR_INSTRUCTIONS.glob("*/encodings.yaml")):
            forms.extend((yaml.safe_load(path.read_text()) or {}).get("forms", []))

        ids = {form["id"] for form in forms}
        self.assertEqual(len(forms), 259)
        self.assertEqual(len(ids), 259)
        self.assertEqual(
            Counter(form["class"] for form in forms),
            Counter({"long": 47, "extralong": 91, "xxlong": 121}),
        )

        # The closed allocation has 254 source rows. Its one fieldless VDUP
        # immediate row is normalized into four fixed-width tail forms.
        source_ids = []
        for form in forms:
            source_id = form["id"]
            if source_id.startswith("long.vdup.v18."):
                source_id = re.sub(r"\.(?:b|w|l|q)$", "", source_id)
            if source_id.startswith(("extralong.vcmpcc.v47.",
                                     "xxlong.vcmpcc.v230.")):
                source_id = source_id.rsplit(".", 1)[0]
            source_ids.append(source_id)
        self.assertEqual(len(set(source_ids)), 254)
        self.assertEqual(Counter(source_ids)["long.vdup.v18"], 4)
        self.assertEqual(Counter(source_ids)["extralong.vcmpcc.v47"], 2)
        self.assertEqual(Counter(source_ids)["xxlong.vcmpcc.v230"], 2)
        self.assertTrue(all(count == 1 for key, count in Counter(source_ids).items()
                            if key not in {"long.vdup.v18",
                                           "extralong.vcmpcc.v47",
                                           "xxlong.vcmpcc.v230"}))
        generated = gen_llvm_vector_catalog._generate()
        generated_ids = set(
            re.findall(r'^  \{"([^"]+)",', generated, flags=re.MULTILINE)
        )
        generated_ids = {
            identifier for identifier in generated_ids
            if identifier.startswith(("long.", "extralong.", "xxlong."))
        }
        self.assertEqual(generated_ids, ids)

    def test_vcmp_domain_constraints_are_complete(self) -> None:
        forms, _ = gen_llvm_vector_catalog._load_forms_and_sizes()
        vcmp = [form for form in forms if form["syntax"].startswith("VCMPcc")]
        self.assertEqual(len(vcmp), 4)
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

    def test_repeat_table_is_derived_and_limits_vector_steps_to_rep(self) -> None:
        entries = gen_llvm_vector_catalog._load_repeat_eligibility()
        self.assertIn(("add", False, True, True), entries)
        vector = [entry for entry in entries if entry[0].startswith("v")]
        self.assertEqual(
            set(vector),
            {
                ("vgather1", False, True, False),
                ("vscatter1", False, True, False),
            },
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
