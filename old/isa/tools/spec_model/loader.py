from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError as exc:  # pragma: no cover - exercised only on incomplete hosts
    raise SystemExit("PyYAML is required: python3 -m pip install pyyaml") from exc

from .core import SpecError, UniqueKeyLoader, is_scalar_value, schema_keys
from .catalog import instruction_catalog
from .schemas import (
    CatalogEntrySchema,
    LocalAllocationSchema,
    LocalAttributesSchema,
    LocalBehaviorSchema,
    LocalDocSchema,
    LocalInstructionSchema,
    SpecDocumentSchema,
    MEMORY_RULES,
    REP_OBSERVED_VALUE_RULES,
    REPFLAGS_RULES,
)

SPEC_FILES = (
    "registers.yaml",
    "segments.yaml",
    "prefixes.yaml",
    "conditions.yaml",
    "ea.yaml",
    "instructions.yaml",
    "opcodes.yaml",
    "semantics.yaml",
    "interrupts.yaml",
    "cpuid.yaml",
    "terminology.yaml",
)
CONTROL_REGISTER_ACCESS_CLASS = "CR"


def checked_rule_id(value: Any, path: Path | str, field: str, allowed: set[str]) -> str:
    if not isinstance(value, str):
        raise SpecError(f"{path}: {field} must be a rule id string")
    if value not in allowed:
        expected = ", ".join(sorted(allowed))
        raise SpecError(f"{path}: {field} has unknown rule id {value!r}; expected one of {expected}")
    return value


def checked_memory_rule(value: Any, path: Path) -> str:
    return checked_rule_id(value, path, "memory", MEMORY_RULES)


def load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as fp:
        data = yaml.load(fp, Loader=UniqueKeyLoader)
    return data or {}


def expand_local_instruction_fragment(
    data: dict[str, Any],
    path: Path,
) -> dict[str, Any]:
    if "mnemonic" not in data:
        return data
    mnemonic = str(data.get("mnemonic") or "").strip()
    if not mnemonic:
        raise SpecError(f"{path}: mnemonic must not be empty")
    local_errors: list[str] = []
    LocalInstructionSchema.validate(data, str(path), local_errors)
    if local_errors:
        raise SpecError(f"{path}: " + "; ".join(local_errors))

    out: dict[str, Any] = {}
    doc = data.get("doc")
    doc_info = doc or {}
    if doc is not None:
        if not isinstance(doc, dict):
            raise SpecError(f"{path}: doc must be a mapping")
        unexpected_doc = sorted(set(doc) - schema_keys(LocalDocSchema))
        if unexpected_doc:
            raise SpecError(f"{path}: unexpected doc keys: {', '.join(unexpected_doc)}")
        out["instruction_docs"] = {mnemonic: deepcopy(doc)}

    behavior = data.get("behavior") or {}
    attributes = data.get("attributes") or {}
    if behavior or attributes:
        if not isinstance(behavior, dict):
            raise SpecError(f"{path}: behavior must be a mapping")
        if not isinstance(attributes, dict):
            raise SpecError(f"{path}: attributes must be a mapping")
        overlap = sorted(set(behavior) & set(attributes))
        if overlap:
            raise SpecError(
                f"{path}: behavior and attributes share keys: {', '.join(overlap)}"
            )
        for source_name, source_body, source_schema in (
            ("behavior", behavior, LocalBehaviorSchema),
            ("attributes", attributes, LocalAttributesSchema),
        ):
            unexpected_semantics = sorted(set(source_body) - source_schema.key_set())
            if unexpected_semantics:
                raise SpecError(
                    f"{path}: unexpected {source_name} keys: "
                    + ", ".join(unexpected_semantics)
                )
        group_name = str(
            behavior.get("group")
            or attributes.get("group")
            or doc_info.get("instruction_family")
            or mnemonic
        )
        body = {
            key: deepcopy(value)
            for source in (behavior, attributes)
            for key, value in source.items()
            if key != "group"
        }
        local_operation = body.pop("operation", None)
        local_operation_text = body.pop("operation_text", None)
        local_operation_by_form = body.pop("operation_by_form", None)
        local_meta = {
            key: body.pop(key)
            for key in (
                "prefix_availability",
                "streaming_candidate",
            )
            if key in body
        }
        if "memory" in body:
            body["memory"] = checked_memory_rule(body["memory"], path)
        local_operation_metadata = local_operation_metadata_fragment(
            mnemonic,
            local_meta,
            doc_info,
            path,
        )
        if local_operation_metadata:
            out = merge_spec_fragment(out, local_operation_metadata, "")
        out = merge_spec_fragment(
            out,
            {"operation_semantics": {"groups": {group_name: {"members": [mnemonic]}}}},
            "",
        )
        instruction_entry = deepcopy(body)
        if local_operation is not None:
            instruction_entry["pcode"] = deepcopy(local_operation)
        if local_operation_text is not None:
            instruction_entry["operation_text"] = deepcopy(local_operation_text)
        if local_operation_by_form is not None:
            instruction_entry["pcode_by_form"] = deepcopy(local_operation_by_form)
        if instruction_entry:
            out = merge_spec_fragment(
                out,
                {"operation_semantics": {"instructions": {mnemonic: instruction_entry}}},
                "",
            )

    allocation = data.get("allocation") or {}
    forms = data.get("forms")
    if forms is not None:
        if not isinstance(allocation, dict):
            raise SpecError(f"{path}: allocation must be a mapping")
        allocation_errors: list[str] = []
        LocalAllocationSchema.validate(allocation, f"{path}.allocation", allocation_errors)
        if allocation_errors:
            raise SpecError(f"{path}: " + "; ".join(allocation_errors))
        if not isinstance(doc_info, dict):
            raise SpecError(f"{path}: doc must be a mapping")
        family = str(
            doc_info.get("instruction_family")
            or ""
        ).strip()
        category = str(doc_info.get("instruction_class") or "").strip()
        section = str(
            allocation.get("catalog_section")
            or ""
        ).strip()
        if not family or not category or not section:
            raise SpecError(f"{path}: local instruction classification fields must not be empty")
        entry_group = str(
            allocation.get("layout_group")
            or mnemonic
        ).strip()
        body = deepcopy(forms)
        if not isinstance(body, dict):
            raise SpecError(f"{path}: forms must be a mapping")
        unexpected_forms = sorted(set(body) - schema_keys(CatalogEntrySchema))
        if unexpected_forms:
            raise SpecError(f"{path}: unexpected forms keys: {', '.join(unexpected_forms)}")
        if "fixed_encoding" in allocation:
            body["fixed_encoding"] = deepcopy(allocation["fixed_encoding"])
        if "encoding" in allocation:
            body["encoding"] = deepcopy(allocation["encoding"])
        body.setdefault("semantic_family", family)
        body.setdefault("mnemonics", [mnemonic])
        entry_key = mnemonic if entry_group == mnemonic else f"{entry_group}.{mnemonic}"
        family_body: dict[str, Any] = {section: {entry_key: body}}
        family_body["category"] = category
        out = merge_spec_fragment(out, {"families": {family: family_body}}, "")
        alias_rule = canonical_alias_rule(mnemonic, body)
        if alias_rule:
            out = merge_spec_fragment(out, {"canonical_aliases": [alias_rule]}, "")

    return out


