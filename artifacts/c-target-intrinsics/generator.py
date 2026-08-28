from __future__ import annotations

from pathlib import Path
import re

from engine.generation import (
    AuthoredTexArtifactGenerator,
    ArtifactGenerationContext,
    GeneratedArtifact,
    GeneratedArtifactSet,
)
from interfaces.c.model import CInterfaceProject
from interfaces.c.model.naming import intrinsic_group_header


class Generator(AuthoredTexArtifactGenerator):
    """Publish target-intrinsic prose from its validated workspace model."""

    def generate(self, context: ArtifactGenerationContext) -> GeneratedArtifactSet:
        project = context.require_provider("interfaces.c")
        if not isinstance(project, CInterfaceProject):
            raise TypeError("interfaces.c provider must be a CInterfaceProject")
        source = context.workspace.root / str(self.definition.data["source"])
        output = Path(str(self.definition.data["output"]))
        content = source.read_text(encoding="utf-8")
        content = content.replace(
            r"\bedrockgeneratedheaderfamilies{}", _render_header_families(project)
        )
        content = content.replace(
            r"\bedrockgeneratedinterfacetypes{}", _render_types(project)
        )

        def replace_group(match: re.Match[str]) -> str:
            return _render_intrinsic_group(project, match.group(1))

        content = re.sub(
            r"\\bedrockgeneratedintrinsicgroup\{([a-z0-9_]+)\}",
            replace_group,
            content,
        )
        self.expander.expand(content, context.workspace.root)
        return GeneratedArtifactSet(
            (GeneratedArtifact(output, content),), artifact_id=self.artifact_id
        )


def _render_header_families(project: CInterfaceProject) -> str:
    membership = {
        group: collection.id
        for collection in project.collections.values()
        for group in collection.groups
    }
    rows = []
    for group in project.intrinsic_groups.values():
        family = group.title.removesuffix(" Intrinsics")
        rows.append(
            f"{family} & \\texttt{{\\textless{{}}"
            f"{intrinsic_group_header(group.id)}\\textgreater{{}}}} & "
            f"{membership[group.id]} & {group.data['exposure']}\\\\"
        )
    return _longtable(
        "Target Intrinsic Header Families",
        ("Family", "Header", "Umbrella", "Exposure"),
        rows,
        "p{1.15in}p{1.65in}p{0.65in}p{2.15in}",
    )


def _render_intrinsic_group(project: CInterfaceProject, group_id: str) -> str:
    group = next(
        item for item in project.intrinsic_groups.values() if item.id == group_id
    )
    rows = []
    for intrinsic in project.intrinsics.values():
        if intrinsic.group != group_id:
            continue
        signature = intrinsic.data["signature"]
        result = _document_type(str(signature["result"]))
        parameters = ",".join(
            _document_type(str(parameter["type"]))
            for parameter in signature["parameters"]
        ) or "void"
        operation = intrinsic.operation.local.element
        operands = intrinsic.data["lowering"].get("operands", {})
        if "size" in operands:
            operation += f".{operands['size']}"
        elif "source" in operands:
            operation += f" {operands['source']}"
        rows.append(
            f"\\texttt{{{_tex(intrinsic.id)}}} & "
            f"\\texttt{{{_tex(result)}({_tex(parameters)})}} & "
            f"\\texttt{{{_tex(operation)}}} & "
            f"{intrinsic.data['description']}\\\\"
        )
    return _longtable(
        group.title,
        ("Name", "C interface", "Lowering", "Availability, constraint, and effect"),
        rows,
        "p{1.4in}p{1.4in}p{0.8in}p{2.0in}",
    )


def _render_types(project: CInterfaceProject) -> str:
    rows = []
    for interface_type in project.types.values():
        spelling = f"__bedrock_{interface_type.id}_t"
        rows.append(
            f"\\texttt{{{_tex(spelling)}}} & "
            f"{interface_type.data.get('summary', interface_type.kind)}\\\\"
        )
    return _longtable(
        "Target Intrinsic Shared Types",
        ("Type", "ABI contract"),
        rows,
        "p{2.05in}p{3.45in}",
    )


def _longtable(
    caption: str,
    headings: tuple[str, ...],
    rows: list[str],
    columns: str,
) -> str:
    heading = " & ".join(f"\\textbf{{{item}}}" for item in headings)
    return "\n".join(
        (
            f"\\manualtablecaption{{{caption}}}",
            r"\begingroup\footnotesize",
            r"\setlength{\tabcolsep}{2pt}",
            f"\\begin{{longtable}}{{@{{}}{columns}@{{}}}}",
            r"\toprule",
            heading + r"\\",
            r"\midrule",
            r"\endhead",
            *rows,
            r"\bottomrule",
            r"\end{longtable}",
            r"\endgroup",
        )
    )


def _document_type(type_id: str) -> str:
    names = {
        "u8": "u8",
        "u16": "u16",
        "u32": "u32",
        "u64": "u64",
        "f32": "float",
        "f64": "double",
        "size": "size_t",
        "void": "void",
        "void_pointer": "void *",
        "const_void_pointer": "const void *",
    }
    if type_id in names:
        return names[type_id]
    if type_id.endswith("_pointer"):
        return names[type_id.removesuffix("_pointer")] + " *"
    if ".types." in type_id:
        return type_id.rsplit(".", 1)[-1]
    return type_id


def _tex(value: str) -> str:
    return value.replace("_", r"\_")
