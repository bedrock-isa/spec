"""Common contracts and discovery for generated specification artifacts."""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Mapping
from dataclasses import dataclass
import importlib.util
from pathlib import Path
from types import MappingProxyType
from typing import TYPE_CHECKING

from ..yaml_document import SchemaValidatedYamlLoader, YamlDocumentLoader
from ..workspace import SpecWorkspace

if TYPE_CHECKING:
    from ..project import IsaProject


@dataclass(frozen=True, slots=True)
class GeneratedArtifact:
    relative_path: Path
    content: str

    def __post_init__(self) -> None:
        if self.relative_path.is_absolute() or ".." in self.relative_path.parts:
            raise ValueError(f"generated artifact path escapes output root: {self.relative_path}")


@dataclass(frozen=True, slots=True)
class GeneratedArtifactSet:
    artifacts: tuple[GeneratedArtifact, ...]
    artifact_id: str | None = None

    def __post_init__(self) -> None:
        paths = [artifact.relative_path for artifact in self.artifacts]
        duplicates = sorted({path for path in paths if paths.count(path) > 1})
        if duplicates:
            raise ValueError(f"duplicate generated artifact paths: {duplicates}")

    def artifact(self, relative_path: str | Path) -> GeneratedArtifact:
        wanted = Path(relative_path)
        matches = [item for item in self.artifacts if item.relative_path == wanted]
        if len(matches) != 1:
            raise ValueError(f"expected one generated artifact {wanted}, found {len(matches)}")
        return matches[0]


@dataclass(frozen=True, slots=True)
class ArtifactDefinition:
    """One declarative artifact definition owned below ``artifacts``."""

    id: str
    source: Path
    data: Mapping[str, object]
    status: str = "implemented"
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
    def declared_outputs(self) -> tuple[Path, ...]:
        if "output" in self.data:
            values = [Path(str(self.data["output"]))]
            if "dependency-graph" in self.data:
                values.append(Path(str(self.data["dependency-graph"])))
            return tuple(values)
        raw = self.data.get("outputs", ())
        values = raw.values() if isinstance(raw, Mapping) else raw
        return tuple(Path(str(item)) for item in values)

    @classmethod
    def load(cls, path: str | Path, schema: Mapping[str, object]) -> "ArtifactDefinition":
        source = Path(path).resolve()
        raw = SchemaValidatedYamlLoader().load(source, schema)
        return cls(
            raw["id"],
            source,
            MappingProxyType(raw),
            str(raw.get("status", "implemented")),
            str(raw["summary"]) if "summary" in raw else None,
        )


@dataclass(frozen=True, slots=True)
class ArtifactGenerationContext:
    """Domain-neutral inputs available to every artifact projection."""

    workspace: SpecWorkspace
    output_root: Path

    @classmethod
    def create(
        cls, workspace: SpecWorkspace | "IsaProject", output_root: str | Path
    ) -> "ArtifactGenerationContext":
        if not isinstance(workspace, SpecWorkspace):
            workspace = SpecWorkspace.from_isa(workspace)
        return cls(workspace, Path(output_root).resolve())

    def require_provider(self, name: str) -> object:
        return self.workspace.require_provider(name)

class ArtifactGenerator(ABC):
    """Pure projection from a specification workspace to an artifact file set."""

    def __init__(self, definition: ArtifactDefinition) -> None:
        self.definition = definition

    @property
    def artifact_id(self) -> str:
        return self.definition.id

    @property
    def status(self) -> str:
        return self.definition.status

    @abstractmethod
    def generate(self, context: ArtifactGenerationContext) -> GeneratedArtifactSet:
        """Render files without mutating the filesystem."""


class PlannedArtifactGenerator(ArtifactGenerator):
    """Visible registry placeholder for an intentionally unimplemented artifact."""

    def generate(self, context: ArtifactGenerationContext) -> GeneratedArtifactSet:
        raise NotImplementedError(
            f"artifact {self.artifact_id!r} is planned but not implemented"
        )


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
        workspace: SpecWorkspace | "IsaProject",
    ) -> "ArtifactGeneratorRegistry":
        if not isinstance(workspace, SpecWorkspace):
            workspace = SpecWorkspace.from_isa(workspace)
        schema_path = workspace.root / "artifacts/schema.yaml"
        schema_raw = YamlDocumentLoader().mapping(schema_path)
        artifact_root = workspace.root / "artifacts"
        definitions = tuple(sorted(artifact_root.glob("*/artifact.yaml")))
        generators: list[ArtifactGenerator] = []
        for path in definitions:
            definition = ArtifactDefinition.load(path, schema_raw)
            missing_inputs = sorted(set(definition.inputs) - set(workspace.providers))
            if missing_inputs:
                raise ValueError(
                    f"{path}: unavailable artifact inputs {missing_inputs}"
                )
            if definition.status == "planned":
                generators.append(PlannedArtifactGenerator(definition))
                continue
            generators.append(cls._load_generator(definition))
        return cls(tuple(generators))

    @staticmethod
    def _load_generator(definition: ArtifactDefinition) -> ArtifactGenerator:
        raw = definition.data.get("generator")
        if not isinstance(raw, str) or not raw:
            raise ValueError(f"{definition.source}: implemented artifact requires generator")
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

    @property
    def implemented_ids(self) -> tuple[str, ...]:
        return tuple(
            artifact_id
            for artifact_id, generator in self._generators.items()
            if generator.status == "implemented"
        )

    def generator(self, artifact_id: str) -> ArtifactGenerator:
        try:
            return self._generators[artifact_id]
        except KeyError as error:
            raise ValueError(f"unknown artifact {artifact_id!r}") from error

    def generate(
        self,
        artifact_id: str,
        workspace: SpecWorkspace | "IsaProject",
        output_root: str | Path,
    ) -> GeneratedArtifactSet:
        context = ArtifactGenerationContext.create(workspace, output_root)
        return self.generator(artifact_id).generate(context)

    def _validate_dependencies(self) -> None:
        active: list[str] = []
        complete: set[str] = set()

        def visit(artifact_id: str) -> None:
            if artifact_id in complete:
                return
            if artifact_id in active:
                start = active.index(artifact_id)
                cycle = (*active[start:], artifact_id)
                raise ValueError(
                    "circular artifact dependency: " + " -> ".join(cycle)
                )
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
        owners: dict[Path, str] = {}
        for artifact_id, generator in self._generators.items():
            for output in generator.definition.declared_outputs:
                previous = owners.get(output)
                if previous is not None:
                    raise ValueError(
                        f"artifact output {output} is declared by both {previous} "
                        f"and {artifact_id}"
                    )
                owners[output] = artifact_id
