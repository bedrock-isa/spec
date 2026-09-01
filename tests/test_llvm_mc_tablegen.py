from __future__ import annotations

from importlib import import_module
from pathlib import Path
import subprocess
import tempfile
import unittest

from engine.encoding import EncodingForm, ExcludedOperandConstraint
from engine.encoding_architecture import ENCODING_CLASSES_BY_WIDTH
from engine.generation import ArtifactDefinition, ArtifactGenerationContext
from engine.project import InstructionBundle, IsaProject
from engine.type_system import (
    ControlRegisterSelectorPayloadType,
    EffectiveAddressFieldType,
    RegisterSelectorPayloadType,
)
from engine.workspace import SpecWorkspace
from engine.yaml_document import YamlDocumentLoader


ROOT = Path(__file__).resolve().parents[1]


class LlvmMcTableGenArtifactTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.workspace = SpecWorkspace.load(ROOT)
        project = cls.workspace.require_provider("isa")
        if not isinstance(project, IsaProject):
            raise TypeError("workspace isa provider must be an IsaProject")
        cls.project = project
        schema = YamlDocumentLoader().mapping(ROOT / "artifacts/schema.yaml")
        definition = ArtifactDefinition.load(
            ROOT / "artifacts/llvm-mc-tablegen/artifact.yaml", schema
        )
        generator_type = import_module("artifacts.llvm-mc-tablegen.generator").Generator
        generator = generator_type(definition)
        generated = generator.generate(
            ArtifactGenerationContext.create(cls.workspace, ROOT)
        )
        cls.projection = generator.projection
        cls.catalog = generated.artifact(definition.outputs["catalog"]).content

    @staticmethod
    def _form_identifier(bundle: InstructionBundle, form: EncodingForm) -> str:
        return f"{bundle.owner}.{bundle.instruction.mnemonic}.{form.id}"

    def test_every_canonical_form_has_one_searchable_record(self) -> None:
        expected = {
            self._form_identifier(bundle, form)
            for bundle in self.project.catalog.instructions.values()
            for form in bundle.encodings.forms
        }
        self.assertEqual({form.identifier for form in self.projection.forms}, expected)

    def test_variable_length_forms_are_not_native_codec_candidates(self) -> None:
        expected: dict[str, bool] = {}
        for bundle in self.project.catalog.instructions.values():
            for form in bundle.encodings.forms:
                field_types = tuple(
                    self.project.types.field_types.resolve(field.type)
                    for field in form.fields
                )
                has_variable_length = any(
                    isinstance(field_type, EffectiveAddressFieldType)
                    for field_type in field_types
                )
                if not has_variable_length:
                    continue
                primary_bytes = ENCODING_CLASSES_BY_WIDTH[
                    form.pattern.bit_width
                ].opcode_space_bytes
                fixed_payload_bytes = sum(
                    self.project.types.payload_types.resolve(payload.type).bytes
                    for payload in form.payloads
                )
                expected[self._form_identifier(bundle, form)] = (
                    not has_variable_length and primary_bytes + fixed_payload_bytes <= 8
                )
        projected = {
            form.identifier: form.tablegen_codec_candidate
            for form in self.projection.forms
            if form.has_variable_length
        }
        self.assertTrue(expected)
        self.assertEqual(projected, expected)

    def test_vector_table_covers_forms_and_projects_alias_policy(self) -> None:
        expected = {
            self._form_identifier(bundle, form): bool(
                dict(bundle.instruction)
                .get("assembly", {})
                .get("width_suffix_aliases", False)
            )
            for bundle in self.project.catalog.instructions.values()
            if bundle.instruction.route == "vector"
            for form in bundle.encodings.forms
        }
        actual = {
            form.identifier: form.has_width_only_aliases
            for form in self.projection.vector_forms
        }
        self.assertEqual(actual, expected)

    def test_scalar_records_reference_canonical_non_vector_forms(self) -> None:
        canonical = {
            self._form_identifier(bundle, form): (bundle, form)
            for bundle in self.project.catalog.instructions.values()
            for form in bundle.encodings.forms
        }
        self.assertTrue(self.projection.scalar_forms)
        for record in self.projection.scalar_forms:
            with self.subTest(identifier=record.identifier):
                bundle, form = canonical[record.identifier]
                self.assertNotEqual(bundle.instruction.route, "vector")
                self.assertEqual(record.pattern, form.pattern.code)
                self.assertEqual(
                    record.fixed_payload_bytes,
                    sum(
                        self.project.types.payload_types.resolve(payload.type).bytes
                        for payload in form.payloads
                    ),
                )

    def test_selector_metadata_comes_from_register_catalogs(self) -> None:
        selector_group_references = {
            payload_type.register_group
            for payload_type in self.project.types.payload_types.values()
            if isinstance(payload_type, RegisterSelectorPayloadType)
        }
        expected_groups = [
            {
                (register.id.lower(), register.encoding)
                for register in self.project.registers.references.groups.resolve(
                    group_reference
                ).registers.values()
                if register.encoding is not None
            }
            for group_reference in selector_group_references
        ]
        if any(
            isinstance(payload_type, ControlRegisterSelectorPayloadType)
            for payload_type in self.project.types.payload_types.values()
        ):
            expected_groups.append(
                {
                    (register.id.lower(), register.selector)
                    for register in self.project.control_registers.references.registers.values()
                }
            )
        actual_groups: dict[int, set[tuple[str, int]]] = {}
        for selector in self.projection.register_selectors:
            actual_groups.setdefault(selector.group, set()).add(
                (selector.name, selector.encoding)
            )
        self.assertCountEqual(list(actual_groups.values()), expected_groups)

    def test_authored_destination_exclusions_reach_scalar_projection(self) -> None:
        canonical = {
            self._form_identifier(bundle, form): form
            for bundle in self.project.catalog.instructions.values()
            for form in bundle.encodings.forms
        }
        scalar_ids = {record.identifier for record in self.projection.scalar_forms}
        constrained = {
            identifier: form
            for identifier, form in canonical.items()
            if identifier in scalar_ids
            and any(
                constraint.role == "dst"
                and isinstance(constraint, ExcludedOperandConstraint)
                and "immediate" in constraint.values
                for constraint in form.constraints
            )
        }
        projected = {
            record.identifier: record
            for record in self.projection.scalar_forms
            if record.identifier in constrained
        }
        self.assertEqual(set(projected), set(constrained))
        for identifier, record in projected.items():
            form = constrained[identifier]
            destination_index = next(
                index
                for index, operand in enumerate(form.syntax.operands)
                if operand.field is not None
                and (binding := form.field_for_marker(operand.field)) is not None
                and binding.role == "dst"
            )
            self.assertFalse(
                record.operands[destination_index].allow_immediate_ea,
                identifier,
            )

    def test_serialized_catalog_is_accepted_by_llvm_tablegen(self) -> None:
        tablegen = ROOT.parent / "llvm-project/build/bin/llvm-tblgen"
        if not tablegen.is_file():
            self.skipTest("workspace llvm-tblgen is unavailable")
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            generated = root / "BedrockGenISACatalog.td"
            generated.write_text(self.catalog, encoding="utf-8")
            source = root / "consume.td"
            source.write_text(
                f'include "llvm/TableGen/SearchableTable.td"\ninclude "{generated}"\n',
                encoding="utf-8",
            )
            completed = subprocess.run(
                [
                    str(tablegen),
                    "-I",
                    str(ROOT.parent / "llvm-project/llvm/include"),
                    "-print-records",
                    str(source),
                ],
                text=True,
                capture_output=True,
                check=False,
            )
        self.assertEqual(completed.returncode, 0, completed.stderr)


if __name__ == "__main__":
    unittest.main()
