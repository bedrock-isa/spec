"""Declared extension metadata and closed-world extension inventory."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .yaml_document import SchemaValidatedYamlLoader, YamlDocumentLoader


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


@dataclass(frozen=True, slots=True)
class ExtensionSetCatalog:
    """The closed-world inventory of extension directories."""

    source: Path
    root: Path
    declared: tuple[str, ...]
    actual: tuple[str, ...]

    @classmethod
    def load(cls, isa_root: str | Path) -> "ExtensionSetCatalog":
        root = Path(isa_root) / "extensions"
        source = root / "extensions.yaml"
        declared = _load_name_list(source, "extensions") if source.is_file() else ()
        actual = (
            tuple(
                sorted(
                    path.name
                    for path in root.iterdir()
                    if path.is_dir() and not path.name.startswith(".")
                )
            )
            if root.is_dir()
            else ()
        )
        return cls(source, root, declared, actual)


def _load_name_list(path: Path, key: str) -> tuple[str, ...]:
    document = _load_mapping(path)
    values = document.get(key)
    if not isinstance(values, list) or any(
        not isinstance(value, str) for value in values
    ):
        raise ValueError(f"{path}: expected a {key} list of strings")
    return tuple(values)


def _load_mapping(path: Path) -> dict[str, object]:
    return YamlDocumentLoader().mapping(path)
