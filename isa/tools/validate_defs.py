#!/usr/bin/env python3
"""Validate instruction definition YAML files for the ISA rewrite."""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from pathlib import Path
import re
import sys
from typing import Any

try:
    import yaml
except ImportError as exc:  # pragma: no cover - environment error path
    raise SystemExit("PyYAML is required to validate definition YAML files") from exc


ROOT = Path("isa/defs")
INSTRUCTION_FILENAME = "instruction.yaml"
INSTRUCTION_DETAILS_FILENAME = "details.tex"
FORBIDDEN_BEHAVIOR_KEYS = {
    "operation",
    "operation_text",
    "operation_by_form",
    "fault_order",
    "fault_atomicity",
    "canonicalization",
    "descriptor_payloads",
}
EXPECTED_DETAILS_MNEMONICS = {
    "ADC", "SBB", "CLMUL", "CLMULH", "CMPXCHG", "DIVS", "DIVU", "MODS", "MODU",
    "DIVMODS", "DIVMODU", "ERET", "EXTRACT", "LCALL", "LJMP", "LRET", "POP", "PUSH",
    "POPP", "PUSHP", "PTQUERY", "REPG", "REPcc", "SAVE", "RESTORE", "SEGLEA", "SYSCALL",
    "SYSRET", "VTOP", "RDPMC", "FCLASS", "FCVT", "FCVTU", "FGETEXP", "FGETMAN", "FMOD",
    "FREM", "FSCALE", "FPOPP", "FPUSHP", "FACOSA", "FASINA", "FATANA", "FATANHA",
    "FCOSA", "FCOSHA", "FETOXA", "FETOXM1A", "FLOG10A", "FLOG2A", "FLOGNA", "FLOGNP1A",
    "FSINA", "FSINCOSA", "FSINHA", "FTANA", "FTANHA", "FTENTOXA", "FTWOTOXA", "ENCINST",
}

FPTRANSA_CONTRACT_IDS = {
    "FSINA": 0x0000,
    "FCOSA": 0x0001,
    "FTANA": 0x0002,
    "FSINCOSA": 0x0003,
    "FASINA": 0x0010,
    "FACOSA": 0x0011,
    "FATANA": 0x0012,
    "FSINHA": 0x0020,
    "FCOSHA": 0x0021,
    "FTANHA": 0x0022,
    "FATANHA": 0x0023,
    "FETOXA": 0x0030,
    "FETOXM1A": 0x0031,
    "FTWOTOXA": 0x0032,
    "FTENTOXA": 0x0033,
    "FLOGNA": 0x0040,
    "FLOGNP1A": 0x0041,
    "FLOG2A": 0x0042,
    "FLOG10A": 0x0043,
}


def load_yaml(path: Path) -> Any:
    with path.open() as f:
        return yaml.safe_load(f)


def scalar_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item) for item in value]
    return [str(value)]


def collect_operand_types(value: Any, out: Counter[str]) -> None:
    if isinstance(value, dict):
        typ = value.get("type")
        if isinstance(typ, str):
            out[typ] += 1
        for child in value.values():
            collect_operand_types(child, out)
    elif isinstance(value, list):
        for child in value:
            collect_operand_types(child, out)


def iter_instruction_files(root: Path, manifest: dict[str, Any]) -> tuple[list[Path], list[str]]:
    errors: list[str] = []
    files: list[Path] = []
    for spec in manifest.get("instruction_sets", []):
        include = root / spec["include"]
        if not include.exists():
            errors.append(f"missing include file: {include}")
            continue
        data = load_yaml(include)
        if not isinstance(data, dict):
            errors.append(f"{include}: expected mapping")
            continue
        common = data.get("common")
        if not isinstance(common, str) or not common.strip():
            errors.append(f"{include}: missing common metadata path")
        elif not (include.parent / common).is_file():
            errors.append(f"{include}: missing common metadata file {common}")
        include_items = data.get("include")
        if not isinstance(include_items, list):
            errors.append(f"{include}: include must be a list of instruction directories")
            continue
        for item in include_items:
            if not isinstance(item, str) or not item.strip():
                errors.append(f"{include}: instruction include entries must be non-empty strings")
                continue
            directory = include.parent / item
            if not directory.is_dir():
                errors.append(f"{include}: missing instruction directory {item}")
                continue
            path = directory / INSTRUCTION_FILENAME
            if not path.is_file():
                errors.append(f"{include}: missing instruction definition {item}/{INSTRUCTION_FILENAME}")
                continue
            files.append(path)
    return files, errors


