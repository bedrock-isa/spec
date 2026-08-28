"""Current-model page ownership and semantic-link registry for the web site."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import PurePosixPath
import re

from ..composition import DocumentComposition, InstructionSetBlock
from ..entity import instruction_label
from .navigation import NavigationGroup, PageRegistry, PageSpec, stable_anchor
from .structure import LabelSpec, LatexStructure, SectionSpec


ROOT_PAGE_KEY = "site:home"
ISA_DOCUMENT_ID = "isa"
INSTRUCTION_PART_ID = "instruction-set-reference"


@dataclass(frozen=True, slots=True)
class DocumentSiteSpec:
    id: str
    navigation_title: str
    download: PurePosixPath
    structure: LatexStructure


@dataclass(frozen=True, slots=True)
class SiteModel:
    registry: PageRegistry
    groups: tuple[NavigationGroup, ...]

    def navigation(self) -> list[dict[str, object]]:
        return self.registry.navigation(ROOT_PAGE_KEY, self.groups)


def scoped_target(document: str, label: str) -> str:
    return f"{document}:{label}"


def document_page_key(document: str) -> str:
    return f"document:{document}"


def section_page_key(document: str, section: str) -> str:
    return f"{document}:section:{section}"


def part_page_key(document: str, part: str) -> str:
    return f"{document}:part:{part}"


def _labels_in_range(
    structure: LatexStructure, start: int, end: int
) -> tuple[LabelSpec, ...]:
    return tuple(label for label in structure.labels if start <= label.start < end)


def _register_targets(
    registry: PageRegistry,
    document: str,
    page: str,
    labels: tuple[LabelSpec, ...],
    owner: str,
    *,
    owner_is_label: bool = True,
) -> None:
    names = [label.name for label in labels]
    expected = 1 if owner_is_label else 0
    if names.count(owner) != expected:
        raise ValueError(
            f"{page}: expected owning label {owner!r} count {expected}, "
            f"found {names.count(owner)}"
        )
    if not owner_is_label:
        registry.add_target(scoped_target(document, owner), page)
    for label in labels:
        registry.add_target(
            scoped_target(document, label.name),
            page,
            anchor=None if label.name == owner else stable_anchor(label.name),
        )


def _landing(registry: PageRegistry, document: DocumentSiteSpec) -> str:
    key = document_page_key(document.id)
    registry.add_page(
        PageSpec(
            key,
            document.structure.title.title,
            PurePosixPath(document.id) / "index.md",
            group=document.id,
            source=document.id,
        ),
        targets=(key,),
    )
    return key


def _flat_sections(
    registry: PageRegistry, document: DocumentSiteSpec, landing: str
) -> None:
    if document.structure.parts:
        raise ValueError(f"{document.id}: only the ISA document may contain parts")
    for section in document.structure.sections:
        page = section_page_key(document.id, section.key)
        registry.add_page(
            PageSpec(
                page,
                section.title,
                PurePosixPath(document.id) / f"{section.key}.md",
                group=document.id,
                parent=landing,
                source=document.id,
            )
        )
        _register_targets(
            registry,
            document.id,
            page,
            _labels_in_range(document.structure, section.start, section.end),
            f"page:{section.key}",
        )


def _slug(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    if not slug:
        raise ValueError(f"cannot derive site slug from {value!r}")
    return slug


def _instruction_pages(
    registry: PageRegistry,
    composition: DocumentComposition,
    document: DocumentSiteSpec,
    part_page: str,
    sections: dict[str, SectionSpec],
) -> set[str]:
    consumed: set[str] = set()
    root = f"{document.id}:instructions"
    registry.add_page(
        PageSpec(
            root,
            "Instructions",
            PurePosixPath(document.id) / "instructions/index.md",
            group=document.id,
            parent=part_page,
            source=document.id,
        ),
        targets=(scoped_target(document.id, "page:instructions"),),
    )

    reading_key = "reading-an-instruction-description"
    reading = sections[reading_key]
    reading_page = section_page_key(document.id, reading.key)
    registry.add_page(
        PageSpec(
            reading_page,
            reading.title,
            PurePosixPath(document.id) / "instructions" / f"{reading.key}.md",
            group=document.id,
            parent=root,
            source=document.id,
        )
    )
    _register_targets(
        registry,
        document.id,
        reading_page,
        _labels_in_range(document.structure, reading.start, reading.end),
        f"page:{reading.key}",
    )
    consumed.add(reading.key)

    positions = {item.label: item for item in document.structure.instructions}
    groups = tuple(
        block
        for block in composition.blocks
        if isinstance(block, InstructionSetBlock)
    )
    for group in groups:
        group_id = _slug(group.owner)
        section = sections[f"instruction-group-{group_id}"]
        ordered = []
        for bundle in group.instructions:
            label = instruction_label(bundle.instruction.mnemonic)
            position = positions.get(label)
            if position is None or not section.start <= position.start < section.end:
                raise ValueError(
                    f"{document.id}: instruction {bundle.instruction.mnemonic} "
                    f"is not owned by section {section.key}"
                )
            ordered.append(position)
        if any(a.start >= b.start for a, b in zip(ordered, ordered[1:])):
            raise ValueError(f"{document.id}: instruction order differs in {section.key}")

        group_page = section_page_key(document.id, section.key)
        registry.add_page(
            PageSpec(
                group_page,
                group.title,
                PurePosixPath(document.id)
                / "instructions"
                / group_id
                / "index.md",
                group=document.id,
                parent=root,
                source=document.id,
            )
        )
        first = ordered[0].start if ordered else section.end
        _register_targets(
            registry,
            document.id,
            group_page,
            _labels_in_range(document.structure, section.start, first),
            f"page:{section.key}",
        )
        consumed.add(section.key)
        for index, bundle in enumerate(group.instructions):
            mnemonic = bundle.instruction.mnemonic
            slug = instruction_label(mnemonic).removeprefix("instr:")
            page = f"{document.id}:instruction:{slug}"
            registry.add_page(
                PageSpec(
                    page,
                    mnemonic,
                    PurePosixPath(document.id) / "instructions" / f"{slug}.md",
                    group=document.id,
                    parent=group_page,
                    source=str(bundle.instruction.source),
                )
            )
            end = ordered[index + 1].start if index + 1 < len(ordered) else section.end
            _register_targets(
                registry,
                document.id,
                page,
                _labels_in_range(document.structure, ordered[index].start, end),
                instruction_label(mnemonic),
                owner_is_label=False,
            )
    return consumed


def _isa_pages(
    registry: PageRegistry,
    composition: DocumentComposition,
    document: DocumentSiteSpec,
    landing: str,
) -> None:
    if not document.structure.parts:
        raise ValueError("isa: expected part-owned navigation groups")
    sections = {section.key: section for section in document.structure.sections}
    consumed: set[str] = set()
    instruction_sections: set[str] = set()
    for part in document.structure.parts:
        part_page = part_page_key(document.id, part.key)
        registry.add_page(
            PageSpec(
                part_page,
                part.title,
                PurePosixPath(document.id) / part.key / "index.md",
                group=document.id,
                parent=landing,
                source=document.id,
            ),
            targets=(scoped_target(document.id, f"part:{part.key}"),),
        )
        for section in document.structure.sections:
            if section.part != part.key:
                continue
            if section.key == "reading-an-instruction-description":
                if part.key != INSTRUCTION_PART_ID:
                    raise ValueError("instruction reference belongs to the wrong part")
                instruction_sections = _instruction_pages(
                    registry,
                    composition,
                    document,
                    part_page,
                    sections,
                )
                consumed.update(instruction_sections)
                continue
            if section.key in instruction_sections:
                continue
            page = section_page_key(document.id, section.key)
            registry.add_page(
                PageSpec(
                    page,
                    section.title,
                    PurePosixPath(document.id) / f"{section.key}.md",
                    group=document.id,
                    parent=part_page,
                    source=document.id,
                )
            )
            _register_targets(
                registry,
                document.id,
                page,
                _labels_in_range(document.structure, section.start, section.end),
                f"page:{section.key}",
            )
            consumed.add(section.key)
    expected = set(sections)
    if consumed != expected:
        raise ValueError(
            f"isa: section ownership mismatch; "
            f"missing={sorted(expected - consumed)}, extra={sorted(consumed - expected)}"
        )


def build_site(
    documents: tuple[DocumentSiteSpec, ...],
    composition: DocumentComposition,
) -> SiteModel:
    expected = ("isa", "elf-abi", "c-abi", "target-intrinsics")
    if tuple(item.id for item in documents) != expected:
        raise ValueError(f"site document order must be {expected}")
    registry = PageRegistry()
    registry.add_page(
        PageSpec(ROOT_PAGE_KEY, "Bedrock Architecture", PurePosixPath("index.md"), source="site"),
        targets=(ROOT_PAGE_KEY,),
    )
    groups = []
    for document in documents:
        groups.append(NavigationGroup(document.id, document.navigation_title))
        landing = _landing(registry, document)
        if document.id == ISA_DOCUMENT_ID:
            _isa_pages(registry, composition, document, landing)
        else:
            _flat_sections(registry, document, landing)
    return SiteModel(registry, tuple(groups))
