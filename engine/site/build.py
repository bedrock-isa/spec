#!/usr/bin/env python3
"""Render the complete Bedrock MkDocs publication site."""

from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
from typing import Iterable

import yaml
from ..composition import DocumentComposition, InstructionSetBlock
from ..entity import instruction_label
from .navigation import PageRegistry, SiteError
from .structure import parse_latex_structure
from .pandoc import (
    read_pandoc_ast,
    render_page_ast,
    require_supported_pandoc,
    split_document_ast,
)
from .model import (
    DocumentSiteSpec,
    ROOT_PAGE_KEY,
    SiteModel,
    build_site,
    document_page_key,
    part_page_key,
    scoped_target,
)
from .visual import extract_visuals, render_visuals


UNRESOLVED_INCLUDE_RE = re.compile(r"\\(?:input|include)\{")
UNRESOLVED_PLACEHOLDER_RE = re.compile(r"@[A-Z0-9_]+@")


class SiteOutputError(SiteError):
    """The complete static publication site cannot be emitted safely."""


@dataclass(frozen=True)
class SiteDocument:
    key: str
    id: str
    navigation_title: str
    source: Path
    pdf_source: Path
    pdf_name: str


@dataclass(frozen=True)
class SiteOutput:
    pages: int
    targets: int
    anchored_targets: int
    visuals: int
    downloads: int


