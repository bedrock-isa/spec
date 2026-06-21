from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable

try:
    import yaml
except ImportError as exc:  # pragma: no cover - exercised only on incomplete hosts
    raise SystemExit("PyYAML is required: python3 -m pip install pyyaml") from exc

class SpecError(ValueError):
    pass


class UniqueKeyLoader(yaml.SafeLoader):
    """YAML loader that rejects duplicate mapping keys."""


def construct_unique_mapping(loader: UniqueKeyLoader, node: yaml.nodes.MappingNode, deep: bool = False) -> dict[Any, Any]:
    loader.flatten_mapping(node)
    mapping: dict[Any, Any] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in mapping:
            mark = key_node.start_mark
            raise SpecError(f"{mark.name}:{mark.line + 1}:{mark.column + 1}: duplicate YAML key {key!r}")
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


UniqueKeyLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, construct_unique_mapping)


@dataclass(frozen=True)
class Pattern:
    raw: str
    width: int
    mask: int
    value: int
    fields: dict[str, int] = field(default_factory=dict)

    @property
    def fixed_bits(self) -> int:
        return self.mask.bit_count()

    @property
    def word_count(self) -> int:
        return (self.width + 15) // 16

    def mask_hex(self) -> str:
        return f"0x{self.mask:0{max(1, (self.width + 3) // 4)}x}"

    def value_hex(self) -> str:
        return f"0x{self.value:0{max(1, (self.width + 3) // 4)}x}"


@dataclass
class PatternEntry:
    id: str
    kind: str
    source: dict[str, Any]
    pattern: Pattern

    @property
    def mnemonic(self) -> str:
        return str(self.source.get("mnemonic") or self.source.get("name") or self.id)


@dataclass
class ValidationResult:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    infos: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors

    def error(self, message: str) -> None:
        self.errors.append(message)

    def warn(self, message: str) -> None:
        self.warnings.append(message)

    def info(self, message: str) -> None:
        self.infos.append(message)


class KeySchema:
    """Base class for one closed YAML object shape."""

    name = "schema"
    keys: Iterable[str] = ()

    def __init_subclass__(cls) -> None:
        cls.keys = frozenset(str(key) for key in cls.keys)

    @classmethod
    def key_set(cls) -> set[str]:
        return set(cls.keys)

    @classmethod
    def unknown_keys(cls, value: dict[Any, Any]) -> list[str]:
        return sorted(str(key) for key in value if str(key) not in cls.keys)

    @classmethod
    def unused_keys(cls, used: Iterable[str]) -> list[str]:
        return sorted(cls.keys - {str(key) for key in used})

    @classmethod
    def validate_mapping(cls, value: Any, path: str, errors: list[str]) -> None:
        check_allowed_keys(value, path, cls, errors)

    @classmethod
    def validate_mapping_values(cls, value: Any, path: str, errors: list[str]) -> None:
        check_mapping_values(value, path, cls, errors)

    @classmethod
    def validate_list_items(cls, value: Any, path: str, errors: list[str]) -> None:
        check_list_items(value, path, cls, errors)

    @classmethod
    def validate(cls, value: Any, path: str, errors: list[str]) -> None:
        check_allowed_keys(value, path, cls, errors)


def schema_keys(schema: Any) -> set[str]:
    if isinstance(schema, type) and issubclass(schema, KeySchema):
        return schema.key_set()
    raise TypeError(f"schema must be a KeySchema class, got {type(schema).__name__}")


def is_scalar_value(value: Any) -> bool:
    return value is None or isinstance(value, str | int | float | bool)


def check_allowed_keys(
    value: Any,
    path: str,
    allowed: type[KeySchema],
    errors: list[str],
) -> None:
    if not isinstance(value, dict):
        errors.append(f"{path} must be a mapping")
        return
    allowed_keys = schema_keys(allowed)
    unknown = sorted(str(key) for key in value if str(key) not in allowed_keys)
    if unknown:
        errors.append(f"{path} contains unknown keys: {', '.join(unknown)}")


def check_mapping_values(
    value: Any,
    path: str,
    allowed: type[KeySchema],
    errors: list[str],
) -> None:
    if not isinstance(value, dict):
        errors.append(f"{path} must be a mapping")
        return
    for key, item in value.items():
        if isinstance(item, dict):
            allowed.validate(item, f"{path}.{key}", errors)


def check_list_items(
    value: Any,
    path: str,
    allowed: type[KeySchema],
    errors: list[str],
) -> None:
    if not isinstance(value, list):
        errors.append(f"{path} must be a list")
        return
    for index, item in enumerate(value):
        if isinstance(item, dict):
            allowed.validate(item, f"{path}[{index}]", errors)


def check_optional_mapping(
    value: Any,
    path: str,
    allowed: type[KeySchema],
    errors: list[str],
) -> None:
    if value is None:
        return
    allowed.validate(value, path, errors)


def check_mapping_item_keys(
    value: Any,
    path: str,
    allowed: type[KeySchema],
    errors: list[str],
) -> None:
    if value is None:
        return
    check_mapping_values(value, path, allowed, errors)


def check_list_item_keys(
    value: Any,
    path: str,
    allowed: type[KeySchema],
    errors: list[str],
) -> None:
    if value is None:
        return
    check_list_items(value, path, allowed, errors)
