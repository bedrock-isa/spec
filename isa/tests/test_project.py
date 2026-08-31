import unittest
from contextlib import contextmanager
from pathlib import Path
import shutil
import tempfile

import yaml

from engine.project import (
    CpuidFlagWidthError,
    ExtensionDependencyCycleError,
    IsaProject,
    ProjectLookupError,
    ProjectLookupReason,
    RepeatedCpuidRequirementError,
    UnknownCpuidFlagError,
)
from engine.reference import Reference


class IsaProjectTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.isa_root = Path(__file__).parents[1]
        cls.project = IsaProject.load(cls.isa_root)

    @contextmanager
    def project_fixture(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "isa"
            shutil.copytree(self.isa_root, root)
            shutil.copytree(
                self.isa_root.parent / "artifacts/isa-reference/document",
                root.parent / "artifacts/isa-reference/document",
            )
            yield root

    @staticmethod
    def update_extension(root: Path, extension_id: str, **updates: object) -> None:
        source = root / "extensions" / extension_id / "extension.yaml"
        document = yaml.safe_load(source.read_text(encoding="utf-8"))
        document.update(updates)
        source.write_text(
            yaml.safe_dump(document, sort_keys=False), encoding="utf-8"
        )

    def test_extension_projects_owner_declared_dependencies(self) -> None:
        extension = self.project.extension("FPTRANSA")

        self.assertEqual(
            tuple(required.id for required in extension.requires),
            extension.metadata.requires,
        )
        inherited_fields = tuple(
            field
            for required in extension.requires
            for field in required.required_cpuid_flags
        )
        direct_fields = tuple(
            self.project.cpuid.references.fields[Reference.parse(reference)]
            for reference in extension.metadata.required_cpuid_flags
        )
        self.assertEqual(
            extension.required_cpuid_flags,
            (*inherited_fields, *direct_fields),
        )
        self.assertIs(extension.types, self.project.types.namespace("FPTRANSA"))

    def test_instruction_bundles_receive_owner_cpuid_requirements(self) -> None:
        owner_requirements = {
            "base": (),
            **{
                extension.id: extension.required_cpuid_flags
                for extension in self.project.catalog.extensions.values()
            },
        }

        for bundle in self.project.select():
            with self.subTest(reference=bundle.reference):
                self.assertEqual(
                    bundle.required_cpuid_flags,
                    owner_requirements[bundle.owner],
                )

    def test_rejects_unknown_extension(self) -> None:
        with self.assertRaises(ProjectLookupError) as caught:
            self.project.extension("DOESNOTEXIST")
        self.assertIs(caught.exception.reason, ProjectLookupReason.UNKNOWN_EXTENSION)

    def test_rejects_unknown_cpuid_requirement_through_public_load(self) -> None:
        reference = "FP.cpuid.EXTENSIONS.DIRECTORY.FEATURES.UNKNOWN"
        with self.project_fixture() as root:
            self.update_extension(root, "FP", required_cpuid_flags=[reference])
            with self.assertRaises(UnknownCpuidFlagError) as caught:
                IsaProject.load(root)

        self.assertEqual(caught.exception.reference, Reference.parse(reference))

    def test_rejects_non_flag_cpuid_requirement_through_public_load(self) -> None:
        reference = "base.cpuid.BASE.IDENTITY.IDENTITY.IMPLEMENTATION_ID"
        with self.project_fixture() as root:
            self.update_extension(root, "FP", required_cpuid_flags=[reference])
            with self.assertRaises(CpuidFlagWidthError) as caught:
                IsaProject.load(root)

        self.assertEqual(caught.exception.field.reference, Reference.parse(reference))
        self.assertNotEqual(caught.exception.field.bits, 1)

    def test_rejects_repeated_inherited_cpuid_requirement(self) -> None:
        reference = "FP.cpuid.EXTENSIONS.DIRECTORY.FEATURES.FP"
        with self.project_fixture() as root:
            self.update_extension(root, "FPTRANSA", required_cpuid_flags=[reference])
            with self.assertRaises(RepeatedCpuidRequirementError) as caught:
                IsaProject.load(root)

        self.assertEqual(caught.exception.field.reference, Reference.parse(reference))

    def test_resolves_dependencies_independently_of_declaration_order(self) -> None:
        with self.project_fixture() as root:
            inventory = root / "extensions/extensions.yaml"
            document = yaml.safe_load(inventory.read_text(encoding="utf-8"))
            document["extensions"] = ["FPTRANSA", "FP", "VECTOR", "VECTORFP"]
            inventory.write_text(
                yaml.safe_dump(document, sort_keys=False), encoding="utf-8"
            )
            project = IsaProject.load(root)

        self.assertIs(
            project.extension("FPTRANSA").requires[0],
            project.extension("FP"),
        )

    def test_rejects_circular_extension_dependencies_through_public_load(self) -> None:
        with self.project_fixture() as root:
            self.update_extension(root, "FP", requires=["FPTRANSA"])
            with self.assertRaises(ExtensionDependencyCycleError) as caught:
                IsaProject.load(root)

        self.assertEqual(caught.exception.cycle, ("FP", "FPTRANSA", "FP"))

    def test_resolves_mnemonic_reference_and_source_path(self) -> None:
        expected = self.project.select()[0]
        by_name = self.project.bundle(expected.instruction.mnemonic)
        by_reference = self.project.bundle(expected.reference)
        by_path = self.project.bundle(expected.encodings.source)

        self.assertIs(expected, by_name)
        self.assertIs(expected, by_reference)
        self.assertIs(expected, by_path)

    def test_select_deduplicates_without_reordering_targets(self) -> None:
        first, second = self.project.select()[:2]
        selected = self.project.select(
            (first.reference, second.reference, first.reference)
        )
        self.assertEqual(selected, (first, second))

    def test_rejects_unknown_instruction(self) -> None:
        with self.assertRaises(ProjectLookupError) as caught:
            self.project.bundle("DOESNOTEXIST")
        self.assertIs(caught.exception.reason, ProjectLookupReason.UNKNOWN_INSTRUCTION)


if __name__ == "__main__":
    unittest.main()
