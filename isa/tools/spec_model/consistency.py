from __future__ import annotations

from typing import Any
import re

from .core import Pattern, PatternEntry, ValidationResult, SpecError, is_scalar_value
from .catalog import instruction_catalog
from .patterns import (
    aliases_for,
    entry_id,
    field_names,
    length_bounds,
    operand_field_refs,
    parse_pattern,
    patterns_overlap,
)
from .schemas import (
    MEMORY_MEMORY_DEFAULT_RULES,
    MEMORY_RULES,
    REP_OBSERVED_VALUE_RULES,
    REPFLAGS_RULES,
)
from .encoding import encoding_schema_errors


def validate_spec_consistency(spec: dict[str, Any]) -> tuple[ValidationResult, list[PatternEntry]]:
    result = ValidationResult()
    entries: list[PatternEntry] = []
    instruction_ids: set[str] = set()

    check_register_model(spec, result)
    check_prefix_model(spec, result)
    check_conditions(spec, result)
    check_effective_addresses(spec, result)
    check_encoding_schema(spec, result)

    opcodes = spec["opcodes"]
    for item in opcodes.get("reserved", []) or []:
        for index, raw in enumerate(item.get("patterns", [item.get("pattern")]) or []):
            if raw is None:
                continue
            source = dict(item)
            source["pattern"] = raw
            ident = f"{entry_id(item, 'reserved')}_{index}" if "patterns" in item else entry_id(item, "reserved")
            try:
                pattern = parse_pattern(str(raw), field_names(source))
            except SpecError as exc:
                result.error(f"{ident}: invalid reserved pattern: {exc}")
                continue
            entries.append(PatternEntry(ident, "reserved", source, pattern))

    check_overlaps(entries, result)
    check_canonical_rules(spec, instruction_ids, result)
    check_semantics_consistency(spec, entries, result)
    return result, entries


def check_encoding_schema(spec: dict[str, Any], result: ValidationResult) -> None:
    for error in encoding_schema_errors(spec):
        result.error(error)


def check_register_model(spec: dict[str, Any], result: ValidationResult) -> None:
    seen: set[str] = set()
    for name, body in (spec["registers"].get("register_classes") or {}).items():
        if name in seen:
            result.error(f"duplicate register class {name}")
        seen.add(str(name))
        count = int(body.get("count", 0))
        width = int(body.get("width", 0))
        if count <= 0 or width <= 0:
            result.error(f"register class {name} must have positive count and width")
    for reg in spec["registers"].get("special_registers", []) or []:
        name = str(reg.get("name", ""))
        if not name:
            result.error("special register without name")
        if int(reg.get("width", 0)) <= 0:
            result.error(f"special register {name} must have positive width")

    named_registers = {str(reg.get("name", "")) for reg in spec["registers"].get("special_registers", []) or []}
    named_registers.update(
        str(reg.get("name", ""))
        for reg in spec.get("segments", {}).get("segment_registers", []) or []
        if isinstance(reg, dict)
    )
    for name, body in (spec["registers"].get("special_register_classes") or {}).items():
        if not isinstance(body, dict):
            result.error(f"special register class {name} must be a mapping")
            continue
        width = int(body.get("width", 0))
        bits = int(body.get("encoding_bits", 0))
        regs = [str(reg) for reg in body.get("registers", []) or []]
        if width <= 0:
            result.error(f"special register class {name} must have positive width")
        if bits <= 0:
            result.error(f"special register class {name} must have positive encoding_bits")
        if len(regs) > (1 << bits):
            result.error(f"special register class {name} has more registers than encoding_bits can encode")
        unknown = sorted(reg for reg in regs if reg not in named_registers)
        if unknown:
            result.error(f"special register class {name} references unknown registers {', '.join(unknown)}")
    for name, body in (spec["registers"].get("control_register_classes") or {}).items():
        if not isinstance(body, dict):
            result.error(f"control register class {name} must be a mapping")
            continue
        width = int(body.get("width", 0))
        bits = int(body.get("encoding_bits", 0))
        regs = [str(reg) for reg in body.get("registers", []) or []]
        if width <= 0:
            result.error(f"control register class {name} must have positive width")
        if bits <= 0:
            result.error(f"control register class {name} must have positive encoding_bits")
        if len(regs) > (1 << bits):
            result.error(f"control register class {name} has more registers than encoding_bits can encode")
        unknown = sorted(reg for reg in regs if reg not in named_registers)
        if unknown:
            result.error(f"control register class {name} references unknown registers {', '.join(unknown)}")
        check_control_register_selectors(str(name), body, regs, named_registers, bits, result)


def parse_int_value(value: Any) -> int | None:
    try:
        if isinstance(value, int):
            return value
        return int(str(value), 0)
    except (TypeError, ValueError):
        return None


def check_control_register_selectors(
    class_name: str,
    body: dict[str, Any],
    regs: list[str],
    named_registers: set[str],
    bits: int,
    result: ValidationResult,
) -> None:
    seen_values: dict[int, str] = {}
    seen_registers: dict[str, int] = {}
    reg_set = set(regs)
    max_value = 1 << bits if bits > 0 else 0
    for group_index, group in enumerate(body.get("selector_groups", []) or []):
        group_path = f"control register class {class_name} selector_groups[{group_index}]"
        if not isinstance(group, dict):
            result.error(f"{group_path} must be a mapping")
            continue
        range_value = group.get("range")
        low = high = None
        if isinstance(range_value, list) and len(range_value) == 2:
            low = parse_int_value(range_value[0])
            high = parse_int_value(range_value[1])
            if low is None or high is None or low > high:
                result.error(f"{group_path} has invalid selector range")
        selectors = group.get("selectors", []) or []
        if not isinstance(selectors, list):
            result.error(f"{group_path}.selectors must be a list")
            continue
        for selector_index, selector in enumerate(selectors):
            selector_path = f"{group_path}.selectors[{selector_index}]"
            if not isinstance(selector, dict):
                result.error(f"{selector_path} must be a mapping")
                continue
            value = parse_int_value(selector.get("value"))
            register = str(selector.get("register", ""))
            if value is None:
                result.error(f"{selector_path}.value must be an integer")
                continue
            if max_value and not 0 <= value < max_value:
                result.error(f"{selector_path}.value 0x{value:x} does not fit {bits} selector bits")
            if low is not None and high is not None and not low <= value <= high:
                result.error(f"{selector_path}.value 0x{value:x} is outside selector group range")
            previous_register = seen_values.get(value)
            if previous_register is not None:
                result.error(
                    f"control register class {class_name} selector value 0x{value:x} "
                    f"is assigned to both {previous_register} and {register}"
                )
            seen_values[value] = register
            previous_value = seen_registers.get(register)
            if previous_value is not None:
                result.error(
                    f"control register class {class_name} register {register} has duplicate selectors "
                    f"0x{previous_value:x} and 0x{value:x}"
                )
            seen_registers[register] = value
            if register not in named_registers:
                result.error(f"{selector_path} references unknown register {register}")
            if register not in reg_set:
                result.error(f"{selector_path} references register {register} not listed in class {class_name}")
    missing = sorted(reg for reg in regs if reg not in seen_registers)
    if missing:
        result.error(
            f"control register class {class_name} registers missing selector entries: "
            + ", ".join(missing)
        )

