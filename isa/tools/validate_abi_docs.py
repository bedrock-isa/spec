#!/usr/bin/env python3
"""Validate cross-source ABI and compiler-interface consistency."""

from __future__ import annotations

from pathlib import Path
import re

import abi_call_model
from defs_loader import load_yaml


ROOT = Path(__file__).resolve().parents[2]
HEADER_ROOT = ROOT / "isa" / "c" / "include"
REGISTER_DEFS = ROOT / "isa" / "defs" / "registers.yaml"
CALL_CASES = ROOT / "isa" / "abi" / "calling_convention_cases.json"
CONTROL_REGISTER_REFERENCE = (
    ROOT
    / "isa"
    / "tools"
    / "latex_builder"
    / "templates"
    / "fragments"
    / "control_register_reference.tex"
)


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


def validate_relocations() -> None:
    path = ROOT / "isa" / "abi" / "bedrock-elf-abi.tex"
    text = normalize_tex(path.read_text(encoding="utf-8"))
    rows = re.findall(r"(?m)^(\d+)\s*&\s*\\texttt\{(R_BEDROCK_[A-Z0-9_]+)\}", text)
    ids = [int(item[0]) for item in rows]
    names = [item[1] for item in rows]
    require(ids, f"{path}: no relocation entries found")
    require(ids == list(range(len(ids))), f"{path}: relocation IDs must be contiguous from zero; found {ids}")
    require(len(names) == len(set(names)), f"{path}: duplicate relocation names")


def builtin_tokens(text: str) -> set[str]:
    return {
        token
        for token in re.findall(r"__builtin_bedrock_[A-Za-z0-9_]+", normalize_tex(text))
        if token != "__builtin_bedrock_"
    }


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
    document_path = ROOT / "isa" / "c" / "bedrock-target-intrinsics.tex"
    document = document_path.read_text(encoding="utf-8")
    suffixes = re.findall(r"\\compilerbuiltin\{([a-z0-9_]+)\}", document)
    require(len(suffixes) == len(set(suffixes)), f"{document_path}: duplicate target builtin entry")
    documented = {f"__builtin_bedrock_{suffix}" for suffix in suffixes}

    declared: set[str] = set()
    for header in sorted(HEADER_ROOT.glob("*.h")):
        declared.update(builtin_tokens(header.read_text(encoding="utf-8")))

    missing = sorted(declared - documented)
    extra = sorted(documented - declared)
    require(not missing, f"{document_path}: missing header builtins: {', '.join(missing)}")
    require(not extra, f"{document_path}: documents undefined builtins: {', '.join(extra)}")

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

    reference = CONTROL_REGISTER_REFERENCE.read_text(encoding="utf-8")
    documented_selectors = {
        name: int(value, 16)
        for value, name in re.findall(
            r"\\texttt\{0x([0-9A-Fa-f]+)\}\s*&\s*\\texttt\{([A-Z0-9]+)\}",
            reference,
        )
    }
    require(
        documented_selectors == header_selectors,
        f"{CONTROL_REGISTER_REFERENCE}: selector table does not match {header_path}",
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
    validate_relocations()
    validate_target_intrinsics()
    validate_control_register_reference()
    validate_calling_convention_model()
    print("Document validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
