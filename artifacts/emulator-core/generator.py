"""Generate the Sail C core and its host-facing C adapter."""

from __future__ import annotations

import hashlib
from importlib import import_module
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

from engine.generation import (
    ArtifactDefinition,
    ArtifactGenerationContext,
    ArtifactGenerator,
    ArtifactWriter,
    GeneratedArtifact,
    GeneratedArtifactSet,
)
from engine.yaml_document import YamlDocumentLoader


_TEMPLATE_ROOT = Path(__file__).with_name("templates")
_PRESERVED_FUNCTIONS = (
    "initial_cpu",
    "platform_reset",
    "decode_and_execute_full",
    "resume_transaction",
    "post_interrupt",
    "advance_time",
)


def _template(name: str) -> str:
    return (_TEMPLATE_ROOT / name).read_text()


class SailCCompiler:
    """Invoke Sail's C backend for one generated project."""

    def __init__(self, executable: str | None = None) -> None:
        self.executable = executable or os.environ.get("SAIL", "sail")

    def cache_key(self) -> str:
        result = subprocess.run(
            [self.executable, "--version"], capture_output=True, text=True
        )
        if result.returncode != 0:
            raise RuntimeError(
                "Sail version query failed\n"
                f"stdout:\n{result.stdout}\n"
                f"stderr:\n{result.stderr}"
            )
        executable = shutil.which(self.executable) or self.executable
        return f"{Path(executable).resolve()}\n{result.stdout}{result.stderr}"

    def compile(self, project: Path, output_prefix: Path) -> tuple[str, str]:
        command = [
            self.executable,
            "--project",
            str(project),
            "--all-modules",
            "-c",
            "--c-no-main",
            "-O",
            "--static",
            "--c-specialize",
            "--Oconstant-fold",
        ]
        for function in _PRESERVED_FUNCTIONS:
            command.extend(("--c-preserve", function))
        command.extend(("-o", str(output_prefix)))
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(
                "Sail C generation failed\n"
                f"stdout:\n{result.stdout}\n"
                f"stderr:\n{result.stderr}"
            )
        return (
            output_prefix.with_suffix(".c").read_text(),
            output_prefix.with_suffix(".h").read_text(),
        )


