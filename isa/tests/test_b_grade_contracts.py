#!/usr/bin/env python3
"""Regression checks for the B-grade architectural contracts."""

from __future__ import annotations

from pathlib import Path
import sys
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[2]
TOOL_DIR = ROOT / "isa" / "tools"
if str(TOOL_DIR) not in sys.path:
    sys.path.insert(0, str(TOOL_DIR))

from defs_schema import decode_encodings  # noqa: E402
from gen_architecture_tables import SOURCE, load_mapping, validate_manifest  # noqa: E402
from gen_docs import entry_ea_fields, load_model  # noqa: E402


class BGradeContractTests(unittest.TestCase):
    def test_cpuid_cache_and_save_wire_values(self) -> None:
        data = load_mapping(SOURCE)
        validate_manifest(data)
        cpuid = data["cpuid"]

        leaves = {
            (int(cls["id"]), int(leaf["id"])): leaf
            for cls in cpuid["classes"]
            for leaf in cls["leaves"]
        }
        self.assertEqual(
            (leaves[(2, 0)]["name"], leaves[(2, 0)]["max_index"]),
            ("IMPLEMENTATION_DIRECTORY", 0),
        )
        self.assertEqual(leaves[(2, 1)]["name"], "CACHE_TOPOLOGY")

        base_header = (2 << 32) | (0 << 16) | 18
        implementation_header = (4 << 16) | 0
        indexed_leaf_header = 4
        self.assertEqual(base_header, 0x0000000200000012)
        self.assertEqual(implementation_header, 0x0000000000040000)
        self.assertEqual(indexed_leaf_header, 0x0000000000000004)
        self.assertEqual(implementation_header & 0xFFFFFFFF00000000, 0)
        self.assertEqual(indexed_leaf_header & 0xFFFFFFFFFFFF0000, 0)

        granule_result = 64
        private_l1d = 1 | (1 << 2) | (6 << 6) | (0x1234 << 32)
        shared_l2u = 3 | (2 << 2) | (6 << 6) | (1 << 12) | (3 << 16) | (0x55 << 32)
        self.assertEqual(granule_result, 0x0000000000000040)
        self.assertEqual(granule_result & 0xFFFFFFFFFFFF0000, 0)
        self.assertEqual(private_l1d, 0x0000123400000185)
        self.assertEqual(shared_l2u, 0x000000550003118B)
        self.assertEqual(
            [(item["name"], item["bits"]) for item in cpuid["cache_topology"]["fields"]],
            [
                ("TYPE", "1..0"),
                ("LEVEL", "5..2"),
                ("LINE_LOG2", "11..6"),
                ("SHARING_LEVEL", "15..12"),
                ("SHARING_LP_COUNT_MINUS1", "31..16"),
                ("SHARING_ID", "63..32"),
            ],
        )

        save = cpuid["save_area_layout"]
        fp = save["components"][0]
        index2 = (
            int(save["fixed_size_bytes"])
            | (len(save["components"]) << 16)
            | (int(save["bitmap_words"]) << 32)
            | (int(save["format"]) << 48)
        )
        descriptor_a = (
            int(fp["id"])
            | (int(fp["bitmap_bit"]) << 16)
            | (int(fp["offset_bytes"]) << 32)
        )
        descriptor_b = (
            int(fp["max_size_bytes"])
            | (int(fp["alignment_bytes"]) << 32)
            | (int(fp["init_policy"]) << 48)
        )
        self.assertEqual(index2, 0x00000001000100C0)
        self.assertEqual(descriptor_a, 0x000000C000000001)
        self.assertEqual(descriptor_b, 0x00010040000000C0)
        self.assertEqual(index2 & 0xFFF0000000000000, 0)
        self.assertEqual(descriptor_a & 0x00000000FFC00000, 0)
        self.assertEqual(descriptor_b & 0xFF00000000000000, 0)
        self.assertEqual(1 << int(fp["bitmap_bit"]), 0x1)
        self.assertEqual(
            [(item["name"], int(item["offset"]), int(item["size"])) for item in fp["layout"]],
            [
                ("F0_F15", 0x000, 0x080),
                ("FFLAGS", 0x080, 0x008),
                ("FSTATUS", 0x088, 0x008),
            ],
        )
        self.assertEqual(int(fp["offset_bytes"]) + int(fp["max_size_bytes"]), 0x180)

    def test_save_lifecycle_and_atomicity_are_normative(self) -> None:
        save_area = (
            ROOT / "isa" / "tools" / "latex_builder" / "templates" / "save_restore_area.tex"
        ).read_text(encoding="utf-8")
        save = (ROOT / "isa" / "defs" / "instructions" / "SAVE" / "details.tex").read_text(
            encoding="utf-8"
        )
        restore = (
            ROOT / "isa" / "defs" / "instructions" / "RESTORE" / "details.tex"
        ).read_text(encoding="utf-8")
        for text in (
            r"\texttt{FMT=0}",
            r"\texttt{GS\_VALID=0x3f}",
            "SAVE does not change clean or modified state",
            "installs that component's initial state",
        ):
            self.assertIn(text, save_area)
        self.assertIn(r"\texttt{SAVE\_AREA\_SIZE\_BYTES}", save)
        self.assertIn("leaves the architectural register state and save area unchanged", save)
        self.assertIn("preserves the current GSn", restore)
        self.assertIn("before architectural state is committed", restore)

    def test_fp_common_vectors_and_text_match(self) -> None:
        vectors = yaml.safe_load(
            (ROOT / "isa" / "reference" / "fp_common_test_vectors.yaml").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual(vectors["schema_version"], 0)
        signed = {item["id"]: item for item in vectors["signed_integer_conversion"]}
        unsigned = {item["id"]: item for item in vectors["unsigned_integer_conversion"]}
        for section in (
            "nan_and_zero",
            "subnormal",
            "rounding_mode",
            "signed_integer_conversion",
            "unsigned_integer_conversion",
            "trap_commit",
        ):
            self.assertEqual({item["format"] for item in vectors[section]}, {"S", "D"})
        self.assertEqual(
            {(item["format"], item["mode"]) for item in vectors["rounding_mode"]},
            {
                (fmt, mode)
                for fmt in ("S", "D")
                for mode in ("nearest_even", "toward_zero", "toward_positive", "toward_negative")
            },
        )
        for prefix in ("s", "d"):
            self.assertEqual(signed[f"{prefix}_negative_overflow"]["result"], 0x8000000000000000)
            self.assertEqual(signed[f"{prefix}_positive_overflow"]["result"], 0x7FFFFFFFFFFFFFFF)
            self.assertEqual(signed[f"{prefix}_nan"]["result"], 0)
            self.assertEqual(unsigned[f"{prefix}_negative"]["result"], 0)
            self.assertEqual(unsigned[f"{prefix}_positive_overflow"]["result"], 0xFFFFFFFFFFFFFFFF)
            self.assertEqual(unsigned[f"{prefix}_nan"]["result"], 0)
            self.assertEqual(signed[f"{prefix}_valid_inexact"]["flags"], ["NX"])
            self.assertEqual(unsigned[f"{prefix}_positive_overflow"]["flags"], ["NV"])
        for item in vectors["trap_commit"][:2]:
            self.assertEqual(
                (item["destination"], item["integer_flags"], item["fflags"]),
                ("unchanged", "unchanged", "unchanged"),
            )

        intro = (
            ROOT / "isa" / "defs" / "extensions" / "fpu" / "introduction.tex"
        ).read_text(encoding="utf-8")
        for text in (
            "0x7fc00000",
            "0x7ff8000000000000",
            "tininess after rounding",
            "greater & 0 & 0 & 0 & 0",
            "unordered & 0 & 0 & 0 & 1",
            "destination, integer FLAGS, and FFLAGS remain unchanged",
        ):
            self.assertIn(text, intro)

    def test_every_ea_has_role_and_width(self) -> None:
        unsized_q = {
            "DJcc",
            "FLSHDCACHE",
            "IJcc",
            "INVDCACHE",
            "INVICACHE",
            "INVPAGE",
            "LCALL",
            "LJMP",
            "PREFETCH",
            "PREFETCHNT",
            "PTQUERY",
            "RESTORE",
            "SAVE",
            "SYNCCACHE",
            "WRBKDCACHE",
        }
        seen_unsized: set[str] = set()
        control_targets: set[str] = set()
        for path in sorted((ROOT / "isa" / "defs").glob("**/instructions/*/encodings.yaml")):
            document = decode_encodings(path, yaml.safe_load(path.read_text(encoding="utf-8")))
            for form in document.forms:
                ea_operands = [operand for operand in form.operands if operand.type == "EA"]
                for operand in ea_operands:
                    self.assertIn(operand.ea_role, {"value", "address", "control_target"})
                    self.assertIn(operand.ea_width, {"operation_size", "B", "W", "L", "Q"})
                    if not form.sizes:
                        self.assertEqual(operand.ea_width, "Q")
                        seen_unsized.add(path.parent.name)
                    if operand.ea_role == "control_target":
                        control_targets.add(path.parent.name)
        self.assertEqual(seen_unsized, unsized_q)
        self.assertEqual(
            control_targets,
            {"CALL", "JMP", "Jcc", "DJcc", "IJcc", "LCALL", "LJMP"},
        )

        model = load_model(ROOT / "isa" / "defs")
        save_entry = model.allocated_by_mnemonic["SAVE"][0]
        lcall_entry = model.allocated_by_mnemonic["LCALL"][0]
        self.assertEqual(entry_ea_fields(save_entry, save_entry.text), [("e", "address operand")])
        self.assertEqual(
            entry_ea_fields(lcall_entry, lcall_entry.text),
            [("e", "control target")],
        )

    def test_cache_range_and_remote_fetch_contract(self) -> None:
        memory = (
            ROOT / "isa" / "tools" / "latex_builder" / "templates" / "memory_model.tex"
        ).read_text(encoding="utf-8")
        intrinsics = (ROOT / "isa" / "c" / "bedrock-target-intrinsics.tex").read_text(
            encoding="utf-8"
        )
        litmus = yaml.safe_load(
            (ROOT / "isa" / "memory_model" / "cache_sync_litmus.yaml").read_text(
                encoding="utf-8"
            )
        )
        self.assertIn("every data or unified cache copy", memory)
        self.assertIn("release/acquire rendezvous", memory)
        self.assertIn("one block instruction per selected block", intrinsics)
        granule = int(litmus["block_selection"]["granule_bytes"])
        for case in litmus["block_selection"]["cases"]:
            selected = int(case["physical_address"]) & -granule
            self.assertEqual(selected, int(case["selected_base"]))
            self.assertEqual(selected + granule, int(case["selected_limit"]))

        ranges = {item["id"]: item for item in litmus["c_ranges"]}
        self.assertEqual(ranges["zero_length"]["selected_blocks"], [])
        two_blocks = ranges["two_blocks"]
        first = int(two_blocks["address"]) & -granule
        last = (int(two_blocks["address"]) + int(two_blocks["length"]) - 1) & -granule
        self.assertEqual(two_blocks["selected_blocks"], [first, last])
        self.assertEqual(two_blocks["retired_before_fault"], "preserved")

        page = litmus["page_boundary"]
        self.assertEqual(page["selected_blocks"], [0x0FC0, 0x1000])
        self.assertEqual(page["translated_pages"], [0x0000, 0x1000])
        self.assertEqual(page["second_page_fault"]["first_block_effect"], "preserved")
        self.assertEqual(page["second_page_fault"]["second_block_effect"], "none")

        broadcast = litmus["data_domain_broadcast"]
        self.assertEqual(broadcast["required_targets"], ["lp0.D", "lp1.D", "lp2.U"])
        self.assertEqual(broadcast["excluded_targets"], ["lp3.I"])
        self.assertEqual(broadcast["retirement"], "after_all_required_targets_complete")

        remote = litmus["remote_instruction_fetch"]
        self.assertIn("release_rendezvous", remote["publisher"])
        for actions in remote["receivers"].values():
            self.assertEqual(
                actions,
                ["acquire_rendezvous", "INVICACHE_each_intersecting_block", "branch_to_code"],
            )
        self.assertEqual(remote["allowed_fetch"], "new")
        self.assertEqual(remote["forbidden_fetch"], "old")


if __name__ == "__main__":
    unittest.main()
