"""Whole-tree loading and lookup for ISA authoring tools."""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from pathlib import Path
from types import MappingProxyType

try:
    from .cpuid import CpuidCatalog, CpuidField
    from .disclosure import ImplementationDisclosureCatalog
    from .ea_mode import EAMode, EAModeCatalog
    from .encoding import EncodingCatalog
    from .entity import EntityCatalog
    from .event import EventCatalog
    from .extension import ExtensionMetadata, ExtensionSetCatalog
    from .instruction import Instruction
    from .model import ModelCatalog
    from .register import RegisterCatalog
    from .reference import Reference, ReferenceIndex, UnknownReferenceError
    from .terminology import TermCatalog
    from .type_system import TypeNamespace, TypeSystem
    from .vector_diagram import VectorDiagram, VectorDiagramCatalog
    from .yaml_document import YamlDocumentLoader
except ImportError:  # Support loading engine directly on PYTHONPATH.
    from cpuid import CpuidCatalog, CpuidField
    from disclosure import ImplementationDisclosureCatalog
    from ea_mode import EAMode, EAModeCatalog
    from encoding import EncodingCatalog
    from entity import EntityCatalog
    from event import EventCatalog
    from extension import ExtensionMetadata, ExtensionSetCatalog
    from instruction import Instruction
    from model import ModelCatalog
    from register import RegisterCatalog
    from reference import Reference, ReferenceIndex, UnknownReferenceError
    from terminology import TermCatalog
    from type_system import TypeNamespace, TypeSystem
    from vector_diagram import VectorDiagram, VectorDiagramCatalog
    from yaml_document import YamlDocumentLoader


@dataclass(frozen=True, slots=True)
class ArtifactSet:
    """Fixed authored companions of one instruction definition."""

    semantics: Path
    description: Path


@dataclass(frozen=True, slots=True)
class InstructionBundle:
    """The complete authoring boundary for one instruction."""

    reference: Reference["InstructionBundle"]
    owner: str
    instruction: Instruction
    encodings: EncodingCatalog
    diagrams: VectorDiagramCatalog
    artifacts: ArtifactSet
    required_cpuid_flags: tuple[CpuidField, ...]


