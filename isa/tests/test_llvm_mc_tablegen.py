from __future__ import annotations

from importlib import import_module
from pathlib import Path
import re
import unittest

from engine.generation import ArtifactDefinition, ArtifactGenerationContext
from engine.encoding import EncodingForm
from engine.encoding_architecture import ENCODING_CLASSES_BY_WIDTH
from engine.project import InstructionBundle, IsaProject
from engine.reference import Reference
from engine.type_system import FieldTypeKind, PayloadTypeKind
from engine.workspace import SpecWorkspace
from engine.yaml_document import YamlDocumentLoader


ROOT = Path(__file__).resolve().parents[2]


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
        generator_type = import_module(
            "artifacts.llvm-mc-tablegen.generator"
        ).Generator
        generated = generator_type(definition).generate(
            ArtifactGenerationContext.create(cls.workspace, ROOT)
        )
        cls.content = generated.artifact("BedrockGenISACatalog.td").content

    @staticmethod
    def _form_identifier(bundle: InstructionBundle, form: EncodingForm) -> str:
        return f"{bundle.owner}.{bundle.instruction.mnemonic}.{form.id}"

    def test_every_canonical_form_has_one_searchable_record(self) -> None:
        expected = {
            self._form_identifier(bundle, form)
            for bundle in self.project.catalog.instructions.values()
            for form in bundle.encodings.forms
        }
        actual = set(
            re.findall(
                r'^def BRForm_[^ ]+ : BedrockISAForm<\n  "([^"]+)"',
                self.content,
                flags=re.MULTILINE,
            )
        )
        self.assertEqual(actual, expected)

    def test_variable_length_forms_are_not_native_codec_candidates(self) -> None:
        expected: dict[str, bool] = {}
        for bundle in self.project.catalog.instructions.values():
            for form in bundle.encodings.forms:
                field_types = tuple(
                    self.project.types.field_types.resolve(field.type)
                    for field in form.fields
                )
                has_variable_length = any(
                    field_type.kind == FieldTypeKind.EFFECTIVE_ADDRESS
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
                    not has_variable_length
                    and primary_bytes + fixed_payload_bytes <= 8
                )

        projected = {
            identifier: codec_candidate == "1"
            for identifier, has_variable_length, codec_candidate in re.findall(
                r'^def BRForm_[^ ]+ : BedrockISAForm<\n'
                r'  "([^"]+)",[^\n]*\n'
                r'  \d+, \d+, [01], ([01]), ([01]),',
                self.content,
                flags=re.MULTILINE,
            )
            if has_variable_length == "1"
        }

        self.assertTrue(expected)
        self.assertEqual(projected, expected)

    def test_vector_table_covers_forms_and_projects_alias_policy(self) -> None:
        expected_aliases = {
            self._form_identifier(bundle, form): bool(
                dict(bundle.instruction).get("assembly", {}).get(
                    "width_suffix_aliases", False
                )
            )
            for bundle in self.project.catalog.instructions.values()
            if bundle.instruction.route == "vector"
            for form in bundle.encodings.forms
        }
        actual_aliases = {
            identifier: alias == "1"
            for identifier, alias in re.findall(
                r'^def BRForm_vector_[^ ]+ : BedrockVectorEncodingForm<\n'
                r'  "([^"]+)", "[^"]+", "[^"]+", "[^"]*", '
                r'[^,]+, [^,]+, [^,]+, [^,]+, [^,]+, [^,]+, ([01]),',
                self.content,
                flags=re.MULTILINE,
            )
        }
        self.assertEqual(actual_aliases, expected_aliases)

    def test_scalar_records_reference_canonical_non_vector_forms(self) -> None:
        canonical = {
            self._form_identifier(bundle, form): (bundle, form)
            for bundle in self.project.catalog.instructions.values()
            for form in bundle.encodings.forms
        }
        records = re.findall(
            r'^def BRForm_scalar_[^ ]+ : BedrockScalarEncodingForm<\n'
            r'  "([^"]+)", "[^"]+", "([^"]+)", (\d+),',
            self.content,
            flags=re.MULTILINE,
        )
        self.assertTrue(records)
        for identifier, pattern, fixed_payload_bytes in records:
            with self.subTest(identifier=identifier):
                bundle, form = canonical[identifier]
                self.assertNotEqual(bundle.instruction.route, "vector")
                self.assertEqual(pattern, form.pattern.code)
                self.assertEqual(
                    int(fixed_payload_bytes),
                    sum(
                        self.project.types.payload_types.resolve(payload.type).bytes
                        for payload in form.payloads
                    ),
                )

    def test_register_selector_metadata_comes_from_register_catalog(self) -> None:
        selector_group_references = {
            payload_type.register_group
            for payload_type in self.project.types.payload_types.values()
            if payload_type.kind == PayloadTypeKind.REGISTER_SELECTOR
            and payload_type.register_group is not None
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
        actual_groups: dict[int, set[tuple[str, int]]] = {}
        for group, name, encoding in re.findall(
            r'BedrockRegisterSelector<(\d+), "([^"]+)", (\d+)>',
            self.content,
        ):
            actual_groups.setdefault(int(group), set()).add((name, int(encoding)))

        self.assertCountEqual(list(actual_groups.values()), expected_groups)

    def test_extz_destinations_reject_immediate_ea(self) -> None:
        # EXTZ destination constraints are authored ISA rules.  The scalar
        # TableGen operand flag is the external LLVM consumer boundary.
        for mnemonic in ("EXTZW", "EXTZL", "EXTZQ"):
            bundle = self.project.catalog.instructions[
                Reference.parse(f"base.instructions.{mnemonic}")
            ]
            for form in bundle.encodings.forms:
                identifier = self._form_identifier(bundle, form)
                match = re.search(
                    r'^def BRForm_scalar_[^ ]+ : BedrockScalarEncodingForm<\n'
                    rf'  "{re.escape(identifier)}",(?P<arguments>.*?)>;',
                    self.content,
                    flags=re.MULTILINE | re.DOTALL,
                )
                self.assertIsNotNone(match, identifier)
                assert match is not None
                arguments = [
                    identifier,
                    *(
                        value.strip().strip('"')
                        for value in match.group("arguments")
                        .replace("\n", "")
                        .split(",")
                    ),
                ]
                destination_index = next(
                    index
                    for index, operand in enumerate(form.syntax.operands)
                    if operand.field is not None
                    and (binding := form.field_for_marker(operand.field)) is not None
                    and binding.role == "dst"
                )
                self.assertTrue(
                    any(
                        constraint.role == "dst"
                        and "immediate" in constraint.exclude
                        for constraint in form.constraints
                    ),
                    identifier,
                )
                allow_immediate_ea = arguments[10 + destination_index * 10 + 4]
                self.assertEqual(allow_immediate_ea, "0", identifier)


if __name__ == "__main__":
    unittest.main()
