"""Read-only, namespace-aware opcode allocation analysis."""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from pathlib import Path

from .encoding import EncodingForm
from .encoding_architecture import (
    ENCODING_CLASSES,
    EncodingClass,
    encoding_class,
    operator_space,
)
from .encoding_reservation import EncodingReservation, EncodingReservationRegion
from .project import IsaProject, InstructionBundle
from .reference import Reference


IMMEDIATE_EA_VALUES = frozenset(range(0x5B, 0x5F))


class CandidateOutsideNamespaceError(ValueError):
    """An allocation candidate is outside its selected namespace."""

    def __init__(
        self,
        encoding_class: str,
        pattern: str,
        space: str | None,
    ) -> None:
        self.encoding_class = encoding_class
        self.pattern = pattern
        self.space = space
        scope = f"{encoding_class}/{space}" if space else encoding_class
        super().__init__(f"candidate {pattern} is outside {scope} namespace")


@dataclass(frozen=True, slots=True)
class AllocationCube:
    """A set of bit strings represented by fixed-bit mask and value."""

    width: int
    mask: int
    value: int

    @classmethod
    def parse(cls, pattern: str, width: int | None = None) -> "AllocationCube":
        normalized = pattern.replace("x", "?").replace("_", "").replace(" ", "")
        target_width = len(normalized) if width is None else width
        if not normalized or len(normalized) > target_width:
            raise ValueError(
                f"pattern must contain 1..{target_width} bits, got {pattern!r}"
            )
        if set(normalized) - set("01?"):
            raise ValueError(f"pattern may contain only 0, 1, ?, x, or _: {pattern!r}")
        normalized += "?" * (target_width - len(normalized))
        mask = 0
        value = 0
        for character in normalized:
            mask <<= 1
            value <<= 1
            if character in "01":
                mask |= 1
                value |= int(character)
        return cls(target_width, mask, value)

    @classmethod
    def from_encoding(cls, form: EncodingForm) -> "AllocationCube":
        return cls(form.pattern.bit_width, form.pattern.fixed_mask, form.pattern.fixed_value)

    @property
    def slots(self) -> int:
        return 1 << (self.width - self.mask.bit_count())

    @property
    def pattern(self) -> str:
        return "".join(
            str((self.value >> bit) & 1) if self.mask & (1 << bit) else "?"
            for bit in range(self.width - 1, -1, -1)
        )

    @property
    def first(self) -> int:
        return self.value

    @property
    def last(self) -> int:
        return self.value | (((1 << self.width) - 1) ^ self.mask)

    def overlaps(self, other: "AllocationCube") -> bool:
        if self.width != other.width:
            return False
        common = self.mask & other.mask
        return (self.value ^ other.value) & common == 0

    def contains(self, other: "AllocationCube") -> bool:
        return (
            self.width == other.width
            and self.mask & other.mask == self.mask
            and (self.value ^ other.value) & self.mask == 0
        )

    def matches(self, value: int) -> bool:
        return value & self.mask == self.value

    def intersection(self, other: "AllocationCube") -> "AllocationCube | None":
        if not self.overlaps(other):
            return None
        return AllocationCube(self.width, self.mask | other.mask, self.value | other.value)

    def split(self) -> tuple["AllocationCube", "AllocationCube"]:
        wildcard = next(
            (bit for bit in range(self.width - 1, -1, -1) if not self.mask & (1 << bit)),
            None,
        )
        if wildcard is None:
            raise ValueError("cannot split a fixed allocation cube")
        mask = self.mask | (1 << wildcard)
        return (
            AllocationCube(self.width, mask, self.value),
            AllocationCube(self.width, mask, self.value | (1 << wildcard)),
        )


