import unittest
from dataclasses import replace
from pathlib import Path
import tempfile

from engine.model import SailUnit
from engine.project import IsaProject
from engine.reference import Reference
from engine.sail import (
    ArtifactWriter,
    IsaConfiguration,
    SailComposer,
    SailCatalogRenderer,
    SailDispatchRenderer,
    SailEntryValidator,
    ArtifactGeneratorRegistry,
    SailProjectRenderer,
    SailRegistryRenderer,
)
from engine.workspace import SpecWorkspace


class SailCompositionTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.workspace = SpecWorkspace.load(Path(__file__).parents[2])
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
        with self.assertRaisesRegex(ValueError, "unknown extension"):
            IsaConfiguration.resolve(self.project, ("DOES_NOT_EXIST",))

    def test_extension_selection_closes_declared_dependencies(self) -> None:
        program = self.compose(("FPTRANSA",))
        registry = SailRegistryRenderer().render(program)

        self.assertEqual(program.configuration.extension_ids, ("FP", "FPTRANSA"))
        self.assertEqual(
            program.bundles,
            tuple(
                bundle
                for bundle in self.project.select()
                if bundle.reference.owner in {"base", "FP", "FPTRANSA"}
            ),
        )
        self.assertIn("Op_FADD", registry)
        self.assertIn("Op_FLOG2A", registry)
        self.assertNotIn("Op_VADD", registry)
        self.assertNotIn("RouteVector", registry)

    def test_registry_derives_route_from_instruction_owner(self) -> None:
        registry = SailRegistryRenderer().render(self.compose(()))

        self.assertIn("Op_ADD => RouteIntegerAlu", registry)
        self.assertIn("BaseSet", registry)
        self.assertNotIn("RouteFpu", registry)
        self.assertNotIn("FloatingPointFault", registry)
        self.assertNotIn("RouteVector", registry)

    def test_registry_adds_types_only_for_active_extensions(self) -> None:
        fptransa = SailRegistryRenderer().render(self.compose(("FPTRANSA",)))
        vector = SailRegistryRenderer().render(self.compose(("VECTOR",)))

        self.assertIn("FpuSet", fptransa)
        self.assertIn("FpuTranscendentalSet", fptransa)
        self.assertIn("FloatingPointFault", fptransa)
        self.assertIn("TranscendentalCompute", fptransa)
        self.assertNotIn("VectorRangeFault", fptransa)
        self.assertIn("VectorSet", vector)
        self.assertIn("VectorRangeFault", vector)
        self.assertNotIn("VectorFpuSet", vector)
        self.assertNotIn("FloatingPointFault", vector)

    def test_registry_projects_only_active_leaf_events(self) -> None:
        base = SailRegistryRenderer().render(self.compose(()))
        fp = SailRegistryRenderer().render(self.compose(("FP",)))
        vector = SailRegistryRenderer().render(self.compose(("VECTOR",)))

        self.assertIn("Event_PAGE_PERMISSION_VIOLATION", base)
        self.assertIn(
            "Event_PAGE_PERMISSION_VIOLATION => Some(0x000021)", base
        )
        self.assertNotIn("Event_FLOATING_POINT_EXCEPTION", base)
        self.assertIn("Event_FLOATING_POINT_EXCEPTION", fp)
        self.assertNotIn("Event_VECTOR_LANE_INDEX_OUT_OF_RANGE", fp)
        self.assertIn("Event_VECTOR_LANE_INDEX_OUT_OF_RANGE", vector)
        self.assertNotIn("Event_FLOATING_POINT_EXCEPTION", vector)

    def test_dispatch_projects_each_instruction_entry(self) -> None:
        program = self.compose()
        dispatch = SailDispatchRenderer().render(program)

        for semantics in program.instruction_semantics:
            self.assertIn(
                f"{semantics.operation} => match {semantics.entry}(instruction, state)",
                dispatch,
                semantics.bundle.reference,
            )

    def test_catalog_projects_every_form_and_representative_record(self) -> None:
        catalog = SailCatalogRenderer().render(self.compose())
        primary, remainder = catalog.split(
            "let effective_address_catalog_cache", 1
        )
        effective_address, representatives = remainder.split(
            "let representative_form_records_cache", 1
        )

        form_count = sum(len(bundle.encodings.forms) for bundle in self.compose().bundles)
        self.assertEqual(primary.count("  struct { form_id = Form_"), form_count)
        self.assertIn("  struct { name = EaForm_", effective_address)
        self.assertEqual(
            representatives.count("  struct { form_id = Form_"), form_count
        )
        self.assertIn(
            "form_id = Form_short_abs_l_q_z_rn_r, bytes = [|0xA8, 0x40|]",
            representatives,
        )

    def test_ea_catalog_projects_only_active_owner_profiles(self) -> None:
        base = SailCatalogRenderer().render(self.compose(()))
        fp = SailCatalogRenderer().render(self.compose(("FP",)))
        vector = SailCatalogRenderer().render(self.compose(("VECTOR",)))

        self.assertIn("profile = Some(EaProfile_ea)", base)
        self.assertNotIn("profile = Some(EaProfile_fea)", base)
        self.assertNotIn("profile = Some(EaProfile_vea)", base)
        self.assertIn("profile = Some(EaProfile_fea)", fp)
        self.assertNotIn("profile = Some(EaProfile_vea)", fp)
        self.assertIn("profile = Some(EaProfile_vea)", vector)
        self.assertNotIn("profile = Some(EaProfile_fea)", vector)
        self.assertIn(
            "update_difference = Some(EaUpdateDifference_scale)", base
        )
        self.assertNotIn("EaUpdateDifference_vlen_bytes", base)
        self.assertNotIn("EaUpdateDifference_element_count", base)
        self.assertIn("EaUpdateDifference_vlen_bytes", vector)
        self.assertIn("EaUpdateDifference_element_count", vector)

        base_registry = SailRegistryRenderer().render(self.compose(()))
        fp_registry = SailRegistryRenderer().render(self.compose(("FP",)))
        vector_registry = SailRegistryRenderer().render(self.compose(("VECTOR",)))
        self.assertNotIn("EaProfile_fea", base_registry)
        self.assertNotIn("EaProfile_vea", base_registry)
        self.assertIn("EaProfile_fea", fp_registry)
        self.assertNotIn("EaProfile_vea", fp_registry)
        self.assertIn("EaProfile_vea", vector_registry)
        self.assertNotIn("EaProfile_fea", vector_registry)

    def test_catalog_binds_fixed_sp_by_operand_role(self) -> None:
        catalog = SailCatalogRenderer().render(self.compose())
        add = next(
            line
            for line in catalog.splitlines()
            if "form_id = Form_short_add_q_imm8_i_sp" in line
            and "operands =" in line
        )

        self.assertIn(
            "name = Operand_dst, operand_type = OperandType_SP, access = AccessReadWrite",
            add,
        )
        self.assertNotIn("name = Operand_src", add)

    def test_registry_declares_generated_catalog_identifiers(self) -> None:
        registry = SailRegistryRenderer().render(self.compose())

        self.assertIn("enum Form_id = Form_invalid", registry)
        self.assertIn("enum Field_id = Field_a", registry)
        self.assertIn("CpuidFlag_FPTRANSA", registry)

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

    def test_project_renderer_preserves_multi_source_unit_order(self) -> None:
        program = self.compose(())
        unit = SailUnit(
            owner="base",
            id="sample",
            reference=Reference.parse("base.sample"),
            source=self.project.root / "model.yaml",
            sources=(
                self.project.root / "privilege/semantics/privilege.sail",
                self.project.root / "predication/semantics/predication.sail",
            ),
            requires=(),
        )
        rendered = SailProjectRenderer().render(
            replace(program, sail_units=(unit,)), self.project.root
        )

        self.assertIn(
            "files\n"
            "    privilege/semantics/privilege.sail,\n"
            "    predication/semantics/predication.sail",
            rendered,
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

            with self.assertRaisesRegex(
                ValueError, program.instruction_semantics[0].entry
            ):
                SailEntryValidator().require(bad_program)


if __name__ == "__main__":
    unittest.main()
