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
from engine.document import DocumentBuilder, TexValidationReport, TexValidator
from engine.generation import (
    ArtifactDefinition,
    ArtifactGenerationContext,
    ArtifactGenerator,
    ArtifactGeneratorRegistry,
    ArtifactWriter,
    GeneratedArtifact,
    GeneratedArtifactSet,
)
from engine.project import IsaProject
from engine.reference import Reference
from engine.render import (
    DocumentFragmentContext,
    DocumentFragmentPipeline,
    DocumentFragmentProvider,
    EventReferenceRenderer,
    LatexSemanticTextRenderer,
    LatexSourcePreprocessor,
    rewrite_direct_terms,
)
from engine.workspace import SpecWorkspace


class _SampleFragmentProvider(DocumentFragmentProvider):
    @property
    def placeholders(self) -> frozenset[str]:
        return frozenset(("@sample@",))

    def expand(self, text: str, context: DocumentFragmentContext) -> str:
        return text.replace("@sample@", str(len(context.project.select())))


class _DeclaredGenerator(ArtifactGenerator):
    def generate(self, context: ArtifactGenerationContext) -> GeneratedArtifactSet:
        raise AssertionError("registry ownership validation must not generate artifacts")


class _FailingCompiler:
    def compile(
        self,
        source: Path,
        output_root: Path,
        repository: Path,
        executable: str,
    ) -> None:
        raise RuntimeError("compiler failed for test")


class _RejectingValidator:
    def validate(
        self, tex: str, *, expected_topics: int, expected_forms: int
    ) -> TexValidationReport:
        return TexValidationReport(
            passed=False,
            errors=("rejected for test",),
            quantitative={},
            qualitative_review={},
        )


def _cpuid_projection_structure(
    rendered: str,
) -> tuple[tuple[tuple[str, str], ...], tuple[tuple[str, int], ...], int]:
    def identifier(value: str) -> str:
        return value.replace(r"\_\allowbreak{}", "_").replace(r"\_", "_")

    table = rendered.split(r"\end{BedrockTabular}", 1)[0]
    table_body = table.split(r"\midrule", 1)[1].rsplit(r"\bottomrule", 1)[0]
    rows = tuple(
        (
            identifier(left.removeprefix(r"\texttt{").removesuffix("}")),
            identifier(right.removeprefix(r"\texttt{").removesuffix("}")),
        )
        for left, right in re.findall(r"(?m)^(.+?) & (.+?)\\\\$", table_body)
    )

    diagram = rendered.split(r"\begin{BedrockListedFormatDiagram}", 1)[1]
    fields = tuple(
        (
            identifier(field),
            int(bit_range.split(":", 1)[0])
            - int(bit_range.split(":", 1)[-1])
            + 1,
        )
        for field, bit_range in re.findall(
            r"\\texttt\{((?:[^{}]|\\allowbreak\{\})+)\}"
            r"\[\\texttt\{([0-9]+(?::[0-9]+)?)\}\]",
            diagram,
        )
    )
    row_count = diagram.count(r"\BedrockFormatRowRange")
    return rows, fields, row_count


class DocumentTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.root = Path(__file__).parents[1].resolve()
        cls.repository = cls.root.parent
        cls.workspace = SpecWorkspace.load(cls.repository)
        project = cls.workspace.require_provider("isa")
        if not isinstance(project, IsaProject):
            raise TypeError("workspace isa provider must be an IsaProject")
        cls.project = project
        cls.composition = DocumentComposition.load(
            cls.repository / "artifacts/isa-reference/artifact.yaml", cls.project
        )
        cls.generator = ArtifactGeneratorRegistry.discover(cls.workspace).generator(
            "isa-reference"
        )
        cls.public_targets = cls.generator.renderer.public_targets(
            cls.composition, cls.project
        )

    def test_generator_renders_explicit_composition_without_writing(self) -> None:
        artifact = self.generator.generate(
            ArtifactGenerationContext.create(self.workspace, self.root / "output")
        ).artifact(
            "tex/isa-reference.tex"
        )

        topic_count = sum(
            1
            if isinstance(block, TopicBlock)
            else len(block.introduction)
            if isinstance(block, InstructionSetBlock)
            else 0
            for block in self.composition.blocks
        )
        term_group_count = sum(
            isinstance(block, TermGroupBlock) for block in self.composition.blocks
        )
        instruction_sets = tuple(
            block
            for block in self.composition.blocks
            if isinstance(block, InstructionSetBlock)
        )
        bundles = tuple(
            bundle for block in instruction_sets for bundle in block.instructions
        )
        form_count = sum(len(bundle.encodings.forms) for bundle in bundles)
        self.assertEqual(
            artifact.content.count("% topic:"),
            topic_count,
        )
        self.assertEqual(
            artifact.content.count("% term-group:"),
            term_group_count,
        )
        self.assertEqual(
            artifact.content.count("% instruction-set:"),
            len(instruction_sets),
        )
        self.assertEqual(
            artifact.content.count(r"\begin{BedrockInstruction}"), len(bundles)
        )
        instruction_entries = re.findall(
            r"\\begin\{BedrockInstruction\}.*?\\end\{BedrockInstruction\}",
            artifact.content,
            re.DOTALL,
        )
        self.assertEqual(
            sum(
                entry.count(r"\begin{BedrockFormBlock}")
                for entry in instruction_entries
            ),
            form_count,
        )
        self.assertEqual(artifact.content.count(r"\begin{document}"), 1)
        self.assertEqual(artifact.content.count(r"\end{document}"), 1)
        self.assertNotIn(r"\input{isa/", artifact.content)

    def test_dependency_graph_references_declared_nodes(self) -> None:
        graph = json.loads(
            self.generator.generate(
                ArtifactGenerationContext.create(self.workspace, self.root / "output")
            ).artifact("graphs/isa-reference-dependencies.json").content
        )
        self.assertTrue(graph["nodes"])
        self.assertTrue(graph["edges"])
        node_ids = {node["id"] for node in graph["nodes"]}
        self.assertTrue(
            all(
                edge["source"] in node_ids
                and edge["target"] in node_ids
                and edge["occurrences"] > 0
                for edge in graph["edges"]
            )
        )
        self.assertTrue(
            any(edge["kind"] == "reference" for edge in graph["edges"])
        )

    def test_public_targets_are_selected_by_the_composition(self) -> None:
        self.assertFalse(
            self.public_targets.contains(Reference.parse("base.field_types.Rn"))
        )
        self.assertFalse(
            self.public_targets.contains(
                Reference.parse("base.architecture.overview.section")
            )
        )
        self.assertFalse(
            self.public_targets.contains(Reference.parse("base.terms.device_memory"))
        )
        self.assertFalse(
            self.public_targets.contains(
                Reference.parse("base.events.EXCEPTION.INVALID_OPCODE")
            )
        )
        machine_check = Reference.parse("base.events.EXCEPTION.MACHINE_CHECK")
        tracing = Reference.parse("base.term_groups.tracing")
        self.assertTrue(self.public_targets.contains(machine_check))
        self.assertTrue(self.public_targets.contains(tracing))
        self.assertEqual(
            self.public_targets.label(machine_check), "event:machine-check"
        )
        self.assertEqual(
            self.public_targets.label(tracing), "term-group:tracing"
        )

    def test_event_code_projection_is_explicit_and_single_grain(self) -> None:
        artifact = self.generator.generate(
            ArtifactGenerationContext.create(self.workspace, self.root / "output")
        ).artifact("tex/isa-reference.tex")
        allocation = artifact.content.split(
            r"\BedrockTableCaption{Fixed Architectural Event-Code Allocations}", 1
        )[1].split(r"\end{BedrockLongTable}", 1)[0]

        self.assertNotIn("Architectural Leaf Event Contracts", artifact.content)
        self.assertIn(r"\textbf{Code} & \textbf{Event}\\", allocation)
        self.assertNotIn(r"\textbf{Family}", allocation)
        self.assertNotIn(r"\textbf{Frame}", allocation)
        self.assertNotIn(r"\textbf{Payload}", allocation)
        self.assertNotIn("The trace mechanism reports", allocation)
        self.assertIn(
            r"\label{event:machine-check}", allocation
        )

    def test_event_code_renderer_projects_only_authored_placements(self) -> None:
        rendered = EventReferenceRenderer().expand(
            "(:event-code:base.events.EXCEPTION.DEBUG_TRACE:)",
            DocumentFragmentContext(
                self.project,
                self.public_targets,
                self.root / "documents/explicit-event-code.tex",
            ),
        )

        self.assertIn(r"\texttt{0x00000000}", rendered)
        self.assertIn("DEBUG", rendered)
        self.assertIn("TRACE", rendered)
        self.assertNotIn("BREAKPOINT", rendered)
        self.assertNotIn("The trace mechanism reports", rendered)

    def test_instruction_formats_render_physical_instruction_bytes(self) -> None:
        artifact = self.generator.generate(
            ArtifactGenerationContext.create(self.workspace, self.root / "output")
        ).artifact("tex/isa-reference.tex")

        extrashort = self._instruction_format(
            artifact.content, "ADD.Q 8, SP"
        )
        self.assertIn(
            r"\BedrockBitFieldRow{}{\BedrockByteRowLabels{0}{1}}{%", extrashort
        )
        self.assertIn(r"\BedrockBitFixed{0}{1}", extrashort)
        self.assertIn(r"\BedrockBitFixed{0001110}{7}", extrashort)

        short = self._instruction_format(
            artifact.content, r"ADD.\{L\textbar{}Q\}(z) Rn(s), Rn(d)"
        )
        self.assertIn(
            r"\BedrockBitFieldRow{}{\BedrockByteRowLabels{0}{2}}{%", short
        )
        self.assertIn(r"\BedrockBitFixed{10}{2}", short)
        self.assertIn(r"\BedrockBitFixed{00001}{5}", short)
        self.assertIn(r"\BedrockBitVariable{z}{1}", short)
        self.assertIn(r"\BedrockBitGap{1}", short)
        self.assertIn(r"\BedrockBitVariable{s}{4}", short)
        self.assertIn(r"\BedrockBitVariable{d}{4}", short)

        extended = self._instruction_format(
            artifact.content, r"ADD.Q \textless{}imm16s\textgreater{}, SP"
        )
        self.assertIn(
            r"\BedrockBitFieldRow{}{\BedrockByteRowLabels{0}{3}}{%", extended
        )
        self.assertIn(r"\BedrockBitFixed{11}{2}", extended)
        self.assertIn(r"\BedrockBitVariable{L}{4}", extended)
        self.assertIn(r"\BedrockBitFixed{10111100}{8}", extended)
        self.assertIn(r"\BedrockBitFixed{00000000}{8}", extended)
        self.assertEqual(extended.count(r"\BedrockBitGap{1}"), 2)

    @staticmethod
    def _instruction_format(tex: str, syntax: str) -> str:
        begin = (
            r"\begin{BedrockBitDiagram}{Format: Instruction format for "
            + syntax
            + "}"
        )
        start = tex.index(begin)
        end = tex.index(r"\end{BedrockBitDiagram}", start)
        return tex[start:end]

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
            project.entities = self.project.entities
            processor = LatexSourcePreprocessor(
                DocumentFragmentPipeline(()), LatexSemanticTextRenderer()
            )

            rendered = processor.render(root, project, self.public_targets)

        self.assertIn(r"\textbf{Raw}", rendered)
        self.assertIn(
            r"\hyperref[term:effective-address]{EA}", rendered
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
            project.entities = self.project.entities
            processor = LatexSourcePreprocessor(
                DocumentFragmentPipeline(()), LatexSemanticTextRenderer()
            )
            with self.assertRaisesRegex(RuntimeError, "cyclic TeX input"):
                processor.render(root, project, self.public_targets)

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
            project.entities = self.project.entities
            processor = LatexSourcePreprocessor(
                DocumentFragmentPipeline(()), LatexSemanticTextRenderer()
            )

            rendered = processor.render(root, project, self.public_targets)

        self.assertIn("field widths are invalid", rendered)
        self.assertNotIn(r"\endinput", rendered)

    def test_direct_term_rewriter_uses_forms_and_protects_tex_identifiers(self) -> None:
        source = (
            r"effective addresses, effective address, instruction-header, "
            r"\label{effective address}\texttt{effective address}% effective address"
        )

        rendered, count = rewrite_direct_terms(source, self.project.terminology)

        self.assertEqual(count, 2)
        self.assertEqual(rendered.count("(:term:detected:)"), 2)
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
            project.entities = self.project.entities
            processor = LatexSourcePreprocessor(
                DocumentFragmentPipeline(()), LatexSemanticTextRenderer()
            )
            with self.assertRaisesRegex(ValueError, "must use"):
                processor.render(root, project, self.public_targets)

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
            project.entities = self.project.entities
            processor = LatexSourcePreprocessor(
                DocumentFragmentPipeline(()), LatexSemanticTextRenderer()
            )
            with self.assertRaises(ValueError):
                processor.render(root, project, self.public_targets)

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

            rendered = processor.render(root, project, self.public_targets)

            root.write_text(
                "(:ref:base.instructions.DOES_NOT_EXIST:)", encoding="utf-8"
            )
            with self.assertRaises(ValueError):
                processor.render(root, project, self.public_targets)

        self.assertEqual(rendered, r"See \hyperref[instr:add]{\texttt{ADD}}.")

    def test_source_preprocessor_rejects_unprojected_register_reference(self) -> None:
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
            with self.assertRaisesRegex(ValueError, "no target in this public projection"):
                LatexSourcePreprocessor(
                    DocumentFragmentPipeline(()), LatexSemanticTextRenderer()
                ).render(root, project, self.public_targets)

    def test_source_preprocessor_rejects_internal_catalog_references(self) -> None:
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
            with self.assertRaisesRegex(ValueError, "no target in this public projection"):
                LatexSourcePreprocessor(
                    DocumentFragmentPipeline(()), LatexSemanticTextRenderer()
                ).render(root, project, self.public_targets)

    def test_composition_allows_catalog_members_to_remain_private(self) -> None:
        source = self.repository / "artifacts/isa-reference/artifact.yaml"
        original = yaml.safe_load(source.read_text(encoding="utf-8"))
        for block_kind in ("topic", "term-group", "instruction-set"):
            with self.subTest(block_kind=block_kind):
                document = yaml.safe_load(source.read_text(encoding="utf-8"))
                removed = next(
                    item for item in document["body"] if block_kind in item
                )
                document["body"].remove(removed)
                with tempfile.TemporaryDirectory() as directory:
                    path = Path(directory) / "artifact.yaml"
                    path.write_text(
                        yaml.safe_dump(document, sort_keys=False), encoding="utf-8"
                    )
                    composition = DocumentComposition.load(path, self.project)

                self.assertEqual(
                    len(composition.blocks), len(original["body"]) - 1
                )

    def test_composition_rejects_duplicate_explicit_placement(self) -> None:
        source = self.repository / "artifacts/isa-reference/artifact.yaml"
        for block_kind in ("topic", "term-group", "instruction-set"):
            with self.subTest(block_kind=block_kind):
                document = yaml.safe_load(source.read_text(encoding="utf-8"))
                placed = next(
                    item for item in document["body"] if block_kind in item
                )
                document["body"].append(placed)
                with tempfile.TemporaryDirectory() as directory:
                    path = Path(directory) / "artifact.yaml"
                    path.write_text(
                        yaml.safe_dump(document, sort_keys=False), encoding="utf-8"
                    )
                    with self.assertRaisesRegex(
                        ValueError, "duplicate public .* placements"
                    ):
                        DocumentComposition.load(path, self.project)

    def test_tex_validation_accepts_current_model_structure(self) -> None:
        tex = """\\begin{document}
% topic: base.events
\\section{Events}\\label{event:new}\\hyperref[event:new]{event}\\begin{BedrockInstruction}{ADD}{Add}{instr:add}
\\begin{BedrockFormBlock}{2.75in}
\\end{BedrockFormBlock}
\\end{BedrockInstruction}
\\end{document}
"""
        report = TexValidator().validate(tex, expected_topics=1, expected_forms=1)

        self.assertTrue(report.passed)

    def test_tex_validation_rejects_model_count_mismatch(self) -> None:
        tex = r"\begin{document}\end{document}"
        report = TexValidator().validate(tex, expected_topics=1, expected_forms=1)

        self.assertFalse(report.passed)
        self.assertIn("rendered 0 topics", report.errors[0])
        self.assertIn("rendered 0 forms", report.errors[1])

    def test_tex_validation_counts_only_instruction_owned_forms(self) -> None:
        tex = r"""\begin{document}
\begin{BedrockFormBlock}{2.75in}
\end{BedrockFormBlock}
\begin{BedrockInstruction}{ADD}{Add}{instr:add}
\begin{BedrockFormBlock}{2.75in}
\end{BedrockFormBlock}
\end{BedrockInstruction}
\end{document}
"""

        report = TexValidator().validate(tex, expected_topics=0, expected_forms=1)

        self.assertTrue(report.passed)

    def test_tex_validation_rejects_reference_without_public_target(self) -> None:
        tex = r"\begin{document}\hyperref[entity:internal-only]{internal}\end{document}"
        report = TexValidator().validate(tex, expected_topics=0, expected_forms=0)

        self.assertFalse(report.passed)
        self.assertIn(
            "unresolved public TeX targets: ['entity:internal-only']",
            report.errors,
        )

    def test_document_builder_publishes_one_declared_owner_without_compiling(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = (Path(directory) / "output").resolve()

            result = DocumentBuilder(generator=self.generator).build(
                self.workspace, output, compile_pdf=False
            )

            self.assertTrue(result.report.passed)
            self.assertEqual(result.tex, output / "tex/isa-reference.tex")
            self.assertIsNone(result.pdf)
            ownership = output / ".artifact-ownership"
            manifests = {
                source.stem: json.loads(source.read_text(encoding="utf-8"))
                for source in ownership.glob("*.json")
            }
            self.assertEqual(set(manifests), {"isa-reference"})
            self.assertEqual(
                set(manifests["isa-reference"]["paths"]),
                self._existing_declared_outputs(output),
            )

    def test_derived_output_root_is_visible_to_registry_collision_validation(self) -> None:
        first = ArtifactDefinition(
            "first",
            Path("first/artifact.yaml"),
            {
                "outputs": {"source": "tex/source.tex"},
                "derived-outputs": {"document": "pdf/manual.pdf"},
            },
        )
        second = ArtifactDefinition(
            "second",
            Path("second/artifact.yaml"),
            {"outputs": {"document": "pdf/manual.pdf"}},
        )

        with self.assertRaisesRegex(ValueError, "overlaps"):
            ArtifactGeneratorRegistry(
                (_DeclaredGenerator(first), _DeclaredGenerator(second))
            )

    def test_document_validate_removes_stale_compiled_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = (Path(directory) / "output").resolve()
            self._seed_compiled_outputs(output)

            result = DocumentBuilder(generator=self.generator).build(
                self.workspace, output, compile_pdf=False
            )

            self.assertTrue(result.report.passed)
            for path in self.generator.definition.derived_outputs.values():
                if path.parts[0] == "pdf":
                    self.assertFalse((output / path).exists())

    def test_document_compile_failure_leaves_no_stale_compiled_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = (Path(directory) / "output").resolve()
            self._seed_compiled_outputs(output)

            with self.assertRaisesRegex(RuntimeError, "compiler failed for test"):
                DocumentBuilder(
                    generator=self.generator,
                    compiler=_FailingCompiler(),
                ).build(self.workspace, output, compile_pdf=True)

            for path in self.generator.definition.derived_outputs.values():
                if path.parts[0] == "pdf":
                    self.assertFalse((output / path).exists())
            manifest = json.loads(
                (output / ".artifact-ownership/isa-reference.json").read_text(
                    encoding="utf-8"
                )
            )
            self.assertEqual(
                set(manifest["paths"]),
                self._existing_declared_outputs(output),
            )

    def test_document_validation_failure_leaves_no_stale_compiled_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = (Path(directory) / "output").resolve()
            self._seed_compiled_outputs(output)

            result = DocumentBuilder(
                generator=self.generator,
                validator=_RejectingValidator(),
            ).build(self.workspace, output, compile_pdf=True)

            self.assertFalse(result.report.passed)
            self.assertIsNone(result.pdf)
            for path in self.generator.definition.derived_outputs.values():
                if path.parts[0] == "pdf":
                    self.assertFalse((output / path).exists())

    def _seed_compiled_outputs(self, output: Path) -> None:
        derived = self.generator.definition.derived_outputs
        ArtifactWriter().write(
            GeneratedArtifactSet(
                (
                    GeneratedArtifact(derived["compiled-document"], b"old pdf"),
                    GeneratedArtifact(derived["compile-log"], b"old log"),
                    GeneratedArtifact(derived["pdf-validation"], "{}\n"),
                ),
                artifact_id=self.generator.artifact_id,
            ),
            output,
        )

    def _existing_declared_outputs(self, output: Path) -> set[str]:
        return {
            path.as_posix()
            for path in self.generator.definition.output_roots
            if (output / path).is_file()
        }

    def test_fragment_pipeline_accepts_independent_providers(self) -> None:
        pipeline = DocumentFragmentPipeline((_SampleFragmentProvider(),))

        self.assertEqual(
            pipeline.expand(
                "instructions: @sample@", self.project, self.public_targets
            ),
            f"instructions: {len(self.project.select())}",
        )

    def test_ea_diagram_projection_is_explicit_and_owner_local(self) -> None:
        source = (
            self.root
            / "ea/documents/topics/effective_address_modes/006_extended_ea_addressing_modes.tex"
        )
        rendered = DocumentFragmentPipeline.default().expand(
            "(:ea-diagram:base.ea.modes.EXT1.default_segment_base:)",
            self.project,
            self.public_targets,
            source,
        )

        self.assertNotIn("(:ea-diagram:", rendered)
        self.assertEqual(rendered.count("% Generated from "), 1)
        self.assertIn(r"\BedrockEAFlowStart", rendered)
        self.assertNotIn("FP FEA", rendered)
        self.assertNotIn("VECTOR VEA", rendered)

        with self.assertRaisesRegex(ValueError, "does not match topic owner"):
            DocumentFragmentPipeline.default().expand(
                "(:ea-diagram:FP.fea.modes.compact.immediate:)",
                self.project,
                self.public_targets,
                source,
            )

    def test_cpuid_leaf_projection_is_explicit_owner_local_and_single_grain(self) -> None:
        source = (
            self.root
            / "cpuid/documents/topics/cpuid_feature_discovery/"
            "007_optional_extension_directory.tex"
        )
        rendered = DocumentFragmentPipeline.default().expand(
            "(:cpuid-leaf:base.cpuid.EXTENSIONS.DIRECTORY:)",
            self.project,
            self.public_targets,
            source,
        )

        rows, fields, diagram_rows = _cpuid_projection_structure(rendered)
        self.assertEqual(
            rows,
            (("0x0000", "HEADER"), ("0x0001", "FEATURES")),
        )
        self.assertEqual(
            fields,
            (
                ("MAX_INDEX", 16),
                ("MAX_LEAF", 16),
                ("FP", 1),
                ("FPTRANSA", 1),
                ("VECTOR", 1),
                ("VECTORFP", 1),
            ),
        )
        self.assertEqual(diagram_rows, 2)

        with self.assertRaises(ValueError):
            DocumentFragmentPipeline.default().expand(
                "(:cpuid-leaf:VECTOR.cpuid.EXTENSIONS.VECTOR_PARAMETERS:)",
                self.project,
                self.public_targets,
                source,
            )

    def test_cpuid_leaf_projection_does_not_iterate_other_leaves(self) -> None:
        source = (
            self.root
            / "cpuid/documents/topics/cpuid_feature_discovery/"
            "013_address_width_discovery.tex"
        )
        rendered = DocumentFragmentPipeline.default().expand(
            "(:cpuid-leaf:base.cpuid.IMPLEMENTATION.ADDRESS_WIDTHS:)",
            self.project,
            self.public_targets,
            source,
        )

        rows, fields, diagram_rows = _cpuid_projection_structure(rendered)
        self.assertEqual(
            rows,
            (("0x0000", "HEADER"), ("0x0001", "PARAMETERS")),
        )
        self.assertEqual(fields, (("MAX_INDEX", 16), ("PABITS", 6)))
        self.assertEqual(diagram_rows, 2)

    def test_register_figure_projection_is_explicit_and_owner_local(self) -> None:
        source = self.root / "registers/documents/topics/register_model/002_register_model.tex"
        rendered = DocumentFragmentPipeline.default().expand(
            "(:register-figure:base:GPR,SPECIAL:)",
            self.project,
            self.public_targets,
            source,
        )

        self.assertNotIn("(:register-figure:", rendered)
        self.assertIn(r"\BedrockFigureCaption{Base Register Model}", rendered)
        self.assertEqual(rendered.count(r"\begin{tikzpicture}"), 1)
        self.assertIn("{R15}", rendered)
        self.assertNotIn("CONTROL", rendered)
        self.assertNotIn("VECTOR", rendered)

        with self.assertRaisesRegex(ValueError, "does not match topic owner"):
            DocumentFragmentPipeline.default().expand(
                "(:register-figure:FP:FPR,STATE:)",
                self.project,
                self.public_targets,
                source,
            )

    def test_fragment_pipeline_rejects_duplicate_placeholder_owners(self) -> None:
        with self.assertRaisesRegex(ValueError, "is owned by both"):
            DocumentFragmentPipeline(
                (_SampleFragmentProvider(), _SampleFragmentProvider())
            )


if __name__ == "__main__":
    unittest.main()