def _expand_latex(
    document: SiteDocument,
    destination: Path,
    *,
    latexpand: str,
    environment: dict[str, str],
) -> str:
    destination.parent.mkdir(parents=True, exist_ok=True)
    result = subprocess.run(
        [
            latexpand,
            "--fatal",
            "--empty-comments",
            "--output",
            str(destination),
            str(document.source),
        ],
        cwd=Path(__file__).resolve().parents[2],
        env=environment,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip() or str(result.returncode)
        raise SiteOutputError(f"latexpand failed for {document.key}: {detail}")
    expanded = destination.read_text(encoding="utf-8")
    if UNRESOLVED_INCLUDE_RE.search(expanded):
        raise SiteOutputError(
            f"{document.key}: latexpand left an unresolved input directive"
        )
    placeholders = sorted(set(UNRESOLVED_PLACEHOLDER_RE.findall(expanded)))
    if placeholders:
        raise SiteOutputError(
            f"{document.key}: unresolved template placeholders: {', '.join(placeholders)}"
        )
    return expanded


def _markdown_label(value: str) -> str:
    return value.replace("[", r"\[").replace("]", r"\]")


def _link(registry: PageRegistry, source: str, target: str, label: str) -> str:
    return f"[{_markdown_label(label)}]({registry.relative_link(source, target)})"


def _asset_link(
    registry: PageRegistry,
    source: str,
    asset: Path | PurePosixPath | str,
    label: str,
) -> str:
    return (
        f"[{_markdown_label(label)}]"
        f"({registry.relative_asset(source, PurePosixPath(asset))})"
    )


def _write_page(
    output_root: Path,
    registry: PageRegistry,
    page_key: str,
    content: str,
    written: set[str],
) -> None:
    if page_key in written:
        raise SiteOutputError(f"page {page_key!r} was rendered more than once")
    page = registry.page(page_key)
    destination = output_root / Path(page.output.as_posix())
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(content.rstrip() + "\n", encoding="utf-8")
    written.add(page_key)


def _root_landing(
    site: SiteModel,
    documents: tuple[DocumentSiteSpec, ...],
) -> str:
    lines = [
        "# Bedrock Architecture",
        "",
        "Reference documents for the Bedrock architecture, ELF ABI, C ABI, and compiler interface.",
        "",
        "## Reference documents",
        "",
    ]
    for document in documents:
        subtitle_suffix = (
            f": {document.structure.title.subtitle}"
            if document.structure.title.subtitle is not None
            else ""
        )
        lines.append(
            "- "
            + _link(
                site.registry,
                ROOT_PAGE_KEY,
                document_page_key(document.id),
                document.structure.title.title,
            )
            + subtitle_suffix
            + " ("
            + _asset_link(
                site.registry,
                ROOT_PAGE_KEY,
                document.download,
                "PDF",
            )
            + ")"
        )
    return "\n".join(lines) + "\n"


def _document_landing(
    site: SiteModel,
    document: DocumentSiteSpec,
) -> str:
    page_key = document_page_key(document.id)
    lines = [
        f"# {document.structure.title.title}",
        "",
    ]
    if document.structure.title.subtitle is not None:
        lines.extend([document.structure.title.subtitle, ""])
    lines.extend(
        [
            _asset_link(site.registry, page_key, document.download, "Download PDF"),
            "",
            "## Contents",
            "",
        ]
    )
    if document.structure.parts:
        for part in document.structure.parts:
            lines.append(
                "- "
                + _link(
                    site.registry,
                    page_key,
                    scoped_target(document.id, f"part:{part.key}"),
                    part.title,
                )
            )
    else:
        for section in document.structure.sections:
            lines.append(
                "- "
                + _link(
                    site.registry,
                    page_key,
                    scoped_target(document.id, f"page:{section.key}"),
                    section.title,
                )
            )
    return "\n".join(lines) + "\n"


def _part_index(
    site: SiteModel,
    document: DocumentSiteSpec,
    part_key: str,
) -> str:
    part = next(part for part in document.structure.parts if part.key == part_key)
    page_key = part_page_key(document.id, part.key)
    lines = [f"# {part.title}", ""]
    for section in document.structure.sections:
        if section.part != part.key:
            continue
        if section.key == "reading-an-instruction-description":
            lines.append(
                "- "
                + _link(
                    site.registry,
                    page_key,
                    scoped_target(document.id, "page:instructions"),
                    "Instructions",
                )
            )
            continue
        if section.key.startswith("instruction-group-"):
            continue
        lines.append(
            "- "
            + _link(
                site.registry,
                page_key,
                scoped_target(document.id, f"page:{section.key}"),
                section.title,
            )
        )
    return "\n".join(lines) + "\n"


def _instruction_index(
    site: SiteModel,
    document: DocumentSiteSpec,
    composition: DocumentComposition,
) -> str:
    page_key = f"{document.id}:instructions"
    lines = [
        "# Instructions",
        "",
        _link(
            site.registry,
            page_key,
            scoped_target(document.id, "page:reading-an-instruction-description"),
            "Reading an Instruction Description",
        ),
        "",
    ]
    groups = (
        block
        for block in composition.blocks
        if isinstance(block, InstructionSetBlock)
    )
    for group in groups:
        group_slug = re.sub(r"[^a-z0-9]+", "-", group.owner.lower()).strip("-")
        group_label = f"page:instruction-group-{group_slug}"
        lines.extend(
            [
                f"## {_markdown_label(group.title)}",
                "",
                _link(
                    site.registry,
                    page_key,
                    scoped_target(document.id, group_label),
                    f"{group.title} overview",
                ),
                "",
            ]
        )
        for bundle in group.instructions:
            mnemonic = bundle.instruction.mnemonic
            lines.append(
                "- "
                + _link(
                    site.registry,
                    page_key,
                    scoped_target(
                        document.id,
                        instruction_label(mnemonic),
                    ),
                    mnemonic,
                )
            )
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def _write_mathjax_configuration(source_root: Path) -> None:
    destination = source_root / "javascripts" / "mathjax.js"
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(
        """window.MathJax = {
  tex: {
    inlineMath: [["\\\\(", "\\\\)"], ["$", "$"]],
    displayMath: [["\\\\[", "\\\\]"], ["$$", "$$"]],
    processEscapes: true,
    processEnvironments: true
  },
  options: {
    ignoreHtmlClass: "\\\\b(?!(arithmatex))\\\\b.*",
    processHtmlClass: "arithmatex"
  }
};

document$.subscribe(() => {
  MathJax.typesetPromise();
});
""",
        encoding="utf-8",
    )


def _write_visual_stylesheet(source_root: Path) -> None:
    destination = source_root / "stylesheets" / "visuals.css"
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(
        """.md-content img[src*="assets/visuals/"] {
  display: block;
  width: 100%;
  height: auto;
}
""",
        encoding="utf-8",
    )


def _write_mkdocs_configuration(
    path: Path,
    source_root: Path,
    output_root: Path,
    site: SiteModel,
) -> None:
    configuration = {
        "site_name": "Bedrock Architecture",
        "site_description": (
            "Reference documents for the Bedrock architecture and its ABI "
            "and C interfaces."
        ),
        "docs_dir": str(source_root),
        "site_dir": str(output_root),
        "use_directory_urls": True,
        "strict": True,
        "theme": {
            "name": "material",
            "language": "en",
            "features": [
                "navigation.indexes",
                "navigation.sections",
                "navigation.top",
                "toc.follow",
            ],
        },
        "plugins": [{"search": {"lang": "en"}}],
        "markdown_extensions": [
            "attr_list",
            "footnotes",
            "tables",
            {"pymdownx.arithmatex": {"generic": True}},
        ],
        "extra_javascript": [
            "javascripts/mathjax.js",
            "https://unpkg.com/mathjax@3/es5/tex-mml-chtml.js",
        ],
        "extra_css": ["stylesheets/visuals.css"],
        "nav": site.navigation(),
    }
    path.write_text(
        yaml.safe_dump(
            configuration,
            allow_unicode=True,
            sort_keys=False,
            width=100,
        ),
        encoding="utf-8",
    )


def _build_mkdocs_site(
    configuration: Path,
    output_root: Path,
    *,
    mkdocs: str,
    environment: dict[str, str],
) -> None:
    result = subprocess.run(
        [mkdocs, "build", "--strict", "--clean", "--config-file", str(configuration)],
        cwd=configuration.parent,
        env=environment,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        detail = "\n".join(
            part for part in (result.stdout.strip(), result.stderr.strip()) if part
        )
        raise SiteOutputError(f"MkDocs build failed:\n{detail}")
    if not (output_root / "index.html").is_file():
        raise SiteOutputError("MkDocs did not produce the root index page")
    (output_root / ".nojekyll").write_text("", encoding="utf-8")


def _copy_downloads(
    documents: tuple[SiteDocument, ...],
    source_root: Path,
) -> dict[str, PurePosixPath]:
    downloads: dict[str, PurePosixPath] = {}
    names: set[str] = set()
    for document in documents:
        if document.id in downloads:
            raise SiteOutputError(f"duplicate site document ID: {document.id}")
        name = document.pdf_name
        if Path(name).name != name or Path(name).suffix.casefold() != ".pdf":
            raise SiteOutputError(
                f"{document.key}: PDF download name must be one safe .pdf filename"
            )
        if name.casefold() in names:
            raise SiteOutputError(f"duplicate PDF download name: {name}")
        names.add(name.casefold())
        if not document.pdf_source.is_file():
            raise SiteOutputError(
                f"{document.key}: validated PDF is missing: {document.pdf_source}"
            )
        pdf = document.pdf_source.read_bytes()
        if not pdf.startswith(b"%PDF-"):
            raise SiteOutputError(
                f"{document.key}: validated PDF has an invalid header"
            )
        asset = PurePosixPath("downloads") / name
        destination = source_root / Path(asset.as_posix())
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(pdf)
        downloads[document.id] = asset
    return downloads


def _require_rendered_pages(output_root: Path, site: SiteModel) -> None:
    missing: list[str] = []
    for page in site.registry.pages:
        url = site.registry.url(page.key).strip("/")
        destination = output_root / url / "index.html" if url else output_root / "index.html"
        if not destination.is_file():
            missing.append(site.registry.url(page.key))
    if missing:
        raise SiteOutputError(
            "MkDocs omitted registered pages: " + ", ".join(missing[:10])
        )


def render_site_output(
    documents: Iterable[SiteDocument],
    composition: DocumentComposition,
    output_root: Path,
    *,
    source_revision: str,
    pandoc: str = "pandoc",
    latexpand: str = "latexpand",
    mkdocs: str = "mkdocs",
    latexmk: str = "latexmk",
    pdfinfo: str = "pdfinfo",
    pdfseparate: str = "pdfseparate",
    pdftocairo: str = "pdftocairo",
    environment: dict[str, str] | None = None,
) -> SiteOutput:
    """Render Markdown sources, validate them, and build the static HTML site."""
    ordered = tuple(documents)
    environment = dict(os.environ if environment is None else environment)
    require_supported_pandoc(
        pandoc=pandoc,
        environment=environment,
    )
    expanded_root = output_root.parent / "site-expanded"
    source_root = output_root.parent / "site-source"
    visual_work_root = output_root.parent / "site-visuals"
    configuration = output_root.parent / "mkdocs.yml"
    expanded_root.mkdir(parents=True, exist_ok=True)
    source_root.mkdir(parents=True, exist_ok=True)

    downloads = _copy_downloads(ordered, source_root)

    structures: list[DocumentSiteSpec] = []
    expanded_paths: dict[str, Path] = {}
    visual_titles: dict[str, dict[str, str]] = {}
    expected_visuals: set[str] = set()
    for document in ordered:
        destination = expanded_root / f"{document.id}.tex"
        expanded = _expand_latex(
            document,
            destination,
            latexpand=latexpand,
            environment=environment,
        )
        structure = parse_latex_structure(expanded)
        visualized = extract_visuals(document.id, expanded, structure)
        render_visuals(
            document.id,
            expanded,
            visualized,
            source_root,
            visual_work_root,
            latexmk=latexmk,
            pdfinfo=pdfinfo,
            pdfseparate=pdfseparate,
            pdftocairo=pdftocairo,
            environment=environment,
        )
        transformed = expanded_root / f"{document.id}-site.tex"
        transformed.write_text(visualized.text, encoding="utf-8")
        expanded_paths[document.id] = transformed
        visual_titles[document.id] = visualized.titles
        expected_visuals.update(visualized.titles)
        structures.append(
            DocumentSiteSpec(
                document.id,
                document.navigation_title,
                downloads[document.id],
                structure,
            )
        )

    document_specs = tuple(structures)
    site = build_site(document_specs, composition)
    written: set[str] = set()
    emitted_targets: set[str] = set()
    emitted_visuals: set[str] = set()

    _write_page(
        source_root,
        site.registry,
        ROOT_PAGE_KEY,
        _root_landing(site, document_specs),
        written,
    )
    for document in document_specs:
        _write_page(
            source_root,
            site.registry,
            document_page_key(document.id),
            _document_landing(site, document),
            written,
        )
        for part in document.structure.parts:
            _write_page(
                source_root,
                site.registry,
                part_page_key(document.id, part.key),
                _part_index(site, document, part.key),
                written,
            )
        if document.id == "isa":
            _write_page(
                source_root,
                site.registry,
                f"{document.id}:instructions",
                _instruction_index(site, document, composition),
                written,
            )

        ast = read_pandoc_ast(
            expanded_paths[document.id],
            pandoc=pandoc,
            environment=environment,
        )
        source_pages = split_document_ast(document.id, document.structure, ast)
        for page_key, page_ast in source_pages.items():
            rendered = render_page_ast(
                page_ast,
                document=document.id,
                title=site.registry.page(page_key).title,
                registry=site.registry,
                visual_titles=visual_titles[document.id],
                api_version=ast.api_version,
                pandoc=pandoc,
                environment=environment,
            )
            emitted_targets.update(rendered.emitted_targets)
            emitted_visuals.update(rendered.emitted_visuals)
            _write_page(
                source_root,
                site.registry,
                page_key,
                rendered.markdown,
                written,
            )

    expected_pages = {page.key for page in site.registry.pages}
    if written != expected_pages:
        missing = sorted(expected_pages - written)
        extra = sorted(written - expected_pages)
        raise SiteOutputError(
            f"rendered page ownership mismatch; missing={missing}, extra={extra}"
        )
    expected_anchors = {
        name for name, target in site.registry.targets.items() if target.anchor is not None
    }
    if emitted_targets != expected_anchors:
        missing = sorted(expected_anchors - emitted_targets)
        extra = sorted(emitted_targets - expected_anchors)
        raise SiteOutputError(
            f"rendered anchor ownership mismatch; missing={missing}, extra={extra}"
        )
    if emitted_visuals != expected_visuals:
        missing = sorted(expected_visuals - emitted_visuals)
        extra = sorted(emitted_visuals - expected_visuals)
        raise SiteOutputError(
            f"rendered visual ownership mismatch; missing={missing}, extra={extra}"
        )

    _write_mathjax_configuration(source_root)
    _write_visual_stylesheet(source_root)
    _write_mkdocs_configuration(configuration, source_root, output_root, site)
    _build_mkdocs_site(
        configuration,
        output_root,
        mkdocs=mkdocs,
        environment=environment,
    )
    _require_rendered_pages(output_root, site)
    (source_root / "source-revision.txt").write_text(
        source_revision + "\n",
        encoding="utf-8",
    )
    return SiteOutput(
        pages=len(written),
        targets=len(site.registry.targets),
        anchored_targets=len(expected_anchors),
        visuals=len(expected_visuals),
        downloads=len(downloads),
    )