def check_prefix_model(spec: dict[str, Any], result: ValidationResult) -> None:
    names: set[str] = set()
    values: dict[int, str] = {}
    prefix_patterns: list[PatternEntry] = []
    for prefix in spec["prefixes"].get("prefixes", []) or []:
        name = str(prefix.get("name", ""))
        if not name:
            result.error("prefix without name")
            continue
        if name in names:
            result.error(f"duplicate prefix name {name}")
        names.add(name)
        if "value" in prefix:
            value = int(prefix["value"])
            if value < 0 or value > 0xff:
                result.error(f"prefix {name} value {value:#x} is not 8-bit")
            if value in values:
                result.error(f"prefix {name} collides with {values[value]} at {value:#x}")
            values[value] = name
        if "pattern" in prefix:
            try:
                pattern = parse_pattern(str(prefix["pattern"]), field_names(prefix))
            except SpecError as exc:
                result.error(f"prefix {name}: invalid pattern: {exc}")
                continue
            if pattern.width != 8:
                result.error(f"prefix {name}: pattern width {pattern.width} is not 8 bits")
            prefix_patterns.append(PatternEntry(name, "prefix", prefix, pattern))

    for value, name in values.items():
        value_pattern = Pattern(raw=f"{value:08b}", width=8, mask=0xFF, value=value)
        prefix_patterns.append(PatternEntry(name, "prefix", {"name": name}, value_pattern))

    check_overlaps(prefix_patterns, result)
    groups = {str(prefix.get("group")) for prefix in spec["prefixes"].get("prefixes", []) or []}
    for group in spec["prefixes"].get("mutually_exclusive_groups", []) or []:
        if str(group) not in groups:
            result.error(f"mutually exclusive prefix group {group} is not defined")

    prefix_by_name = {str(item.get("name")): item for item in spec["prefixes"].get("prefixes", []) or []}
    for prefix in spec["prefixes"].get("prefixes", []) or []:
        if not isinstance(prefix, dict):
            continue
        name = str(prefix.get("name", "prefix"))
        syntax = prefix.get("syntax") or {}
        if isinstance(syntax, dict):
            terminator = syntax.get("terminator_prefix")
            if terminator and str(terminator) not in prefix_by_name:
                result.error(f"prefix {name}: unknown terminator prefix {terminator}")
            closes = syntax.get("closes")
            if closes and str(closes) not in prefix_by_name:
                result.error(f"prefix {name}: unknown prefix closed by syntax.closes {closes}")

        if "pattern" in prefix:
            try:
                pattern = parse_pattern(str(prefix["pattern"]), field_names(prefix))
            except SpecError:
                continue
            for metadata_key in ("condition", "operand"):
                metadata = prefix.get(metadata_key) or {}
                if not isinstance(metadata, dict):
                    continue
                field_name = metadata.get("field")
                if field_name and str(field_name) not in pattern.fields:
                    result.error(f"prefix {name}: {metadata_key} field {field_name} is not present in the pattern")

        alignment = prefix.get("alignment") or {}
        if isinstance(alignment, dict) and "grouping_window_bytes" in alignment:
            try:
                grouping_window_bytes = int(alignment.get("grouping_window_bytes", 0) or 0)
            except (TypeError, ValueError):
                grouping_window_bytes = 0
            if grouping_window_bytes <= 0:
                result.error(f"prefix {name}: grouping_window_bytes must be positive")

        fault_behavior = prefix.get("fault_behavior") or {}
        continuation = fault_behavior.get("continuation_state") if isinstance(fault_behavior, dict) else {}
        if isinstance(continuation, dict):
            for field_name in ("group_start", "counter_register"):
                field = continuation.get(field_name)
                if not isinstance(field, dict) or "bits" not in field:
                    continue
                try:
                    bit_count = int(field.get("bits", 0) or 0)
                except (TypeError, ValueError):
                    bit_count = 0
                if bit_count <= 0:
                    result.error(f"prefix {name}: continuation field {field_name} must have a positive bit width")

        if name == "REPcc":
            check_rule_id_map(
                prefix.get("observed_value"),
                f"prefix {name}.observed_value",
                REP_OBSERVED_VALUE_RULES,
                result,
            )
            check_rule_id_map(
                prefix.get("repflags"),
                f"prefix {name}.repflags",
                REPFLAGS_RULES,
                result,
            )


def check_conditions(spec: dict[str, Any], result: ValidationResult) -> None:
    values: dict[int, str] = {}
    names: set[str] = set()
    for condition in spec["conditions"].get("conditions", []) or []:
        name = str(condition.get("name", ""))
        value = int(condition.get("value", -1))
        if not name:
            result.error("condition without name")
        if value < 0 or value > 0xf:
            result.error(f"condition {name} value {value:#x} is not 4-bit")
        if value in values:
            result.error(f"condition {name} collides with {values[value]} at {value:#x}")
        values[value] = name
        for alias in [name] + list(condition.get("aliases", []) or []):
            if str(alias) in names:
                result.error(f"duplicate condition name/alias {alias}")
            names.add(str(alias))


