#!/usr/bin/env python3
"""Generate retained ABI quick-reference tables from the ABI manifest."""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from pathlib import Path
import re
from typing import Any

import yaml

import abi_call_model
from latex_builder.common import tex_code


ROOT = Path(__file__).resolve().parents[2]
MANIFEST_PATH = ROOT / "isa" / "interfaces" / "abi" / "abi_tables.yaml"
CALL_CASES_PATH = ROOT / "isa" / "interfaces" / "abi" / "calling_convention_cases.json"
FRAGMENT_DIR = ROOT / "isa" / "interfaces" / "abi" / "generated"

FRAGMENT_NAMES = (
    "c_return_register_quick_reference.tex",
    "c_call_relocation_quick_reference.tex",
    "ordinary_memory_access_guarantees.tex",
    "native_atomic_primitive_quick_reference.tex",
    "elf_relocation_rows.tex",
    "tls_relocation_families.tex",
)

RETURN_CLASS_LABELS = {
    "general_scalar": "General scalar",
    "floating_point_scalar": "Floating-point scalar",
    "long_double_scalar": r"\texttt{long double} scalar",
    "complex_scalar": "Complex scalar",
    "int128_scalar": r"\texttt{\_\_int128} scalar",
    "small_aggregate": "Small aggregate",
    "large_aggregate": "Large aggregate",
}

CALL_FORM_LABELS = {
    "direct_c_call": "Direct C call",
    "external_plt_call": "External call through the PLT",
}
TABLE_WIDTH_RE = re.compile(r"^\d+(?:\.\d+)?(?:pt|in|cm|mm|em|ex)$")


class ManifestError(ValueError):
    """An ABI table manifest is malformed or internally inconsistent."""


