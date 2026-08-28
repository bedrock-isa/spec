"""Directory-backed document topics for non-ISA specification domains."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .inventory import DirectoryInventory
from .reference import QualifiedReference, Reference, ReferenceIndex
from .yaml_document import SchemaValidatedYamlLoader


@dataclass(frozen=True, slots=True)
class DomainDocumentTopic:
    reference: Reference
    source: Path
    root: Path
    id: str
    title: str
    document: Path
    label: str
    objects: tuple[QualifiedReference, ...]


@dataclass(frozen=True, slots=True)
class DomainDocumentCatalog:
    inventory: DirectoryInventory
    topics: ReferenceIndex[DomainDocumentTopic]

    @classmethod
    def load(
        cls,
        *,
        owner: str,
        documents_root: str | Path,
        schema: str | Path,
    ) -> "DomainDocumentCatalog":
        root = Path(documents_root).resolve()
        inventory = DirectoryInventory.load(
            owner=owner,
            kind="document-topic",
            source=root / "topics/topics.yaml",
            root=root / "topics",
            key="topics",
        )
        topics = ReferenceIndex[DomainDocumentTopic]()
        positions: dict[Path, int] = {}
        for entity_id in inventory.declared:
            entity_root = inventory.root / entity_id
            source = entity_root / "topic.yaml"
            raw = SchemaValidatedYamlLoader().load(source, schema)
            if raw["id"] != entity_id:
                raise ValueError(
                    f"{source}: topic ID {raw['id']!r}; directory is {entity_id!r}"
                )
            document = (root / raw["document"]).resolve()
            if (
                not document.is_relative_to(root)
                or document.suffix != ".tex"
                or not document.is_file()
            ):
                raise ValueError(f"{source}: invalid topic document {raw['document']!r}")
            label = str(raw["label"])
            marker = rf"\label{{{label}}}"
            text = document.read_text(encoding="utf-8")
            if text.count(marker) != 1:
                raise ValueError(
                    f"{source}: document must contain exactly one {marker}"
                )
            position = text.index(marker)
            previous = positions.get(document, -1)
            if position <= previous:
                raise ValueError(
                    f"{source}: topic order differs from labels in {document}"
                )
            positions[document] = position
            reference = Reference(owner, ("document_topics",), entity_id)
            topic = DomainDocumentTopic(
                reference,
                source,
                entity_root,
                entity_id,
                str(raw["title"]),
                document,
                label,
                tuple(
                    QualifiedReference.parse(item)
                    for item in raw.get("objects", ())
                ),
            )
            topics.register(reference, topic)
        return cls(inventory, topics)

    def validate(self, workspace) -> None:
        for topic in self.topics.values():
            for reference in topic.objects:
                workspace.resolve(reference)
