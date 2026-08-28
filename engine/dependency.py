"""Semantic dependency graph collected from authored strings."""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path

from .reference import Reference
from .semantic_text import EntityReferenceText, SemanticText, TermReferenceText


@dataclass(frozen=True, slots=True)
class DependencyEdge:
    source: Reference
    target: Reference
    kind: str
    source_path: Path
    offset: int


class DependencyGraph:
    def __init__(self) -> None:
        self._edges: list[DependencyEdge] = []

    @property
    def edges(self) -> tuple[DependencyEdge, ...]:
        return tuple(self._edges)

    def clear(self) -> None:
        self._edges.clear()

    def record(self, source: Reference, text: SemanticText) -> None:
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
        grouped: dict[tuple[Reference, Reference, str], list[DependencyEdge]] = {}
        for edge in self._edges:
            grouped.setdefault((edge.source, edge.target, edge.kind), []).append(edge)
        incoming: dict[Reference, int] = {}
        outgoing: dict[Reference, int] = {}
        edges = []
        for (source, target, kind), occurrences in sorted(
            grouped.items(), key=lambda item: tuple(map(str, item[0]))
        ):
            incoming[target] = incoming.get(target, 0) + len(occurrences)
            outgoing[source] = outgoing.get(source, 0) + len(occurrences)
            edges.append(
                {
                    "source": str(source),
                    "target": str(target),
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
        referenced = {edge.source for edge in self._edges} | {
            edge.target for edge in self._edges
        }
        nodes = []
        for reference in sorted(referenced, key=str):
            entity = entities.resolve(reference)
            nodes.append(
                {
                    "reference": str(reference),
                    "kind": entity.kind.value,
                    "display": entity.display,
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
