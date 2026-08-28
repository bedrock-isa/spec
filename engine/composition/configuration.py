"""Dependency-closed ISA extension configurations."""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass

from ..project import IsaProject


@dataclass(frozen=True, slots=True)
class IsaConfiguration:
    """An ordered, dependency-closed set of active extensions."""

    extension_ids: tuple[str, ...]

    @classmethod
    def resolve(
        cls,
        project: IsaProject,
        requested: Iterable[str] | None = None,
    ) -> "IsaConfiguration":
        requested_ids = (
            tuple(project.catalog.extensions)
            if requested is None
            else tuple(dict.fromkeys(requested))
        )
        enabled: set[str] = set()

        def enable(extension_id: str) -> None:
            extension = project.extension(extension_id)
            for required in extension.requires:
                enable(required.id)
            enabled.add(extension_id)

        for extension_id in requested_ids:
            enable(extension_id)
        return cls(
            tuple(
                extension_id
                for extension_id in project.catalog.extensions
                if extension_id in enabled
            )
        )

    @property
    def owners(self) -> frozenset[str]:
        return frozenset(("base", *self.extension_ids))

    def enables(self, extension_id: str) -> bool:
        return extension_id in self.extension_ids
