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
    PlannedArtifactGenerator,
)
from engine.model import SailUnit
from engine.render import SailProjectRenderer
from engine.workspace import SpecWorkspace
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
outputs: [combined.txt]
"""
            )
            (source / "generator.py").write_text(
                """from engine.generation import ArtifactGenerator, GeneratedArtifactSet

class Generator(ArtifactGenerator):
    def generate(self, context):
        context.require_provider('isa')
        context.require_provider('abi')
        return GeneratedArtifactSet((), self.artifact_id)
"""
            )
            workspace = SpecWorkspace.create(root, {"isa": object(), "abi": object()})

            registry = ArtifactGeneratorRegistry.discover(workspace)
            generated = registry.generate("combined-reference", workspace, root / "out")

            self.assertEqual(registry.implemented_ids, ("combined-reference",))
            self.assertEqual(generated.artifact_id, "combined-reference")

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
                    SailUnit("base", "core", Path("model.yaml"), (core,), ()),
                    SailUnit(
                        "base",
                        "boundary",
                        Path("model.yaml"),
                        (boundary,),
                        ("base.core",),
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

    def test_emulator_core_wraps_compiled_sail_behind_declared_abi(self) -> None:
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
                "outputs": outputs,
            },
        )
        compiler = _SailCCompiler()
        generator = EmulatorCoreArtifactGenerator(definition, compiler=compiler)
        model_definition = ArtifactDefinition(
            "sail-model", Path("sail-model/artifact.yaml"), {}
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
        self.assertIn("#define BEDROCK_CORE_ABI_VERSION 5u", abi)
        self.assertIn("typedef struct bedrock_core bedrock_core;", abi)
        self.assertIn("typedef struct bedrock_core_request", abi)
        self.assertIn("int32_t operation;", abi)
        self.assertIn("int32_t form_id;", abi)
        self.assertNotIn("bedrock_core_fp_request", abi)

    def test_writer_is_the_filesystem_mutation_boundary(self) -> None:
        artifacts = GeneratedArtifactSet(
            (GeneratedArtifact(Path("generated/value.txt"), "value\n"),)
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
            (GeneratedArtifact(Path("generated/asset.bin"), b"\x00\xff\x10"),)
        )
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "output"

            written = ArtifactWriter().write(artifacts, root)

            self.assertEqual(written[0].read_bytes(), b"\x00\xff\x10")

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
                )
            )

    def test_planned_artifact_is_visible_but_not_generatable(self) -> None:
        definition = ArtifactDefinition(
            "future",
            Path("future/artifact.yaml"),
            {"outputs": ["future/output.txt"]},
            status="planned",
        )
        registry = ArtifactGeneratorRegistry((PlannedArtifactGenerator(definition),))

        self.assertEqual(registry.artifact_ids, ("future",))
        self.assertEqual(registry.implemented_ids, ())
        with self.assertRaisesRegex(NotImplementedError, "planned but not implemented"):
            registry.generate(
                "future",
                SpecWorkspace.create(Path.cwd(), {"isa": _Project()}),
                Path("output"),
            )

    def test_registry_rejects_unknown_dependencies_and_output_collisions(self) -> None:
        missing = ArtifactDefinition(
            "dependent",
            Path("dependent/artifact.yaml"),
            {"depends-on": ["missing"], "outputs": ["dependent.txt"]},
        )
        with self.assertRaisesRegex(ValueError, "unknown artifact dependency"):
            ArtifactGeneratorRegistry((_Generator(missing),))

        first = ArtifactDefinition(
            "first", Path("first/artifact.yaml"), {"outputs": ["same.txt"]}
        )
        second = ArtifactDefinition(
            "second",
            Path("second/artifact.yaml"),
            {"outputs": ["same.txt"]},
        )
        with self.assertRaisesRegex(ValueError, "declared by both"):
            ArtifactGeneratorRegistry((_Generator(first), _Generator(second)))


if __name__ == "__main__":
    unittest.main()
