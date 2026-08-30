"""Generated EA encoding and address-flow diagrams for the ISA reference."""

from __future__ import annotations

from typing import cast

from ..entity import Entity
from ..generate_ea_diagrams import render_catalog
from ..reference import Reference
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
        labeled_modes = []
        for reference, mode in context.project.catalog.ea_modes.items():
            entity = context.project.entities.resolve(
                cast(Reference[Entity], reference)
            )
            if entity.latex_label is None:
                raise ValueError("EA mode has no target in this LaTeX artifact")
            labeled_modes.append((entity.latex_label, mode))
        diagrams = render_catalog(labeled_modes)
        return text.replace(self.PLACEHOLDER, diagrams)
