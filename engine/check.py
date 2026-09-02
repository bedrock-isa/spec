"""Relational validation for the complete ISA authoring model."""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Iterable, Iterator, Mapping
from dataclasses import dataclass
import logging
from pathlib import Path
from typing import Any

from .encoding_space import EncodingCube, forms_overlap, numeric_bounds, reservation_cube
from .cpuid import (
    CpuidClassDefinition,
    CpuidCatalog,
    CpuidLeaf,
    CpuidLeafDefinition,
    CpuidLeafOverlay,
    CpuidQuery,
    CpuidResolutionError,
)
from .control_register import ControlRegister, ControlRegisterCatalog
from .diagnostics import Diagnostic, DiagnosticBag, RelatedLocation, Severity
from .encoding import OperandConstraint
from .encoding_architecture import ENCODING_CLASSES_BY_WIDTH, encoding_class
from .encoding_reservation import (
    EncodingReservation,
    EncodingReservationCatalog,
    EncodingReservationRegion,
)
from .event import EventCatalog, EventClass, EventClassDefinition, EventClassOverlay
from .observability import log_phase
from .project import IsaProject, InstructionBundle
from .reference import Reference, ReferenceError
from .register import (
    ConstantReset,
    ExplicitRegisterGroup,
    Register,
    RegisterCatalog,
    RegisterGroup,
    RegisterInventory,
    SourcedReset,
)
from .semantic_text import TermReferenceText
from .terminology import Term, TermCatalog, TerminologyInventory
from .instruction_metasyntax import OperandReference
from .type_system import (
    RegisterFieldType,
    RegisterPairSelectorFieldType,
    RegisterSelectorFieldType,
    RegisterSelectorPayloadType,
    SizeSelectorFieldType,
    TypeSystem,
)
from .validation import SailEntryValidator


_LOGGER = logging.getLogger(__name__)


def _error(
    code: str,
    source: Path,
    message: str,
    *path: str | int,
    related: tuple[RelatedLocation, ...] = (),
) -> Diagnostic:
    return Diagnostic(Severity.ERROR, code, source, message, tuple(path), related)


