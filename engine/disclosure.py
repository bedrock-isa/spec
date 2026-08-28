"""Typed implementation-defined disclosure registry."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .yaml_document import SchemaValidatedYamlLoader


@dataclass(frozen=True, slots=True)
class ImplementationDisclosure:
    id: str
    item: str
    defining_rules: tuple[str, ...]
    publication: str


@dataclass(frozen=True, slots=True)
class ImplementationDisclosureCatalog:
    source: Path
    disclosures: tuple[ImplementationDisclosure, ...]

    @classmethod
    def load(cls, isa_root: str | Path) -> "ImplementationDisclosureCatalog":
        root = Path(isa_root).resolve()
        source = root / "implementation_disclosures.yaml"
        schema_source = root / "schemas/implementation-disclosures.yaml"
        if not source.is_file():
            return cls(source, ())
        document = SchemaValidatedYamlLoader().load(source, schema_source)
        seen: set[str] = set()
        disclosures = []
        for raw in document["disclosures"]:
            if raw["id"] in seen:
                raise ValueError(f"{source}: duplicate disclosure {raw['id']}")
            seen.add(raw["id"])
            disclosures.append(
                ImplementationDisclosure(
                    id=raw["id"],
                    item=raw["item"],
                    defining_rules=tuple(raw["defining_rules"]),
                    publication=raw["publication"],
                )
            )
        return cls(source, tuple(disclosures))
