#!/usr/bin/env python3
"""Generate the Bedrock target-intrinsic reference tables from their manifest."""

from __future__ import annotations

from pathlib import Path
import re
from typing import Any

from latex_builder.common import tex_code, tex_escape

try:
    import yaml
except ImportError as exc:  # pragma: no cover - environment error path
    raise SystemExit("PyYAML is required to generate target-intrinsic tables") from exc


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_MANIFEST = ROOT / "isa" / "interfaces" / "c" / "target_intrinsics.yaml"
DEFAULT_OUTPUT_DIR = ROOT / "isa" / "interfaces" / "c" / "generated" / "target_intrinsics"
HEADER_ROOT = ROOT / "isa" / "interfaces" / "c" / "include"

BUILTIN_LAYOUTS = {
    "core": ("1.25in", "1.25in", "0.8in", "2.3in"),
    "memory": ("1.35in", "1.3in", "0.75in", "2.2in"),
    "integer": ("1.3in", "1.55in", "0.75in", "2.0in"),
    "floating_point": ("1.25in", "1.3in", "0.85in", "2.2in"),
    "system_registers": ("1.4in", "1.3in", "0.7in", "2.2in"),
    "cache": ("1.45in", "1.3in", "0.9in", "1.95in"),
    "mmu": ("1.4in", "1.35in", "0.75in", "2.1in"),
    "processor_state": ("1.55in", "1.35in", "0.8in", "1.9in"),
}
TABLE_WIDTH_RE = re.compile(r"^\d+(?:\.\d+)?(?:pt|in|cm|mm|em|ex)$")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def require_mapping(value: Any, context: str) -> dict[str, Any]:
    require(isinstance(value, dict), f"{context}: expected a mapping")
    return value


def require_list(value: Any, context: str) -> list[Any]:
    require(isinstance(value, list), f"{context}: expected a list")
    return value


def require_string(value: Any, context: str) -> str:
    require(isinstance(value, str) and bool(value), f"{context}: expected a non-empty string")
    return value


def load_manifest(path: Path = DEFAULT_MANIFEST) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    manifest = require_mapping(data, str(path))
    validate_manifest(manifest, path)
    return manifest


def validate_manifest(manifest: dict[str, Any], path: Path = DEFAULT_MANIFEST) -> None:
    require(manifest.get("version") == 0, f"{path}: version must be 0")

    header_families = require_list(manifest.get("header_families"), f"{path}: header_families")
    builtin_families = require_list(manifest.get("builtin_families"), f"{path}: builtin_families")
    shared_types = require_list(manifest.get("shared_types"), f"{path}: shared_types")

    header_ids: list[str] = []
    headers: list[str] = []
    for index, raw_family in enumerate(header_families):
        context = f"{path}: header_families[{index}]"
        family = require_mapping(raw_family, context)
        family_id = require_string(family.get("id"), f"{context}.id")
        header_ids.append(family_id)
        headers.append(require_string(family.get("header"), f"{context}.header"))
        require_string(family.get("name"), f"{context}.name")
        require(
            family.get("umbrella") in {"public", "system"},
            f"{context}.umbrella: expected 'public' or 'system'",
        )
        require_string(family.get("exposure"), f"{context}.exposure")

    require(len(header_ids) == len(set(header_ids)), f"{path}: duplicate header family id")
    require(len(headers) == len(set(headers)), f"{path}: duplicate family header")

    builtin_ids: list[str] = []
    builtin_names: list[str] = []
    for family_index, raw_family in enumerate(builtin_families):
        context = f"{path}: builtin_families[{family_index}]"
        family = require_mapping(raw_family, context)
        family_id = require_string(family.get("id"), f"{context}.id")
        builtin_ids.append(family_id)
        require(family_id in BUILTIN_LAYOUTS, f"{context}.id: no table layout for {family_id!r}")
        require_string(family.get("caption"), f"{context}.caption")
        require_string(family.get("effect_heading"), f"{context}.effect_heading")

        builtins = require_list(family.get("builtins"), f"{context}.builtins")
        require(bool(builtins), f"{context}.builtins: expected at least one builtin")
        for builtin_index, raw_builtin in enumerate(builtins):
            builtin_context = f"{context}.builtins[{builtin_index}]"
            builtin = require_mapping(raw_builtin, builtin_context)
            name = require_string(builtin.get("name"), f"{builtin_context}.name")
            require(
                re.fullmatch(r"[a-z0-9_]+", name) is not None,
                f"{builtin_context}.name: invalid builtin suffix {name!r}",
            )
            builtin_names.append(name)
            require_string(builtin.get("c_interface"), f"{builtin_context}.c_interface")
            require_string(builtin.get("effect"), f"{builtin_context}.effect")
            lowering = require_mapping(builtin.get("lowering"), f"{builtin_context}.lowering")
            require(
                lowering.get("kind") in {"instruction", "description"},
                f"{builtin_context}.lowering.kind: expected 'instruction' or 'description'",
            )
            require_string(lowering.get("value"), f"{builtin_context}.lowering.value")

    require(len(builtin_ids) == len(set(builtin_ids)), f"{path}: duplicate builtin family id")
    require(
        builtin_ids == header_ids,
        f"{path}: builtin families must match header families in order",
    )
    require(len(builtin_names) == len(set(builtin_names)), f"{path}: duplicate builtin name")

    type_names: list[str] = []
    for index, raw_type in enumerate(shared_types):
        context = f"{path}: shared_types[{index}]"
        shared_type = require_mapping(raw_type, context)
        type_names.append(require_string(shared_type.get("name"), f"{context}.name"))
        contract = require_mapping(shared_type.get("contract"), f"{context}.contract")
        require(
            contract.get("kind") in {"text", "c_layout"},
            f"{context}.contract.kind: expected 'text' or 'c_layout'",
        )
        require_string(contract.get("value"), f"{context}.contract.value")
    require(len(type_names) == len(set(type_names)), f"{path}: duplicate shared type")