class BundleValidator:
    """Validate relationships owned by one instruction bundle."""

    def validate(
        self, bundle: InstructionBundle, project: IsaProject
    ) -> Iterator[Diagnostic]:
        source = bundle.encodings.source
        mnemonic = bundle.instruction.mnemonic
        operands: Mapping[str, Mapping[str, Any]] = bundle.instruction["operands"]

        for companion, path in (
            ("semantics", bundle.artifacts.semantics),
            ("description", bundle.artifacts.description),
        ):
            if not path.is_file():
                yield _error(
                    "artifact.missing",
                    path,
                    f"{mnemonic} has no required {companion} artifact",
                )

        missing_entry = SailEntryValidator().missing(bundle)
        if missing_entry is not None:
            yield _error(
                "sail.entry",
                bundle.instruction.source,
                f"instruction-owned Sail entry {missing_entry!r} is not defined by "
                f"{bundle.artifacts.semantics}",
                "mnemonic",
            )

        for form in bundle.encodings.forms:
            base = ("encodings", form.id)
            owner = ENCODING_CLASSES_BY_WIDTH.get(form.pattern.bit_width)
            if owner is None:
                yield _error(
                    "encoding.class",
                    source,
                    f"pattern width {form.pattern.bit_width} has no encoding class",
                    *base,
                    "pattern",
                )
            else:
                raw_cube = EncodingCube.from_encoding(form)
                namespaces = tuple(
                    EncodingCube.parse(pattern) for pattern in owner.namespace
                )
                if not any(namespace.contains(raw_cube) for namespace in namespaces):
                    yield _error(
                        "encoding.namespace",
                        source,
                        f"pattern is outside the {owner.name} namespace",
                        *base,
                        "pattern",
                    )
                for reservation in project.encoding_reservations.reservations.values():
                    for region_index, region in enumerate(reservation.regions):
                        if region.encoding_class != owner.name:
                            continue
                        try:
                            reserved_cube = reservation_cube(region)
                        except ValueError:
                            continue
                        if not raw_cube.overlaps(reserved_cube):
                            continue
                        yield _error(
                            "encoding.reserved",
                            source,
                            f"{mnemonic}.{form.id} overlaps opcode reservation "
                            f"{reservation.id}",
                            *base,
                            "pattern",
                            related=(
                                RelatedLocation(
                                    reservation.source,
                                    reservation.summary,
                                    ("regions", region_index, "prefix"),
                                ),
                            ),
                        )
            if form.syntax.mnemonic != mnemonic:
                yield _error(
                    "syntax.mnemonic",
                    source,
                    f"syntax names {form.syntax.mnemonic}, expected {mnemonic}",
                    *base,
                    "syntax",
                )
            if form.syntax.encoding_id != form.id:
                yield _error(
                    "syntax.encoding-id",
                    source,
                    f"syntax derives encoding ID {form.syntax.encoding_id!r}",
                    *base,
                    "syntax",
                )

            markers = frozenset(field.marker for field in form.fields)
            if markers != form.pattern.fields:
                yield _error(
                    "pattern.fields",
                    source,
                    f"pattern fields {sorted(form.pattern.fields)} do not match "
                    f"bindings {sorted(markers)}",
                    *base,
                    "fields",
                )

            representation_roles = [
                *(field.role for field in form.fields),
                *(payload.role for payload in form.payloads),
            ]
            duplicates = sorted(
                role
                for role in set(representation_roles)
                if representation_roles.count(role) > 1
            )
            for role in duplicates:
                yield _error(
                    "representation.duplicate-role",
                    source,
                    f"role {role!r} has more than one field or payload representation",
                    *base,
                )

            for field in form.fields:
                definition = project.types.field_types.resolve(field.type)
                width = definition.bits
                actual = form.pattern.field_width(field.marker)
                if width != actual:
                    yield _error(
                        "field.width",
                        source,
                        f"field {field.marker!r} occupies {actual} bits but "
                        f"{field.type} declares {width}",
                        *base,
                        "fields",
                        field.marker,
                    )
                yield from self._validate_representation_access(
                    source, base, field.role, field.access, operands
                )

            for payload_index, payload in enumerate(form.payloads):
                yield from self._validate_representation_access(
                    source, base, payload.role, payload.access, operands, payload_index
                )

            for displayed in form.syntax.displayed_operands:
                if (
                    isinstance(displayed, OperandReference)
                    and displayed.field is not None
                    and displayed.field not in markers
                ):
                    yield _error(
                        "syntax.unknown-field",
                        source,
                        f"syntax references field {displayed.field!r} with no binding",
                        *base,
                        "syntax",
                    )

            if form.syntax.size_field is not None:
                size_binding = form.field_for_marker(form.syntax.size_field)
                if size_binding is None or size_binding.role != "size":
                    yield _error(
                        "syntax.size-field",
                        source,
                        f"selected size field {form.syntax.size_field!r} is not bound "
                        "to role 'size'",
                        *base,
                        "syntax",
                    )
                elif size_binding is not None:
                    definition = project.types.field_types.resolve(size_binding.type)
                    declared_codes = tuple(
                        value.code for value in definition.values
                    ) if isinstance(definition, SizeSelectorFieldType) else ()
                    if not set(form.syntax.selected_size_codes).issubset(
                        declared_codes
                    ):
                        yield _error(
                            "syntax.size-codes",
                            source,
                            f"size alternatives {form.syntax.selected_size_codes} are not "
                            f"a subset of {size_binding.type} values {declared_codes}",
                            *base,
                            "syntax",
                        )

            constraint_roles: set[str] = set()
            for index, constraint in enumerate(form.constraints):
                constraint_field = form.field_for_role(constraint.role)
                if constraint_field is None:
                    yield _error(
                        "constraint.role",
                        source,
                        f"constraint role {constraint.role!r} does not resolve to a field",
                        *base,
                        "constraints",
                        index,
                        "role",
                    )
                    continue
                if constraint.role in constraint_roles:
                    yield _error(
                        "constraint.duplicate-role",
                        source,
                        f"role {constraint.role!r} has multiple constraints",
                        *base,
                        "constraints",
                        index,
                    )
                constraint_roles.add(constraint.role)
                yield from self._validate_constraint_values(
                    source,
                    base,
                    index,
                    constraint,
                    form.pattern.field_width(constraint_field.marker),
                )

            for index, overlap in enumerate(form.overlaps):
                for role in overlap.operands:
                    operand = operands.get(role)
                    overlap_field = form.field_for_role(role)
                    if operand is None or overlap_field is None:
                        yield _error(
                            "overlap.operand",
                            source,
                            f"overlap operand {role!r} must be a field-backed logical operand",
                            *base,
                            "overlaps",
                            index,
                        )
                    elif overlap.type == "same_value" and operand["access"] not in {
                        "write",
                        "read_write",
                    }:
                        yield _error(
                            "overlap.access",
                            source,
                            f"same_value overlap operand {role!r} is not writable",
                            *base,
                            "overlaps",
                            index,
                        )

    @staticmethod
    def _validate_representation_access(
        source: Path,
        base: tuple[str, str],
        role: str,
        access: str | None,
        operands: Mapping[str, Mapping[str, Any]],
        payload_index: int | None = None,
    ) -> Iterator[Diagnostic]:
        operand = operands.get(role)
        if operand is None:
            if role != "size":
                location: tuple[str | int, ...] = (
                    (*base, "fields")
                    if payload_index is None
                    else (*base, "payloads", payload_index)
                )
                yield _error(
                    "representation.role",
                    source,
                    f"role {role!r} is neither an instruction operand nor a known selector",
                    *location,
                )
            return
        if access is not None and access == operand["access"]:
            yield _error(
                "representation.redundant-access",
                source,
                f"role {role!r} repeats inherited access {access!r}",
                *base,
            )

    @staticmethod
    def _validate_constraint_values(
        source: Path,
        base: tuple[str, str],
        index: int,
        constraint: OperandConstraint,
        width: int,
    ) -> Iterator[Diagnostic]:
        limit = 1 << width
        for value in constraint.values:
            bounds = numeric_bounds(value)
            if bounds is None:
                continue
            lower, upper = bounds
            if lower > upper or lower < 0 or upper >= limit:
                yield _error(
                    "constraint.range",
                    source,
                    f"constraint value {value!r} is outside unsigned {width}-bit range",
                    *base,
                    "constraints",
                    index,
                )


class CatalogValidator:
    """Validate declared inventories and cross-form opcode relationships."""

    def validate(
        self,
        project: IsaProject,
        selected: tuple[InstructionBundle, ...],
        *,
        complete: bool,
    ) -> Iterator[Diagnostic]:
        if complete:
            extension_catalog = project.catalog.extension_catalog
            for missing in extension_catalog.missing:
                yield _error(
                    "extension.missing-directory",
                    extension_catalog.source,
                    f"declared extension {missing!r} has no directory",
                )
            for undeclared in extension_catalog.undeclared:
                yield _error(
                    "extension.undeclared-directory",
                    extension_catalog.root / undeclared,
                    f"extension directory {undeclared!r} is not in "
                    f"{extension_catalog.source.name}",
                )
            for duplicate in extension_catalog.duplicates:
                yield _error(
                    "extension.duplicate",
                    extension_catalog.source,
                    f"extension {duplicate!r} is listed more than once",
                )

            instruction_sets = (
                project.catalog.base,
                *(
                    extension.instruction_set
                    for extension in project.catalog.extensions.values()
                ),
            )
            for instruction_set in instruction_sets:
                catalog = instruction_set.catalog
                for missing in catalog.missing:
                    yield _error(
                        "catalog.missing-directory",
                        catalog.source,
                        f"declared instruction {missing!r} has no directory",
                    )
                for undeclared in catalog.undeclared:
                    yield _error(
                        "catalog.undeclared-directory",
                        catalog.root / undeclared,
                        f"instruction directory {undeclared!r} is not in {catalog.source.name}",
                    )
                for duplicate in catalog.duplicates:
                    yield _error(
                        "catalog.duplicate",
                        catalog.source,
                        f"instruction {duplicate!r} is listed more than once",
                    )

        selected_refs = {bundle.reference for bundle in selected}
        all_forms = [
            (bundle, form)
            for bundle in project.select()
            for form in bundle.encodings.forms
        ]
        for index, (left_bundle, left) in enumerate(all_forms):
            for right_bundle, right in all_forms[index + 1 :]:
                if (
                    left_bundle.reference not in selected_refs
                    and right_bundle.reference not in selected_refs
                ):
                    continue
                if not left.pattern.overlaps(right.pattern):
                    continue
                if not forms_overlap(left, right):
                    continue
                related = (
                    RelatedLocation(
                        right_bundle.encodings.source,
                        f"conflicts with {right_bundle.instruction.mnemonic}.{right.id}",
                        ("encodings", right.id, "pattern"),
                    ),
                )
                yield _error(
                    "encoding.overlap",
                    left_bundle.encodings.source,
                    f"{left_bundle.instruction.mnemonic}.{left.id} overlaps "
                    f"{right_bundle.instruction.mnemonic}.{right.id}",
                    "encodings",
                    left.id,
                    "pattern",
                    related=related,
                )


