"""Load ISA definition indexes and extension metadata."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from defs_schema import (
    InstructionSetIndex,
    decode_extension_catalog,
    decode_extension_manifest,
    decode_instruction_index,
    decode_operand_registry,
    decode_register_registry,
    decode_size_registry,
)

try:
    import yaml
except ImportError as exc:  # pragma: no cover - environment error path
    raise SystemExit("PyYAML is required to load ISA definition files") from exc


@dataclass(frozen=True)
class ExtensionDef:
    path: Path
    name: str
    data: dict[str, Any]


@dataclass(frozen=True)
class InstructionSetDef:
    name: str
    root: Path
    include: Path
    title: str
    introduction: Path | None = None


def load_yaml(path: Path) -> Any:
    with path.open(encoding="utf-8") as stream:
        return yaml.safe_load(stream)


def load_extension_catalog(defs_root: Path) -> dict[str, Any]:
    path = defs_root / "extensions.yaml"
    data = load_yaml(path)
    if not isinstance(data, dict):
        raise ValueError(f"{path}: expected mapping")
    decode_extension_catalog(path, data)
    return data


def load_extensions(
    defs_root: Path,
    catalog: dict[str, Any] | None = None,
) -> dict[str, ExtensionDef]:
    catalog = catalog if catalog is not None else load_extension_catalog(defs_root)
    extensions: dict[str, ExtensionDef] = {}
    loaded_paths: set[Path] = set()

    def visit(
        path: Path,
        parent_name: str | None = None,
        expected_local_name: str | None = None,
    ) -> None:
        resolved_path = path.resolve()
        if resolved_path in loaded_paths:
            raise ValueError(f"{path}: extension definition is referenced more than once")
        loaded_paths.add(resolved_path)
        data = load_yaml(path)
        if not isinstance(data, dict):
            raise ValueError(f"{path}: expected mapping")
        decode_extension_manifest(path, data)
        local_name = data.get("name")
        if not isinstance(local_name, str) or not local_name:
            raise ValueError(f"{path}: extension name must be a non-empty string")
        if expected_local_name is not None and local_name != expected_local_name:
            raise ValueError(
                f"{path}: extension name {local_name!r} does not match "
                f"catalog entry {expected_local_name!r}"
            )
        qualified_name = f"{parent_name}.{local_name}" if parent_name else local_name
        if qualified_name in extensions:
            raise ValueError(f"{path}: duplicate extension name {qualified_name!r}")
        extensions[qualified_name] = ExtensionDef(path, qualified_name, data)

        children = data.get("extensions", [])
        if not isinstance(children, list):
            raise ValueError(f"{path}: extensions must be a list")
        for child_ref in children:
            if not isinstance(child_ref, str) or not child_ref:
                raise ValueError(f"{path}: extension references must be non-empty strings")
            visit(path.parent / child_ref, qualified_name)

    extension_names = catalog.get("extensions", [])
    catalog_path = defs_root / "extensions.yaml"
    if not isinstance(extension_names, list):
        raise ValueError(f"{catalog_path}: extensions must be a list")
    for extension_name in extension_names:
        if not isinstance(extension_name, str) or not extension_name:
            raise ValueError(
                f"{catalog_path}: extension names must be non-empty strings"
            )
        visit(
            defs_root / "extensions" / extension_name / "extension.yaml",
            expected_local_name=extension_name,
        )
    return extensions


def load_instruction_sets(
    defs_root: Path,
    extensions: dict[str, ExtensionDef] | None = None,
) -> list[InstructionSetDef]:
    extensions = extensions if extensions is not None else load_extensions(defs_root)
    base_include = defs_root / "instructions.yaml"
    base_index = decode_instruction_index(base_include, load_yaml(base_include))
    instruction_sets = [
        InstructionSetDef(
            "base",
            defs_root,
            base_include,
            base_index.title,
            base_include.parent / base_index.introduction
            if base_index.introduction
            else None,
        )
    ]
    names = {"base"}

    for extension in extensions.values():
        include_ref = extension.data.get("instructions")
        if include_ref is None:
            continue
        if not isinstance(include_ref, str) or not include_ref:
            raise ValueError(f"{extension.path}: instructions path must be a string")
        if extension.name in names:
            raise ValueError(f"{extension.path}: duplicate instruction set {extension.name!r}")
        include_path = extension.path.parent / include_ref
        index = decode_instruction_index(include_path, load_yaml(include_path))
        instruction_sets.append(
            InstructionSetDef(
                extension.name,
                extension.path.parent,
                include_path,
                index.title,
                include_path.parent / index.introduction
                if index.introduction
                else None,
            )
        )
        names.add(extension.name)
    return instruction_sets


def load_operand_types(
    defs_root: Path,
    extensions: dict[str, ExtensionDef] | None = None,
) -> dict[str, Any]:
    extensions = extensions if extensions is not None else load_extensions(defs_root)
    paths = [defs_root / "operands.yaml"]
    for extension in extensions.values():
        operands_ref = extension.data.get("operands")
        if operands_ref is None:
            continue
        if not isinstance(operands_ref, str) or not operands_ref:
            raise ValueError(f"{extension.path}: operands path must be a string")
        paths.append(extension.path.parent / operands_ref)

    operand_types: dict[str, Any] = {}
    for path in paths:
        data = load_yaml(path)
        decode_operand_registry(path, data)
        declared = data.get("operand_types") if isinstance(data, dict) else None
        if not isinstance(declared, dict):
            raise ValueError(f"{path}: expected operand_types mapping")
        for name, definition in declared.items():
            if name in operand_types:
                raise ValueError(f"{path}: duplicate operand type {name!r}")
            if not isinstance(definition, dict):
                raise ValueError(f"{path}: operand type {name!r} must be a mapping")
            operand_types[str(name)] = definition
    return operand_types


def load_size_definitions(
    defs_root: Path,
    extensions: dict[str, ExtensionDef] | None = None,
) -> dict[str, Any]:
    extensions = extensions if extensions is not None else load_extensions(defs_root)
    paths = [defs_root / "sizes.yaml"]
    for extension in extensions.values():
        sizes_ref = extension.data.get("sizes")
        if sizes_ref is None:
            continue
        if not isinstance(sizes_ref, str) or not sizes_ref:
            raise ValueError(f"{extension.path}: sizes path must be a string")
        paths.append(extension.path.parent / sizes_ref)

    merged: dict[str, dict[str, Any]] = {
        "size_codes": {},
        "size_kinds": {},
    }
    for path in paths:
        data = load_yaml(path)
        decode_size_registry(path, data)
        if not isinstance(data, dict):
            raise ValueError(f"{path}: expected mapping")
        for section, definitions in merged.items():
            additions = data.get(section, {})
            if not isinstance(additions, dict):
                raise ValueError(f"{path}: {section} must be a mapping")
            duplicates = definitions.keys() & additions.keys()
            if duplicates:
                duplicate = sorted(duplicates)[0]
                raise ValueError(f"{path}: duplicate {section} entry {duplicate!r}")
            definitions.update(additions)
    return merged


def load_register_groups(
    defs_root: Path,
    extensions: dict[str, ExtensionDef] | None = None,
) -> dict[str, Any]:
    extensions = extensions if extensions is not None else load_extensions(defs_root)
    paths = [defs_root / "registers.yaml"]
    for extension in extensions.values():
        registers_ref = extension.data.get("registers")
        if registers_ref is None:
            continue
        if not isinstance(registers_ref, str) or not registers_ref:
            raise ValueError(f"{extension.path}: registers path must be a string")
        paths.append(extension.path.parent / registers_ref)

    groups: dict[str, Any] = {}
    for path in paths:
        data = load_yaml(path)
        decode_register_registry(path, data)
        if not isinstance(data, dict) or not isinstance(data.get("registers"), dict):
            raise ValueError(f"{path}: expected registers mapping")
        for name, group in data["registers"].items():
            if name in groups:
                raise ValueError(f"{path}: duplicate register group {name!r}")
            groups[str(name)] = group
    return groups