def builtin_tokens(text: str) -> set[str]:
    return set(re.findall(r"__builtin_bedrock_([A-Za-z0-9_]+)", text))


def included_headers(text: str) -> set[str]:
    return set(re.findall(r"(?m)^\s*#include\s+<([^>]+)>", text))


def validate_manifest_against_headers(
    manifest: dict[str, Any], header_root: Path = HEADER_ROOT
) -> None:
    expected_by_family = {
        family["id"]: {builtin["name"] for builtin in family["builtins"]}
        for family in manifest["builtin_families"]
    }

    expected_umbrella_members = {"public": set(), "system": set()}
    for family in manifest["header_families"]:
        family_id = family["id"]
        header_name = family["header"]
        header_path = header_root / header_name
        require(header_path.is_file(), f"{header_path}: target-intrinsic family header not found")
        actual = builtin_tokens(header_path.read_text(encoding="utf-8"))
        expected = expected_by_family[family_id]
        require(
            actual == expected,
            f"{header_path}: manifest/header builtin mismatch; "
            f"missing={sorted(actual - expected)}, extra={sorted(expected - actual)}",
        )
        expected_umbrella_members[family["umbrella"]].add(header_name)

    umbrella_headers = {
        "public": "bedrockintrin.h",
        "system": "bedrocksystemintrin.h",
    }
    for umbrella, header_name in umbrella_headers.items():
        path = header_root / header_name
        actual = included_headers(path.read_text(encoding="utf-8"))
        expected = expected_umbrella_members[umbrella]
        require(
            actual == expected,
            f"{path}: manifest/umbrella header mismatch; "
            f"missing={sorted(expected - actual)}, extra={sorted(actual - expected)}",
        )


def tex_plain(value: str) -> str:
    return tex_escape(value)


def tex_inline(value: str) -> str:
    parts = value.split("`")
    require(len(parts) % 2 == 1, f"unbalanced inline-code delimiter in {value!r}")
    return "".join(tex_code(part) if index % 2 else tex_plain(part) for index, part in enumerate(parts))


def generated_preamble(manifest_path: Path) -> list[str]:
    try:
        source = manifest_path.resolve().relative_to(ROOT)
    except ValueError:
        source = manifest_path
    return [
        f"% Generated from {source} by isa/tools/gen_target_intrinsics.py.",
        "% Do not edit this file directly.",
    ]


