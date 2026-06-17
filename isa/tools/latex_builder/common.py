"""Common LaTeX rendering helpers for the ISA reference generator."""

from __future__ import annotations

from pathlib import Path
from typing import Any
import json
import re

import yaml

ARCH_NAME = "Bedrock"
MANUAL_TITLE = "Bedrock Programmer's Reference Manual"
MANUAL_SUBTITLE = "Bounded Word-Oriented CISC Architecture"
CAPTION_PREFIX_RE = re.compile(r"^(?:Table|Figure)\s+\d+(?:-\d+)?\.\s*")
TEMPLATE_DIR = Path(__file__).with_name("templates")
TABLE_INLINE_LIST_MAX_CHARS = 32
TABLE_INLINE_ITEM_MAX_CHARS = 20


def load_allocation(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as fp:
        return json.load(fp)


def latex_template(name: str) -> str:
    return (TEMPLATE_DIR / name).read_text(encoding="utf-8")


def render_latex_template(name: str, values: dict[str, Any] | None = None) -> str:
    text = latex_template(name)
    for key, value in (values or {}).items():
        text = text.replace(f"@{key}@", str(value))
    unresolved = sorted(set(re.findall(r"@[A-Z0-9_]+@", text)))
    if unresolved:
        raise ValueError(f"unresolved LaTeX template placeholders in {name}: {', '.join(unresolved)}")
    return text


def tex_escape(value: Any) -> str:
    text = str(value)
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


def tex_code(value: Any) -> str:
    return r"\texttt{" + tex_escape(value) + "}"


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
    return CAPTION_PREFIX_RE.sub("", str(value)).strip()


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


def document_preamble() -> str:
    return render_latex_template(
        "document_preamble.tex",
        {
            "ARCH_NAME": ARCH_NAME,
            "MANUAL_TITLE": MANUAL_TITLE,
        },
    )


def document_end() -> str:
    return render_latex_template("document_end.tex")


def title_page(plan: dict[str, Any], mnemonic_count: int, form_count: int) -> str:
    solver = plan.get("solver", {})
    return render_latex_template(
        "title_page.tex",
        {
            "MNEMONIC_COUNT": mnemonic_count,
            "FORM_COUNT": form_count,
            "SOLVER_STATUS": tex_escape(solver.get("status", "unknown")),
            "ARCH_NAME": ARCH_NAME,
            "ARCH_NAME_UPPER": ARCH_NAME.upper(),
            "MANUAL_TITLE": MANUAL_TITLE,
            "MANUAL_SUBTITLE": MANUAL_SUBTITLE,
        },
    )


def top_section(title: str) -> str:
    return "\n".join([r"\clearpage", rf"\section{{{tex_escape(title)}}}"])


def hidden_top_section(title: str) -> str:
    return "\n".join(
        [
            r"\clearpage",
            r"\phantomsection",
            r"\refstepcounter{section}",
            rf"\addcontentsline{{toc}}{{section}}{{\protect\numberline{{\thesection}}{tex_escape(title)}}}",
        ]
    )


def latex_longtable(
    headers: list[str],
    rows: list[list[str]],
    widths: list[str] | None = None,
    caption: str | None = None,
) -> str:
    if not rows:
        return "No entries.\\par\n"
    if widths:
        spec = "@{}" + "".join(rf">{{\raggedright\arraybackslash}}p{{{width}}}" for width in widths) + "@{}"
    else:
        spec = "@{}" + " ".join("l" for _ in headers) + "@{}"
    out = []
    out.extend(
        [
            "\\begingroup\\footnotesize",
            r"\setlength{\LTpre}{2pt}",
            r"\setlength{\LTpost}{2pt}",
            f"\\begin{{longtable}}{{{spec}}}",
            "\\toprule",
        ]
    )
    out.append(" & ".join(r"\textbf{" + tex_escape(header) + "}" for header in headers) + r"\\")
    out.append("\\midrule")
    out.append("\\endhead")
    for row in rows:
        out.append(" & ".join(row) + r"\\")
    out.append("\\bottomrule")
    out.append("\\end{longtable}")
    if caption:
        out.append(rf"\manualtablecaption{{{tex_escape(caption_title(caption))}}}")
    out.append("\\endgroup")
    return "\n".join(out) + "\n"


def latex_tabular(
    headers: list[str],
    rows: list[list[str]],
    widths: list[str] | None = None,
    caption: str | None = None,
) -> str:
    if not rows:
        return "No entries.\\par\n"
    if widths:
        spec = "@{}" + "".join(rf">{{\raggedright\arraybackslash}}p{{{width}}}" for width in widths) + "@{}"
    else:
        spec = "@{}" + " ".join("l" for _ in headers) + "@{}"
    out = [
        r"\Needspace{1.25in}",
        r"\begingroup\footnotesize",
        r"\begin{center}",
        f"\\begin{{tabular}}{{{spec}}}",
        r"\toprule",
        " & ".join(r"\textbf{" + tex_escape(header) + "}" for header in headers) + r"\\",
        r"\midrule",
    ]
    for row in rows:
        out.append(" & ".join(row) + r"\\")
    out.extend(
        [
            r"\bottomrule",
            r"\end{tabular}",
        ]
    )
    if caption:
        out.append(rf"\manualtablecaption{{{tex_escape(caption_title(caption))}}}")
    out.extend([r"\end{center}", r"\endgroup"])
    return "\n".join(out) + "\n"