class EncodingReservationValidator:
    """Validate the closed reservation inventory and its encoding relations."""

    def validate(self, catalog: EncodingReservationCatalog) -> Iterator[Diagnostic]:
        inventory = catalog.inventory
        for missing in inventory.missing:
            yield _error(
                "encoding-reservation.missing-directory",
                inventory.source,
                f"declared reservation {missing!r} has no directory",
            )
        for undeclared in inventory.undeclared:
            yield _error(
                "encoding-reservation.undeclared-directory",
                inventory.root / undeclared,
                f"reservation directory {undeclared!r} is not in "
                f"{inventory.source.name}",
            )
        for duplicate in inventory.duplicates:
            yield _error(
                "encoding-reservation.duplicate",
                inventory.source,
                f"reservation {duplicate!r} is listed more than once",
            )

        resolved: list[
            tuple[
                EncodingReservation,
                int,
                EncodingReservationRegion,
                EncodingCube,
            ]
        ] = []
        for reservation in catalog.reservations.values():
            for region_index, region in enumerate(reservation.regions):
                base = ("regions", region_index)
                try:
                    owner = encoding_class(region.encoding_class)
                except ValueError:
                    yield _error(
                        "encoding-reservation.class",
                        reservation.source,
                        f"unknown encoding class {region.encoding_class!r}",
                        *base,
                        "encoding_class",
                    )
                    continue
                try:
                    cube = reservation_cube(region)
                except ValueError as error:
                    yield _error(
                        "encoding-reservation.prefix",
                        reservation.source,
                        str(error),
                        *base,
                        "prefix",
                    )
                    continue
                namespaces = tuple(
                    EncodingCube.parse(pattern) for pattern in owner.namespace
                )
                if not any(namespace.contains(cube) for namespace in namespaces):
                    yield _error(
                        "encoding-reservation.namespace",
                        reservation.source,
                        f"prefix is outside the {owner.name} namespace",
                        *base,
                        "prefix",
                    )
                    continue
                resolved.append((reservation, region_index, region, cube))

        for index, (left, left_index, left_region, left_cube) in enumerate(resolved):
            for right, right_index, right_region, right_cube in resolved[index + 1 :]:
                if not left_cube.overlaps(right_cube):
                    continue
                yield _error(
                    "encoding-reservation.overlap",
                    left.source,
                    f"{left_region.encoding_class} region in reservation {left.id} "
                    f"overlaps {right_region.encoding_class} region in reservation "
                    f"{right.id}",
                    "regions",
                    left_index,
                    "prefix",
                    related=(
                        RelatedLocation(
                            right.source,
                            f"conflicting reservation {right.id}",
                            ("regions", right_index, "prefix"),
                        ),
                    ),
                )


