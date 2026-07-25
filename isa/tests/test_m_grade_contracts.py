#!/usr/bin/env python3
"""Regression tests for the resolved M-grade ISA reference contracts."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import sys
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[2]
TOOL_DIR = ROOT / "isa" / "tools"
if str(TOOL_DIR) not in sys.path:
    sys.path.insert(0, str(TOOL_DIR))

from encoding_store import load_encoding_store  # noqa: E402
from validate_conformance import (  # noqa: E402
    ConformanceError,
    validate_golden_document,
    validate_manifest_document,
)


def load_yaml(relative: str):
    return yaml.safe_load((ROOT / relative).read_text(encoding="utf-8"))


class MGradeContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.store = load_encoding_store(ROOT / "isa" / "defs")

    def test_atomic_inventory_fences_and_litmus_families(self) -> None:
        memory_model = (
            ROOT / "isa/tools/latex_builder/templates/memory_model.tex"
        ).read_text(encoding="utf-8")
        self.assertIn(
            r"\texttt{CMPXCHG}, \texttt{FETCHADD}, \texttt{FETCHSUB}, "
            r"\texttt{FETCHAND}, \texttt{FETCHOR}, and",
            memory_model,
        )
        self.assertIn(r"\texttt{FETCHXOR} are the atomic read-modify-write", memory_model)
        self.assertIn("contributes no write and therefore creates no release sequence", memory_model)
        self.assertIn(r"\texttt{RFENCE} & ordered & baseline & baseline & baseline", memory_model)
        self.assertIn(r"\texttt{WFENCE} & baseline & baseline & baseline & ordered", memory_model)
        self.assertIn(r"\texttt{AFENCE} & ordered & ordered & ordered & ordered", memory_model)

        vectors = load_yaml("isa/memory_model/atomic_order_litmus.yaml")
        self.assertEqual(
            vectors["ordered_before_pairs"],
            {
                "RFENCE": ["read_to_read"],
                "WFENCE": ["write_to_write"],
                "AFENCE": [
                    "read_to_read",
                    "read_to_write",
                    "write_to_read",
                    "write_to_write",
                ],
            },
        )
        families = {
            case["model_family"]
            for case in vectors["cases"]
            if "model_family" in case
        }
        self.assertEqual(families, {"MP", "SB", "IRIW", "RWC"})
        seqcst_failure = next(
            case
            for case in vectors["cases"]
            if case["id"] == "failed_cmpxchg_seqcst_classification"
        )
        self.assertEqual(seqcst_failure["required_events"][0]["kind"], "sc_load")
        self.assertEqual(seqcst_failure["final"]["value"], 1)

    def test_cross_page_fault_priority_and_commit_vectors(self) -> None:
        vectors = load_yaml("isa/reference/address_translation_test_vectors.yaml")
        by_id = {case["id"]: case for case in vectors["vectors"]}
        paging_off = by_id["paging_disabled_full_width"]
        self.assertEqual(
            paging_off["linear_address"],
            paging_off["expected"]["memory_system_address"],
        )
        for case_id, cause in (
            ("cross_page_qword_second_not_present", "NOT_PRESENT"),
            ("cross_page_qword_second_permission", "PERMISSION"),
            ("cross_page_second_address_type", "ADDRESS_TYPE"),
        ):
            expected = by_id[case_id]["expected"]
            self.assertEqual(expected["cause"], cause)
            self.assertEqual(expected["visible_store_bytes"], 0)
            self.assertEqual(expected["changed_leaf_d_bits"], 0)
        fetch = by_id["cross_page_instruction_fetch_permission"]["expected"]
        self.assertFalse(fetch["decode_started"])
        self.assertFalse(fetch["operand_evaluation_started"])

    def test_stack_wait_and_halt_commit_vectors(self) -> None:
        vectors = load_yaml("isa/reference/stack_event_test_vectors.yaml")
        stack = {case["id"]: case for case in vectors["ordinary_stack"]["cases"]}
        self.assertEqual(stack["push_or_call"]["committed_sp"], 0x0FF8)
        self.assertEqual(stack["pop_or_ret"]["committed_sp"], 0x1008)
        self.assertEqual(stack["pair_push"]["range_half_open"], [0x0FF0, 0x1000])
        self.assertEqual(stack["pair_pop"]["range_half_open"], [0x1000, 0x1010])
        self.assertEqual(stack["far_call"]["committed_sp"], 0x0FF0)
        self.assertEqual(stack["far_return"]["committed_sp"], 0x1010)
        self.assertEqual(
            vectors["ordinary_stack"]["fault_before_commit"],
            {"memory": "unchanged", "sp": "unchanged", "destinations": "unchanged"},
        )
        wait_cases = {case["id"]: case for case in vectors["wait"]["cases"]}
        self.assertEqual(wait_cases["zero_delay"]["architectural_effect"], "normal_retirement")
        self.assertEqual(wait_cases["finite_delay"]["retired_pc"], "following_instruction")
        halt_cases = {case["id"]: case for case in vectors["halt"]["cases"]}
        self.assertFalse(halt_cases["pending_admissible_event"]["enters_halted_state"])
        self.assertEqual(halt_cases["later_admissible_event"]["fetch_while_halted"], "stopped")
        self.assertEqual(
            halt_cases["logical_processor_scope"]["other_logical_processors"],
            "continue_independent_execution",
        )

    def test_pmc_contract_remains_unprivileged_and_fixed(self) -> None:
        instruction = load_yaml("isa/defs/instructions/RDPMC/instruction.yaml")
        details = (ROOT / "isa/defs/instructions/RDPMC/details.tex.in").read_text(
            encoding="utf-8"
        )
        self.assertEqual(instruction["attributes"]["privilege"], "unprivileged")
        self.assertIn(r"modulo $2^{64}$", details)
        self.assertIn("Cold reset and warm RESET clear them to zero", details)
        self.assertIn("Clearing PMC.EN freezes the current counter values", details)

    def test_identity_revision_contract(self) -> None:
        text = (
            ROOT / "isa/tools/latex_builder/templates/cpuid_feature_discovery.tex"
        ).read_text(encoding="utf-8")
        self.assertIn(
            "unsigned 16-bit, monotonically increasing compatibility level",
            text,
        )
        self.assertIn("within one\n\\texttt{ARCHITECTURE\\_ID}", text)
        self.assertIn("selected from their CPUID leaves and feature bits", text)
        self.assertIn(
            "\\texttt{VENDOR\\_ID} selects the vendor namespace",
            text,
        )
        self.assertIn("and is compared only when both", text)

    def test_golden_vectors_reconstruct_and_reject_drift(self) -> None:
        golden = load_yaml("isa/reference/assembler_golden_vectors.yaml")
        validate_golden_document(golden, self.store)
        broken = deepcopy(golden)
        broken["cases"][0]["encoded_bytes"][0] ^= 1
        with self.assertRaises(ConformanceError):
            validate_golden_document(broken, self.store)

    def test_manifest_references_only_present_case_ids(self) -> None:
        manifest = load_yaml("isa/reference/conformance_manifest.yaml")
        validate_manifest_document(manifest, ROOT)
        broken = deepcopy(manifest)
        broken["families"][0]["required_cases"].append("missing_case")
        with self.assertRaises(ConformanceError):
            validate_manifest_document(broken, ROOT)

    def test_review_drops_scope_expansion_arguments(self) -> None:
        review = (ROOT / "ISA_REFERENCE_COMPARISON_REVIEW.md").read_text(
            encoding="utf-8"
        )
        for forbidden in (
            "지원하지 않는다고 한 줄로 명시",
            "Intel SDM처럼 기능을 확장할 필요는 없다",
            "VM migration",
            "spurious wake",
            "per-counter user",
            "global privilege",
        ):
            self.assertNotIn(forbidden, review)
        for item in range(1, 9):
            self.assertIn(f"M-{item:02d}", review)


if __name__ == "__main__":
    unittest.main()
