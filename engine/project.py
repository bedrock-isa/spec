"""Whole-tree loading and lookup for ISA authoring tools."""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from enum import StrEnum
import logging
from pathlib import Path
from types import MappingProxyType
from typing import Callable, TypeVar, cast

from .cpuid import CpuidCatalog, CpuidClassOverlay, CpuidField, CpuidLeafOverlay
from .control_register import ControlRegisterCatalog
from .debug_trigger import DebugTriggerCatalog
from .dependency import EntityDependency
from .disclosure import ImplementationDisclosureCatalog
from .ea_mode import EAMode, EAModeCatalog
from .encoding import EncodingCatalog, EncodingForm
from .encoding_reservation import EncodingReservationCatalog
from .entity import Entity, EntityCatalog, EntityDisplayStyle
from .event import EventCatalog, EventClassOverlay
from .event_structure import EventFrameCatalog, EventPayloadCatalog
from .extension import ExtensionMetadata, ExtensionSetCatalog
from .inventory import DirectoryInventory
from .instruction import Instruction
from .instruction_header import InstructionHeaderCatalog
from .memory_record import MemoryRecordCatalog
from .model import ModelCatalog
from .observability import log_phase
from .page_table_entry import PageTableEntryCatalog
from .register import RegisterCatalog, SourcedReset
from .reference import (
    QualifiedReference,
    Reference,
    ReferenceIndex,
    UnknownReferenceError,
)
from .terminology import TermCatalog
from .type_system import EffectiveAddressFieldType, TypeNamespace, TypeSystem
from .vector_diagram import VectorDiagram, VectorDiagramCatalog


_T = TypeVar("_T")
_LOGGER = logging.getLogger(__name__)


class ProjectLookupReason(StrEnum):
    UNKNOWN_INSTRUCTION = "unknown_instruction"
    UNKNOWN_EXTENSION = "unknown_extension"


class ProjectLookupError(ValueError):
    def __init__(self, reason: ProjectLookupReason, value: object) -> None:
        self.reason = reason
        self.value = value
        super().__init__(f"{reason.value}: {value!r}")


class SourceCatalogError(ValueError):
    """Base class for a rejected source-catalog relation."""


class ExtensionDependencyCycleError(SourceCatalogError):
    def __init__(self, source: Path, cycle: tuple[str, ...]) -> None:
        self.source = source
        self.cycle = cycle
        super().__init__(f"{source}: circular extension dependency: {' -> '.join(cycle)}")


class RequiredExtensionUnavailableError(SourceCatalogError):
    def __init__(self, source: Path | str, extension_id: str) -> None:
        self.source = source
        self.extension_id = extension_id
        super().__init__(f"{source}: required extension {extension_id!r} is not available")


class UnknownCpuidFlagError(SourceCatalogError):
    def __init__(self, source: Path, reference: Reference[object]) -> None:
        self.source = source
        self.reference = reference
        super().__init__(f"{source}: unknown CPUID flag reference {reference!r}")


class CpuidFlagWidthError(SourceCatalogError):
    def __init__(self, source: Path, field: CpuidField) -> None:
        self.source = source
        self.field = field
        super().__init__(
            f"{source}: CPUID flag {field.id!r} names a {field.bits}-bit field"
        )


class RepeatedCpuidRequirementError(SourceCatalogError):
    def __init__(self, source: Path, field: CpuidField) -> None:
        self.source = source
        self.field = field
        super().__init__(
            f"{source}: CPUID flag {field.id!r} repeats an inherited requirement"
        )


@dataclass(frozen=True, slots=True)
class ArtifactSet:
    """Fixed authored companions of one instruction definition."""

    semantics: Path
    description: Path


