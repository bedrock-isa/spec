"""Semantic dependency graph collected from authored strings."""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
import re
from typing import cast

from .reference import QualifiedReference, Reference
from .semantic_text import EntityReferenceText, SemanticText, TermReferenceText
from .entity import Entity


@dataclass(frozen=True, slots=True)
class DependencyEdge:
    source: Reference[object]
    target: Reference[object]
    kind: str
    source_path: Path
    offset: int


@dataclass(frozen=True, slots=True)
class EntityDependency:
    """One provider-owned authored or structured relationship."""

    source: Reference[object]
    target: QualifiedReference[object]
    kind: str


class DependencyGraph:
    def __init__(self) -> None:
        self._edges: list[DependencyEdge] = []

    @property
    def edges(self) -> tuple[DependencyEdge, ...]:
        return tuple(self._edges)

    def clear(self) -> None:
        self._edges.clear()

    def record(self, source: Reference[object], text: SemanticText) -> None:
        for part in text.parts:
            if isinstance(part, EntityReferenceText):
                self._edges.append(
                    DependencyEdge(source, part.reference, "reference", text.origin.source, part.start)
                )
            elif isinstance(part, TermReferenceText):
                self._edges.append(
                    DependencyEdge(source, part.reference, "term", text.origin.source, part.start)
                )

    def render_json(self, entities, root: Path) -> str:
        grouped: dict[
            tuple[Reference[object], Reference[object], str], list[DependencyEdge]
        ] = {}
        for edge in self._edges:
            grouped.setdefault((edge.source, edge.target, edge.kind), []).append(edge)
        incoming: dict[Reference[object], int] = {}
        outgoing: dict[Reference[object], int] = {}
        referenced = {edge.source for edge in self._edges} | {
            edge.target for edge in self._edges
        }
        ordered_references = sorted(referenced)
        node_ids = {
            reference: f"node-{index}"
            for index, reference in enumerate(ordered_references)
        }
        edges = []
        for (source, target, kind), occurrences in sorted(
            grouped.items(), key=lambda item: item[0]
        ):
            incoming[target] = incoming.get(target, 0) + len(occurrences)
            outgoing[source] = outgoing.get(source, 0) + len(occurrences)
            edges.append(
                {
                    "source": node_ids[source],
                    "target": node_ids[target],
                    "kind": kind,
                    "occurrences": len(occurrences),
                    "locations": [
                        {
                            "source": _relative(edge.source_path, root),
                            "offset": edge.offset,
                        }
                        for edge in occurrences
                    ],
                }
            )
        nodes = []
        for reference in ordered_references:
            entity = entities.resolve(cast(Reference[Entity], reference))
            presentation = entities.presentation(reference)
            nodes.append(
                {
                    "id": node_ids[reference],
                    "kind": _entity_type_name(entity),
                    "display": presentation.display,
                    "incoming": incoming.get(reference, 0),
                    "outgoing": outgoing.get(reference, 0),
                    "degree": incoming.get(reference, 0) + outgoing.get(reference, 0),
                }
            )
        return json.dumps(
            {"nodes": nodes, "edges": edges}, indent=2, sort_keys=True
        ) + "\n"


def _relative(path: Path, root: Path) -> str:
    resolved = path.resolve()
    try:
        return str(resolved.relative_to(root.resolve()))
    except ValueError:
        return str(resolved)


def _entity_type_name(entity: Entity) -> str:
    """Return a diagnostic type name without a parallel kind discriminator."""

    return re.sub(r"(?<!^)(?=[A-Z])", "-", type(entity).__name__).lower()
