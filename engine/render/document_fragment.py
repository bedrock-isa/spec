"""Composable expansion of generated fragments inside authored document topics."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..project import IsaProject


@dataclass(frozen=True, slots=True)
class DocumentFragmentContext:
    """Typed source-model context shared by topic fragment providers."""

    project: "IsaProject"
    source: Path | None = None


class DocumentFragmentProvider(ABC):
    """Expand one independently owned generated-fragment vocabulary."""

    @property
    @abstractmethod
    def placeholders(self) -> frozenset[str]:
        """Return the placeholder vocabulary exclusively owned by this provider."""

    @abstractmethod
    def expand(self, text: str, context: DocumentFragmentContext) -> str:
        """Return topic text with this provider's placeholders expanded."""


class DocumentFragmentPipeline:
    """Apply registered fragment providers in explicit deterministic order."""

    def __init__(self, providers: tuple[DocumentFragmentProvider, ...]) -> None:
        owned: dict[str, DocumentFragmentProvider] = {}
        for provider in providers:
            for placeholder in provider.placeholders:
                previous = owned.get(placeholder)
                if previous is not None:
                    raise ValueError(
                        f"document fragment placeholder {placeholder!r} is owned by "
                        f"both {type(previous).__name__} and {type(provider).__name__}"
                    )
                owned[placeholder] = provider
        self.providers = providers

    @classmethod
    def default(cls) -> "DocumentFragmentPipeline":
        from .cpuid_reference import CpuidEntityReferenceRenderer
        from .ea_diagram import EaDiagramFragmentRenderer
        from .event_reference import EventReferenceRenderer
        from .implementation_disclosure import ImplementationDisclosureRenderer
        from .register_model_figure import RegisterModelFigureRenderer
        from .registry_anchor import RegistryAnchorRenderer
        from .type_reference import EncodingTypeReferenceRenderer

        return cls(
            (
                CpuidEntityReferenceRenderer(),
                EncodingTypeReferenceRenderer(),
                EaDiagramFragmentRenderer(),
                EventReferenceRenderer(),
                ImplementationDisclosureRenderer(),
                RegisterModelFigureRenderer(),
                RegistryAnchorRenderer(),
            )
        )

    def expand(
        self, text: str, project: "IsaProject", source: Path | None = None
    ) -> str:
        context = DocumentFragmentContext(project, source)
        for provider in self.providers:
            text = provider.expand(text, context)
        return text
