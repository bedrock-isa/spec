#!/usr/bin/env python3
"""Validate cross-source ABI and compiler-interface consistency."""

from __future__ import annotations

import argparse
from pathlib import Path
import re

import abi_call_model
from defs_loader import load_yaml
import gen_abi_tables
import gen_architecture_tables
import gen_target_intrinsics


ROOT = Path(__file__).resolve().parents[2]
HEADER_ROOT = ROOT / "isa" / "interfaces" / "c" / "include"
REGISTER_DEFS = ROOT / "isa" / "instructions" / "definitions" / "registers.yaml"
CALL_CASES = ROOT / "isa" / "interfaces" / "abi" / "calling_convention_cases.json"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def validate_abi_manifest() -> None:
    manifest = gen_abi_tables.load_manifest()
    gen_abi_tables.validate_relocation_relationships(manifest)


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
    documented_selectors = {
        str(entry["name"]): int(entry["selector"])
        for entry in manifest["control_registers"]
    }
    require(
        documented_selectors == header_selectors,
        f"{gen_architecture_tables.SOURCE}: control-register selectors do not match {header_path}",
    )


def validate_calling_convention_model() -> None:
    abi_call_model.validate_cases(CALL_CASES)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    validate_abi_manifest()
    validate_target_intrinsics()
    validate_control_register_reference()
    validate_calling_convention_model()
    print("Document validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
