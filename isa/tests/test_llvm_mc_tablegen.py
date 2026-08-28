from __future__ import annotations

from importlib import import_module
from pathlib import Path
import re
import unittest

from engine.generation import ArtifactDefinition, ArtifactGenerationContext
from engine.project import IsaProject
from engine.yaml_document import YamlDocumentLoader


ROOT = Path(__file__).resolve().parents[2]


class LlvmMcTableGenArtifactTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.project = IsaProject.load(ROOT / "isa")
        schema = YamlDocumentLoader().mapping(ROOT / "artifacts/schema.yaml")
        definition = ArtifactDefinition.load(
            ROOT / "artifacts/llvm-mc-tablegen/artifact.yaml", schema
        )
        cls.generator_module = import_module("artifacts.llvm-mc-tablegen.generator")
        generator_type = cls.generator_module.Generator
        generated = generator_type(definition).generate(
            ArtifactGenerationContext.create(cls.project, ROOT)
        )
        cls.content = generated.artifact("BedrockGenISACatalog.td").content

    def test_every_canonical_form_has_one_searchable_record(self) -> None:
        expected = {
            f"{bundle.reference}.{form.id}"
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
        records = [
            record
            for record in self.content.split("\ndef BRForm_")[1:]
            if ": BedrockISAForm<" in record.splitlines()[0]
        ]
        variable = [record for record in records if ", 1, 1, " in record]
        self.assertTrue(variable)
        for record in variable:
            with self.subTest(record=record.splitlines()[0]):
                flags = record.splitlines()[2]
                self.assertIn(", 1, 1, 0,", flags)

    def test_vector_table_covers_forms_and_projects_alias_policy(self) -> None:
        vector = self.project.catalog.extensions["VECTOR"].instructions
        expected_aliases = {
            f"{bundle.reference}.{form.id}": bool(
                dict(bundle.instruction).get("assembly", {}).get(
                    "width_suffix_aliases", False
                )
            )
            for bundle in vector
            for form in bundle.encodings.forms
        }
        actual_aliases = {
            identifier: alias == "1"
            for identifier, alias in re.findall(
                r'^def BRForm_vector_[^ ]+ : BedrockVectorEncodingForm<\n'
                r'  "([^"]+)", "[^"]+", "[^"]+", "[^"]*", '
                r'[^,]+, [^,]+, [^,]+, [^,]+, [^,]+, ([01]),',
                self.content,
                flags=re.MULTILINE,
            )
        }
        self.assertEqual(actual_aliases, expected_aliases)

    def test_scalar_table_covers_every_supported_fixed_form(self) -> None:
        expected = set()
        used_names: set[str] = set()
        for bundle in self.project.catalog.instructions.values():
            if bundle.reference.owner == "VECTOR":
                continue
            for form in bundle.encodings.forms:
                identifier = f"{bundle.reference}.{form.id}"
                rendered = self.generator_module._render_scalar_form(
                    self.project, bundle, form, identifier, used_names
                )
                if rendered is not None:
                    expected.add(identifier)

        actual = set(
            re.findall(
                r'^def BRForm_scalar_[^ ]+ : BedrockScalarEncodingForm<\n'
                r'  "([^"]+)"',
                self.content,
                flags=re.MULTILINE,
            )
        )
        self.assertEqual(actual, expected)
        all_non_vector = {
            f"{bundle.reference}.{form.id}"
            for bundle in self.project.catalog.instructions.values()
            if bundle.reference.owner != "VECTOR"
            for form in bundle.encodings.forms
        }
        self.assertEqual(
            all_non_vector - actual,
            {"base.instructions.REPcc.rn_r_instruction"},
        )

    def test_register_selector_metadata_comes_from_register_catalog(self) -> None:
        self.assertRegex(
            self.content,
            r'BedrockRegisterSelector<\d+, "ptcr", 0>',
        )
        self.assertRegex(
            self.content,
            r'BedrockRegisterSelector<\d+, "cycle", 1>',
        )
        self.assertIn(
            self.generator_module._OPERAND_REGISTER_SELECTOR,
            {
                operand.kind
                for bundle in self.project.catalog.instructions.values()
                for form in bundle.encodings.forms
                for rendered in [
                    self.generator_module._render_scalar_form(
                        self.project,
                        bundle,
                        form,
                        f"{bundle.reference}.{form.id}",
                        set(),
                    )
                ]
                if rendered is not None
                for operand in rendered.operands
            },
        )

    def test_extz_destinations_reject_immediate_ea(self) -> None:
        used_names: set[str] = set()
        for mnemonic in ("EXTZW", "EXTZL", "EXTZQ"):
            bundle = self.project.catalog.instructions[
                f"base.instructions.{mnemonic}"
            ]
            for form in bundle.encodings.forms:
                rendered = self.generator_module._render_scalar_form(
                    self.project,
                    bundle,
                    form,
                    f"{bundle.reference}.{form.id}",
                    used_names,
                )
                self.assertIsNotNone(rendered)
                destination = next(
                    operand
                    for operand, displayed in zip(
                        rendered.operands, form.syntax.displayed_operands
                    )
                    if displayed.field is not None
                    and form.field_for_marker(displayed.field).role == "dst"
                )
                self.assertFalse(destination.allow_immediate_ea)


if __name__ == "__main__":
    unittest.main()