class CpuidValidator:
    """Validate distributed CPUID catalogs, overlays, and numeric values."""

    def validate(self, catalog: CpuidCatalog) -> Iterator[Diagnostic]:
        yield from self._validate_inventories(catalog)
        try:
            resolved = catalog.resolved_leaves()
        except CpuidResolutionError as error:
            yield _error("cpuid.resolution", error.source, str(error))
            return
        leaf_values = {
            item.leaf.reference: (item.class_value, item.leaf_value)
            for item in resolved
        }
        leaf_roots = {
            item.leaf.reference: item.root_leaf.reference for item in resolved
        }
        yield from self._validate_class_values(catalog)
        yield from self._validate_leaf_values(catalog, leaf_values)
        yield from self._validate_query_indexes(catalog, leaf_values, leaf_roots)

    @staticmethod
    def _validate_inventories(catalog: CpuidCatalog) -> Iterator[Diagnostic]:
        for namespace in catalog.namespaces.values():
            inventories = [namespace.class_inventory]
            inventories.extend(
                cpuid_class.leaf_inventory for cpuid_class in namespace.classes.values()
            )
            for inventory in inventories:
                kind = inventory.kind
                for missing in inventory.missing:
                    yield _error(
                        f"cpuid.{kind}.missing-directory",
                        inventory.source,
                        f"declared CPUID {kind} {missing!r} has no directory",
                    )
                for undeclared in inventory.undeclared:
                    yield _error(
                        f"cpuid.{kind}.undeclared-directory",
                        inventory.root / undeclared,
                        f"CPUID {kind} directory {undeclared!r} is not in "
                        f"{inventory.source.name}",
                    )
                for duplicate in inventory.duplicates:
                    yield _error(
                        f"cpuid.{kind}.duplicate",
                        inventory.source,
                        f"CPUID {kind} {duplicate!r} is listed more than once",
                    )

    @staticmethod
    def _validate_class_values(catalog: CpuidCatalog) -> Iterator[Diagnostic]:
        definitions = [
            cpuid_class
            for cpuid_class in catalog.references.classes.values()
            if isinstance(cpuid_class, CpuidClassDefinition)
        ]
        for index, left in enumerate(definitions):
            for right in definitions[index + 1 :]:
                if left.value != right.value:
                    continue
                yield _error(
                    "cpuid.class.value-overlap",
                    left.source,
                    f"class value 0x{left.value:08x} is also assigned to {right.id!r}",
                    "value",
                    related=(
                        RelatedLocation(right.source, "conflicting class value"),
                    ),
                )

    @staticmethod
    def _validate_leaf_values(
        catalog: CpuidCatalog,
        leaf_values: Mapping[Reference[CpuidLeaf], tuple[int, int]],
    ) -> Iterator[Diagnostic]:
        definitions: list[tuple[tuple[int, int], CpuidLeaf]] = []
        for namespace in catalog.namespaces.values():
            for cpuid_class in namespace.classes.values():
                for leaf in cpuid_class.leaves.values():
                    if isinstance(leaf, CpuidLeafOverlay):
                        continue
                    selector = leaf_values.get(leaf.reference)
                    if selector is not None:
                        definitions.append((selector, leaf))
        for index, (left_selector, left) in enumerate(definitions):
            for right_selector, right in definitions[index + 1 :]:
                if left_selector != right_selector:
                    continue
                path = ("value",) if isinstance(left, CpuidLeafDefinition) else ()
                yield _error(
                    "cpuid.leaf.value-overlap",
                    left.source,
                    f"leaf value 0x{left_selector[1]:04x} in class "
                    f"0x{left_selector[0]:08x} "
                    f"is also assigned to {right.id!r}",
                    *path,
                    related=(
                        RelatedLocation(right.source, "conflicting leaf value"),
                    ),
                )

    @staticmethod
    def _validate_query_indexes(
        catalog: CpuidCatalog,
        leaf_values: Mapping[Reference[CpuidLeaf], tuple[int, int]],
        leaf_roots: Mapping[Reference[CpuidLeaf], Reference[CpuidLeaf]],
    ) -> Iterator[Diagnostic]:
        entries: list[tuple[tuple[int, int], Reference[CpuidLeaf], CpuidQuery]] = []
        for namespace in catalog.namespaces.values():
            for cpuid_class in namespace.classes.values():
                for leaf in cpuid_class.leaves.values():
                    selector = leaf_values.get(leaf.reference)
                    root = leaf_roots.get(leaf.reference)
                    if selector is None or root is None:
                        continue
                    for query in leaf.queries:
                        for field in query.fields:
                            if field.msb > 63:
                                yield _error(
                                    "cpuid.field.range",
                                    field.source,
                                    f"field {field.id!r} occupies bits "
                                    f"{field.msb}..{field.lsb} outside a 64-bit result",
                                    "queries",
                                )
                        for field_index, left_field in enumerate(query.fields):
                            for right_field in query.fields[field_index + 1 :]:
                                if left_field.overlaps(right_field):
                                    yield _error(
                                        "cpuid.field.overlap",
                                        left_field.source,
                                        f"fields {left_field.id!r} and {right_field.id!r} overlap",
                                        "queries",
                                    )
                        entries.append((selector, root, query))

        for index, (left_selector, left_root, left) in enumerate(entries):
            for right_selector, right_root, right in entries[index + 1 :]:
                if left_selector != right_selector or not left.indexes.overlaps(
                    right.indexes
                ):
                    continue
                same_overlay_query = (
                    left_root == right_root
                    and left.id == right.id
                    and left.indexes == right.indexes
                )
                if not same_overlay_query:
                    yield _error(
                        "cpuid.query.index-overlap",
                        left.source,
                        f"query {left.id!r} overlaps {right.id!r} in "
                        f"class 0x{left_selector[0]:08x}, leaf 0x{left_selector[1]:04x}",
                        "queries",
                        related=(
                            RelatedLocation(
                                right.source, "conflicting query index"
                            ),
                        ),
                    )
                    continue
                for left_field in left.fields:
                    for right_field in right.fields:
                        if left_field.overlaps(right_field):
                            yield _error(
                                "cpuid.field.overlay-overlap",
                                left_field.source,
                                f"field {left_field.id!r} overlaps "
                                f"{right_field.id!r} in a shared query",
                                "queries",
                                related=(
                                    RelatedLocation(
                                        right_field.source,
                                        "conflicting result field",
                                    ),
                                ),
                            )