def operation_attribute_domain(doc_info: dict[str, Any], path: Path) -> str:
    instruction_class = str(doc_info.get("instruction_class") or "").strip()
    if instruction_class == "fpu":
        return "fpu"
    return "integer"


def local_operation_metadata_fragment(
    mnemonic: str,
    meta: dict[str, Any],
    doc_info: dict[str, Any],
    path: Path,
) -> dict[str, Any]:
    fragment: dict[str, Any] = {}

    def merge(value: dict[str, Any]) -> None:
        nonlocal fragment
        fragment = merge_spec_fragment(fragment, value, "")

    streaming_candidate = meta.get("streaming_candidate")
    if streaming_candidate not in (None, False):
        if streaming_candidate is not True:
            raise SpecError(f"{path}: streaming_candidate must be true when present")
        domain = operation_attribute_domain(doc_info, path)
        merge(
            {
                "operation_semantics": {
                    "operation_attributes": {
                        "streaming_candidate": {domain: [mnemonic]}
                    }
                }
            }
        )

    prefixes = meta.get("prefix_availability")
    if prefixes:
        if isinstance(prefixes, str):
            prefix_names = [prefixes]
        elif isinstance(prefixes, list) and all(isinstance(item, str) for item in prefixes):
            prefix_names = prefixes
        else:
            raise SpecError(f"{path}: prefix_availability must be a string or string list")
        for prefix_name in prefix_names:
            merge(
                {
                    "operation_semantics": {
                        "prefix_availability": {
                            prefix_name: {"mnemonics": [mnemonic]}
                        }
                    }
                }
            )

    return fragment


