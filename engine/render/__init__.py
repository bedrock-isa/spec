"""Pure renderers used by specification artifact generators."""

from .document_fragment import (
    DocumentFragmentContext,
    DocumentFragmentPipeline,
    DocumentFragmentProvider,
)
from .cpuid_reference import CpuidEntityReferenceRenderer
from .event_reference import EventReferenceRenderer
from .implementation_disclosure import ImplementationDisclosureRenderer
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

__all__ = [
    "DocumentFragmentContext",
    "DocumentFragmentPipeline",
    "DocumentFragmentProvider",
    "CpuidEntityReferenceRenderer",
    "EncodingTypeReferenceRenderer",
    "EventReferenceRenderer",
    "ImplementationDisclosureRenderer",
    "InstructionEntryRenderer",
    "LatexDocumentRenderer",
    "LatexSemanticTextRenderer",
    "LatexSourcePreprocessor",
    "SailDispatchRenderer",
    "SailCatalogRenderer",
    "SailProjectRenderer",
    "SailRegistryRenderer",
    "TermGroupRenderer",
    "rewrite_direct_terms",
    "rewrite_direct_entity_codes",
]
