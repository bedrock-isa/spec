#!/usr/bin/env python3
"""Build the Bedrock reference-site registry from owning document structures."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import PurePosixPath
from typing import Iterable

import gen_docs
from site_backend import NavigationGroup, PageRegistry, PageSpec, stable_anchor
from site_latex import InstructionSpec, LabelSpec, LatexStructure, SectionSpec


ROOT_PAGE_KEY = "site:home"
ISA_DOCUMENT_ID = "isa"
INSTRUCTION_PART_ID = "instruction-set-reference"
INSTRUCTION_PAGE_PREFIX = "instruction-group-"


@dataclass(frozen=True)
class DocumentSiteSpec:
    """Public identity and parsed structure for one reference document."""

    id: str
    navigation_title: str
    download: PurePosixPath
    structure: LatexStructure


@dataclass(frozen=True)
class SiteModel:
    """Validated page registry and its top-level navigation groups."""

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
    structure: LatexStructure,
    start: int,
    end: int,
) -> tuple[LabelSpec, ...]:
    return tuple(label for label in structure.labels if start <= label.start < end)


def _register_source_targets(
    registry: PageRegistry,
    document: str,
    page: str,
    labels: Iterable[LabelSpec],
    owner: str,
    *,
    owner_is_label: bool = True,
) -> None:
    owned_labels = tuple(labels)
    names = [label.name for label in owned_labels]
    expected_count = 1 if owner_is_label else 0
    if names.count(owner) != expected_count:
        raise ValueError(
            f"{page}: expected owning label {owner!r} count {expected_count}, "
            f"found {names.count(owner)}"
        )
    if not owner_is_label:
        registry.add_target(scoped_target(document, owner), page)
    for label in owned_labels:
        registry.add_target(
            scoped_target(document, label.name),
            page,
            anchor=None if label.name == owner else stable_anchor(label.name),
        )


def _add_document_landing(registry: PageRegistry, document: DocumentSiteSpec) -> str:
    key = document_page_key(document.id)
    registry.add_page(
        PageSpec(
            key=key,
            title=document.structure.title.title,
            output=PurePosixPath(document.id) / "index.md",
            group=document.id,
            source=document.id,
        ),
        targets=(key,),
    )
    return key


def _add_flat_document_sections(
    registry: PageRegistry,
    document: DocumentSiteSpec,
    landing: str,
) -> None:
    if document.structure.parts:
        raise ValueError(f"{document.id}: only the ISA document may contain parts")
    for section in document.structure.sections:
        page_key = section_page_key(document.id, section.key)
        registry.add_page(
            PageSpec(
                key=page_key,
                title=section.title,
                output=PurePosixPath(document.id) / f"{section.key}.md",
                group=document.id,
                parent=landing,
                source=document.id,
            )
        )
        _register_source_targets(
            registry,
            document.id,
            page_key,
            _labels_in_range(document.structure, section.start, section.end),
            f"page:{section.key}",
        )


def _instruction_group_id(set_name: str) -> str:
    label = gen_docs.instruction_set_page_label(set_name)
    return label.removeprefix("page:").removeprefix(INSTRUCTION_PAGE_PREFIX)


def _instruction_slug(mnemonic: str) -> str:
    return gen_docs.instruction_label(mnemonic).removeprefix("instr:")


def _add_instruction_pages(
    registry: PageRegistry,
    model: gen_docs.IsaModel,
    document: DocumentSiteSpec,
    landing: str,
    sections: dict[str, SectionSpec],
) -> set[str]:
    consumed: set[str] = set()
    instruction_root = f"{document.id}:instructions"
    registry.add_page(
        PageSpec(
            key=instruction_root,
            title="Instructions",
            output=PurePosixPath(document.id) / "instructions" / "index.md",
            group=document.id,
            parent=landing,
            source=document.id,
        ),
        targets=(scoped_target(document.id, "page:instructions"),),
    )

    reading_key = "reading-an-instruction-description"
    reading = sections[reading_key]
    reading_page = section_page_key(document.id, reading.key)
    registry.add_page(
        PageSpec(
            key=reading_page,
            title=reading.title,
            output=PurePosixPath(document.id) / "instructions" / f"{reading.key}.md",
            group=document.id,
            parent=instruction_root,
            source=document.id,
        )
    )
    _register_source_targets(
        registry,
        document.id,
        reading_page,
        _labels_in_range(document.structure, reading.start, reading.end),
        f"page:{reading.key}",
    )
    consumed.add(reading.key)

    for set_name, title, _introduction, instructions in gen_docs.instruction_set_groups(
        model, model.instructions
    ):
        group_id = _instruction_group_id(set_name)
        section_id = INSTRUCTION_PAGE_PREFIX + group_id
        section = sections[section_id]
        instruction_list = tuple(instructions)
        instruction_positions = {
            instruction.label: instruction for instruction in document.structure.instructions
        }
        instruction_labels: list[InstructionSpec] = []
        for instruction in instruction_list:
            label_name = gen_docs.instruction_label(instruction.mnemonic)
            label = instruction_positions.get(label_name)
            if label is None or not section.start <= label.start < section.end:
                raise ValueError(
                    f"{document.id}: instruction {instruction.mnemonic} label is not "
                    f"owned by section {section.key}"
                )
            instruction_labels.append(label)
        if any(
            current.start >= following.start
            for current, following in zip(instruction_labels, instruction_labels[1:])
        ):
            raise ValueError(f"{document.id}: instruction order differs from section {section.key}")

        group_page = section_page_key(document.id, section.key)
        registry.add_page(
            PageSpec(
                key=group_page,
                title=title,
                output=PurePosixPath(document.id) / "instructions" / f"{group_id}.md",
                group=document.id,
                parent=instruction_root,
                source=document.id,
            )
        )
        first_instruction = instruction_labels[0].start if instruction_labels else section.end
        _register_source_targets(
            registry,
            document.id,
            group_page,
            _labels_in_range(document.structure, section.start, first_instruction),
            f"page:{section.key}",
        )
        consumed.add(section.key)
        for index, instruction in enumerate(instruction_list):
            slug = _instruction_slug(instruction.mnemonic)
            page_key = f"{document.id}:instruction:{slug}"
            registry.add_page(
                PageSpec(
                    key=page_key,
                    title=instruction.mnemonic,
                    output=PurePosixPath(document.id) / "instructions" / f"{slug}.md",
                    group=document.id,
                    parent=instruction_root,
                    source=str(instruction.path),
                )
            )
            end = (
                instruction_labels[index + 1].start
                if index + 1 < len(instruction_labels)
                else section.end
            )
            owner = gen_docs.instruction_label(instruction.mnemonic)
            _register_source_targets(
                registry,
                document.id,
                page_key,
                _labels_in_range(
                    document.structure,
                    instruction_labels[index].start,
                    end,
                ),
                owner,
                owner_is_label=False,
            )
    return consumed


def _add_isa_pages(
    registry: PageRegistry,
    model: gen_docs.IsaModel,
    document: DocumentSiteSpec,
    landing: str,
) -> None:
    if not document.structure.parts:
        raise ValueError("isa: expected part-owned navigation groups")
    sections = {section.key: section for section in document.structure.sections}
    consumed: set[str] = set()
    instruction_sections: set[str] = set()

    for part in document.structure.parts:
        registry.add_page(
            PageSpec(
                key=part_page_key(document.id, part.key),
                title=part.title,
                output=PurePosixPath(document.id) / f"{part.key}.md",
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
                    raise ValueError(
                        "isa: instruction-description page must belong to the "
                        f"{INSTRUCTION_PART_ID!r} part"
                    )
                instruction_sections = _add_instruction_pages(
                    registry, model, document, landing, sections
                )
                consumed.update(instruction_sections)
                continue
            if section.key in instruction_sections:
                continue
            page_key = section_page_key(document.id, section.key)
            registry.add_page(
                PageSpec(
                    key=page_key,
                    title=section.title,
                    output=PurePosixPath(document.id) / f"{section.key}.md",
                    group=document.id,
                    parent=landing,
                    source=document.id,
                )
            )
            _register_source_targets(
                registry,
                document.id,
                page_key,
                _labels_in_range(document.structure, section.start, section.end),
                f"page:{section.key}",
            )
            consumed.add(section.key)

    expected = set(sections)
    if consumed != expected:
        missing = sorted(expected - consumed)
        extra = sorted(consumed - expected)
        raise ValueError(f"isa: section ownership mismatch; missing={missing}, extra={extra}")


def build_site(
    documents: Iterable[DocumentSiteSpec],
    model: gen_docs.IsaModel,
) -> SiteModel:
    """Build and validate every page and link target in publication order."""
    ordered = tuple(documents)
    ids = [document.id for document in ordered]
    expected = [
        "isa",
        "elf-abi",
        "c-abi",
        "c-far-extensions",
        "target-intrinsics",
    ]
    if ids != expected:
        raise ValueError(f"site document order must be {expected}, got {ids}")

    registry = PageRegistry()
    registry.add_page(
        PageSpec(
            key=ROOT_PAGE_KEY,
            title="Bedrock Architecture",
            output=PurePosixPath("index.md"),
            source="site",
        ),
        targets=(ROOT_PAGE_KEY,),
    )

    groups: list[NavigationGroup] = []
    for document in ordered:
        groups.append(NavigationGroup(document.id, document.navigation_title))
        landing = _add_document_landing(registry, document)
        if document.id == ISA_DOCUMENT_ID:
            _add_isa_pages(registry, model, document, landing)
        else:
            _add_flat_document_sections(registry, document, landing)
    return SiteModel(registry, tuple(groups))
