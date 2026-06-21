"""Instruction candidate generation for the opcode allocator."""

from __future__ import annotations

from typing import Any
import math

from alloc_model import *
from isa_spec import (
    PatternEntry,
    cleaned_pattern,
    instruction_catalog,
    semantic_entry_mnemonics,
)
from spec_model.encoding import (
    bitmap_operand,
    compact_ea_forms,
    condition_entries,
    int_value,
    named_value_width,
    register_class_count,
    size_kind_field,
    size_kind_width,
    size_kinds as spec_size_kinds,
    special_register_class,
)


ACTIVE_SPEC: dict[str, Any] | None = None


def set_active_spec(spec: dict[str, Any]) -> None:
    global ACTIVE_SPEC
    ACTIVE_SPEC = spec


def active_spec() -> dict[str, Any]:
    if ACTIVE_SPEC is None:
        raise RuntimeError("active ISA spec is not set")
    return ACTIVE_SPEC


def is_declared_size_kind(kind: str) -> bool:
    return kind.upper() in spec_size_kinds(active_spec())


def get_path(data: dict[str, Any], dotted: str) -> Any:
    current: Any = data
    for part in dotted.split("."):
        if not isinstance(current, dict):
            return None
        current = current.get(part)
    return current


def bits_needed(count: int) -> int:
    if count <= 1:
        return 0
    return math.ceil(math.log2(count))


def register_field_width(class_name: str) -> int:
    return bits_needed(register_class_count(active_spec(), class_name))


def special_register_field_width(class_name: str) -> int:
    body = special_register_class(active_spec(), class_name)
    return int(body.get("encoding_bits", bits_needed(len(body.get("encoding", []) or []))))


def dbank_field_width() -> int:
    banking = (active_spec().get("registers", {}) or {}).get("data_register_banking", {})
    selector = (banking or {}).get("selector", {}) if isinstance(banking, dict) else {}
    return int(selector.get("width", 0))


def condition_field_width() -> int:
    values = [int_value(item.get("value")) for item in condition_entries(active_spec())]
    return bits_needed(max(values) + 1) if values else 0


def bitmap_field_width(name: str) -> int:
    return int(bitmap_operand(active_spec(), name).get("width", 0))


def ea_field_width() -> int:
    widths = {len(str(form.get("pattern", "")).replace(" ", "")) for form in compact_ea_forms(active_spec())}
    if len(widths) != 1:
        raise ValueError(f"compact EA forms must have one selector width, got {sorted(widths)}")
    return widths.pop()


def data_or_address_field_width() -> int:
    return 1 + max(register_field_width("D"), register_field_width("A"))


def ceil_words(bits: int) -> int:
    if bits <= 0:
        return 0
    return (bits + 15) // 16


def fixed_primary_payload(body: dict[str, Any]) -> int | None:
    fixed = body.get("fixed_encoding")
    if not isinstance(fixed, dict) or "primary_payload" not in fixed:
        return None
    value = fixed["primary_payload"]
    if isinstance(value, int):
        return value
    return int(str(value), 0)


def instruction_operands(entry: PatternEntry) -> tuple[str, ...]:
    out = []
    for operand in entry.source.get("operands", []) or []:
        text = operand_spec_text(operand)
        if text:
            out.append(text)
    return tuple(out)


def operand_spec_text(operand: Any) -> str:
    if isinstance(operand, dict):
        name = str(operand.get("name") or operand.get("role") or operand.get("type") or "operand")
        typ = str(operand.get("type") or operand.get("kind") or name)
        return name if name.upper() == typ.upper() else f"{name}:{typ}"
    return str(operand)


def split_operand_spec(operand: str) -> tuple[str, str]:
    if ":" in operand:
        source, typ = operand.split(":", 1)
        return source, typ
    return operand, operand


def condition_value(spec: dict[str, Any], name: str) -> int:
    for condition in spec["conditions"].get("conditions", []) or []:
        names = [condition.get("name")] + list(condition.get("aliases", []) or [])
        if name in {str(item) for item in names if item}:
            return int(condition["value"])
    raise KeyError(f"unknown condition {name}")


def canonical_alias_rules(spec: dict[str, Any]) -> list[dict[str, Any]]:
    rules: list[dict[str, Any]] = []
    for rule in instruction_catalog(spec).get("canonical_aliases", []) or []:
        if not isinstance(rule, dict):
            continue
        condition = str(rule.get("condition", ""))
        rules.append(
            {
                "alias": str(rule.get("alias", "")),
                "target": str(rule.get("target", "")),
                "condition": condition,
                "condition_value": condition_value(spec, condition),
                "required_target_forms": [
                    [str(item) for item in form]
                    for form in rule.get("required_target_forms", []) or []
                    if isinstance(form, list)
                ],
            }
        )
    return [rule for rule in rules if rule["alias"] and rule["target"] and rule["condition"]]


def canonical_alias_sources(spec: dict[str, Any]) -> set[str]:
    return {rule["alias"].upper() for rule in canonical_alias_rules(spec)}


def canonical_alias_family_mnemonics(spec: dict[str, Any]) -> list[str]:
    names: set[str] = set()
    for rule in canonical_alias_rules(spec):
        names.add(rule["alias"].upper())
        names.add(rule["target"].upper())
    return sorted(names)