@dataclass(frozen=True, slots=True)
class InstructionBundle(Entity):
    """The complete authoring boundary for one instruction."""

    reference: Reference["InstructionBundle"]
    owner: str
    instruction: Instruction
    encodings: EncodingCatalog
    diagrams: VectorDiagramCatalog
    artifacts: ArtifactSet
    required_cpuid_flags: tuple[CpuidField, ...]

    @property
    def source(self) -> Path:
        return self.instruction.source

    def required_cpuid_flags_for(
        self, form: EncodingForm
    ) -> tuple[CpuidField, ...]:
        """Return inherited and form-local CPUID requirements."""

        return (*self.required_cpuid_flags, *form.additional_cpuid_flags)


class InstructionSetCatalog(DirectoryInventory):
    """One declared base or extension instruction catalog."""


@dataclass(frozen=True, slots=True)
class InstructionSet:
    """One instruction inventory and the bundles successfully loaded from it."""

    catalog: InstructionSetCatalog
    instructions: tuple[InstructionBundle, ...]


@dataclass(frozen=True, slots=True)
class Extension:
    """One declared ISA extension and all instructions owned by it."""

    metadata: ExtensionMetadata
    types: TypeNamespace
    instruction_set: InstructionSet
    requires: tuple["Extension", ...]
    required_cpuid_flags: tuple[CpuidField, ...]

    @property
    def id(self) -> str:
        return self.metadata.id

    @property
    def name(self) -> str:
        return self.metadata.name

    @property
    def required_ids(self) -> tuple[str, ...]:
        return self.metadata.requires

    @property
    def source(self) -> Path:
        return self.metadata.source

    @property
    def root(self) -> Path:
        return self.metadata.root

    @property
    def instructions(self) -> tuple[InstructionBundle, ...]:
        return self.instruction_set.instructions


@dataclass(frozen=True, slots=True)
class _ExtensionComponents:
    """Loaded extension-owned objects awaiting dependency resolution."""

    metadata: ExtensionMetadata
    types: TypeNamespace
    instruction_set: InstructionSet
    required_cpuid_flags: tuple[CpuidField, ...] = ()


def _build_entities(
    types,
    sources,
    cpuid,
    events,
    event_frames,
    event_payloads,
    registers,
    control_registers,
    debug_triggers,
    page_table_entries,
    instruction_headers,
    terminology,
    model,
) -> EntityCatalog:
    """Compose the ISA provider's typed indexes into its workspace catalog."""

    entries: list[tuple[Entity, str, EntityDisplayStyle]] = []

    def add(
        reference: Reference[object],
        value: object,
        display: str,
        style: EntityDisplayStyle = EntityDisplayStyle.TEXT,
    ) -> None:
        if not isinstance(value, Entity):
            raise TypeError(
                f"{reference!r}: referencable value must inherit Entity"
            )
        if value.reference != reference:
            raise ValueError(
                f"{reference!r}: entity reference disagrees with its typed index"
            )
        entries.append((value, display, style))

    def add_index(
        typed_index,
        display: Callable[[Reference[object], object], str],
        style: EntityDisplayStyle = EntityDisplayStyle.TEXT,
    ) -> None:
        for reference, value in typed_index.items():
            normalized = cast(Reference[object], reference)
            add(normalized, value, display(normalized, value), style)

    def identifier(_reference: Reference[object], value: object) -> str:
        return str(getattr(value, "id"))

    def name_or_identifier(
        _reference: Reference[object], value: object
    ) -> str:
        return str(getattr(value, "name", None) or getattr(value, "id"))

    def qualified_field(
        reference: Reference[object], value: object
    ) -> str:
        return f"{reference.path[-1]}.{getattr(value, 'id')}"

    for topic in model.document_topics.values():
        add(
            cast(Reference[object], topic.reference),
            topic,
            topic.id.replace("-", " ").replace("_", " "),
        )
    for reference, bundle in sources.instructions.items():
        add(
            cast(Reference[object], reference),
            bundle,
            bundle.instruction.mnemonic,
            EntityDisplayStyle.CODE,
        )
    for values in (
        sources.ea_modes,
        types.field_types,
        types.payload_types,
    ):
        add_index(values, identifier, EntityDisplayStyle.CODE)

    code = EntityDisplayStyle.CODE
    for typed_index, display, style in (
        (cpuid.references.classes, name_or_identifier, EntityDisplayStyle.TEXT),
        (cpuid.references.leaves, identifier, code),
        (cpuid.references.layouts, identifier, code),
        (cpuid.references.queries, identifier, code),
        (cpuid.references.fields, identifier, code),
        (cpuid.references.layout_fields, identifier, code),
        (cpuid.references.common_headers, identifier, code),
        (cpuid.references.common_header_fields, qualified_field, code),
        (events.references.classes, name_or_identifier, EntityDisplayStyle.TEXT),
        (events.references.events, identifier, code),
        (event_frames.references.frames, identifier, code),
        (event_frames.references.slots, identifier, code),
        (event_frames.references.fields, qualified_field, code),
        (event_payloads.references.formats, identifier, code),
        (event_payloads.references.fields, qualified_field, code),
        (registers.references.groups, identifier, EntityDisplayStyle.TEXT),
        (registers.references.registers, identifier, code),
        (registers.references.fields, qualified_field, code),
        (
            control_registers.references.namespaces,
            identifier,
            EntityDisplayStyle.TEXT,
        ),
        (
            control_registers.references.registers,
            identifier,
            EntityDisplayStyle.TEXT,
        ),
        (control_registers.references.fields, qualified_field, code),
        (debug_triggers.references.slots, identifier, code),
        (debug_triggers.references.words, identifier, code),
        (debug_triggers.references.fields, qualified_field, code),
        (page_table_entries.references.entries, identifier, code),
        (page_table_entries.references.fields, qualified_field, code),
        (instruction_headers.references.headers, identifier, code),
        (instruction_headers.references.fields, qualified_field, code),
    ):
        add_index(typed_index, display, style)

    for group in terminology.references.groups.values():
        add(cast(Reference[object], group.reference), group, group.title)
    for term in terminology.references.terms.values():
        add(
            cast(Reference[object], term.reference),
            term,
            term.forms.canonical,
        )
    return EntityCatalog.create(entries)