class EventValidator:
    """Validate distributed event inventories, overlays, and event codes."""

    def validate(self, catalog: EventCatalog) -> Iterator[Diagnostic]:
        yield from self._validate_inventories(catalog)
        roots, diagnostics = self._resolve_classes(catalog)
        yield from diagnostics
        yield from self._validate_class_values(catalog)
        yield from self._validate_events(catalog, roots)

    @staticmethod
    def _validate_inventories(catalog: EventCatalog) -> Iterator[Diagnostic]:
        for namespace in catalog.namespaces.values():
            inventories = [namespace.class_inventory]
            inventories.extend(
                event_class.event_inventory
                for event_class in namespace.classes.values()
            )
            for inventory in inventories:
                kind = inventory.kind
                for missing in inventory.missing:
                    yield _error(
                        f"event.{kind}.missing-directory",
                        inventory.source,
                        f"declared event {kind} {missing!r} has no directory",
                    )
                for undeclared in inventory.undeclared:
                    yield _error(
                        f"event.{kind}.undeclared-directory",
                        inventory.root / undeclared,
                        f"event {kind} directory {undeclared!r} is not in "
                        f"{inventory.source.name}",
                    )
                for duplicate in inventory.duplicates:
                    yield _error(
                        f"event.{kind}.duplicate",
                        inventory.source,
                        f"event {kind} {duplicate!r} is listed more than once",
                    )

    @staticmethod
    def _resolve_classes(
        catalog: EventCatalog,
    ) -> tuple[dict[Reference[EventClass], EventClass], tuple[Diagnostic, ...]]:
        roots: dict[Reference[EventClass], EventClass] = {}
        diagnostics: list[Diagnostic] = []
        active: list[Reference[EventClass]] = []

        def resolve(event_class: EventClass) -> EventClass | None:
            if event_class.reference in roots:
                return roots[event_class.reference]
            if event_class.reference in active:
                cycle = (
                    *active[active.index(event_class.reference) :],
                    event_class.reference,
                )
                diagnostics.append(
                    _error(
                        "event.class.extend-cycle",
                        event_class.source,
                        "circular event class overlay: "
                        + " -> ".join(
                            catalog.references.classes.resolve(item).id
                            for item in cycle
                        ),
                    )
                )
                return None
            if not isinstance(event_class, EventClassOverlay):
                roots[event_class.reference] = event_class
                return event_class
            try:
                target = catalog.references.classes.resolve(event_class.extends)
            except ValueError:
                diagnostics.append(
                    _error(
                        "event.class.unknown-extends",
                        event_class.source,
                        "unknown event class overlay target",
                        "extends",
                    )
                )
                return None
            if event_class.id != target.id:
                diagnostics.append(
                    _error(
                        "event.class.extend-id",
                        event_class.source,
                        f"class ID {event_class.id!r} does not match overlay target "
                        f"ID {target.id!r}",
                        "extends",
                    )
                )
            active.append(event_class.reference)
            root = resolve(target)
            active.pop()
            if root is not None:
                roots[event_class.reference] = root
            return root

        for event_class in catalog.references.classes.values():
            resolve(event_class)
        return roots, tuple(diagnostics)

    @staticmethod
    def _validate_class_values(catalog: EventCatalog) -> Iterator[Diagnostic]:
        definitions = [
            event_class
            for event_class in catalog.references.classes.values()
            if isinstance(event_class, EventClassDefinition)
        ]
        for index, left in enumerate(definitions):
            for right in definitions[index + 1 :]:
                if left.value != right.value:
                    continue
                yield _error(
                    "event.class.value-overlap",
                    left.source,
                    f"class value 0x{left.value:02x} is also assigned to {right.id!r}",
                    "value",
                    related=(
                        RelatedLocation(right.source, "conflicting class value"),
                    ),
                )

    @staticmethod
    def _validate_events(
        catalog: EventCatalog,
        roots: Mapping[Reference[EventClass], EventClass],
    ) -> Iterator[Diagnostic]:
        assigned_codes: dict[tuple[Reference[EventClass], int], Any] = {}
        event_ids: dict[str, Any] = {}
        for event_class in catalog.references.classes.values():
            root = roots.get(event_class.reference)
            if not isinstance(root, EventClassDefinition):
                continue
            for event in event_class.events.values():
                previous_id = event_ids.get(event.id)
                if previous_id is not None:
                    yield _error(
                        "event.id-overlap",
                        event.source,
                        f"event ID {event.id!r} is also used by {previous_id.id!r}",
                        "id",
                        related=(
                            RelatedLocation(previous_id.source, "conflicting event ID"),
                        ),
                    )
                else:
                    event_ids[event.id] = event

                if root.selector.kind == "fixed":
                    if event.code is None:
                        yield _error(
                            "event.code.missing",
                            event.source,
                            f"event in fixed-selector class {root.id} requires a code",
                            "code",
                        )
                        continue
                    if event.code >= 1 << root.selector.bits:
                        yield _error(
                            "event.code.range",
                            event.source,
                            f"event code 0x{event.code:x} exceeds the "
                            f"{root.selector.bits}-bit selector space",
                            "code",
                        )
                        continue
                    key = (root.reference, event.code)
                    previous = assigned_codes.get(key)
                    if previous is not None:
                        yield _error(
                            "event.code.overlap",
                            event.source,
                            f"event code 0x{event.code:06x} is also assigned to "
                            f"{previous.id!r}",
                            "code",
                            related=(
                                RelatedLocation(
                                    previous.source, "conflicting event code"
                                ),
                            ),
                        )
                    else:
                        assigned_codes[key] = event
                elif event.code is not None:
                    yield _error(
                        "event.code.external-selector",
                        event.source,
                        f"{root.selector.kind}-selected event must not fix a code",
                        "code",
                    )

                if event.frame == "basic" and event.payload:
                    yield _error(
                        "event.payload.basic-frame",
                        event.source,
                        "basic event frame cannot carry an event payload",
                        "payload",
                    )


