"""Distributed architectural-event registry loading and lookup."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from types import MappingProxyType
from typing import cast

from .entity import Entity
from .extension import ExtensionSetCatalog
from .inventory import DirectoryInventory
from .reference import Reference, ReferenceIndex
from .yaml_document import SchemaValidatedYamlLoader


class EventInventory(DirectoryInventory):
    """One closed-world event class or event directory inventory."""


@dataclass(frozen=True, slots=True)
class EventSelector:
    """How an event class interprets the low event-code bits."""

    kind: str
    bits: int


@dataclass(frozen=True, slots=True)
class ArchitecturalEvent(Entity):
    """One independently defined leaf architectural event."""

    reference: Reference["ArchitecturalEvent"]
    source: Path
    root: Path
    id: str
    name: str
    summary: str
    code: int | None
    family: str | None
    frame: str
    payload: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class EventClass(Entity):
    """Common authored content of one event-code class fragment."""

    reference: Reference["EventClass"]
    source: Path
    root: Path
    id: str
    event_inventory: EventInventory
    events: Mapping[str, ArchitecturalEvent]


@dataclass(frozen=True, slots=True)
class EventClassDefinition(EventClass):
    name: str
    value: int
    selector: EventSelector


@dataclass(frozen=True, slots=True)
class EventClassOverlay(EventClass):
    extends: Reference[EventClass]


@dataclass(frozen=True, slots=True)
class EventCode:
    """Resolved class/selector representation of one architectural event."""

    class_value: int
    selector: EventSelector
    event_selector: int | None

    @property
    def value(self) -> int | None:
        if self.event_selector is None:
            return None
        return compose_event_code(self.class_value, self.event_selector)


@dataclass(frozen=True, slots=True)
class ResolvedEvent:
    """Leaf event joined with its owner, overlay class, root class, and code."""

    owner: str
    event_class: EventClass
    root_class: EventClassDefinition
    event: ArchitecturalEvent
    code: EventCode


@dataclass(frozen=True, slots=True)
class EventNamespace:
    """All architectural events owned by base or one extension."""

    owner: str
    root: Path
    class_inventory: EventInventory
    classes: Mapping[str, EventClass]


@dataclass(frozen=True, slots=True)
class EventReferenceIndexes:
    """Typed global event logical-reference indexes."""

    classes: ReferenceIndex[EventClass]
    events: ReferenceIndex[ArchitecturalEvent]


@dataclass(frozen=True, slots=True)
class EventCatalog:
    """The union of base and extension-owned event definitions."""

    namespaces: Mapping[str, EventNamespace]
    references: EventReferenceIndexes

    @classmethod
    def load(
        cls,
        isa_root: str | Path,
        extension_catalog: ExtensionSetCatalog | None = None,
    ) -> "EventCatalog":
        root = Path(isa_root).resolve()
        extensions = extension_catalog or ExtensionSetCatalog.load(root)
        references = EventReferenceIndexes(
            ReferenceIndex[EventClass](), ReferenceIndex[ArchitecturalEvent]()
        )
        namespaces: dict[str, EventNamespace] = {}
        for owner, namespace_root in extensions.owner_roots():
            namespaces[owner] = _load_namespace(owner, namespace_root, root, references)
        return cls(MappingProxyType(namespaces), references)

    @property
    def base(self) -> EventNamespace:
        return self.namespaces["base"]

    def namespace(self, owner: str) -> EventNamespace:
        try:
            return self.namespaces[owner]
        except KeyError as error:
            raise ValueError(f"unknown event namespace {owner!r}") from error

    def root_class(self, event_class: EventClass) -> EventClassDefinition:
        """Resolve an event class overlay to its numeric class definition."""

        active: list[Reference[EventClass]] = []
        current = event_class
        while isinstance(current, EventClassOverlay):
            if current.reference in active:
                cycle = (*active[active.index(current.reference) :], current.reference)
                raise ValueError(
                    "circular event class overlay: "
                    + " -> ".join(str(reference) for reference in cycle)
                )
            active.append(current.reference)
            current = self.references.classes.resolve(current.extends)
        if not isinstance(current, EventClassDefinition):
            raise ValueError(f"incomplete event class definition {current.id!r}")
        return current

    def selected_events(
        self, owners: set[str] | frozenset[str]
    ) -> tuple[tuple[EventClass, ArchitecturalEvent], ...]:
        """Return owner-selected events in inventory order with their class fragments."""

        return tuple(
            (resolved.event_class, resolved.event)
            for resolved in self.resolved_events(owners)
        )

    def resolved_events(
        self, owners: set[str] | frozenset[str] | None = None
    ) -> tuple[ResolvedEvent, ...]:
        """Return fully resolved leaf-event views in authored inventory order."""

        selected = frozenset(self.namespaces) if owners is None else frozenset(owners)
        result: list[ResolvedEvent] = []
        for owner, namespace in self.namespaces.items():
            if owner not in selected:
                continue
            for event_class in namespace.classes.values():
                root = self.root_class(event_class)
                for event in event_class.events.values():
                    result.append(
                        ResolvedEvent(
                            owner,
                            event_class,
                            root,
                            event,
                            EventCode(root.value, root.selector, event.code),
                        )
                    )
        return tuple(result)


def compose_event_code(class_value: int, selector: int) -> int:
    """Compose the fixed 8-bit class and 24-bit selector representation."""

    for name, value, limit in (
        ("class", class_value, 1 << 8),
        ("selector", selector, 1 << 24),
    ):
        if not isinstance(value, int) or isinstance(value, bool) or not 0 <= value < limit:
            raise ValueError(f"event {name} value {value!r} is out of range")
    return class_value << 24 | selector


def _load_namespace(
    owner: str,
    namespace_root: Path,
    isa_root: Path,
    references: EventReferenceIndexes,
) -> EventNamespace:
    classes_root = namespace_root / "events/classes"
    inventory = _load_inventory(owner, classes_root, "classes")
    classes: dict[str, EventClass] = {}
    for class_id in inventory.declared:
        class_root = classes_root / class_id
        if class_id in classes or not class_root.is_dir():
            continue
        event_class = _load_class(owner, class_root, isa_root, references)
        references.classes.register(event_class.reference, event_class)
        classes[class_id] = event_class
    return EventNamespace(owner, namespace_root, inventory, MappingProxyType(classes))


def _load_class(
    owner: str,
    root: Path,
    isa_root: Path,
    references: EventReferenceIndexes,
) -> EventClass:
    source = root / "class.yaml"
    raw = _load_validated(source, isa_root / "schemas/event-class.yaml")
    class_id = root.name
    reference: Reference[EventClass] = Reference(
        owner, ("events",), class_id
    )
    events_root = root / "events"
    inventory = _load_inventory(owner, events_root, "events")
    events: dict[str, ArchitecturalEvent] = {}
    for event_id in inventory.declared:
        event_root = events_root / event_id
        if event_id in events or not event_root.is_dir():
            continue
        event = _load_event(owner, class_id, event_root, isa_root)
        references.events.register(event.reference, event)
        events[event_id] = event
    common = (
        reference,
        source,
        root,
        class_id,
        inventory,
        MappingProxyType(events),
    )
    if "extends" in raw:
        return EventClassOverlay(
            *common, Reference.parse(cast(str, raw["extends"]))
        )
    selector_raw = cast(Mapping[str, object], raw["selector"])
    return EventClassDefinition(
        *common,
        cast(str, raw["name"]),
        cast(int, raw["value"]),
        EventSelector(
            cast(str, selector_raw["kind"]), cast(int, selector_raw["bits"])
        ),
    )


def _load_event(
    owner: str, class_id: str, root: Path, isa_root: Path
) -> ArchitecturalEvent:
    source = root / "event.yaml"
    raw = _load_validated(source, isa_root / "schemas/event.yaml")
    event_id = root.name
    return ArchitecturalEvent(
        reference=Reference(owner, ("events", class_id), event_id),
        source=source,
        root=root,
        id=event_id,
        name=cast(str, raw["name"]),
        summary=cast(str, raw["summary"]),
        code=cast(int | None, raw.get("code")),
        family=cast(str | None, raw.get("family")),
        frame=cast(str, raw["frame"]),
        payload=tuple(cast(list[str], raw.get("payload", ()))),
    )


def _load_inventory(owner: str, root: Path, key: str) -> EventInventory:
    return EventInventory.inspect(
        owner=owner,
        kind={"classes": "class", "events": "event"}[key],
        source=root / f"{key}.yaml",
        root=root,
        key=key,
        allow_missing=True,
        name_pattern=r"[A-Z][A-Z0-9_]*",
    )


def _load_validated(path: Path, schema_path: Path) -> dict[str, object]:
    return SchemaValidatedYamlLoader().load(path, schema_path)
