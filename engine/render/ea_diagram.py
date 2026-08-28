"""Generated EA encoding and address-flow diagrams for the ISA reference."""

from __future__ import annotations

from ..generate_ea_diagrams import render_catalog
from .document_fragment import DocumentFragmentContext, DocumentFragmentProvider


class EaDiagramFragmentRenderer(DocumentFragmentProvider):
    """Expand the EA diagram island from the project's loaded source catalog."""

    PLACEHOLDER = "@EA_MODE_DIAGRAMS@"

    @property
    def placeholders(self) -> frozenset[str]:
        return frozenset((self.PLACEHOLDER,))

    def expand(self, text: str, context: DocumentFragmentContext) -> str:
        if self.PLACEHOLDER not in text:
            return text
        diagrams = render_catalog(context.project.catalog.ea_modes.items())
        return text.replace(self.PLACEHOLDER, diagrams)
