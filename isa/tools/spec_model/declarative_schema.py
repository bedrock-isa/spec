from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from .core import SpecError, UniqueKeyLoader, ValidationResult


CONTRACT_PATH = Path("schema/validation_contracts.yaml")


def validate_declarative_contracts(spec: dict[str, Any], result: ValidationResult) -> None:
    contract = load_contract(spec)
    if not contract:
        return
    validate_required_paths(spec, contract.get("required") or {}, result)
    validate_item_required(spec, contract.get("item_required") or [], result)
    validate_contains(spec, contract.get("contains") or [], result)
    validate_mapping_keys(spec, contract.get("mapping_keys") or [], result)
    validate_coverage(spec, contract.get("coverage") or [], result)


def load_contract(spec: dict[str, Any]) -> dict[str, Any]:
    root = spec.get("__dir__")
    if not isinstance(root, Path):
        root = Path(str(root))
    return load_contract_from_root(root)


def load_contract_from_root(root: Path, *, required: bool = False) -> dict[str, Any]:
    path = root / CONTRACT_PATH
    if not path.exists():
        if required:
            raise SpecError(f"{path} is required")
        return {}
    with path.open("r", encoding="utf-8") as fp:
        data = yaml.load(fp, Loader=UniqueKeyLoader)
    if data is None:
        return {}
    if not isinstance(data, dict):
        raise SpecError(f"{path} must contain a mapping")
    return data


def local_instruction_forms_required(contract: dict[str, Any]) -> list[str]:
    local = contract.get("local_instruction") or {}
    if not isinstance(local, dict):
        raise SpecError(f"{CONTRACT_PATH}: local_instruction must be a mapping")
    fields = local.get("forms_required") or []
    if not isinstance(fields, list) or not all(isinstance(field, str) for field in fields):
        raise SpecError(f"{CONTRACT_PATH}: local_instruction.forms_required must be a string list")
    return list(fields)


def path_value(root: Any, path: str) -> Any:
    matches = resolve_path(root, path)
    if not matches:
        return None
    return matches[0][1]


def validate_required_paths(spec: dict[str, Any], required: Any, result: ValidationResult) -> None:
    if not isinstance(required, dict):
        result.error(f"{CONTRACT_PATH}: required must be a mapping")
        return
    for item in required.get("mappings", []) or []:
        validate_required_path(spec, item, "mapping", result)
    for item in required.get("lists", []) or []:
        validate_required_path(spec, item, "list", result)


def validate_required_path(spec: dict[str, Any], item: Any, expected_kind: str, result: ValidationResult) -> None:
    if not isinstance(item, dict):
        result.error(f"{CONTRACT_PATH}: required.{expected_kind}s entries must be mappings")
        return
    path = str(item.get("path") or "")
    if not path:
        result.error(f"{CONTRACT_PATH}: required.{expected_kind}s entry is missing path")
        return
    matches = resolve_path(spec, path)
    value = matches[0][1] if matches else None
    if not present(value):
        result.error(f"{path} is required by {CONTRACT_PATH}")
        return
    if expected_kind == "mapping" and not isinstance(value, dict):
        result.error(f"{path} must be a mapping")
    if expected_kind == "list" and not isinstance(value, list):
        result.error(f"{path} must be a list")


def validate_item_required(spec: dict[str, Any], rules: Any, result: ValidationResult) -> None:
    if not isinstance(rules, list):
        result.error(f"{CONTRACT_PATH}: item_required must be a list")
        return
    for rule in rules:
        if not isinstance(rule, dict):
            result.error(f"{CONTRACT_PATH}: item_required entries must be mappings")
            continue
        path = str(rule.get("path") or "")
        fields = rule.get("fields") or []
        when = rule.get("when")
        if not path:
            result.error(f"{CONTRACT_PATH}: item_required entry is missing path")
            continue
        if not isinstance(fields, list) or not all(isinstance(field, str) for field in fields):
            result.error(f"{CONTRACT_PATH}: item_required.{path}.fields must be a string list")
            continue
        if when is not None and not isinstance(when, dict):
            result.error(f"{CONTRACT_PATH}: item_required.{path}.when must be a mapping")
            continue
        for item_path, item in resolve_path(spec, path):
            if not isinstance(item, dict):
                result.error(f"{item_path} must be a mapping")
                continue
            if isinstance(when, dict) and not all(item.get(key) == value for key, value in when.items()):
                continue
            for field in fields:
                if not present(item.get(field)):
                    result.error(f"{item_path}.{field} is required by {CONTRACT_PATH}")