@dataclass(frozen=True, slots=True)
class AllocationEntry:
    """Raw reservation and constraint-filtered assignment for one form."""

    reference: Reference[InstructionBundle]
    owner: str
    mnemonic: str
    form_id: str
    source: Path
    pattern: str
    raw_cubes: tuple[AllocationCube, ...]
    legal_cubes: tuple[AllocationCube, ...]

    @property
    def width(self) -> int:
        return len(self.pattern)

    @property
    def name(self) -> str:
        return f"{self.mnemonic}.{self.form_id}"

    @property
    def raw_slots(self) -> int:
        return sum(cube.slots for cube in self.raw_cubes)

    @property
    def assigned_slots(self) -> int:
        return sum(cube.slots for cube in self.legal_cubes)

    @property
    def reclaimed_slots(self) -> int:
        return self.raw_slots - self.assigned_slots


@dataclass(frozen=True, slots=True)
class AllocationCollision:
    left: AllocationEntry
    right: AllocationEntry


@dataclass(frozen=True, slots=True)
class AllocationSummary:
    encoding_class: str
    width: int
    forms: int
    namespace_slots: int
    allocated_slots: int
    reclaimed_slots: int
    reserved_slots: int
    clean_free_slots: int
    remaining_slots: int


@dataclass(frozen=True, slots=True)
class AllocationHole:
    cube: AllocationCube

    @property
    def pattern(self) -> str:
        return self.cube.pattern

    @property
    def slots(self) -> int:
        return self.cube.slots


@dataclass(frozen=True, slots=True)
class CandidateCheck:
    encoding_class: str
    pattern: str
    slots: int
    allocated_slots: int
    reclaimed_slots: int
    reserved_slots: int
    clean_free_slots: int
    allocated_entries: tuple[AllocationEntry, ...]
    reclaimed_entries: tuple[AllocationEntry, ...]
    reservations: tuple[EncodingReservation, ...]

    @property
    def state(self) -> str:
        states = []
        if self.allocated_slots:
            states.append("allocated")
        if self.reclaimed_slots:
            states.append("reclaimed")
        if self.reserved_slots:
            states.append("reserved")
        if self.clean_free_slots:
            states.append("clean-free")
        return "+".join(states)


@dataclass(frozen=True, slots=True)
class AllocationMap:
    entries: tuple[AllocationEntry, ...]
    collisions: tuple[AllocationCollision, ...]