class RegisterValidator:
    """Validate register inventories, layouts, reset state, and type bindings."""

    def validate(
        self,
        catalog: RegisterCatalog,
        types: TypeSystem,
        control_registers: ControlRegisterCatalog,
    ) -> Iterator[Diagnostic]:
        yield from self._validate_inventories(catalog)
        yield from self._validate_groups(catalog)
        yield from self._validate_resets(catalog, control_registers)
        yield from self._validate_types(catalog, types)

    @staticmethod
    def _validate_inventories(catalog: RegisterCatalog) -> Iterator[Diagnostic]:
        for namespace in catalog.namespaces.values():
            inventories = [namespace.group_inventory]
            inventories.extend(
                group.register_inventory
                for group in namespace.groups.values()
                if isinstance(group, ExplicitRegisterGroup)
            )
            for inventory in inventories:
                yield from RegisterValidator._validate_inventory(inventory)

    @staticmethod
    def _validate_inventory(inventory: RegisterInventory) -> Iterator[Diagnostic]:
        for missing in inventory.missing:
            yield _error(
                f"register.{inventory.kind}.missing-directory",
                inventory.source,
                f"declared register {inventory.kind} {missing!r} has no directory",
            )
        for undeclared in inventory.undeclared:
            yield _error(
                f"register.{inventory.kind}.undeclared-directory",
                inventory.root / undeclared,
                f"register {inventory.kind} directory {undeclared!r} is not in "
                f"{inventory.source.name}",
            )
        for duplicate in inventory.duplicates:
            yield _error(
                f"register.{inventory.kind}.duplicate",
                inventory.source,
                f"register {inventory.kind} {duplicate!r} is listed more than once",
            )

    @staticmethod
    def _validate_groups(catalog: RegisterCatalog) -> Iterator[Diagnostic]:
        for namespace in catalog.namespaces.values():
            for group in namespace.groups.values():
                encodings: dict[int, Register] = {}
                for register in group.registers.values():
                    if register.encoding is not None:
                        previous = encodings.get(register.encoding)
                        if previous is not None:
                            yield _error(
                                "register.encoding.duplicate",
                                register.source,
                                f"encoding {register.encoding} in group {group.id!r} "
                                "is used more than once",
                                "encoding",
                                related=(
                                    RelatedLocation(
                                        previous.source, "conflicting register encoding"
                                    ),
                                ),
                            )
                        else:
                            encodings[register.encoding] = register
                    layout = register.layout
                    if layout is None:
                        continue
                    if (
                        isinstance(register.width, int)
                        and layout.bits != register.width
                    ):
                        yield _error(
                            "register.layout.width",
                            layout.source,
                            f"layout has {layout.bits} bits but register {register.id!r} "
                            f"has width {register.width}",
                            "bits",
                        )
                    for field in layout.fields:
                        if field.msb >= layout.bits:
                            yield _error(
                                "register.layout.field-range",
                                layout.source,
                                f"field {field.id!r} occupies bits {field.msb}..{field.lsb} "
                                f"outside a {layout.bits}-bit layout",
                                "fields",
                            )
                    for index, left in enumerate(layout.fields):
                        for right in layout.fields[index + 1 :]:
                            if left.overlaps(right):
                                yield _error(
                                    "register.layout.field-overlap",
                                    layout.source,
                                    f"fields {left.id!r} and {right.id!r} overlap",
                                    "fields",
                                )

    @staticmethod
    def _validate_resets(
        catalog: RegisterCatalog, control_registers: ControlRegisterCatalog
    ) -> Iterator[Diagnostic]:
        active: list[Reference[Register]] = []
        resolved: set[Reference[Register]] = set()

        def resolve(register: Register) -> Iterator[Diagnostic]:
            reference = register.reference
            if reference in resolved:
                return
            reset = register.reset
            if isinstance(reset, ConstantReset):
                if (
                    isinstance(register.width, int)
                    and reset.value >= 1 << register.width
                ):
                    yield _error(
                        "register.reset.range",
                        register.source,
                        f"reset value {reset.value} does not fit {register.width}-bit "
                        f"register {register.id!r}",
                        "reset",
                    )
            if isinstance(reset, SourcedReset):
                try:
                    target = (
                        control_registers.references.registers.resolve(reset.source)
                        if reset.source.path[:1] == ("control_registers",)
                        else catalog.references.registers.resolve(reset.source)
                    )
                except (ReferenceError, ValueError):
                    yield _error(
                        "register.reset.unknown-source",
                        register.source,
                        "unknown reset source",
                        "reset",
                    )
                else:
                    if target.width != register.width:
                        yield _error(
                            "register.reset.width",
                            register.source,
                            f"reset source {target.id!r} has width {target.width}, "
                            f"expected {register.width}",
                            "reset",
                        )
                    if target.reference in active:
                        cycle = (
                            *active[active.index(target.reference) :],
                            target.reference,
                        )
                        yield _error(
                            "register.reset.cycle",
                            register.source,
                            "register reset cycle: "
                            + " -> ".join(
                                (
                                    control_registers.references.registers.resolve(
                                        item
                                    ).id
                                    if item.path[:1] == ("control_registers",)
                                    else catalog.references.registers.resolve(item).id
                                )
                                for item in cycle
                            ),
                            "reset",
                        )
                    else:
                        active.append(reference)
                        if target.reference.path[:1] == ("registers",):
                            yield from resolve(target)
                        active.pop()
            resolved.add(reference)

        for register in catalog.references.registers.values():
            yield from resolve(register)

    @staticmethod
    def _validate_types(
        catalog: RegisterCatalog, types: TypeSystem
    ) -> Iterator[Diagnostic]:
        for field in types.field_types.values():
            if not isinstance(
                field,
                (
                    RegisterFieldType,
                    RegisterSelectorFieldType,
                    RegisterPairSelectorFieldType,
                ),
            ):
                continue
            group = RegisterValidator._resolve_group(catalog, field.register_group)
            if group is None:
                yield _error(
                    "register.group.unknown",
                    field.source,
                    f"field type {field.id!r} uses an unknown register group",
                    "field_types",
                    field.id,
                    "register_group",
                )
                continue
            if isinstance(field, RegisterPairSelectorFieldType):
                yield from RegisterValidator._validate_pair_type(
                    group, field.bits, field.source
                )
            else:
                yield from RegisterValidator._validate_direct_type(
                    group,
                    field.bits,
                    field.source,
                    require_complete=isinstance(field, RegisterSelectorFieldType),
                )

        for payload in types.payload_types.values():
            if not isinstance(payload, RegisterSelectorPayloadType):
                continue
            group = RegisterValidator._resolve_group(catalog, payload.register_group)
            if group is None:
                yield _error(
                    "register.group.unknown",
                    payload.source,
                    f"payload type {payload.id!r} uses an unknown register group",
                    "payload_types",
                    payload.id,
                    "register_group",
                )
                continue
            yield from RegisterValidator._validate_direct_type(
                group, payload.bytes * 8, payload.source, require_complete=True
            )

    @staticmethod
    def _resolve_group(
        catalog: RegisterCatalog,
        reference: Reference[RegisterGroup],
    ) -> RegisterGroup | None:
        try:
            return catalog.references.groups.resolve(reference)
        except (ReferenceError, ValueError):
            return None

    @staticmethod
    def _validate_direct_type(
        group: RegisterGroup,
        bits: int,
        source: Path,
        *,
        require_complete: bool,
    ) -> Iterator[Diagnostic]:
        limit = 1 << bits
        for register in group.registers.values():
            if register.encoding is None:
                if require_complete:
                    yield _error(
                        "register.encoding.missing",
                        register.source,
                        f"register {register.id!r} has no encoding for the "
                        f"selector declared in {source}",
                        "encoding",
                    )
                continue
            if register.encoding >= limit:
                yield _error(
                    "register.encoding.range",
                    register.source,
                    f"register {register.id!r} encoding {register.encoding} does "
                    f"not fit the {bits}-bit selector declared in {source}",
                    "encoding",
                )

    @staticmethod
    def _validate_pair_type(
        group: RegisterGroup, bits: int, source: Path
    ) -> Iterator[Diagnostic]:
        encodings = sorted(
            register.encoding
            for register in group.registers.values()
            if register.encoding is not None
        )
        if len(encodings) != len(group.registers) or encodings != list(
            range(len(group.registers))
        ):
            yield _error(
                "register.pair.layout",
                group.source,
                f"pair-selected group {group.id!r} must use contiguous "
                "zero-based member encodings",
            )
            return
        if len(group.registers) % 2:
            yield _error(
                "register.pair.odd-count",
                group.source,
                f"pair-selected group {group.id!r} has an odd member count",
            )
        if (len(group.registers) + 1) // 2 > 1 << bits:
            yield _error(
                "register.pair.range",
                group.source,
                f"register pairs in {group.id!r} do not fit the {bits}-bit "
                f"selector declared in {source}",
            )


