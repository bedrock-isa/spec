"""Command-line entry point for ISA authoring tools."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import sys
from typing import Sequence

from .allocation import AllocationAnalyzer, CandidateOutsideNamespaceError
from .check import CheckService
from .diagnostics import Diagnostic, DiagnosticBag, Severity
from .document import DocumentBuilder
from .generation import ArtifactGeneratorRegistry, ArtifactWriter
from .project import IsaProject, ProjectLookupError
from .workspace import SpecWorkspace


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="python -m engine")
    parser.add_argument(
        "--isa-root",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "isa",
        help="ISA source root (default: repository/isa)",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    check = subparsers.add_parser("check", help="validate ISA authoring sources")
    check.add_argument(
        "targets", nargs="*", help="instruction names, references, or paths"
    )
    check.add_argument(
        "--format", choices=("text", "json"), default="text", dest="output_format"
    )
    alloc = subparsers.add_parser(
        "alloc", help="inspect named opcode spaces without editing sources"
    )
    allocation_commands = alloc.add_subparsers(dest="allocation_command", required=True)

    summary = allocation_commands.add_parser("summary", help="show occupancy by class")
    _add_format(summary)

    entries = allocation_commands.add_parser("entries", help="list allocations in a class")
    entries.add_argument("encoding_class", metavar="CLASS")
    _add_allocation_scope(entries)
    entries.add_argument("--grep", help="case-insensitive instruction/form filter")
    _add_format(entries)

    candidate = allocation_commands.add_parser("check", help="check a candidate prefix")
    candidate.add_argument("encoding_class", metavar="CLASS")
    candidate.add_argument("pattern", metavar="PATTERN")
    candidate.add_argument("--space", help="named operator space")
    _add_format(candidate)

    holes = allocation_commands.add_parser("holes", help="list maximal free prefixes")
    holes.add_argument("encoding_class", metavar="CLASS")
    _add_allocation_scope(holes)
    holes.add_argument(
        "--include-reclaimed",
        action="store_true",
        help="treat constraint-reclaimed slots as available",
    )
    holes.add_argument("--min-slots", type=int, default=1)
    holes.add_argument("--max-slots", type=int)
    holes.add_argument("--limit", type=int, default=32)
    holes.add_argument("--sort", choices=("address", "size"), default="address")
    _add_format(holes)

    docs = subparsers.add_parser(
        "docs", help="validate and compile reader-facing documents"
    )
    docs.add_argument("action", choices=("validate", "build"))
    docs.add_argument(
        "--output-root",
        type=Path,
        default=Path("output"),
        help="generated document root (default: output)",
    )
    docs.add_argument(
        "--latexmk",
        default=os.environ.get("LATEXMK", "latexmk"),
        help="latexmk executable",
    )

    artifacts = subparsers.add_parser(
        "artifacts", help="discover and generate declared specification artifacts"
    )
    artifacts.add_argument("action", choices=("list", "generate"))
    artifacts.add_argument(
        "artifact_ids",
        nargs="*",
        metavar="ARTIFACT",
        help="artifact ids (default for generate: all)",
    )
    artifacts.add_argument(
        "--output-root",
        type=Path,
        default=Path("output"),
        help="generated artifact root (default: output)",
    )
    return parser


def _add_format(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--format", choices=("text", "json"), default="text", dest="output_format"
    )


def _add_allocation_scope(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--space", help="named operator space")
    parser.add_argument(
        "--leading", help="leading 0/1/? prefix; omitted bits remain wildcards"
    )


def _load_failure(root: Path, error: Exception) -> DiagnosticBag:
    if isinstance(error, ProjectLookupError):
        code = f"project.lookup.{error.reason.value.replace('_', '-')}"
    elif isinstance(error, CandidateOutsideNamespaceError):
        code = "allocation.candidate-outside-namespace"
    else:
        code = "project.load"
    return DiagnosticBag(
        [
            Diagnostic(
                Severity.ERROR,
                code,
                root,
                str(error),
            )
        ]
    )


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        workspace = SpecWorkspace.load(args.isa_root.resolve().parent)
        provider = workspace.require_provider("isa")
        if not isinstance(provider, IsaProject):
            raise TypeError("workspace isa provider must be an IsaProject")
        project = provider
    except (OSError, ValueError) as error:
        diagnostics = _load_failure(args.isa_root, error)
        rendered = (
            diagnostics.render_json()
            if getattr(args, "output_format", "text") == "json"
            else diagnostics.render_text()
        )
        print(rendered, file=sys.stderr)
        return 1

    if args.command == "alloc":
        return _run_allocation(args, project)
    if args.command == "docs":
        return _run_docs(args, workspace)
    if args.command == "artifacts":
        return _run_artifacts(args, workspace)

    try:
        diagnostics = CheckService().check(project, args.targets)
    except (OSError, ValueError) as error:
        diagnostics = _load_failure(args.isa_root, error)

    rendered = (
        diagnostics.render_json()
        if args.output_format == "json"
        else diagnostics.render_text()
    )
    if rendered:
        print(rendered, file=sys.stderr if diagnostics.has_errors else sys.stdout)
    elif args.output_format == "json":
        print("[]")
    else:
        selected = project.select(args.targets)
        instruction_count = len(selected)
        form_count = sum(len(bundle.encodings.forms) for bundle in selected)
        instruction_label = "instruction" if instruction_count == 1 else "instructions"
        encoding_label = "encoding" if form_count == 1 else "encodings"
        print(
            f"checked {instruction_count} {instruction_label}, "
            f"{form_count} {encoding_label}: ok"
        )
    return 1 if diagnostics.has_errors else 0


def _run_docs(args: argparse.Namespace, workspace: SpecWorkspace) -> int:
    try:
        result = DocumentBuilder().build(
            workspace,
            args.output_root,
            compile_pdf=args.action == "build",
            latexmk=args.latexmk,
        )
    except (OSError, RuntimeError, ValueError) as error:
        print(f"document build failed: {error}", file=sys.stderr)
        return 1
    print(f"TeX validation: {'passed' if result.report.passed else 'failed'}")
    print(f"TeX: {result.tex}")
    print(f"validation report: {result.report_path}")
    if result.pdf is not None:
        print(f"PDF: {result.pdf}")
        print(f"PDF validation: {result.pdf_report}")
    return 0 if result.report.passed else 1


def _run_artifacts(args: argparse.Namespace, workspace: SpecWorkspace) -> int:
    try:
        registry = ArtifactGeneratorRegistry.discover(workspace)
        if args.action == "list":
            for artifact_id in registry.artifact_ids:
                generator = registry.generator(artifact_id)
                print(f"{artifact_id}\t{generator.definition.source}")
            return 0
        selected = tuple(args.artifact_ids) or registry.artifact_ids
        writer = ArtifactWriter()
        for artifact_id in selected:
            artifacts = registry.generate(artifact_id, workspace, args.output_root)
            written = writer.write(artifacts, args.output_root)
            print(f"generated {artifact_id}:")
            for path in written:
                print(f"  {path}")
        return 0
    except (NotImplementedError, OSError, ValueError) as error:
        print(f"artifact generation failed: {error}", file=sys.stderr)
        return 1


def _run_allocation(args: argparse.Namespace, project: IsaProject) -> int:
    analyzer = AllocationAnalyzer()
    try:
        if args.allocation_command == "summary":
            summaries = analyzer.summaries(project)
            if args.output_format == "json":
                print(
                    json.dumps(
                        [
                            {
                                "class": item.encoding_class,
                                "width": item.width,
                                "forms": item.forms,
                                "namespace": item.namespace_slots,
                                "allocated": item.allocated_slots,
                                "reclaimed": item.reclaimed_slots,
                                "clean_free": item.clean_free_slots,
                                "remaining": item.remaining_slots,
                            }
                            for item in summaries
                        ],
                        indent=2,
                    )
                )
            else:
                print("class       bits  forms       namespace       allocated       reclaimed      clean-free       remaining")
                for item in summaries:
                    print(
                        f"{item.encoding_class:<11}{item.width:>4}{item.forms:>7}"
                        f"{item.namespace_slots:>16,}{item.allocated_slots:>16,}"
                        f"{item.reclaimed_slots:>16,}{item.clean_free_slots:>16,}"
                        f"{item.remaining_slots:>16,}"
                    )
            return 0

        if args.allocation_command == "entries":
            entries = analyzer.entries(
                project,
                args.encoding_class,
                space=args.space,
                leading=args.leading,
                grep=args.grep,
            )
            if args.output_format == "json":
                print(
                    json.dumps(
                        [
                            {
                                "id": entry.name,
                                "instruction": f"{entry.owner}.{entry.mnemonic}",
                                "pattern": entry.pattern,
                                "raw": entry.raw_slots,
                                "assigned": entry.assigned_slots,
                                "reclaimed": entry.reclaimed_slots,
                                "source": str(entry.source),
                            }
                            for entry in entries
                        ],
                        indent=2,
                    )
                )
            else:
                print("id  pattern  raw  assigned  reclaimed")
                for entry in entries:
                    print(
                        f"{entry.name}  {entry.pattern}  {entry.raw_slots:,}  "
                        f"{entry.assigned_slots:,}  {entry.reclaimed_slots:,}"
                    )
            return 0

        if args.allocation_command == "check":
            result = analyzer.check_candidate(
                project,
                args.encoding_class,
                args.pattern,
                space=args.space,
            )
            if args.output_format == "json":
                print(
                    json.dumps(
                        {
                            "class": result.encoding_class,
                            "pattern": result.pattern,
                            "state": result.state,
                            "slots": result.slots,
                            "allocated": result.allocated_slots,
                            "reclaimed": result.reclaimed_slots,
                            "clean_free": result.clean_free_slots,
                            "allocated_entries": [
                                entry.name for entry in result.allocated_entries
                            ],
                            "reclaimed_entries": [
                                entry.name for entry in result.reclaimed_entries
                            ],
                        },
                        indent=2,
                    )
                )
            else:
                print(f"class:      {result.encoding_class}")
                print(f"pattern:    {result.pattern}")
                print(f"state:      {result.state}")
                print(f"slots:      {result.slots:,}")
                print(f"allocated:  {result.allocated_slots:,}")
                print(f"reclaimed:  {result.reclaimed_slots:,}")
                print(f"clean-free: {result.clean_free_slots:,}")
                if result.allocated_entries:
                    print("allocated overlaps:")
                    for entry in result.allocated_entries:
                        print(f"  {entry.name}  {entry.pattern}")
                if result.reclaimed_entries:
                    print("reclaimed overlaps:")
                    for entry in result.reclaimed_entries:
                        print(f"  {entry.name}  {entry.pattern}")
            return 1 if result.allocated_slots else 0

        holes = analyzer.holes(
            project,
            args.encoding_class,
            space=args.space,
            leading=args.leading,
            include_reclaimed=args.include_reclaimed,
            min_slots=args.min_slots,
            max_slots=args.max_slots,
            limit=args.limit,
            sort=args.sort,
        )
        if args.output_format == "json":
            print(
                json.dumps(
                    [
                        {
                            "pattern": hole.pattern,
                            "first": hole.cube.first,
                            "last": hole.cube.last,
                            "slots": hole.slots,
                        }
                        for hole in holes
                    ],
                    indent=2,
                )
            )
        else:
            print("pattern  first..last  slots")
            for hole in holes:
                digits = (hole.cube.width + 3) // 4
                print(
                    f"{hole.pattern}  0x{hole.cube.first:0{digits}x}.."
                    f"0x{hole.cube.last:0{digits}x}  {hole.slots:,}"
                )
        return 0
    except (OSError, ValueError) as error:
        diagnostics = _load_failure(args.isa_root, error)
        rendered = (
            diagnostics.render_json()
            if args.output_format == "json"
            else diagnostics.render_text()
        )
        print(rendered, file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
