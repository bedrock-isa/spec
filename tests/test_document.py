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
from engine.document import (
    DocumentBuilder,
    TexValidationCode,
    TexValidationIssue,
    TexValidationReport,
    TexValidator,
)
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
from engine.semantic_text import (
    EntityReferenceText,
    LiteralText,
    TermForm,
    TermReferenceText,
)
from engine.render import (
    DocumentFragmentContext,
    DocumentFragmentPipeline,
    DocumentFragmentProvider,
    CpuidLeafProjection,
    EaDiagramFragmentRenderer,
    EventReferenceRenderer,
    LatexSemanticTextRenderer,
    LatexSourcePreprocessor,
    ProjectedInstructionSet,
    ProjectedTermGroup,
    ProjectedTopic,
    RegisterModelFigureRenderer,
)
from engine.workspace import SpecWorkspace


def _reference_text(reference: Reference[object]) -> str:
    return ".".join((reference.owner, *reference.path, reference.element))


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
    def validate(self, tex: str) -> TexValidationReport:
        return TexValidationReport(
            passed=False,
            issues=(
                TexValidationIssue(TexValidationCode.UNRESOLVED_PLACEHOLDERS),
            ),
            quantitative={},
            qualitative_review={},
        )


class DocumentTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.root = (Path(__file__).parents[1] / "isa").resolve()
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
        projection = self.generator.renderer.project(
            self.composition, self.project
        )
        self.assertIs(projection.composition, self.composition)
        self.assertEqual(len(projection.blocks), len(self.composition.blocks))
        for authored, projected in zip(
            self.composition.blocks, projection.blocks, strict=True
        ):
            with self.subTest(block=authored):
                if isinstance(authored, TopicBlock):
                    self.assertIsInstance(projected, ProjectedTopic)
                    self.assertIs(projected.topic, authored.topic)
                elif isinstance(authored, TermGroupBlock):
                    self.assertIsInstance(projected, ProjectedTermGroup)
                    self.assertIs(projected.block, authored)
                else:
                    self.assertIsInstance(authored, InstructionSetBlock)
                    self.assertIsInstance(projected, ProjectedInstructionSet)
                    self.assertIs(projected.block, authored)
                    self.assertEqual(
                        tuple(topic.topic for topic in projected.introduction),
                        authored.introduction,
                    )
                    self.assertEqual(
                        tuple(entry.bundle for entry in projected.instructions),
                        authored.instructions,
                    )
                    for entry in projected.instructions:
                        self.assertEqual(
                            tuple(item.form for item in entry.formats),
                            entry.bundle.encodings.forms,
                        )
                        for item in entry.formats:
                            encoded = "".join(
                                segment.label
                                if segment.fixed
                                else segment.label * segment.width
                                for byte in item.bytes
                                for segment in byte.segments
                            )
                            framing = (
                                "0"
                                if item.form.pattern.bit_width == 7
                                else "10"
                                if item.form.pattern.bit_width == 14
                                else "11" + "L" * 4
                            )
                            self.assertEqual(
                                encoded,
                                framing + item.form.pattern.code,
                            )
                            self.assertTrue(
                                all(
                                    sum(segment.width for segment in byte.segments)
                                    == 8
                                    for byte in item.bytes
                                )
                            )

        generated = self.generator.generate(
            ArtifactGenerationContext.create(self.workspace, self.root / "output")
        )

        self.generator.definition.validate_generated(generated)
        self.assertEqual(generated.artifact_id, self.composition.artifact)
        self.assertEqual(
            {artifact.relative_path for artifact in generated.artifacts},
            set(self.generator.definition.outputs.values()),
        )

    def test_dependency_graph_references_declared_nodes(self) -> None:
        graph = json.loads(
            self.generator.generate(
                ArtifactGenerationContext.create(self.workspace, self.root / "output")
            )
            .artifact(self.generator.definition.outputs["dependencies"])
            .content
        )
        node_ids = {node["id"] for node in graph["nodes"]}
        for edge in graph["edges"]:
            with self.subTest(edge=edge):
                self.assertIn(edge["source"], node_ids)
                self.assertIn(edge["target"], node_ids)
                self.assertGreater(edge["occurrences"], 0)

    def test_event_code_rows_preserve_resolved_fixed_allocations(self) -> None:
        for resolved in self.project.events.resolved_events():
            if resolved.code.value is None:
                continue
            with self.subTest(event=resolved.event.reference):
                row = EventReferenceRenderer.project_row(
                    self.project.events, resolved.event.reference
                )
                self.assertEqual(row.reference, resolved.event.reference)
                self.assertEqual(row.code, resolved.code.value)
                self.assertEqual(row.event_id, resolved.event.id)

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

            projection = processor.project(root, project, self.public_targets)

        self.assertEqual(projection.source, root.resolve())
        self.assertEqual(len(projection.inputs), 1)
        self.assertEqual(projection.inputs[0].requested, "isa/child.tex")
        child_projection = projection.inputs[0].source
        self.assertEqual(child_projection.source, child.resolve())
        term = next(
            part
            for part in child_projection.semantic.parts
            if isinstance(part, TermReferenceText)
        )
        self.assertEqual(
            term.reference,
            Reference.parse("base.terms.effective_address"),
        )
        self.assertIs(term.form, TermForm.SHORT)
        self.assertTrue(
            any(
                isinstance(part, LiteralText) and r"\textbf{Raw}" in part.value
                for part in projection.semantic.parts
            )
        )

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
            with self.assertRaises(RuntimeError):
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

            projection = processor.project(root, project, self.public_targets)

        self.assertEqual(len(projection.inputs), 1)
        self.assertEqual(
            projection.inputs[0].source.style_text,
            r"\PackageError{sample}{field widths are invalid}{}",
        )

    def test_source_preprocessor_preserves_authored_literal_prose(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repository = Path(directory)
            source_root = repository / "isa"
            source_root.mkdir()
            root = source_root / "root.tex"
            root.write_text(
                r"an effective address and \texttt{ADD}", encoding="utf-8"
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

            projection = processor.project(root, project, self.public_targets)

        self.assertEqual(len(projection.semantic.parts), 1)
        self.assertIsInstance(projection.semantic.parts[0], LiteralText)
        self.assertEqual(
            projection.semantic.parts[0].value,
            r"an effective address and \texttt{ADD}",
        )

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
        instruction = next(
            bundle
            for block in self.composition.blocks
            if isinstance(block, InstructionSetBlock)
            for bundle in block.instructions
        )
        with tempfile.TemporaryDirectory() as directory:
            repository = Path(directory)
            source_root = repository / "isa"
            source_root.mkdir()
            root = source_root / "root.tex"
            root.write_text(
                f"See (:ref:{_reference_text(instruction.reference)}:).",
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

            projection = processor.project(root, project, self.public_targets)

            root.write_text(
                "(:ref:base.instructions.DOES_NOT_EXIST:)", encoding="utf-8"
            )
            with self.assertRaises(ValueError):
                processor.render(root, project, self.public_targets)

        reference = next(
            part
            for part in projection.semantic.parts
            if isinstance(part, EntityReferenceText)
        )
        entity, label = self.public_targets.resolve(reference.reference)
        self.assertEqual(entity.reference, instruction.reference)
        self.assertEqual(label, self.public_targets.label(instruction.reference))

    def test_source_preprocessor_rejects_unprojected_register_reference(self) -> None:
        private_reference = next(
            reference
            for reference, _ in self.project.entities.references.items()
            if not self.public_targets.contains(reference)
        )
        with tempfile.TemporaryDirectory() as directory:
            source_root = Path(directory) / "isa"
            source_root.mkdir()
            root = source_root / "root.tex"
            root.write_text(
                f"Use (:ref:{_reference_text(private_reference)}:).",
                encoding="utf-8",
            )

            class Project:
                pass

            project = Project()
            project.root = source_root
            project.terminology = self.project.terminology
            project.entities = self.project.entities
            with self.assertRaises(ValueError):
                LatexSourcePreprocessor(
                    DocumentFragmentPipeline(()), LatexSemanticTextRenderer()
                ).render(root, project, self.public_targets)

    def test_composition_allows_catalog_members_to_remain_private(self) -> None:
        source = self.repository / "artifacts/isa-reference/artifact.yaml"
        original = yaml.safe_load(source.read_text(encoding="utf-8"))
        original["body"] = [original["body"][0]]
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "artifact.yaml"
            path.write_text(
                yaml.safe_dump(original, sort_keys=False), encoding="utf-8"
            )
            composition = DocumentComposition.load(path, self.project)

        self.assertEqual(len(composition.blocks), 1)

    def test_composition_rejects_duplicate_explicit_placement(self) -> None:
        source = self.repository / "artifacts/isa-reference/artifact.yaml"
        document = yaml.safe_load(source.read_text(encoding="utf-8"))
        placed = document["body"][0]
        document["body"] = [placed, placed]
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "artifact.yaml"
            path.write_text(
                yaml.safe_dump(document, sort_keys=False), encoding="utf-8"
            )
            with self.assertRaises(ValueError):
                DocumentComposition.load(path, self.project)

    def test_tex_validation_requires_one_document_environment(self) -> None:
        tex = r"\begin{document}\end{document}"
        report = TexValidator().validate(tex + r"\begin{document}")

        self.assertFalse(report.passed)
        self.assertEqual(
            report.issues,
            (
                TexValidationIssue(
                    TexValidationCode.DOCUMENT_ENVIRONMENT_COUNT,
                    counts=(("begin", 2), ("end", 1)),
                ),
            ),
        )

    def test_tex_validation_rejects_reference_without_public_target(self) -> None:
        tex = r"\begin{document}\hyperref[entity:internal-only]{internal}\end{document}"
        report = TexValidator().validate(tex)

        self.assertFalse(report.passed)
        self.assertEqual(
            report.issues,
            (
                TexValidationIssue(
                    TexValidationCode.UNRESOLVED_PUBLIC_TARGETS,
                    values=("entity:internal-only",),
                ),
            ),
        )

    def test_document_builder_publishes_one_declared_owner_without_compiling(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = (Path(directory) / "output").resolve()

            result = DocumentBuilder(generator=self.generator).build(
                self.workspace, output, compile_pdf=False
            )

            self.assertTrue(result.report.passed)
            self.assertEqual(
                result.tex,
                output / self.generator.definition.outputs["document"],
            )
            self.assertIsNone(result.pdf)
            ownership = output / ".artifact-ownership"
            manifest = json.loads(
                (ownership / f"{self.generator.artifact_id}.json").read_text(
                    encoding="utf-8"
                )
            )
            self.assertEqual(
                set(manifest["paths"]),
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

        with self.assertRaises(ValueError):
            ArtifactGeneratorRegistry(
                (_DeclaredGenerator(first), _DeclaredGenerator(second))
            )

    def test_document_compile_failure_leaves_no_stale_compiled_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = (Path(directory) / "output").resolve()
            self._seed_compiled_outputs(output)

            with self.assertRaises(RuntimeError):
                DocumentBuilder(
                    generator=self.generator,
                    compiler=_FailingCompiler(),
                ).build(self.workspace, output, compile_pdf=True)

            for path in self.generator.definition.derived_outputs.values():
                if path.parts[0] == "pdf":
                    self.assertFalse((output / path).exists())
            manifest = json.loads(
                (
                    output
                    / ".artifact-ownership"
                    / f"{self.generator.artifact_id}.json"
                ).read_text(encoding="utf-8")
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
        topic, reference = next(
            (topic, Reference.parse(match.group(1)))
            for topic in self.project.model.document_topics.values()
            for match in re.finditer(
                r"(?m)^\(:ea-diagram:([A-Za-z0-9_.-]+):\)$",
                topic.document.read_text(encoding="utf-8"),
            )
        )
        context = DocumentFragmentContext(
            self.project, self.public_targets, topic.document
        )
        projection = EaDiagramFragmentRenderer.project(
            context, _reference_text(reference)
        )

        self.assertEqual(projection.diagram.reference, reference)
        self.assertEqual(projection.diagram.owner, topic.owner)

        foreign = next(
            mode.reference
            for mode in self.project.catalog.ea_modes.values()
            if mode.reference.owner != topic.owner
        )
        with self.assertRaises(ValueError):
            EaDiagramFragmentRenderer.project(context, _reference_text(foreign))

    def test_cpuid_leaf_projection_is_explicit_owner_local_and_single_grain(self) -> None:
        catalog = self.project.cpuid

        def root_reference(leaf):
            while leaf.extends is not None:
                leaf = catalog.references.leaves.resolve(leaf.extends)
            return leaf.reference

        leaves = tuple(catalog.references.leaves.values())
        for leaf in leaves:
            if leaf.extends is not None:
                continue
            with self.subTest(leaf=leaf.reference):
                projection = CpuidLeafProjection.create(catalog, leaf)
                expected: dict[
                    tuple[str, int, int, int], set[Reference[object]]
                ] = {}
                for candidate in leaves:
                    if root_reference(candidate) != leaf.reference:
                        continue
                    for query in candidate.queries:
                        key = (
                            query.id,
                            query.indexes.first,
                            query.indexes.last,
                            query.indexes.stride,
                        )
                        expected.setdefault(key, set()).update(
                            field.reference for field in query.fields
                        )
                projected = {
                    (query.id, query.first, query.last, query.stride): {
                        field.reference for field in query.fields
                    }
                    for query in projection.queries
                }
                self.assertEqual(projected, expected)
                expected_fields = {
                    reference
                    for references in expected.values()
                    for reference in references
                }
                projected_fields = {
                    field.reference
                    for query in projection.queries
                    for field in query.fields
                }
                self.assertEqual(projected_fields, expected_fields)
                self.assertEqual(
                    tuple(projected),
                    tuple(
                        sorted(
                            expected,
                            key=lambda key: (key[1], key[2], key[3], key[0]),
                        )
                    ),
                )
                for query in projection.queries:
                    self.assertEqual(
                        tuple(field.lsb for field in query.fields),
                        tuple(sorted(field.lsb for field in query.fields)),
                    )

        topic, reference = next(
            (topic, Reference.parse(match.group(1)))
            for topic in self.project.model.document_topics.values()
            for match in re.finditer(
                r"(?m)^\(:cpuid-leaf:([A-Za-z0-9_.-]+):\)$",
                topic.document.read_text(encoding="utf-8"),
            )
        )
        foreign = next(
            leaf.reference
            for leaf in leaves
            if leaf.extends is None and leaf.reference.owner != topic.owner
        )
        with self.assertRaises(ValueError):
            DocumentFragmentPipeline.default().expand(
                f"(:cpuid-leaf:{_reference_text(foreign)}:)",
                self.project,
                self.public_targets,
                topic.document,
            )
        self.assertEqual(reference.owner, topic.owner)

    def test_register_figure_projection_is_explicit_and_owner_local(self) -> None:
        topic, owner, groups = next(
            (topic, match.group(1), tuple(match.group(2).split(",")))
            for topic in self.project.model.document_topics.values()
            for match in re.finditer(
                r"(?m)^\(:register-figure:"
                r"(base|[A-Z][A-Z0-9_]*):"
                r"([A-Z][A-Z0-9_]*(?:,[A-Z][A-Z0-9_]*)*):\)$",
                topic.document.read_text(encoding="utf-8"),
            )
        )
        context = DocumentFragmentContext(
            self.project, self.public_targets, topic.document
        )
        projection = RegisterModelFigureRenderer.project(
            context, owner, groups
        )

        self.assertEqual(projection.namespace.owner, topic.owner)
        self.assertEqual(
            tuple(group.id for group in projection.groups),
            groups,
        )

        foreign = next(
            namespace.owner
            for namespace in self.project.registers.namespaces.values()
            if namespace.owner != topic.owner
        )
        with self.assertRaises(ValueError):
            RegisterModelFigureRenderer.project(
                context,
                foreign,
                tuple(self.project.registers.namespace(foreign).groups)[:1],
            )

    def test_fragment_pipeline_rejects_duplicate_placeholder_owners(self) -> None:
        with self.assertRaises(ValueError):
            DocumentFragmentPipeline(
                (_SampleFragmentProvider(), _SampleFragmentProvider())
            )


if __name__ == "__main__":
    unittest.main()