class Generator(ArtifactGenerator):
    """Compile the generated Sail model and attach its C adapter."""

    def __init__(
        self,
        definition: ArtifactDefinition,
        compiler: SailCCompiler | None = None,
    ) -> None:
        super().__init__(definition)
        self.compiler = compiler or SailCCompiler()

    def generate(self, context: ArtifactGenerationContext) -> GeneratedArtifactSet:
        outputs = self.definition.outputs
        # Sail project files do not quote paths. Keeping the temporary model
        # next to the ISA tree prevents repository names containing '-' from
        # appearing in generated relative paths without touching Cargo's
        # watched ISA directory.
        temporary_parent = context.workspace.root
        with tempfile.TemporaryDirectory(
            prefix="bedrock-emulator-core-", dir=temporary_parent
        ) as directory:
            root = Path(directory).resolve()
            model_root = root / "model"
            model = self._sail_model_generator(context)
            model_context = ArtifactGenerationContext.create(
                context.workspace, model_root
            )
            model_artifacts = model.generate(model_context)
            model.definition.validate_generated(model_artifacts)
            ArtifactWriter().write(model_artifacts, model_root)
            compiler_cache_key = getattr(self.compiler, "cache_key", None)
            cacheable = callable(compiler_cache_key)
            fingerprint = _generation_fingerprint(
                model_artifacts,
                compiler_cache_key() if cacheable else type(self.compiler).__qualname__,
                context.workspace.root / "isa",
            )

            cached_c = context.output_root / outputs["implementation"]
            cached_h = context.output_root / outputs["model-header"]
            cached_stamp = context.output_root / outputs["generation-stamp"]
            cache_hit = (
                cacheable
                and cached_c.is_file()
                and cached_h.is_file()
                and cached_stamp.is_file()
                and cached_stamp.read_text() == fingerprint
            )
            if cache_hit:
                generated_c = cached_c.read_text()
                generated_h = cached_h.read_text()
            else:
                generated_c, generated_h = self.compiler.compile(
                    model_root / model.definition.outputs["project"],
                    root / "bedrock_core",
                )
                generated_c = _supply_library_main(
                    generated_c, _template("model_main.c")
                )
                generated_c += "\n" + _template("bedrock_core_adapter.c")

        return GeneratedArtifactSet(
            (
                GeneratedArtifact(
                    outputs["implementation"],
                    generated_c,
                ),
                GeneratedArtifact(outputs["model-header"], generated_h),
                GeneratedArtifact(
                    outputs["abi-header"],
                    _template("bedrock_core_abi.h"),
                ),
                GeneratedArtifact(outputs["generation-stamp"], fingerprint),
            ),
            self.artifact_id,
        )

    def validate(self, context: ArtifactGenerationContext) -> None:
        """Validate the source projection without invoking the Sail compiler."""

        model = self._sail_model_generator(context)
        model_context = ArtifactGenerationContext.create(
            context.workspace, context.output_root / "sail-model"
        )
        model_artifacts = model.generate(model_context)
        model.definition.validate_generated(model_artifacts)

        for template in (
            "model_main.c",
            "bedrock_core_adapter.c",
            "bedrock_core_abi.h",
        ):
            _template(template)

        outputs = self.definition.outputs
        projected = GeneratedArtifactSet(
            tuple(
                GeneratedArtifact(outputs[name], b"")
                for name in (
                    "implementation",
                    "model-header",
                    "abi-header",
                    "generation-stamp",
                )
            ),
            artifact_id=self.artifact_id,
        )
        self.definition.validate_generated(projected)

    @staticmethod
    def _sail_model_generator(context: ArtifactGenerationContext) -> ArtifactGenerator:
        workspace_root = context.workspace.root
        schema = YamlDocumentLoader().mapping(workspace_root / "artifacts/schema.yaml")
        definition = ArtifactDefinition.load(
            workspace_root / "artifacts/sail-model/artifact.yaml", schema
        )
        generator_type = import_module("artifacts.sail-model.generator").Generator
        return generator_type(definition)


def _generation_fingerprint(
    model: GeneratedArtifactSet, compiler_cache_key: str, sail_source_root: Path
) -> str:
    digest = hashlib.sha256()
    digest.update(b"bedrock-emulator-core-generation\0")
    digest.update(Path(__file__).read_bytes())
    digest.update(b"\0")
    digest.update(compiler_cache_key.encode())
    for artifact in sorted(model.artifacts, key=lambda item: item.relative_path):
        digest.update(b"\0path\0")
        digest.update(artifact.relative_path.as_posix().encode())
        digest.update(b"\0content\0")
        digest.update(artifact.content.encode())
    for source in sorted(sail_source_root.rglob("*.sail")):
        digest.update(b"\0sail-source\0")
        digest.update(source.relative_to(sail_source_root).as_posix().encode())
        digest.update(b"\0")
        digest.update(source.read_bytes())
    for template in sorted(_TEMPLATE_ROOT.iterdir()):
        if template.is_file():
            digest.update(b"\0template\0")
            digest.update(template.name.encode())
            digest.update(b"\0")
            digest.update(template.read_bytes())
    return digest.hexdigest() + "\n"


def _supply_library_main(generated_c: str, library_main: str) -> str:
    """Satisfy Sail 0.20's retained model_main in --c-no-main output."""
    if "unit zmain(" in generated_c:
        return generated_c
    marker = '#include "bedrock_core.h"\n'
    if generated_c.count(marker) != 1:
        raise ValueError("generated Sail C is missing its model header include")
    return generated_c.replace(marker, marker + library_main, 1)