def _mapping(value: Any, where: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise ManifestError(f"{where}: expected a mapping")
    return value


def _list(value: Any, where: str) -> list[Any]:
    if not isinstance(value, list):
        raise ManifestError(f"{where}: expected a list")
    return value


def _keys(value: Mapping[str, Any], required: set[str], optional: set[str], where: str) -> None:
    missing = required - set(value)
    unknown = set(value) - required - optional
    if missing:
        raise ManifestError(f"{where}: missing keys: {', '.join(sorted(missing))}")
    if unknown:
        raise ManifestError(f"{where}: unknown keys: {', '.join(sorted(unknown))}")


def _identifier(value: Any, where: str) -> str:
    if not isinstance(value, str) or not value:
        raise ManifestError(f"{where}: expected a non-empty string")
    return value


def _identifiers(value: Any, where: str) -> list[str]:
    result = [_identifier(item, f"{where}[]") for item in _list(value, where)]
    if not result:
        raise ManifestError(f"{where}: must not be empty")
    if len(result) != len(set(result)):
        raise ManifestError(f"{where}: duplicate values")
    return result


def _unique(values: Iterable[str], where: str) -> None:
    items = list(values)
    if len(items) != len(set(items)):
        raise ManifestError(f"{where}: duplicate values")


def _tt(value: str) -> str:
    return tex_code(value)


def load_manifest(path: Path = MANIFEST_PATH) -> Mapping[str, Any]:
    raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    manifest = _mapping(raw, str(path))
    validate_manifest(manifest)
    return manifest


def validate_manifest(manifest: Mapping[str, Any]) -> None:
    _keys(manifest, {"schema_version", "c_abi", "elf_abi"}, set(), "manifest")
    if manifest["schema_version"] != 0:
        raise ManifestError("manifest.schema_version: expected 0")

    c_abi = _mapping(manifest["c_abi"], "manifest.c_abi")
    _keys(
        c_abi,
        {
            "return_registers",
            "call_relocations",
            "ordinary_access_guarantees",
            "native_atomic_primitives",
        },
        set(),
        "manifest.c_abi",
    )
    returns = _list(c_abi["return_registers"], "manifest.c_abi.return_registers")
    return_classes: list[str] = []
    for index, raw_row in enumerate(returns):
        where = f"manifest.c_abi.return_registers[{index}]"
        row = _mapping(raw_row, where)
        _keys(row, {"result_class", "convention"}, set(), where)
        result_class = _identifier(row["result_class"], f"{where}.result_class")
        if result_class not in RETURN_CLASS_LABELS:
            raise ManifestError(f"{where}.result_class: unknown class {result_class!r}")
        return_classes.append(result_class)
        convention = _mapping(row["convention"], f"{where}.convention")
        kind = _identifier(convention.get("kind"), f"{where}.convention.kind")
        required_by_kind = {
            "single_register": {"kind", "register"},
            "complex_registers": {"kind", "real", "imaginary"},
            "register_pair": {"kind", "high", "low"},
            "sret_pointer": {"kind", "argument", "result"},
        }
        if kind not in required_by_kind:
            raise ManifestError(f"{where}.convention.kind: unknown kind {kind!r}")
        _keys(convention, required_by_kind[kind], set(), f"{where}.convention")
        for key in required_by_kind[kind] - {"kind"}:
            _identifier(convention[key], f"{where}.convention.{key}")
    _unique(return_classes, "manifest.c_abi.return_registers.result_class")

    calls = _list(c_abi["call_relocations"], "manifest.c_abi.call_relocations")
    call_forms: list[str] = []
    call_relocations: list[str] = []
    for index, raw_row in enumerate(calls):
        where = f"manifest.c_abi.call_relocations[{index}]"
        row = _mapping(raw_row, where)
        _keys(row, {"call_form", "relocation"}, set(), where)
        call_form = _identifier(row["call_form"], f"{where}.call_form")
        if call_form not in CALL_FORM_LABELS:
            raise ManifestError(f"{where}.call_form: unknown form {call_form!r}")
        call_forms.append(call_form)
        call_relocations.append(_identifier(row["relocation"], f"{where}.relocation"))
    _unique(call_forms, "manifest.c_abi.call_relocations.call_form")
    _unique(call_relocations, "manifest.c_abi.call_relocations.relocation")

    guarantees = _list(
        c_abi["ordinary_access_guarantees"],
        "manifest.c_abi.ordinary_access_guarantees",
    )
    for index, raw_row in enumerate(guarantees):
        where = f"manifest.c_abi.ordinary_access_guarantees[{index}]"
        row = _mapping(raw_row, where)
        _keys(row, {"access", "guarantee"}, set(), where)
        access = _mapping(row["access"], f"{where}.access")
        guarantee = _identifier(row["guarantee"], f"{where}.guarantee")
        if guarantee == "tear_free":
            _keys(access, {"alignment", "widths_bytes", "operations"}, set(), f"{where}.access")
            if access["alignment"] != "aligned" or access["widths_bytes"] != [1, 2, 4, 8]:
                raise ManifestError(f"{where}.access: tear-free baseline must be aligned 1/2/4/8-byte access")
            if access["operations"] != ["load", "store"]:
                raise ManifestError(f"{where}.access.operations: expected load and store")
        elif guarantee == "not_atomic":
            _keys(access, {"minimum_width_bytes"}, set(), f"{where}.access")
            if access["minimum_width_bytes"] != 16:
                raise ManifestError(f"{where}.access.minimum_width_bytes: expected 16")
        elif guarantee == "no_tear_free_guarantee":
            _keys(access, {"alignment"}, set(), f"{where}.access")
            if access["alignment"] != "unaligned":
                raise ManifestError(f"{where}.access.alignment: expected unaligned")
        else:
            raise ManifestError(f"{where}.guarantee: unknown guarantee {guarantee!r}")

    primitives = _list(
        c_abi["native_atomic_primitives"],
        "manifest.c_abi.native_atomic_primitives",
    )
    primitive_operations: list[str] = []
    for index, raw_row in enumerate(primitives):
        where = f"manifest.c_abi.native_atomic_primitives[{index}]"
        row = _mapping(raw_row, where)
        _keys(row, {"c_operations", "lowering"}, set(), where)
        operations = _identifiers(row["c_operations"], f"{where}.c_operations")
        primitive_operations.extend(operations)
        lowering = _mapping(row["lowering"], f"{where}.lowering")
        kind = _identifier(lowering.get("kind"), f"{where}.lowering.kind")
        if kind == "aligned_access_with_ordering":
            _keys(lowering, {"kind"}, set(), f"{where}.lowering")
        elif kind in {"width_matched_instruction", "instruction_loop"}:
            _keys(lowering, {"kind", "instruction"}, set(), f"{where}.lowering")
            _identifier(lowering["instruction"], f"{where}.lowering.instruction")
        else:
            raise ManifestError(f"{where}.lowering.kind: unknown kind {kind!r}")
    _unique(primitive_operations, "manifest.c_abi.native_atomic_primitives.c_operations")

    elf_abi = _mapping(manifest["elf_abi"], "manifest.elf_abi")
    _keys(
        elf_abi,
        {"relocations", "tls_relocation_families"},
        set(),
        "manifest.elf_abi",
    )
    relocations = _list(elf_abi["relocations"], "manifest.elf_abi.relocations")
    relocation_ids: list[int] = []
    relocation_names: list[str] = []
    for index, raw_row in enumerate(relocations):
        where = f"manifest.elf_abi.relocations[{index}]"
        row = _mapping(raw_row, where)
        _keys(row, {"id", "name", "size", "calculation"}, set(), where)
        relocation_id = row["id"]
        if not isinstance(relocation_id, int) or isinstance(relocation_id, bool):
            raise ManifestError(f"{where}.id: expected an integer")
        relocation_ids.append(relocation_id)
        name = _identifier(row["name"], f"{where}.name")
        if not name.startswith("R_BEDROCK_"):
            raise ManifestError(f"{where}.name: expected an R_BEDROCK_ name")
        relocation_names.append(name)
        _identifier(row["size"], f"{where}.size")
        _identifier(row["calculation"], f"{where}.calculation")
    if relocation_ids != list(range(len(relocation_ids))):
        raise ManifestError(
            "manifest.elf_abi.relocations.id: expected contiguous IDs from zero"
        )
    _unique(relocation_names, "manifest.elf_abi.relocations.name")

    families = _list(elf_abi["tls_relocation_families"], "manifest.elf_abi.tls_relocation_families")
    models: list[str] = []
    tls_relocations: list[str] = []
    for index, raw_row in enumerate(families):
        where = f"manifest.elf_abi.tls_relocation_families[{index}]"
        row = _mapping(raw_row, where)
        _keys(row, {"model", "relocations"}, set(), where)
        models.append(_identifier(row["model"], f"{where}.model"))
        tls_relocations.extend(_identifiers(row["relocations"], f"{where}.relocations"))
    _unique(models, "manifest.elf_abi.tls_relocation_families.model")
    _unique(tls_relocations, "manifest.elf_abi.tls_relocation_families.relocations")


def referenced_relocations(manifest: Mapping[str, Any]) -> set[str]:
    c_abi = manifest["c_abi"]
    elf_abi = manifest["elf_abi"]
    names = {row["relocation"] for row in c_abi["call_relocations"]}
    for family in elf_abi["tls_relocation_families"]:
        names.update(family["relocations"])
    return names


def validate_relocation_relationships(manifest: Mapping[str, Any]) -> None:
    defined = {row["name"] for row in manifest["elf_abi"]["relocations"]}
    missing = sorted(referenced_relocations(manifest) - defined)
    if missing:
        raise ManifestError(
            "ABI table manifest references undefined ELF relocations: " + ", ".join(missing)
        )


def _return_rule(convention: Mapping[str, Any]) -> str:
    kind = convention["kind"]
    if kind == "single_register":
        return _tt(convention["register"])
    if kind == "complex_registers":
        return f"real component in {_tt(convention['real'])}, imaginary component in {_tt(convention['imaginary'])}"
    if kind == "register_pair":
        return _tt(f"{convention['high']}:{convention['low']}")
    if kind == "sret_pointer":
        return f"sret pointer in {_tt(convention['argument'])}, result pointer returned in {_tt(convention['result'])}"
    raise AssertionError(kind)


def _render_returns(rows: list[Mapping[str, Any]]) -> list[tuple[str, str]]:
    return [
        (RETURN_CLASS_LABELS[row["result_class"]], _return_rule(row["convention"]))
        for row in rows
    ]


def _render_calls(rows: list[Mapping[str, Any]]) -> list[tuple[str, str]]:
    return [
        (CALL_FORM_LABELS[row["call_form"]], _tt(row["relocation"]))
        for row in rows
    ]


def _render_access_guarantees(
    rows: list[Mapping[str, Any]],
) -> list[tuple[str, str]]:
    rendered: list[tuple[str, str]] = []
    for row in rows:
        guarantee = row["guarantee"]
        if guarantee == "tear_free":
            access = "Aligned 1/2/4/8-byte load or store"
            result = "tear-free"
        elif guarantee == "not_atomic":
            access = "Access of 16 bytes or more"
            result = "not atomic"
        else:
            access = "Unaligned access"
            result = "no tear-free guarantee"
        rendered.append((access, result))
    return rendered


def _render_atomic_primitives(
    rows: list[Mapping[str, Any]],
) -> list[tuple[str, str]]:
    operation_labels = {
        ("load", "store"): "Atomic load or store",
        ("compare_exchange",): "Compare-exchange",
        ("exchange",): "Exchange",
    }
    rendered: list[tuple[str, str]] = []
    for row in rows:
        operations = tuple(row["c_operations"])
        lowering = row["lowering"]
        if lowering["kind"] == "aligned_access_with_ordering":
            primitive = "ordinary aligned tear-free access plus the required ordering sequence"
        elif lowering["kind"] == "width_matched_instruction":
            primitive = f"width-matched {_tt(lowering['instruction'])}"
        else:
            primitive = f"compare-exchange loop using {_tt(lowering['instruction'])}"
        rendered.append((operation_labels[operations], primitive))
    return rendered


def _render_relocations(rows: list[Mapping[str, Any]]) -> str:
    rendered: list[tuple[str, str, str, str]] = []
    for row in rows:
        name = _tt(row["name"]).replace(r"\_", r"\_\allowbreak{}")
        rendered.append(
            (
                str(row["id"]),
                name,
                tex_code(row["size"]),
                tex_code(row["calculation"]),
            )
        )
    return _serialize_rows(rendered, 4, "ELF relocation rows")


def _render_call_case_registry(case_ids: Iterable[str]) -> str:
    identifiers = sorted(case_ids)
    definitions = [
        rf"\expandafter\def\csname bedrockabicase@known@{identifier}\endcsname{{}}"
        for identifier in identifiers
    ]
    completeness_checks = [
        (
            rf"\ifcsname bedrockabicase@seen@{identifier}\endcsname\else"
            rf"\PackageError{{bedrock-reference}}"
            rf"{{Missing ABI calling-convention case `{identifier}'}}"
            r"{Reference every documented calling-convention case with "
            r"\string\manualabicase.}\fi"
        )
        for identifier in identifiers
    ]
    return "\n".join(
        [
            *definitions,
            r"\newcommand{\manualabicase}[1]{%",
            r"  \ifcsname bedrockabicase@known@#1\endcsname",
            r"    \expandafter\gdef\csname bedrockabicase@seen@#1\endcsname{}%",
            r"  \else",
            r"    \PackageError{bedrock-reference}{Unknown ABI calling-convention case `#1'}%",
            r"      {Use an ID declared in isa/interfaces/abi/calling_convention_cases.json.}%",
            r"  \fi}",
            r"\AtEndDocument{%",
            *completeness_checks,
            r"}",
            "",
        ]
    )


def _render_tls(rows: list[Mapping[str, Any]]) -> list[tuple[str, str]]:
    model_labels = {"local_exec": "local-exec", "tlsdesc": "TLSDESC"}
    rendered: list[tuple[str, str]] = []
    for row in rows:
        relocations = r"\\".join(_tt(name) for name in row["relocations"])
        rendered.append(
            (
                model_labels[row["model"]],
                r"\begin{tabular}[t]{@{}l@{}}"
                + relocations
                + r"\end{tabular}",
            )
        )
    return rendered


def _serialize_rows(
    rows: Iterable[tuple[str, ...]],
    column_count: int,
    context: str,
) -> str:
    rendered: list[str] = []
    for index, row in enumerate(rows):
        if len(row) != column_count:
            raise ManifestError(
                f"{context}: row {index} has {len(row)} cells; "
                f"expected {column_count}"
            )
        rendered.append(" & ".join(row) + "\\\\\n")
    return "".join(rendered)


def _table_fragment(
    *,
    caption: str,
    widths: tuple[str, ...],
    headers: tuple[str, ...],
    rows: list[tuple[str, ...]],
    environment: str = "longtable",
    compact: bool = False,
) -> str:
    if len(widths) != len(headers):
        raise ManifestError(
            f"{caption}: {len(widths)} widths for {len(headers)} columns"
        )
    for index, width in enumerate(widths):
        if TABLE_WIDTH_RE.fullmatch(width) is None:
            raise ManifestError(f"{caption}: invalid width for column {index}: {width!r}")
    columns = "@{}" + "".join(f"p{{{width}}}" for width in widths) + "@{}"
    rendered_rows = _serialize_rows(rows, len(headers), caption)
    prefix = f"\\manualtablecaption{{{caption}}}\n"
    suffix = ""
    if compact:
        prefix += "\\begingroup\\footnotesize\n\\setlength{\\tabcolsep}{2pt}\n"
        suffix = "\\endgroup\n"
    header_row = " & ".join(rf"\textbf{{{header}}}" for header in headers)
    return (
        prefix
        + rf"\begin{{{environment}}}{{{columns}}}"
        + "\n\\toprule\n"
        + header_row
        + "\\\\\n\\midrule\n\\endhead\n"
        + rendered_rows
        + "\\bottomrule\n"
        + rf"\end{{{environment}}}"
        + "\n"
        + suffix
    )


def render_fragments(
    manifest: Mapping[str, Any], documented_call_cases: Iterable[str]
) -> dict[str, str]:
    validate_manifest(manifest)
    validate_relocation_relationships(manifest)
    c_abi = manifest["c_abi"]
    elf_abi = manifest["elf_abi"]
    generated_header = (
        "% Generated by isa/tools/gen_abi_tables.py. Do not edit.\n"
        "% Source: isa/interfaces/abi/abi_tables.yaml\n"
    )
    bodies = {
        "c_return_register_quick_reference.tex": (
            _render_call_case_registry(documented_call_cases)
            + _table_fragment(
                caption="C Return Register Quick Reference",
                widths=("2.15in", "3.35in"),
                headers=("Result Class", "Register Rule"),
                rows=_render_returns(c_abi["return_registers"]),
                compact=True,
            )
        ),
        "c_call_relocation_quick_reference.tex": _table_fragment(
            caption="C Call Relocation Quick Reference",
            widths=("2.15in", "3.25in"),
            headers=("Call form", "Relocation"),
            rows=_render_calls(c_abi["call_relocations"]),
            environment="manuallongtable",
        ),
        "ordinary_memory_access_guarantees.tex": _table_fragment(
            caption="Ordinary Normal-Memory Access Guarantees",
            widths=("2.75in", "2.65in"),
            headers=("Access", "Guarantee"),
            rows=_render_access_guarantees(c_abi["ordinary_access_guarantees"]),
            environment="manuallongtable",
        ),
        "native_atomic_primitive_quick_reference.tex": _table_fragment(
            caption="Native Atomic Primitive Quick Reference",
            widths=("2.15in", "3.25in"),
            headers=("C operation", "Bedrock primitive"),
            rows=_render_atomic_primitives(c_abi["native_atomic_primitives"]),
            environment="manuallongtable",
        ),
        "elf_relocation_rows.tex": (
            "\\newcommand{\\bedrockelfrelocationrows}{%\n"
            + _render_relocations(elf_abi["relocations"])
            + "}\n"
        ),
        "tls_relocation_families.tex": _table_fragment(
            caption="TLS Relocation Families",
            widths=("1.25in", "4.25in"),
            headers=("Model", "Relocations"),
            rows=_render_tls(elf_abi["tls_relocation_families"]),
            compact=True,
        ),
    }
    return {name: generated_header + bodies[name] for name in FRAGMENT_NAMES}


def render_artifacts() -> dict[Path, str]:
    manifest = load_manifest()
    documented_call_cases = abi_call_model.validate_cases(CALL_CASES_PATH)
    return {
        FRAGMENT_DIR / name: content
        for name, content in render_fragments(
            manifest, documented_call_cases
        ).items()
    }
