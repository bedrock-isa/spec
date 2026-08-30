"""Preprocessing for authored LaTeX sources."""

from __future__ import annotations

from collections import defaultdict
from pathlib import Path
import re

from ..dependency import DependencyGraph
from ..entity import EntityKind
from ..semantic_text import SemanticText, TextOrigin
from .document_fragment import DocumentFragmentPipeline
from .vector_diagram import VectorDiagramPlacementRenderer


LOCAL_INPUT_RE = re.compile(r"\\input\{((?!/)(?![^}]*\.\.)[^}]+)\}")
_PROTECTED_TEX_RE = re.compile(
    r"\(:[a-z][a-z0-9_-]*:[^\n]*?:\)"
    r"|(?<!\\)%[^\n]*"
    r"|\\(?:input|include|label|ref|pageref|autoref|eqref|cite|texttt|url|path|begin|end)"
    r"\*?(?:\[[^\]]*\])?\{[^{}]*\}"
)
_ESCAPE_OR_COMMENT_RE = re.compile(
    r"\(:[a-z][a-z0-9_-]*:[^\n]*?:\)|(?<!\\)%[^\n]*"
)


def rewrite_direct_terms(text: str, catalog) -> tuple[str, int]:
    """Replace unambiguous registered prose spellings with semantic escapes."""

    spellings = []
    for term in catalog.references.terms.values():
        for value in (
            term.forms.canonical,
            term.forms.plural,
            term.forms.adjective,
        ):
            if value is not None:
                spellings.append((value, "(:term:detected:)"))
    spellings.sort(key=lambda item: len(item[0]), reverse=True)
    protected = tuple((match.start(), match.end()) for match in _PROTECTED_TEX_RE.finditer(text))
    replacements: list[tuple[int, int, str]] = []
    occupied: list[tuple[int, int]] = []
    for spelling, escape in spellings:
        pattern = re.compile(
            rf"(?<![A-Za-z0-9_-]){re.escape(spelling)}(?![A-Za-z0-9_-])"
        )
        for match in pattern.finditer(text):
            span = (match.start(), match.end())
            if any(_overlaps(span, item) for item in (*protected, *occupied)):
                continue
            replacements.append((span[0], span[1], escape))
            occupied.append(span)
    for start, end, replacement in sorted(replacements, reverse=True):
        text = text[:start] + replacement + text[end:]
    return text, len(replacements)


def rewrite_direct_entity_codes(text: str, entities) -> tuple[str, int]:
    """Replace unambiguous code-form instruction and event mentions."""

    candidates: dict[str, int] = defaultdict(int)
    for entity in entities.references.values():
        if entity.kind not in {EntityKind.INSTRUCTION, EntityKind.EVENT}:
            continue
        escaped = entity.display.replace("_", r"\_")
        candidates[rf"\texttt{{{escaped}}}"] += 1
    protected = tuple(
        (match.start(), match.end()) for match in _ESCAPE_OR_COMMENT_RE.finditer(text)
    )
    replacements: list[tuple[int, int, str]] = []
    for marker, count in candidates.items():
        if count != 1:
            continue
        for match in re.finditer(re.escape(marker), text):
            span = (match.start(), match.end())
            if any(_overlaps(span, item) for item in protected):
                continue
            replacements.append((span[0], span[1], "(:ref:detected:)"))
    for start, end, replacement in sorted(replacements, reverse=True):
        text = text[:start] + replacement + text[end:]
    return text, len(replacements)


def _overlaps(left: tuple[int, int], right: tuple[int, int]) -> bool:
    return left[0] < right[1] and right[0] < left[1]


class LatexSourcePreprocessor:
    """Expand and semantically resolve one repository-local LaTeX source tree."""

    def __init__(
        self,
        fragments: DocumentFragmentPipeline,
        semantic,
        dependencies: DependencyGraph | None = None,
        diagrams: VectorDiagramPlacementRenderer | None = None,
    ) -> None:
        self.fragments = fragments
        self.semantic = semantic
        self.dependencies = dependencies or DependencyGraph()
        self.diagrams = diagrams or VectorDiagramPlacementRenderer()

    def render(self, source: str | Path, project, owner=None) -> str:
        repository = project.root.parent.resolve()
        path = Path(source).resolve()
        self._require_source(path, repository, str(source))
        return self._render(path, project, repository, (), owner).rstrip()

    def _render(
        self,
        path: Path,
        project,
        repository: Path,
        active: tuple[Path, ...],
        owner,
    ) -> str:
        if path in active:
            cycle = " -> ".join(str(item) for item in (*active, path))
            raise RuntimeError(f"cyclic TeX input: {cycle}")
        text = path.read_text(encoding="utf-8")
        if path.suffix != ".sty":
            migrated, replacements = rewrite_direct_terms(text, project.terminology)
            if replacements:
                first = _first_difference(text, migrated)
                raise ValueError(
                    f"{path}, offset {first}: registered terminology must use "
                    "(:term:...:) escapes"
                )
            entities = getattr(project, "entities", None)
            if entities is not None:
                migrated, replacements = rewrite_direct_entity_codes(text, entities)
                if replacements:
                    first = _first_difference(text, migrated)
                    raise ValueError(
                        f"{path}, offset {first}: registered entity mentions must use "
                        "(:ref:...:) escapes"
                    )
            text = self.fragments.expand(text, project, path)
            text = self.diagrams.expand(text, project, path, owner)
            semantic = SemanticText.parse(text, origin=TextOrigin(path))
            if owner is not None:
                self.dependencies.record(owner, semantic)
            text = self.semantic.render(
                semantic,
                project.terminology,
                entities=getattr(project, "entities", None),
                escape_literals=False,
            )

        def replace(match: re.Match[str]) -> str:
            requested = match.group(1)
            included = (repository / requested).resolve()
            if included.suffix == "":
                included = included.with_suffix(".tex")
            self._require_source(included, repository, requested)
            content = self._render(
                included, project, repository, (*active, path), owner
            )
            if included.suffix == ".sty":
                content = re.sub(r"(?m)^\\endinput\s*$", "", content).rstrip()
            return (
                f"% begin input: {requested}\n{content}\n"
                f"% end input: {requested}"
            )

        return LOCAL_INPUT_RE.sub(replace, text)

    @staticmethod
    def _require_source(path: Path, repository: Path, requested: str) -> None:
        if not path.is_relative_to(repository) or not path.is_file():
            raise RuntimeError(f"cannot preprocess TeX source {requested!r}")


def _first_difference(left: str, right: str) -> int:
    return next(
        index
        for index, (before, after) in enumerate(zip(left, right))
        if before != after
    )
