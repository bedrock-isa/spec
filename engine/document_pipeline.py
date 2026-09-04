"""Collaborators for TeX expansion, LaTeX compilation, and PDF validation."""

from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path
import re
import subprocess


LOCAL_INPUT_RE = re.compile(r"\\input\{((?!/)(?![^}]*\.\.)[^}]+)\}")
FORBIDDEN_LOG_PATTERNS = (
    re.compile(r"LaTeX Warning: There were undefined references"),
    re.compile(r"LaTeX Warning: Reference .* undefined"),
    re.compile(r"Missing character:"),
    re.compile(r"destination with the same identifier"),
)


class TexInputExpander:
    """Expand repository-local ISA TeX inputs for stable source comparison."""

    def expand(
        self, text: str, source_root: str | Path, active: tuple[Path, ...] = ()
    ) -> str:
        root = Path(source_root).resolve()

        def replace(match: re.Match[str]) -> str:
            relative = Path(match.group(1))
            path = (root / relative).resolve()
            if path.suffix == "":
                path = path.with_suffix(".tex")
            if not path.is_relative_to(root) or not path.is_file():
                raise RuntimeError(f"cannot expand TeX input {match.group(1)!r}")
            if path in active:
                cycle = " -> ".join(str(item) for item in (*active, path))
                raise RuntimeError(f"cyclic TeX input: {cycle}")
            content = path.read_text(encoding="utf-8")
            expanded = self.expand(content, root, (*active, path))
            return (
                f"% begin input: {match.group(1)}\n{expanded}\n"
                f"% end input: {match.group(1)}"
            )

        return LOCAL_INPUT_RE.sub(replace, text)


@dataclass(frozen=True, slots=True)
class CompiledPdf:
    pdf: Path
    log: Path


class LatexCompiler:
    """Invoke the external LaTeX toolchain without interpreting its PDF."""

    def compile(
        self,
        source: Path,
        output_root: Path,
        repository: Path,
        executable: str,
    ) -> CompiledPdf:
        pdf_root = output_root / "pdf"
        pdf_root.mkdir(parents=True, exist_ok=True)
        environment = dict(os.environ)
        environment["TEXINPUTS"] = os.pathsep.join(
            (str(repository), str(repository / "style"), "")
        )
        result = subprocess.run(
            [
                executable,
                "-pdf",
                "-interaction=nonstopmode",
                "-halt-on-error",
                "-file-line-error",
                f"-outdir={pdf_root}",
                str(source),
            ],
            cwd=repository,
            env=environment,
            text=True,
            capture_output=True,
            check=False,
        )
        if result.returncode != 0:
            detail = "\n".join(part for part in (result.stdout, result.stderr) if part)
            raise RuntimeError(
                f"{source.stem} LaTeX compilation failed:\n" + detail[-12000:]
            )
        compiled = CompiledPdf(
            pdf_root / source.with_suffix(".pdf").name,
            pdf_root / source.with_suffix(".log").name,
        )
        if not compiled.pdf.is_file() or not compiled.log.is_file():
            raise RuntimeError("latexmk did not produce the expected PDF and log")
        return compiled


class PdfArtifactValidator:
    """Validate reader-visible PDF structure, fonts, and LaTeX diagnostics."""

    def validate(self, compiled: CompiledPdf) -> dict[str, object]:
        log_text = compiled.log.read_text(encoding="utf-8", errors="replace")
        failures = [
            pattern.pattern
            for pattern in FORBIDDEN_LOG_PATTERNS
            if pattern.search(log_text)
        ]
        if failures:
            raise RuntimeError("forbidden LaTeX diagnostics: " + ", ".join(failures))
        info = subprocess.run(
            ["pdfinfo", str(compiled.pdf)],
            text=True,
            capture_output=True,
            check=True,
        ).stdout
        page_match = re.search(r"^Pages:\s+(\d+)$", info, flags=re.MULTILINE)
        size_match = re.search(r"^Page size:\s+(.+)$", info, flags=re.MULTILINE)
        if page_match is None or int(page_match.group(1)) < 1:
            raise RuntimeError("compiled PDF has no readable pages")
        fonts = subprocess.run(
            ["pdffonts", str(compiled.pdf)],
            text=True,
            capture_output=True,
            check=True,
        ).stdout.splitlines()[2:]
        if not fonts:
            raise RuntimeError("compiled PDF has no readable fonts")
        unembedded = []
        for row in fonts:
            columns = row.split()
            if len(columns) < 6 or columns[-5] != "yes":
                unembedded.append(row)
        if unembedded:
            raise RuntimeError("compiled PDF contains unembedded fonts")
        return {
            "pages": int(page_match.group(1)),
            "page_size": size_match.group(1) if size_match else None,
            "fonts": len(fonts),
            "unembedded_fonts": len(unembedded),
            "undefined_references": 0,
            "missing_characters": 0,
            "duplicate_destinations": 0,
            "overfull_boxes": len(re.findall(r"Overfull \\[hv]box", log_text)),
            "underfull_boxes": len(re.findall(r"Underfull \\[hv]box", log_text)),
        }
