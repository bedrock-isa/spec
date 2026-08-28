"""Closed-world directory inventories shared by specification domains."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re

from .yaml_document import YamlDocumentLoader


@dataclass(frozen=True, slots=True)
class DirectoryInventory:
    """One ordered YAML inventory paired with its member directories."""

    owner: str
    kind: str
    source: Path
    root: Path
    declared: tuple[str, ...]
    actual: tuple[str, ...]

    @classmethod
    def load(
        cls,
        *,
        owner: str,
        kind: str,
        source: str | Path,
        root: str | Path,
        key: str,
    ) -> "DirectoryInventory":
        source_path = Path(source).resolve()
        root_path = Path(root).resolve()
        document = YamlDocumentLoader().mapping(source_path)
        if set(document) != {key}:
            raise ValueError(
                f"{source_path}: inventory keys must be exactly {key!r}"
            )
        values = document.get(key)
        if not isinstance(values, list) or any(
            not isinstance(value, str)
            or re.fullmatch(r"[A-Za-z][A-Za-z0-9_-]*", value) is None
            for value in values
        ):
            raise ValueError(f"{source_path}: expected a {key} list of names")
        declared = tuple(values)
        duplicates = sorted(
            {value for value in declared if declared.count(value) > 1}
        )
        if duplicates:
            raise ValueError(f"{source_path}: duplicate {key} entries {duplicates}")
        if not root_path.is_dir():
            raise ValueError(f"{source_path}: member directory is missing: {root_path}")
        actual = tuple(
            sorted(
                path.name
                for path in root_path.iterdir()
                if path.is_dir() and not path.name.startswith(".")
            )
        )
        if set(declared) != set(actual):
            raise ValueError(
                f"{source_path}: declared {key} {declared}; "
                f"member directories are {actual}"
            )
        return cls(owner, kind, source_path, root_path, declared, actual)