def check_effective_addresses(spec: dict[str, Any], result: ValidationResult) -> None:
    fields = spec["ea"].get("fields") or {}
    entries: list[PatternEntry] = []
    names: set[str] = set()
    compact_names: set[str] = set()
    extended_names: set[str] = set()
    forms_by_name: dict[str, dict[str, Any]] = {}

    def add_form(form: dict[str, Any], default_name: str, kind: str) -> None:
        name = entry_id(form, default_name)
        if name in names:
            result.error(f"duplicate EA form {name}")
        names.add(name)
        forms_by_name[name] = form
        if kind == "ea":
            compact_names.add(name)
        if "pattern" not in form:
            return
        declared = list(fields) + field_names(form)
        try:
            pattern = parse_pattern(str(form["pattern"]), declared)
        except (KeyError, SpecError) as exc:
            result.error(f"{name}: invalid EA pattern: {exc}")
            return
        entries.append(PatternEntry(name, kind, form, pattern))
        for field_name, width in pattern.fields.items():
            if field_name in fields:
                declared_width = int(fields[field_name].get("width", width))
                if declared_width != width:
                    result.error(
                        f"{name}: EA field {field_name} width is {width}, declared {declared_width}"
                    )

    ea_forms = spec["ea"].get("ea_forms", []) or []
    if isinstance(ea_forms, dict):
        compact_forms = ea_forms.get("compact", []) or []
    else:
        compact_forms = ea_forms
    for index, form in enumerate(compact_forms):
        add_form(form, f"ea_forms_{index}", "ea")

    for index, form in enumerate(spec["ea"].get("reserved_forms", []) or []):
        add_form(form, f"reserved_forms_{index}", "ea_reserved")

    extended_values: dict[tuple[str, int], str] = {}
    extended_forms = spec["ea"].get("extended_ea_forms", []) or []
    for index, form in enumerate(extended_forms):
        name = entry_id(form, f"extended_ea_forms_{index}")
        if name in names:
            result.error(f"duplicate EA form {name}")
        names.add(name)
        extended_names.add(name)
        forms_by_name[name] = form
        if "value" in form:
            value = int(form["value"])
            escape = str(form.get("escape", "EXTENDED"))
            key = (escape, value)
            if value < 0 or value > 0x1F:
                result.error(f"{name}: extended EA value {value:#x} is not 5-bit")
            if key in extended_values:
                result.error(
                    f"{name}: extended EA value collides with {extended_values[key]} "
                    f"at {escape}:{value:#x}"
                )
            extended_values[key] = name
    check_overlaps(entries, result)
    check_ea_coverage(spec["ea"], forms_by_name, compact_names, extended_names, result)
    check_ea_operand_policy(spec["ea"], compact_names, extended_names, result)


def check_ea_coverage(
    ea: dict[str, Any],
    forms_by_name: dict[str, dict[str, Any]],
    compact_names: set[str],
    extended_names: set[str],
    result: ValidationResult,
) -> None:
    audit = ea.get("ea_coverage_audit") or {}
    required_compact = {str(name) for name in audit.get("required_compact_ea_forms", []) or []}
    missing_compact = sorted(required_compact - compact_names)
    if missing_compact:
        result.error(f"EA coverage audit: missing compact forms {', '.join(missing_compact)}")

    required_extended = {str(name) for name in audit.get("required_extended_ea_forms", []) or []}
    missing_extended = sorted(required_extended - extended_names)
    if missing_extended:
        result.error(f"EA coverage audit: missing extended forms {', '.join(missing_extended)}")

    for name, expected in (audit.get("required_properties") or {}).items():
        form = forms_by_name.get(str(name))
        if form is None:
            result.error(f"EA coverage audit: required properties reference unknown form {name}")
            continue
        for key, value in (expected or {}).items():
            actual = form.get(key)
            if actual != value:
                result.error(
                    f"EA coverage audit: {name}.{key} is {actual!r}, expected {value!r}"
                )


def check_ea_operand_policy(
    ea: dict[str, Any],
    compact_names: set[str],
    extended_names: set[str],
    result: ValidationResult,
) -> None:
    policy = ea.get("ea_operand_policy") or {}
    ea_sets = policy.get("ea_sets") or {}
    if not ea_sets:
        return

    default_set = policy.get("default_allowed_ea_set")
    if default_set and str(default_set) not in ea_sets:
        result.error(f"EA operand policy: default set {default_set} is not defined")

    resolved: dict[str, set[str]] = {}

    def resolve_set(name: str, stack: tuple[str, ...] = ()) -> set[str]:
        if name in resolved:
            return set(resolved[name])
        if name in stack:
            result.error(f"EA operand policy: inheritance cycle {' -> '.join(stack + (name,))}")
            return set()
        body = ea_sets.get(name)
        if not isinstance(body, dict):
            result.error(f"EA operand policy: unknown EA set {name}")
            return set()
        values: set[str] = set()
        inherited = body.get("inherits")
        if inherited:
            values.update(resolve_set(str(inherited), stack + (name,)))
        includes = {str(item) for item in body.get("includes", []) or []}
        excludes = {str(item) for item in body.get("excludes", []) or []}
        unknown = sorted((includes | excludes) - compact_names)
        if unknown:
            result.error(f"EA operand policy {name}: references unknown compact EA forms {', '.join(unknown)}")
        values.update(includes)
        values.difference_update(excludes)
        resolved[name] = values
        return set(values)

    for name in ea_sets:
        resolve_set(str(name))

    extended_constraints = policy.get("extended_form_constraints") or {}
    if isinstance(extended_constraints, dict):
        for constraint_name, body in extended_constraints.items():
            if not isinstance(body, dict):
                result.error(f"EA operand policy extended_form_constraints.{constraint_name}: must be a mapping")
                continue
            referenced = {
                str(item)
                for key in ("includes", "excludes")
                for item in (body.get(key, []) or [])
            }
            unknown = sorted(referenced - extended_names)
            if unknown:
                result.error(
                    "EA operand policy "
                    f"extended_form_constraints.{constraint_name}: references unknown extended EA forms "
                    + ", ".join(unknown)
                )

    allowed_atoms = compact_names | {"PC_relative"}
    constraints = ea.get("instruction_ea_constraints") or {}
    for name, body in constraints.items():
        if not isinstance(body, dict):
            continue
        for key, value in body.items():
            if key.endswith("_ea_set") and str(value) not in ea_sets:
                result.error(f"instruction EA constraint {name}.{key}: unknown EA set {value}")
            if key in {"src", "dst"} and str(value) not in allowed_atoms:
                result.error(f"instruction EA constraint {name}.{key}: unknown operand atom {value}")
            if key == "disallow":
                unknown = sorted({str(item) for item in value or []} - allowed_atoms)
                if unknown:
                    result.error(
                        f"instruction EA constraint {name}.disallow references unknown atoms {', '.join(unknown)}"
                    )


def check_canonical_rules(spec: dict[str, Any], instruction_ids: set[str], result: ValidationResult) -> None:
    for rule in spec["opcodes"].get("canonical_rules", []) or []:
        ident = str(rule.get("id", "canonical_rule"))
        for key in ("canonical", "noncanonical"):
            target = str(rule.get(key, ""))
            if not target:
                result.error(f"{ident}: missing {key} target")
            elif instruction_ids and target not in instruction_ids:
                result.error(f"{ident}: {key} target {target} is not an instruction id")


