"""Domain-neutral workspace exposed to artifact generators."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from types import MappingProxyType
from typing import TYPE_CHECKING, Callable, TypeVar, cast

from .reference import QualifiedReference, Reference

if TYPE_CHECKING:
    from .project import IsaProject


_T = TypeVar("_T")


@dataclass(frozen=True, slots=True)
class SpecWorkspace:
    """Repository root and named domain providers available to generators."""

    root: Path
    providers: Mapping[str, object]

    @classmethod
    def create(
        cls, root: str | Path, providers: Mapping[str, object]
    ) -> "SpecWorkspace":
        return cls(
            Path(root).resolve(),
            MappingProxyType(dict(providers)),
        )

    @classmethod
    def from_isa(cls, project: "IsaProject") -> "SpecWorkspace":
        isa_root = project.root.resolve()
        repository = isa_root.parent
        providers: dict[str, object] = {"isa": project}
        elf_root = repository / "abi/elf"
        if elf_root.is_dir():
            from abi.elf.model import ElfAbiProject

            providers["abi.elf"] = ElfAbiProject.load(elf_root, project)
        c_abi_root = repository / "abi/c"
        if c_abi_root.is_dir():
            from abi.c.model import CAbiProject

            providers["abi.c"] = CAbiProject.load(c_abi_root)
        interface_root = repository / "interfaces/c"
        if interface_root.is_dir():
            from interfaces.c.model import CInterfaceProject

            providers["interfaces.c"] = CInterfaceProject.load(interface_root)
        workspace = cls.create(repository, providers)
        elf = providers.get("abi.elf")
        if elf is not None:
            validate = getattr(elf, "validate", None)
            if callable(validate):
                validate(workspace)
        c_abi = providers.get("abi.c")
        if c_abi is not None:
            validate = getattr(c_abi, "validate", None)
            if callable(validate):
                validate(workspace)
        interface = providers.get("interfaces.c")
        if interface is not None:
            validate = getattr(interface, "validate", None)
            if callable(validate):
                validate(workspace)
        return workspace

    def require_provider(self, name: str) -> object:
        try:
            return self.providers[name]
        except KeyError as error:
            available = ", ".join(sorted(self.providers)) or "none"
            raise ValueError(
                f"workspace does not provide {name!r}; available providers: {available}"
            ) from error

    def resolve(
        self,
        reference: QualifiedReference[_T],
    ) -> _T:
        """Resolve a qualified reference through its owning provider."""

        provider = self.require_provider(reference.domain)
        resolver = getattr(provider, "resolve", None)
        if callable(resolver):
            typed_resolver = cast(
                Callable[[Reference[_T]], _T], resolver
            )
            return typed_resolver(reference.local)
        entities = getattr(provider, "entities", None)
        if entities is not None and callable(getattr(entities, "resolve", None)):
            entity = entities.resolve(reference.local)
            return cast(_T, getattr(entity, "value", entity))
        raise ValueError(
            f"workspace provider {reference.domain!r} cannot resolve references"
        )
