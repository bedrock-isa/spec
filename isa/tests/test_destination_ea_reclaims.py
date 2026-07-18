#!/usr/bin/env python3
"""Regression tests for reclaiming immediate EA encodings from destinations."""

from __future__ import annotations

from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[2]
TOOL_DIR = ROOT / "isa" / "tools"
if str(TOOL_DIR) not in sys.path:
    sys.path.insert(0, str(TOOL_DIR))

from validate_alloc import (  # noqa: E402
    compact_bits,
    entry_claims,
    field_value,
)
from encoding_store import allocation_entry_dict, load_encoding_store  # noqa: E402


DEFS_ROOT = ROOT / "isa" / "defs"
IMMEDIATE_EA_VALUES = range(0x6C, 0x70)


def immediate_claim_count(entry_id: str) -> int:
    store = load_encoding_store(DEFS_ROOT)
    encoding_class = store.classes_by_name["medium"]
    path = store.class_path
    entry = allocation_entry_dict(
        next(item for item in store.for_class("medium") if item.form.id == entry_id)
    )
    pattern = compact_bits(str(entry["bits"]))
    ea_fields = [
        name
        for name, spec in (entry.get("fields") or {}).items()
        if isinstance(spec, dict) and spec.get("kind") == "ea7"
    ]
    if len(ea_fields) != 1:
        raise AssertionError(f"{entry_id}: expected one EA field, got {ea_fields}")
    claims, _ = entry_claims(
        path,
        encoding_class.payload_bits,
        list(encoding_class.namespace),
        entry,
    )
    result = 0
    for value, _claim in claims:
        ea_value, width = field_value(value, pattern, ea_fields[0])
        if width != 7:
            raise AssertionError(f"{entry_id}: expected a 7-bit EA field, got {width}")
        if ea_value in IMMEDIATE_EA_VALUES:
            result += 1
    return result


class DestinationEaReclaimTests(unittest.TestCase):
    def test_read_only_and_source_eas_keep_immediate_forms(self) -> None:
        self.assertEqual(immediate_claim_count("medium.add_x_ea_e_rn_d"), 128)
        self.assertEqual(immediate_claim_count("medium.test_x_rn_s_ea_e"), 128)

    def test_both_xchg_operands_reclaim_immediate_forms(self) -> None:
        self.assertEqual(immediate_claim_count("medium.xchg_x_rn_s_ea_e"), 0)
        self.assertEqual(immediate_claim_count("medium.xchg_x_ea_e_rn_d"), 0)


if __name__ == "__main__":
    unittest.main()