def check_semantics_consistency(spec: dict[str, Any], entries: list[PatternEntry], result: ValidationResult) -> None:
    semantics = spec.get("semantics") or {}
    if not isinstance(semantics, dict):
        result.error("semantics.yaml must contain a mapping")
        return

    for section in ("encoding_rules", "compatibility_rules"):
        if section not in semantics:
            result.error(f"semantics.yaml missing {section}")
    encoding_rules = semantics.get("encoding_rules") or {}
    if isinstance(encoding_rules, dict):
        memory_operands = encoding_rules.get("memory_operands") or {}
        if isinstance(memory_operands, dict) and "default" in memory_operands:
            check_rule_id_value(
                memory_operands.get("default"),
                "semantics.encoding_rules.memory_operands.default",
                MEMORY_RULES,
                result,
            )

    catalog = instruction_catalog(spec)
    if not isinstance(catalog, dict):
        result.error("instructions.yaml must contain a mapping")
        return

    if "compact_primary_instructions" not in catalog:
        result.error("instructions.yaml missing compact_primary_instructions")

    compact = catalog.get("compact_primary_instructions") or {}
    if not isinstance(compact, dict):
        result.error("compact_primary_instructions must be a mapping")
        return
    operand_schema = catalog_operand_schema(catalog)
    check_catalog_section(
        "compact_primary_instructions",
        compact,
        result,
        source="instructions.yaml",
        operand_schema=operand_schema,
    )

    for section in (
        "integer_instructions",
        "atomic_system_cache_instructions",
    ):
        check_catalog_section(
            section,
            catalog.get(section),
            result,
            source="instructions.yaml",
            operand_schema=operand_schema,
        )

    fpu = catalog.get("fpu") or {}
    if isinstance(fpu, dict):
        check_catalog_section(
            "fpu.instructions",
            fpu.get("instructions"),
            result,
            source="instructions.yaml",
            operand_schema=operand_schema,
        )
    elif "fpu" in catalog:
        result.error("fpu must be a mapping")

    check_catalog_global_consistency(catalog, spec, result)
    check_fixed_instruction_encodings(catalog, spec, result)
    check_operation_semantics(catalog, spec, entries, result)


def semantic_entry_mnemonics(key: str, body: dict[str, Any]) -> list[str]:
    names = body.get("mnemonics")
    if isinstance(names, list):
        return [str(name) for name in names]
    if "_" in key and key.upper() == key:
        return []
    return [key]


def check_catalog_section(
    section: str,
    body: Any,
    result: ValidationResult,
    *,
    source: str = "semantics.yaml",
    operand_schema: dict[str, Any] | None = None,
) -> None:
    if body is None:
        result.error(f"{source} missing {section}")
        return
    if not isinstance(body, dict):
        result.error(f"{section} must be a mapping")
        return
    seen: set[str] = set()
    for key, item in body.items():
        if not isinstance(item, dict):
            result.error(f"{section}.{key} must be a mapping")
            continue
        names = semantic_entry_mnemonics(str(key), item)
        if not names:
            result.error(f"{section}.{key} does not name any mnemonic")
            continue
        for name in names:
            if name in seen:
                result.error(f"duplicate mnemonic {name} in {section}")
            seen.add(name)
        check_catalog_entry(section, str(key), item, names, result, operand_schema or {})


def catalog_sections(catalog: dict[str, Any]) -> list[tuple[str, Any]]:
    fpu = catalog.get("fpu") or {}
    return [
        ("compact_primary_instructions", catalog.get("compact_primary_instructions")),
        ("integer_instructions", catalog.get("integer_instructions")),
        ("atomic_system_cache_instructions", catalog.get("atomic_system_cache_instructions")),
        (
            "fpu.instructions",
            fpu.get("instructions") if isinstance(fpu, dict) else None,
        ),
    ]


def catalog_operand_schema(catalog: dict[str, Any]) -> dict[str, Any]:
    schema = catalog.get("operand_schema") or {}
    if not isinstance(schema, dict):
        return {
            "role_name_pattern": r"^[a-z][a-z0-9_]*$",
            "types": set(),
            "selector_roles": set(),
        }
    types = schema.get("types", [])
    if isinstance(types, dict):
        type_names = {str(name) for name in types}
    elif isinstance(types, list):
        type_names = {str(name) for name in types}
    else:
        type_names = set()
    selector_roles = schema.get("selector_roles", [])
    return {
        "role_name_pattern": str(schema.get("role_name_pattern", r"^[a-z][a-z0-9_]*$")),
        "types": type_names,
        "condition_role": str(schema.get("condition_role", "cc")),
        "selector_roles": {str(name) for name in selector_roles or []}
        if isinstance(selector_roles, list)
        else set(),
    }


def check_catalog_global_consistency(catalog: dict[str, Any], spec: dict[str, Any], result: ValidationResult) -> None:
    owners: dict[str, str] = {}
    for section, body in catalog_sections(catalog):
        if not isinstance(body, dict):
            continue
        for key, item in body.items():
            if not isinstance(item, dict):
                continue
            for mnemonic in semantic_entry_mnemonics(str(key), item):
                previous = owners.get(mnemonic)
                if previous is not None:
                    result.error(f"mnemonic {mnemonic} appears in both {previous} and {section}.{key}")
                owners[mnemonic] = f"{section}.{key}"

    compact = catalog.get("compact_primary_instructions") or {}
    if isinstance(compact, dict):
        check_canonical_alias_rules(catalog, spec, result)

    fpu = catalog.get("fpu") or {}
    registers = fpu.get("registers") if isinstance(fpu, dict) else None
    if isinstance(registers, dict) and isinstance(registers.get("F"), dict):
        fregs = registers["F"]
        for key in ("count", "width"):
            value = fregs.get(key)
            if not isinstance(value, int) or value <= 0:
                result.error(f"fpu.registers.F.{key} must be a positive integer, got {value!r}")


def word0_payload_width(spec: dict[str, Any]) -> int:
    payload = (((spec.get("opcodes") or {}).get("word0") or {}).get("payload") or {})
    bits = payload.get("bits") if isinstance(payload, dict) else None
    if isinstance(bits, list) and len(bits) == 2:
        endpoints = [parse_int_value(item) for item in bits]
        if endpoints[0] is not None and endpoints[1] is not None:
            return abs(endpoints[0] - endpoints[1]) + 1
    bit = payload.get("bit") if isinstance(payload, dict) else None
    if parse_int_value(bit) is not None:
        return 1
    return 12


def check_fixed_instruction_encodings(
    catalog: dict[str, Any], spec: dict[str, Any], result: ValidationResult
) -> None:
    width = word0_payload_width(spec)
    limit = 1 << width
    used: dict[int, str] = {}
    for section, body in catalog_sections(catalog):
        if not isinstance(body, dict):
            continue
        for key, item in body.items():
            if not isinstance(item, dict):
                continue
            fixed = item.get("fixed_encoding")
            if fixed is None:
                continue
            path = f"{section}.{key}.fixed_encoding"
            if section != "compact_primary_instructions":
                result.error(f"{path}: primary_payload is only valid for compact primary instructions")
            if not isinstance(fixed, dict):
                result.error(f"{path} must be a mapping")
                continue
            payload = parse_int_value(fixed.get("primary_payload"))
            if payload is None:
                result.error(f"{path}.primary_payload must be an integer")
                continue
            if not 0 <= payload < limit:
                result.error(f"{path}.primary_payload 0x{payload:x} does not fit {width} payload bits")
            previous = used.get(payload)
            if previous is not None:
                result.error(f"{path}.primary_payload 0x{payload:03x} duplicates {previous}")
            used[payload] = path
            operands = item.get("operands", [])
            if operands not in (None, []):
                result.error(f"{path}: fixed primary payload entries must not declare primary operand fields")
            if item.get("compact_forms") or item.get("extended_forms"):
                result.error(f"{path}: fixed primary payload entries must not declare alternate forms")


