#!/usr/bin/env python3
"""Validate cross-source ABI and compiler-interface consistency."""

from __future__ import annotations

import argparse
from pathlib import Path
import re

import abi_call_model
from defs_loader import load_yaml


ROOT = Path(__file__).resolve().parents[2]
HEADER_ROOT = ROOT / "isa" / "interfaces" / "c" / "include"
REGISTER_DEFS = ROOT / "isa" / "instructions" / "definitions" / "registers.yaml"
CALL_CASES = ROOT / "isa" / "interfaces" / "abi" / "calling_convention_cases.json"
C_ABI_DOCUMENT = ROOT / "isa" / "interfaces" / "abi" / "bedrock-c-abi.tex"
DOCUMENTED_CALL_CASE_REGISTRY = (
    ROOT
    / "isa"
    / "interfaces"
    / "abi"
    / "c"
    / "documented_calling_convention_case_registry.tex"
)
KNOWN_CALL_CASE_RE = re.compile(r"bedrockabicase@known@([a-z0-9-]+)\\endcsname")
CALL_CASE_REFERENCE_RE = re.compile(r"\\manualabicase\s*\{([^{}]+)\}")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def segment_selectors_from_metadata() -> dict[str, int]:
    data = load_yaml(REGISTER_DEFS)
    groups = data.get("registers") or {}
    entries = (groups.get("segment") or {}).get("entries") or []
    return {
        str(entry["name"]): int(entry["encoding"])
        for entry in entries
        if entry.get("encoding") is not None
    }


def validate_segment_selector_interface() -> None:
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


def validate_calling_convention_model() -> None:
    documented = abi_call_model.validate_cases(CALL_CASES)
    registry = set(
        KNOWN_CALL_CASE_RE.findall(
            DOCUMENTED_CALL_CASE_REGISTRY.read_text(encoding="utf-8")
        )
    )
    references = set(
        CALL_CASE_REFERENCE_RE.findall(C_ABI_DOCUMENT.read_text(encoding="utf-8"))
    )
    require(
        registry == documented,
        f"{DOCUMENTED_CALL_CASE_REGISTRY}: calling-convention case registry does not match "
        f"documented cases in {CALL_CASES}; missing={sorted(documented - registry)}, "
        f"extra={sorted(registry - documented)}",
    )
    require(
        references == documented,
        f"{C_ABI_DOCUMENT}: calling-convention case references do not match "
        f"documented cases in {CALL_CASES}; missing={sorted(documented - references)}, "
        f"extra={sorted(references - documented)}",
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    validate_segment_selector_interface()
    validate_calling_convention_model()
    print("Document validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
