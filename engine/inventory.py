"""Closed-world directory inventories shared by specification domains."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
from typing import Self

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

    @property
    def missing(self) -> tuple[str, ...]:
        """Declared members without a corresponding directory."""

        return tuple(sorted(set(self.declared) - set(self.actual)))

    @property
    def undeclared(self) -> tuple[str, ...]:
        """Member directories absent from the declaration."""

        return tuple(sorted(set(self.actual) - set(self.declared)))

    @property
    def duplicates(self) -> tuple[str, ...]:
        """Names declared more than once."""

        return tuple(
            sorted({value for value in self.declared if self.declared.count(value) > 1})
        )

    @classmethod
    def inspect(
        cls,
        *,
        owner: str,
        kind: str,
        source: str | Path,
        root: str | Path,
        key: str,
        allow_missing: bool = False,
        exact_keys: bool = False,
        validate_names: bool = False,
        name_pattern: str | None = None,
    ) -> Self:
        """Inspect membership without rejecting declared-versus-actual drift."""

        source_path = Path(source).resolve()
        root_path = Path(root).resolve()
        if not source_path.is_file():
            if not allow_missing:
                raise ValueError(f"required inventory does not exist: {source_path}")
            declared: tuple[str, ...] = ()
        else:
            document = YamlDocumentLoader().mapping(source_path)
            if exact_keys and set(document) != {key}:
                raise ValueError(
                    f"{source_path}: inventory keys must be exactly {key!r}"
                )
            values = document.get(key)
            if not isinstance(values, list) or any(
                not isinstance(value, str) for value in values
            ):
                raise ValueError(f"{source_path}: expected a {key} list of names")
            pattern = (
                name_pattern
                if name_pattern is not None
                else r"[A-Za-z][A-Za-z0-9_-]*" if validate_names else None
            )
            invalid = tuple(
                value
                for value in values
                if pattern is not None and re.fullmatch(pattern, value) is None
            )
            if invalid:
                raise ValueError(
                    f"{source_path}: invalid {key} names {invalid}; "
                    f"expected pattern {pattern!r}"
                )
            declared = tuple(values)
        actual = (
            tuple(
                sorted(
                    path.name
                    for path in root_path.iterdir()
                    if path.is_dir() and not path.name.startswith(".")
                )
            )
            if root_path.is_dir()
            else ()
        )
        return cls(owner, kind, source_path, root_path, declared, actual)

    def require_exact(self, key: str) -> Self:
        """Reject malformed closed-world membership and return this inventory."""

        if self.duplicates:
            raise ValueError(
                f"{self.source}: duplicate {key} entries {list(self.duplicates)}"
            )
        if not self.root.is_dir():
            raise ValueError(f"{self.source}: member directory is missing: {self.root}")
        if self.missing or self.undeclared:
            raise ValueError(
                f"{self.source}: declared {key} {self.declared}; "
                f"member directories are {self.actual}"
            )
        return self

    @classmethod
    def load_strict(
        cls,
        *,
        owner: str,
        kind: str,
        source: str | Path,
        root: str | Path,
        key: str,
        name_pattern: str = r"[A-Za-z][A-Za-z0-9_-]*",
    ) -> Self:
        return cls.inspect(
            owner=owner,
            kind=kind,
            source=source,
            root=root,
            key=key,
            exact_keys=True,
            name_pattern=name_pattern,
        ).require_exact(key)