def check_operation_semantics(
    catalog: dict[str, Any],
    spec: dict[str, Any],
    entries: list[PatternEntry],
    result: ValidationResult,
) -> None:
    instructions = spec.get("instructions") or {}
    operation_semantics = instructions.get("operation_semantics")
    if not isinstance(operation_semantics, dict):
        result.error("instructions.yaml missing operation_semantics mapping")
        return

    defaults = operation_semantics.get("defaults") or {}
    if isinstance(defaults, dict) and "memory_memory" in defaults:
        check_rule_id_value(
            defaults.get("memory_memory"),
            "operation_semantics.defaults.memory_memory",
            MEMORY_MEMORY_DEFAULT_RULES,
            result,
        )

    check_repeat_prefix_semantics(operation_semantics, result)

    groups = operation_semantics.get("groups")
    if not isinstance(groups, dict):
        result.error("operation_semantics.groups must be a mapping")
        return

    known = set(catalog_entry_map(catalog))
    covered: dict[str, str] = {}
    semantics_by_mnemonic: dict[str, dict[str, Any]] = {}
    for group_name, group in groups.items():
        if not isinstance(group, dict):
            result.error(f"operation_semantics.groups.{group_name} must be a mapping")
            continue
        members = group.get("members")
        if not isinstance(members, list) or not members:
            result.error(f"operation_semantics.groups.{group_name}.members must be a non-empty list")
            continue
        member_names = {str(member) for member in members}
        unknown_members = sorted(member_names - known)
        if unknown_members:
            result.error(
                f"operation_semantics.groups.{group_name} references unknown mnemonics "
                + ", ".join(unknown_members)
            )
        for mnemonic in member_names & known:
            previous = covered.get(mnemonic)
            if previous is not None:
                result.error(
                    f"operation_semantics duplicate coverage for {mnemonic}: "
                    f"{previous} and {group_name}"
                )
            covered[mnemonic] = str(group_name)
        for mnemonic in member_names & known:
            target = semantics_by_mnemonic.setdefault(mnemonic, {})
            for semantic_key in ("inputs", "input_output", "output"):
                by_mnemonic = group.get(f"{semantic_key}_by_mnemonic")
                if isinstance(by_mnemonic, dict) and mnemonic in by_mnemonic:
                    target[semantic_key] = by_mnemonic[mnemonic]
                elif semantic_key in group:
                    target[semantic_key] = group[semantic_key]
        for key, value in group.items():
            if not key.endswith("_by_mnemonic"):
                continue
            if not isinstance(value, dict):
                result.error(f"operation_semantics.groups.{group_name}.{key} must be a mapping")
                continue
            unknown_keys = sorted({str(name) for name in value} - member_names)
            if unknown_keys:
                result.error(
                    f"operation_semantics.groups.{group_name}.{key} contains non-member keys "
                    + ", ".join(unknown_keys)
                )
        if "memory" in group:
            check_rule_id_value(
                group.get("memory"),
                f"operation_semantics.groups.{group_name}.memory",
                MEMORY_RULES,
                result,
            )
        check_rule_id_map(
            group.get("memory_by_mnemonic"),
            f"operation_semantics.groups.{group_name}.memory_by_mnemonic",
            MEMORY_RULES,
            result,
        )

    explicit = operation_semantics.get("instructions") or {}
    if explicit and not isinstance(explicit, dict):
        result.error("operation_semantics.instructions must be a mapping")
        explicit = {}
    unknown_explicit = sorted({str(name) for name in explicit} - known)
    if unknown_explicit:
        result.error(
            "operation_semantics.instructions references unknown mnemonics "
            + ", ".join(unknown_explicit)
        )
    for mnemonic, entry in explicit.items():
        if isinstance(entry, dict) and "pcode" in entry:
            check_pcode_value(
                entry["pcode"],
                f"operation_semantics.instructions.{mnemonic}.pcode",
                result,
            )
        if isinstance(entry, dict) and "pcode_by_form" in entry:
            check_pcode_by_form_value(
                entry["pcode_by_form"],
                f"operation_semantics.instructions.{mnemonic}.pcode_by_form",
                result,
            )
        if isinstance(entry, dict):
            target = semantics_by_mnemonic.setdefault(str(mnemonic), {})
            for semantic_key in ("inputs", "input_output", "output", "pcode", "pcode_by_form"):
                if semantic_key in entry:
                    target[semantic_key] = entry[semantic_key]

    covered.update({str(name): "instruction_override" for name in explicit if str(name) in known})
    missing = sorted(known - set(covered))
    if missing:
        result.error(
            "operation_semantics missing operation details for "
            + ", ".join(missing)
        )
    missing_pcode = sorted(
        mnemonic for mnemonic in known
        if "pcode" not in semantics_by_mnemonic.get(mnemonic, {})
        and "pcode_by_form" not in semantics_by_mnemonic.get(mnemonic, {})
    )
    if missing_pcode:
        result.error(
            "operation_semantics missing per-instruction SLEIGH pcode for "
            + ", ".join(missing_pcode)
        )
    catalog_entries = catalog_entry_map(catalog)
    for mnemonic, semantics in sorted(semantics_by_mnemonic.items()):
        entry = catalog_entries.get(mnemonic)
        if entry is not None:
            check_pcode_form_role_bindings(mnemonic, entry, semantics, result)


def check_repeat_prefix_semantics(operation_semantics: dict[str, Any], result: ValidationResult) -> None:
    repeat_prefixes = operation_semantics.get("repeat_prefixes") or {}
    if not isinstance(repeat_prefixes, dict):
        result.error("operation_semantics.repeat_prefixes must be a mapping")
        return
    repcc = repeat_prefixes.get("REPcc") or {}
    if not isinstance(repcc, dict):
        result.error("operation_semantics.repeat_prefixes.REPcc must be a mapping")
        return
    check_rule_id_map(
        repcc.get("observed_value_by_mnemonic"),
        "operation_semantics.repeat_prefixes.REPcc.observed_value_by_mnemonic",
        REP_OBSERVED_VALUE_RULES,
        result,
    )
    check_rule_id_map(
        repcc.get("repflags_by_mnemonic"),
        "operation_semantics.repeat_prefixes.REPcc.repflags_by_mnemonic",
        REPFLAGS_RULES,
        result,
    )


