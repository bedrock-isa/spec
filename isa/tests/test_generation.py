import tempfile
import unittest
from importlib import import_module
from pathlib import Path

from engine.generation import (
    ArtifactDefinition,
    ArtifactGenerationContext,
    ArtifactGenerator,
    ArtifactGeneratorRegistry,
    ArtifactWriter,
    GeneratedArtifact,
    GeneratedArtifactSet,
)
from engine.model import SailUnit
from engine.reference import Reference
from engine.render import SailProjectRenderer
from engine.workspace import SpecWorkspace
from engine.yaml_document import YamlDocumentLoader
from types import SimpleNamespace


SailModelArtifactGenerator = import_module(
    "artifacts.sail-model.generator"
).Generator
EmulatorCoreArtifactGenerator = import_module(
    "artifacts.emulator-core.generator"
).Generator


class _Renderer:
    def __init__(self, content: str) -> None:
        self.content = content

    def render(self, program) -> str:
        return self.content


class _ProjectRenderer(_Renderer):
    def render(self, program, output_root) -> str:
        return self.content


class _Composer:
    def compose(self, project, configuration):
        return object()


class _Catalog:
    extensions = {}


class _Project:
    catalog = _Catalog()


class _Generator(ArtifactGenerator):
    def generate(self, context):
        return GeneratedArtifactSet((), self.artifact_id)


class _SailModelGenerator(ArtifactGenerator):
    def generate(self, context):
        return GeneratedArtifactSet(
            (GeneratedArtifact(Path("bedrock-model.sail_project"), "project\n"),),
            self.artifact_id,
        )


class _SailCCompiler:
    def __init__(self) -> None:
        self.project = None
        self.calls = 0

    def cache_key(self):
        return "test-sail"

    def compile(self, project, output_prefix):
        self.calls += 1
        self.project = project
        if project.read_text() != "project\n":
            raise AssertionError(f"unexpected staged Sail project: {project}")
        return '#include "bedrock_core.h"\ngenerated C\n', "generated header\n"


