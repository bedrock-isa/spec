"""Typed manifests for executable Sail units and reader-ordered TeX topics."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
import re
from types import MappingProxyType

try:
    from .extension import ExtensionMetadata, ExtensionSetCatalog
    from .reference import Reference
    from .yaml_document import SchemaValidatedYamlLoader, YamlDocumentLoader
except ImportError:  # Support loading engine directly on PYTHONPATH.
    from extension import ExtensionMetadata, ExtensionSetCatalog
    from reference import Reference
    from yaml_document import SchemaValidatedYamlLoader, YamlDocumentLoader


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
class DocumentTopic:
    """One authored TeX source representing one reader-facing subtopic."""

    owner: str
    id: str
    reference: Reference["DocumentTopic"]
    source: Path
    document: Path
    artifact: str
    concept: str | None



@dataclass(frozen=True, slots=True)
class ModelNamespace:
    """The Sail units and document topics owned by base or one extension."""

    owner: str
    source: Path
    root: Path
    sail_units: tuple[SailUnit, ...]
    document_topics: tuple[DocumentTopic, ...]


class ModelManifestLoader:
    """Load and validate one owner-local model manifest."""

    def __init__(self, schema: Mapping[str, object]) -> None:
        self.schema = schema

    def load(self, owner: str, root: str | Path) -> ModelNamespace:
        namespace_root = Path(root).resolve()
        source = namespace_root / "model.yaml"
        if not source.is_file():
            raise FileNotFoundError(f"required model manifest does not exist: {source}")

        manifest = SchemaValidatedYamlLoader().load(source, self.schema)

        sail_units = self._load_sail_units(owner, namespace_root, source, manifest)
        topics = self._load_document_topics(owner, namespace_root, source, manifest)
        return ModelNamespace(owner, source, namespace_root, sail_units, topics)

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
                raise ValueError(f"{manifest_path}: duplicate Sail unit {owner}.{unit_id}")
            seen.add(unit_id)
            sources = tuple(
                _owned_source(owner, root, item, ".sail", manifest_path)
                for item in raw["sources"]
            )
            for path in sources:
                previous = owned_sources.get(path)
                if previous is not None:
                    raise ValueError(
                        f"{manifest_path}: Sail source {path} is owned by both "
                        f"{owner}.{previous} and {owner}.{unit_id}"
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
                raise ValueError(
                    f"{manifest_path}: document source {document} is owned by both "
                    f"{owner}.{previous} and {owner}.{topic_id}"
                )
            owned_sources[document] = topic_id
            topics.append(
                DocumentTopic(
                    owner=owner,
                    id=topic_id,
                    reference=Reference.parse(f"{owner}.{topic_id}"),
                    source=manifest_path,
                    document=document,
                    artifact=raw.get("artifact", "isa-reference"),
                    concept=raw.get("concept"),
                )
            )
        return tuple(topics)


@dataclass(frozen=True, slots=True)
class ModelCatalog:
    """Independent Sail dependency and TeX reading-order catalogs."""

    base: ModelNamespace
    extensions: Mapping[str, ModelNamespace]
    sail_units: Mapping[Reference[SailUnit], SailUnit]
    sail_order: tuple[Reference[SailUnit], ...]
    document_topics: Mapping[Reference[DocumentTopic], DocumentTopic]
    document_order: tuple[Reference[DocumentTopic], ...]
    document_orders: Mapping[str, tuple[Reference[DocumentTopic], ...]]

    @classmethod
    def load(
        cls,
        isa_root: str | Path,
        extension_catalog: ExtensionSetCatalog,
        extensions: Mapping[str, ExtensionMetadata],
    ) -> "ModelCatalog":
        return ModelCatalogLoader().load(isa_root, extension_catalog, extensions)

    def selected_document_topics(
        self,
        owners: set[str] | frozenset[str],
        artifact: str = "isa-reference",
    ) -> tuple[DocumentTopic, ...]:
        """Return TeX topics in authored compile order for selected owners."""

        return tuple(
            self.document_topics[reference]
            for reference in self.document_order
            if self.document_topics[reference].owner in owners
            and self.document_topics[reference].artifact == artifact
        )


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
            extension_id: extension_catalog.root / extension_id
            for extension_id in extension_catalog.declared
            if (extension_catalog.root / extension_id).is_dir()
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
    """Resolve Sail dependencies while preserving authored document order."""

    def __init__(self, extensions: Mapping[str, ExtensionMetadata]) -> None:
        self.extensions = extensions

    def resolve(
        self,
        base: ModelNamespace,
        extensions: Mapping[str, ModelNamespace],
    ) -> ModelCatalog:
        sail_units: dict[Reference[SailUnit], SailUnit] = {}
        topics: dict[Reference[DocumentTopic], DocumentTopic] = {}
        topic_order: list[Reference[DocumentTopic]] = []
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
                topic_order.append(topic.reference)

        sail_order = self._resolve_sail_units(sail_units)
        document_orders: dict[str, list[Reference[DocumentTopic]]] = {}
        for reference in topic_order:
            topic = topics[reference]
            document_orders.setdefault(topic.artifact, []).append(reference)
        return ModelCatalog(
            base=base,
            extensions=MappingProxyType(dict(extensions)),
            sail_units=MappingProxyType(sail_units),
            sail_order=sail_order,
            document_topics=MappingProxyType(topics),
            document_order=tuple(topic_order),
            document_orders=MappingProxyType(
                {key: tuple(value) for key, value in document_orders.items()}
            ),
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
                raise ValueError(
                    "circular Sail dependency"
                )
            unit = units.get(reference)
            if unit is None:
                requiring = active[-1] if active else reference
                raise ValueError(
                    "unknown required Sail unit"
                )
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
        raise ValueError(f"{manifest}: {owner} source {raw!r} is outside {root}")
    if owner == "base" and path.is_relative_to((root / "extensions").resolve()):
        raise ValueError(f"{manifest}: base source {raw!r} is owned by an extension")
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


def _require_one_topic_heading(
    document: Path, manifest: Path, topic_id: str
) -> None:
    headings = _TOPIC_HEADING.findall(document.read_text(encoding="utf-8"))
    if len(headings) != 1:
        raise ValueError(
            f"{manifest}: document topic {topic_id!r} must contain exactly one "
            f"section heading, found {len(headings)} in {document}"
        )


def _load_mapping(path: Path) -> dict[str, object]:
    return YamlDocumentLoader().mapping(path)