def alias_rules_by_target(alias_rules: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {rule["target"]: rule for rule in alias_rules}


def collect_candidates(spec: dict[str, Any], entries: list[PatternEntry]) -> list[Candidate]:
    set_active_spec(spec)
    candidates: list[Candidate] = []
    catalog = instruction_catalog(spec)
    allocation = allocation_params(spec)
    alias_sources = canonical_alias_sources(spec)
    allocated_mnemonics = {
        entry.mnemonic
        for entry in entries
        if entry.kind == "instruction"
    }

    for entry in entries:
        if entry.kind in {"reserved", "extension_space"}:
            continue
        if entry.kind != "instruction":
            continue
        if entry.mnemonic.upper() in alias_sources:
            continue
        operands = instruction_operands(entry)
        candidates.append(
            build_candidate(
                ident=instruction_candidate_id(entry, operands),
                mnemonic=entry.mnemonic,
                category=instruction_category(entry),
                group=str(entry.source.get("form") or entry.source.get("class") or entry.mnemonic),
                operands=operands,
                body=entry.source,
                allocation=allocation,
                origin="instructions.yaml",
                shape_hint=str(entry.source.get("pattern", "")),
                must_compact=False,
                can_extend=True,
                fixed_payload=fixed_primary_payload(entry.source),
            )
        )

    candidates.extend(semantic_compact_primary_candidates(spec, allocated_mnemonics, alias_sources))
    candidates.extend(semantic_extended_form_candidates(spec, allocated_mnemonics))
    for section_path, category, default_weight in SEMANTIC_SECTIONS:
        section = get_path(catalog, section_path)
        if not isinstance(section, dict):
            continue
        for group, body in section.items():
            if not isinstance(body, dict):
                continue
            for mnemonic in semantic_entry_mnemonics(str(group), body):
                if mnemonic in allocated_mnemonics:
                    continue
                for operands in semantic_operand_alternatives(mnemonic, body):
                    merged = body_with_operation_metadata(spec, mnemonic, body)
                    ident = semantic_candidate_id(mnemonic, operands, merged)
                    item_category = semantic_category_from_body(merged, category)
                    candidates.append(
                        build_candidate(
                            ident=ident,
                            mnemonic=mnemonic,
                            category=item_category,
                            group=str(group),
                            operands=tuple(operands),
                            body=merged,
                            allocation=allocation,
                            origin="instructions.yaml",
                            shape_hint="semantic_operands",
                            must_compact=False,
                            can_extend=fixed_primary_payload(merged) is None,
                            fixed_payload=fixed_primary_payload(merged),
                            default_weight=default_weight,
                        )
                    )
    return uniquify_candidate_ids(candidates)


def allocation_params(spec: dict[str, Any]) -> dict[str, Any]:
    params = instruction_catalog(spec).get("allocation") or {}
    return params if isinstance(params, dict) else {}


OPERATION_METADATA_KEYS = (
    "privilege",
    "atomic",
    "memory",
    "flags",
    "fp_flags",
    "serializing",
    "signedness",
    "bounds_mode",
    "interval",
    "destination_size",
    "output",
)


def body_with_operation_metadata(
    spec: dict[str, Any],
    mnemonic: str,
    body: dict[str, Any],
) -> dict[str, Any]:
    metadata = operation_metadata_for_mnemonic(spec, mnemonic)
    if not metadata:
        return dict(body)
    merged = dict(body)
    for key, value in metadata.items():
        merged.setdefault(key, value)
    return merged


def operation_metadata_for_mnemonic(spec: dict[str, Any], mnemonic: str) -> dict[str, Any]:
    groups = (((spec.get("instructions") or {}).get("operation_semantics") or {}).get("groups") or {})
    if not isinstance(groups, dict):
        return {}
    out: dict[str, Any] = {}
    for group in groups.values():
        if not isinstance(group, dict):
            continue
        members = {str(member) for member in group.get("members", []) or []}
        if mnemonic not in members:
            continue
        for key in OPERATION_METADATA_KEYS:
            if key in group:
                out[key] = group[key]
            value = group.get(f"{key}_by_mnemonic")
            if isinstance(value, dict) and mnemonic in value:
                out[key] = value[mnemonic]
        return out
    return out


def semantic_extended_form_candidates(
    spec: dict[str, Any], allocated_mnemonics: set[str]
) -> list[Candidate]:
    out: list[Candidate] = []
    compact = instruction_catalog(spec).get("compact_primary_instructions", {}) or {}
    for group, body in compact.items():
        if not isinstance(body, dict):
            continue
        forms = body.get("extended_forms") or []
        if not isinstance(forms, list):
            continue
        for mnemonic in semantic_entry_mnemonics(str(group), body):
            for form in forms:
                if not isinstance(form, dict):
                    continue
                for operands in normalize_operand_alternatives(form.get("operands", [])):
                    merged = dict(body)
                    merged.update(form)
                    merged = body_with_operation_metadata(spec, mnemonic, merged)
                    force_size_suffix = bool(form.get("force_size_suffix", False))
                    ident = semantic_candidate_id(
                        mnemonic, operands, merged, force_size_suffix=force_size_suffix
                    )
                    category = semantic_category_from_body(
                        merged, semantic_compact_category(mnemonic, str(group))
                    )
                    out.append(
                        build_candidate(
                            ident=ident,
                            mnemonic=mnemonic,
                            category=category,
                            group=f"{group}.extended_forms",
                            operands=operands,
                            body=merged,
                            allocation=allocation_params(spec),
                            origin="instructions.yaml",
                            shape_hint="declared_extended_form",
                            must_compact=False,
                            can_extend=True,
                            fixed_payload=None,
                            default_weight=70 if category == "integer" else 55,
                        )
                    )
    return out


def semantic_compact_primary_candidates(
    spec: dict[str, Any], allocated_mnemonics: set[str], alias_sources: set[str]
) -> list[Candidate]:
    out: list[Candidate] = []
    compact = instruction_catalog(spec).get("compact_primary_instructions", {}) or {}
    if not isinstance(compact, dict):
        return out
    for group, body in compact.items():
        if not isinstance(body, dict):
            continue
        for mnemonic in semantic_entry_mnemonics(str(group), body):
            if mnemonic in allocated_mnemonics or mnemonic.upper() in alias_sources:
                continue
            forms = body.get("compact_forms")
            if isinstance(forms, list):
                for form in forms:
                    if not isinstance(form, dict):
                        continue
                    merged = dict(body)
                    merged.update(form)
                    merged = body_with_operation_metadata(spec, mnemonic, merged)
                    for operands in expanded_operand_alternatives(merged):
                        out.append(
                            build_candidate(
                                ident=semantic_candidate_id(mnemonic, operands, merged),
                                mnemonic=mnemonic,
                                category=semantic_category_from_body(
                                    merged, semantic_compact_category(mnemonic, str(group))
                                ),
                                group=str(group),
                                operands=tuple(operands),
                                body=merged,
                                allocation=allocation_params(spec),
                                origin="instructions.yaml",
                                shape_hint="semantic_compact",
                                must_compact=False,
                                can_extend=fixed_primary_payload(merged) is None,
                                fixed_payload=fixed_primary_payload(merged),
                                default_weight=80,
                            )
                        )
                continue
            for operands in expanded_operand_alternatives(body):
                merged = body_with_operation_metadata(spec, mnemonic, body)
                out.append(
                    build_candidate(
                        ident=semantic_candidate_id(mnemonic, operands, merged),
                        mnemonic=mnemonic,
                        category=semantic_category_from_body(
                            merged, semantic_compact_category(mnemonic, str(group))
                        ),
                        group=str(group),
                        operands=tuple(operands),
                        body=merged,
                        allocation=allocation_params(spec),
                        origin="instructions.yaml",
                        shape_hint="semantic_compact",
                        must_compact=False,
                        can_extend=fixed_primary_payload(merged) is None,
                        fixed_payload=fixed_primary_payload(merged),
                        default_weight=80,
                    )
                )
    return out


def expanded_operand_alternatives(body: dict[str, Any]) -> list[tuple[str, ...]]:
    out: list[tuple[str, ...]] = []
    for operands in semantic_operand_alternatives("", body):
        if any(operand_norm(str(operand)) == "DREG_OR_AREG" for operand in operands):
            d_operands = []
            a_operands = []
            for operand in operands:
                text = str(operand)
                source, _typ = split_operand_spec(text)
                if operand_norm(text) == "DREG_OR_AREG":
                    d_operands.append(f"{source}:DREG")
                    a_operands.append(f"{source}:AREG")
                else:
                    d_operands.append(text)
                    a_operands.append(text)
            out.append(tuple(d_operands))
            out.append(tuple(a_operands))
        else:
            out.append(tuple(str(operand) for operand in operands))
    return out


def semantic_compact_category(mnemonic: str, group: str) -> str:
    group_upper = group.upper()
    if "CONTROL" in group_upper or "MISC" in group_upper:
        return "system"
    return "integer"


def semantic_category_from_body(body: dict[str, Any], default_category: str) -> str:
    category = body.get("semantic_category") or body.get("category")
    return str(category) if category else default_category


def build_candidate(
    *,
    ident: str,
    mnemonic: str,
    category: str,
    group: str,
    operands: tuple[str, ...],
    body: dict[str, Any],
    allocation: dict[str, Any],
    origin: str,
    shape_hint: str,
    must_compact: bool,
    can_extend: bool,
    fixed_payload: int | None,
    default_weight: int = 45,
) -> Candidate:
    compact_fields = tuple(generate_fields(mnemonic, group, operands, body, category, mode="compact"))
    descriptor_fields = tuple(generate_fields(mnemonic, group, operands, body, category, mode="descriptor"))
    compact_bits = sum(
        field.width
        for field in compact_fields
        if field.storage == "primary" and field.value is None
    )
    compact_action = allocation_compact_action(
        allocation,
        mnemonic=mnemonic,
        category=category,
        group=group,
        body=body,
        compact_fields=compact_fields,
        descriptor_fields=descriptor_fields,
        operands=operands,
    )
    fixed_primary = fixed_payload is not None
    compact_disabled = (
        not fixed_primary
        and (
            body.get("compact") is False
            or str(body.get("compact_preference", "")).lower() == "extended"
            or compact_action == "never"
        )
    )
    compact_slots = (1 << compact_bits) if not compact_disabled and compact_bits <= PRIMARY_BITS else None
    descriptor_bits = sum(
        field.width
        for field in descriptor_fields
        if field.storage in {"descriptor", "payload"} and field.kind != "condition" and field.value is None
    )
    base_weight = instruction_weight(mnemonic, ident, category, operands, body, default_weight)
    weight = allocation_weight(
        allocation,
        base_weight=base_weight,
        mnemonic=mnemonic,
        category=category,
        group=group,
        body=body,
        compact_fields=compact_fields,
        descriptor_fields=descriptor_fields,
        operands=operands,
    )
    min_words, max_words = candidate_length_bounds(body, shape_hint)
    compact_payload_words = ceil_words(
        sum(field.width for field in compact_fields if field.storage == "payload")
    )
    min_words = max(min_words, 1 + compact_payload_words)
    return Candidate(
        id=ident,
        mnemonic=mnemonic,
        category=category,
        group=group,
        extension_family=candidate_extension_family(
            allocation,
            mnemonic=mnemonic,
            category=category,
            group=group,
            body=body,
            compact_fields=compact_fields,
            descriptor_fields=descriptor_fields,
            operands=operands,
        ),
        operands=operands,
        origin=origin,
        compact_fields=compact_fields,
        descriptor_fields=descriptor_fields,
        compact_bits=compact_bits,
        compact_slots=compact_slots,
        descriptor_bits=descriptor_bits,
        descriptor_words=ceil_words(descriptor_bits),
        weight=weight,
        must_compact=must_compact or compact_action == "required" or fixed_primary,
        can_extend=can_extend and not fixed_primary,
        fixed_payload=fixed_payload,
        shape_hint=shape_hint,
        min_words=min_words,
        max_words=max_words,
        allow_memory_memory=allows_memory_memory(body),
        fixed_size_suffix=fixed_size_suffix(body),
        privilege=candidate_privilege(body),
        allocation_cluster=candidate_allocation_cluster(body),
    )


def candidate_allocation_cluster(body: dict[str, Any]) -> str:
    value = body.get("allocation_cluster") or body.get("primary_cluster")
    return str(value) if value else ""


def candidate_extension_family(
    allocation: dict[str, Any],
    *,
    mnemonic: str,
    category: str,
    group: str,
    body: dict[str, Any],
    compact_fields: tuple[Field, ...],
    descriptor_fields: tuple[Field, ...],
    operands: tuple[str, ...],
) -> str:
    context = allocation_match_context(
        mnemonic=mnemonic,
        category=category,
        group=group,
        body=body,
        compact_fields=compact_fields,
        descriptor_fields=descriptor_fields,
        operands=operands,
    )
    for rule in allocation.get("extension_family_rules", []) or []:
        if not isinstance(rule, dict) or not allocation_rule_matches(rule, context):
            continue
        value = rule.get("extension_family")
        if value:
            return str(value)
    return str(body.get("extension_family", ""))


def candidate_privilege(body: dict[str, Any]) -> str:
    value = body.get("privilege")
    if isinstance(value, dict):
        base = value.get("level") or value.get("default") or value.get("mode")
        if value.get("policy_controlled"):
            return "policy_controlled" if not base else f"{base}_or_policy_controlled"
        return str(base or "")
    return str(value) if value else ""


def allocation_weight(
    allocation: dict[str, Any],
    *,
    base_weight: int,
    mnemonic: str,
    category: str,
    group: str,
    body: dict[str, Any],
    compact_fields: tuple[Field, ...],
    descriptor_fields: tuple[Field, ...],
    operands: tuple[str, ...],
) -> int:
    model = allocation.get("frequency_model", {}) if isinstance(allocation, dict) else {}
    default_by_category = model.get("default_weight_by_category", {}) if isinstance(model, dict) else {}
    weight = max(base_weight, int(default_by_category.get(category, 0) or 0))
    context = allocation_match_context(
        mnemonic=mnemonic,
        category=category,
        group=group,
        body=body,
        compact_fields=compact_fields,
        descriptor_fields=descriptor_fields,
        operands=operands,
    )
    for rule in model.get("rules", []) or []:
        if not isinstance(rule, dict) or not allocation_rule_matches(rule, context):
            continue
        if "weight" in rule:
            weight = max(weight, int(rule["weight"]))
    return weight


def allocation_compact_action(
    allocation: dict[str, Any],
    *,
    mnemonic: str,
    category: str,
    group: str,
    body: dict[str, Any],
    compact_fields: tuple[Field, ...],
    descriptor_fields: tuple[Field, ...],
    operands: tuple[str, ...],
) -> str:
    body_compact = str(body.get("compact", "")).lower()
    if body_compact in {"required", "never"}:
        return body_compact
    model = allocation.get("frequency_model", {}) if isinstance(allocation, dict) else {}
    context = allocation_match_context(
        mnemonic=mnemonic,
        category=category,
        group=group,
        body=body,
        compact_fields=compact_fields,
        descriptor_fields=descriptor_fields,
        operands=operands,
    )
    action = ""
    for rule in model.get("rules", []) or []:
        if not isinstance(rule, dict) or not allocation_rule_matches(rule, context):
            continue
        compact = str(rule.get("compact", "")).lower()
        if compact in {"required", "never"}:
            action = compact
    return action


def allocation_match_context(
    *,
    mnemonic: str,
    category: str,
    group: str,
    body: dict[str, Any],
    compact_fields: tuple[Field, ...],
    descriptor_fields: tuple[Field, ...],
    operands: tuple[str, ...],
) -> dict[str, str]:
    _ = descriptor_fields, operands
    semantic_family = str(body.get("semantic_family") or group).split(".", 1)[0]
    group_name = str(group).split(".", 1)[0]
    return {
        "mnemonic": mnemonic,
        "category": category,
        "semantic_family": semantic_family,
        "group": group_name,
        "profile": "_TO_".join(profile_form_parts(compact_fields)) or "NO_OPERANDS",
        "size": size_tag_from_fields(compact_fields),
    }


def allocation_rule_matches(rule: dict[str, Any], context: dict[str, str]) -> bool:
    match = rule.get("match", {})
    if not isinstance(match, dict):
        return False
    for key, expected in match.items():
        actual = context.get(str(key), "")
        if isinstance(expected, list):
            allowed = {str(item).upper() for item in expected}
            if str(actual).upper() not in allowed:
                return False
            continue
        if str(actual).upper() != str(expected).upper():
            return False
    return True


def allows_memory_memory(body: dict[str, Any]) -> bool:
    value = body.get("memory_memory")
    if value is True:
        return True
    if isinstance(value, dict):
        return bool(value.get("allowed"))
    if isinstance(value, str) and value.lower() not in {"", "disallowed", "false", "no"}:
        return True
    return str(body.get("constraint", "")).lower() == "memory_memory"


def candidate_length_bounds(body: dict[str, Any], shape_hint: str) -> tuple[int, int]:
    length = body.get("length")
    if isinstance(length, int):
        return int(length), int(length)
    if isinstance(length, dict):
        words = int(length.get("words", 0) or 0)
        min_words = int(length.get("min_words", words or 0) or 0)
        max_words = int(length.get("max_words", words or 8) or 8)
        if min_words <= 0:
            min_words = pattern_word_count(shape_hint) or 1
        return min_words, max_words
    words = pattern_word_count(shape_hint)
    return (words or 1), 8


def pattern_word_count(raw: str) -> int:
    if raw in {"semantic_operands", "semantic_compact", "declared_extended_form"}:
        return 0
    bits = cleaned_pattern(raw)
    if not bits:
        return 0
    return ceil_words(len(bits))


def generate_fields(
    mnemonic: str,
    group: str,
    operands: tuple[str, ...],
    body: dict[str, Any],
    category: str,
    *,
    mode: str,
) -> list[Field]:
    fields: list[Field] = []
    size = size_field(body, mode)
    if size is not None:
        fields.append(size)
    fields.extend(semantic_encoding_fields(mnemonic, body, mode, operands))
    norms = [operand_norm(str(operand)) for operand in operands]
    allow_memory_memory = allows_memory_memory(body)
    explicit_ea_count = sum(1 for norm in norms if is_ea_operand(norm) or "MEMORY" in norm)
    ea_budget = 2 if allow_memory_memory else 1
    generic_ea_budget = 0 if explicit_ea_count >= ea_budget else ea_budget - explicit_ea_count
    ea_seen = 0

    for index, operand in enumerate(operands):
        produced = operand_fields(
            str(operand),
            body,
            category,
            mode,
            mnemonic=mnemonic,
            group=group,
            index=index,
            generic_ea_budget=generic_ea_budget,
        )
        normalized: list[Field] = []
        for field in produced:
            if field.kind == "EA":
                if not allow_memory_memory and ea_seen >= 1:
                    normalized.append(Field("d", "DREG", register_field_width("D"), field.source, field.storage))
                    continue
                ea_seen += 1
            normalized.append(field)
        if any(field.kind == "EA" for field in normalized) and is_generic_data_operand(norms[index]):
            generic_ea_budget = max(0, generic_ea_budget - 1)
        fields.extend(normalized)
    return fields


def operand_norm(operand: str) -> str:
    token = operand.strip()
    if ":" in token:
        token = token.split(":", 1)[1]
    return token.replace("-", "_").replace("/", "_").upper()


def operand_source(operand: str) -> str:
    source, _typ = split_operand_spec(operand.strip())
    return source.replace("-", "_").replace("/", "_").upper()


def size_field(body: dict[str, Any], mode: str) -> Field | None:
    width = size_bits(body)
    if width <= 0:
        return None
    tag = size_tag(body)
    name = size_kind_field(active_spec(), tag) if tag and is_declared_size_kind(tag) else "s"
    storage = "primary" if mode == "compact" else "descriptor"
    return Field(name=name, kind=tag or "size", width=width, source="size", storage=storage)


def size_bits(body: dict[str, Any]) -> int:
    size = body.get("size")
    if isinstance(size, dict):
        if "field" in size and isinstance(size.get("values"), dict):
            return bits_needed(len(size["values"]))
        if size.get("fixed") or size.get("implicit"):
            return 0
    if isinstance(size, list):
        return bits_needed(len(size))
    if isinstance(size, str):
        normalized = size.replace("/", "_").replace("-", "_").upper()
        if normalized in {"B_W_L_Q", "L_Q", "W_L"}:
            normalized = normalized.replace("_", "")
        if is_declared_size_kind(normalized):
            return size_kind_width(active_spec(), normalized)
        if "Q_ONLY" in normalized or "IMPLICIT_Q" in normalized or normalized == "Q":
            return 0
    if body.get("D_size") == "BWLQ":
        return size_kind_width(active_spec(), "BWLQ")
    if body.get("source_size"):
        values = body.get("source_size")
        if isinstance(values, list):
            return bits_needed(len(values) + len(body.get("invalid_sizes", []) or []))
    return 0


def size_tag(body: dict[str, Any]) -> str:
    size = body.get("size")
    if isinstance(size, str):
        normalized = size.replace("/", "_").replace("-", "_").upper()
        if normalized in {"B_W_L_Q", "L_Q", "W_L"}:
            normalized = normalized.replace("_", "")
        return normalized
    if isinstance(size, dict):
        if size.get("fixed"):
            return str(size["fixed"]).upper()
        if isinstance(size.get("values"), dict):
            values = list(size["values"].values())
            return "".join(str(item) for item in values).replace("invalid", "X").upper()
    if body.get("D_size") == "BWLQ":
        return "BWLQ"
    if body.get("A_size") == "Q_only":
        return "Q"
    if body.get("source_size"):
        values = body.get("source_size") or []
        return "".join(str(item) for item in values).upper()
    return ""


def fixed_size_suffix(body: dict[str, Any]) -> str:
    values = body.get("source_size")
    if isinstance(values, list) and len(values) == 1 and not body.get("invalid_sizes"):
        return str(values[0]).upper()
    return ""


def semantic_encoding_fields(
    mnemonic: str, body: dict[str, Any], mode: str, operands: tuple[str, ...]
) -> list[Field]:
    specs = body.get("encoding_fields", []) or []
    if not isinstance(specs, list):
        return []
    storage = "primary" if mode == "compact" else "descriptor"
    fields: list[Field] = []
    for spec in specs:
        if not isinstance(spec, dict):
            continue
        if not semantic_encoding_spec_matches(spec, mnemonic, body, operands):
            continue
        values = spec.get("values", [])
        width = int(spec.get("width", bits_needed(len(values) if isinstance(values, list) else 0)) or 0)
        if width <= 0:
            continue
        value, label = semantic_encoding_value(mnemonic, spec)
        fields.append(
            Field(
                name=str(spec.get("field") or spec.get("name") or "x"),
                kind=str(spec.get("kind") or spec.get("name") or "semantic"),
                width=width,
                source=str(spec.get("source") or spec.get("name") or "semantic"),
                storage=storage,
                value=value,
                value_label=label,
                placement=str(spec.get("placement", "")),
            )
        )
    return fields


def semantic_encoding_spec_matches(
    spec: dict[str, Any], mnemonic: str, body: dict[str, Any], operands: tuple[str, ...]
) -> bool:
    match = spec.get("match")
    if not isinstance(match, dict):
        return True
    context = {
        "mnemonic": mnemonic,
        "semantic_family": str(body.get("semantic_family") or "").split(".", 1)[0],
        "profile": form_name(operands) or "NO_OPERANDS",
        "size": size_tag(body),
    }
    for key, expected in match.items():
        actual = context.get(str(key), "")
        if isinstance(expected, list):
            if str(actual).upper() not in {str(item).upper() for item in expected}:
                return False
            continue
        if str(actual).upper() != str(expected).upper():
            return False
    return True


def semantic_encoding_value(mnemonic: str, spec: dict[str, Any]) -> tuple[int | None, str]:
    values = spec.get("values", [])
    if "value" in spec:
        raw_value = spec["value"]
        if isinstance(raw_value, int):
            return int(raw_value), str(raw_value)
        label = str(raw_value)
        if isinstance(values, list):
            for index, value in enumerate(values):
                if label.upper() == str(value).upper():
                    return index, str(value)
        return int(label, 0), label
    if not isinstance(values, list):
        return None, ""
    derive = str(spec.get("derive", ""))
    if derive == "mnemonic":
        upper = mnemonic.upper()
        for index, value in enumerate(values):
            label = str(value)
            if upper == label.upper():
                return index, label
    if derive == "mnemonic_suffix":
        upper = mnemonic.upper()
        for index, value in enumerate(values):
            label = str(value)
            if upper.endswith(label.upper()):
                return index, label
    return None, ""


def operand_fields(
    operand: str,
    body: dict[str, Any],
    category: str,
    mode: str,
    *,
    mnemonic: str,
    group: str,
    index: int,
    generic_ea_budget: int,
) -> list[Field]:
    token = operand.strip()
    source, token = split_operand_spec(token)
    norm = token.replace("-", "_").replace("/", "_").upper()
    source_norm = source.replace("-", "_").replace("/", "_").upper()
    storage = "primary" if mode == "compact" else "descriptor"

    if norm in {"", "NONE"}:
        return []
    if norm in {"MEMORY_ORDER", "MEMORYORDER", "ORDER"} or source_norm in {"ORDER", "MEMORY_ORDER"}:
        return [Field("o", "memory_order", named_value_width(active_spec(), "memory_order"), source, "payload")]
    if "CONDITION" in norm or norm in {"CC"}:
        return [Field("c", "condition", condition_field_width(), source, storage)]
    if is_dbank_operand(norm, source_norm):
        return [Field("k", "DBANK", dbank_field_width(), source, storage)]
    if norm in {"DREG_OR_AREG"}:
        return [Field("r", "D_or_A", data_or_address_field_width(), source, storage)]
    if source_norm in {"COUNT", "BIT_INDEX"} and norm in {"SELECTOR_IMM6", "IMM6_SELECTOR"}:
        return [Field("n", "selector6", 6, source, storage)]
    if source_norm in {"COUNT", "BIT_INDEX"} and is_d_operand(norm):
        return [Field("n", "DREG", register_field_width("D"), source, storage)]
    if is_d_operand(norm):
        return [Field("d", "DREG", register_field_width("D"), source, storage)]
    if is_a_operand(norm):
        return [Field("a", "AREG", register_field_width("A"), source, storage)]
    if is_sp_operand(norm):
        return [Field("p", "SPREG", 0, source, storage)]
    if is_s_operand(norm):
        return [Field("g", "SREG", special_register_field_width("S"), source, storage)]
    if is_f_operand(norm):
        return [Field("f", "FREG", register_field_width("F"), source, storage)]
    if is_immediate_ea_operand(norm):
        return [Field("i", "IMM_EA", ea_field_width(), source, storage)]
    if is_ea_operand(norm) or "MEMORY" in norm:
        return [Field("e", "EA", ea_field_width(), source, storage)]
    if is_selector_operand(norm, source_norm):
        if source_norm in {"COUNT", "BIT_INDEX"}:
            return [Field("n", "selector6", 6, source, storage)]
        return [Field("n", "small_selector", 4, source, storage)]
    if "BITMAP" in norm:
        return [Field("b", "bitmap16", bitmap_field_width("bitmap16"), source, "payload")]
    if "IMM" in norm or norm in {"CR", "CREG", "CONTROL_REGISTER"}:
        width = immediate_payload_width(norm)
        return [Field("i", norm.lower(), width, source, "payload")]
    if "OUTPUT" in norm or "LEAF" in norm or "SUBLEAF" in norm:
        return []
    if is_generic_data_operand(norm):
        return generic_operand_field(
            norm,
            category,
            mode,
            source,
            mnemonic=mnemonic,
            group=group,
            index=index,
            generic_ea_budget=generic_ea_budget,
        )
    return []


def generic_operand_field(
    norm: str,
    category: str,
    mode: str,
    source: str,
    *,
    mnemonic: str,
    group: str,
    index: int,
    generic_ea_budget: int,
) -> list[Field]:
    if category == "fpu":
        storage = "primary" if mode == "compact" else "descriptor"
        return [Field("f", "FREG", register_field_width("F"), source, storage)]
    if mode == "compact":
        return [Field("d", "DREG", register_field_width("D"), source, "primary")]
    if generic_ea_budget > 0 and index == 0 and not is_destination_like(norm):
        return [Field("e", "EA", ea_field_width(), source, "descriptor")]
    return [Field("d", "DREG", register_field_width("D"), source, "descriptor")]


def is_generic_data_operand(norm: str) -> bool:
    if norm in {
        "SRC",
        "DST",
        "LO",
        "X",
        "HI",
        "VALUE",
        "SRC_OR_DST",
        "DST_OR_VALUE",
        "EXPECTED",
        "DESIRED",
    }:
        return True
    markers = ("SRC", "DST", "LO", "HI", "VALUE", "EXPECTED", "DESIRED")
    return any(marker in norm for marker in markers)


def is_selector_operand(norm: str, source_norm: str) -> bool:
    return (
        norm in {"SELECTOR", "DREG_OR_IMM", "REG_OR_IMM", "SMALL_SELECTOR"}
        or source_norm in {"COUNT", "BIT_INDEX", "OFFSET", "WIDTH"}
        or "COUNT" in norm
        or "OFFSET" in norm
        or "WIDTH" in norm
        or "BIT_INDEX" in norm
        or "SELECTOR" in norm
    )


def is_destination_like(norm: str) -> bool:
    return "DST" in norm or "DEST" in norm or "VALUE" in norm or "EXPECTED" in norm or "DESIRED" in norm


def immediate_payload_width(norm: str) -> int:
    if "IMM16" in norm or norm in {"CR", "CREG", "CONTROL_REGISTER"}:
        return 16
    if "IMM32" in norm:
        return 32
    if "IMM64" in norm:
        return 64
    return 16


def is_d_operand(norm: str) -> bool:
    return norm in {"DREG", "DLO", "DX", "DHI"} or (
        norm.startswith("D") and any(key in norm for key in ("REG", "SRC", "DST", "COUNTER"))
    )


def is_dbank_operand(norm: str, source_norm: str = "") -> bool:
    return norm in {"DBANK", "DATA_BANK", "DATA_REGISTER_BANK"} or source_norm in {
        "BANK",
        "SRC_BANK",
        "DST_BANK",
        "BANK_A",
        "BANK_B",
        "DBANK",
    }


def is_a_operand(norm: str) -> bool:
    return norm in {"AREG"} or (
        norm.startswith("A") and any(key in norm for key in ("REG", "SRC", "DST"))
    )


def is_s_operand(norm: str) -> bool:
    if is_sp_operand(norm):
        return False
    return norm in {"SREG", "SEGREG", "SEGMENT_REGISTER"} or (
        norm.startswith("S") and any(key in norm for key in ("REG", "SRC", "DST"))
    )


def is_sp_operand(norm: str) -> bool:
    return norm in {"SP", "SPREG", "STACK_POINTER", "STACK_REGISTER"} or norm.startswith("SPREG")


def is_f_operand(norm: str) -> bool:
    return norm.startswith("F") and (
        "SRC" in norm
        or "DST" in norm
        or norm in {"FA", "FB", "FLO", "FX", "FHI", "FREG", "FREGISTER"}
    )


def is_ea_operand(norm: str) -> bool:
    return (
        norm == "EA"
        or norm.startswith("EA_")
        or norm.endswith("_EA")
        or "_EA_" in norm
        or norm in {"LINEAR_OR_EA", "EA_OR_RANGE", "EA_OR_D"}
    )


def is_immediate_ea_operand(norm: str) -> bool:
    return norm in {"IMM_EA", "IMMEDIATE_EA", "IMMEA", "IMMEDIATE_OPERAND_EA"}


def uniquify_candidate_ids(candidates: list[Candidate]) -> list[Candidate]:
    seen: dict[str, int] = {}
    result: list[Candidate] = []
    for candidate in candidates:
        count = seen.get(candidate.id, 0)
        seen[candidate.id] = count + 1
        if count == 0:
            result.append(candidate)
            continue
        result.append(replace_candidate_id(candidate, f"{candidate.id}.{count + 1}"))
    return result


def replace_candidate_id(candidate: Candidate, ident: str) -> Candidate:
    return Candidate(
        id=ident,
        mnemonic=candidate.mnemonic,
        category=candidate.category,
        group=candidate.group,
        extension_family=candidate.extension_family,
        operands=candidate.operands,
        origin=candidate.origin,
        compact_fields=candidate.compact_fields,
        descriptor_fields=candidate.descriptor_fields,
        compact_bits=candidate.compact_bits,
        compact_slots=candidate.compact_slots,
        descriptor_bits=candidate.descriptor_bits,
        descriptor_words=candidate.descriptor_words,
        weight=candidate.weight,
        must_compact=candidate.must_compact,
        can_extend=candidate.can_extend,
        fixed_payload=candidate.fixed_payload,
        shape_hint=candidate.shape_hint,
        min_words=candidate.min_words,
        max_words=candidate.max_words,
        allow_memory_memory=candidate.allow_memory_memory,
        fixed_size_suffix=candidate.fixed_size_suffix,
        privilege=candidate.privilege,
    )


def instruction_candidate_id(entry: PatternEntry, operands: tuple[str, ...]) -> str:
    form = str(entry.source.get("form") or "")
    if form:
        return f"{entry.mnemonic}.{form}"
    operand_form = form_name(operands)
    if operand_form:
        return f"{entry.mnemonic}.{operand_form}"
    return entry.mnemonic


def semantic_candidate_id(
    mnemonic: str, operands: tuple[str, ...] | list[str], body: dict[str, Any], *, force_size_suffix: bool = False
) -> str:
    explicit_profile = body.get("profile")
    if explicit_profile:
        return f"{mnemonic}.{str(explicit_profile).replace('-', '_').replace('/', '_').upper()}"
    form = form_name(operands)
    ident = mnemonic if not form else f"{mnemonic}.{form}"
    tag = size_tag(body)
    if force_size_suffix and tag and tag not in {"LQ", "Q"}:
        ident = f"{ident}.{tag}"
    return ident


def form_name(operands: tuple[str, ...] | list[str]) -> str:
    parts = []
    for operand in operands:
        norm = str(operand)
        if ":" in norm:
            norm = norm.split(":", 1)[1]
        norm = norm.replace("-", "_").replace("/", "_").upper()
        source = operand_source(str(operand))
        if "CONDITION" in norm:
            continue
        if is_immediate_ea_operand(norm):
            parts.append("IMM")
        elif is_dbank_operand(norm, source):
            parts.append("DB")
        elif is_ea_operand(norm):
            parts.append("EA")
        elif is_d_operand(norm):
            parts.append("D")
        elif is_a_operand(norm):
            parts.append("A")
        elif is_sp_operand(norm):
            parts.append("SP")
        elif is_s_operand(norm):
            parts.append("S")
        elif is_f_operand(norm):
            parts.append("F")
        elif "MEMORY" in norm:
            parts.append("MEM")
        elif norm in {"SELECTOR_IMM6", "IMM6_SELECTOR"}:
            parts.append("I6")
        elif "IMM" in norm:
            parts.append("IMM")
        elif "BITMAP" in norm:
            parts.append("BITMAP")
        elif is_selector_operand(norm, source):
            parts.append("N")
        elif norm in {"SRC", "DST", "LO", "X", "HI", "VALUE", "SRC_OR_DST", "DST_OR_VALUE"}:
            parts.append("VALUE")
    return "_TO_".join(parts)


def instruction_category(entry: PatternEntry) -> str:
    cls = str(entry.source.get("class") or "")
    if cls in {"arithmetic", "conversion"}:
        return "integer"
    if cls in {"transfer", "address", "stack"}:
        return "data_movement"
    if cls in {"control_flow", "conditional"}:
        return "control_flow"
    if cls in {"fence", "debug", "trace", "system", "validation"}:
        return "system"
    if entry.source.get("privilege") == "supervisor":
        return "system"
    return "misc"


def instruction_weight(
    mnemonic: str,
    ident: str,
    category: str,
    operands: tuple[str, ...],
    body: dict[str, Any],
    default_weight: int,
) -> int:
    _ = mnemonic, ident
    if category == "data_movement" and has_ea_register_mix(operands):
        return 9000
    if category == "integer" and all_direct_d(operands):
        return 7200
    if category == "control_flow":
        return 3600
    if len(operands) == 1 and is_direct_register_operand(operands[0]):
        return 2600
    if category == "data_movement" and operands:
        return 2200
    if body.get("atomic"):
        return 500
    if category == "system":
        return 120
    if category == "fpu":
        return 160
    return default_weight


def has_ea_register_mix(operands: tuple[str, ...]) -> bool:
    norms = [operand_norm(str(operand)) for operand in operands]
    return any(is_ea_operand(norm) for norm in norms) and any(
        is_d_operand(norm) or is_a_operand(norm) or is_s_operand(norm) for norm in norms
    )


def is_direct_register_operand(operand: str) -> bool:
    norm = operand_norm(str(operand))
    return is_d_operand(norm) or is_a_operand(norm) or is_s_operand(norm) or is_f_operand(norm)


def all_direct_d(operands: tuple[str, ...]) -> bool:
    if not operands:
        return False
    for operand in operands:
        norm = str(operand)
        if ":" in norm:
            norm = norm.split(":", 1)[1]
        if not is_d_operand(norm.replace("-", "_").replace("/", "_").upper()):
            return False
    return True


def semantic_operand_alternatives(mnemonic: str, body: dict[str, Any]) -> list[tuple[str, ...]]:
    operands = body.get("operands", [])
    if isinstance(operands, dict):
        value = operands.get(mnemonic, [])
        return normalize_operand_alternatives(value)
    return normalize_operand_alternatives(operands)


def normalize_operand_alternatives(value: Any) -> list[tuple[str, ...]]:
    if value is None:
        return [()]
    if isinstance(value, dict):
        return [(operand_spec_text(value),)]
    if not isinstance(value, list):
        return [(str(value),)]
    if not value:
        return [()]
    if all(isinstance(item, list) for item in value):
        alternatives = [tuple(operand_spec_text(part) for part in item) for item in value]
    else:
        alternatives = [tuple(operand_spec_text(item) for item in value)]
    return [
        expanded
        for alternative in alternatives
        for expanded in expand_selector_operand_variants(alternative)
    ]


def expand_selector_operand_variants(operands: tuple[str, ...]) -> list[tuple[str, ...]]:
    has_ea_destination = any(
        operand_source(str(operand)) == "DST" and is_ea_operand(operand_norm(str(operand)))
        for operand in operands
    )
    variants: list[tuple[str, ...]] = [()]
    for operand in operands:
        source, typ = split_operand_spec(str(operand))
        source_norm = source.replace("-", "_").replace("/", "_").upper()
        typ_norm = typ.replace("-", "_").replace("/", "_").upper()
        choices = [str(operand)]
        if typ_norm == "SELECTOR" and source_norm == "COUNT":
            choices = [f"{source}:DREG"]
            if has_ea_destination:
                choices.insert(0, f"{source}:selector_imm6")
        elif typ_norm == "SELECTOR" and source_norm == "BIT_INDEX":
            choices = [f"{source}:DREG"]
            if has_ea_destination:
                choices.insert(0, f"{source}:selector_imm6")
        variants = [prefix + (choice,) for prefix in variants for choice in choices]
    return variants
