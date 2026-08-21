#!/usr/bin/env python3

from __future__ import annotations

import unittest
from pathlib import Path
from types import SimpleNamespace

from gen_opcode_quadtree import (
    build_payload,
    count_entry_in_prefix,
    count_pattern_in_prefix,
    namespace_root_prefix,
    render_html,
)


class OpcodeQuadtreeTests(unittest.TestCase):
    def test_pattern_prefix_intersection(self) -> None:
        self.assertEqual(count_pattern_in_prefix("10????", "10"), 16)
        self.assertEqual(count_pattern_in_prefix("10????", "1001"), 4)
        self.assertEqual(count_pattern_in_prefix("10????", "11"), 0)

    def test_namespace_root_prefix_finds_zoom_anchor(self) -> None:
        self.assertEqual(namespace_root_prefix(["11110?", "111110"]), "1111")
        self.assertEqual(namespace_root_prefix(["111111????"]), "111111")
        self.assertEqual(namespace_root_prefix(["0?????", "10????"]), "")

    def test_entry_count_honors_named_fields_and_prefixes(self) -> None:
        entry = {"id": "short.demo", "bits": "10aabb??"}
        self.assertEqual(count_entry_in_prefix(entry, "10"), 64)
        self.assertEqual(count_entry_in_prefix(entry, "1001"), 16)
        self.assertEqual(count_entry_in_prefix(entry, "11"), 0)

    def test_entry_count_honors_allow_and_exclude_constraints(self) -> None:
        allowed = {
            "id": "short.conditional",
            "bits": "11ccccii",
            "constraints": [{"field": "c", "allow": ["0x2..0xf"]}],
        }
        excluded = {
            "id": "medium.destination",
            "bits": "0eeeeeee",
            "constraints": [{"field": "e", "exclude": "immediate"}],
        }
        self.assertEqual(count_entry_in_prefix(allowed, "11"), 56)
        self.assertEqual(count_entry_in_prefix(allowed, "1100"), 8)
        self.assertEqual(count_entry_in_prefix(excluded, "0"), 124)

    def test_html_embeds_payload_without_external_dependencies(self) -> None:
        html = render_html({"classes": [], "source": "</script>"})
        self.assertIn("Opcode allocation quadtree", html)
        self.assertIn("<\\/script>", html)
        self.assertNotIn("https://", html)

    def test_payload_accepts_relative_or_external_definition_roots(self) -> None:
        relative_store = SimpleNamespace(defs_root=Path("isa/instructions/definitions"))
        external_store = SimpleNamespace(defs_root=Path("/private/tmp/custom-definitions"))
        self.assertEqual(
            build_payload(relative_store, [], 1)["source"],
            "isa/instructions/definitions",
        )
        self.assertEqual(
            build_payload(external_store, [], 1)["source"],
            "external definitions (custom-definitions)",
        )


if __name__ == "__main__":
    unittest.main()
