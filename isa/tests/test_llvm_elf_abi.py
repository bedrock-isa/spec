from __future__ import annotations

from importlib import import_module
from pathlib import Path
import re
from types import SimpleNamespace
import unittest

from abi.elf.model import RelocationMetasyntax
from engine.generation import ArtifactDefinition, ArtifactGenerationContext
from engine.project import IsaProject
from engine.workspace import SpecWorkspace
from engine.yaml_document import YamlDocumentLoader


ROOT = Path(__file__).resolve().parents[2]


class LlvmElfAbiArtifactTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.isa = IsaProject.load(ROOT / "isa")
        cls.workspace = SpecWorkspace.from_isa(cls.isa)
        cls.elf = cls.workspace.require_provider("abi.elf")
        schema = YamlDocumentLoader().mapping(ROOT / "artifacts/schema.yaml")
        definition = ArtifactDefinition.load(
            ROOT / "artifacts/llvm-elf-abi/artifact.yaml", schema
        )
        cls.generator_module = import_module("artifacts.llvm-elf-abi.generator")
        generated = cls.generator_module.Generator(definition).generate(
            ArtifactGenerationContext.create(cls.workspace, ROOT)
        )
        cls.relocations = generated.artifact("ELFRelocs/Bedrock.def").content
        cls.catalog = generated.artifact("BedrockGenELFABI.inc").content

    def test_elf_relocation_definition_covers_the_numeric_catalog(self) -> None:
        actual = {
            name: int(value)
            for name, value in re.findall(
                r"^ELF_RELOC\((R_BEDROCK_[A-Z0-9_]+), ([0-9]+)\)$",
                self.relocations,
                flags=re.MULTILINE,
            )
        }
        expected = {
            relocation.id: relocation.value
            for relocation in self.elf.relocations.values()
        }
        self.assertEqual(actual, expected)

    def test_metadata_covers_every_relocation_and_lld_expression(self) -> None:
        records = re.findall(
            r"^BEDROCK_ELF_RELOCATION\((R_BEDROCK_[A-Z0-9_]+), "
            r"([0-9]+), ([A-Z0-9_]+), ([A-Z0-9_]+), ([0-9]+), "
            r"([01]), ([A-Z0-9_]+),",
            self.catalog,
            flags=re.MULTILINE,
        )
        self.assertEqual(len(records), len(self.elf.relocations))
        by_name = {record[0]: record for record in records}
        self.assertEqual(by_name["R_BEDROCK_CALL32S"][6], "PC")
        self.assertEqual(by_name["R_BEDROCK_TLSDESC"][6], "TLSDESC")
        self.assertEqual(by_name["R_BEDROCK_ABS32S"][4:6], ("32", "1"))

    def test_relocation_fields_use_authored_type_ids(self) -> None:
        actual = dict(
            re.findall(
                r'^BEDROCK_ELF_RELOCATION\((R_BEDROCK_[A-Z0-9_]+), '
                r'.*, "([A-Z0-9_]*)"\)$',
                self.catalog,
                flags=re.MULTILINE,
            )
        )
        expected = {
            relocation.id: (
                self.workspace.resolve(relocation.field).id
                if relocation.field
                else ""
            )
            for relocation in self.elf.relocations.values()
        }
        self.assertEqual(actual, expected)

    def test_relaxation_edges_come_from_the_catalog(self) -> None:
        actual = set(
            re.findall(
                r"^BEDROCK_ELF_RELAXATION\((R_BEDROCK_[A-Z0-9_]+), "
                r"(R_BEDROCK_[A-Z0-9_]+)\)$",
                self.catalog,
                flags=re.MULTILINE,
            )
        )
        expected = {
            (relocation.id, target.element)
            for relocation in self.elf.relocations.values()
            for target in relocation.relaxations
        }
        self.assertEqual(actual, expected)

    def test_code_tls_and_linkage_inventories_are_projected(self) -> None:
        for model in self.elf.code_models.values():
            self.assertIn(f"BEDROCK_ELF_CODE_MODEL({model.id},", self.catalog)
        for model in self.elf.tls_models.values():
            self.assertIn(f"BEDROCK_ELF_TLS_MODEL({model.id},", self.catalog)
        for protocol in self.elf.linkage_protocols.values():
            self.assertIn(
                f"BEDROCK_ELF_LINKAGE_PROTOCOL({protocol.id})", self.catalog
            )
        self.assertIn(
            "BEDROCK_ELF_LINKAGE_PROPERTY(ORDINARY_PLT, ENTRY_SIZE_BYTES, 32)",
            self.catalog,
        )
        self.assertIn(
            "BEDROCK_ELF_TLS_PROPERTY(TLSDESC, DESCRIPTOR_SIZE_BYTES, 16)",
            self.catalog,
        )

    def test_debug_register_inventory_is_projected_completely(self) -> None:
        ranges = set(
            re.findall(
                r"^BEDROCK_ELF_DEBUG_REGISTER_RANGE\(([A-Z0-9_]+),",
                self.catalog,
                flags=re.MULTILINE,
            )
        )
        assignments = self.elf.resolved_debug_registers(self.workspace)
        expected_ranges = {
            f"RESERVED_{item.first}" if item.status == "reserved" else item.group
            for item in assignments
        }
        self.assertEqual(ranges, expected_ranges)
        mappings = re.findall(
            r"^BEDROCK_ELF_DEBUG_REGISTER_MAPPING\(([A-Z0-9_]+), "
            r"([0-9]+), ([A-Z][A-Z0-9]+)\)$",
            self.catalog,
            flags=re.MULTILINE,
        )
        self.assertEqual(
            len(mappings),
            sum(len(item.registers) for item in assignments),
        )
        self.assertIn(("SPECIAL", "16", "SP"), mappings)
        self.assertIn(("VECTOR", "95", "V31"), mappings)

    def test_entry_state_inventory_is_projected_completely(self) -> None:
        state = self.elf.process_entry
        self.assertIn(
            f"BEDROCK_ELF_ENTRY_STATE({state.entry_point.local.element},",
            self.catalog,
        )
        for permission in state.stack_permissions:
            self.assertIn(
                f"BEDROCK_ELF_ENTRY_STACK_PERMISSION({permission.upper()})",
                self.catalog,
            )
        for role, register in state.segment_contexts.items():
            self.assertIn(
                f"BEDROCK_ELF_ENTRY_SEGMENT_CONTEXT("
                f"{role.upper()}, {register.local.element})",
                self.catalog,
            )

    def test_lld_expression_mapping_uses_the_parsed_ast(self) -> None:
        relocation = SimpleNamespace(
            id="R_BEDROCK_EQUIVALENT",
            source=Path("equivalent.yaml"),
            calculation=RelocationMetasyntax.parse(
                "(symbol + addend) - place"
            ),
        )
        self.assertEqual(self.generator_module._lld_expression(relocation), "PC")

    def test_unmapped_calculation_is_rejected(self) -> None:
        relocation = SimpleNamespace(
            id="R_BEDROCK_FUTURE",
            source=Path("future.yaml"),
            calculation=RelocationMetasyntax.parse("symbol - addend"),
        )
        with self.assertRaisesRegex(ValueError, "no LLVM/LLD expression mapping"):
            self.generator_module._lld_expression(relocation)


if __name__ == "__main__":
    unittest.main()
