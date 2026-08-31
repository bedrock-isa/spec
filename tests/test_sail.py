import unittest
from dataclasses import replace
from pathlib import Path
import tempfile

from engine.project import IsaProject
from engine.sail import (
    ArtifactWriter,
    IsaConfiguration,
    SailComposer,
    SailCatalogRenderer,
    SailDispatchRenderer,
    SailEntryValidator,
    ArtifactGeneratorRegistry,
    SailRegistryRenderer,
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
        with self.assertRaises(ValueError):
            IsaConfiguration.resolve(self.project, ("DOES_NOT_EXIST",))

    def test_extension_selection_closes_declared_dependencies(self) -> None:
        program = self.compose(("FPTRANSA",))
        self.assertEqual(program.configuration.extension_ids, ("FP", "FPTRANSA"))
        self.assertEqual(
            program.bundles,
            tuple(
                bundle
                for bundle in self.project.select()
                if bundle.reference.owner in {"base", "FP", "FPTRANSA"}
            ),
        )

    def test_registry_projection_matches_selected_operations_and_events(self) -> None:
        program = self.compose(("FPTRANSA",))
        projection = SailRegistryRenderer().project(program)

        self.assertEqual(
            tuple(
                (item.operation, item.mnemonic, item.route)
                for item in projection.operations
            ),
            tuple(
                (
                    semantics.operation,
                    semantics.bundle.instruction.mnemonic,
                    semantics.bundle.instruction.route,
                )
                for semantics in program.instruction_semantics
            ),
        )
        resolved_events = self.project.events.resolved_events(
            program.configuration.owners
        )
        self.assertEqual(
            tuple(
                (
                    item.event_id,
                    item.class_value,
                    item.selector,
                    item.frame,
                    item.family,
                )
                for item in projection.events
            ),
            tuple(
                (
                    item.event.id,
                    item.code.class_value,
                    item.code.event_selector,
                    item.event.frame,
                    item.event.family,
                )
                for item in resolved_events
            ),
        )
        self.assertEqual(
            projection.cpuid_flags,
            tuple(
                dict.fromkeys(
                    field.id
                    for bundle in program.bundles
                    for field in bundle.required_cpuid_flags
                )
            ),
        )
        self.assertEqual(
            projection.instruction_sets,
            ("BaseSet", "FpuSet", "FpuTranscendentalSet"),
        )

    def test_catalog_projection_preserves_form_and_ea_owner_relations(self) -> None:
        program = self.compose(("VECTOR",))
        projection = SailCatalogRenderer().project(program)

        self.assertEqual(
            tuple(
                (item.bundle.reference, item.form.id)
                for item in projection.forms
            ),
            tuple(
                (bundle.reference, form.id)
                for bundle in program.bundles
                for form in bundle.encodings.forms
            ),
        )
        self.assertTrue(
            all(
                len(item.representative_record)
                >= item.form.pattern.bit_width // 8
                for item in projection.forms
            )
        )
        active_modes = tuple(
            mode
            for mode in self.project.catalog.ea_modes.values()
            if mode.catalog.owner in program.configuration.owners
        )
        self.assertEqual(
            len(projection.ea_forms),
            sum(len(mode["encodings"]) for mode in active_modes),
        )
        self.assertEqual(
            {item.profile for item in projection.ea_forms},
            {mode.catalog.profile for mode in active_modes},
        )
        for item in projection.forms:
            projected_names = tuple(operand.name for operand in item.operands)
            self.assertEqual(
                projected_names,
                tuple(
                    name
                    for name in item.bundle.instruction["operands"]
                    if name in projected_names
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

    def test_declared_entries_are_defined_by_their_instruction_source(self) -> None:
        SailEntryValidator().require(self.compose())

    def test_declared_full_model_artifact_writes_sail_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            registry = ArtifactGeneratorRegistry.discover(self.workspace)
            generator = registry.generator("sail-model")
            artifacts = registry.generate(
                "sail-model", self.workspace, directory
            )
            outputs = ArtifactWriter().write(artifacts, directory)
            output_root = Path(directory).resolve()

            self.assertEqual(artifacts.artifact_id, generator.definition.id)
            self.assertEqual(
                {path.relative_to(output_root) for path in outputs},
                {artifact.relative_path for artifact in artifacts.artifacts},
            )
            for artifact in artifacts.artifacts:
                self.assertEqual(
                    (output_root / artifact.relative_path).read_bytes(),
                    artifact.content
                    if isinstance(artifact.content, bytes)
                    else artifact.content.encode("utf-8"),
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
