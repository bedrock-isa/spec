"""Pure renderers used by specification artifact generators."""

from .document_fragment import (
    DocumentFragmentContext,
    DocumentFragmentPipeline,
    DocumentFragmentProvider,
)
from .control_register_reference import ControlRegisterReferenceRenderer
from .cpuid_leaf import (
    CpuidLeafFragmentRenderer,
    CpuidLeafProjection,
    ProjectedCpuidQuery,
)
from .ea_diagram import EaDiagramFragmentRenderer, EaDiagramProjection
from .event_reference import EventCodeRow, EventReferenceRenderer
from .implementation_disclosure import ImplementationDisclosureRenderer
from .memory_record import (
    MemoryRecordComponentProjection,
    MemoryRecordFragmentRenderer,
    MemoryRecordPaddingProjection,
    MemoryRecordProjection,
    MemoryRecordRowProjection,
)
from .register_model_figure import (
    RegisterFigureProjection,
    RegisterModelFigureRenderer,
)
from .page_table_entry_field_target import PageTableEntryFieldTargetRenderer
from .register_field_target import RegisterFieldTargetRenderer
from .structured_field_target import (
    CpuidFieldTargetRenderer,
    DebugTriggerTargetRenderer,
    EventStructureTargetRenderer,
    InstructionHeaderFieldTargetRenderer,
)
from .latex_document import (
    DocumentProjection,
    InstructionBitSegment,
    InstructionByteProjection,
    InstructionEntryRenderer,
    InstructionFormatProjection,
    InstructionSetSummaryProjection,
    InstructionSummaryRow,
    LatexDocumentRenderer,
    LatexSemanticTextRenderer,
    ProjectedInstructionEntry,
    ProjectedInstructionSet,
    ProjectedTermGroup,
    ProjectedTopic,
    TermGroupRenderer,
)
from .latex_source import (
    LatexSourceInputProjection,
    LatexSourcePreprocessor,
    LatexSourceProjection,
)
from .sail_dispatch import (
    SailDispatchEntry,
    SailDispatchProjection,
    SailDispatchRenderer,
)
from .sail_catalog import (
    SailCatalogProjection,
    SailCatalogRenderer,
    SailEaFormProjection,
    SailFormProjection,
    SailOperandBindingProjection,
)
from .sail_project import SailProject, SailProjectModule, SailProjectRenderer
from .sail_registry import (
    SailEventProjection,
    SailOperationProjection,
    SailRegistryProjection,
    SailRegistryRenderer,
)
from .vector_diagram import VectorDiagramPlacementRenderer
from .vector_tikz import VectorDiagramRenderer

__all__ = [
    "ControlRegisterReferenceRenderer",
    "CpuidLeafFragmentRenderer",
    "CpuidLeafProjection",
    "DocumentFragmentContext",
    "DocumentFragmentPipeline",
    "DocumentFragmentProvider",
    "DocumentProjection",
    "EaDiagramFragmentRenderer",
    "EaDiagramProjection",
    "EventReferenceRenderer",
    "EventCodeRow",
    "ImplementationDisclosureRenderer",
    "MemoryRecordComponentProjection",
    "MemoryRecordFragmentRenderer",
    "MemoryRecordPaddingProjection",
    "MemoryRecordProjection",
    "MemoryRecordRowProjection",
    "RegisterModelFigureRenderer",
    "RegisterFigureProjection",
    "PageTableEntryFieldTargetRenderer",
    "RegisterFieldTargetRenderer",
    "CpuidFieldTargetRenderer",
    "DebugTriggerTargetRenderer",
    "EventStructureTargetRenderer",
    "InstructionHeaderFieldTargetRenderer",
    "InstructionEntryRenderer",
    "InstructionBitSegment",
    "InstructionByteProjection",
    "InstructionFormatProjection",
    "InstructionSetSummaryProjection",
    "InstructionSummaryRow",
    "LatexDocumentRenderer",
    "LatexSemanticTextRenderer",
    "LatexSourcePreprocessor",
    "LatexSourceInputProjection",
    "LatexSourceProjection",
    "ProjectedCpuidQuery",
    "ProjectedInstructionEntry",
    "ProjectedInstructionSet",
    "ProjectedTermGroup",
    "ProjectedTopic",
    "SailDispatchRenderer",
    "SailDispatchEntry",
    "SailDispatchProjection",
    "SailCatalogRenderer",
    "SailCatalogProjection",
    "SailEaFormProjection",
    "SailFormProjection",
    "SailOperandBindingProjection",
    "SailProject",
    "SailProjectModule",
    "SailProjectRenderer",
    "SailRegistryRenderer",
    "SailEventProjection",
    "SailOperationProjection",
    "SailRegistryProjection",
    "TermGroupRenderer",
    "VectorDiagramPlacementRenderer",
    "VectorDiagramRenderer",
]