def check_rule_id_map(
    value: Any,
    path: str,
    allowed: set[str],
    result: ValidationResult,
) -> None:
    if value is None:
        return
    if not isinstance(value, dict):
        result.error(f"{path} must be a mapping")
        return
    for key, item in value.items():
        if not isinstance(item, str):
            result.error(f"{path}.{key} must be a rule id string")
        elif item not in allowed:
            expected = ", ".join(sorted(allowed))
            result.error(f"{path}.{key} has unknown rule id {item!r}; expected one of {expected}")


def check_rule_id_value(
    value: Any,
    path: str,
    allowed: set[str],
    result: ValidationResult,
) -> None:
    if not isinstance(value, str):
        result.error(f"{path} must be a rule id string")
    elif value not in allowed:
        expected = ", ".join(sorted(allowed))
        result.error(f"{path} has unknown rule id {value!r}; expected one of {expected}")


LEGACY_PCODE_PRIMITIVES = {
    "isa_unimplemented",
    "read_operand",
    "write_operand",
    "read_memory",
    "write_memory",
    "flags_add",
    "flags_sub",
    "flags_logic",
    "condition",
    "segment_translate",
    "effective_address",
}

OPAQUE_INSTRUCTION_PCODEOP_RE = re.compile(r"^\s*bedrock_[A-Za-z0-9_]+\s*\(\s*\)\s*;\s*$")
ISA_USER_PCODEOP_RE = re.compile(r"\bisa_[A-Za-z0-9_]*\s*\(")
PCODE_ROLE_VAR_RE = re.compile(r"\b([a-z][a-z0-9_]*?)_old_v\b|\b([a-z][a-z0-9_]*)_v\b")
LOCAL_PCODE_VAR_RE = re.compile(r"^\s*local\s+([A-Za-z][A-Za-z0-9_]*)(?::\d+)?\b")
UNSIZED_LOCAL_PCODE_VAR_RE = re.compile(r"^\s*local\s+[A-Za-z][A-Za-z0-9_]*\s*=")
PCODE_SCRATCH_ROLES = {"size", "result", "tmp", "carry", "borrow"}
CANONICAL_ROLE_ALIASES = (
    ("src", "imm"),
    ("src", "lhs"),
    ("dst", "rhs"),
    ("constant", "constant_id"),
    ("page", "src"),
)


def pcode_lines(value: Any) -> list[tuple[int, str]]:
    if isinstance(value, str):
        return [(index, line) for index, line in enumerate(value.splitlines())]
    if isinstance(value, list):
        return [(index, str(line)) for index, line in enumerate(value) if isinstance(line, str)]
    return []


def is_sleigh_pcode_label(text: str) -> bool:
    return bool(re.fullmatch(r"<[A-Za-z_][A-Za-z0-9_]*>", text))


def is_sleigh_pcode_comment(text: str) -> bool:
    return (
        not text
        or text.startswith("#")
        or text.startswith("//")
        or text.startswith("/*")
        or (text.startswith("*") and not text.startswith("*:"))
        or text.startswith("*/")
    )


def check_pcode_value(value: Any, path: str, result: ValidationResult) -> None:
    if not isinstance(value, (str, list)):
        result.error(f"{path} must be a SLEIGH p-code string or list of SLEIGH statement strings")
        return
    if isinstance(value, list):
        if not value:
            result.error(f"{path} must contain at least one SLEIGH statement")
            return
        for index, statement in enumerate(value):
            if not isinstance(statement, str):
                result.error(f"{path}[{index}] must be a SLEIGH statement string")
                continue
            if not statement.strip():
                result.error(f"{path}[{index}] must not be empty")
    elif not value.strip():
        result.error(f"{path} must not be empty")
        return

    saw_statement = False
    for index, raw_line in pcode_lines(value):
        line = raw_line.strip()
        if is_sleigh_pcode_comment(line):
            continue
        for primitive in LEGACY_PCODE_PRIMITIVES:
            if re.search(rf"\b{re.escape(primitive)}\s*\(", line):
                result.error(
                    f"{path}[{index}] uses legacy pseudo-code primitive {primitive}; "
                    "pcode must be literal Ghidra SLEIGH p-code"
                )
        if OPAQUE_INSTRUCTION_PCODEOP_RE.fullmatch(line):
            result.error(
                f"{path}[{index}] hides instruction semantics behind an opaque bedrock_* pcodeop; "
                "pcode must describe the SLEIGH semantic section directly"
            )
        if UNSIZED_LOCAL_PCODE_VAR_RE.match(line):
            result.error(
                f"{path}[{index}] declares a local p-code variable without an explicit size; "
                "use SLEIGH local syntax such as 'local tmp_v:8 = ...;'"
            )
        if ISA_USER_PCODEOP_RE.search(line):
            result.error(
                f"{path}[{index}] hides instruction semantics behind an isa_* user pcodeop; "
                "pcode must use Ghidra/SLEIGH built-in p-code operators directly"
            )
        if " then " in f" {line} " or line.endswith(" then"):
            result.error(f"{path}[{index}] uses pseudo-code 'then'; use SLEIGH branch syntax")
        if "fall_through" in line:
            result.error(f"{path}[{index}] uses pseudo-code fall_through; use SLEIGH control-flow syntax")
        if is_sleigh_pcode_label(line):
            saw_statement = True
            continue
        if not line.endswith(";"):
            result.error(f"{path}[{index}] SLEIGH p-code statements must end with ';'")
        else:
            saw_statement = True
    if not saw_statement:
        result.error(f"{path} must contain at least one SLEIGH p-code statement")


def check_pcode_by_form_value(value: Any, path: str, result: ValidationResult) -> None:
    if not isinstance(value, list) or not value:
        result.error(f"{path} must be a non-empty list")
        return
    for index, item in enumerate(value):
        item_path = f"{path}[{index}]"
        if not isinstance(item, dict):
            result.error(f"{item_path} must be a mapping")
            continue
        unexpected = sorted(set(item) - {"operands", "operation"})
        if unexpected:
            result.error(f"{item_path} has unexpected keys: {', '.join(unexpected)}")
        operands = item.get("operands")
        if "operands" in item and (
            not isinstance(operands, list) or not operands or not all(isinstance(op, str) for op in operands)
        ):
            result.error(f"{item_path}.operands must be a non-empty string list")
        if "operation" in item:
            check_pcode_value(item["operation"], f"{item_path}.operation", result)