class ControlRegisterValidator:
    """Validate distributed control-register membership and image contracts."""

    def validate(self, catalog: ControlRegisterCatalog) -> Iterator[Diagnostic]:
        for namespace in catalog.namespaces.values():
            inventory = namespace.inventory
            for missing in inventory.missing:
                yield _error(
                    "control-register.missing-directory",
                    inventory.source,
                    f"declared control register {missing!r} has no directory",
                )
            for undeclared in inventory.undeclared:
                yield _error(
                    "control-register.undeclared-directory",
                    inventory.root / undeclared,
                    f"control-register directory {undeclared!r} is not declared",
                )
            for duplicate in inventory.duplicates:
                yield _error(
                    "control-register.duplicate",
                    inventory.source,
                    f"control register {duplicate!r} is listed more than once",
                )
        for register in catalog.references.registers.values():
            yield from self._validate_register(register)

    @staticmethod
    def _validate_register(register: ControlRegister) -> Iterator[Diagnostic]:
        if not register.semantics.is_file():
            yield _error(
                "control-register.semantics.missing",
                register.semantics,
                f"control register {register.id!r} has no required semantics artifact",
            )
        reset = register.reset
        if isinstance(reset, ConstantReset) and reset.value >= 1 << 64:
            yield _error(
                "control-register.reset.range",
                register.source,
                f"reset value does not fit control register {register.id!r}",
                "reset",
            )
        layout = register.layout
        if layout is None:
            return
        for field in layout.fields:
            if field.msb >= 64:
                yield _error(
                    "control-register.layout.field-range",
                    layout.source,
                    f"field {field.id!r} occupies bits {field.msb}..{field.lsb} "
                    "outside a 64-bit control register",
                    "fields",
                )
        for index, left in enumerate(layout.fields):
            for right in layout.fields[index + 1 :]:
                if left.overlaps(right):
                    yield _error(
                        "control-register.layout.field-overlap",
                        layout.source,
                        f"fields {left.id!r} and {right.id!r} overlap",
                        "fields",
                    )


class TerminologyValidator:
    """Validate terminology inventories, references, forms, and relations."""

    def validate(self, catalog: TermCatalog) -> Iterator[Diagnostic]:
        yield from self._validate_inventories(catalog)
        yield from self._validate_references(catalog)
        yield from self._validate_spellings(catalog)
        yield from self._validate_broader_relations(catalog)

    @staticmethod
    def _validate_inventories(catalog: TermCatalog) -> Iterator[Diagnostic]:
        for namespace in catalog.namespaces.values():
            yield from TerminologyValidator._validate_inventory(
                namespace.group_inventory
            )
            for group in namespace.groups.values():
                yield from TerminologyValidator._validate_inventory(
                    group.term_inventory
                )

    @staticmethod
    def _validate_inventory(
        inventory: TerminologyInventory,
    ) -> Iterator[Diagnostic]:
        for missing in inventory.missing:
            yield _error(
                f"terminology.{inventory.kind}.missing-directory",
                inventory.source,
                f"declared terminology {inventory.kind} {missing!r} has no directory",
            )
        for undeclared in inventory.undeclared:
            yield _error(
                f"terminology.{inventory.kind}.undeclared-directory",
                inventory.root / undeclared,
                f"terminology {inventory.kind} directory {undeclared!r} is not in "
                f"{inventory.source.name}",
            )
        for duplicate in inventory.duplicates:
            yield _error(
                f"terminology.{inventory.kind}.duplicate",
                inventory.source,
                f"terminology {inventory.kind} {duplicate!r} is listed more than once",
            )

    @staticmethod
    def _validate_references(catalog: TermCatalog) -> Iterator[Diagnostic]:
        terms = catalog.references.terms
        for term in terms.values():
            for relation_name, references in (
                ("broader", term.relations.broader),
                ("related", term.relations.related),
            ):
                for index, reference in enumerate(references):
                    if reference not in terms:
                        yield _error(
                            "terminology.relation.unknown",
                            term.source,
                            f"{relation_name} relation names an unknown term",
                            "relations",
                            relation_name,
                            index,
                        )
            for part in term.definition.parts:
                if not isinstance(part, TermReferenceText):
                    continue
                if part.reference not in terms:
                    yield _error(
                        "terminology.definition.unknown-term",
                        term.source,
                        "definition names an unknown term",
                        "definition",
                    )
                    continue
                target = terms.resolve(part.reference)
                if not target.forms.supports(part.form, target.abbreviation):
                    yield _error(
                        "terminology.definition.unavailable-form",
                        term.source,
                        f"term {target.id!r} does not define form {part.form.value!r}",
                        "definition",
                    )

    @staticmethod
    def _validate_spellings(catalog: TermCatalog) -> Iterator[Diagnostic]:
        for spellings in catalog.spellings.values():
            references = {item.reference for item in spellings}
            if len(references) < 2:
                continue
            first = catalog.references.terms[spellings[0].reference]
            conflicting = catalog.references.terms[spellings[1].reference]
            yield _error(
                "terminology.spelling.conflict",
                conflicting.source,
                f"spelling {spellings[1].value!r} is also owned by {first.id!r}",
                related=(
                    RelatedLocation(first.source, "conflicting terminology spelling"),
                ),
            )

    @staticmethod
    def _validate_broader_relations(catalog: TermCatalog) -> Iterator[Diagnostic]:
        terms = catalog.references.terms
        complete: set[Reference[Term]] = set()
        active: list[Reference[Term]] = []

        def visit(term: Term) -> Iterator[Diagnostic]:
            if term.reference in complete:
                return
            if term.reference in active:
                start = active.index(term.reference)
                cycle = (*active[start:], term.reference)
                yield _error(
                    "terminology.relation.broader-cycle",
                    term.source,
                    "circular broader relation: "
                    + " -> ".join(terms.resolve(item).id for item in cycle),
                    "relations",
                    "broader",
                )
                return
            active.append(term.reference)
            for reference in term.relations.broader:
                if reference in terms:
                    yield from visit(terms.resolve(reference))
            active.pop()
            complete.add(term.reference)

        for term in terms.values():
            yield from visit(term)


