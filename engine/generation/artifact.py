"""Common contracts and discovery for generated specification artifacts."""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Mapping
from dataclasses import dataclass
import importlib.util
import logging
from pathlib import Path
import re
from types import MappingProxyType
from ..observability import log_phase
from ..yaml_document import SchemaValidatedYamlLoader, YamlDocumentLoader
from ..workspace import SpecWorkspace, SpecificationProvider


_LOGGER = logging.getLogger(__name__)
_ARTIFACT_ID = re.compile(r"[a-z][a-z0-9]*(?:[._-][a-z0-9]+)*")


@dataclass(frozen=True, slots=True)
class GeneratedArtifact:
    relative_path: Path
    content: str | bytes

    def __post_init__(self) -> None:
        if (
            not self.relative_path.parts
            or self.relative_path == Path(".")
            or self.relative_path.is_absolute()
            or ".." in self.relative_path.parts
        ):
            raise ValueError(
                f"generated artifact path escapes output root: {self.relative_path}"
            )


@dataclass(frozen=True, slots=True)
class GeneratedArtifactSet:
    artifacts: tuple[GeneratedArtifact, ...]
    artifact_id: str

    def __post_init__(self) -> None:
        if not self.artifact_id:
            raise ValueError("generated artifact set requires a non-empty artifact id")
        paths = [artifact.relative_path for artifact in self.artifacts]
        duplicates = sorted({path for path in paths if paths.count(path) > 1})
        if duplicates:
            raise ValueError(f"duplicate generated artifact paths: {duplicates}")

    def artifact(self, relative_path: str | Path) -> GeneratedArtifact:
        wanted = Path(relative_path)
        matches = [item for item in self.artifacts if item.relative_path == wanted]
        if len(matches) != 1:
            raise ValueError(
                f"expected one generated artifact {wanted}, found {len(matches)}"
            )
        return matches[0]


@dataclass(frozen=True, slots=True)
class ArtifactDefinition:
    """One declarative artifact definition owned below ``artifacts``."""

    id: str
    source: Path
    data: Mapping[str, object]
    summary: str | None = None

    @property
    def dependencies(self) -> tuple[str, ...]:
        raw = self.data.get("depends-on", ())
        return tuple(str(item) for item in raw)

    @property
    def inputs(self) -> tuple[str, ...]:
        raw = self.data.get("inputs", ())
        return tuple(str(item) for item in raw)

    @property
    def outputs(self) -> Mapping[str, Path]:
        return self._output_mapping("outputs")

    @property
    def derived_outputs(self) -> Mapping[str, Path]:
        return self._output_mapping("derived-outputs", required=False)

    def _output_mapping(self, key: str, *, required: bool = True) -> Mapping[str, Path]:
        raw = self.data[key] if required else self.data.get(key, {})
        if not isinstance(raw, Mapping):
            raise ValueError(f"{self.source}: {key} must be a mapping")
        outputs = {str(name): Path(str(path)) for name, path in raw.items()}
        for name, path in outputs.items():
            if (
                not path.parts
                or path == Path(".")
                or path.is_absolute()
                or ".." in path.parts
            ):
                raise ValueError(
                    f"{self.source}: {key} root {name!r} escapes the output tree"
                )
        return MappingProxyType(outputs)

    @property
    def output_roots(self) -> tuple[Path, ...]:
        return (*self.outputs.values(), *self.derived_outputs.values())

    def validate_generated(self, artifacts: GeneratedArtifactSet) -> None:
        """Require the generated set to populate exactly its declared roots."""

        if artifacts.artifact_id != self.id:
            raise ValueError(
                f"{self.source}: generated owner {artifacts.artifact_id!r} does not "
                f"match artifact id {self.id!r}"
            )
        roots = tuple(self.outputs.values())
        self._validate_owned_paths(artifacts, roots)
        populated = {
            root
            for root in roots
            if any(
                artifact.relative_path == root
                or artifact.relative_path.is_relative_to(root)
                for artifact in artifacts.artifacts
            )
        }
        missing = tuple(root for root in roots if root not in populated)
        if missing:
            raise ValueError(
                f"{self.source}: generated set does not populate output roots "
                f"{[path.as_posix() for path in missing]}"
            )

    def validate_owned(self, artifacts: GeneratedArtifactSet) -> None:
        """Require every published path to belong to this declared artifact."""

        if artifacts.artifact_id != self.id:
            raise ValueError(
                f"{self.source}: generated owner {artifacts.artifact_id!r} does not "
                f"match artifact id {self.id!r}"
            )
        self._validate_owned_paths(artifacts, self.output_roots)

    def _validate_owned_paths(
        self, artifacts: GeneratedArtifactSet, roots: tuple[Path, ...]
    ) -> None:
        for artifact in artifacts.artifacts:
            owners = tuple(
                root
                for root in roots
                if artifact.relative_path == root
                or artifact.relative_path.is_relative_to(root)
            )
            if len(owners) != 1:
                raise ValueError(
                    f"{self.source}: generated path {artifact.relative_path} is "
                    f"owned by {len(owners)} declared output roots"
                )

    @classmethod
    def load(
        cls, path: str | Path, schema: Mapping[str, object]
    ) -> "ArtifactDefinition":
        source = Path(path).resolve()
        raw = SchemaValidatedYamlLoader().load(source, schema)
        artifact_id = source.parent.name
        if source.name != "artifact.yaml":
            raise ValueError(f"{source}: expected a file named artifact.yaml")
        if _ARTIFACT_ID.fullmatch(artifact_id) is None:
            raise ValueError(f"{source}: invalid artifact directory {artifact_id!r}")
        return cls(
            artifact_id,
            source,
            MappingProxyType(raw),
            str(raw["summary"]) if "summary" in raw else None,
        )


