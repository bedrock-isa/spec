"""Pure renderers used by specification artifact generators."""

from .document_fragment import (
    DocumentFragmentContext,
    DocumentFragmentPipeline,
    DocumentFragmentProvider,
)
from .cpuid_reference import CpuidEntityReferenceRenderer
from .ea_diagram import EaDiagramFragmentRenderer
from .event_reference import EventReferenceRenderer
from .implementation_disclosure import ImplementationDisclosureRenderer
from .register_model_figure import RegisterModelFigureRenderer
from .latex_document import (
    InstructionEntryRenderer,
    LatexDocumentRenderer,
    LatexSemanticTextRenderer,
    TermGroupRenderer,
)
from .latex_source import (
    LatexSourcePreprocessor,
    rewrite_direct_entity_codes,
    rewrite_direct_terms,
)
from .sail_dispatch import SailDispatchRenderer
from .sail_catalog import SailCatalogRenderer
from .sail_project import SailProjectRenderer
from .sail_registry import SailRegistryRenderer
from .type_reference import EncodingTypeReferenceRenderer
from .vector_diagram import VectorDiagramPlacementRenderer, VectorDiagramRenderer

__all__ = [
    "DocumentFragmentContext",
    "DocumentFragmentPipeline",
    "DocumentFragmentProvider",
    "CpuidEntityReferenceRenderer",
    "EaDiagramFragmentRenderer",
    "EncodingTypeReferenceRenderer",
    "EventReferenceRenderer",
    "ImplementationDisclosureRenderer",
    "RegisterModelFigureRenderer",
    "InstructionEntryRenderer",
    "LatexDocumentRenderer",
    "LatexSemanticTextRenderer",
    "LatexSourcePreprocessor",
    "SailDispatchRenderer",
    "SailCatalogRenderer",
    "SailProjectRenderer",
    "SailRegistryRenderer",
    "TermGroupRenderer",
    "VectorDiagramPlacementRenderer",
    "VectorDiagramRenderer",
    "rewrite_direct_terms",
    "rewrite_direct_entity_codes",
]