def canonical_alias_rule(mnemonic: str, forms: dict[str, Any]) -> dict[str, Any] | None:
    alias_of = forms.get("alias_of")
    if not alias_of:
        return None
    alias_text = str(alias_of)
    if "." not in alias_text:
        return None
    target, condition = alias_text.rsplit(".", 1)
    rule = {
        "alias": mnemonic,
        "target": target,
        "condition": condition,
        "canonical_disassembly": str(forms.get("canonical_disassembly") or mnemonic),
    }
    required_forms = required_alias_forms(forms.get("aliases"))
    if required_forms:
        rule["required_target_forms"] = required_forms
    return rule


def required_alias_forms(aliases: Any) -> list[list[str]]:
    if not isinstance(aliases, list):
        return []
    out: list[list[str]] = []
    for item in aliases:
        if not isinstance(item, str):
            continue
        tokens = item.split()
        if not tokens:
            continue
        head = tokens[0]
        operands = tokens[1:]
        if "." in head:
            operands = ["condition", *operands]
        if operands and operands not in out:
            out.append(operands)
    return out


def merge_spec_fragment(base: dict[str, Any], fragment: dict[str, Any], path: str) -> dict[str, Any]:
    merged = deepcopy(base)
    for key, value in fragment.items():
        key_path = f"{path}.{key}" if path else str(key)
        if key not in merged:
            merged[key] = deepcopy(value)
            continue
        existing = merged[key]
        if isinstance(existing, dict) and isinstance(value, dict):
            merged[key] = merge_spec_fragment(existing, value, key_path)
        elif isinstance(existing, list) and isinstance(value, list):
            merged[key] = deepcopy(existing) + deepcopy(value)
        elif existing == value:
            continue
        else:
            raise SpecError(f"conflicting included spec values at {key_path}")
    return merged


def load_yaml_with_includes(
    path: Path,
    stack: tuple[Path, ...] = (),
) -> dict[str, Any]:
    resolved = path.resolve()
    if resolved in stack:
        chain = " -> ".join(str(item) for item in (*stack, resolved))
        raise SpecError(f"recursive spec include: {chain}")
    data = load_yaml(path)
    if not isinstance(data, dict):
        raise SpecError(f"{path} must contain a mapping")

    includes = data.pop("include", []) or []
    if isinstance(includes, str):
        includes = [includes]
    if not isinstance(includes, list) or not all(isinstance(item, str) for item in includes):
        raise SpecError(f"{path}: include must be a string or a list of strings")

    merged = expand_local_instruction_fragment(deepcopy(data), path)
    next_stack = (*stack, resolved)
    for include in includes:
        include_path = (path.parent / include).resolve()
        if not include_path.exists():
            raise SpecError(f"{path}: included spec file not found: {include}")
        fragment = load_yaml_with_includes(include_path, next_stack)
        merged = merge_spec_fragment(merged, fragment, "")
    return merged


def load_spec(spec_dir: str | Path) -> dict[str, Any]:
    root = Path(spec_dir)
    spec: dict[str, Any] = {"__dir__": root}
    missing = [name for name in SPEC_FILES if not (root / name).exists()]
    if missing:
        raise SpecError(f"missing spec files: {', '.join(missing)}")
    for name in SPEC_FILES:
        spec[name[:-5]] = load_yaml_with_includes(root / name)
    normalize_loaded_spec(spec)
    SpecDocumentSchema.validate_or_raise(spec)
    return spec


def normalize_loaded_spec(spec: dict[str, Any]) -> None:
    groups = (
        ((spec.get("instructions") or {}).get("operation_semantics") or {}).get("groups")
        or {}
    )
    if not isinstance(groups, dict):
        return
    for group in groups.values():
        if not isinstance(group, dict):
            continue
        members = group.get("members")
        if isinstance(members, list):
            group["members"] = unique_preserve_order(members)
        dedupe_scalar_lists(group)
    derive_repeat_prefix_semantics(spec)
    dedupe_scalar_lists(
        ((spec.get("instructions") or {}).get("operation_semantics") or {})
    )
    derive_control_register_access_pcode(spec)
    derive_condition_code_applies_to(spec)


def parse_int_value(value: Any) -> int:
    if isinstance(value, int):
        return value
    return int(str(value), 0)


def prefix_entry(spec: dict[str, Any], name: str) -> dict[str, Any] | None:
    for prefix in (spec.get("prefixes") or {}).get("prefixes", []) or []:
        if isinstance(prefix, dict) and prefix.get("name") == name:
            return prefix
    return None