@dataclass(frozen=True, slots=True)
class SourceCatalog:
    """Declared instruction and EA source inventories."""

    instructions: ReferenceIndex[InstructionBundle]
    ea_modes: ReferenceIndex[EAMode]
    instruction_order: tuple[Reference[InstructionBundle], ...]
    base: InstructionSet
    extensions: Mapping[str, Extension]
    extension_catalog: ExtensionSetCatalog

    @classmethod
    def discover(
        cls,
        root: str | Path,
        types: TypeSystem,
        cpuid: CpuidCatalog,
        extension_catalog: ExtensionSetCatalog | None = None,
    ) -> "SourceCatalog":
        isa_root = Path(root).resolve()
        instructions = ReferenceIndex[InstructionBundle]()
        ea_modes = ReferenceIndex[EAMode]()
        order: list[Reference[InstructionBundle]] = []
        extension_catalog = extension_catalog or ExtensionSetCatalog.load(isa_root)
        extension_roots = extension_catalog.owner_roots()[1:]

        base = cls._load_instruction_set(
            "base",
            isa_root / "instructions/definitions",
            isa_root,
            types,
            instructions,
            order,
            (),
            cpuid,
        )
        extension_metadata: dict[str, ExtensionMetadata] = {}
        for extension_id, extension_root in extension_roots:
            if extension_root.is_dir():
                extension_metadata[extension_id] = ExtensionMetadata.load(
                    extension_root / "extension.yaml", isa_root
                )
        cpuid_requirements = cls._resolve_cpuid_requirements(
            extension_metadata, extension_catalog.declared, cpuid
        )
        extension_components: dict[str, _ExtensionComponents] = {}
        for extension_id, extension_root in extension_roots:
            if not extension_root.is_dir():
                continue
            metadata = extension_metadata[extension_id]
            instruction_set = cls._load_instruction_set(
                extension_id,
                extension_root / "instructions/definitions",
                isa_root,
                types,
                instructions,
                order,
                cpuid_requirements[extension_id],
                cpuid,
            )
            extension_components[extension_id] = _ExtensionComponents(
                metadata=metadata,
                types=types.namespace(extension_id),
                instruction_set=instruction_set,
                required_cpuid_flags=cpuid_requirements[extension_id],
            )
        extensions = cls._resolve_extensions(
            extension_components, extension_catalog.declared
        )

        owners = ("base", *extension_catalog.declared)
        for catalog in EAModeCatalog.discover(isa_root, types, owners):
            for mode_id in catalog.modes:
                mode = EAMode.load(
                    catalog.mode_path(mode_id),
                    isa_root,
                    types,
                    catalog=catalog,
                )
                ea_modes.register(mode.reference, mode)

        return cls(
            instructions=instructions,
            ea_modes=ea_modes,
            instruction_order=tuple(order),
            base=base,
            extensions=extensions,
            extension_catalog=extension_catalog,
        )

    @staticmethod
    def _resolve_cpuid_requirements(
        metadata: Mapping[str, ExtensionMetadata],
        declared: tuple[str, ...],
        cpuid: CpuidCatalog,
    ) -> Mapping[str, tuple[CpuidField, ...]]:
        resolved: dict[str, tuple[CpuidField, ...]] = {}
        active: list[str] = []

        def resolve(extension_id: str) -> tuple[CpuidField, ...]:
            existing = resolved.get(extension_id)
            if existing is not None:
                return existing
            if extension_id in active:
                start = active.index(extension_id)
                cycle = (*active[start:], extension_id)
                cycle_source = metadata[active[-1]].source
                raise ExtensionDependencyCycleError(cycle_source, cycle)
            extension = metadata.get(extension_id)
            if extension is None:
                requiring = metadata[active[-1]] if active else None
                missing_source = (
                    requiring.source if requiring is not None else extension_id
                )
                raise RequiredExtensionUnavailableError(
                    missing_source, extension_id
                )

            active.append(extension_id)
            fields: list[CpuidField] = []
            seen: set[Reference[CpuidField]] = set()
            for required_id in extension.requires:
                for field in resolve(required_id):
                    if field.reference not in seen:
                        fields.append(field)
                        seen.add(field.reference)
            for raw_reference in extension.required_cpuid_flags:
                field = SourceCatalog._resolve_cpuid_flag(
                    raw_reference, extension.source, cpuid
                )
                if field.reference in seen:
                    raise RepeatedCpuidRequirementError(
                        extension.source, field
                    )
                fields.append(field)
                seen.add(field.reference)
            active.pop()
            resolved[extension_id] = tuple(fields)
            return resolved[extension_id]

        for extension_id in declared:
            if extension_id in metadata:
                resolve(extension_id)
        return MappingProxyType(resolved)

    @staticmethod
    def _resolve_cpuid_flag(
        raw_reference: str, source: Path, cpuid: CpuidCatalog
    ) -> CpuidField:
        reference: Reference[CpuidField] = Reference.parse(raw_reference)
        try:
            field = cpuid.references.fields.resolve(reference)
        except UnknownReferenceError as error:
            raise UnknownCpuidFlagError(source, reference) from error
        if field.bits != 1:
            raise CpuidFlagWidthError(source, field)
        return field

    @staticmethod
    def _resolve_extensions(
        components: Mapping[str, _ExtensionComponents],
        declared: tuple[str, ...],
    ) -> Mapping[str, Extension]:
        resolved: dict[str, Extension] = {}
        active: list[str] = []

        def resolve(extension_id: str) -> Extension:
            existing = resolved.get(extension_id)
            if existing is not None:
                return existing
            if extension_id in active:
                start = active.index(extension_id)
                cycle = (*active[start:], extension_id)
                cycle_source = components[active[-1]].metadata.source
                raise ExtensionDependencyCycleError(cycle_source, cycle)
            component = components.get(extension_id)
            if component is None:
                requiring = components[active[-1]].metadata if active else None
                missing_source = (
                    requiring.source if requiring is not None else extension_id
                )
                raise RequiredExtensionUnavailableError(
                    missing_source, extension_id
                )

            active.append(extension_id)
            dependencies = tuple(
                resolve(required_id) for required_id in component.metadata.requires
            )
            active.pop()
            extension = Extension(
                metadata=component.metadata,
                types=component.types,
                instruction_set=component.instruction_set,
                requires=dependencies,
                required_cpuid_flags=component.required_cpuid_flags,
            )
            resolved[extension_id] = extension
            return extension

        for extension_id in declared:
            if extension_id in components:
                resolve(extension_id)
        return MappingProxyType(
            {
                extension_id: resolved[extension_id]
                for extension_id in dict.fromkeys(declared)
                if extension_id in resolved
            }
        )

    @classmethod
    def _load_instruction_set(
        cls,
        owner: str,
        instruction_root: Path,
        isa_root: Path,
        types: TypeSystem,
        instructions: ReferenceIndex[InstructionBundle],
        order: list[Reference[InstructionBundle]],
        required_cpuid_flags: tuple[CpuidField, ...],
        cpuid: CpuidCatalog,
    ) -> InstructionSet:
        catalog = InstructionSetCatalog.inspect(
            owner=owner,
            kind="instruction",
            source=instruction_root / "instructions.yaml",
            root=instruction_root,
            key="instructions",
        )
        bundles: list[InstructionBundle] = []
        for mnemonic in catalog.declared:
            directory = instruction_root / mnemonic
            reference: Reference[InstructionBundle] = Reference(
                owner, ("instructions",), mnemonic
            )
            if reference in instructions or not directory.is_dir():
                continue
            instruction = Instruction.load(directory / "instruction.yaml", isa_root)
            cpuid_flags = list(required_cpuid_flags)
            seen_cpuid_flags = {field.reference for field in cpuid_flags}
            for raw_reference in instruction.to_dict().get(
                "additional_cpuid_flags", ()
            ):
                field = cls._resolve_cpuid_flag(
                    raw_reference, instruction.source, cpuid
                )
                if field.reference in seen_cpuid_flags:
                    raise RepeatedCpuidRequirementError(
                        instruction.source, field
                    )
                cpuid_flags.append(field)
                seen_cpuid_flags.add(field.reference)
            encoding_catalog = EncodingCatalog.load(
                directory / "encodings.yaml", types, isa_root, cpuid
            )
            common_cpuid_references = {field.reference for field in cpuid_flags}
            for form in encoding_catalog.forms:
                repeated = tuple(
                    field.id
                    for field in form.additional_cpuid_flags
                    if field.reference in common_cpuid_references
                )
                if repeated:
                    raise ValueError(
                        f"{encoding_catalog.source}: {form.id}: additional CPUID "
                        f"flags repeat inherited requirements {repeated}"
                    )
            diagram_catalog = VectorDiagramCatalog.load(
                owner=owner,
                mnemonic=mnemonic,
                instruction=reference,
                root=directory / "diagrams",
                schema=isa_root / "schemas/vector-diagram.yaml",
            )
            bundle = InstructionBundle(
                reference=reference,
                owner=owner,
                instruction=instruction,
                encodings=encoding_catalog,
                diagrams=diagram_catalog,
                artifacts=ArtifactSet(
                    semantics=directory / "semantics.sail",
                    description=directory / "descriptions.tex",
                ),
                required_cpuid_flags=tuple(cpuid_flags),
            )
            instructions.register(reference, bundle)
            order.append(reference)
            bundles.append(bundle)
        return InstructionSet(catalog, tuple(bundles))


