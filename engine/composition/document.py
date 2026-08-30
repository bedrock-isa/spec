"""Validated composition of one reader-facing TeX document."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from ..model import DocumentTopic
from ..project import InstructionBundle, IsaProject
from ..reference import Reference
from ..terminology import TermGroup
from ..yaml_document import YamlDocumentLoader


@dataclass(frozen=True, slots=True)
class TopicBlock:
    """One owner-local authored topic placed in a global document."""

    topic: DocumentTopic


@dataclass(frozen=True, slots=True)
class InstructionSetBlock:
    """One generated instruction group placed in a global document."""

    owner: str
    title: str
    introduction: tuple[DocumentTopic, ...]
    instructions: tuple[InstructionBundle, ...]


@dataclass(frozen=True, slots=True)
class TermGroupBlock:
    """One terminology group placed in a reader-facing document."""

    group: TermGroup


DocumentBlock = TopicBlock | InstructionSetBlock | TermGroupBlock


@dataclass(frozen=True, slots=True)
class DocumentComposition:
    """A complete document frame and its explicit reader order."""

    artifact: str
    source: Path
    preamble: Path
    title_page: Path
    blocks: tuple[DocumentBlock, ...]
    postamble: Path

    @classmethod
    def load(
        cls, path: str | Path, project: IsaProject
    ) -> "DocumentComposition":
        source = Path(path).resolve()
        document = YamlDocumentLoader().mapping(source)
        artifact = document.get("id")
        if not isinstance(artifact, str) or not artifact:
            raise ValueError(f"{source}: artifact must be a non-empty string")

        root = project.root.parent

        def fragment(key: str) -> Path:
            raw = document.get(key)
            if not isinstance(raw, str):
                raise ValueError(f"{source}: {key} must be a TeX path")
            resolved = (root / raw).resolve()
            if not resolved.is_relative_to(root) or resolved.suffix != ".tex":
                raise ValueError(f"{source}: {key} escapes the specification root")
            if not resolved.is_file():
                raise ValueError(f"{source}: missing {key} {resolved}")
            return resolved

        raw_blocks = document.get("body")
        if not isinstance(raw_blocks, list) or not raw_blocks:
            raise ValueError(f"{source}: body must be a non-empty list")
        blocks: list[DocumentBlock] = []
        included_topics: list[Reference[DocumentTopic]] = []
        included_groups: list[Reference[TermGroup]] = []
        included_owners: list[str] = []
        for index, raw in enumerate(raw_blocks):
            if not isinstance(raw, dict) or len(raw) != 1:
                raise ValueError(f"{source}: body[{index}] must have one block kind")
            if "topic" in raw:
                raw_reference = raw["topic"]
                if not isinstance(raw_reference, str):
                    raise ValueError(f"{source}: body[{index}].topic must be a reference")
                topic_reference: Reference[DocumentTopic] = Reference.parse(
                    raw_reference
                )
                topic = project.model.document_topics.get(topic_reference)
                if topic is None:
                    raise ValueError(f"{source}: unknown topic")
                if topic.artifact != artifact:
                    raise ValueError(
                        f"{source}: topic {topic.id!r} belongs to {topic.artifact}"
                    )
                included_topics.append(topic_reference)
                blocks.append(TopicBlock(topic))
                continue
            if "term-group" in raw:
                raw_reference = raw["term-group"]
                if not isinstance(raw_reference, str):
                    raise ValueError(
                        f"{source}: body[{index}].term-group must be a reference"
                    )
                try:
                    group_reference: Reference[TermGroup] = Reference.parse(
                        raw_reference
                    )
                    group = project.terminology.references.groups.resolve(
                        group_reference
                    )
                except ValueError as error:
                    raise ValueError(f"{source}: unknown terminology group") from error
                included_groups.append(group.reference)
                blocks.append(TermGroupBlock(group))
                continue
            if "instruction-set" in raw:
                item = raw["instruction-set"]
                if not isinstance(item, dict):
                    raise ValueError(
                        f"{source}: body[{index}].instruction-set must be a mapping"
                    )
                owner = item.get("owner")
                title = item.get("title")
                if not isinstance(owner, str) or not isinstance(title, str) or not title:
                    raise ValueError(
                        f"{source}: instruction-set requires owner and title"
                    )
                if owner == "base":
                    instructions = project.catalog.base.instructions
                else:
                    extension = project.catalog.extensions.get(owner)
                    if extension is None:
                        raise ValueError(
                            f"{source}: unknown instruction-set owner {owner!r}"
                        )
                    instructions = extension.instructions
                introduction: list[DocumentTopic] = []
                raw_introduction = item.get("introduction", [])
                if not isinstance(raw_introduction, list):
                    raise ValueError(
                        f"{source}: instruction-set introduction must be a list"
                    )
                for raw_reference in raw_introduction:
                    if not isinstance(raw_reference, str):
                        raise ValueError(
                            f"{source}: instruction-set introduction must contain references"
                        )
                    introduction_reference: Reference[DocumentTopic] = Reference.parse(
                        raw_reference
                    )
                    topic = project.model.document_topics.get(
                        introduction_reference
                    )
                    if topic is None:
                        raise ValueError(f"{source}: unknown introduction topic")
                    if topic.owner != owner or topic.artifact != artifact:
                        raise ValueError(
                            f"{source}: introduction topic {topic.id!r} does not belong "
                            f"to {owner}.{artifact}"
                        )
                    introduction.append(topic)
                    included_topics.append(introduction_reference)
                included_owners.append(owner)
                blocks.append(
                    InstructionSetBlock(owner, title, tuple(introduction), instructions)
                )
                continue
            raise ValueError(f"{source}: body[{index}] has an unknown block kind")

        expected_topics = set(project.model.document_orders.get(artifact, ()))
        actual_topics = set(included_topics)
        duplicate_topics = sorted(
            reference
            for reference in actual_topics
            if included_topics.count(reference) != 1
        )
        missing_topics = sorted(expected_topics - actual_topics)
        extra_topics = sorted(actual_topics - expected_topics)
        if duplicate_topics or missing_topics or extra_topics:
            duplicate_topic_ids = [
                project.model.document_topics[reference].id
                for reference in duplicate_topics
            ]
            missing_topic_ids = [
                project.model.document_topics[reference].id
                for reference in missing_topics
            ]
            extra_topic_ids = [
                project.model.document_topics[reference].id
                for reference in extra_topics
            ]
            raise ValueError(
                f"{source}: invalid topic coverage: "
                f"duplicates={duplicate_topic_ids}, "
                f"missing={missing_topic_ids}, extra={extra_topic_ids}"
            )

        expected_groups = set(project.terminology.references.groups)
        actual_groups = set(included_groups)
        duplicate_groups = sorted(
            reference
            for reference in actual_groups
            if included_groups.count(reference) != 1
        )
        missing_groups = sorted(expected_groups - actual_groups)
        extra_groups = sorted(actual_groups - expected_groups)
        if duplicate_groups or missing_groups or extra_groups:
            duplicate_group_ids = [
                project.terminology.references.groups.resolve(reference).id
                for reference in duplicate_groups
            ]
            missing_group_ids = [
                project.terminology.references.groups.resolve(reference).id
                for reference in missing_groups
            ]
            extra_group_ids = [
                project.terminology.references.groups.resolve(reference).id
                for reference in extra_groups
            ]
            raise ValueError(
                f"{source}: invalid terminology group coverage: "
                f"duplicates={duplicate_group_ids}, "
                f"missing={missing_group_ids}, extra={extra_group_ids}"
            )

        expected_owners = ["base", *project.catalog.extensions]
        if included_owners != expected_owners:
            raise ValueError(
                f"{source}: instruction-set order {included_owners} does not match "
                f"{expected_owners}"
            )

        return cls(
            artifact=artifact,
            source=source,
            preamble=fragment("preamble"),
            title_page=fragment("title-page"),
            blocks=tuple(blocks),
            postamble=fragment("postamble"),
        )
