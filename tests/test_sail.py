import unittest
from dataclasses import replace
from pathlib import Path
import tempfile

from engine.project import ProjectLookupError, ProjectLookupReason
from engine.project import IsaProject
from engine.sail import (
    IsaConfiguration,
    SailComposer,
    SailDispatchRenderer,
    SailEntryValidator,
)
from engine.workspace import SpecWorkspace


class SailCompositionTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.workspace = SpecWorkspace.load(Path(__file__).parents[1])
        project = cls.workspace.require_provider("isa")
        if not isinstance(project, IsaProject):
            raise TypeError("workspace isa provider must be an IsaProject")
        cls.project = project
        cls.composer = SailComposer()

    def compose(self, extensions=None):
        configuration = IsaConfiguration.resolve(self.project, extensions)
        return self.composer.compose(self.project, configuration)

    def test_default_composition_contains_all_owned_instructions(self) -> None:
        program = self.compose()

        self.assertEqual(
            program.configuration.extension_ids,
            tuple(self.project.catalog.extensions),
        )
        self.assertEqual(program.bundles, self.project.select())
        self.assertEqual(
            tuple(item.bundle for item in program.instruction_semantics),
            program.bundles,
        )
        self.assertEqual(
            tuple(unit.reference for unit in program.sail_units),
            self.project.model.sail_order,
        )

    def test_configuration_rejects_unknown_extension(self) -> None:
        with self.assertRaises(ProjectLookupError) as caught:
            IsaConfiguration.resolve(self.project, ("DOES_NOT_EXIST",))
        self.assertIs(caught.exception.reason, ProjectLookupReason.UNKNOWN_EXTENSION)

    def test_extension_selection_closes_declared_dependencies(self) -> None:
        selected = next(
            extension
            for extension in self.project.catalog.extensions.values()
            if extension.requires
        )
        program = self.compose((selected.id,))

        required = set()

        def collect(extension) -> None:
            for dependency in extension.requires:
                collect(dependency)
            required.add(extension.id)

        collect(selected)
        expected_ids = tuple(
            extension_id
            for extension_id in self.project.catalog.extensions
            if extension_id in required
        )
        self.assertEqual(program.configuration.extension_ids, expected_ids)
        self.assertEqual(
            program.bundles,
            tuple(
                bundle
                for bundle in self.project.select()
                if bundle.reference.owner in {"base", *expected_ids}
            ),
        )

    def test_dispatch_projection_is_exhaustive_for_selected_entries(self) -> None:
        program = self.compose()

        self.assertEqual(
            tuple(
                (item.operation, item.entry)
                for item in SailDispatchRenderer().project(program).entries
            ),
            tuple(
                (semantics.operation, semantics.entry)
                for semantics in program.instruction_semantics
            ),
        )

    def test_missing_declared_entry_is_rejected(self) -> None:
        program = self.compose(())
        first = program.bundles[0]
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "semantics.sail"
            source.write_text("function execute_other() -> unit = ()\n")
            bad_bundle = replace(
                first,
                artifacts=replace(first.artifacts, semantics=source),
            )
            bad_semantics = replace(
                program.instruction_semantics[0], bundle=bad_bundle
            )
            bad_program = replace(
                program, instruction_semantics=(bad_semantics,)
            )

            with self.assertRaises(ValueError):
                SailEntryValidator().require(bad_program)


if __name__ == "__main__":
    unittest.main()
