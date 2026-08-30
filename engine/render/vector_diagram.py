"""Explicit placement and TeX projection for instruction-owned vector diagrams."""

from __future__ import annotations

from pathlib import Path
import re

from ..reference import Reference, ReferenceError, UnknownReferenceError
from ..vector_diagram import VectorDiagram, VectorExample, render_tikz, tex_escape


_DIAGRAM_DIRECTIVE_RE = re.compile(
    r"(?m)^[ \t]*\(:diagram:([A-Za-z0-9_.-]+):\)[ \t]*$"
)
_DIAGRAM_OPEN = "(:diagram:"


def _reference_text(reference: Reference[object]) -> str:
    return ".".join((reference.owner, *reference.path, reference.element))


def _layout(example: VectorExample) -> tuple[str, str, str]:
    """Return the established page reservation and TikZ unit scales."""

    has_predicate_row = any(row["role"] == "predicate" for row in example.rows)
    if example.variant == "vector-lane-transfer" and has_predicate_row:
        needspace = 2.21 + 0.48 * (len(example.rows) - 2)
        if not example.scalable:
            needspace += 0.22
        return f"{needspace:.2f}in", ".76cm", ".70cm"
    if example.variant == "predicate-width-conversion":
        return "3.20in", ".76cm", ".70cm"
    if example.variant == "predicate-lane-transfer":
        if len(example.rows) == 3:
            needspace = "2.69in" if example.scalable else "2.91in"
        else:
            needspace = "2.60in"
        return needspace, ".76cm", ".70cm"
    if example.variant == "integer-width-conversion" and has_predicate_row:
        return "3.29in", ".76cm", ".70cm"
    if example.variant == "predicate-range-generation":
        needspace = (
            "3.45in"
            if example.data is not None and "states" in example.data
            else "3.25in"
        )
        return needspace, ".76cm", ".70cm"
    if example.variant == "scalar-vector-transfer":
        needspace = "3.25in" if len(example.data["scalars"]) > 1 else "2.50in"
        return needspace, ".76cm", ".70cm"
    if example.variant == "predicated-vector-load":
        return "4.25in", ".76cm", ".70cm"
    if example.variant == "predicated-vector-reduction":
        return "4.05in", ".76cm", ".70cm"
    if example.variant == "floating-point-width-conversion":
        return "3.29in", ".76cm", ".70cm"
    x_scale = ".94cm" if example.variant == "integer-width-conversion" else "0.72cm"
    return "2.50in", x_scale, "0.66cm"


class VectorDiagramRenderer:
    """Project one validated finite vector example into the reference TeX DSL."""

    def render(self, diagram: VectorDiagram) -> str:
        needspace, x_scale, y_scale = _layout(diagram.example)
        return "\n".join(
            (
                rf"\begin{{BedrockVectorExample}}{{{needspace}}}{{{x_scale}}}"
                rf"{{{y_scale}}}{{{tex_escape(diagram.caption)}}}"
                rf"{{{tex_escape(diagram.alt_text)}}}",
                render_tikz(diagram.example),
                r"\end{BedrockVectorExample}",
            )
        )


class VectorDiagramPlacementRenderer:
    """Resolve standalone diagram directives for one instruction description."""

    def __init__(self, diagrams: VectorDiagramRenderer | None = None) -> None:
        self.diagrams = diagrams or VectorDiagramRenderer()

    def expand(self, text: str, project, source: str | Path, owner=None) -> str:
        path = Path(source).resolve()
        matches = tuple(_DIAGRAM_DIRECTIVE_RE.finditer(text))
        if text.count(_DIAGRAM_OPEN) != len(matches):
            position = text.find(_DIAGRAM_OPEN)
            while position >= 0 and any(
                match.start() <= position < match.end() for match in matches
            ):
                position = text.find(_DIAGRAM_OPEN, position + len(_DIAGRAM_OPEN))
            line = text.count("\n", 0, max(position, 0)) + 1
            raise ValueError(
                f"{path}:{line}: (:diagram:...:) must occupy a standalone line"
            )

        bundle = None
        if isinstance(owner, Reference):
            try:
                bundle = project.catalog.instructions.resolve(owner)
            except UnknownReferenceError:
                pass

        if bundle is None:
            if matches:
                raise ValueError(
                    f"{path}: diagram placement requires an instruction description owner"
                )
            return text

        if path != bundle.artifacts.description.resolve():
            if matches:
                raise ValueError(
                    f"{path}: diagram placement is allowed only in the owning "
                    "instruction descriptions.tex"
                )
            return text

        placed: list[VectorDiagram] = []
        placed_references: list[Reference[VectorDiagram]] = []
        for match in matches:
            raw_reference = match.group(1)
            try:
                reference: Reference[VectorDiagram] = Reference.parse(raw_reference)
                diagram = project.vector_diagram(reference)
            except (ReferenceError, ValueError) as error:
                line = text.count("\n", 0, match.start()) + 1
                raise ValueError(
                    f"{path}:{line}: invalid vector diagram reference "
                    f"{raw_reference!r}"
                ) from error
            if reference not in bundle.diagrams.diagrams:
                line = text.count("\n", 0, match.start()) + 1
                raise ValueError(
                    f"{path}:{line}: diagram {_reference_text(reference)!r} is not "
                    "owned by this instruction"
                )
            placed.append(diagram)
            placed_references.append(reference)

        duplicates = sorted(
            {
                _reference_text(reference)
                for reference in placed_references
                if placed_references.count(reference) > 1
            }
        )
        if duplicates:
            raise ValueError(f"{path}: duplicate diagram placements {duplicates}")

        expected = set(bundle.diagrams.diagrams)
        missing = sorted(
            _reference_text(reference)
            for reference in expected - set(placed_references)
        )
        if missing:
            raise ValueError(f"{path}: unplaced declared diagrams {missing}")

        rendered = iter(self.diagrams.render(diagram) for diagram in placed)
        return _DIAGRAM_DIRECTIVE_RE.sub(lambda _match: next(rendered), text)


__all__ = ["VectorDiagramPlacementRenderer", "VectorDiagramRenderer"]
