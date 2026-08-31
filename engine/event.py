"""Distributed architectural-event registry loading and lookup."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from types import MappingProxyType
from typing import cast

from .extension import ExtensionSetCatalog
from .reference import Reference, ReferenceIndex
from .yaml_document import SchemaValidatedYamlLoader, YamlDocumentLoader


@dataclass(frozen=True, slots=True)
class EventInventory:
    """One closed-world event class or event directory inventory."""

    owner: str
    source: Path
    root: Path
    declared: tuple[str, ...]
    actual: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class EventSelector:
    """How an event class interprets the low event-code bits."""

    kind: str
    bits: int


@dataclass(frozen=True, slots=True)
class ArchitecturalEvent:
    """One independently allocated leaf architectural event."""

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
class EventClass:
    """One event-code class definition or extension overlay."""

    reference: Reference["EventClass"]
    source: Path
    root: Path
    id: str
    name: str | None
    value: int | None
    selector: EventSelector | None
    extends: Reference["EventClass"] | None
    event_inventory: EventInventory
    events: Mapping[str, ArchitecturalEvent]


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
    root_class: EventClass
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
    """The union of base and extension-owned event allocations."""

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
        for owner, namespace_root in (
            ("base", root),
            *((extension_id, extensions.root / extension_id) for extension_id in extensions.declared),
        ):
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

    def root_class(self, event_class: EventClass) -> EventClass:
        """Resolve an event class overlay to its numeric class definition."""

        active: list[Reference[EventClass]] = []
        current = event_class
        while current.extends is not None:
            if current.reference in active:
                cycle = (*active[active.index(current.reference) :], current.reference)
                raise ValueError(
                    "circular event class overlay"
                )
            active.append(current.reference)
            current = self.references.classes.resolve(current.extends)
        if current.value is None or current.selector is None:
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
                assert root.value is not None and root.selector is not None
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
    if raw["id"] != root.name:
        raise ValueError(
            f"{source}: event class ID {raw['id']!r} does not match directory {root.name!r}"
        )
    class_id = cast(str, raw["id"])
    reference: Reference[EventClass] = Reference(
        owner, ("events",), class_id
    )
    selector_raw = raw.get("selector")
    selector = (
        EventSelector(
            cast(str, cast(Mapping[str, object], selector_raw)["kind"]),
            cast(int, cast(Mapping[str, object], selector_raw)["bits"]),
        )
        if selector_raw is not None
        else None
    )
    extends: Reference[EventClass] | None = (
        Reference.parse(cast(str, raw["extends"])) if "extends" in raw else None
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
    return EventClass(
        reference=reference,
        source=source,
        root=root,
        id=class_id,
        name=cast(str | None, raw.get("name")),
        value=cast(int | None, raw.get("value")),
        selector=selector,
        extends=extends,
        event_inventory=inventory,
        events=MappingProxyType(events),
    )


def _load_event(
    owner: str, class_id: str, root: Path, isa_root: Path
) -> ArchitecturalEvent:
    source = root / "event.yaml"
    raw = _load_validated(source, isa_root / "schemas/event.yaml")
    if raw["id"] != root.name:
        raise ValueError(
            f"{source}: event ID {raw['id']!r} does not match directory {root.name!r}"
        )
    event_id = cast(str, raw["id"])
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
    source = root.parent / f"{key}.yaml"
    declared = _load_name_list(source, key) if source.is_file() else ()
    actual = (
        tuple(sorted(path.name for path in root.iterdir() if path.is_dir() and not path.name.startswith(".")))
        if root.is_dir()
        else ()
    )
    return EventInventory(owner, source, root, declared, actual)


def _load_name_list(path: Path, key: str) -> tuple[str, ...]:
    raw = _load_mapping(path)
    values = raw.get(key)
    if not isinstance(values, list) or any(not isinstance(value, str) for value in values):
        raise ValueError(f"{path}: expected a {key} list of strings")
    return tuple(values)


def _load_validated(path: Path, schema_path: Path) -> dict[str, object]:
    return SchemaValidatedYamlLoader().load(path, schema_path)


def _load_mapping(path: Path) -> dict[str, object]:
    return YamlDocumentLoader().mapping(path)
