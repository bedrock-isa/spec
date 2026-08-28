import unittest
from pathlib import Path, PurePosixPath

from engine.composition import DocumentComposition
from engine.generation import ArtifactGenerationContext, ArtifactGeneratorRegistry
from engine.project import IsaProject
from engine.site.model import DocumentSiteSpec, build_site
from engine.site.pandoc import normalize_latex_for_site
from engine.site.structure import parse_latex_structure
from engine.workspace import SpecWorkspace


class WebReferenceTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.repository = Path(__file__).parents[2]
        cls.project = IsaProject.load(cls.repository / "isa")
        cls.workspace = SpecWorkspace.from_isa(cls.project)
        cls.registry = ArtifactGeneratorRegistry.discover(cls.workspace)
        context = ArtifactGenerationContext.create(
            cls.workspace, cls.repository / "output"
        )
        documents = (
            ("isa-reference", "tex/isa-reference.tex", "isa", "ISA"),
            ("elf-abi", "tex/bedrock-elf-abi.tex", "elf-abi", "ELF ABI"),
            ("c-abi", "tex/bedrock-c-abi.tex", "c-abi", "C ABI"),
            (
                "c-target-intrinsics",
                "tex/bedrock-target-intrinsics.tex",
                "target-intrinsics",
                "Target Intrinsics",
            ),
        )
        specs = []
        cls.structures = {}
        for artifact_id, output, document_id, title in documents:
            content = (
                cls.registry.generator(artifact_id)
                .generate(context)
                .artifact(output)
                .content
            )
            if not isinstance(content, str):
                raise TypeError(f"{artifact_id}: expected text document")
            structure = parse_latex_structure(content)
            cls.structures[document_id] = structure
            specs.append(
                DocumentSiteSpec(
                    document_id,
                    title,
                    PurePosixPath("downloads") / f"{document_id}.pdf",
                    structure,
                )
            )
        composition = DocumentComposition.load(
            cls.registry.generator("isa-reference").definition.source,
            cls.project,
        )
        cls.site = build_site(tuple(specs), composition)

    def test_web_reference_is_a_current_workspace_artifact(self) -> None:
        generator = self.registry.generator("web-reference")

        self.assertEqual(
            generator.definition.inputs,
            ("isa", "abi.elf", "abi.c", "interfaces.c"),
        )
        self.assertEqual(
            generator.definition.dependencies,
            ("isa-reference", "elf-abi", "c-abi", "c-target-intrinsics"),
        )

    def test_current_documents_preserve_the_site_ownership_contract(self) -> None:
        isa = self.structures["isa"]

        self.assertEqual((len(isa.parts), len(isa.sections)), (4, 21))
        self.assertEqual(len(isa.instructions), 327)
        self.assertEqual(
            tuple(
                len(self.structures[key].sections)
                for key in ("elf-abi", "c-abi", "target-intrinsics")
            ),
            (11, 8, 5),
        )
        self.assertEqual(len(self.site.registry.pages), 382)
        self.assertEqual(len(self.site.registry.targets), 1041)

    def test_current_style_wrappers_are_lowered_at_the_pandoc_boundary(self) -> None:
        normalized = normalize_latex_for_site(
            r"""\begin{document}
\begin{manuallongtable}{ll}A & B\\\end{manuallongtable}
\manualfield{Profile:}{bedrock-elf}
\end{document}
"""
        )

        self.assertNotIn("manuallongtable", normalized)
        self.assertNotIn(r"\manualfield", normalized)
        self.assertEqual(normalized.count(r"\begin{longtable}"), 1)
        self.assertEqual(normalized.count(r"\begin{tabular}"), 1)


if __name__ == "__main__":
    unittest.main()