@dataclass(frozen=True, slots=True)
class IsaProject:
    """The single public loading and lookup facade for authoring commands."""

    root: Path
    types: TypeSystem
    encoding_reservations: EncodingReservationCatalog
    catalog: SourceCatalog
    cpuid: CpuidCatalog
    events: EventCatalog
    event_frames: EventFrameCatalog
    event_payloads: EventPayloadCatalog
    registers: RegisterCatalog
    memory_records: MemoryRecordCatalog
    control_registers: ControlRegisterCatalog
    debug_triggers: DebugTriggerCatalog
    page_table_entries: PageTableEntryCatalog
    instruction_headers: InstructionHeaderCatalog
    terminology: TermCatalog
    model: ModelCatalog
    disclosures: ImplementationDisclosureCatalog
    entities: EntityCatalog

    @classmethod
    def load(cls, root: str | Path) -> "IsaProject":
        return IsaProjectLoader().load(root)

    def resolve(self, reference: Reference[_T]) -> _T:
        """Resolve one provider-local entity through the ISA entity catalog."""

        return cast(
            _T,
            self.entities.resolve(cast(Reference[Entity], reference)),
        )

    def entity_dependencies(
        self,
    ) -> tuple[EntityDependency, ...]:
        """Return the ISA domain's authored and typed entity relationships."""

        result: list[EntityDependency] = []

        def local(reference: Reference[object]) -> QualifiedReference[object]:
            return QualifiedReference("isa", reference)

        def add(
            source: Reference[object],
            target: Reference[object],
            kind: str,
        ) -> None:
            result.append(EntityDependency(source, local(target), kind))

        for bundle in self.catalog.instructions.values():
            source = cast(Reference[object], bundle.reference)
            required_cpuid_fields = {
                field.reference: field
                for field in (
                    *bundle.required_cpuid_flags,
                    *(
                        local
                        for form in bundle.encodings.forms
                        for local in form.additional_cpuid_flags
                    ),
                )
            }
            for field in required_cpuid_fields.values():
                add(
                    source,
                    cast(Reference[object], field.reference),
                    "requires-cpuid",
                )
            for form in bundle.encodings.forms:
                for field in form.fields:
                    add(
                        source,
                        cast(Reference[object], field.type),
                        "instruction-field-type",
                    )
                for payload in form.payloads:
                    add(
                        source,
                        cast(Reference[object], payload.type),
                        "instruction-payload-type",
                    )

        profile_types = {
            (definition.owner, definition.profile): definition.reference
            for definition in self.types.field_types.values()
            if isinstance(definition, EffectiveAddressFieldType)
        }
        for mode in self.catalog.ea_modes.values():
            source = cast(Reference[object], mode.reference)
            profile_type = profile_types.get((mode.catalog.owner, mode.catalog.profile))
            if profile_type is not None:
                add(
                    source,
                    cast(Reference[object], profile_type),
                    "ea-profile-type",
                )
            for field in mode.fields:
                add(
                    source,
                    cast(Reference[object], field.type),
                    "ea-field-type",
                )
            for encoding in mode.encodings:
                for payload in encoding.payloads:
                    add(
                        source,
                        cast(Reference[object], payload.type),
                        "ea-payload-type",
                    )

        for cpuid_class in self.cpuid.references.classes.values():
            if isinstance(cpuid_class, CpuidClassOverlay):
                add(
                    cast(Reference[object], cpuid_class.reference),
                    cast(Reference[object], cpuid_class.extends),
                    "cpuid-class-overlay",
                )
        for leaf in self.cpuid.references.leaves.values():
            if isinstance(leaf, CpuidLeafOverlay):
                add(
                    cast(Reference[object], leaf.reference),
                    cast(Reference[object], leaf.extends),
                    "cpuid-leaf-overlay",
                )
        for event_class in self.events.references.classes.values():
            if isinstance(event_class, EventClassOverlay):
                add(
                    cast(Reference[object], event_class.reference),
                    cast(Reference[object], event_class.extends),
                    "event-class-overlay",
                )

        for register in self.registers.references.registers.values():
            if isinstance(register.reset, SourcedReset):
                add(
                    cast(Reference[object], register.reference),
                    cast(Reference[object], register.reset.source),
                    "register-reset-source",
                )
        for register in self.control_registers.references.registers.values():
            if isinstance(register.reset, SourcedReset):
                add(
                    cast(Reference[object], register.reference),
                    cast(Reference[object], register.reset.source),
                    "control-register-reset-source",
                )

        for term in self.terminology.references.terms.values():
            source = cast(Reference[object], term.reference)
            for target in term.relations.broader:
                add(
                    source,
                    cast(Reference[object], target),
                    "term-broader",
                )
            for target in term.relations.related:
                add(
                    source,
                    cast(Reference[object], target),
                    "term-related",
                )
        return tuple(result)

    def bundle(
        self, value: str | Reference[InstructionBundle] | Path
    ) -> InstructionBundle:
        if isinstance(value, Reference):
            return self.catalog.instructions.resolve(value)

        candidate = Path(value)
        if candidate.exists():
            resolved = candidate.resolve()
            for bundle in self.catalog.instructions.values():
                directory = bundle.instruction.source.parent.resolve()
                if resolved == directory or resolved.is_relative_to(directory):
                    return bundle
            raise ValueError(f"path is outside every declared instruction: {resolved}")

        text = str(value)
        if "." in text:
            try:
                return self.catalog.instructions.resolve(Reference.parse(text))
            except UnknownReferenceError as error:
                raise ProjectLookupError(
                    ProjectLookupReason.UNKNOWN_INSTRUCTION, value
                ) from error

        matches = [
            bundle
            for bundle in self.catalog.instructions.values()
            if bundle.instruction.mnemonic == text
        ]
        if not matches:
            raise ProjectLookupError(ProjectLookupReason.UNKNOWN_INSTRUCTION, value)
        if len(matches) != 1:
            owners = ", ".join(bundle.owner for bundle in matches)
            raise ValueError(f"ambiguous instruction {text!r}: {owners}")
        return matches[0]

    def extension(self, extension_id: str) -> Extension:
        """Resolve one extension by its architectural ID."""

        try:
            return self.catalog.extensions[extension_id]
        except KeyError as error:
            raise ProjectLookupError(
                ProjectLookupReason.UNKNOWN_EXTENSION, extension_id
            ) from error

    def vector_diagram(self, value: str | Reference[VectorDiagram]) -> VectorDiagram:
        """Resolve one fully qualified instruction-owned vector diagram."""

        reference: Reference[VectorDiagram] = Reference.parse(value)
        if (
            reference.owner not in {"VECTOR", "VECTORFP"}
            or len(reference.path) != 3
            or reference.path[0] != "instructions"
            or reference.path[2] != "diagrams"
        ):
            raise ValueError(
                "vector diagram references must have the form "
                "VECTOR|VECTORFP.instructions.<mnemonic>.diagrams.<id>"
            )
        instruction_reference: Reference[InstructionBundle] = Reference(
            reference.owner,
            ("instructions",),
            reference.path[1],
        )
        try:
            bundle = self.catalog.instructions.resolve(instruction_reference)
            return bundle.diagrams.resolve(reference)
        except UnknownReferenceError as error:
            raise ValueError("unknown vector diagram reference") from error

    def select(
        self, targets: Iterable[str | Reference[InstructionBundle] | Path] = ()
    ) -> tuple[InstructionBundle, ...]:
        requested = tuple(targets)
        if not requested:
            return tuple(
                self.catalog.instructions.resolve(reference)
                for reference in self.catalog.instruction_order
            )
        selected: list[InstructionBundle] = []
        seen: set[Reference[InstructionBundle]] = set()
        for target in requested:
            bundle = self.bundle(target)
            if bundle.reference not in seen:
                selected.append(bundle)
                seen.add(bundle.reference)
        return tuple(selected)


