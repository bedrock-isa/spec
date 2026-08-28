import unittest
from pathlib import Path

from engine.allocation import AllocationAnalyzer, AllocationCube
from engine.encoding_architecture import (
    ENCODING_CLASSES,
    encoding_class,
    operator_space,
)
from engine.project import IsaProject


class EncodingArchitectureTest(unittest.TestCase):
    def test_named_classes_retain_architectural_namespaces(self) -> None:
        self.assertEqual(encoding_class("short").allocation_bits, 14)
        self.assertEqual(
            encoding_class("medium").namespace,
            (
                "0?????????????????",
                "10????????????????",
                "110???????????????",
                "1110??????????????",
            ),
        )
    def test_operator_spaces_are_scoped_by_class(self) -> None:
        self.assertEqual(
            operator_space("extralong", "vector").prefix, "11111101??"
        )
        with self.assertRaisesRegex(ValueError, "has no operator space"):
            operator_space("long", "vector")


class AllocationCubeTest(unittest.TestCase):
    def test_short_pattern_is_right_padded_and_intersected(self) -> None:
        prefix = AllocationCube.parse("1111", 8)
        subset = AllocationCube.parse("111100??")

        self.assertEqual(prefix.pattern, "1111????")
        self.assertTrue(prefix.contains(subset))
        self.assertEqual(prefix.intersection(subset), subset)


class AllocationAnalyzerTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.isa_root = Path(__file__).parents[1]
        cls.project = IsaProject.load(cls.isa_root)
        cls.analyzer = AllocationAnalyzer()
        cls.entries = cls.analyzer.entries(cls.project)

    def test_complete_map_contains_every_form_without_collisions(self) -> None:
        allocation = self.analyzer.analyze(self.project)
        form_count = sum(
            len(bundle.encodings.forms) for bundle in self.project.select()
        )

        self.assertEqual(len(allocation.entries), form_count)
        self.assertEqual(allocation.collisions, ())
        self.assertEqual(
            {entry.width for entry in allocation.entries},
            {item.allocation_bits for item in ENCODING_CLASSES},
        )

    def test_summary_separates_allocated_reclaimed_and_clean_free(self) -> None:
        summaries = self.analyzer.summaries(self.project)

        self.assertEqual([item.encoding_class for item in summaries], [item.name for item in ENCODING_CLASSES])
        for item in summaries:
            self.assertEqual(
                item.namespace_slots,
                item.allocated_slots + item.reclaimed_slots + item.clean_free_slots,
            )
            self.assertEqual(
                item.remaining_slots,
                item.reclaimed_slots + item.clean_free_slots,
            )
        self.assertGreater(next(item for item in summaries if item.encoding_class == "extralong").reclaimed_slots, 0)

    def test_entries_can_be_scoped_to_named_operator_space(self) -> None:
        entries = self.analyzer.entries(
            self.project, "extralong", space="vector", grep="VADD"
        )

        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0].mnemonic, "VADD")
        self.assertGreater(entries[0].reclaimed_slots, 0)

    def test_candidate_outside_class_namespace_is_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "outside xxlong namespace"):
            self.analyzer.check_candidate(self.project, "xxlong", "0000")

    def test_holes_stay_inside_operator_space_and_avoid_raw_reservations(self) -> None:
        holes = self.analyzer.holes(
            self.project,
            "xxlong",
            space="vector",
            min_slots=16,
            limit=5,
        )
        scope = AllocationCube.parse("1111111100", 42)
        raw = tuple(
            cube
            for entry in self.entries
            if entry.width == 42
            for cube in entry.raw_cubes
        )

        self.assertEqual(len(holes), 5)
        for hole in holes:
            self.assertTrue(scope.contains(hole.cube))
            self.assertFalse(any(hole.cube.overlaps(cube) for cube in raw))

    def test_reclaimed_slots_can_optionally_be_explored_as_holes(self) -> None:
        clean = self.analyzer.holes(
            self.project, "short", limit=200, include_reclaimed=False
        )
        reusable = self.analyzer.holes(
            self.project, "short", limit=200, include_reclaimed=True
        )

        self.assertGreater(
            sum(item.slots for item in reusable),
            sum(item.slots for item in clean),
        )


if __name__ == "__main__":
    unittest.main()