@dataclass(frozen=True, slots=True)
class ValidationScope:
    """One complete or targeted project-validation request."""

    project: IsaProject
    selected: tuple[InstructionBundle, ...]
    complete: bool


class ValidationRule(ABC):
    """Extensible project-level validation rule contract."""

    @abstractmethod
    def validate(self, scope: ValidationScope) -> Iterator[Diagnostic]:
        """Yield diagnostics applicable to this validation scope."""


class BundleValidationRule(ValidationRule):
    def __init__(self, validator: BundleValidator | None = None) -> None:
        self.validator = validator or BundleValidator()

    def validate(self, scope: ValidationScope) -> Iterator[Diagnostic]:
        for bundle in scope.selected:
            yield from self.validator.validate(bundle, scope.project)


class CatalogValidationRule(ValidationRule):
    def __init__(self, validator: CatalogValidator | None = None) -> None:
        self.validator = validator or CatalogValidator()

    def validate(self, scope: ValidationScope) -> Iterator[Diagnostic]:
        yield from self.validator.validate(
            scope.project, scope.selected, complete=scope.complete
        )


class EncodingReservationValidationRule(ValidationRule):
    def __init__(self, validator: EncodingReservationValidator | None = None) -> None:
        self.validator = validator or EncodingReservationValidator()

    def validate(self, scope: ValidationScope) -> Iterator[Diagnostic]:
        if scope.complete:
            yield from self.validator.validate(scope.project.encoding_reservations)


class CpuidValidationRule(ValidationRule):
    def __init__(self, validator: CpuidValidator | None = None) -> None:
        self.validator = validator or CpuidValidator()

    def validate(self, scope: ValidationScope) -> Iterator[Diagnostic]:
        if scope.complete:
            yield from self.validator.validate(scope.project.cpuid)


class EventValidationRule(ValidationRule):
    def __init__(self, validator: EventValidator | None = None) -> None:
        self.validator = validator or EventValidator()

    def validate(self, scope: ValidationScope) -> Iterator[Diagnostic]:
        if scope.complete:
            yield from self.validator.validate(scope.project.events)


class RegisterValidationRule(ValidationRule):
    def __init__(self, validator: RegisterValidator | None = None) -> None:
        self.validator = validator or RegisterValidator()

    def validate(self, scope: ValidationScope) -> Iterator[Diagnostic]:
        if scope.complete and scope.project.registers.references.groups:
            yield from self.validator.validate(
                scope.project.registers,
                scope.project.types,
                scope.project.control_registers,
            )


class ControlRegisterValidationRule(ValidationRule):
    def __init__(self, validator: ControlRegisterValidator | None = None) -> None:
        self.validator = validator or ControlRegisterValidator()

    def validate(self, scope: ValidationScope) -> Iterator[Diagnostic]:
        if scope.complete:
            yield from self.validator.validate(scope.project.control_registers)


class TerminologyValidationRule(ValidationRule):
    def __init__(self, validator: TerminologyValidator | None = None) -> None:
        self.validator = validator or TerminologyValidator()

    def validate(self, scope: ValidationScope) -> Iterator[Diagnostic]:
        if scope.complete:
            yield from self.validator.validate(scope.project.terminology)


class DocumentSourceValidationRule(ValidationRule):
    """Render manual sources in memory so preprocessing failures are diagnostics."""

    def validate(self, scope: ValidationScope) -> Iterator[Diagnostic]:
        if not scope.complete:
            return
        project = scope.project
        artifact_root = project.root.parent / "artifacts"
        if not artifact_root.is_dir() or not (artifact_root / "schema.yaml").is_file():
            return
        from .generation import (
            ArtifactGenerationContext,
            ArtifactGeneratorRegistry,
        )
        from .workspace import SpecWorkspace

        try:
            workspace = SpecWorkspace.load(project.root.parent)
            registry = ArtifactGeneratorRegistry.discover(workspace)
        except (OSError, RuntimeError, ValueError) as error:
            yield _error("document.source", artifact_root, str(error))
            return
        context = ArtifactGenerationContext.create(workspace, project.root / ".check")
        for artifact_id in registry.artifact_ids:
            generator = registry.generator(artifact_id)
            if not any(
                output.suffix == ".tex" for output in generator.definition.output_roots
            ):
                continue
            try:
                registry.generate(artifact_id, workspace, context.output_root)
            except (OSError, RuntimeError, ValueError) as error:
                yield _error("document.source", generator.definition.source, str(error))


class CheckService:
    """Apply an ordered set of validation rules to one project scope."""

    def __init__(self, rules: tuple[ValidationRule, ...] | None = None) -> None:
        self.rules = rules or (
            BundleValidationRule(),
            CatalogValidationRule(),
            EncodingReservationValidationRule(),
            CpuidValidationRule(),
            EventValidationRule(),
            RegisterValidationRule(),
            ControlRegisterValidationRule(),
            TerminologyValidationRule(),
            DocumentSourceValidationRule(),
        )

    def check(
        self,
        project: IsaProject,
        targets: Iterable[str | Path] = (),
    ) -> DiagnosticBag:
        requested = tuple(targets)
        with log_phase(_LOGGER, "check", targets=len(requested)) as phase:
            scope = ValidationScope(project, project.select(requested), not requested)
            diagnostics = DiagnosticBag()
            for rule in self.rules:
                before = len(diagnostics)
                with log_phase(
                    _LOGGER,
                    "check.rule",
                    level=logging.DEBUG,
                    rule=type(rule).__name__,
                ) as rule_phase:
                    diagnostics.extend(rule.validate(scope))
                    rule_phase["diagnostics"] = len(diagnostics) - before
            phase["complete"] = scope.complete
            phase["diagnostics"] = len(diagnostics)
            return diagnostics
