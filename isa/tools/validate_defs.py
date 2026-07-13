#!/usr/bin/env python3
"""Validate instruction definition YAML files for the ISA rewrite."""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from pathlib import Path
import sys
from typing import Any

try:
    import yaml
except ImportError as exc:  # pragma: no cover - environment error path
    raise SystemExit("PyYAML is required to validate definition YAML files") from exc


ROOT = Path("isa/defs")

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
        for item in data.get("include", []):
            path = include.parent / item
            if not path.exists():
                errors.append(f"{include}: missing child include {item}")
                continue
            files.append(path)
    return files, errors


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

    mnemonics: dict[str, Path] = {}
    counts = Counter()
    operand_types = Counter()
    instruction_families = Counter()
    extension_families = Counter()
    legacy_operand_files: dict[str, set[Path]] = defaultdict(set)
    unknown_operand_files: dict[str, set[Path]] = defaultdict(set)
    missing_external_allocation: list[Path] = []
    fptransa_contracts: dict[int, tuple[str, Path]] = {}

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
            for family in scalar_list(doc.get("instruction_family")):
                instruction_families[family] += 1

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
                    operation_text = " ".join(str(item) for item in (behavior.get("operation") or []))
                    if "unbounded precision" in operation_text or "using FSTATUS.RM" in operation_text:
                        errors.append(f"{path}: correctly-rounded language remains in FPTRANSA operation")
                    if expected_id is not None and f"FPTRANSA_ACCURACY contract 0x{expected_id:04x}" not in operation_text:
                        errors.append(f"{path}: operation does not gate execution on its accuracy contract")
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

    summary = {
        "instruction_files": len(instruction_files),
        "instructions": counts["instructions"],
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
    for key in ("instruction_files", "instructions"):
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