def normalized_sentence(value: str) -> str:
    return " ".join(re.sub(r"[^A-Za-z0-9]+", " ", value).lower().split())


def forbidden_key_locations(value: Any, prefix: str = "") -> list[str]:
    locations: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            location = f"{prefix}.{key}" if prefix else str(key)
            if key in FORBIDDEN_BEHAVIOR_KEYS or key == "description_tex":
                locations.append(location)
            locations.extend(forbidden_key_locations(child, location))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            locations.extend(forbidden_key_locations(child, f"{prefix}[{index}]"))
    return locations


def validate_details_tex(path: Path) -> list[str]:
    if not path.exists():
        return []
    if not path.is_file():
        return [f"{path}: expected a regular details.tex file"]
    text = path.read_text(encoding="utf-8").strip()
    errors: list[str] = []
    if not text:
        errors.append(f"{path}: details.tex must not be empty")
    forbidden = (
        re.search(r"\\(?:sub)*section\s*(?!\*)\{", text)
        or re.search(r"\\addcontentsline\s*\{toc\}", text)
        or re.search(
            r"\\(?:input|include|documentclass)\b|\\begin\s*\{document\}|\\end\s*\{document\}",
            text,
        )
    )
    if forbidden:
        errors.append(f"{path}: details.tex contains a forbidden document-structure command")
    return errors