def render_fixed_longtable(
    manifest_path: Path,
    *,
    caption: str,
    headers: tuple[str, ...],
    widths: tuple[str, ...],
    rows: list[tuple[str, ...]],
) -> str:
    require(
        len(widths) == len(headers),
        f"{caption}: {len(widths)} widths for {len(headers)} columns",
    )
    for index, width in enumerate(widths):
        require(
            TABLE_WIDTH_RE.fullmatch(width) is not None,
            f"{caption}: invalid width for column {index}: {width!r}",
        )
    for index, row in enumerate(rows):
        require(
            len(row) == len(headers),
            f"{caption}: row {index} has {len(row)} cells; "
            f"expected {len(headers)}",
        )
    column_spec = "".join(f"p{{{width}}}" for width in widths)
    lines = generated_preamble(manifest_path) + [
        rf"\manualtablecaption{{{caption}}}",
        r"\begingroup\footnotesize",
        r"\setlength{\tabcolsep}{2pt}",
        rf"\begin{{longtable}}{{@{{}}{column_spec}@{{}}}}",
        r"\toprule",
        " & ".join(rf"\textbf{{{header}}}" for header in headers) + r"\\",
        r"\midrule",
        r"\endhead",
    ]
    lines.extend(" & ".join(row) + r"\\" for row in rows)
    lines.extend([r"\bottomrule", r"\end{longtable}", r"\endgroup", ""])
    return "\n".join(lines)


def render_header_families(manifest: dict[str, Any], manifest_path: Path) -> str:
    rows: list[tuple[str, ...]] = []
    for family in manifest["header_families"]:
        header = tex_code(f"<{family['header']}>")
        rows.append(
            (
                tex_plain(family["name"]),
                header,
                tex_plain(family["umbrella"]),
                tex_inline(family["exposure"]),
            )
        )
    return render_fixed_longtable(
        manifest_path,
        caption="Target Intrinsic Header Families",
        headers=("Family", "Header", "Umbrella", "Exposure"),
        widths=("1.15in", "1.65in", "0.65in", "2.15in"),
        rows=rows,
    )


def render_builtin_family(family: dict[str, Any], manifest_path: Path) -> str:
    widths = BUILTIN_LAYOUTS[family["id"]]
    rows: list[tuple[str, ...]] = []
    for builtin in family["builtins"]:
        lowering = builtin["lowering"]
        lowering_tex = (
            tex_code(lowering["value"])
            if lowering["kind"] == "instruction"
            else tex_plain(lowering["value"])
        )
        rows.append(
            (
                tex_code(builtin["name"]),
                tex_code(builtin["c_interface"]),
                lowering_tex,
                tex_inline(builtin["effect"]),
            )
        )
    return render_fixed_longtable(
        manifest_path,
        caption=tex_plain(family["caption"]),
        headers=(
            "Name",
            "C interface",
            "Lowering",
            tex_plain(family["effect_heading"]),
        ),
        widths=widths,
        rows=rows,
    )


def render_shared_types(manifest: dict[str, Any], manifest_path: Path) -> str:
    rows: list[tuple[str, ...]] = []
    for shared_type in manifest["shared_types"]:
        contract = shared_type["contract"]
        contract_tex = (
            tex_code(contract["value"])
            if contract["kind"] == "c_layout"
            else tex_inline(contract["value"])
        )
        rows.append((tex_code(shared_type["name"]), contract_tex))
    return render_fixed_longtable(
        manifest_path,
        caption="Target Intrinsic Shared Types",
        headers=("Type", "ABI contract"),
        widths=("2.05in", "3.45in"),
        rows=rows,
    )


def render_tables(manifest: dict[str, Any], manifest_path: Path = DEFAULT_MANIFEST) -> dict[str, str]:
    rendered = {"header_families.tex": render_header_families(manifest, manifest_path)}
    rendered.update(
        {
            f"{family['id']}.tex": render_builtin_family(family, manifest_path)
            for family in manifest["builtin_families"]
        }
    )
    rendered["shared_types.tex"] = render_shared_types(manifest, manifest_path)
    return rendered


def render_artifacts() -> dict[Path, str]:
    manifest = load_manifest(DEFAULT_MANIFEST)
    validate_manifest_against_headers(manifest)
    return {
        DEFAULT_OUTPUT_DIR / name: content
        for name, content in render_tables(manifest, DEFAULT_MANIFEST).items()
    }