@dataclass(frozen=True, slots=True)
class InstructionSetCatalog:
    """One declared base or extension instruction catalog."""

    owner: str
    source: Path
    root: Path
    declared: tuple[str, ...]
    actual: tuple[str, ...]


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
        for extension_id in extension_catalog.declared:
            extension_root = extension_catalog.root / extension_id
            if extension_root.is_dir():
                extension_metadata[extension_id] = ExtensionMetadata.load(
                    extension_root / "extension.yaml", isa_root
                )
        cpuid_requirements = cls._resolve_cpuid_requirements(
            extension_metadata, extension_catalog.declared, cpuid
        )
        extension_components: dict[str, _ExtensionComponents] = {}
        for extension_id in extension_catalog.declared:
            extension_root = extension_catalog.root / extension_id
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
                raise ValueError(
                    f"{cycle_source}: circular extension dependency: "
                    f"{' -> '.join(cycle)}"
                )
            extension = metadata.get(extension_id)
            if extension is None:
                requiring = metadata[active[-1]] if active else None
                missing_source = (
                    requiring.source if requiring is not None else extension_id
                )
                raise ValueError(
                    f"{missing_source}: required extension {extension_id!r} "
                    "is not available"
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
                    raise ValueError(
                        f"{extension.source}: CPUID flag {field.id!r} "
                        "repeats an inherited requirement"
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
            raise ValueError(f"{source}: unknown CPUID flag reference") from error
        if field.bits != 1:
            raise ValueError(
                f"{source}: CPUID flag {field.id!r} names a {field.bits}-bit field"
            )
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
                raise ValueError(
                    f"{cycle_source}: circular extension dependency: "
                    f"{' -> '.join(cycle)}"
                )
            component = components.get(extension_id)
            if component is None:
                requiring = components[active[-1]].metadata if active else None
                missing_source = (
                    requiring.source if requiring is not None else extension_id
                )
                raise ValueError(
                    f"{missing_source}: required extension {extension_id!r} "
                    "is not available"
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
        source = instruction_root / "instructions.yaml"
        declared = cls._load_name_list(source, "instructions")
        actual = tuple(
            sorted(
                path.name
                for path in instruction_root.iterdir()
                if path.is_dir() and not path.name.startswith(".")
            )
        )
        catalog = InstructionSetCatalog(
            owner, source, instruction_root, declared, actual
        )
        bundles: list[InstructionBundle] = []
        for mnemonic in declared:
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
                    raise ValueError(
                        f"{instruction.source}: additional CPUID flag "
                        f"{field.id!r} repeats an inherited requirement"
                    )
                cpuid_flags.append(field)
                seen_cpuid_flags.add(field.reference)
            encoding_catalog = EncodingCatalog.load(
                directory / "encodings.yaml", types, isa_root
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

    @staticmethod
    def _load_name_list(path: Path, key: str) -> tuple[str, ...]:
        document = YamlDocumentLoader().mapping(path)
        if not isinstance(document, Mapping) or not isinstance(document.get(key), list):
            raise ValueError(f"{path}: expected a {key} list")
        values = document[key]
        if any(not isinstance(value, str) for value in values):
            raise ValueError(f"{path}: {key} entries must be strings")
        return tuple(values)

@dataclass(frozen=True, slots=True)
class IsaProject:
    """The single public loading and lookup facade for authoring commands."""

    root: Path
    types: TypeSystem
    catalog: SourceCatalog
    cpuid: CpuidCatalog
    events: EventCatalog
    registers: RegisterCatalog
    terminology: TermCatalog
    model: ModelCatalog
    disclosures: ImplementationDisclosureCatalog
    entities: EntityCatalog

    @classmethod
    def load(cls, root: str | Path) -> "IsaProject":
        return IsaProjectLoader().load(root)

    def bundle(self, value: str | Reference[InstructionBundle] | Path) -> InstructionBundle:
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
                raise ValueError("unknown instruction reference") from error

        matches = [
            bundle
            for bundle in self.catalog.instructions.values()
            if bundle.instruction.mnemonic == text
        ]
        if not matches:
            raise ValueError(f"unknown instruction {text!r}")
        if len(matches) != 1:
            owners = ", ".join(bundle.owner for bundle in matches)
            raise ValueError(f"ambiguous instruction {text!r}: {owners}")
        return matches[0]

    def extension(self, extension_id: str) -> Extension:
        """Resolve one extension by its architectural ID."""

        try:
            return self.catalog.extensions[extension_id]
        except KeyError as error:
            raise ValueError(f"unknown extension {extension_id!r}") from error

    def vector_diagram(
        self, value: str | Reference[VectorDiagram]
    ) -> VectorDiagram:
        """Resolve one fully qualified instruction-owned VECTOR diagram."""

        reference: Reference[VectorDiagram] = Reference.parse(value)
        if (
            reference.owner != "VECTOR"
            or len(reference.path) != 3
            or reference.path[0] != "instructions"
            or reference.path[2] != "diagrams"
        ):
            raise ValueError(
                "VECTOR diagram references must have the form "
                "VECTOR.instructions.<mnemonic>.diagrams.<id>"
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
            raise ValueError("unknown VECTOR diagram reference") from error

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
        extension_catalog = ExtensionSetCatalog.load(isa_root)
        types = TypeSystem.load(isa_root, extension_catalog)
        cpuid = CpuidCatalog.load(isa_root, extension_catalog)
        events = EventCatalog.load(isa_root, extension_catalog)
        registers = RegisterCatalog.load(isa_root, extension_catalog)
        terminology = TermCatalog.load(isa_root, extension_catalog)
        catalog = SourceCatalog.discover(isa_root, types, cpuid, extension_catalog)
        model = ModelCatalog.load(
            isa_root,
            extension_catalog,
            {
                extension_id: extension.metadata
                for extension_id, extension in catalog.extensions.items()
            },
        )
        disclosures = ImplementationDisclosureCatalog.load(isa_root, extension_catalog)
        entities = EntityCatalog.build(
            isa_root,
            types,
            catalog,
            cpuid,
            events,
            registers,
            terminology,
            model,
        )
        return IsaProject(
            isa_root,
            types,
            catalog,
            cpuid,
            events,
            registers,
            terminology,
            model,
            disclosures,
            entities,
        )
