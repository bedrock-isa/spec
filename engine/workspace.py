"""Domain-neutral workspace exposed to artifact generators."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from types import MappingProxyType
from typing import Protocol, TypeVar

from .dependency import EntityDependency
from .entity import EntityCatalog
from .reference import QualifiedReference, Reference

_T = TypeVar("_T")


class SpecificationProvider(Protocol):
    """One domain exposed through the workspace's uniform entity contract."""

    entities: EntityCatalog

    def resolve(self, reference: Reference[_T]) -> _T: ...

    def entity_dependencies(self) -> tuple[EntityDependency, ...]: ...


@dataclass(frozen=True, slots=True)
class SpecWorkspace:
    """Repository root and named domain providers available to generators."""

    root: Path
    providers: Mapping[str, SpecificationProvider]

    @classmethod
    def create(
        cls, root: str | Path, providers: Mapping[str, SpecificationProvider]
    ) -> "SpecWorkspace":
        return cls(
            Path(root).resolve(),
            MappingProxyType(dict(providers)),
        )

    @classmethod
    def load(cls, root: str | Path) -> "SpecWorkspace":
        """Load the repository's declared, closed-world provider composition."""

        from abi.c.model import CAbiProject
        from abi.elf.model import ElfAbiProject
        from interfaces.c.model import CInterfaceProject

        from .project import IsaProject

        repository = Path(root).resolve()
        isa = IsaProject.load(repository / "isa")
        elf = ElfAbiProject.load(repository / "abi/elf", isa)
        c_abi = CAbiProject.load(repository / "abi/c")
        interface = CInterfaceProject.load(repository / "interfaces/c")
        workspace = cls.create(
            repository,
            {
                "isa": isa,
                "abi.elf": elf,
                "abi.c": c_abi,
                "interfaces.c": interface,
            },
        )
        elf.validate(workspace)
        c_abi.validate(workspace)
        interface.validate(workspace)
        return workspace

    def require_provider(self, name: str) -> SpecificationProvider:
        try:
            return self.providers[name]
        except KeyError as error:
            available = ", ".join(sorted(self.providers)) or "none"
            raise ValueError(
                f"workspace does not provide {name!r}; available providers: {available}"
            ) from error

    def resolve(
        self,
        reference: str | QualifiedReference[_T],
    ) -> _T:
        """Resolve a qualified reference through its owning provider."""

        qualified = QualifiedReference.parse(reference)
        provider = self.require_provider(qualified.domain)
        return provider.resolve(qualified.local)