class AllocationAnalyzer:
    """Project allocation analysis built from canonical encoding forms."""

    def analyze(
        self,
        project: IsaProject,
        targets: tuple[str | Path, ...] = (),
    ) -> AllocationMap:
        all_entries = self.entries(project)
        selected_references = {bundle.reference for bundle in project.select(targets)}
        entries = tuple(
            entry for entry in all_entries if entry.reference in selected_references
        )
        collisions = tuple(
            AllocationCollision(left, right)
            for index, left in enumerate(all_entries)
            for right in all_entries[index + 1 :]
            if (
                left.reference in selected_references
                or right.reference in selected_references
            )
            and entries_overlap(left, right)
        )
        return AllocationMap(entries, collisions)

    def entries(
        self,
        project: IsaProject,
        class_name: str | None = None,
        *,
        space: str | None = None,
        leading: str | None = None,
        grep: str | None = None,
    ) -> tuple[AllocationEntry, ...]:
        entries = tuple(
            self._entry(bundle, form)
            for bundle in project.select()
            for form in bundle.encodings.forms
        )
        if class_name is None:
            return entries
        owner = encoding_class(class_name)
        regions = search_regions(owner, space=space, leading=leading)
        needle = grep.lower() if grep else None
        return tuple(
            entry
            for entry in entries
            if entry.width == owner.allocation_bits
            and any(raw.overlaps(region) for raw in entry.raw_cubes for region in regions)
            and (needle is None or needle in entry.name.lower())
        )

    def summaries(self, project: IsaProject) -> tuple[AllocationSummary, ...]:
        entries = self.entries(project)
        result = []
        for owner in ENCODING_CLASSES:
            regions = _namespace_cubes(owner)
            selected = tuple(
                entry for entry in entries if entry.width == owner.allocation_bits
            )
            raw = tuple(cube for entry in selected for cube in entry.raw_cubes)
            legal = tuple(cube for entry in selected for cube in entry.legal_cubes)
            reserved = reservation_cubes(project, owner.name)
            namespace_slots = sum(region.slots for region in regions)
            raw_slots = covered_slots(regions, raw)
            allocated_slots = covered_slots(regions, legal)
            unavailable_slots = covered_slots(regions, (*raw, *reserved))
            result.append(
                AllocationSummary(
                    owner.name,
                    owner.allocation_bits,
                    len(selected),
                    namespace_slots,
                    allocated_slots,
                    raw_slots - allocated_slots,
                    unavailable_slots - raw_slots,
                    namespace_slots - unavailable_slots,
                    raw_slots
                    - allocated_slots
                    + namespace_slots
                    - unavailable_slots,
                )
            )
        return tuple(result)

    def holes(
        self,
        project: IsaProject,
        class_name: str,
        *,
        space: str | None = None,
        leading: str | None = None,
        include_reclaimed: bool = False,
        min_slots: int = 1,
        max_slots: int | None = None,
        limit: int = 32,
        sort: str = "address",
    ) -> tuple[AllocationHole, ...]:
        if min_slots <= 0 or (max_slots is not None and max_slots <= 0):
            raise ValueError("hole slot limits must be positive")
        if max_slots is not None and min_slots > max_slots:
            raise ValueError("--min-slots cannot exceed --max-slots")
        if limit <= 0:
            raise ValueError("--limit must be positive")
        owner = encoding_class(class_name)
        regions = search_regions(owner, space=space, leading=leading)
        entries = self.entries(project, owner.name, space=space, leading=leading)
        unavailable = unavailable_cubes(
            entries,
            include_reclaimed=include_reclaimed,
            reservations=reservation_cubes(project, owner.name),
        )
        cubes = [cube for region in regions for cube in _uncovered(region, unavailable)]
        if max_slots is not None:
            cubes = [piece for cube in cubes for piece in _cap_cube(cube, max_slots)]
        cubes = [cube for cube in cubes if cube.slots >= min_slots]
        if sort == "size":
            cubes.sort(key=lambda cube: (-cube.slots, cube.first))
        elif sort == "address":
            cubes.sort(key=lambda cube: cube.first)
        else:
            raise ValueError("hole sort must be 'address' or 'size'")
        return tuple(AllocationHole(cube) for cube in cubes[:limit])

    def check_candidate(
        self,
        project: IsaProject,
        class_name: str,
        pattern: str,
        *,
        space: str | None = None,
    ) -> CandidateCheck:
        owner = encoding_class(class_name)
        candidate = AllocationCube.parse(pattern, owner.allocation_bits)
        regions = search_regions(owner, space=space)
        if covered_slots((candidate,), regions) != candidate.slots:
            raise CandidateOutsideNamespaceError(
                owner.name,
                candidate.pattern,
                space,
            )
        entries = self.entries(project, owner.name, space=space)
        legal = tuple(cube for entry in entries for cube in entry.legal_cubes)
        raw = tuple(cube for entry in entries for cube in entry.raw_cubes)
        reservation_entries = tuple(
            reservation
            for reservation in project.encoding_reservations.reservations.values()
            if any(
                region.encoding_class == owner.name
                and candidate.overlaps(reservation_cube(region))
                for region in reservation.regions
            )
        )
        reserved = tuple(
            reservation_cube(region)
            for reservation in reservation_entries
            for region in reservation.regions
            if region.encoding_class == owner.name
            and candidate.overlaps(reservation_cube(region))
        )
        allocated_slots = covered_slots((candidate,), legal)
        raw_slots = covered_slots((candidate,), raw)
        unavailable_slots = covered_slots((candidate,), (*raw, *reserved))
        allocated_entries = tuple(
            entry
            for entry in entries
            if any(candidate.overlaps(cube) for cube in entry.legal_cubes)
        )
        reclaimed_entries = tuple(
            entry
            for entry in entries
            if covered_slots((candidate,), entry.raw_cubes)
            > covered_slots((candidate,), entry.legal_cubes)
        )
        return CandidateCheck(
            owner.name,
            candidate.pattern,
            candidate.slots,
            allocated_slots,
            raw_slots - allocated_slots,
            unavailable_slots - raw_slots,
            candidate.slots - unavailable_slots,
            allocated_entries,
            reclaimed_entries,
            reservation_entries,
        )

    @staticmethod
    def _entry(bundle: InstructionBundle, form: EncodingForm) -> AllocationEntry:
        return AllocationEntry(
            bundle.reference,
            bundle.owner,
            bundle.instruction.mnemonic,
            form.id,
            bundle.encodings.source,
            form.pattern.code,
            (AllocationCube.from_encoding(form),),
            form_cubes(form),
        )