def validate_defs(root: Path = ROOT) -> tuple[dict[str, Any], list[str]]:
    manifest_path = root / "manifest.yaml"
    errors: list[str] = []
    if not manifest_path.exists():
        return {}, [f"missing manifest: {manifest_path}"]

    manifest = load_yaml(manifest_path)
    if not isinstance(manifest, dict):
        return {}, [f"{manifest_path}: expected mapping"]

    family_order = set(manifest.get("extension_grouping", {}).get("family_order", []))
    operands_path = root / "operands.yaml"
    operand_schema = load_yaml(operands_path) if operands_path.exists() else {}
    allowed_operand_types = set(
        (operand_schema.get("operand_schema", {}) if isinstance(operand_schema, dict) else {}).get("types", [])
    )
    instruction_files, include_errors = iter_instruction_files(root, manifest)
    errors.extend(include_errors)
    discovered_instruction_files = set(root.glob("**/instructions/*/instruction.yaml"))
    listed_instruction_files = set(instruction_files)
    discovered_instruction_dirs = {
        path for path in root.glob("**/instructions/*") if path.is_dir()
    }
    for path in sorted(discovered_instruction_files - listed_instruction_files):
        errors.append(f"{path}: instruction definition is not listed by a manifest")
    for path in sorted(listed_instruction_files - discovered_instruction_files):
        errors.append(f"{path}: listed instruction definition is outside the directory contract")
    if len(discovered_instruction_files) != 206:
        errors.append(f"expected 206 instruction.yaml files, found {len(discovered_instruction_files)}")
    if len(discovered_instruction_dirs) != 206:
        errors.append(f"expected 206 instruction directories, found {len(discovered_instruction_dirs)}")
    if discovered_instruction_dirs != {path.parent for path in discovered_instruction_files}:
        errors.append("instruction directories and instruction.yaml parents do not match exactly")

    mnemonics: dict[str, Path] = {}
    counts = Counter()
    operand_types = Counter()
    instruction_families = Counter()
    extension_families = Counter()
    legacy_operand_files: dict[str, set[Path]] = defaultdict(set)
    unknown_operand_files: dict[str, set[Path]] = defaultdict(set)
    missing_external_allocation: list[Path] = []
    fptransa_contracts: dict[int, tuple[str, Path]] = {}
    details_count = 0

    for path in instruction_files:
        data = load_yaml(path)
        if not isinstance(data, dict):
            errors.append(f"{path}: expected mapping")
            continue

        if "allocation" in data:
            errors.append(f"{path}: instruction definition still contains allocation block")

        mnemonic = data.get("mnemonic")
        if mnemonic is None:
            # Common include files are allowed to carry shared metadata.
            if path.name != "_common.yaml":
                errors.append(f"{path}: missing mnemonic")
            continue

        mnemonic = str(mnemonic)
        for location in forbidden_key_locations(data):
            errors.append(f"{path}: forbidden field {location}")
        if path.name != INSTRUCTION_FILENAME:
            errors.append(f"{path}: instruction definition must be named {INSTRUCTION_FILENAME}")
        if path.parent.name != mnemonic:
            errors.append(f"{path}: directory name must match mnemonic {mnemonic}")
        previous = mnemonics.get(mnemonic)
        if previous is not None:
            errors.append(f"duplicate mnemonic {mnemonic}: {previous} and {path}")
        mnemonics[mnemonic] = path
        counts["instructions"] += 1

        status = data.get("definition_status", {})
        if not isinstance(status, dict) or status.get("allocation") != "external: isa/alloc":
            missing_external_allocation.append(path)
        doc = data.get("doc", {})
        if isinstance(doc, dict):
            summary_text = doc.get("summary")
            if not isinstance(summary_text, str) or not summary_text.strip():
                errors.append(f"{path}: doc.summary must be a non-empty string")
            else:
                summary_text = " ".join(summary_text.split())
                if len(summary_text) > 120:
                    errors.append(f"{path}: doc.summary exceeds 120 characters")
                if len(re.findall(r"[.!?](?:\s|$)", summary_text)) != 1:
                    errors.append(f"{path}: doc.summary must contain exactly one sentence")
            description_text = doc.get("description")
            if not isinstance(description_text, str) or not description_text.strip():
                errors.append(f"{path}: doc.description must be a non-empty string")
            else:
                if "\n\n" in description_text.strip():
                    errors.append(f"{path}: doc.description must be a single paragraph")
                if isinstance(summary_text, str):
                    summary_norm = normalized_sentence(summary_text)
                    description_norm = normalized_sentence(description_text)
                    if summary_norm and description_norm.startswith(summary_norm):
                        errors.append(f"{path}: doc.description repeats doc.summary as its opening sentence")
            for family in scalar_list(doc.get("instruction_family")):
                instruction_families[family] += 1

        behavior = data.get("behavior", {})
        if not isinstance(behavior, dict):
            errors.append(f"{path}: behavior must be a mapping")
            behavior = {}
        details_path = path.with_name(INSTRUCTION_DETAILS_FILENAME)
        if details_path.exists():
            details_count += 1
            errors.extend(validate_details_tex(details_path))

        forms = data.get("forms", {})
        if isinstance(forms, dict):
            ext_family = forms.get("extension_family")
            if isinstance(ext_family, str):
                extension_families[ext_family] += 1
                if ext_family not in family_order:
                    errors.append(f"{path}: extension_family {ext_family!r} not present in manifest family_order")
                if ext_family == "fpu_transcendental_approx":
                    expected_id = FPTRANSA_CONTRACT_IDS.get(mnemonic)
                    if expected_id is None:
                        errors.append(f"{path}: unexpected FPTRANSA mnemonic {mnemonic}")
                    if forms.get("size") != "S_D":
                        errors.append(f"{path}: FPTRANSA instructions must support S and D together")
                    behavior = data.get("behavior") or {}
                    approximation = behavior.get("approximation") if isinstance(behavior, dict) else None
                    if not isinstance(approximation, dict):
                        errors.append(f"{path}: missing behavior.approximation contract")
                    else:
                        raw_contract_id = approximation.get("contract_id")
                        try:
                            contract_id = int(str(raw_contract_id), 0)
                        except (TypeError, ValueError):
                            errors.append(f"{path}: invalid FPTRANSA contract_id {raw_contract_id!r}")
                        else:
                            if expected_id is not None and contract_id != expected_id:
                                errors.append(
                                    f"{path}: contract_id 0x{contract_id:04x} does not match expected 0x{expected_id:04x}"
                                )
                            previous_contract = fptransa_contracts.get(contract_id)
                            if previous_contract is not None:
                                errors.append(
                                    f"duplicate FPTRANSA contract_id 0x{contract_id:04x}: "
                                    f"{previous_contract[1]} and {path}"
                                )
                            fptransa_contracts[contract_id] = (mnemonic, path)
                        if approximation.get("max_ulp") != {"S": 4, "D": 4}:
                            errors.append(f"{path}: FPTRANSA max_ulp must be S=4 and D=4")
                        for key in ("reference_function", "domain", "exact_anchors", "properties"):
                            if not approximation.get(key):
                                errors.append(f"{path}: approximation contract is missing {key}")
                    documentation_text = " ".join(
                        [
                            str(doc.get("description", "")),
                            details_path.read_text(encoding="utf-8") if details_path.is_file() else "",
                        ]
                    )
                    documentation_plain = documentation_text.replace(r"\_", "_")
                    if "unbounded precision" in documentation_text or "using FSTATUS.RM" in documentation_text:
                        errors.append(f"{path}: correctly-rounded language remains in FPTRANSA documentation")
                    if expected_id is not None and f"0x{expected_id:04x}" not in documentation_text:
                        errors.append(f"{path}: details do not identify FPTRANSA contract 0x{expected_id:04x}")
                    if "PRESENT" not in documentation_plain or "ILLEGAL_INSTRUCTION" not in documentation_plain:
                        errors.append(f"{path}: details do not define unavailable-contract handling")
                    fp_flags = data.get("attributes", {}).get("fp_flags", {})
                    updates = fp_flags.get("update", []) if isinstance(fp_flags, dict) else []
                    if "NX" in updates:
                        errors.append(f"{path}: FPTRANSA must leave NX unchanged")

        collect_operand_types(data, operand_types)
        file_operand_types = Counter()
        collect_operand_types(data, file_operand_types)
        for legacy in ("DREG", "AREG", "DBANK", "DREG_OR_AREG"):
            if file_operand_types[legacy]:
                legacy_operand_files[legacy].add(path)

        if allowed_operand_types:
            for typ in file_operand_types:
                if typ not in allowed_operand_types:
                    unknown_operand_files[typ].add(path)

    if missing_external_allocation:
        sample = ", ".join(str(path) for path in missing_external_allocation[:5])
        errors.append(
            f"{len(missing_external_allocation)} instruction files lack definition_status allocation marker: {sample}"
        )
    if legacy_operand_files:
        details = ", ".join(f"{key}={len(value)}" for key, value in sorted(legacy_operand_files.items()))
        errors.append(f"instruction files still use legacy operand types: {details}")
    if unknown_operand_files:
        details = ", ".join(f"{key}={len(value)}" for key, value in sorted(unknown_operand_files.items()))
        errors.append(f"instruction files use operand types not listed in operands.yaml: {details}")
    actual_fptransa = {mnemonic for mnemonic, _path in fptransa_contracts.values()}
    missing_fptransa = sorted(set(FPTRANSA_CONTRACT_IDS) - actual_fptransa)
    if missing_fptransa:
        errors.append("missing FPTRANSA contracts: " + " ".join(missing_fptransa))
    discovered_details_paths = set(root.glob("**/instructions/*/details.tex"))
    actual_details_mnemonics = {path.parent.name for path in discovered_details_paths}
    if actual_details_mnemonics != EXPECTED_DETAILS_MNEMONICS:
        missing = sorted(EXPECTED_DETAILS_MNEMONICS - actual_details_mnemonics)
        extra = sorted(actual_details_mnemonics - EXPECTED_DETAILS_MNEMONICS)
        errors.append(f"details.tex mnemonic set mismatch: missing={missing}, extra={extra}")
    if details_count != 60:
        errors.append(f"expected 60 details.tex files, found {details_count}")
    if len(discovered_details_paths) != 60:
        errors.append(f"expected 60 discovered details.tex files, found {len(discovered_details_paths)}")
    if any(path.parent not in discovered_instruction_dirs for path in discovered_details_paths):
        errors.append("details.tex found outside a valid instruction directory")

    summary = {
        "instruction_files": len(instruction_files),
        "instructions": counts["instructions"],
        "instruction_details": details_count,
        "instruction_families": dict(sorted(instruction_families.items())),
        "extension_families": dict(sorted(extension_families.items())),
        "operand_types": dict(sorted(operand_types.items())),
        "legacy_operand_files": {key: len(value) for key, value in sorted(legacy_operand_files.items())},
        "unknown_operand_files": {key: len(value) for key, value in sorted(unknown_operand_files.items())},
    }
    return summary, errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()

    summary, errors = validate_defs(args.root)

    print(f"{args.root}")
    for key in ("instruction_files", "instructions", "instruction_details"):
        print(f"  {key}: {summary.get(key, 0)}")
    print("  extension families:", len(summary.get("extension_families", {})))
    print("  instruction families:", len(summary.get("instruction_families", {})))
    legacy = summary.get("legacy_operand_files", {})
    if legacy:
        details = ", ".join(f"{key}={value}" for key, value in legacy.items())
        print(f"  legacy operand files: {details}")

    print(f"  errors: {len(errors)}")
    for error in errors[:40]:
        print(f"    {error}")
    if len(errors) > 40:
        print(f"    ... {len(errors) - 40} more")

    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