class IsaProjectLoader:
    """Construct an immutable project facade from its domain catalogs."""

    def load(self, root: str | Path) -> IsaProject:
        isa_root = Path(root).resolve()
        with log_phase(
            _LOGGER,
            "project.catalog.load",
            level=logging.DEBUG,
            catalog="extensions",
        ):
            extension_catalog = ExtensionSetCatalog.load(isa_root)
        with log_phase(
            _LOGGER, "project.catalog.load", level=logging.DEBUG, catalog="types"
        ):
            types = TypeSystem.load(isa_root, extension_catalog)
        with log_phase(
            _LOGGER,
            "project.catalog.load",
            level=logging.DEBUG,
            catalog="encoding-reservations",
        ):
            encoding_reservations = EncodingReservationCatalog.load(isa_root)
        with log_phase(
            _LOGGER, "project.catalog.load", level=logging.DEBUG, catalog="cpuid"
        ):
            cpuid = CpuidCatalog.load(isa_root, extension_catalog)
        with log_phase(
            _LOGGER, "project.catalog.load", level=logging.DEBUG, catalog="events"
        ):
            events = EventCatalog.load(isa_root, extension_catalog)
        with log_phase(
            _LOGGER,
            "project.catalog.load",
            level=logging.DEBUG,
            catalog="event-frames",
        ):
            event_frames = EventFrameCatalog.load(isa_root)
        with log_phase(
            _LOGGER,
            "project.catalog.load",
            level=logging.DEBUG,
            catalog="event-payloads",
        ):
            event_payloads = EventPayloadCatalog.load(isa_root)
        with log_phase(
            _LOGGER, "project.catalog.load", level=logging.DEBUG, catalog="registers"
        ):
            registers = RegisterCatalog.load(isa_root, extension_catalog)
        with log_phase(
            _LOGGER,
            "project.catalog.load",
            level=logging.DEBUG,
            catalog="memory-records",
        ):
            memory_records = MemoryRecordCatalog.load(isa_root, extension_catalog)
        with log_phase(
            _LOGGER,
            "project.catalog.load",
            level=logging.DEBUG,
            catalog="control-registers",
        ):
            control_registers = ControlRegisterCatalog.load(
                isa_root, extension_catalog
            )
        with log_phase(
            _LOGGER,
            "project.catalog.load",
            level=logging.DEBUG,
            catalog="page-table-entries",
        ):
            page_table_entries = PageTableEntryCatalog.load(isa_root)
        with log_phase(
            _LOGGER,
            "project.catalog.load",
            level=logging.DEBUG,
            catalog="debug-triggers",
        ):
            debug_triggers = DebugTriggerCatalog.load(isa_root)
        with log_phase(
            _LOGGER,
            "project.catalog.load",
            level=logging.DEBUG,
            catalog="instruction-headers",
        ):
            instruction_headers = InstructionHeaderCatalog.load(isa_root)
        with log_phase(
            _LOGGER,
            "project.catalog.load",
            level=logging.DEBUG,
            catalog="terminology",
        ):
            terminology = TermCatalog.load(isa_root, extension_catalog)
        with log_phase(
            _LOGGER,
            "project.catalog.load",
            level=logging.DEBUG,
            catalog="instructions",
        ):
            catalog = SourceCatalog.discover(
                isa_root, types, cpuid, extension_catalog
            )
        with log_phase(
            _LOGGER, "project.catalog.load", level=logging.DEBUG, catalog="model"
        ):
            model = ModelCatalog.load(
                isa_root,
                extension_catalog,
                {
                    extension_id: extension.metadata
                    for extension_id, extension in catalog.extensions.items()
                },
            )
        with log_phase(
            _LOGGER,
            "project.catalog.load",
            level=logging.DEBUG,
            catalog="disclosures",
        ):
            disclosures = ImplementationDisclosureCatalog.load(
                isa_root, extension_catalog
            )
        with log_phase(
            _LOGGER, "project.catalog.load", level=logging.DEBUG, catalog="entities"
        ):
            entities = _build_entities(
                types,
                catalog,
                cpuid,
                events,
                event_frames,
                event_payloads,
                registers,
                control_registers,
                debug_triggers,
                page_table_entries,
                instruction_headers,
                terminology,
                model,
            )
        return IsaProject(
            isa_root,
            types,
            encoding_reservations,
            catalog,
            cpuid,
            events,
            event_frames,
            event_payloads,
            registers,
            memory_records,
            control_registers,
            debug_triggers,
            page_table_entries,
            instruction_headers,
            terminology,
            model,
            disclosures,
            entities,
        )