def unavailable_cubes(
    entries: tuple[AllocationEntry, ...],
    *,
    include_reclaimed: bool,
    reservations: tuple[AllocationCube, ...] = (),
) -> tuple[AllocationCube, ...]:
    """Return the occupied cubes under the requested allocation policy."""

    assigned = tuple(
        cube
        for entry in entries
        for cube in (entry.legal_cubes if include_reclaimed else entry.raw_cubes)
    )
    return (*assigned, *reservations)


def reservation_cube(region: EncodingReservationRegion) -> AllocationCube:
    """Lower one authored reservation prefix into its encoding-class cube."""

    owner = encoding_class(region.encoding_class)
    return AllocationCube.parse(region.prefix, owner.allocation_bits)


def reservation_cubes(
    project: IsaProject, class_name: str
) -> tuple[AllocationCube, ...]:
    """Return authored reservation cubes in one encoding class."""

    return tuple(
        reservation_cube(region)
        for reservation in project.encoding_reservations.reservations.values()
        for region in reservation.regions
        if region.encoding_class == class_name
    )


def numeric_bounds(value: int | str) -> tuple[int, int] | None:
    if isinstance(value, int) and not isinstance(value, bool):
        return value, value
    if isinstance(value, str) and ".." in value:
        lower, upper = value.split("..", 1)
        return int(lower, 0), int(upper, 0)
    return None


def _constraint_values(values: tuple[int | str, ...], width: int) -> set[int]:
    result: set[int] = set()
    for item in values:
        bounds = numeric_bounds(item)
        if bounds is not None:
            lower, upper = bounds
            result.update(range(lower, upper + 1))
        elif item == "immediate":
            result.update(IMMEDIATE_EA_VALUES)
        else:
            raise ValueError(f"unknown symbolic constraint {item!r}")
    return {value for value in result if 0 <= value < 1 << width}


def form_cubes(form: EncodingForm) -> tuple[AllocationCube, ...]:
    """Lower a form and all constraints into disjoint legal cubes."""

    constrained: list[tuple[str, tuple[int, ...]]] = []
    for constraint in form.constraints:
        field = form.field_for_role(constraint.role)
        if field is None:
            continue
        width = form.pattern.field_width(field.marker)
        domain = set(range(1 << width))
        if constraint.allow:
            domain &= _constraint_values(constraint.allow, width)
        if constraint.exclude:
            domain -= _constraint_values(constraint.exclude, width)
        constrained.append((field.marker, tuple(sorted(domain))))

    assignments = product(*(values for _, values in constrained)) if constrained else [()]
    cubes = []
    for values in assignments:
        mask = form.pattern.fixed_mask
        value = form.pattern.fixed_value
        selected = dict(zip((marker for marker, _ in constrained), values))
        seen = {marker: 0 for marker in selected}
        widths = {marker: form.pattern.field_width(marker) for marker in selected}
        for index, marker in enumerate(form.pattern.code):
            if marker not in selected:
                continue
            position = form.pattern.bit_width - index - 1
            bit_index = widths[marker] - seen[marker] - 1
            seen[marker] += 1
            mask |= 1 << position
            if selected[marker] >> bit_index & 1:
                value |= 1 << position
            else:
                value &= ~(1 << position)
        cubes.append(AllocationCube(form.pattern.bit_width, mask, value))
    return _compress_cubes(tuple(cubes))


