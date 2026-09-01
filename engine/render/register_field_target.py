"""Explicit public-target placement for architectural register fields."""

from __future__ import annotations

from pathlib import Path
import re

from ..entity import EntityKind
from ..reference import Reference, UnknownReferenceError
from .document_fragment import DocumentFragmentContext, DocumentFragmentProvider


_REGISTER_FIELD_TARGET_OPEN = "(:register-field-target:"
_REGISTER_FIELD_TARGET_RE = re.compile(
    r"\(:register-field-target:([A-Za-z0-9_.-]+):\)"
)


class RegisterFieldTargetRenderer(DocumentFragmentProvider):
    """Place anchors selected by authored register-field definition prose."""

    PLACEHOLDER = _REGISTER_FIELD_TARGET_OPEN

    @property
    def placeholders(self) -> frozenset[str]:
        return frozenset((self.PLACEHOLDER,))

    def expand(self, text: str, context: DocumentFragmentContext) -> str:
        matches = tuple(_REGISTER_FIELD_TARGET_RE.finditer(text))
        if text.count(_REGISTER_FIELD_TARGET_OPEN) != len(matches):
            raise ValueError(
                f"{context.source}: malformed (:register-field-target:...:) directive"
            )

        def replacement(match: re.Match[str]) -> str:
            reference = Reference.parse(match.group(1))
            self._require_field(context.project, reference, context.source)
            return (
                rf"\phantomsection\label{{"
                rf"{context.public_targets.label(reference)}}}"
            )

        return _REGISTER_FIELD_TARGET_RE.sub(replacement, text)

    @classmethod
    def public_targets(
        cls, project, sources: tuple[Path, ...]
    ) -> tuple[tuple[Reference[object], str], ...]:
        """Declare the field targets explicitly placed in authored sources."""

        targets: list[tuple[Reference[object], str]] = []
        placed: dict[Reference[object], Path] = {}
        for source in sources:
            if source.suffix == ".sty":
                continue
            text = source.read_text(encoding="utf-8")
            matches = tuple(_REGISTER_FIELD_TARGET_RE.finditer(text))
            if text.count(_REGISTER_FIELD_TARGET_OPEN) != len(matches):
                raise ValueError(
                    f"{source}: malformed (:register-field-target:...:) directive"
                )
            for match in matches:
                reference = Reference.parse(match.group(1))
                cls._require_field(project, reference, source)
                previous = placed.get(reference)
                if previous is not None:
                    raise ValueError(
                        f"{source}: duplicate public register-field target "
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
                targets.append((reference, f"register-field:{slug}"))
        return tuple(targets)

    @staticmethod
    def _require_field(project, reference, source: Path | None) -> None:
        try:
            entity = project.entities.resolve(reference)
        except UnknownReferenceError as error:
            raise ValueError(
                f"{source}: unknown register-field target reference"
            ) from error
        if entity.kind not in {
            EntityKind.REGISTER_FIELD,
            EntityKind.CONTROL_REGISTER_FIELD,
        }:
            raise ValueError(
                f"{source}: register-field target resolves to {entity.kind.value}"
            )