def validate_contains(spec: dict[str, Any], rules: Any, result: ValidationResult) -> None:
    if not isinstance(rules, list):
        result.error(f"{CONTRACT_PATH}: contains must be a list")
        return
    for rule in rules:
        if not isinstance(rule, dict):
            result.error(f"{CONTRACT_PATH}: contains entries must be mappings")
            continue
        path = str(rule.get("path") or "")
        values = rule.get("values") or []
        if not path:
            result.error(f"{CONTRACT_PATH}: contains entry is missing path")
            continue
        if not isinstance(values, list) or not all(isinstance(value, str | int) for value in values):
            result.error(f"{CONTRACT_PATH}: contains.{path}.values must be a scalar list")
            continue
        observed = {str(value) for _path, value in resolve_path(spec, path)}
        missing = sorted(str(value) for value in values if str(value) not in observed)
        if missing:
            result.error(f"{path} must contain: " + ", ".join(missing))


def validate_mapping_keys(spec: dict[str, Any], rules: Any, result: ValidationResult) -> None:
    if not isinstance(rules, list):
        result.error(f"{CONTRACT_PATH}: mapping_keys must be a list")
        return
    for rule in rules:
        if not isinstance(rule, dict):
            result.error(f"{CONTRACT_PATH}: mapping_keys entries must be mappings")
            continue
        path = str(rule.get("path") or "")
        keys = rule.get("keys") or []
        if not path:
            result.error(f"{CONTRACT_PATH}: mapping_keys entry is missing path")
            continue
        if not isinstance(keys, list) or not all(isinstance(key, str | int) for key in keys):
            result.error(f"{CONTRACT_PATH}: mapping_keys.{path}.keys must be a scalar list")
            continue
        matches = resolve_path(spec, path)
        value = matches[0][1] if matches else None
        if not isinstance(value, dict):
            result.error(f"{path} must be a mapping")
            continue
        missing = sorted(str(key) for key in keys if key not in value)
        if missing:
            result.error(f"{path} is missing keys: " + ", ".join(missing))


def validate_coverage(spec: dict[str, Any], rules: Any, result: ValidationResult) -> None:
    if not isinstance(rules, list):
        result.error(f"{CONTRACT_PATH}: coverage must be a list")
        return
    for rule in rules:
        if not isinstance(rule, dict):
            result.error(f"{CONTRACT_PATH}: coverage entries must be mappings")
            continue
        target_path = str(rule.get("target") or "")
        source_paths = rule.get("sources") or []
        if not target_path:
            result.error(f"{CONTRACT_PATH}: coverage entry is missing target")
            continue
        if not isinstance(source_paths, list) or not all(isinstance(path, str) for path in source_paths):
            result.error(f"{CONTRACT_PATH}: coverage.{target_path}.sources must be a string list")
            continue
        target_matches = resolve_path(spec, target_path)
        target = target_matches[0][1] if target_matches else None
        if not isinstance(target, dict):
            result.error(f"{target_path} must be a mapping")
            continue
        source_values: set[str] = set()
        for source_path in source_paths:
            for _path, value in resolve_path(spec, source_path):
                if present(value):
                    source_values.add(str(value))
        missing = sorted(value for value in source_values if value not in target or not present(target.get(value)))
        if missing:
            result.error(f"{target_path} is missing entries for: " + ", ".join(missing))


def resolve_path(root: Any, path: str) -> list[tuple[str, Any]]:
    items: list[tuple[str, Any]] = [("", root)]
    for token in path.split("."):
        if not token:
            return []
        next_items: list[tuple[str, Any]] = []
        if token == "*":
            for label, value in items:
                if isinstance(value, dict):
                    for key, child in value.items():
                        next_items.append((join_path(label, str(key)), child))
            items = next_items
            continue
        if token.endswith("[]"):
            key = token[:-2]
            for label, value in items:
                if not isinstance(value, dict):
                    continue
                child = value.get(key)
                if not isinstance(child, list):
                    continue
                parent = join_path(label, key)
                for index, entry in enumerate(child):
                    next_items.append((f"{parent}[{index}]", entry))
            items = next_items
            continue
        for label, value in items:
            if isinstance(value, dict) and token in value:
                next_items.append((join_path(label, token), value[token]))
        items = next_items
    return items


def join_path(prefix: str, token: str) -> str:
    return token if not prefix else f"{prefix}.{token}"


def present(value: Any) -> bool:
    return value not in (None, "", [], {})