def forms_overlap(left: EncodingForm, right: EncodingForm) -> bool:
    return any(a.overlaps(b) for a in form_cubes(left) for b in form_cubes(right))


def entries_overlap(left: AllocationEntry, right: AllocationEntry) -> bool:
    return any(a.overlaps(b) for a in left.legal_cubes for b in right.legal_cubes)


def _compress_cubes(cubes: tuple[AllocationCube, ...]) -> tuple[AllocationCube, ...]:
    """Merge complete sibling pairs without enumerating the represented slots."""

    current = set(cubes)
    while True:
        consumed: set[AllocationCube] = set()
        merged: set[AllocationCube] = set()
        for cube in sorted(current, key=lambda item: (item.mask, item.value)):
            if cube in consumed:
                continue
            for bit in range(cube.width):
                flag = 1 << bit
                if not cube.mask & flag:
                    continue
                sibling = AllocationCube(cube.width, cube.mask, cube.value ^ flag)
                if sibling in current and sibling not in consumed:
                    consumed.update((cube, sibling))
                    merged.add(
                        AllocationCube(
                            cube.width,
                            cube.mask ^ flag,
                            cube.value & ~flag,
                        )
                    )
                    break
        if not merged:
            break
        current = (current - consumed) | merged
    return tuple(sorted(current, key=lambda item: (item.value, item.mask)))


def search_regions(
    owner: EncodingClass,
    *,
    space: str | None = None,
    leading: str | None = None,
) -> tuple[AllocationCube, ...]:
    regions = _namespace_cubes(owner)
    filters = []
    if space is not None:
        filters.append(
            AllocationCube.parse(operator_space(owner.name, space).prefix, owner.allocation_bits)
        )
    if leading is not None:
        filters.append(AllocationCube.parse(leading, owner.allocation_bits))
    for selected_filter in filters:
        regions = tuple(
            intersection
            for region in regions
            if (intersection := region.intersection(selected_filter)) is not None
        )
    if not regions:
        raise ValueError("selected prefix does not intersect the encoding namespace")
    return regions


def _namespace_cubes(owner: EncodingClass) -> tuple[AllocationCube, ...]:
    return tuple(AllocationCube.parse(pattern) for pattern in owner.namespace)


def covered_slots(
    regions: tuple[AllocationCube, ...], cubes: tuple[AllocationCube, ...]
) -> int:
    """Count the union of ``cubes`` clipped to disjoint search regions."""

    return sum(_covered(region, cubes) for region in regions)


def _covered(region: AllocationCube, cubes: tuple[AllocationCube, ...]) -> int:
    relevant = tuple(cube for cube in cubes if cube.overlaps(region))
    if not relevant:
        return 0
    if any(cube.contains(region) for cube in relevant):
        return region.slots
    if region.slots == 1:
        return 1
    left, right = region.split()
    return _covered(left, relevant) + _covered(right, relevant)


def _uncovered(
    region: AllocationCube, unavailable: tuple[AllocationCube, ...]
) -> tuple[AllocationCube, ...]:
    relevant = tuple(cube for cube in unavailable if cube.overlaps(region))
    if not relevant:
        return (region,)
    if any(cube.contains(region) for cube in relevant):
        return ()
    if region.slots == 1:
        return ()
    left, right = region.split()
    return (*_uncovered(left, relevant), *_uncovered(right, relevant))


def _cap_cube(cube: AllocationCube, max_slots: int) -> tuple[AllocationCube, ...]:
    if cube.slots <= max_slots:
        return (cube,)
    left, right = cube.split()
    return (*_cap_cube(left, max_slots), *_cap_cube(right, max_slots))
