#!/usr/bin/env python3
"""Validate cross-source ABI and compiler-interface consistency."""

from __future__ import annotations

from pathlib import Path
import re

import abi_call_model
from defs_loader import load_yaml
import gen_abi_tables
import gen_architecture_tables
import gen_target_intrinsics


ROOT = Path(__file__).resolve().parents[2]
HEADER_ROOT = ROOT / "isa" / "c" / "include"
REGISTER_DEFS = ROOT / "isa" / "defs" / "registers.yaml"
CALL_CASES = ROOT / "isa" / "abi" / "calling_convention_cases.json"


def normalize_tex(text: str) -> str:
    return (
        text.replace(r"\_\allowbreak{}", "_")
        .replace(r"\_", "_")
        .replace(r"\allowbreak{}", "")
        .replace(r"\textless{}", "<")
        .replace(r"\textgreater{}", ">")
    )


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def validate_relocations() -> set[str]:
    path = ROOT / "isa" / "abi" / "bedrock-elf-abi.tex"
    text = normalize_tex(path.read_text(encoding="utf-8"))
    rows = re.findall(r"(?m)^(\d+)\s*&\s*\\texttt\{(R_BEDROCK_[A-Z0-9_]+)\}", text)
    ids = [int(item[0]) for item in rows]
    names = [item[1] for item in rows]
    require(ids, f"{path}: no relocation entries found")
    require(ids == list(range(len(ids))), f"{path}: relocation IDs must be contiguous from zero; found {ids}")
    require(len(names) == len(set(names)), f"{path}: duplicate relocation names")
    return set(names)


def validate_generated_abi_tables(defined_relocations: set[str]) -> None:
    manifest = gen_abi_tables.load_manifest()
    gen_abi_tables.validate_relocation_relationships(manifest, defined_relocations)
    stale = gen_abi_tables.check_fragments(manifest)
    require(
        not stale,
        "generated ABI table fragments are stale: "
        + ", ".join(str(path) for path in stale),
    )


def segment_selectors_from_metadata() -> dict[str, int]:
    data = load_yaml(REGISTER_DEFS)
    groups = data.get("registers") or {}
    entries = (groups.get("segment") or {}).get("entries") or []
    return {
        str(entry["name"]): int(entry["encoding"])
        for entry in entries
        if entry.get("encoding") is not None
    }


def validate_target_intrinsics() -> None:
    manifest = gen_target_intrinsics.load_manifest()
    gen_target_intrinsics.validate_manifest_against_headers(manifest, HEADER_ROOT)
    gen_target_intrinsics.check_tables(
        gen_target_intrinsics.render_tables(manifest),
        gen_target_intrinsics.DEFAULT_OUTPUT_DIR,
    )

    header_path = HEADER_ROOT / "bedrocksysregintrin.h"
    header = header_path.read_text(encoding="utf-8")
    header_selectors = {
        name: int(value)
        for name, value in re.findall(r"__BEDROCK_SEG_([A-Z0-9]+)\s*=\s*(\d+)", header)
    }
    metadata_selectors = segment_selectors_from_metadata()
    require(
        header_selectors == metadata_selectors,
        f"{header_path}: segment-register selector set does not match {REGISTER_DEFS}",
    )


def validate_control_register_reference() -> None:
    header_path = HEADER_ROOT / "bedrocksysregintrin.h"
    header = header_path.read_text(encoding="utf-8")
    header_selectors = {
        name: int(value, 16)
        for name, value in re.findall(r"__BEDROCK_CR_([A-Z0-9]+)\s*=\s*0x([0-9A-Fa-f]+)", header)
    }

    manifest = gen_architecture_tables.load_mapping(gen_architecture_tables.SOURCE)
    gen_architecture_tables.validate_manifest(manifest)
    stale = gen_architecture_tables.generate(check=True)
    require(
        not stale,
        "generated architecture table fragments are stale: "
        + ", ".join(str(path) for path in stale),
    )
    documented_selectors = {
        str(entry["name"]): int(entry["selector"])
        for entry in manifest["control_registers"]
    }
    require(
        documented_selectors == header_selectors,
        f"{gen_architecture_tables.SOURCE}: control-register selectors do not match {header_path}",
    )


def validate_calling_convention_model() -> None:
    documented_cases = abi_call_model.validate_cases(CALL_CASES)
    c_abi_path = ROOT / "isa" / "abi" / "bedrock-c-abi.tex"
    c_abi = c_abi_path.read_text(encoding="utf-8")
    markers = re.findall(r"(?m)^% ABI-CALL-CASE: ([a-z0-9-]+)$", c_abi)
    require(len(markers) == len(set(markers)), f"{c_abi_path}: duplicate ABI call-case marker")
    marker_set = set(markers)
    missing = sorted(documented_cases - marker_set)
    extra = sorted(marker_set - documented_cases)
    require(not missing, f"{c_abi_path}: missing documented call cases: {', '.join(missing)}")
    require(not extra, f"{c_abi_path}: unknown documented call cases: {', '.join(extra)}")


def main() -> int:
    defined_relocations = validate_relocations()
    validate_generated_abi_tables(defined_relocations)
    validate_target_intrinsics()
    validate_control_register_reference()
    validate_calling_convention_model()
    print("Document validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
