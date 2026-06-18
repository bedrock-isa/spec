from __future__ import annotations

from typing import Any
import re

from .core import SpecError


def int_value(value: Any) -> int:
    if isinstance(value, int):
        return value
    return int(str(value), 0)


def require_mapping(value: Any, path: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise SpecError(f"{path} must be a mapping")
    return value


def require_list(value: Any, path: str) -> list[Any]:
    if not isinstance(value, list):
        raise SpecError(f"{path} must be a list")
    return value


def operand_schema(spec: dict[str, Any]) -> dict[str, Any]:
    return require_mapping(
        require_mapping(spec.get("instructions"), "instructions.yaml").get("operand_schema"),
        "instructions.yaml.operand_schema",
    )


def size_codes(spec: dict[str, Any]) -> dict[str, dict[str, Any]]:
    raw = require_mapping(operand_schema(spec).get("size_codes"), "instructions.yaml.operand_schema.size_codes")
    return {str(name).upper(): require_mapping(body, f"size_codes.{name}") for name, body in raw.items()}


def size_kinds(spec: dict[str, Any]) -> dict[str, dict[str, Any]]:
    raw = require_mapping(operand_schema(spec).get("size_kinds"), "instructions.yaml.operand_schema.size_kinds")
    return {str(name).upper(): require_mapping(body, f"size_kinds.{name}") for name, body in raw.items()}


def is_size_kind(spec: dict[str, Any], kind: str) -> bool:
    return kind.upper() in size_kinds(spec)


def size_kind_field(spec: dict[str, Any], kind: str) -> str:
    body = size_kinds(spec).get(kind.upper())
    if body is None:
        raise SpecError(f"unknown size kind {kind}")
    field = str(body.get("field", "")).strip()
    if not field:
        raise SpecError(f"size kind {kind} has no field name")
    return field


def size_kind_entries(spec: dict[str, Any], kind: str, *, include_reserved: bool = False) -> list[dict[str, Any]]:
    body = size_kinds(spec).get(kind.upper())
    if body is None:
        raise SpecError(f"unknown size kind {kind}")
    entries = [dict(item) for item in require_list(body.get("values"), f"size_kinds.{kind}.values")]
    if include_reserved:
        entries.extend(dict(item) for item in body.get("reserved_values", []) or [])
    return sorted(entries, key=lambda item: int_value(item.get("value")))


def size_kind_width(spec: dict[str, Any], kind: str) -> int:
    max_value = max(int_value(item.get("value")) for item in size_kind_entries(spec, kind, include_reserved=True))
    return max(1, max_value.bit_length())


def size_kind_suffixes(spec: dict[str, Any], kind: str) -> list[str]:
    codes = size_codes(spec)
    entries = size_kind_entries(spec, kind, include_reserved=True)
    max_value = max(int_value(item.get("value")) for item in entries)
    out = [f".reserved{value}" for value in range(max_value + 1)]
    for item in entries:
        value = int_value(item.get("value"))
        code = item.get("code")
        if code is not None:
            out[value] = str(codes[str(code).upper()].get("suffix"))
        else:
            out[value] = "." + str(item.get("name"))
    return out


def size_kind_byte_widths(spec: dict[str, Any], kind: str) -> list[tuple[int, int]]:
    codes = size_codes(spec)
    out: list[tuple[int, int]] = []
    for item in size_kind_entries(spec, kind):
        code = str(item.get("code", "")).upper()
        out.append((int_value(item.get("value")), int(codes[code].get("bytes", 0))))
    return out


def size_code_bytes(spec: dict[str, Any], code: str) -> int:
    return int(size_codes(spec)[code.upper()].get("bytes", 0))


def size_code_label(spec: dict[str, Any], code: str) -> str:
    return str(size_codes(spec)[code.upper()].get("label", code))


def named_value_set(spec: dict[str, Any], name: str) -> dict[str, Any]:
    named = require_mapping(operand_schema(spec).get("named_values"), "instructions.yaml.operand_schema.named_values")
    body = named.get(name)
    return body if isinstance(body, dict) else {}


def named_values(spec: dict[str, Any], name: str, *, include_reserved: bool = False) -> list[tuple[str, int]]:
    body = named_value_set(spec, name)
    raw_values = body.get("values")
    if not isinstance(raw_values, list):
        return []
    values = [dict(item) for item in raw_values]
    if include_reserved:
        values.extend(dict(item) for item in body.get("reserved_values", []) or [])
    return [(str(item.get("name")), int_value(item.get("value"))) for item in sorted(values, key=lambda item: int_value(item.get("value")))]


def named_value_width(spec: dict[str, Any], name: str) -> int:
    return int(named_value_set(spec, name).get("width", 0))


def bitmap_operand(spec: dict[str, Any], name: str) -> dict[str, Any]:
    bitmaps = require_mapping(operand_schema(spec).get("bitmap_operands"), "instructions.yaml.operand_schema.bitmap_operands")
    body = bitmaps.get(name)
    return body if isinstance(body, dict) else {}


def bitmap_operand_ranges(spec: dict[str, Any], name: str) -> list[dict[str, Any]]:
    ranges = bitmap_operand(spec, name).get("ranges")
    if not isinstance(ranges, list):
        return []
    return [dict(item) for item in ranges]


def condition_entries(spec: dict[str, Any]) -> list[dict[str, Any]]:
    raw = require_list(
        require_mapping(spec.get("conditions"), "conditions.yaml").get("conditions"),
        "conditions.yaml.conditions",
    )
    return sorted((dict(item) for item in raw if isinstance(item, dict)), key=lambda item: int_value(item.get("value")))


def condition_named_values(spec: dict[str, Any]) -> list[tuple[str, int]]:
    out: list[tuple[str, int]] = []
    for condition in condition_entries(spec):
        value = int_value(condition.get("value"))
        names = [condition.get("name"), *(condition.get("aliases") or [])]
        for name in names:
            if name:
                out.append((str(name), value))
    return out


def condition_names_by_value(spec: dict[str, Any]) -> list[str]:
    out = [""] * 16
    for condition in condition_entries(spec):
        value = int_value(condition.get("value"))
        if 0 <= value < 16:
            out[value] = str(condition.get("name"))
    missing = [str(index) for index, name in enumerate(out) if not name]
    if missing:
        raise SpecError("conditions.yaml must define all 4-bit condition values; missing " + ", ".join(missing))
    return out


FLAG_TOKEN_RE = re.compile(r"\b([ZNCV])\b")


def condition_expression_for_sleigh(expression: str) -> str:
    lowered = expression.strip().lower()
    if lowered == "true":
        return "1"
    if lowered == "false":
        return "0"
    return FLAG_TOKEN_RE.sub(lambda match: match.group(1) + "F", expression)


def condition_sleigh_checks(spec: dict[str, Any]) -> list[tuple[int, str]]:
    return [
        (int_value(condition.get("value")), condition_expression_for_sleigh(str(condition.get("expression", "false"))))
        for condition in condition_entries(spec)
    ]


def register_class_count(spec: dict[str, Any], name: str) -> int:
    classes = require_mapping(require_mapping(spec.get("registers"), "registers.yaml").get("register_classes"), "registers.yaml.register_classes")
    body = require_mapping(classes.get(name), f"registers.yaml.register_classes.{name}")
    return int(body.get("count", 0))


def register_names(spec: dict[str, Any], class_name: str) -> list[str]:
    return [f"{class_name}{index}" for index in range(register_class_count(spec, class_name))]


def special_register_by_name(spec: dict[str, Any], name: str) -> dict[str, Any]:
    for reg in require_mapping(spec.get("registers"), "registers.yaml").get("special_registers", []) or []:
        if isinstance(reg, dict) and reg.get("name") == name:
            return reg
    raise SpecError(f"registers.yaml.special_registers has no {name}")


def special_register_layout(spec: dict[str, Any], name: str) -> dict[str, dict[str, Any]]:
    layout = special_register_by_name(spec, name).get("layout")
    return require_mapping(layout, f"registers.yaml.special_registers.{name}.layout")


def flag_names(spec: dict[str, Any]) -> list[str]:
    layout = special_register_layout(spec, "FLAGS")
    return [
        name
        for name, _field in sorted(
            layout.items(),
            key=lambda item: int_value(require_mapping(item[1], f"FLAGS.layout.{item[0]}").get("bit")),
            reverse=True,
        )
    ]


def flag_pseudo_registers(spec: dict[str, Any]) -> list[str]:
    return [f"{name}F" for name in flag_names(spec)]


def fflag_bits(spec: dict[str, Any]) -> dict[str, dict[str, Any]]:
    fpu = require_mapping(
        require_mapping(spec.get("registers"), "registers.yaml").get("floating_point_register_model"),
        "registers.yaml.floating_point_register_model",
    )
    fflags = require_mapping(fpu.get("fflags"), "floating_point_register_model.fflags")
    return require_mapping(fflags.get("bits"), "floating_point_register_model.fflags.bits")


def fflag_names(spec: dict[str, Any]) -> list[str]:
    bits = fflag_bits(spec)
    return [
        name
        for name, _field in sorted(
            bits.items(),
            key=lambda item: int_value(require_mapping(item[1], f"fflags.bits.{item[0]}").get("bit")),
            reverse=True,
        )
    ]


def fflag_meanings(spec: dict[str, Any]) -> dict[str, str]:
    return {name: str(body.get("description", name)) for name, body in fflag_bits(spec).items()}


def special_register_class(spec: dict[str, Any], class_name: str) -> dict[str, Any]:
    classes = require_mapping(
        require_mapping(spec.get("registers"), "registers.yaml").get("special_register_classes"),
        "registers.yaml.special_register_classes",
    )
    return require_mapping(classes.get(class_name), f"registers.yaml.special_register_classes.{class_name}")


def special_register_encoding(spec: dict[str, Any], class_name: str) -> list[dict[str, Any]]:
    body = special_register_class(spec, class_name)
    return sorted(
        (dict(item) for item in require_list(body.get("encoding"), f"special_register_classes.{class_name}.encoding")),
        key=lambda item: int_value(item.get("value")),
    )


def special_register_named_values(spec: dict[str, Any], class_name: str) -> list[tuple[str, int]]:
    out: list[tuple[str, int]] = []
    for item in special_register_encoding(spec, class_name):
        register = str(item.get("register", ""))
        if register and register.lower() != "reserved":
            out.append((register, int_value(item.get("value"))))
    return out


def special_register_attach_names(spec: dict[str, Any], class_name: str) -> list[str]:
    body = special_register_class(spec, class_name)
    width = int(body.get("encoding_bits", 0))
    values: dict[int, str] = {}
    for item in special_register_encoding(spec, class_name):
        value = int_value(item.get("value"))
        register = str(item.get("register", "") or f"{class_name}RES{value}")
        values[value] = register
    missing = [value for value in range(1 << width) if value not in values]
    if missing:
        raise SpecError(f"special register class {class_name} encoding missing values {missing}")
    return [values[value] for value in range(1 << width)]


def control_register_selectors(spec: dict[str, Any], class_name: str = "CR") -> list[tuple[int, str]]:
    classes = require_mapping(
        require_mapping(spec.get("registers"), "registers.yaml").get("control_register_classes"),
        "registers.yaml.control_register_classes",
    )
    body = require_mapping(classes.get(class_name), f"registers.yaml.control_register_classes.{class_name}")
    out: list[tuple[int, str]] = []
    for group in body.get("selector_groups", []) or []:
        if not isinstance(group, dict):
            continue
        for selector in group.get("selectors", []) or []:
            if isinstance(selector, dict):
                out.append((int_value(selector.get("value")), str(selector.get("register"))))
    return sorted(out)


def control_register_named_values(spec: dict[str, Any], class_name: str = "CR") -> list[tuple[str, int]]:
    return [(name, value) for value, name in control_register_selectors(spec, class_name) if name]


def ea_segment_named_values(spec: dict[str, Any]) -> list[tuple[str, int]]:
    descriptor = require_mapping(
        require_mapping(spec.get("ea"), "ea.yaml").get("extended_ea_descriptor"),
        "ea.yaml.extended_ea_descriptor",
    )
    values = require_mapping(descriptor.get("segment_values"), "ea.yaml.extended_ea_descriptor.segment_values")
    return sorted((str(name), int_value(value)) for value, name in values.items())


def compact_ea_forms(spec: dict[str, Any]) -> list[dict[str, Any]]:
    forms = require_mapping(require_mapping(spec.get("ea"), "ea.yaml").get("ea_forms"), "ea.yaml.ea_forms")
    out: list[dict[str, Any]] = []
    for form in require_list(forms.get("compact"), "ea.yaml.ea_forms.compact"):
        if isinstance(form, dict):
            out.append(dict(form))
    return out


def compact_pattern_value(pattern: str) -> int:
    bits = str(pattern).replace(" ", "")
    value = 0
    for ch in bits:
        value <<= 1
        if ch == "1":
            value |= 1
        elif ch in {"0", "_"} or ch.isalpha():
            continue
        else:
            raise SpecError(f"invalid compact pattern character {ch!r} in {pattern!r}")
    return value


def compact_ea_values_by_name(spec: dict[str, Any]) -> dict[str, int]:
    return {str(form.get("name")): compact_pattern_value(str(form.get("pattern"))) for form in compact_ea_forms(spec)}


def prefix_value(spec: dict[str, Any], name: str) -> int:
    for prefix in require_mapping(spec.get("prefixes"), "prefixes.yaml").get("prefixes", []) or []:
        if isinstance(prefix, dict) and prefix.get("name") == name:
            return int_value(prefix.get("value"))
    raise SpecError(f"prefixes.yaml has no prefix {name}")


def mnemonic_policy(spec: dict[str, Any]) -> dict[str, Any]:
    allocation = require_mapping(require_mapping(spec.get("instructions"), "instructions.yaml").get("allocation"), "instructions.yaml.allocation")
    return require_mapping(allocation.get("mnemonic_policy"), "instructions.yaml.allocation.mnemonic_policy")


def encoding_schema_errors(spec: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    try:
        codes = size_codes(spec)
        if not codes:
            errors.append("operand_schema.size_codes must not be empty")
        for code, body in codes.items():
            if int(body.get("bytes", 0)) <= 0:
                errors.append(f"operand_schema.size_codes.{code}.bytes must be positive")
            if not str(body.get("suffix", "")).startswith("."):
                errors.append(f"operand_schema.size_codes.{code}.suffix must start with '.'")
        for kind, body in size_kinds(spec).items():
            seen_values: set[int] = set()
            for item in size_kind_entries(spec, kind, include_reserved=True):
                value = int_value(item.get("value"))
                if value in seen_values:
                    errors.append(f"operand_schema.size_kinds.{kind} duplicates value {value}")
                seen_values.add(value)
                code = item.get("code")
                if code is not None and str(code).upper() not in codes:
                    errors.append(f"operand_schema.size_kinds.{kind} references unknown size code {code}")
        for name, body in require_mapping(operand_schema(spec).get("named_values"), "named_values").items():
            width = int(require_mapping(body, f"named_values.{name}").get("width", 0))
            if width <= 0:
                errors.append(f"operand_schema.named_values.{name}.width must be positive")
                continue
            seen_values: set[int] = set()
            seen_names: set[str] = set()
            for source_key in ("values", "reserved_values"):
                for item in body.get(source_key, []) or []:
                    if not isinstance(item, dict):
                        continue
                    value = int_value(item.get("value"))
                    named = str(item.get("name", ""))
                    if not 0 <= value < (1 << width):
                        errors.append(f"operand_schema.named_values.{name}.{named} value {value} does not fit width {width}")
                    if value in seen_values:
                        errors.append(f"operand_schema.named_values.{name} duplicates value {value}")
                    if named in seen_names:
                        errors.append(f"operand_schema.named_values.{name} duplicates name {named}")
                    seen_values.add(value)
                    seen_names.add(named)
        register_classes = require_mapping(require_mapping(spec.get("registers"), "registers.yaml").get("register_classes"), "register_classes")
        for name, body in require_mapping(operand_schema(spec).get("bitmap_operands"), "bitmap_operands").items():
            bitmap = require_mapping(body, f"bitmap_operands.{name}")
            width = int(bitmap.get("width", 0))
            if width <= 0:
                errors.append(f"operand_schema.bitmap_operands.{name}.width must be positive")
            for item in bitmap.get("ranges", []) or []:
                if not isinstance(item, dict):
                    continue
                bits = item.get("bits")
                if not isinstance(bits, list) or len(bits) != 2:
                    errors.append(f"operand_schema.bitmap_operands.{name}.ranges.bits must be [lo, hi]")
                    continue
                lo = int_value(bits[0])
                hi = int_value(bits[1])
                reg_class = str(item.get("register_class"))
                reg_count = int(require_mapping(register_classes.get(reg_class), f"register_classes.{reg_class}").get("count", 0))
                if lo < 0 or hi < lo or hi >= width:
                    errors.append(f"operand_schema.bitmap_operands.{name}.{reg_class} bit range is outside width {width}")
                if hi - lo + 1 != reg_count:
                    errors.append(f"operand_schema.bitmap_operands.{name}.{reg_class} range width must match register count {reg_count}")
        condition_names_by_value(spec)
    except (KeyError, TypeError, ValueError, SpecError) as exc:
        errors.append(str(exc))
    return errors
