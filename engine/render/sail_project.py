"""Render Sail project modules for shared model units."""

from __future__ import annotations

import os
from pathlib import Path
import re

from ..composition import SailProgram


class SailProjectRenderer:
    def render(self, program: SailProgram, output_root: str | Path) -> str:
        root = Path(output_root).resolve()
        lines = ["registry {", "  files generated/registry.sail", "}", ""]
        selected = {unit.reference: unit for unit in program.sail_units}
        boundary = selected.pop("base.boundary", None)
        ordinary_units = tuple(
            unit for unit in program.sail_units if unit.reference != "base.boundary"
        )
        for unit in ordinary_units:
            requirements = ["registry"]
            requirements.extend(
                _module_name(required)
                for required in unit.requires
                if required in selected
            )
            sources = tuple(
                Path(os.path.relpath(source, root)).as_posix()
                for source in unit.sources
            )
            if unit.reference == "base.decode":
                sources = ("generated/catalog.sail", *sources)
            lines.extend(
                [
                    f"{_module_name(unit.reference)} {{",
                    f"  requires {', '.join(requirements)}",
                    *_render_sources(sources),
                    "}",
                    "",
                ]
            )

        operation_sources = tuple(
            dict.fromkeys(
                Path(os.path.relpath(semantics.source, root)).as_posix()
                for semantics in program.instruction_semantics
            )
        ) + ("generated/dispatch.sail",)
        operation_requirements = [
            "registry", *(_module_name(unit.reference) for unit in ordinary_units)
        ]
        lines.extend(
            [
                "operation_entries {",
                f"  requires {', '.join(operation_requirements)}",
                *_render_sources(operation_sources),
                "}",
                "",
            ]
        )

        if boundary is not None:
            requirements = ["registry", "operation_entries"]
            requirements.extend(
                _module_name(required)
                for required in boundary.requires
                if required in selected
            )
            sources = tuple(
                Path(os.path.relpath(source, root)).as_posix()
                for source in boundary.sources
            )
            lines.extend(
                [
                    f"{_module_name(boundary.reference)} {{",
                    f"  requires {', '.join(requirements)}",
                    *_render_sources(sources),
                    "}",
                    "",
                ]
            )
        return "\n".join(lines)


def _render_sources(sources: tuple[str, ...]) -> list[str]:
    if len(sources) == 1:
        return [f"  files {sources[0]}"]
    return [
        "  files",
        *(f"    {source}{',' if index + 1 < len(sources) else ''}" for index, source in enumerate(sources)),
    ]


def _module_name(reference: str) -> str:
    return "model_" + re.sub(r"[^A-Za-z0-9_]", "_", reference)
