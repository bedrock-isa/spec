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
        cls.workspace = SpecWorkspace.load(cls.repository)
        cls.project = cls.workspace.require_provider("isa")
        if not isinstance(cls.project, IsaProject):
            raise TypeError("workspace isa provider must be an IsaProject")
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

    def test_navigation_projects_each_owned_page_once(self) -> None:
        def outputs(entries: list[dict[str, object]]) -> list[str]:
            projected: list[str] = []
            for entry in entries:
                value = next(iter(entry.values()))
                if isinstance(value, str):
                    projected.append(value)
                elif isinstance(value, list):
                    projected.extend(outputs(value))
                else:
                    self.fail(f"unexpected navigation entry: {entry!r}")
            return projected

        projected = outputs(self.site.navigation())
        owned = [page.output.as_posix() for page in self.site.registry.pages]

        self.assertEqual(sorted(projected), sorted(owned))

    def test_current_style_wrappers_are_lowered_at_the_pandoc_boundary(self) -> None:
        normalized = normalize_latex_for_site(
            r"""\begin{document}
\begin{BedrockLongTable}{ll}A & B\\\end{BedrockLongTable}
\BedrockField{Profile:}{bedrock-elf}
\end{document}
"""
        )

        self.assertNotIn("BedrockLongTable", normalized)
        self.assertNotIn(r"\BedrockField", normalized)
        self.assertEqual(normalized.count(r"\begin{longtable}"), 1)
        self.assertEqual(normalized.count(r"\begin{tabular}"), 1)


if __name__ == "__main__":
    unittest.main()
