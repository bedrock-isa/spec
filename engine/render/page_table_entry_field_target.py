"""Explicit public-target placement for page-table-entry fields."""

from __future__ import annotations

from pathlib import Path
import re

from ..page_table_entry import PageTableEntryField
from ..reference import Reference, UnknownReferenceError
from .document_fragment import DocumentFragmentContext, DocumentFragmentProvider


_PTE_FIELD_TARGET_OPEN = "(:pte-field-target:"
_PTE_FIELD_TARGET_RE = re.compile(
    r"\(:pte-field-target:([A-Za-z0-9_.-]+):\)"
)


class PageTableEntryFieldTargetRenderer(DocumentFragmentProvider):
    """Place anchors selected by authored PTE field definitions."""

    PLACEHOLDER = _PTE_FIELD_TARGET_OPEN

    @property
    def placeholders(self) -> frozenset[str]:
        return frozenset((self.PLACEHOLDER,))

    def expand(self, text: str, context: DocumentFragmentContext) -> str:
        matches = tuple(_PTE_FIELD_TARGET_RE.finditer(text))
        if text.count(_PTE_FIELD_TARGET_OPEN) != len(matches):
            raise ValueError(
                f"{context.source}: malformed (:pte-field-target:...:) directive"
            )

        def replacement(match: re.Match[str]) -> str:
            reference = Reference.parse(match.group(1))
            self._require_field(context.project, reference, context.source)
            return (
                rf"\phantomsection\label{{"
                rf"{context.public_targets.label(reference)}}}"
            )

        return _PTE_FIELD_TARGET_RE.sub(replacement, text)

    @classmethod
    def public_targets(
        cls, project, sources: tuple[Path, ...]
    ) -> tuple[tuple[Reference[object], str], ...]:
        """Declare PTE field targets explicitly placed in authored sources."""

        targets: list[tuple[Reference[object], str]] = []
        placed: dict[Reference[object], Path] = {}
        for source in sources:
            if source.suffix == ".sty":
                continue
            text = source.read_text(encoding="utf-8")
            matches = tuple(_PTE_FIELD_TARGET_RE.finditer(text))
            if text.count(_PTE_FIELD_TARGET_OPEN) != len(matches):
                raise ValueError(
                    f"{source}: malformed (:pte-field-target:...:) directive"
                )
            for match in matches:
                reference = Reference.parse(match.group(1))
                cls._require_field(project, reference, source)
                previous = placed.get(reference)
                if previous is not None:
                    raise ValueError(
                        f"{source}: duplicate public PTE field target "
                        f"{match.group(1)!r}; first placed by {previous}"
                    )
                placed[reference] = source
                slug = re.sub(
                    r"[^a-z0-9]+",
                    "-",
                    ".".join(
                        (reference.owner, *reference.path, reference.element)
                    ).lower(),
                ).strip("-")
                targets.append((reference, f"pte-field:{slug}"))
        return tuple(targets)

    @staticmethod
    def _require_field(project, reference, source: Path | None) -> None:
        try:
            entity = project.entities.resolve(reference)
        except UnknownReferenceError as error:
            raise ValueError(f"{source}: unknown PTE field target reference") from error
        if not isinstance(entity, PageTableEntryField):
            raise ValueError(
                f"{source}: PTE field target resolves to "
                f"{type(entity).__name__}"
            )
