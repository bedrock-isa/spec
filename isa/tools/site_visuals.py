#!/usr/bin/env python3
"""Extract reader-visible TeX diagrams and render them as site SVG assets."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path, PurePosixPath
import re
import subprocess
from typing import Iterable

from site_backend import SiteError
from site_latex import LatexStructure


DOCUMENT_BEGIN = r"\begin{document}"
DOCUMENT_END = r"\end{document}"
VISUAL_ENVIRONMENTS = {
    "manualtikzdiagram": (4, False),
    "manuallistedtikzdiagram": (4, False),
    "BedrockVectorExample": (5, False),
    "manualbitdiagram": (1, False),
    "manuallistedbitdiagram": (1, True),
    "manualformatdiagram": (1, False),
    "manuallistedformatdiagram": (1, True),
    "manualbyteorderdiagram": (6, False),
    "manuallistedbyteorderdiagram": (6, False),
    "manualstructlayout": (4, False),
    "manuallistedstructlayout": (4, False),
    "manualstackframediagram": (1, False),
    "manuallistedstackframediagram": (1, False),
}
FLOW_COMMANDS = {
    "manualeadirectflow": 4,
    "manualeaimmediateflow": 3,
    "manualeasimplememoryflow": 4,
    "manualeaadditivememoryflow": 5,
    "manualeaindexedmemoryflow": 6,
}
VISUAL_BEGIN_RE = re.compile(
    r"\\begin\{(?P<environment>"
    + "|".join((*VISUAL_ENVIRONMENTS, "center", "tikzpicture"))
    + r")\}|\\(?P<command>"
    + "|".join(FLOW_COMMANDS)
    + r")\b"
)
FIGURE_CAPTION_RE = re.compile(r"\\manualfigurecaption\s*\{")
LABEL_RE = re.compile(r"\\label\s*\{")
PDFINFO_PAGES_RE = re.compile(r"^Pages:\s+(\d+)\s*$", flags=re.MULTILINE)


class SiteVisualError(SiteError):
    """A TeX visual cannot be represented as a generated SVG asset."""


@dataclass(frozen=True)
class VisualSpec:
    id: str
    title: str
    caption_tex: str
    source: str
    marker: str
    asset: PurePosixPath
    start: int
    end: int
    label: str | None


@dataclass(frozen=True)
class VisualizedLatex:
    text: str
    visuals: tuple[VisualSpec, ...]

    @property
    def titles(self) -> dict[str, str]:
        return {visual.marker: visual.title for visual in self.visuals}


def _balanced_value(
    text: str,
    open_index: int,
    opening: str,
    closing: str,
    where: str,
) -> tuple[str, int]:
    if open_index >= len(text) or text[open_index] != opening:
        raise SiteVisualError(f"{where}: expected {opening!r}")
    depth = 0
    index = open_index
    while index < len(text):
        if text[index] == "\\":
            index += 2
            continue
        if text[index] == opening:
            depth += 1
        elif text[index] == closing:
            depth -= 1
            if depth == 0:
                return text[open_index + 1 : index], index + 1
        index += 1
    raise SiteVisualError(f"{where}: unterminated {opening!r} value")


def _next_argument(text: str, cursor: int, where: str) -> tuple[str, int]:
    while cursor < len(text) and text[cursor].isspace():
        cursor += 1
    return _balanced_value(text, cursor, "{", "}", where)


def _environment_end(text: str, environment: str, start: int) -> int:
    token_re = re.compile(
        rf"\\(?P<kind>begin|end)\{{{re.escape(environment)}\}}"
    )
    depth = 0
    for match in token_re.finditer(text, start):
        if match.group("kind") == "begin":
            depth += 1
        else:
            depth -= 1
            if depth == 0:
                return match.end()
    raise SiteVisualError(f"{environment} environment at byte {start} is unterminated")


def _plain_title(value: str) -> str:
    text = value
    # Public syntax is normally wrapped in \texttt{}.  Unwrap it with balanced
    # TeX arguments so metasyntax grouping braces remain visible rather than
    # being mistaken for the wrapper's closing delimiter.
    while True:
        command = text.find(r"\texttt{")
        if command < 0:
            break
        body, end = _balanced_value(
            text, command + len(r"\texttt"), "{", "}", "plain title texttt"
        )
        text = text[:command] + body + text[end:]
    replacements = {
        r"\_": "_",
        r"\{": "{",
        r"\}": "}",
        r"\<": "<",
        r"\textless{}": "<",
        r"\textgreater{}": ">",
        r"\textbar{}": "|",
        r"\textemdash{}": "—",
        "~": " ",
    }
    for source, destination in replacements.items():
        text = text.replace(source, destination)
    previous = None
    while text != previous:
        previous = text
        text = re.sub(r"\\[A-Za-z@]+\*?\s*\{([^{}]*)\}", r"\1", text)
    text = re.sub(r"\\[A-Za-z@]+\*?", "", text)
    text = " ".join(text.split())
    return text or "Diagram"


def _slug(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.casefold()).strip("-")
    return slug or "diagram"


def _owner_at(structure: LatexStructure, position: int) -> str:
    owner = "document"
    for section in structure.sections:
        if section.start <= position < section.end:
            owner = section.key
            for instruction in structure.instructions:
                if section.start <= instruction.start <= position:
                    owner = instruction.label.removeprefix("instr:")
                elif instruction.start > position:
                    break
            break
    return owner


def _optional_label(text: str, cursor: int, where: str) -> tuple[str | None, int]:
    while cursor < len(text) and text[cursor].isspace():
        cursor += 1
    if cursor >= len(text) or text[cursor] != "[":
        return None, cursor
    label, cursor = _balanced_value(text, cursor, "[", "]", where)
    normalized = label.strip()
    return normalized or None, cursor


def _label_in_snippet(snippet: str) -> str | None:
    match = LABEL_RE.search(snippet)
    if match is None:
        return None
    value, _ = _balanced_value(snippet, match.end() - 1, "{", "}", "visual label")
    return value.strip() or None


def _environment_visual(
    text: str,
    match: re.Match[str],
) -> tuple[int, str, str, str | None, str] | None:
    environment = match.group("environment")
    if environment is None:
        return None
    end = _environment_end(text, environment, match.start())
    snippet = text[match.start() : end]
    if environment == "center":
        if r"\begin{tikzpicture}" not in snippet:
            return None
        caption = FIGURE_CAPTION_RE.search(snippet)
        if caption is None:
            title = "Diagram"
        else:
            title, _ = _balanced_value(
                snippet,
                caption.end() - 1,
                "{",
                "}",
                "direct TikZ caption",
            )
        return end, title, snippet, _label_in_snippet(snippet), title
    if environment == "tikzpicture":
        return end, "Diagram", snippet, _label_in_snippet(snippet), "Diagram"

    argument_count, has_optional_label = VISUAL_ENVIRONMENTS[environment]
    cursor = match.end()
    arguments: list[str] = []
    for index in range(argument_count):
        value, cursor = _next_argument(
            text,
            cursor,
            f"{environment} argument {index + 1}",
        )
        arguments.append(value)
    label = None
    if has_optional_label:
        label, _ = _optional_label(text, cursor, f"{environment} label")
    if environment == "BedrockVectorExample":
        # The PDF caption and the image's nonvisual equivalent are separately
        # authored.  Existing generic consumers continue to receive title=alt.
        return end, arguments[4], snippet, label or _label_in_snippet(snippet), arguments[3]
    title = arguments[3] if environment.endswith("tikzdiagram") else arguments[0]
    return end, title, snippet, label or _label_in_snippet(snippet), title


def _command_visual(
    text: str,
    match: re.Match[str],
) -> tuple[int, str, str, str | None, str]:
    command = match.group("command")
    if command is None:
        raise AssertionError("visual command match has no command")
    cursor = match.end()
    arguments: list[str] = []
    for index in range(FLOW_COMMANDS[command]):
        value, cursor = _next_argument(
            text,
            cursor,
            f"{command} argument {index + 1}",
        )
        arguments.append(value)
    return cursor, arguments[0], text[match.start() : cursor], None, arguments[0]


def _replacement(visual: VisualSpec, title_tex: str) -> str:
    label = f"\\phantomsection\\label{{{visual.label}}}\n" if visual.label else ""
    # Keep site-only reader text intact across Pandoc's LaTeX and GFM writers.
    # Escaped ampersands become literal entity spellings in the Markdown, while
    # the Unicode dash avoids Pandoc dropping the TeX textemdash command.
    title_tex = (
        title_tex.replace(r"\textless{}", r"\&lt;")
        .replace(r"\textgreater{}", r"\&gt;")
        .replace(r"\textemdash{}", "—")
    )
    return (
        "\n\n"
        + label
        + "\\begin{center}\n"
        + f"\\includegraphics{{{visual.marker}}}\n"
        + f"\\par\\smallskip\\textbf{{{title_tex}}}\n"
        + "\\end{center}\n\n"
    )


def extract_visuals(
    document: str,
    text: str,
    structure: LatexStructure,
) -> VisualizedLatex:
    """Replace document-body visual constructs with stable image markers."""
    body_start = text.find(DOCUMENT_BEGIN)
    body_end = text.rfind(DOCUMENT_END)
    if body_start < 0 or body_end < body_start:
        raise SiteVisualError(f"{document}: expanded LaTeX has no document body")
    cursor = body_start + len(DOCUMENT_BEGIN)
    replacements: list[tuple[int, int, str]] = []
    visuals: list[VisualSpec] = []
    owner_counts: dict[str, int] = {}
    markers: set[str] = set()

    while True:
        match = VISUAL_BEGIN_RE.search(text, cursor, body_end)
        if match is None:
            break
        parsed = (
            _command_visual(text, match)
            if match.group("command") is not None
            else _environment_visual(text, match)
        )
        if parsed is None:
            cursor = _environment_end(text, match.group("environment") or "", match.start())
            continue
        end, title_tex, snippet, label, caption_tex = parsed
        owner = _owner_at(structure, match.start())
        ordinal = owner_counts.get(owner, 0) + 1
        owner_counts[owner] = ordinal
        visual_id = f"{_slug(owner)}-{ordinal:02d}"
        asset = PurePosixPath("assets") / "visuals" / document / f"{visual_id}.svg"
        marker = (PurePosixPath("_site_visual") / document / f"{visual_id}.svg").as_posix()
        if marker in markers:
            raise SiteVisualError(f"{document}: duplicate visual marker {marker}")
        markers.add(marker)
        visual = VisualSpec(
            id=visual_id,
            title=_plain_title(title_tex),
            caption_tex=caption_tex,
            source=snippet,
            marker=marker,
            asset=asset,
            start=match.start(),
            end=end,
            label=label,
        )
        visuals.append(visual)
        replacements.append((match.start(), end, _replacement(visual, caption_tex)))
        cursor = end

    transformed = text
    for start, end, replacement in reversed(replacements):
        transformed = transformed[:start] + replacement + transformed[end:]
    return VisualizedLatex(transformed, tuple(visuals))


def _run(
    command: list[str],
    *,
    cwd: Path,
    environment: dict[str, str],
    description: str,
) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        command,
        cwd=cwd,
        env=environment,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        detail = "\n".join(
            part for part in (result.stdout.strip(), result.stderr.strip()) if part
        )
        raise SiteVisualError(f"{description} failed:\n{detail}")
    return result


def _visual_document(expanded: str, visuals: Iterable[VisualSpec]) -> str:
    rendered = expanded
    ordered = tuple(visuals)
    for visual in reversed(ordered):
        rendered = (
            rendered[: visual.start]
            + "\n\\begin{preview}\n"
            + visual.source
            + "\n\\end{preview}\n"
            + rendered[visual.end :]
        )
    preamble_end = rendered.find(DOCUMENT_BEGIN)
    if preamble_end < 0:
        raise SiteVisualError("expanded LaTeX has no document preamble")
    setup = "\n".join(
        [
        r"\usepackage[active,tightpage]{preview}",
        DOCUMENT_BEGIN,
        r"\pagestyle{empty}",
        r"\setlength\PreviewBorder{6pt}",
        r"\renewcommand{\manualcaption}[1]{}",
        r"\renewcommand{\manualschemacaption}[1]{}",
        r"\renewcommand{\manualfigurecaption}[1]{}",
        r"\renewcommand{\manualfigurecaptionandlabel}[2]{}",
        r"\renewcommand{\manualtablecaption}[1]{}",
        ]
    )
    return rendered[:preamble_end] + setup + rendered[preamble_end + len(DOCUMENT_BEGIN) :]


def render_visuals(
    document: str,
    expanded: str,
    visualized: VisualizedLatex,
    source_root: Path,
    work_root: Path,
    *,
    latexmk: str,
    pdfinfo: str,
    pdfseparate: str,
    pdftocairo: str,
    environment: dict[str, str],
) -> None:
    """Compile all visuals once and convert each tightly cropped page to SVG."""
    visuals = visualized.visuals
    if not visuals:
        return
    document_root = work_root / document
    document_root.mkdir(parents=True, exist_ok=True)
    tex = document_root / "visuals.tex"
    tex.write_text(_visual_document(expanded, visuals), encoding="utf-8")
    _run(
        [
            latexmk,
            "-pdf",
            "-interaction=nonstopmode",
            "-halt-on-error",
            "-file-line-error",
            f"-outdir={document_root}",
            str(tex),
        ],
        cwd=document_root,
        environment=environment,
        description=f"TeX SVG staging for {document}",
    )
    pdf = document_root / "visuals.pdf"
    if not pdf.is_file():
        raise SiteVisualError(f"{document}: visual PDF was not produced")
    info = _run(
        [pdfinfo, str(pdf)],
        cwd=document_root,
        environment=environment,
        description=f"visual PDF inspection for {document}",
    )
    page_match = PDFINFO_PAGES_RE.search(info.stdout)
    pages = int(page_match.group(1)) if page_match else 0
    if pages != len(visuals):
        raise SiteVisualError(
            f"{document}: visual PDF has {pages} pages for {len(visuals)} visuals"
        )

    page_pattern = document_root / "visual-%d.pdf"
    _run(
        [pdfseparate, str(pdf), str(page_pattern)],
        cwd=document_root,
        environment=environment,
        description=f"visual PDF separation for {document}",
    )
    for page_number, visual in enumerate(visuals, start=1):
        page_pdf = document_root / f"visual-{page_number}.pdf"
        destination = source_root / Path(visual.asset.as_posix())
        destination.parent.mkdir(parents=True, exist_ok=True)
        _run(
            [pdftocairo, "-svg", str(page_pdf), str(destination)],
            cwd=document_root,
            environment=environment,
            description=f"SVG conversion for {document} visual {visual.id}",
        )
        if not destination.is_file() or "<svg" not in destination.read_text(
            encoding="utf-8", errors="replace"
        )[:1000]:
            raise SiteVisualError(
                f"{document}: invalid SVG output for visual {visual.id}"
            )