def derive_repeat_prefix_semantics(spec: dict[str, Any]) -> None:
    repcc_prefix = prefix_entry(spec, "REPcc")
    if not isinstance(repcc_prefix, dict):
        return
    operation_semantics = (spec.get("instructions") or {}).get("operation_semantics") or {}
    if not isinstance(operation_semantics, dict):
        return
    repeat_prefixes = operation_semantics.setdefault("repeat_prefixes", {})
    if not isinstance(repeat_prefixes, dict):
        raise SpecError("operation_semantics.repeat_prefixes must be a mapping")
    repcc = repeat_prefixes.setdefault("REPcc", {})
    if not isinstance(repcc, dict):
        raise SpecError("operation_semantics.repeat_prefixes.REPcc must be a mapping")

    derive_repeat_rule_map_from_instructions(
        repcc,
        operation_semantics,
        "repeat_observed_value",
        "observed_values",
        REP_OBSERVED_VALUE_RULES,
    )
    derive_repeat_rule_map_from_instructions(
        repcc,
        operation_semantics,
        "repflags",
        "repflag_rules",
        REPFLAGS_RULES,
    )
    fpu_conditional = repcc_prefix.get("fpu_conditional_mnemonics")
    if fpu_conditional is not None:
        if not isinstance(fpu_conditional, list) or not all(isinstance(item, str) for item in fpu_conditional):
            raise SpecError("prefixes.yaml REPcc.fpu_conditional_mnemonics must be a string list")
        set_derived_repeat_value(repcc, "fpu_conditional_mnemonics", list(fpu_conditional))


def derive_repeat_rule_map_from_instructions(
    repcc: dict[str, Any],
    operation_semantics: dict[str, Any],
    source_key: str,
    target_key: str,
    allowed: set[str],
) -> None:
    instructions = operation_semantics.get("instructions") or {}
    if not isinstance(instructions, dict):
        return
    derived: dict[str, str] = {}
    for mnemonic, entry in instructions.items():
        if not isinstance(entry, dict):
            continue
        source = entry.get(source_key)
        if source is None:
            continue
        mnemonic_key = str(mnemonic)
        rule_id = checked_rule_id(
            source,
            "instruction semantics",
            f"instructions.{mnemonic_key}.{source_key}",
            allowed,
        )
        previous = derived.get(mnemonic_key)
        if previous is not None and previous != rule_id:
            raise SpecError(
                f"operation_semantics instructions define conflicting REPcc {source_key} "
                f"rules for {mnemonic_key}: {previous} and {rule_id}"
            )
        derived[mnemonic_key] = rule_id
    if derived:
        set_derived_repeat_value(repcc, target_key, derived, source_key)


def set_derived_repeat_value(repcc: dict[str, Any], key: str, value: Any, source: str = "derived metadata") -> None:
    if key in repcc and repcc[key] != value:
        raise SpecError(f"operation_semantics.repeat_prefixes.REPcc.{key} conflicts with {source}")
    repcc[key] = value


def control_register_selectors(spec: dict[str, Any]) -> list[tuple[int, str]]:
    control_classes = (spec.get("registers") or {}).get("control_register_classes") or {}
    cr_class = control_classes.get(CONTROL_REGISTER_ACCESS_CLASS) or {}
    selectors: list[tuple[int, str]] = []
    if not isinstance(cr_class, dict):
        return selectors
    for group in cr_class.get("selector_groups", []) or []:
        if not isinstance(group, dict):
            continue
        for selector in group.get("selectors", []) or []:
            if not isinstance(selector, dict):
                continue
            selectors.append((parse_int_value(selector.get("value", 0)), str(selector.get("register", ""))))
    return selectors


def control_register_access_pcode(spec: dict[str, Any], mnemonic: str, access: dict[str, Any]) -> list[str]:
    unexpected = sorted(set(access) - {"selector", "read", "write"})
    if unexpected:
        raise SpecError(
            f"{mnemonic}: control_register_access has unexpected keys: "
            + ", ".join(unexpected)
        )
    selector_role = str(access.get("selector") or "cr")
    read_role = access.get("read")
    write_role = access.get("write")
    if bool(read_role) == bool(write_role):
        raise SpecError(f"{mnemonic}: control_register_access must specify exactly one of read or write")

    selector_var = f"{selector_role}_v"
    prefix = mnemonic.lower()
    done_label = f"<{prefix}_done>"
    invalid_label = f"<{prefix}_invalid>"
    selectors = control_register_selectors(spec)
    if not selectors:
        raise SpecError(
            f"{mnemonic}: control register class {CONTROL_REGISTER_ACCESS_CLASS} has no selectors"
        )

    lines: list[str] = []
    for index, (value, register) in enumerate(selectors):
        next_label = invalid_label if index == len(selectors) - 1 else f"<{prefix}_{selectors[index + 1][1].lower()}>"
        lines.append(f"if ({selector_var} != 0x{value:04x}) goto {next_label};")
        if read_role:
            lines.append(f"{read_role}_v = {register};")
        else:
            lines.append(f"{register} = {write_role}_v;")
        lines.append(f"goto {done_label};")
        if index != len(selectors) - 1:
            lines.append(next_label)
    lines.append(invalid_label)
    lines.append(f"arch_raise_invalid_control_state({selector_var});")
    lines.append(done_label)
    return lines


