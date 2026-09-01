"""Declared extension metadata and closed-world extension inventory."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .inventory import DirectoryInventory
from .yaml_document import SchemaValidatedYamlLoader


@dataclass(frozen=True, slots=True)
class ExtensionMetadata:
    """Schema-decoded metadata from one ``extension.yaml`` file."""

    id: str
    name: str
    requires: tuple[str, ...]
    required_cpuid_flags: tuple[str, ...]
    source: Path
    root: Path

    @classmethod
    def load(cls, path: str | Path, isa_root: str | Path) -> "ExtensionMetadata":
        source = Path(path)
        root = Path(isa_root)
        document = SchemaValidatedYamlLoader().load(
            source, root / "schemas/extension.yaml"
        )
        if document["id"] != source.parent.name:
            raise ValueError(
                f"{source}: extension ID {document['id']!r} does not match "
                f"directory {source.parent.name!r}"
            )
        return cls(
            id=document["id"],
            name=document["name"],
            requires=tuple(document.get("requires", ())),
            required_cpuid_flags=tuple(document.get("required_cpuid_flags", ())),
            source=source,
            root=source.parent,
        )


class ExtensionSetCatalog(DirectoryInventory):
    """The closed-world inventory of extension directories."""

    def owner_roots(self) -> tuple[tuple[str, Path], ...]:
        """Return base and declared extension roots in declaration order."""

        return (
            ("base", self.root.parent),
            *(
                (extension_id, self.root / extension_id)
                for extension_id in self.declared
            ),
        )

    @classmethod
    def load(cls, isa_root: str | Path) -> "ExtensionSetCatalog":
        root = Path(isa_root) / "extensions"
        return cls.inspect(
            owner="isa",
            kind="extension",
            source=root / "extensions.yaml",
            root=root,
            key="extensions",
            allow_missing=True,
        )
