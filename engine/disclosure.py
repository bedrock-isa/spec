"""Typed implementation-defined disclosure registry."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .extension import ExtensionSetCatalog
from .yaml_document import SchemaValidatedYamlLoader


@dataclass(frozen=True, slots=True)
class ImplementationDisclosure:
    owner: str
    source: Path
    id: str
    item: str
    defining_rules: tuple[str, ...]
    publication: str


@dataclass(frozen=True, slots=True)
class ImplementationDisclosureCatalog:
    sources: tuple[Path, ...]
    disclosures: tuple[ImplementationDisclosure, ...]

    @classmethod
    def load(
        cls,
        isa_root: str | Path,
        extension_catalog: ExtensionSetCatalog | None = None,
    ) -> "ImplementationDisclosureCatalog":
        root = Path(isa_root).resolve()
        schema_source = root / "schemas/implementation-disclosures.yaml"
        extensions = extension_catalog or ExtensionSetCatalog.load(root)
        seen: set[str] = set()
        disclosures = []
        sources = []
        for owner, namespace_root in extensions.owner_roots():
            source = namespace_root / "implementation_disclosures.yaml"
            if not source.is_file():
                continue
            sources.append(source)
            document = SchemaValidatedYamlLoader().load(source, schema_source)
            for raw in document["disclosures"]:
                if raw["id"] in seen:
                    raise ValueError(f"{source}: duplicate disclosure {raw['id']}")
                seen.add(raw["id"])
                disclosures.append(
                    ImplementationDisclosure(
                        owner=owner,
                        source=source,
                        id=raw["id"],
                        item=raw["item"],
                        defining_rules=tuple(raw["defining_rules"]),
                        publication=raw["publication"],
                    )
                )
        return cls(tuple(sources), tuple(disclosures))
