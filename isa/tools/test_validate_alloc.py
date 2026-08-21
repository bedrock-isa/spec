from collections import Counter
from pathlib import Path
import unittest

from validate_alloc import (
    entry_claim_summary,
    entry_claims,
    entries_overlap,
    expand_pattern,
    pattern_union_cardinality,
)


class SymbolicAllocationTests(unittest.TestCase):
    def assert_differential(self, bits, constraints=()):
        entry = {"id": "fixture", "bits": bits, "constraints": list(constraints)}
        exhaustive, exhaustive_skipped = entry_claims(Path("fixture"), len(bits), ["?" * len(bits)], entry)
        count, symbolic_skipped, _ = entry_claim_summary(Path("fixture"), len(bits), ["?" * len(bits)], entry)
        self.assertEqual(count, len(exhaustive))
        self.assertEqual(symbolic_skipped, exhaustive_skipped)

    def test_symbolic_cardinality_matches_small_exhaustive_spaces(self):
        self.assert_differential("10aabb")
        self.assert_differential("10aabb", [{"field": "a", "allow": ["0x1..0x2"], "reason": "range"}])
        self.assert_differential("10aeeeeeee", [{"field": "e", "exclude": "immediate", "reason": "ea"}])
        self.assert_differential(
            "10zzaeeeeeee",
            [
                {"field": "z", "allow": [0, 2, 3], "reason": "size"},
                {"field": "e", "exclude": "immediate", "reason": "ea"},
            ],
        )

    def test_known_overlap_and_disjoint_constraints(self):
        left = {"id": "left", "bits": "10zzaa", "constraints": [{"field": "z", "allow": [0, 1], "reason": "size"}]}
        overlapping = {"id": "overlap", "bits": "10bb00"}
        fixed_disjoint = {"id": "fixed", "bits": "11bb00"}
        constrained_disjoint = {"id": "constraint", "bits": "10zzbb", "constraints": [{"field": "z", "allow": [2, 3], "reason": "size"}]}
        self.assertIsNotNone(entries_overlap(left, overlapping))
        self.assertIsNone(entries_overlap(left, fixed_disjoint))
        self.assertIsNone(entries_overlap(left, constrained_disjoint))

    def test_skip_counts_preserve_first_constraint_reason(self):
        entry = {
            "id": "reasons",
            "bits": "10zzaeeeeeee",
            "constraints": [
                {"field": "z", "allow": [0], "reason": "size"},
                {"field": "e", "exclude": "immediate", "reason": "ea"},
            ],
        }
        count, skipped, _ = entry_claim_summary(Path("fixture"), 12, ["?" * 12], entry)
        self.assertEqual(count + sum(skipped.values()), 1 << 10)
        self.assertEqual(skipped["size"], 3 * 128 * 2)
        self.assertEqual(skipped["ea"], 4 * 2)

    def test_pattern_union_cardinality_matches_exhaustive_small_space(self):
        fixtures = [
            ["00??", "01??"],
            ["0???", "?0??"],
            ["00??", "001?", "?111"],
        ]
        for patterns in fixtures:
            expected = len(
                {
                    value
                    for pattern in patterns
                    for value in expand_pattern(pattern)
                }
            )
            self.assertEqual(pattern_union_cardinality(patterns), expected)


if __name__ == "__main__":
    unittest.main()
