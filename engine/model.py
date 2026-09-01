"""Typed manifests for executable Sail units and owner-local TeX topics."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
import re
from types import MappingProxyType

from .entity import Entity
from .extension import ExtensionMetadata, ExtensionSetCatalog
from .reference import Reference
from .yaml_document import SchemaValidatedYamlLoader, YamlDocumentLoader


class ModelError(ValueError):
    """Base class for a rejected model ownership or dependency relation."""


class MissingModelManifestError(ModelError):
    def __init__(self, source: Path) -> None:
        self.source = source
        super().__init__(f"required model manifest does not exist: {source}")


class ModelSourceOwnershipConflictError(ModelError):
    def __init__(
        self,
        manifest: Path,
        source: Path,
        first_owner: str,
        second_owner: str,
    ) -> None:
        self.manifest = manifest
        self.source = source
        self.first_owner = first_owner
        self.second_owner = second_owner
        super().__init__(
            f"{manifest}: source {source} is owned by both "
            f"{first_owner} and {second_owner}"
        )


class ModelSourceOutsideOwnerError(ModelError):
    def __init__(self, manifest: Path, owner: str, source: Path, root: Path) -> None:
        self.manifest = manifest
        self.owner = owner
        self.source = source
        self.root = root
        super().__init__(f"{manifest}: {owner} source {source} is outside {root}")


class InvalidTopicStructureError(ModelError):
    def __init__(
        self,
        manifest: Path,
        topic_id: str,
        document: Path,
        heading_count: int,
    ) -> None:
        self.manifest = manifest
        self.topic_id = topic_id
        self.document = document
        self.heading_count = heading_count
        super().__init__(
            f"{manifest}: document topic {topic_id!r} has {heading_count} headings "
            f"in {document}"
        )


class SailDependencyCycleError(ModelError):
    def __init__(
        self, source: Path, cycle: tuple[Reference["SailUnit"], ...]
    ) -> None:
        self.source = source
        self.cycle = cycle
        super().__init__(f"{source}: circular Sail dependency: {cycle!r}")


class UnknownSailDependencyError(ModelError):
    def __init__(
        self,
        source: Path,
        requiring: Reference["SailUnit"],
        required: Reference["SailUnit"],
    ) -> None:
        self.source = source
        self.requiring = requiring
        self.required = required
        super().__init__(f"{source}: {requiring!r} requires unknown unit {required!r}")


@dataclass(frozen=True, slots=True)
class SailUnit:
    """One dependency-ordered executable semantics unit."""

    owner: str
    id: str
    reference: Reference["SailUnit"]
    source: Path
    sources: tuple[Path, ...]
    requires: tuple[Reference["SailUnit"], ...]


@dataclass(frozen=True, slots=True)
class ExecutionProvider:
    """One owner-local implementation of the injectable execution boundaries."""

    owner: str
    source: Path
    provider: Path


@dataclass(frozen=True, slots=True)
class DocumentTopic(Entity):
    """One owner-local authored TeX source available to public composers."""

    owner: str
    id: str
    reference: Reference["DocumentTopic"]
    source: Path
    document: Path


@dataclass(frozen=True, slots=True)
class ModelNamespace:
    """The Sail units and document topics owned by base or one extension."""

    owner: str
    source: Path
    root: Path
    instruction_set: str | None
    fault_kinds: tuple[str, ...]
    sail_units: tuple[SailUnit, ...]
    execution_provider: ExecutionProvider | None
    document_topics: tuple[DocumentTopic, ...]


class ModelManifestLoader:
    """Load and validate one owner-local model manifest."""

    def __init__(self, schema: Mapping[str, object]) -> None:
        self.schema = schema

    def load(self, owner: str, root: str | Path) -> ModelNamespace:
        namespace_root = Path(root).resolve()
        source = namespace_root / "model.yaml"
        if not source.is_file():
            raise MissingModelManifestError(source)

        manifest = SchemaValidatedYamlLoader().load(source, self.schema)

        sail = manifest.get("sail", {})
        instruction_set = (
            str(sail["instruction_set"])
            if isinstance(sail, Mapping) and "instruction_set" in sail
            else None
        )
        fault_kinds = (
            tuple(str(item) for item in sail.get("fault_kinds", ()))
            if isinstance(sail, Mapping)
            else ()
        )
        sail_units = self._load_sail_units(owner, namespace_root, source, manifest)
        provider = self._load_execution_provider(
            owner, namespace_root, source, manifest, sail_units
        )
        topics = self._load_document_topics(owner, namespace_root, source, manifest)
        return ModelNamespace(
            owner,
            source,
            namespace_root,
            instruction_set,
            fault_kinds,
            sail_units,
            provider,
            topics,
        )

    @staticmethod
    def _load_sail_units(
        owner: str,
        root: Path,
        manifest_path: Path,
        manifest: Mapping[str, object],
    ) -> tuple[SailUnit, ...]:
        section = manifest.get("sail", {})
        raw_units = section.get("units", ()) if isinstance(section, Mapping) else ()
        units: list[SailUnit] = []
        seen: set[str] = set()
        owned_sources: dict[Path, str] = {}
        for raw in raw_units:
            unit_id = raw["id"]
            if unit_id in seen:
                raise ValueError(
                    f"{manifest_path}: duplicate Sail unit {owner}.{unit_id}"
                )
            seen.add(unit_id)
            sources = tuple(
                _owned_source(owner, root, item, ".sail", manifest_path)
                for item in raw["sources"]
            )
            for path in sources:
                previous = owned_sources.get(path)
                if previous is not None:
                    raise ModelSourceOwnershipConflictError(
                        manifest_path,
                        path,
                        f"{owner}.{previous}",
                        f"{owner}.{unit_id}",
                    )
                owned_sources[path] = unit_id
            units.append(
                SailUnit(
                    owner=owner,
                    id=unit_id,
                    reference=Reference.parse(f"{owner}.{unit_id}"),
                    source=manifest_path,
                    sources=sources,
                    requires=tuple(
                        Reference.parse(reference)
                        for reference in raw.get("requires", ())
                    ),
                )
            )
        return tuple(units)

    @staticmethod
    def _load_execution_provider(
        owner: str,
        root: Path,
        manifest_path: Path,
        manifest: Mapping[str, object],
        sail_units: tuple[SailUnit, ...],
    ) -> ExecutionProvider | None:
        section = manifest.get("sail", {})
        raw_provider = (
            section.get("execution_provider")
            if isinstance(section, Mapping)
            else None
        )
        if raw_provider is None:
            return None
        provider = _owned_source(
            owner, root, raw_provider, ".sail", manifest_path
        )
        for unit in sail_units:
            if provider in unit.sources:
                raise ModelSourceOwnershipConflictError(
                    manifest_path,
                    provider,
                    f"{owner}.{unit.id}",
                    f"{owner}.execution_provider",
                )
        return ExecutionProvider(owner, manifest_path, provider)

    @staticmethod
    def _load_document_topics(
        owner: str,
        root: Path,
        manifest_path: Path,
        manifest: Mapping[str, object],
    ) -> tuple[DocumentTopic, ...]:
        section = manifest.get("documents", {})
        raw_topics = section.get("topics", ()) if isinstance(section, Mapping) else ()
        topics: list[DocumentTopic] = []
        seen: set[str] = set()
        owned_sources: dict[Path, str] = {}
        for raw in raw_topics:
            topic_id = raw["id"]
            if topic_id in seen:
                raise ValueError(
                    f"{manifest_path}: duplicate document topic {owner}.{topic_id}"
                )
            seen.add(topic_id)
            document = _document_source(owner, root, raw["source"], manifest_path)
            _require_one_topic_heading(document, manifest_path, topic_id)
            previous = owned_sources.get(document)
            if previous is not None:
                raise ModelSourceOwnershipConflictError(
                    manifest_path,
                    document,
                    f"{owner}.{previous}",
                    f"{owner}.{topic_id}",
                )
            owned_sources[document] = topic_id
            topics.append(
                DocumentTopic(
                    owner=owner,
                    id=topic_id,
                    reference=Reference.parse(f"{owner}.{topic_id}"),
                    source=manifest_path,
                    document=document,
                )
            )
        return tuple(topics)


@dataclass(frozen=True, slots=True)
class ModelCatalog:
    """Independent Sail dependency and owner-local document catalogs."""

    base: ModelNamespace
    extensions: Mapping[str, ModelNamespace]
    sail_units: Mapping[Reference[SailUnit], SailUnit]
    sail_order: tuple[Reference[SailUnit], ...]
    document_topics: Mapping[Reference[DocumentTopic], DocumentTopic]

    @classmethod
    def load(
        cls,
        isa_root: str | Path,
        extension_catalog: ExtensionSetCatalog,
        extensions: Mapping[str, ExtensionMetadata],
    ) -> "ModelCatalog":
        return ModelCatalogLoader().load(isa_root, extension_catalog, extensions)


class ModelCatalogLoader:
    """Coordinate manifest loading and resolve only executable dependencies."""

    def load(
        self,
        isa_root: str | Path,
        extension_catalog: ExtensionSetCatalog,
        extensions: Mapping[str, ExtensionMetadata],
    ) -> ModelCatalog:
        root = Path(isa_root).resolve()
        extension_roots = {
            extension_id: extension_root
            for extension_id, extension_root in extension_catalog.owner_roots()[1:]
            if extension_root.is_dir()
        }
        schema = _load_mapping(root / "schemas/model.yaml")
        loader = ModelManifestLoader(schema)
        base = loader.load("base", root)
        namespaces = {
            extension_id: loader.load(extension_id, extension_root)
            for extension_id, extension_root in extension_roots.items()
        }
        return ModelDependencyResolver(extensions).resolve(base, namespaces)


class ModelDependencyResolver:
    """Resolve Sail dependencies and index owner-local document topics."""

    def __init__(self, extensions: Mapping[str, ExtensionMetadata]) -> None:
        self.extensions = extensions

    def resolve(
        self,
        base: ModelNamespace,
        extensions: Mapping[str, ModelNamespace],
    ) -> ModelCatalog:
        sail_units: dict[Reference[SailUnit], SailUnit] = {}
        topics: dict[Reference[DocumentTopic], DocumentTopic] = {}
        for namespace in (base, *extensions.values()):
            for unit in namespace.sail_units:
                if unit.reference in sail_units:
                    raise ValueError(f"duplicate Sail unit {unit.owner}.{unit.id}")
                sail_units[unit.reference] = unit
            for topic in namespace.document_topics:
                if topic.reference in topics:
                    raise ValueError(
                        f"duplicate document topic {topic.owner}.{topic.id}"
                    )
                topics[topic.reference] = topic

        sail_order = self._resolve_sail_units(sail_units)
        return ModelCatalog(
            base=base,
            extensions=MappingProxyType(dict(extensions)),
            sail_units=MappingProxyType(sail_units),
            sail_order=sail_order,
            document_topics=MappingProxyType(topics),
        )

    @staticmethod
    def _resolve_sail_units(
        units: Mapping[Reference[SailUnit], SailUnit],
    ) -> tuple[Reference[SailUnit], ...]:
        resolved: list[Reference[SailUnit]] = []
        complete: set[Reference[SailUnit]] = set()
        active: list[Reference[SailUnit]] = []

        def resolve(reference: Reference[SailUnit]) -> None:
            if reference in complete:
                return
            if reference in active:
                start = active.index(reference)
                cycle = (*active[start:], reference)
                raise SailDependencyCycleError(
                    units[reference].source, cycle
                )
            unit = units.get(reference)
            if unit is None:
                requiring = active[-1] if active else reference
                source = units[requiring].source if requiring in units else Path("model.yaml")
                raise UnknownSailDependencyError(source, requiring, reference)
            active.append(reference)
            for required in unit.requires:
                resolve(required)
            active.pop()
            complete.add(reference)
            resolved.append(reference)

        for reference in units:
            resolve(reference)
        return tuple(resolved)


def _owned_source(
    owner: str, root: Path, raw: object, suffix: str, manifest: Path
) -> Path:
    relative = Path(str(raw))
    path = (root / relative).resolve()
    if relative.is_absolute() or not path.is_relative_to(root) or path.suffix != suffix:
        raise ModelSourceOutsideOwnerError(manifest, owner, path, root)
    if owner == "base" and path.is_relative_to((root / "extensions").resolve()):
        raise ModelSourceOutsideOwnerError(manifest, owner, path, root)
    if not path.is_file():
        raise ValueError(f"{manifest}: required {owner} source does not exist: {path}")
    return path


def _document_source(owner: str, root: Path, raw: object, manifest: Path) -> Path:
    """Resolve owner-local topics plus artifact-owned document structure."""

    relative = Path(str(raw))
    if relative.parts and relative.parts[0] == "artifacts":
        repository = root.parent if owner == "base" else root.parents[2]
        path = (repository / relative).resolve()
        if (
            relative.is_absolute()
            or not path.is_relative_to(repository / "artifacts")
            or path.suffix != ".tex"
        ):
            raise ValueError(
                f"{manifest}: artifact document source {raw!r} escapes artifacts"
            )
        if not path.is_file():
            raise ValueError(
                f"{manifest}: required artifact document source does not exist: {path}"
            )
        return path
    return _owned_source(owner, root, raw, ".tex", manifest)


_TOPIC_HEADING = re.compile(
    r"^[ \t]*\\(?:part|chapter|section|subsection|subsubsection)\*?\{",
    re.MULTILINE,
)


def _require_one_topic_heading(document: Path, manifest: Path, topic_id: str) -> None:
    headings = _TOPIC_HEADING.findall(document.read_text(encoding="utf-8"))
    if len(headings) != 1:
        raise InvalidTopicStructureError(
            manifest, topic_id, document, len(headings)
        )


def _load_mapping(path: Path) -> dict[str, object]:
    return YamlDocumentLoader().mapping(path)
