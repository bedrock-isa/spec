import unittest
import json
from pathlib import Path
import re
import tempfile

import yaml

from engine.composition import (
    DocumentComposition,
    InstructionSetBlock,
    TermGroupBlock,
    TopicBlock,
)
from engine.document import TexValidator
from engine.generation import (
    ArtifactGenerationContext,
    ArtifactGeneratorRegistry,
)
from engine.project import IsaProject
from engine.render import (
    DocumentFragmentContext,
    DocumentFragmentPipeline,
    DocumentFragmentProvider,
    LatexSemanticTextRenderer,
    LatexSourcePreprocessor,
    rewrite_direct_terms,
)


class _SampleFragmentProvider(DocumentFragmentProvider):
    @property
    def placeholders(self) -> frozenset[str]:
        return frozenset(("@sample@",))

    def expand(self, text: str, context: DocumentFragmentContext) -> str:
        return text.replace("@sample@", str(len(context.project.select())))


class DocumentTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.root = Path(__file__).parents[1].resolve()
        cls.repository = cls.root.parent
        cls.project = IsaProject.load(cls.root)
        cls.composition = DocumentComposition.load(
            cls.repository / "artifacts/isa-reference/artifact.yaml", cls.project
        )
        cls.generator = ArtifactGeneratorRegistry.discover(cls.project).generator(
            "isa-reference"
        )

    def test_composition_covers_every_topic_and_instruction_owner(self) -> None:
        topics = []
        owners = []
        term_groups = []
        for block in self.composition.blocks:
            if isinstance(block, TopicBlock):
                topics.append(block.topic.reference)
            elif isinstance(block, TermGroupBlock):
                term_groups.append(block.group.reference)
            elif isinstance(block, InstructionSetBlock):
                owners.append(block.owner)
                topics.extend(topic.reference for topic in block.introduction)

        topic_references = tuple(map(str, topics))
        self.assertEqual(len(topic_references), len(set(topic_references)))
        self.assertEqual(set(topic_references), set(self.project.model.document_order))
        self.assertEqual(
            tuple(map(str, term_groups)),
            (
                "base.term_groups.address_values",
                "base.term_groups.memory_behavior",
                "base.term_groups.segmentation_and_paging",
                "base.term_groups.instruction_encoding",
                "base.term_groups.control_flow",
                "base.term_groups.tracing",
                "base.term_groups.architectural_state",
                "base.term_groups.architectural_exceptions",
                "FP.term_groups.floating_point_and_exceptions",
                "VECTOR.term_groups.vector_architectural_state",
                "base.term_groups.compatibility",
            ),
        )
        self.assertEqual(owners, ["base", *self.project.catalog.extensions])

    def test_base_reader_sources_do_not_define_extension_domains(self) -> None:
        forbidden = re.compile(
            r"\b(?:FPTRANSA|FEA|VEA|FFLAGS|FSTATUS|VLEN|VECTOR)\b"
            r"|floating[- ]point|scalable[- ]vector|predicate register",
            re.IGNORECASE,
        )
        semantic_reference = re.compile(r"\(:(?:ref|term):(FP|FPTRANSA|VECTOR)\.")
        violations = []
        for path in self.root.rglob("*.tex"):
            relative = path.relative_to(self.root)
            if relative.parts[0] in {"extensions", "indexes"}:
                continue
            text = path.read_text(encoding="utf-8")
            if forbidden.search(text) or semantic_reference.search(text):
                violations.append(str(relative))
        self.assertEqual(violations, [])

    def test_generator_renders_complete_tex_without_writing(self) -> None:
        self.assertEqual(type(self.generator).__module__, "_bedrock_artifact_isa_reference")
        artifact = self.generator.generate(
            ArtifactGenerationContext.create(self.project, self.root / "output")
        ).artifact(
            "tex/isa-reference.tex"
        )

        bundles = self.project.select()
        form_count = sum(len(bundle.encodings.forms) for bundle in bundles)
        self.assertEqual(
            artifact.content.count("% topic:"),
            len(self.project.model.document_order),
        )
        self.assertEqual(
            artifact.content.count("% term-group:"),
            len(self.project.terminology.references.groups),
        )
        self.assertEqual(
            artifact.content.count("% instruction-set:"),
            1 + len(self.project.catalog.extensions),
        )
        self.assertEqual(
            artifact.content.count(r"\begin{manualinstruction}"), len(bundles)
        )
        self.assertEqual(artifact.content.count("Allocation pattern:"), form_count)
        self.assertEqual(artifact.content.count(r"\begin{document}"), 1)
        self.assertEqual(artifact.content.count(r"\end{document}"), 1)
        self.assertIn("Architectural Leaf Event Contracts", artifact.content)
        self.assertIn("INVALID\\_\\allowbreak{}OPCODE", artifact.content)
        self.assertNotIn(r"\BedrockGeneratedEventCodeReference", artifact.content)
        self.assertIn("Implementation-Defined Disclosure Register", artifact.content)
        self.assertNotIn(
            r"\BedrockGeneratedImplementationDisclosures", artifact.content
        )
        self.assertIn(r"\subsection{Address Values}", artifact.content)
        self.assertIn(r"\label{term:base-terms-effective-address}", artifact.content)
        self.assertIn(r"\emph{effective address (EA)}", artifact.content)
        self.assertIn(r"\subsection{Architectural State}", artifact.content)
        self.assertIn(r"\subsection{Compatibility}", artifact.content)
        self.assertNotIn(r"\manualeaadditivememoryflow", artifact.content)
        self.assertNotIn(r"\manualeaindexedmemoryflow", artifact.content)
        self.assertNotIn("Compact Effective-Address Field", artifact.content)
        self.assertNotIn("EXT2 Explicit Segment Base Auto-Update", artifact.content)
        self.assertNotIn("EXT2 SP/PC Indexed", artifact.content)
        self.assertIn("Postincrement Address Generation", artifact.content)
        self.assertIn("Predecrement Address Generation", artifact.content)
        self.assertIn("updateopfeedbackout", artifact.content)
        self.assertIn(
            r"\BedrockEAProfileTitle{FP FEA Compact Floating-Point Immediate}",
            artifact.content,
        )
        self.assertIn(
            r"\BedrockEAProfileTitle{VECTOR VEA EXT2 Explicit-Segment Indexed / Plain}",
            artifact.content,
        )
        self.assertNotIn(r"\input{isa/", artifact.content)
        self.assertIn(
            "% begin input: artifacts/_shared/latex/bedrock-reference-common.tex",
            artifact.content,
        )
        self.assertIn(
            r"\label{entity:base-architecture-overview-section}",
            artifact.content,
        )
        graph = json.loads(
            self.generator.generate(
                ArtifactGenerationContext.create(self.project, self.root / "output")
            ).artifact("graphs/isa-reference-dependencies.json").content
        )
        self.assertTrue(graph["nodes"])
        self.assertTrue(graph["edges"])
        node_ids = {node["reference"] for node in graph["nodes"]}
        self.assertTrue(
            all(
                edge["source"] in node_ids
                and edge["target"] in node_ids
                and edge["occurrences"] > 0
                for edge in graph["edges"]
            )
        )
        self.assertTrue(any(edge["kind"] == "reference" for edge in graph["edges"]))
        for entity in self.project.entities.references.values():
            if entity.latex_label is None or entity.kind.value == "instruction":
                continue
            with self.subTest(reference=str(entity.reference)):
                self.assertEqual(
                    artifact.content.count(rf"\label{{{entity.latex_label}}}"),
                    1,
                )

    def test_source_preprocessor_expands_inputs_and_term_escapes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repository = Path(directory)
            source_root = repository / "isa"
            source_root.mkdir()
            root = source_root / "root.tex"
            child = source_root / "child.tex"
            root.write_text(
                r"\textbf{Raw} \input{isa/child.tex}", encoding="utf-8"
            )
            child.write_text(
                "(:term:base.terms.effective_address|short:)", encoding="utf-8"
            )

            class Project:
                pass

            project = Project()
            project.root = source_root
            project.terminology = self.project.terminology
            processor = LatexSourcePreprocessor(
                DocumentFragmentPipeline(()), LatexSemanticTextRenderer()
            )

            rendered = processor.render(root, project)

        self.assertIn(r"\textbf{Raw}", rendered)
        self.assertIn(
            r"\hyperref[term:base-terms-effective-address]{EA}", rendered
        )
        self.assertNotIn(r"\input{isa/", rendered)

    def test_source_preprocessor_rejects_input_cycles(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repository = Path(directory)
            source_root = repository / "isa"
            source_root.mkdir()
            root = source_root / "root.tex"
            child = source_root / "child.tex"
            root.write_text(r"\input{isa/child.tex}", encoding="utf-8")
            child.write_text(r"\input{isa/root.tex}", encoding="utf-8")

            class Project:
                pass

            project = Project()
            project.root = source_root
            project.terminology = self.project.terminology
            processor = LatexSourcePreprocessor(
                DocumentFragmentPipeline(()), LatexSemanticTextRenderer()
            )
            with self.assertRaisesRegex(RuntimeError, "cyclic TeX input"):
                processor.render(root, project)

    def test_source_preprocessor_treats_style_files_as_code(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repository = Path(directory)
            source_root = repository / "isa"
            style_root = repository / "style"
            source_root.mkdir()
            style_root.mkdir()
            root = source_root / "root.tex"
            style = style_root / "sample.sty"
            root.write_text(r"\input{style/sample.sty}", encoding="utf-8")
            style.write_text(
                r"\PackageError{sample}{field widths are invalid}{}",
                encoding="utf-8",
            )

            class Project:
                pass

            project = Project()
            project.root = source_root
            project.terminology = self.project.terminology
            processor = LatexSourcePreprocessor(
                DocumentFragmentPipeline(()), LatexSemanticTextRenderer()
            )

            rendered = processor.render(root, project)

        self.assertIn("field widths are invalid", rendered)
        self.assertNotIn(r"\endinput", rendered)

    def test_direct_term_rewriter_uses_forms_and_protects_tex_identifiers(self) -> None:
        source = (
            r"effective addresses, effective address, instruction-header, "
            r"\label{effective address}\texttt{effective address}% effective address"
        )

        rendered, count = rewrite_direct_terms(source, self.project.terminology)

        self.assertEqual(count, 2)
        self.assertIn(
            "(:term:base.terms.effective_address|plural:)", rendered
        )
        self.assertIn("(:term:base.terms.effective_address:)", rendered)
        self.assertIn("instruction-header", rendered)
        self.assertIn(r"\label{effective address}", rendered)
        self.assertIn(r"\texttt{effective address}", rendered)

    def test_source_preprocessor_rejects_direct_registered_term(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repository = Path(directory)
            source_root = repository / "isa"
            source_root.mkdir()
            root = source_root / "root.tex"
            root.write_text("an effective address", encoding="utf-8")

            class Project:
                pass

            project = Project()
            project.root = source_root
            project.terminology = self.project.terminology
            processor = LatexSourcePreprocessor(
                DocumentFragmentPipeline(()), LatexSemanticTextRenderer()
            )
            with self.assertRaisesRegex(ValueError, "must use"):
                processor.render(root, project)

    def test_source_preprocessor_rejects_unknown_term_reference(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repository = Path(directory)
            source_root = repository / "isa"
            source_root.mkdir()
            root = source_root / "root.tex"
            root.write_text(
                "(:term:base.terms.does_not_exist:)", encoding="utf-8"
            )

            class Project:
                pass

            project = Project()
            project.root = source_root
            project.terminology = self.project.terminology
            processor = LatexSourcePreprocessor(
                DocumentFragmentPipeline(()), LatexSemanticTextRenderer()
            )
            with self.assertRaises(ValueError):
                processor.render(root, project)

    def test_source_preprocessor_renders_instruction_reference(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repository = Path(directory)
            source_root = repository / "isa"
            source_root.mkdir()
            root = source_root / "root.tex"
            root.write_text("See (:ref:base.instructions.ADD:).", encoding="utf-8")

            class Project:
                pass

            project = Project()
            project.root = source_root
            project.terminology = self.project.terminology
            project.entities = self.project.entities
            processor = LatexSourcePreprocessor(
                DocumentFragmentPipeline(()), LatexSemanticTextRenderer()
            )

            rendered = processor.render(root, project)

            root.write_text(
                "(:ref:base.instructions.DOES_NOT_EXIST:)", encoding="utf-8"
            )
            with self.assertRaises(ValueError):
                processor.render(root, project)

        self.assertEqual(rendered, r"See \hyperref[instr:add]{\texttt{ADD}}.")

    def test_source_preprocessor_renders_register_reference(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            source_root = Path(directory) / "isa"
            source_root.mkdir()
            root = source_root / "root.tex"
            root.write_text(
                "Use (:ref:base.registers.CONTROL.PTCR:).", encoding="utf-8"
            )

            class Project:
                pass

            project = Project()
            project.root = source_root
            project.terminology = self.project.terminology
            project.entities = self.project.entities
            rendered = LatexSourcePreprocessor(
                DocumentFragmentPipeline(()), LatexSemanticTextRenderer()
            ).render(root, project)

        self.assertEqual(
            rendered,
            r"Use \hyperref[entity:base-registers-control-ptcr]{\texttt{PTCR}}.",
        )

    def test_source_preprocessor_renders_registry_entity_references(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            source_root = Path(directory) / "isa"
            source_root.mkdir()
            root = source_root / "root.tex"
            root.write_text(
                " ".join(
                    (
                        "(:ref:base.ea.modes.compact.register:)",
                        "(:ref:base.field_types.Rn:)",
                        "(:ref:base.payload_types.IMM8:)",
                        "(:ref:base.cpuid.BASE.IDENTITY.HEADER:)",
                        "(:ref:base.cpuid.BASE.IDENTITY.HEADER.MAX_INDEX:)",
                    )
                ),
                encoding="utf-8",
            )

            class Project:
                pass

            project = Project()
            project.root = source_root
            project.terminology = self.project.terminology
            project.entities = self.project.entities
            rendered = LatexSourcePreprocessor(
                DocumentFragmentPipeline(()), LatexSemanticTextRenderer()
            ).render(root, project)

        expected = (
            ("base-ea-modes-compact-register", "register"),
            ("base-field-types-rn", "Rn"),
            ("base-payload-types-imm8", "IMM8"),
            ("base-cpuid-base-identity-header", "HEADER"),
            ("base-cpuid-base-identity-header-max-index", "MAX\\_INDEX"),
        )
        for label, display in expected:
            with self.subTest(label=label):
                self.assertIn(
                    rf"\hyperref[entity:{label}]{{\texttt{{{display}}}}}",
                    rendered,
                )

    def test_composition_requires_every_terminology_group_once(self) -> None:
        source = self.repository / "artifacts/isa-reference/artifact.yaml"
        document = yaml.safe_load(source.read_text(encoding="utf-8"))
        document["body"] = [
            item for item in document["body"] if "term-group" not in item
        ]
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "artifact.yaml"
            path.write_text(
                yaml.safe_dump(document, sort_keys=False), encoding="utf-8"
            )
            with self.assertRaisesRegex(
                ValueError, "invalid terminology group coverage"
            ):
                DocumentComposition.load(path, self.project)

    def test_tex_validation_accepts_current_model_structure(self) -> None:
        tex = """\\begin{document}
% topic: base.events
\\section{Events}\\label{event:new}\\begin{manualinstruction}{ADD}{Add}{instr:add}
Allocation pattern:
\\end{document}
"""
        report = TexValidator().validate(tex, expected_topics=1, expected_forms=1)

        self.assertTrue(report.passed)

    def test_tex_validation_rejects_model_count_mismatch(self) -> None:
        tex = r"\begin{document}\end{document}"
        report = TexValidator().validate(tex, expected_topics=1, expected_forms=1)

        self.assertFalse(report.passed)
        self.assertIn("rendered 0 topics", report.errors[0])

    def test_fragment_pipeline_accepts_independent_providers(self) -> None:
        pipeline = DocumentFragmentPipeline((_SampleFragmentProvider(),))

        self.assertEqual(
            pipeline.expand("instructions: @sample@", self.project),
            f"instructions: {len(self.project.select())}",
        )

    def test_default_fragment_pipeline_expands_loaded_ea_modes(self) -> None:
        rendered = DocumentFragmentPipeline.default().expand(
            "@EA_MODE_DIAGRAMS@", self.project
        )

        self.assertNotIn("@EA_MODE_DIAGRAMS@", rendered)
        self.assertEqual(
            rendered.count("% Generated from "),
            len(self.project.catalog.ea_modes),
        )
        self.assertIn(r"\BedrockEAFlowStart", rendered)

    def test_default_fragment_pipeline_expands_register_model_figure(self) -> None:
        placeholder = r"\BedrockGeneratedRegisterModelFigure"

        rendered = DocumentFragmentPipeline.default().expand(
            placeholder, self.project
        )

        self.assertNotIn(placeholder, rendered)
        self.assertIn(r"\manualfigurecaption{Base Register Model}", rendered)
        self.assertIn(
            r"\manualfigurecaption{Floating-Point Register Model}", rendered
        )
        self.assertIn(
            r"\manualfigurecaption{Vector and Predicate Register Model}", rendered
        )
        self.assertEqual(rendered.count(r"\begin{tikzpicture}"), 3)
        self.assertIn("{R15}", rendered)
        self.assertIn("{GS5}", rendered)
        self.assertIn(r"{24 named\\registers}", rendered)
        self.assertIn("{VLEN-1}", rendered)
        self.assertIn("{127}", rendered)
        self.assertIn("{P15}", rendered)
        self.assertNotIn("dash pattern=on 6pt off 3pt", rendered)

    def test_fragment_pipeline_rejects_duplicate_placeholder_owners(self) -> None:
        with self.assertRaisesRegex(ValueError, "is owned by both"):
            DocumentFragmentPipeline(
                (_SampleFragmentProvider(), _SampleFragmentProvider())
            )


if __name__ == "__main__":
    unittest.main()
