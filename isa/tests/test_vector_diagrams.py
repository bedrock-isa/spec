import unittest
from copy import deepcopy
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

from engine.project import IsaProject
from engine.reference import Reference
from engine.render.vector_diagram import VectorDiagramPlacementRenderer


def _reference_text(reference: Reference[object]) -> str:
    return ".".join((reference.owner, *reference.path, reference.element))


class VectorDiagramTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.root = Path(__file__).parents[1]
        cls.project = IsaProject.load(cls.root)
        cls.schema = yaml.safe_load(
            (cls.root / "schemas/vector-diagram.yaml").read_text(encoding="utf-8")
        )
        Draft202012Validator.check_schema(cls.schema)
        cls.validator = Draft202012Validator(cls.schema)

    def _diagram_bundles(self):
        return tuple(
            bundle
            for bundle in self.project.catalog.instructions.values()
            if len(bundle.diagrams.diagrams)
        )

    def _placement_fixture(self):
        bundle = self._diagram_bundles()[0]
        reference = next(iter(bundle.diagrams.diagrams))
        directive = f"(:diagram:{_reference_text(reference)}:)"
        return bundle, reference, directive, VectorDiagramPlacementRenderer()

    def test_predicate_range_schema_accepts_closed_forms_and_rejects_hybrids(self) -> None:
        documents = [
            yaml.safe_load(diagram.source.read_text(encoding="utf-8"))
            for bundle in self._diagram_bundles()
            for diagram in bundle.diagrams.diagrams.values()
        ]
        count_form = next(
            document
            for document in documents
            if document["kind"] == "predicate-range-generation"
            and "count" in document
        )
        state_form = next(
            document
            for document in documents
            if document["kind"] == "predicate-range-generation"
            and "states" in document
        )
        self.assertTrue(self.validator.is_valid(count_form))
        self.assertTrue(self.validator.is_valid(state_form))

        count_with_states = deepcopy(count_form)
        count_with_states["states"] = deepcopy(state_form["states"])
        state_with_count = deepcopy(state_form)
        state_with_count["count"] = deepcopy(count_form["count"])
        flattened = deepcopy(count_form)
        flattened["result"] = {
            "label": "new Pn",
            "element_bits": 16,
            "cells": [{"value": "0", "effect": "clear"}] * 8,
        }

        for name, invalid in (
            ("count-with-states", count_with_states),
            ("state-with-count", state_with_count),
            ("flattened-result", flattened),
        ):
            with self.subTest(name=name):
                self.assertFalse(self.validator.is_valid(invalid))

    def test_predicate_range_projection_matches_its_declared_bounds(self) -> None:
        examples = tuple(
            diagram.example
            for bundle in self._diagram_bundles()
            for diagram in bundle.diagrams.diagrams.values()
            if diagram.example.variant == "predicate-range-generation"
        )

        self.assertTrue(examples)
        for example in examples:
            start = example.data["start"]
            end = example.data["end"]
            groups = example.rows[0]["groups"]
            self.assertEqual(len(groups), 8)
            for index, group in enumerate(groups):
                active = index >= start and (
                    end == "lane-count" or index < end
                )
                self.assertEqual(
                    tuple(cell["bits"] for cell in group),
                    (8, 8),
                )
                self.assertEqual(
                    (
                        group[0]["value"],
                        group[0]["effect"],
                        group[0]["appearance"],
                    ),
                    ("1", "copy", "predicate-result")
                    if active
                    else ("0", "zero", "zero"),
                )
                self.assertEqual(
                    (
                        group[1]["value"],
                        group[1]["effect"],
                        group[1]["appearance"],
                    ),
                    ("0", "zero", "zero"),
                )

    def test_rejects_inline_placement(self) -> None:
        bundle, _reference, directive, placements = self._placement_fixture()
        with self.assertRaises(ValueError):
            placements.expand(
                f"prose {directive}",
                self.project,
                bundle.artifacts.description,
                bundle.reference,
            )

    def test_rejects_duplicate_placement(self) -> None:
        bundle, _reference, directive, placements = self._placement_fixture()
        with self.assertRaises(ValueError):
            placements.expand(
                f"{directive}\n{directive}",
                self.project,
                bundle.artifacts.description,
                bundle.reference,
            )

    def test_rejects_unplaced_declared_diagram(self) -> None:
        bundle, _reference, _directive, placements = self._placement_fixture()
        with self.assertRaises(ValueError):
            placements.expand(
                "No diagram here.",
                self.project,
                bundle.artifacts.description,
                bundle.reference,
            )

    def test_rejects_unknown_diagram_reference(self) -> None:
        bundle, reference, _directive, placements = self._placement_fixture()
        unknown = Reference(reference.owner, reference.path, "unknown")
        with self.assertRaises(ValueError):
            placements.expand(
                f"(:diagram:{_reference_text(unknown)}:)",
                self.project,
                bundle.artifacts.description,
                bundle.reference,
            )

    def test_rejects_diagram_owned_by_another_instruction(self) -> None:
        bundle, _reference, _directive, placements = self._placement_fixture()
        other = next(item for item in self._diagram_bundles() if item is not bundle)
        other_reference = next(iter(other.diagrams.diagrams))
        with self.assertRaises(ValueError):
            placements.expand(
                f"(:diagram:{_reference_text(other_reference)}:)",
                self.project,
                bundle.artifacts.description,
                bundle.reference,
            )

    def test_project_resolves_full_instruction_diagram_reference(self) -> None:
        _bundle, reference, _directive, _placements = self._placement_fixture()
        diagram = self.project.vector_diagram(_reference_text(reference))
        self.assertIs(diagram, self.project.vector_diagram(reference))

    def test_project_rejects_non_vector_diagram_reference_shapes(self) -> None:
        _bundle, reference, _directive, _placements = self._placement_fixture()
        invalid = (
            f"VECTOR.diagrams.{reference.element}",
            ".".join(("base", *reference.path, reference.element)),
        )
        for value in invalid:
            with self.subTest(reference=value):
                with self.assertRaises(ValueError):
                    self.project.vector_diagram(value)


if __name__ == "__main__":
    unittest.main()
