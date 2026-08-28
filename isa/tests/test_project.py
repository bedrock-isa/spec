import unittest
from dataclasses import replace
from pathlib import Path

from engine.project import (
    IsaProject,
    SourceCatalog,
    _ExtensionComponents,
)


class IsaProjectTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.isa_root = Path(__file__).parents[1]
        cls.project = IsaProject.load(cls.isa_root)

    def test_loads_complete_declared_corpus(self) -> None:
        bundles = self.project.select()

        self.assertEqual(
            tuple(bundle.reference for bundle in bundles),
            self.project.catalog.instruction_order,
        )
        instruction_sets = (
            self.project.catalog.base,
            *(extension.instruction_set for extension in self.project.catalog.extensions.values()),
        )
        for instruction_set in instruction_sets:
            with self.subTest(owner=instruction_set.catalog.owner):
                self.assertEqual(
                    set(instruction_set.catalog.declared),
                    set(instruction_set.catalog.actual),
                )
                self.assertEqual(
                    tuple(bundle.instruction.mnemonic for bundle in instruction_set.instructions),
                    instruction_set.catalog.declared,
                )
        self.assertEqual(
            self.project.entities.resolve("base.instructions.ADD").latex_label,
            "instr:add",
        )
        self.assertEqual(
            self.project.entities.resolve(
                "base.architecture.overview.section"
            ).latex_label,
            "entity:base-architecture-overview-section",
        )
        self.assertEqual(
            tuple(self.project.events.namespaces),
            ("base", "FP", "FPTRANSA", "VECTOR"),
        )
        self.assertEqual(
            self.project.model.sail_order,
            (
                "base.architectural-types",
                "base.decode-types",
                "base.decode",
                "FP.contract",
                "base.runtime",
                "FP.execution",
                "VECTOR.execution",
                "base.continuations",
                "base.boundary",
                "FPTRANSA.contract",
                "FPTRANSA.execution",
            ),
        )
        document_order = self.project.model.document_order
        self.assertEqual(
            document_order[:20],
            (
                "base.manual.part.architectural-foundations",
                "base.architecture.overview.section",
                "base.architecture.overview.contract-position",
                "base.architecture.overview.manual-scope",
                "base.architecture.overview.profile",
                "base.manual.about.normative-material",
                "base.architecture.terminology.section",
                "base.manual.compatibility.contract",
                "base.manual.compatibility.reserved-fields",
                "base.encoding.instruction.compatibility.reserved-encodings",
                "base.cpuid.compatibility.contract",
                "base.registers.register-model.programming-model",
                "base.registers.register-model.register-model",
                "base.registers.state-register-format-diagrams.flags-and-status-registers",
                "base.registers.state-register-format-diagrams.floating-point-register-model",
                "base.registers.state-register-format-diagrams.fflags-and-fstatus-registers",
                "base.registers.register-model.segment-registers",
                "base.registers.register-model.segment-register-operand-class",
                "base.registers.register-model.control-registers",
                "base.encoding.data.data-formats.data-formats",
            ),
        )
        ordered_landmarks = (
            "base.registers.register-model.programming-model",
            "base.encoding.data.data-formats.data-formats",
            "base.manual.part.encoding-addressing-and-execution",
            "base.memory.translation.page-walk-reference.paging-stage",
            "base.manual.part.system-programming",
            "base.events.event-error-codes.address-context-error-code",
            "base.manual.part.instruction-set-reference",
            "base.instructions.instruction-description-intro.reading-an-instruction-description",
            "base.indexes.reference-navigation.reference-indexes",
            "FP.introduction.common-floating-point-semantics",
            "FPTRANSA.introduction.fptransa-common-model",
            "VECTOR.introduction.element-types-and-assembly-spelling",
        )
        self.assertEqual(
            [document_order.index(reference) for reference in ordered_landmarks],
            sorted(document_order.index(reference) for reference in ordered_landmarks),
        )
        self.assertEqual(
            tuple(self.project.model.extensions), ("FP", "FPTRANSA", "VECTOR")
        )
        self.assertEqual(
            self.project.disclosures.disclosures[0].id, "HIGHER_CPUID_CLASSES"
        )
        self.assertEqual(
            self.project.model.extensions["FP"].source,
            self.isa_root / "extensions/FP/model.yaml",
        )
        self.assertEqual(
            self.project.model.sail_units["base.architectural-types"].sources,
            (
                self.isa_root / "privilege/semantics/privilege.sail",
                self.isa_root / "predication/semantics/predication.sail",
                self.isa_root / "decode/semantics/decode_stage.sail",
                self.isa_root / "commit/semantics/commit_kind.sail",
            ),
        )
        self.assertEqual(
            self.project.model.document_topics[
                "base.architecture.overview.section"
            ].document,
            self.isa_root.parent
            / "artifacts/isa-reference/document/topics/overview/001_section.tex",
        )

    def test_extension_groups_metadata_dependencies_and_instructions(self) -> None:
        extension = self.project.extension("FPTRANSA")

        self.assertEqual(
            extension.name, "Approximate Transcendental Floating-Point Extension"
        )
        self.assertEqual(extension.required_ids, ("FP",))
        self.assertEqual(extension.requires, (self.project.extension("FP"),))
        self.assertIs(extension.requires[0], self.project.extension("FP"))
        self.assertEqual(
            tuple(str(field.reference) for field in extension.required_cpuid_flags),
            (
                "FP.cpuid.EXTENSIONS.DIRECTORY.FEATURES.FP",
                "FPTRANSA.cpuid.EXTENSIONS.DIRECTORY.FEATURES.FPTRANSA",
            ),
        )
        self.assertEqual(extension.instructions[0].reference.owner, "FPTRANSA")
        self.assertIs(extension.types, self.project.types.namespace("FPTRANSA"))

    def test_instruction_bundles_receive_inherited_cpuid_requirements(self) -> None:
        expected = {
            "ADD": (),
            "FADD": ("FP.cpuid.EXTENSIONS.DIRECTORY.FEATURES.FP",),
            "FLOG2A": (
                "FP.cpuid.EXTENSIONS.DIRECTORY.FEATURES.FP",
                "FPTRANSA.cpuid.EXTENSIONS.DIRECTORY.FEATURES.FPTRANSA",
            ),
            "VADD": ("VECTOR.cpuid.EXTENSIONS.DIRECTORY.FEATURES.VECTOR",),
            "VDIV": (
                "VECTOR.cpuid.EXTENSIONS.DIRECTORY.FEATURES.VECTOR",
                "FP.cpuid.EXTENSIONS.DIRECTORY.FEATURES.FP",
            ),
        }

        for mnemonic, references in expected.items():
            with self.subTest(mnemonic=mnemonic):
                bundle = self.project.bundle(mnemonic)
                self.assertEqual(
                    tuple(
                        str(field.reference) for field in bundle.required_cpuid_flags
                    ),
                    references,
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
                "base.cpuid.IMPLEMENTATION.CACHE_TOPOLOGY"
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
