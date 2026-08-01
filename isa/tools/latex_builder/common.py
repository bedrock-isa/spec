"""Common LaTeX rendering helpers for the ISA reference generator."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any
import json
import re

import yaml

CAPTION_LABEL_RE = re.compile(r"^(?:Table|Figure)\s+\d+(?:-\d+)?\.\s*")
PLACEHOLDER_RE = re.compile(r"@[A-Z0-9_]+@")
TABLE_WIDTH_RE = re.compile(r"^(?:\d+(?:\.\d+)?(?:pt|in|cm|mm|em|ex)|X)$")
TEMPLATE_DIR = Path(__file__).with_name("templates")
TABLE_INLINE_LIST_MAX_CHARS = 32
TABLE_INLINE_ITEM_MAX_CHARS = 20


@dataclass(frozen=True)
class TextTex:
    """Untrusted ordinary text that must be escaped before entering TeX."""

    value: Any

    def render(self) -> str:
        text = str(self.value)
        replacements = {
            "\\": r"\textbackslash{}",
            "&": r"\&",
            "%": r"\%",
            "$": r"\$",
            "#": r"\#",
            "_": r"\_",
            "{": r"\{",
            "}": r"\}",
            "~": r"\textasciitilde{}",
            "^": r"\textasciicircum{}",
            "|": r"\textbar{}",
            "<": r"\textless{}",
            ">": r"\textgreater{}",
        }
        out = "".join(replacements.get(ch, ch) for ch in text)
        return (
            out.replace("->", r"\ensuremath{\rightarrow{}}")
            .replace("<-", r"\ensuremath{\leftarrow{}}")
            .replace("=>", r"\ensuremath{\Rightarrow{}}")
        )


@dataclass(frozen=True)
class CodeTex:
    """Untrusted code text rendered in a TeX code span."""

    value: Any

    def render(self) -> str:
        escaped = TextTex(self.value).render().replace("--", r"{-}{-}")
        return r"\texttt{" + escaped + "}"


@dataclass(frozen=True)
class TrustedRawTex:
    """Generator-owned TeX assembled only from literals and escaped values."""

    value: str

    def render(self) -> str:
        return self.value


def load_allocation(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as fp:
        return json.load(fp)


def latex_template(name: str) -> str:
    return (TEMPLATE_DIR / name).read_text(encoding="utf-8")


def tex_escape(value: Any) -> str:
    return TextTex(value).render()


def tex_code(value: Any) -> str:
    return CodeTex(value).render()


def tex_multiline(lines: list[str]) -> str:
    body = r"\\".join(tex_escape(line) for line in lines)
    return r"\begin{tabular}[t]{@{}l@{}}" + body + r"\end{tabular}"


def tex_multiline_latex(lines: list[str]) -> str:
    body = r"\\".join(lines)
    return r"\begin{tabular}[t]{@{}l@{}}" + body + r"\end{tabular}"


def table_list_should_stack(items: list[Any], text_fn: Any = str) -> bool:
    texts = [" ".join(str(text_fn(item)).split()) for item in items]
    joined = ", ".join(texts)
    return (
        len(joined) > TABLE_INLINE_LIST_MAX_CHARS
        or any(len(text) > TABLE_INLINE_ITEM_MAX_CHARS for text in texts)
    )


def tex_table_value(value: Any) -> str:
    if isinstance(value, list):
        if not value:
            return tex_escape("-")
        if table_list_should_stack(value, readable_text):
            return tex_multiline([readable_text(item) for item in value])
        return tex_escape(", ".join(readable_text(item) for item in value))
    if isinstance(value, set):
        if not value:
            return tex_escape("-")
        items = sorted(value)
        if table_list_should_stack(items, readable_text):
            return tex_multiline([readable_text(item) for item in items])
        return tex_escape(", ".join(readable_text(item) for item in items))
    return tex_escape(readable_text(value))


def tex_table_code_value(value: Any) -> str:
    if isinstance(value, list):
        if not value:
            return tex_escape("-")
        if table_list_should_stack(value):
            return tex_multiline_latex([tex_code(item) for item in value])
        return ", ".join(tex_code(item) for item in value)
    if isinstance(value, set):
        if not value:
            return tex_escape("-")
        items = sorted(value)
        if table_list_should_stack(items):
            return tex_multiline_latex([tex_code(item) for item in items])
        return ", ".join(tex_code(item) for item in items)
    return tex_code(value)


def caption_title(value: Any) -> str:
    return CAPTION_LABEL_RE.sub("", str(value)).strip()


def listed_figure_caption(caption: str) -> str:
    return rf"\manualfigurecaption{{{tex_escape(caption_title(caption))}}}"


def tex_yaml(value: Any) -> str:
    dumped = yaml.safe_dump(value, sort_keys=False, allow_unicode=False).strip()
    return tex_escape(dumped)


def mdash_join(items: list[str]) -> str:
    return ", ".join(item for item in items if item) or "-"


def pretty_key(key: str) -> str:
    return key.replace("_", " ").replace(".", " ").title()


def normalize_text(value: Any) -> str:
    if isinstance(value, list):
        return ", ".join(str(item) for item in value)
    if isinstance(value, dict):
        return yaml.safe_dump(value, sort_keys=False, allow_unicode=False).strip()
    return str(value)


def compact_text(value: Any) -> str:
    text = normalize_text(value)
    return " ".join(line.strip() for line in text.splitlines() if line.strip())


def readable_text(value: Any) -> str:
    return compact_text(value).replace("_", " ")


def memory_rule_text(value: Any) -> str:
    return readable_text(value)


def latex_paragraph(value: Any) -> str:
    return tex_escape(compact_text(value))


def instruction_docs(spec: dict[str, Any]) -> dict[str, dict[str, Any]]:
    docs = (spec.get("instructions") or {}).get("instruction_docs") or {}
    if not isinstance(docs, dict):
        return {}
    return {str(key): value for key, value in docs.items() if isinstance(value, dict)}


class LatexComponent:
    """Renderable LaTeX component."""

    def render(self) -> str:
        raise NotImplementedError

    def __str__(self) -> str:
        return self.render()


def render_component(value: Any) -> str:
    if isinstance(value, (LatexComponent, TextTex, CodeTex, TrustedRawTex)):
        return value.render()
    return str(value)


@dataclass(frozen=True)
class LatexTemplate(LatexComponent):
    name: str
    values: dict[str, Any] | None = None

    def render(self) -> str:
        text = latex_template(self.name)
        occurrences = PLACEHOLDER_RE.findall(text)
        duplicates = sorted(
            placeholder
            for placeholder in set(occurrences)
            if occurrences.count(placeholder) != 1
        )
        if duplicates:
            raise ValueError(
                f"duplicate LaTeX template placeholders in {self.name}: "
                + ", ".join(duplicates)
            )
        expected = {placeholder[1:-1] for placeholder in occurrences}
        provided = set(self.values or {})
        missing = sorted(expected - provided)
        unused = sorted(provided - expected)
        if missing or unused:
            raise ValueError(
                f"LaTeX template value mismatch in {self.name}: "
                f"missing [{', '.join(missing) or '-'}], "
                f"unused [{', '.join(unused) or '-'}]"
            )
        for key, value in (self.values or {}).items():
            if not isinstance(
                value,
                (LatexComponent, TextTex, CodeTex, TrustedRawTex),
            ):
                raise TypeError(
                    f"LaTeX template value {key} in {self.name} must have an "
                    "explicit TeX rendering type"
                )
            text = text.replace(f"@{key}@", value.render())
        return text


def _validate_table_shape(
    headers: list[str],
    rows: list[list[str]],
    widths: list[str] | None,
    where: str,
) -> None:
    if not headers:
        raise ValueError(f"{where}: table must have at least one column")
    column_count = len(headers)
    for row_index, row in enumerate(rows):
        if len(row) != column_count:
            raise ValueError(
                f"{where}: row {row_index} has {len(row)} cells; "
                f"expected {column_count}"
            )
    if widths is None:
        return
    if len(widths) != column_count:
        raise ValueError(
            f"{where}: {len(widths)} widths for {column_count} columns"
        )
    for index, width in enumerate(widths):
        if not TABLE_WIDTH_RE.fullmatch(width):
            raise ValueError(f"{where}: invalid width for column {index}: {width!r}")


@dataclass(frozen=True)
class LatexSequence(LatexComponent):
    parts: list[Any]
    separator: str = "\n"

    def render(self) -> str:
        return self.separator.join(render_component(part) for part in self.parts if part is not None)


@dataclass(frozen=True)
class LatexTopSection(LatexComponent):
    title: str

    def render(self) -> str:
        return "\n".join([r"\clearpage", rf"\section{{{tex_escape(self.title)}}}"])


@dataclass(frozen=True)
class LatexHiddenTopSection(LatexComponent):
    title: str
    clear_page: bool = True

    def render(self) -> str:
        lines = []
        if self.clear_page:
            lines.append(r"\clearpage")
        lines.extend(
            [
                r"\phantomsection",
                r"\refstepcounter{section}",
                rf"\addcontentsline{{toc}}{{section}}{{\protect\numberline{{\thesection}}{tex_escape(self.title)}}}",
            ]
        )
        return "\n".join(lines)


@dataclass(frozen=True)
class LatexLongTable(LatexComponent):
    headers: list[str]
    rows: list[list[str]]
    widths: list[str] | None = None
    caption: str | None = None
    style: str = "default"
    listed: bool = True

    def render(self) -> str:
        _validate_table_shape(self.headers, self.rows, self.widths, "LatexLongTable")
        if not self.rows:
            return "No entries.\\par\n"
        if self.widths:
            if "X" in self.widths:
                raise ValueError("LatexLongTable: flexible X columns are unsupported")
            spec = "@{}" + "".join(rf">{{\raggedright\arraybackslash}}p{{{width}}}" for width in self.widths) + "@{}"
        else:
            spec = "@{}" + " ".join("l" for _ in self.headers) + "@{}"
        environments = {
            "default": "manuallongtable",
            "dense": "manualdenselongtable",
        }
        if self.style not in environments:
            raise ValueError(f"unknown longtable style: {self.style}")
        environment = environments[self.style]
        out = []
        if self.caption:
            out.append(rf"\manualtablecaption{{{tex_escape(caption_title(self.caption))}}}")
        out.extend(
            [
                rf"\begin{{{environment}}}{{{spec}}}",
                "\\toprule",
                r"\rowcolor{ManualHeaderFill}",
            ]
        )
        header = " & ".join(r"\textbf{" + tex_escape(item) + "}" for item in self.headers) + r"\\"
        out.append(header)
        out.append("\\midrule")
        out.append("\\endfirsthead")
        if self.caption:
            out.append(
                rf"\multicolumn{{{len(self.headers)}}}{{@{{}}l}}{{\scriptsize\itshape "
                rf"Table \themanualtable\ (continued)}}\\"
            )
        out.append("\\toprule")
        out.append(r"\rowcolor{ManualHeaderFill}")
        out.append(header)
        out.append("\\midrule")
        out.append("\\endhead")
        for row in self.rows:
            out.append(" & ".join(row) + r"\\")
        out.append("\\bottomrule")
        out.append(rf"\end{{{environment}}}")
        return "\n".join(out) + "\n"


@dataclass(frozen=True)
class LatexTabular(LatexComponent):
    headers: list[str]
    rows: list[list[str]]
    widths: list[str] | None = None
    caption: str | None = None
    listed: bool = True

    def render(self) -> str:
        _validate_table_shape(self.headers, self.rows, self.widths, "LatexTabular")
        if not self.rows:
            return "No entries.\\par\n"
        if self.widths:
            spec = "@{}" + "".join(
                r">{\raggedright\arraybackslash}X"
                if width == "X"
                else rf">{{\raggedright\arraybackslash}}p{{{width}}}"
                for width in self.widths
            ) + "@{}"
        else:
            spec = (
                "@{}"
                + " ".join("l" for _ in self.headers[:-1])
                + (r" >{\raggedright\arraybackslash}X" if self.headers else "")
                + "@{}"
            )
        flexible = not self.widths or "X" in self.widths
        out = []
        if self.caption:
            out.append(rf"\manualtablecaption{{{tex_escape(caption_title(self.caption))}}}")
        if flexible:
            out.extend(
                [
                    r"\Needspace{1.25in}",
                    r"\begingroup\footnotesize",
                    r"\setlength{\aboverulesep}{0pt}",
                    r"\setlength{\belowrulesep}{0pt}",
                    r"\setlength{\extrarowheight}{1.2pt}",
                    r"\begin{center}",
                    rf"\begin{{tabularx}}{{\linewidth}}{{{spec}}}",
                ]
            )
        else:
            out.append(rf"\begin{{manualtabular}}{{{spec}}}")
        out.extend(
            [
                r"\toprule",
                r"\rowcolor{ManualHeaderFill}",
                " & ".join(
                    r"\textbf{" + tex_escape(header) + "}"
                    for header in self.headers
                )
                + r"\\",
                r"\midrule",
            ]
        )
        for row in self.rows:
            out.append(" & ".join(row) + r"\\")
        out.append(r"\bottomrule")
        if flexible:
            out.extend([r"\end{tabularx}", r"\end{center}", r"\endgroup"])
        else:
            out.append(r"\end{manualtabular}")
        return "\n".join(out) + "\n"


def render_latex_template(name: str, values: dict[str, Any] | None = None) -> str:
    return LatexTemplate(name, values).render()


def top_section(title: str) -> str:
    return LatexTopSection(title).render()


def hidden_top_section(title: str) -> str:
    return LatexHiddenTopSection(title).render()


def latex_longtable(
    headers: list[str],
    rows: list[list[str]],
    widths: list[str] | None = None,
    caption: str | None = None,
    *,
    style: str = "default",
    listed: bool = True,
) -> str:
    return LatexLongTable(headers, rows, widths, caption, style, listed).render()


def latex_tabular(
    headers: list[str],
    rows: list[list[str]],
    widths: list[str] | None = None,
    caption: str | None = None,
    *,
    listed: bool = True,
) -> str:
    return LatexTabular(headers, rows, widths, caption, listed).render()