@dataclass(frozen=True, slots=True)
class ArtifactGenerationContext:
    """Domain-neutral inputs available to every artifact projection."""

    workspace: SpecWorkspace
    output_root: Path

    @classmethod
    def create(
        cls, workspace: SpecWorkspace, output_root: str | Path
    ) -> "ArtifactGenerationContext":
        return cls(workspace, Path(output_root).resolve())

    def require_provider(self, name: str) -> SpecificationProvider:
        return self.workspace.require_provider(name)


class ArtifactGenerator(ABC):
    """Pure projection from a specification workspace to an artifact file set."""

    def __init__(self, definition: ArtifactDefinition) -> None:
        self.definition = definition

    @property
    def artifact_id(self) -> str:
        return self.definition.id

    @abstractmethod
    def generate(self, context: ArtifactGenerationContext) -> GeneratedArtifactSet:
        """Render files without mutating the filesystem."""

    def validate(self, context: ArtifactGenerationContext) -> None:
        """Validate this projector without publishing its generated files."""

        artifacts = self.generate(context)
        self.definition.validate_generated(artifacts)


class ArtifactGeneratorRegistry:
    """Discover definitions and load artifact-owned generator entrypoints."""

    def __init__(self, generators: tuple[ArtifactGenerator, ...]) -> None:
        by_id: dict[str, ArtifactGenerator] = {}
        for generator in generators:
            if generator.artifact_id in by_id:
                raise ValueError(f"duplicate artifact id {generator.artifact_id!r}")
            by_id[generator.artifact_id] = generator
        self._generators = MappingProxyType(by_id)
        self._validate_dependencies()
        self._validate_output_ownership()

    @classmethod
    def discover(
        cls,
        workspace: SpecWorkspace,
    ) -> "ArtifactGeneratorRegistry":
        with log_phase(
            _LOGGER,
            "artifact.registry.discover",
            level=logging.DEBUG,
        ) as phase:
            schema_path = workspace.root / "artifacts/schema.yaml"
            schema_raw = YamlDocumentLoader().mapping(schema_path)
            artifact_root = workspace.root / "artifacts"
            definitions = tuple(sorted(artifact_root.glob("*/artifact.yaml")))
            generators: list[ArtifactGenerator] = []
            for path in definitions:
                definition = ArtifactDefinition.load(path, schema_raw)
                missing_inputs = sorted(
                    set(definition.inputs) - set(workspace.providers)
                )
                if missing_inputs:
                    raise ValueError(
                        f"{path}: unavailable artifact inputs {missing_inputs}"
                    )
                generators.append(cls._load_generator(definition))
            registry = cls(tuple(generators))
            phase["artifacts"] = len(registry.artifact_ids)
            return registry

    @staticmethod
    def _load_generator(definition: ArtifactDefinition) -> ArtifactGenerator:
        raw = definition.data.get("generator")
        if not isinstance(raw, str) or not raw:
            raise ValueError(
                f"{definition.source}: implemented artifact requires generator"
            )
        source = (definition.source.parent / raw).resolve()
        if not source.is_relative_to(definition.source.parent) or not source.is_file():
            raise ValueError(f"{definition.source}: invalid generator path {raw!r}")
        module_name = "_bedrock_artifact_" + definition.id.replace("-", "_")
        spec = importlib.util.spec_from_file_location(module_name, source)
        if spec is None or spec.loader is None:
            raise ValueError(f"{definition.source}: cannot load generator {source}")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        generator_type = getattr(module, "Generator", None)
        if not isinstance(generator_type, type) or not issubclass(
            generator_type, ArtifactGenerator
        ):
            raise ValueError(
                f"{source}: must export Generator as an ArtifactGenerator subclass"
            )
        return generator_type(definition)

    @property
    def artifact_ids(self) -> tuple[str, ...]:
        return tuple(self._generators)

    def generator(self, artifact_id: str) -> ArtifactGenerator:
        try:
            return self._generators[artifact_id]
        except KeyError as error:
            raise ValueError(f"unknown artifact {artifact_id!r}") from error

    def generate(
        self,
        artifact_id: str,
        workspace: SpecWorkspace,
        output_root: str | Path,
    ) -> GeneratedArtifactSet:
        with log_phase(_LOGGER, "artifact.generate", artifact=artifact_id) as phase:
            context = ArtifactGenerationContext.create(workspace, output_root)
            generator = self.generator(artifact_id)
            artifacts = generator.generate(context)
            generator.definition.validate_generated(artifacts)
            phase["files"] = len(artifacts.artifacts)
            return artifacts

    def validate(
        self,
        artifact_id: str,
        workspace: SpecWorkspace,
        output_root: str | Path,
    ) -> None:
        with log_phase(_LOGGER, "artifact.validate", artifact=artifact_id):
            context = ArtifactGenerationContext.create(workspace, output_root)
            self.generator(artifact_id).validate(context)

    def _validate_dependencies(self) -> None:
        active: list[str] = []
        complete: set[str] = set()

        def visit(artifact_id: str) -> None:
            if artifact_id in complete:
                return
            if artifact_id in active:
                start = active.index(artifact_id)
                cycle = (*active[start:], artifact_id)
                raise ValueError("circular artifact dependency: " + " -> ".join(cycle))
            active.append(artifact_id)
            generator = self._generators[artifact_id]
            for dependency in generator.definition.dependencies:
                if dependency not in self._generators:
                    raise ValueError(
                        f"{generator.definition.source}: unknown artifact dependency "
                        f"{dependency!r}"
                    )
                visit(dependency)
            active.pop()
            complete.add(artifact_id)

        for artifact_id in self._generators:
            visit(artifact_id)

    def _validate_output_ownership(self) -> None:
        owners: list[tuple[Path, str]] = []
        for artifact_id, generator in self._generators.items():
            for output in generator.definition.output_roots:
                for previous, previous_id in owners:
                    if (
                        output == previous
                        or output.is_relative_to(previous)
                        or previous.is_relative_to(output)
                    ):
                        raise ValueError(
                            f"artifact output root {output} owned by {artifact_id} "
                            f"overlaps {previous} owned by {previous_id}"
                        )
                owners.append((output, artifact_id))
