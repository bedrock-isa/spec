"""Render Sail project modules for shared model units."""

from __future__ import annotations

import os
from pathlib import Path
import re
from dataclasses import dataclass

from ..composition import SailProgram
from ..model import SailUnit


@dataclass(frozen=True, slots=True)
class SailProjectModule:
    """One owned module in the generated Sail project."""

    name: str
    requirements: tuple[str, ...]
    sources: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class SailProject:
    """Semantic Sail project structure before textual serialization."""

    modules: tuple[SailProjectModule, ...]


class SailProjectRenderer:
    def project(self, program: SailProgram, output_root: str | Path) -> SailProject:
        root = Path(output_root).resolve()
        registry_sources = (
            *(
                Path(os.path.relpath(source, root)).as_posix()
                for source in _registry_type_sources(program)
            ),
            "generated/registry.sail",
        )
        modules = [SailProjectModule("registry", (), registry_sources)]
        selected = {unit.reference: unit for unit in program.sail_units}
        control_register_semantics = _control_register_semantics(program)
        boundary = next(
            (
                unit
                for unit in program.sail_units
                if unit.owner == "base" and unit.id == "boundary"
            ),
            None,
        )
        if boundary is not None:
            selected.pop(boundary.reference)
        ordinary_units = tuple(
            unit for unit in program.sail_units if unit is not boundary
        )
        for unit in ordinary_units:
            requirements = ["registry"]
            requirements.extend(
                _module_name(selected[required])
                for required in unit.requires
                if required in selected
            )
            owned_sources: list[Path] = []
            for source in unit.sources:
                owned_sources.append(source)
                owned_sources.extend(
                    control_register_semantics.get(source.resolve(), ())
                )
            sources = tuple(
                Path(os.path.relpath(source, root)).as_posix()
                for source in owned_sources
            )
            if unit.owner == "base" and unit.id == "decode":
                sources = ("generated/catalog.sail", *sources)
            modules.append(
                SailProjectModule(_module_name(unit), tuple(requirements), sources)
            )

        operation_sources = tuple(
            dict.fromkeys(
                Path(os.path.relpath(semantics.source, root)).as_posix()
                for semantics in program.instruction_semantics
            )
        ) + ("generated/dispatch.sail",)
        provider = getattr(program, "execution_provider", None)
        if provider is not None:
            operation_sources += (
                Path(os.path.relpath(provider.provider, root)).as_posix(),
            )
        operation_requirements = [
            "registry",
            *(_module_name(unit) for unit in ordinary_units),
        ]
        modules.append(
            SailProjectModule(
                "operation_entries",
                tuple(operation_requirements),
                operation_sources,
            )
        )

        if boundary is not None:
            requirements = ["registry", "operation_entries"]
            requirements.extend(
                _module_name(selected[required])
                for required in boundary.requires
                if required in selected
            )
            sources = tuple(
                Path(os.path.relpath(source, root)).as_posix()
                for source in boundary.sources
            )
            modules.append(
                SailProjectModule(_module_name(boundary), tuple(requirements), sources)
            )
        return SailProject(tuple(modules))

    def render(self, program: SailProgram, output_root: str | Path) -> str:
        lines: list[str] = []
        for module in self.project(program, output_root).modules:
            lines.append(f"{module.name} {{")
            if module.requirements:
                lines.append(f"  requires {', '.join(module.requirements)}")
            lines.extend(_render_sources(module.sources))
            lines.extend(("}", ""))
        return "\n".join(lines)


def _render_sources(sources: tuple[str, ...]) -> list[str]:
    if len(sources) == 1:
        return [f"  files {sources[0]}"]
    return [
        "  files",
        *(
            f"    {source}{',' if index + 1 < len(sources) else ''}"
            for index, source in enumerate(sources)
        ),
    ]


def _registry_type_sources(program: SailProgram) -> tuple[Path, ...]:
    project = getattr(program, "project", None)
    model = getattr(project, "model", None)
    base = getattr(model, "base", None)
    if base is None:
        return ()
    return (base.root / "control_registers/semantics/types.sail",)


def _control_register_semantics(
    program: SailProgram,
) -> dict[Path, tuple[Path, ...]]:
    project = getattr(program, "project", None)
    configuration = getattr(program, "configuration", None)
    catalog = getattr(project, "control_registers", None)
    if catalog is None or configuration is None:
        return {}
    return {
        (
            namespace.root / "control_registers/semantics/control_state.sail"
        ).resolve(): tuple(
            register.semantics for register in namespace.registers.values()
        )
        for owner, namespace in catalog.namespaces.items()
        if owner in configuration.owners and namespace.registers
    }


def _module_name(unit: SailUnit) -> str:
    name = f"{unit.owner}_{unit.id}"
    return "model_" + re.sub(r"[^A-Za-z0-9_]", "_", name)