class GenerationTest(unittest.TestCase):
    def test_artifact_schema_requires_named_outputs(self) -> None:
        repository = Path(__file__).parents[2]
        schema = YamlDocumentLoader().mapping(repository / "artifacts/schema.yaml")
        invalid_definitions = {
            "singular": "id: legacy\ngenerator: generator.py\noutput: legacy.txt\n",
            "array": "id: legacy\ngenerator: generator.py\noutputs: [legacy.txt]\n",
            "special": (
                "id: legacy\ngenerator: generator.py\n"
                "outputs: {document: legacy.tex}\n"
                "dependency-graph: graph.json\n"
            ),
            "planned": (
                "id: future\nstatus: planned\n"
                "outputs: {reserved: future/output.txt}\n"
            ),
        }
        with tempfile.TemporaryDirectory() as directory:
            for name, content in invalid_definitions.items():
                with self.subTest(shape=name):
                    source = Path(directory) / f"{name}.yaml"
                    source.write_text(content)
                    with self.assertRaises(ValueError):
                        ArtifactDefinition.load(source, schema)

    def test_discovery_loads_artifact_local_generator_with_multiple_domains(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            artifact_root = root / "artifacts"
            source = artifact_root / "combined-reference"
            source.mkdir(parents=True)
            (artifact_root / "schema.yaml").write_text(
                (Path(__file__).parents[2] / "artifacts/schema.yaml").read_text()
            )
            (source / "artifact.yaml").write_text(
                """id: combined-reference
generator: generator.py
inputs: [isa, abi]
outputs: {combined: combined.txt}
"""
            )
            (source / "generator.py").write_text(
                """from engine.generation import ArtifactGenerator, GeneratedArtifact, GeneratedArtifactSet

class Generator(ArtifactGenerator):
    def generate(self, context):
        context.require_provider('isa')
        context.require_provider('abi')
        return GeneratedArtifactSet(
            (GeneratedArtifact(self.definition.outputs['combined'], 'combined\\n'),),
            self.artifact_id,
        )
"""
            )
            workspace = SpecWorkspace.create(root, {"isa": object(), "abi": object()})

            registry = ArtifactGeneratorRegistry.discover(workspace)
            generated = registry.generate("combined-reference", workspace, root / "out")

            self.assertEqual(registry.artifact_ids, ("combined-reference",))
            self.assertEqual(generated.artifact_id, "combined-reference")
            self.assertEqual(generated.artifact("combined.txt").content, "combined\n")

    def test_sail_project_places_instruction_entries_before_boundary(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            core = root / "core.sail"
            instruction = root / "instruction.sail"
            boundary = root / "boundary.sail"
            core.write_text("$property\n")
            instruction.write_text("$property\n")
            boundary.write_text("$property\n")
            instruction_semantics = SimpleNamespace(source=instruction)
            program = SimpleNamespace(
                sail_units=(
                    SailUnit(
                        owner="base",
                        id="core",
                        reference=Reference.parse("base.core"),
                        source=Path("model.yaml"),
                        sources=(core,),
                        requires=(),
                    ),
                    SailUnit(
                        owner="base",
                        id="boundary",
                        reference=Reference.parse("base.boundary"),
                        source=Path("model.yaml"),
                        sources=(boundary,),
                        requires=(Reference.parse("base.core"),),
                    ),
                ),
                instruction_semantics=(instruction_semantics,),
            )

            rendered = SailProjectRenderer().render(program, root)

            self.assertLess(rendered.index("model_base_core {"), rendered.index("operation_entries {"))
            self.assertLess(rendered.index("operation_entries {"), rendered.index("model_base_boundary {"))
            self.assertIn("files\n    instruction.sail,\n    generated/dispatch.sail", rendered)
            self.assertIn("requires registry, operation_entries, model_base_core", rendered)

    def test_generator_assembles_artifacts_without_writing(self) -> None:
        definition = ArtifactDefinition(
            "sail-model",
            Path("artifact.yaml"),
            {
                "id": "sail-model",
                "extensions": [],
                "outputs": {
                    "registry": "generated/registry.sail",
                    "catalog": "generated/catalog.sail",
                    "dispatch": "generated/dispatch.sail",
                    "project": "bedrock-model.sail_project",
                },
            },
        )
        generator = SailModelArtifactGenerator(
            definition,
            composer=_Composer(),
            registry=_Renderer("registry"),
            catalog=_Renderer("catalog"),
            dispatch=_Renderer("dispatch"),
            project=_ProjectRenderer("project"),
        )
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "not-created"

            artifacts = generator.generate(
                ArtifactGenerationContext.create(
                    SpecWorkspace.create(Path.cwd(), {"isa": _Project()}), output
                )
            )

            self.assertFalse(output.exists())
            self.assertEqual(artifacts.artifact_id, "sail-model")
            self.assertEqual(
                artifacts.artifact("generated/registry.sail").content, "registry"
            )
            self.assertEqual(
                artifacts.artifact("generated/catalog.sail").content, "catalog"
            )
            self.assertEqual(
                artifacts.artifact("generated/dispatch.sail").content, "dispatch"
            )
            self.assertEqual(
                artifacts.artifact("bedrock-model.sail_project").content, "project"
            )

    def test_emulator_core_wraps_compiled_sail_with_generated_c_adapter(self) -> None:
        outputs = (
            "emulator/core/bedrock_core.c",
            "emulator/core/bedrock_core.h",
            "emulator/core/bedrock_core_abi.h",
            "emulator/core/.generation-stamp",
        )
        definition = ArtifactDefinition(
            "emulator-core",
            Path("artifact.yaml"),
            {
                "id": "emulator-core",
                "depends-on": ["sail-model"],
                "outputs": {
                    "implementation": outputs[0],
                    "model-header": outputs[1],
                    "abi-header": outputs[2],
                    "generation-stamp": outputs[3],
                },
            },
        )
        compiler = _SailCCompiler()
        generator = EmulatorCoreArtifactGenerator(definition, compiler=compiler)
        model_definition = ArtifactDefinition(
            "sail-model",
            Path("sail-model/artifact.yaml"),
            {"outputs": {"project": "bedrock-model.sail_project"}},
        )
        generator._sail_model_generator = lambda context: _SailModelGenerator(
            model_definition
        )
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            sail_source = root / "isa/model.sail"
            sail_source.parent.mkdir()
            sail_source.write_text("function value() -> int = 1\n")
            workspace = SpecWorkspace.create(root, {"isa": _Project()})
            output = root / "output"
            context = ArtifactGenerationContext.create(workspace, output)
            artifacts = generator.generate(context)
            ArtifactWriter().write(artifacts, output)
            cached_artifacts = generator.generate(context)
            sail_source.write_text("function value() -> int = 2\n")
            changed_artifacts = generator.generate(context)

        self.assertEqual(
            tuple(artifact.relative_path.as_posix() for artifact in artifacts.artifacts),
            outputs,
        )
        self.assertIsNotNone(compiler.project)
        self.assertEqual(compiler.calls, 2)
        self.assertEqual(
            cached_artifacts.artifact(outputs[0]).content,
            artifacts.artifact(outputs[0]).content,
        )
        self.assertNotEqual(
            changed_artifacts.artifact(outputs[3]).content,
            artifacts.artifact(outputs[3]).content,
        )
        core = artifacts.artifact(outputs[0]).content
        abi = artifacts.artifact(outputs[2]).content
        self.assertIn("generated C", core)
        self.assertIn("bedrock_core_execute", core)
        self.assertIn("BEDROCK_CORE_VECTOR_LANE = 7", abi)
        self.assertIn("typedef struct bedrock_core bedrock_core;", abi)
        self.assertIn("typedef struct bedrock_core_request", abi)
        self.assertIn("int32_t operation;", abi)
        self.assertIn("int32_t form_id;", abi)

    def test_writer_is_the_filesystem_mutation_boundary(self) -> None:
        artifacts = GeneratedArtifactSet(
            (GeneratedArtifact(Path("generated/value.txt"), "value\n"),),
            artifact_id="example",
        )
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "output"

            written = ArtifactWriter().write(artifacts, root)

            self.assertEqual(
                written, ((root / "generated/value.txt").resolve(),)
            )
            self.assertEqual(written[0].read_text(), "value\n")

    def test_writer_preserves_binary_artifacts(self) -> None:
        artifacts = GeneratedArtifactSet(
            (GeneratedArtifact(Path("generated/asset.bin"), b"\x00\xff\x10"),),
            artifact_id="binary-example",
        )
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "output"

            written = ArtifactWriter().write(artifacts, root)

            self.assertEqual(written[0].read_bytes(), b"\x00\xff\x10")

    def test_writer_removes_only_stale_files_owned_by_the_same_artifact(self) -> None:
        writer = ArtifactWriter()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "output"
            writer.write(
                GeneratedArtifactSet(
                    (
                        GeneratedArtifact(Path("site/index.html"), "old index\n"),
                        GeneratedArtifact(Path("site/topics/legacy.html"), "legacy\n"),
                    ),
                    artifact_id="web-reference",
                ),
                root,
            )
            writer.write(
                GeneratedArtifactSet(
                    (GeneratedArtifact(Path("tex/isa-reference.tex"), "isa\n"),),
                    artifact_id="isa-reference",
                ),
                root,
            )

            written = writer.write(
                GeneratedArtifactSet(
                    (GeneratedArtifact(Path("site/index.html"), "new index\n"),),
                    artifact_id="web-reference",
                ),
                root,
            )

            self.assertEqual(written, ((root / "site/index.html").resolve(),))
            self.assertEqual(written[0].read_text(), "new index\n")
            self.assertFalse((root / "site/topics/legacy.html").exists())
            self.assertFalse((root / "site/topics").exists())
            self.assertEqual((root / "tex/isa-reference.tex").read_text(), "isa\n")

    def test_writer_rejects_a_path_owned_by_another_artifact(self) -> None:
        writer = ArtifactWriter()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "output"
            writer.write(
                GeneratedArtifactSet(
                    (GeneratedArtifact(Path("shared/value.txt"), "first\n"),),
                    artifact_id="first",
                ),
                root,
            )

            with self.assertRaisesRegex(ValueError, "conflicts with owner 'first'"):
                writer.write(
                    GeneratedArtifactSet(
                        (GeneratedArtifact(Path("shared/value.txt"), "second\n"),),
                        artifact_id="second",
                    ),
                    root,
                )

            self.assertEqual((root / "shared/value.txt").read_text(), "first\n")

    def test_writer_rejects_nested_symlinks_before_mutating_output(self) -> None:
        writer = ArtifactWriter()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "output"
            actual = root / "actual"
            actual.mkdir(parents=True)
            value = actual / "value.txt"
            value.write_text("original\n")
            (root / "alias").symlink_to(actual, target_is_directory=True)

            with self.assertRaisesRegex(ValueError, "traverses a symlink"):
                writer.write(
                    GeneratedArtifactSet(
                        (GeneratedArtifact(Path("alias/value.txt"), "replacement\n"),),
                        artifact_id="symlink-example",
                    ),
                    root,
                )

            self.assertEqual(value.read_text(), "original\n")
            self.assertFalse(
                (root / ".artifact-ownership/symlink-example.json").exists()
            )

    def test_writer_refuses_to_overwrite_an_unowned_existing_file(self) -> None:
        writer = ArtifactWriter()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "output"
            existing = root / "generated/value.txt"
            existing.parent.mkdir(parents=True)
            existing.write_text("user-owned\n")

            with self.assertRaisesRegex(ValueError, "unowned"):
                writer.write(
                    GeneratedArtifactSet(
                        (GeneratedArtifact(Path("generated/value.txt"), "new\n"),),
                        artifact_id="example",
                    ),
                    root,
                )

            self.assertEqual(existing.read_text(), "user-owned\n")
            self.assertFalse((root / ".artifact-ownership/example.json").exists())

    def test_artifact_rejects_output_escape(self) -> None:
        for path in (Path("../outside"), Path("/absolute")):
            with self.subTest(path=path), self.assertRaisesRegex(
                ValueError, "escapes output root"
            ):
                GeneratedArtifact(path, "")

    def test_registry_rejects_duplicate_artifact_ids(self) -> None:
        definition = ArtifactDefinition("duplicate", Path("artifact.yaml"), {})
        with self.assertRaisesRegex(ValueError, "duplicate artifact id"):
            ArtifactGeneratorRegistry((_Generator(definition), _Generator(definition)))

    def test_artifact_set_rejects_duplicate_output_paths(self) -> None:
        with self.assertRaisesRegex(ValueError, "duplicate generated artifact paths"):
            GeneratedArtifactSet(
                (
                    GeneratedArtifact(Path("same.txt"), "first"),
                    GeneratedArtifact(Path("same.txt"), "second"),
                ),
                artifact_id="duplicate",
            )

    def test_registry_rejects_unknown_dependencies_and_output_collisions(self) -> None:
        missing = ArtifactDefinition(
            "dependent",
            Path("dependent/artifact.yaml"),
            {"depends-on": ["missing"], "outputs": {"result": "dependent.txt"}},
        )
        with self.assertRaisesRegex(ValueError, "unknown artifact dependency"):
            ArtifactGeneratorRegistry((_Generator(missing),))

        first = ArtifactDefinition(
            "first", Path("first/artifact.yaml"), {"outputs": {"result": "same.txt"}}
        )
        second = ArtifactDefinition(
            "second",
            Path("second/artifact.yaml"),
            {"outputs": {"result": "same.txt"}},
        )
        with self.assertRaisesRegex(ValueError, "overlaps"):
            ArtifactGeneratorRegistry((_Generator(first), _Generator(second)))

        tree = ArtifactDefinition(
            "tree", Path("tree/artifact.yaml"), {"outputs": {"site": "site"}}
        )
        member = ArtifactDefinition(
            "member",
            Path("member/artifact.yaml"),
            {"outputs": {"index": "site/index.html"}},
        )
        with self.assertRaisesRegex(ValueError, "overlaps"):
            ArtifactGeneratorRegistry((_Generator(tree), _Generator(member)))

    def test_generated_paths_must_populate_their_declared_output_roots(self) -> None:
        definition = ArtifactDefinition(
            "publication",
            Path("publication/artifact.yaml"),
            {"outputs": {"site": "site"}},
        )

        definition.validate_generated(
            GeneratedArtifactSet(
                (GeneratedArtifact(Path("site/index.html"), "index\n"),),
                artifact_id="publication",
            )
        )
        with self.assertRaisesRegex(ValueError, "owned by 0 declared output roots"):
            definition.validate_generated(
                GeneratedArtifactSet(
                    (GeneratedArtifact(Path("outside.txt"), "outside\n"),),
                    artifact_id="publication",
                )
            )


if __name__ == "__main__":
    unittest.main()