def derive_control_register_access_pcode(spec: dict[str, Any]) -> None:
    operation_semantics = (spec.get("instructions") or {}).get("operation_semantics") or {}
    if not isinstance(operation_semantics, dict):
        return
    explicit = operation_semantics.setdefault("instructions", {})
    if not isinstance(explicit, dict):
        raise SpecError("operation_semantics.instructions must be a mapping")
    for mnemonic, entry in explicit.items():
        if not isinstance(entry, dict):
            continue
        access = entry.get("control_register_access")
        if access is None:
            continue
        if not isinstance(access, dict):
            raise SpecError(f"{mnemonic}: control_register_access must be a mapping")
        if "pcode" in entry or "pcode_by_form" in entry:
            raise SpecError(f"{mnemonic}: control_register_access conflicts with explicit pcode")
        entry["pcode"] = control_register_access_pcode(spec, str(mnemonic), access)


def derive_condition_code_applies_to(spec: dict[str, Any]) -> None:
    operation_semantics = (spec.get("instructions") or {}).get("operation_semantics") or {}
    if not isinstance(operation_semantics, dict):
        return
    syntax_policy = operation_semantics.get("syntax_policy") or {}
    if not isinstance(syntax_policy, dict):
        return
    condition_code = syntax_policy.get("condition_code") or {}
    if not isinstance(condition_code, dict) or condition_code.get("applies_to"):
        return

    applies_to: list[str] = []
    try:
        entries = mnemonic_catalog_entries(instruction_catalog(spec))
    except SpecError:
        entries = {}
    for mnemonic, item in entries.items():
        if entry_has_operand_type(item, "condition"):
            applies_to.append(mnemonic)

    for prefix in (spec.get("prefixes") or {}).get("prefixes", []) or []:
        if not isinstance(prefix, dict):
            continue
        if prefix.get("condition") or (
            isinstance(prefix.get("syntax"), dict)
            and prefix["syntax"].get("condition_suffix")
        ):
            name = prefix.get("name")
            if name:
                applies_to.append(str(name))

    if applies_to:
        condition_code["applies_to"] = unique_preserve_order(applies_to)
        syntax_policy["condition_code"] = condition_code
        operation_semantics["syntax_policy"] = syntax_policy


def entry_has_operand_type(value: Any, operand_type: str) -> bool:
    if isinstance(value, dict):
        if value.get("type") == operand_type:
            return True
        return any(entry_has_operand_type(item, operand_type) for item in value.values())
    if isinstance(value, list):
        return any(entry_has_operand_type(item, operand_type) for item in value)
    return False


def mnemonic_catalog_entries(catalog: dict[str, Any]) -> dict[str, dict[str, Any]]:
    entries: dict[str, dict[str, Any]] = {}
    sections = [
        catalog.get("compact_primary_instructions"),
        catalog.get("integer_instructions"),
        catalog.get("atomic_system_cache_instructions"),
        (catalog.get("fpu") or {}).get("instructions")
        if isinstance(catalog.get("fpu"), dict)
        else None,
    ]
    for section in sections:
        if not isinstance(section, dict):
            continue
        for key, item in section.items():
            if not isinstance(item, dict):
                continue
            mnemonics = item.get("mnemonics")
            if isinstance(mnemonics, list):
                names = [str(mnemonic) for mnemonic in mnemonics]
            else:
                names = [str(key).split(".")[-1]]
            for mnemonic in names:
                entries[mnemonic] = item
    return entries


def unique_preserve_order(values: list[Any]) -> list[Any]:
    seen: set[str] = set()
    out: list[Any] = []
    for value in values:
        key = str(value)
        if key in seen:
            continue
        seen.add(key)
        out.append(value)
    return out


def dedupe_scalar_lists(value: Any) -> Any:
    if isinstance(value, dict):
        for key, item in list(value.items()):
            if key in {"pcode", "operation", "operands"}:
                continue
            value[key] = dedupe_scalar_lists(item)
        return value
    if isinstance(value, list):
        if all(is_scalar_value(item) for item in value):
            return unique_preserve_order(value)
        return [dedupe_scalar_lists(item) for item in value]
    return value