def pcode_referenced_roles(value: Any) -> set[str]:
    local_roles: set[str] = set()
    for _index, raw_line in pcode_lines(value):
        match = LOCAL_PCODE_VAR_RE.match(raw_line)
        if match and match.group(1).endswith("_v"):
            local_roles.add(match.group(1)[:-2])

    out: set[str] = set()
    for _index, raw_line in pcode_lines(value):
        for match in PCODE_ROLE_VAR_RE.finditer(raw_line):
            role = match.group(1) or match.group(2)
            if role not in PCODE_SCRATCH_ROLES and role not in local_roles:
                out.add(role)
    return out


def semantic_role_names(value: Any) -> set[str]:
    if value is None:
        return set()
    if isinstance(value, dict):
        explicit = value.get("explicit")
        return {str(explicit)} if explicit else set()
    if isinstance(value, list):
        return {str(item) for item in value if str(item) != "none"}
    text = str(value).strip()
    if not text or text == "none":
        return set()
    return {text}


def expanded_form_roles(roles: set[str]) -> set[str]:
    out = set(roles)
    for canonical, alias in CANONICAL_ROLE_ALIASES:
        if alias in out:
            out.add(canonical)
    return out


def catalog_operand_forms_for_mnemonic(mnemonic: str, item: dict[str, Any]) -> list[tuple[str, set[str], list[Any]]]:
    forms: list[tuple[str, set[str], list[Any]]] = []

    def add_forms(path: str, value: Any) -> None:
        if isinstance(value, dict) and not is_operand_spec(value):
            value = value.get(mnemonic)
        parsed = operand_forms_from_value(value)
        if parsed is None:
            return
        for index, form in enumerate(parsed):
            roles = {str(operand.get("name")) for operand in form if isinstance(operand, dict)}
            forms.append((f"{path}[{index}]", roles, form))

    if "operands" in item:
        add_forms("operands", item.get("operands"))
    for form_key in ("compact_forms", "extended_forms"):
        for index, form in enumerate(item.get(form_key, []) or []):
            if isinstance(form, dict):
                add_forms(f"{form_key}[{index}].operands", form.get("operands"))
    return forms


def operand_form_kind_profile(form: list[Any]) -> list[str]:
    return [
        str(operand.get("type", "")).upper()
        for operand in form
        if isinstance(operand, dict)
    ]


def pcode_form_matches_catalog(form: dict[str, Any], operands: list[Any]) -> bool:
    expected = [str(kind).upper() for kind in form.get("operands", []) or []]
    return expected == operand_form_kind_profile(operands)


def check_pcode_form_role_bindings(
    mnemonic: str,
    entry: dict[str, Any],
    semantics: dict[str, Any],
    result: ValidationResult,
) -> None:
    common_required = set()
    common_required.update(pcode_referenced_roles(semantics.get("pcode")))
    common_required.update(semantic_role_names(semantics.get("inputs")))
    common_required.update(semantic_role_names(semantics.get("input_output")))
    common_required.update(semantic_role_names(semantics.get("output")))
    common_required.discard("none")
    form_pcode = [form for form in semantics.get("pcode_by_form", []) or [] if isinstance(form, dict)]
    for path, roles, operands in catalog_operand_forms_for_mnemonic(mnemonic, entry):
        required = set(common_required)
        matching_form_pcode = [
            form for form in form_pcode
            if pcode_form_matches_catalog(form, operands)
        ]
        for form in matching_form_pcode:
            required.update(pcode_referenced_roles(form.get("operation")))
        if form_pcode and not matching_form_pcode and "pcode" not in semantics:
            result.error(
                f"{mnemonic}.{path} has no matching operation_by_form pcode for operand kinds "
                + ", ".join(operand_form_kind_profile(operands))
            )
            continue
        missing = sorted(required - expanded_form_roles(roles))
        if missing:
            result.error(
                f"{mnemonic}.{path} does not bind operation role(s) "
                + ", ".join(missing)
            )


def check_canonical_alias_rules(catalog: dict[str, Any], spec: dict[str, Any], result: ValidationResult) -> None:
    rules = catalog.get("canonical_aliases", []) or []
    if not isinstance(rules, list):
        result.error("canonical_aliases must be a list")
        return

    entries = catalog_entry_map(catalog)
    declared_aliases = {
        mnemonic
        for mnemonic, item in entries.items()
        if isinstance(item, dict) and item.get("alias_of")
    }
    condition_names = {
        str(name)
        for condition in spec["conditions"].get("conditions", []) or []
        for name in [condition.get("name")] + list(condition.get("aliases", []) or [])
        if name
    }
    rule_aliases: set[str] = set()

    for index, rule in enumerate(rules):
        path = f"canonical_aliases[{index}]"
        if not isinstance(rule, dict):
            result.error(f"{path} must be a mapping")
            continue
        alias = str(rule.get("alias", ""))
        target = str(rule.get("target", ""))
        condition = str(rule.get("condition", ""))
        canonical = str(rule.get("canonical_disassembly", alias))
        if not alias or alias not in entries:
            result.error(f"{path}: alias {alias!r} is not a catalog mnemonic")
            continue
        if not target or target not in entries:
            result.error(f"{path}: target {target!r} is not a catalog mnemonic")
            continue
        if not condition:
            result.error(f"{path}: missing condition")
        elif condition not in condition_names:
            result.error(f"{path}: unknown condition {condition}")
        rule_aliases.add(alias)

        alias_body = entries[alias]
        target_body = entries[target]
        expected = f"{target}.{condition}"
        if alias_body.get("alias_of") != expected:
            result.error(f"{path}: {alias}.alias_of must be {expected}")
        if alias_body.get("canonical_disassembly") != canonical:
            result.error(f"{path}: {alias}.canonical_disassembly must be {canonical}")

        required_forms = rule.get("required_target_forms", []) or []
        if not isinstance(required_forms, list):
            result.error(f"{path}.required_target_forms must be a list")
            continue
        for form_index, form_types in enumerate(required_forms):
            if not isinstance(form_types, list):
                result.error(f"{path}.required_target_forms[{form_index}] must be a list")
                continue
            if not entry_has_operand_profile(target_body, [str(item) for item in form_types]):
                result.error(
                    f"{path}: target {target} is missing required form "
                    f"[{', '.join(str(item) for item in form_types)}]"
                )

    missing_rules = sorted(declared_aliases - rule_aliases)
    if missing_rules:
        result.error(
            "canonical_aliases missing rules for alias entries "
            + ", ".join(missing_rules)
        )


def catalog_entry_map(catalog: dict[str, Any]) -> dict[str, dict[str, Any]]:
    entries: dict[str, dict[str, Any]] = {}
    for _section, body in catalog_sections(catalog):
        if not isinstance(body, dict):
            continue
        for key, item in body.items():
            if not isinstance(item, dict):
                continue
            for mnemonic in semantic_entry_mnemonics(str(key), item):
                entries[mnemonic] = item
    return entries


