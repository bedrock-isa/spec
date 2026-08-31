import unittest
from dataclasses import replace
from pathlib import Path

from engine.project import (
    IsaProject,
    SourceCatalog,
    _ExtensionComponents,
)
from engine.reference import Reference


class IsaProjectTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.isa_root = Path(__file__).parents[1]
        cls.project = IsaProject.load(cls.isa_root)

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

    def test_cpuid_requirements_reject_unknown_and_non_flag_fields(self) -> None:
        fp = self.project.extension("FP").metadata
        cases = (
            (
                replace(
                    fp,
                    required_cpuid_flags=(
                        "FP.cpuid.EXTENSIONS.DIRECTORY.FEATURES.UNKNOWN",
                    ),
                ),
                "unknown CPUID flag reference",
            ),
            (
                replace(
                    fp,
                    required_cpuid_flags=(
                        "base.cpuid.BASE.IDENTITY.IDENTITY.IMPLEMENTATION_ID",
                    ),
                ),
                "names a 32-bit field",
            ),
        )

        for metadata, message in cases:
            with (
                self.subTest(message=message),
                self.assertRaisesRegex(ValueError, message),
            ):
                SourceCatalog._resolve_cpuid_requirements(
                    {"FP": metadata}, ("FP",), self.project.cpuid
                )

    def test_cpuid_requirements_reject_repeated_inherited_flags(self) -> None:
        fp = self.project.extension("FP").metadata
        fptransa = replace(
            self.project.extension("FPTRANSA").metadata,
            required_cpuid_flags=("FP.cpuid.EXTENSIONS.DIRECTORY.FEATURES.FP",),
        )

        with self.assertRaisesRegex(ValueError, "repeats an inherited requirement"):
            SourceCatalog._resolve_cpuid_requirements(
                {"FP": fp, "FPTRANSA": fptransa},
                ("FP", "FPTRANSA"),
                self.project.cpuid,
            )

    def test_exposes_cpuid_as_an_independent_project_catalog(self) -> None:
        self.assertEqual(self.project.cpuid.base.owner, "base")
        self.assertIs(
            self.project.cpuid.references.leaves[
                Reference.parse("base.cpuid.IMPLEMENTATION.CACHE_TOPOLOGY")
            ],
            self.project.cpuid.base.classes["IMPLEMENTATION"].leaves["CACHE_TOPOLOGY"],
        )

    def test_rejects_unknown_extension(self) -> None:
        with self.assertRaisesRegex(ValueError, "unknown extension"):
            self.project.extension("DOESNOTEXIST")

    def test_resolves_dependencies_independently_of_declaration_order(self) -> None:
        components = {
            extension.id: _ExtensionComponents(
                extension.metadata, extension.types, extension.instruction_set
            )
            for extension in self.project.catalog.extensions.values()
        }

        resolved = SourceCatalog._resolve_extensions(
            components, ("FPTRANSA", "VECTOR", "FP")
        )

        self.assertIs(resolved["FPTRANSA"].requires[0], resolved["FP"])
        self.assertEqual(tuple(resolved), ("FPTRANSA", "VECTOR", "FP"))

    def test_rejects_circular_extension_dependencies(self) -> None:
        fp = self.project.extension("FP")
        fptransa = self.project.extension("FPTRANSA")
        components = {
            "FP": _ExtensionComponents(
                replace(fp.metadata, requires=("FPTRANSA",)),
                fp.types,
                fp.instruction_set,
            ),
            "FPTRANSA": _ExtensionComponents(
                fptransa.metadata,
                fptransa.types,
                fptransa.instruction_set,
            ),
        }

        with self.assertRaisesRegex(ValueError, "FP -> FPTRANSA -> FP"):
            SourceCatalog._resolve_extensions(components, ("FP", "FPTRANSA"))

    def test_resolves_mnemonic_reference_and_source_path(self) -> None:
        by_name = self.project.bundle("VADD")
        by_reference = self.project.bundle("VECTOR.instructions.VADD")
        by_path = self.project.bundle(
            self.isa_root
            / "extensions/VECTOR/instructions/definitions/VADD/encodings.yaml"
        )

        self.assertIs(by_name, by_reference)
        self.assertIs(by_name, by_path)

    def test_select_deduplicates_without_reordering_targets(self) -> None:
        selected = self.project.select(("ADD", "SUB", "ADD"))
        self.assertEqual(
            [bundle.instruction.mnemonic for bundle in selected], ["ADD", "SUB"]
        )

    def test_rejects_unknown_instruction(self) -> None:
        with self.assertRaisesRegex(ValueError, "unknown instruction"):
            self.project.bundle("DOESNOTEXIST")


if __name__ == "__main__":
    unittest.main()