def entry_has_operand_profile(item: dict[str, Any], types: list[str]) -> bool:
    values: list[Any] = []
    if "operands" in item:
        values.append(item.get("operands"))
    for form_key in ("compact_forms", "extended_forms"):
        for form in item.get(form_key, []) or []:
            if isinstance(form, dict) and "operands" in form:
                values.append(form.get("operands"))
    for value in values:
        forms = operand_forms_from_value(value)
        if forms is None:
            continue
        for form in forms:
            form_types = [
                str(operand.get("type"))
                for operand in form
                if isinstance(operand, dict)
            ]
            if form_types == types:
                return True
    return False


def check_catalog_entry(
    section: str,
    key: str,
    item: dict[str, Any],
    mnemonics: list[str],
    result: ValidationResult,
    operand_schema: dict[str, Any],
) -> None:
    path = f"{section}.{key}"
    check_no_unresolved_placeholders(item, path, result)
    for field in item:
        if str(field).endswith("_allowed"):
            result.error(f"{path}: field {field} is not allowed; encode choices in structured operands")
    if "alias" in item:
        result.error(f"{path}: legacy alias field is not allowed; use alias_of/canonical_disassembly")

    alias_of = item.get("alias_of")
    if alias_of:
        if not item.get("canonical_disassembly"):
            result.error(f"{path}: alias_of requires canonical_disassembly")
        for form_key in ("operands", "compact_forms", "extended_forms"):
            if form_key in item and item.get(form_key) not in (None, []):
                result.error(f"{path}: alias entries must not declare {form_key}; declare forms on the target")
        return

    has_any_forms = False
    if "operands" in item:
        has_any_forms = True
        check_operand_declaration(item.get("operands"), path, mnemonics, result, operand_schema)

    for form_key in ("compact_forms", "extended_forms"):
        if form_key not in item:
            continue
        has_any_forms = True
        forms = item.get(form_key)
        if not isinstance(forms, list) or not forms:
            result.error(f"{path}.{form_key} must be a non-empty list")
            continue
        for index, form in enumerate(forms):
            form_path = f"{path}.{form_key}[{index}]"
            if not isinstance(form, dict):
                result.error(f"{form_path} must be a mapping")
                continue
            if "operands" not in form:
                result.error(f"{form_path} missing operands")
                continue
            check_operand_declaration(
                form.get("operands"), form_path, mnemonics, result, operand_schema
            )

    if not has_any_forms:
        result.error(f"{path}: non-alias entry must declare operands or explicit forms")


def check_no_unresolved_placeholders(value: Any, path: str, result: ValidationResult) -> None:
    if isinstance(value, str):
        if value == "TBD":
            result.error(f"{path}: unresolved TBD value")
        return
    if isinstance(value, list):
        for index, item in enumerate(value):
            check_no_unresolved_placeholders(item, f"{path}[{index}]", result)
        return
    if isinstance(value, dict):
        for key, item in value.items():
            check_no_unresolved_placeholders(item, f"{path}.{key}", result)


def check_operand_declaration(
    value: Any,
    path: str,
    mnemonics: list[str],
    result: ValidationResult,
    operand_schema: dict[str, Any],
) -> None:
    if isinstance(value, dict) and not is_operand_spec(value):
        expected = set(mnemonics)
        actual = {str(key) for key in value}
        unknown = sorted(actual - expected)
        missing = sorted(expected - actual)
        if unknown:
            result.error(f"{path}.operands contains unknown mnemonic keys {', '.join(unknown)}")
        if missing:
            result.error(f"{path}.operands missing mnemonic keys {', '.join(missing)}")
        for mnemonic, operands in value.items():
            check_operand_declaration(
                operands,
                f"{path}.operands.{mnemonic}",
                [str(mnemonic)],
                result,
                operand_schema,
            )
        return

    forms = operand_forms_from_value(value)
    if forms is None:
        result.error(f"{path}.operands must be a list of operand mappings or alternatives")
        return
    for form_index, form in enumerate(forms):
        for operand_index, operand in enumerate(form):
            check_operand_spec(
                operand,
                f"{path}.operands[{form_index}][{operand_index}]",
                result,
                operand_schema,
            )


def operand_forms_from_value(value: Any) -> list[list[Any]] | None:
    if value is None:
        return None
    if isinstance(value, dict):
        return [[value]] if is_operand_spec(value) else None
    if not isinstance(value, list):
        return None
    if not value:
        return [[]]
    if all(is_operand_spec(item) for item in value):
        return [list(value)]
    if all(isinstance(item, list) for item in value):
        forms: list[list[Any]] = []
        for item in value:
            if not all(is_operand_spec(operand) for operand in item):
                return None
            forms.append(list(item))
        return forms
    return None


def is_operand_spec(value: Any) -> bool:
    return isinstance(value, dict) and "name" in value and "type" in value


def check_operand_spec(
    operand: Any, path: str, result: ValidationResult, operand_schema: dict[str, Any]
) -> None:
    if not is_operand_spec(operand):
        result.error(f"{path}: operand must be {{name, type}}")
        return
    extra = sorted(set(operand) - {"name", "type"})
    if extra:
        result.error(f"{path}: unknown operand keys {', '.join(extra)}")
    name = str(operand.get("name", ""))
    typ = str(operand.get("type", ""))
    role_re = re.compile(str(operand_schema.get("role_name_pattern", r"^[a-z][a-z0-9_]*$")))
    if not role_re.match(name):
        result.error(f"{path}: operand name {name!r} must be lower_snake_case")
    types = operand_schema.get("types", set())
    if types and typ not in types:
        result.error(f"{path}: unknown operand type {typ!r}")
    condition_role = str(operand_schema.get("condition_role", "cc"))
    if typ == "condition" and name != condition_role:
        result.error(f"{path}: condition operand must use name {condition_role}")
    selector_roles = operand_schema.get("selector_roles", set())
    if typ == "selector" and selector_roles and name not in selector_roles:
        result.error(
            f"{path}: selector operand must be one of {', '.join(sorted(selector_roles))}"
        )




def check_overlaps(entries: list[PatternEntry], result: ValidationResult) -> None:
    for index, left in enumerate(entries):
        for right in entries[index + 1 :]:
            if not patterns_overlap(left.pattern, right.pattern):
                continue
            if overlap_allowed(left, right):
                result.info(f"allowed overlap: {left.id} <-> {right.id}")
                continue
            if "reserved" in (left.kind, right.kind):
                result.error(f"reserved-space collision: {left.id} <-> {right.id}")
            else:
                result.error(f"opcode overlap: {left.id} <-> {right.id}")
