"""Field-layout scoring and placement for opcode allocation."""

from __future__ import annotations

from typing import Any

from alloc_model import (
    Candidate,
    Field,
    profile_candidate_id,
)


def policy_primary_bits(compact_policy: dict[str, Any]) -> int:
    model = compact_policy.get("allocation_model")
    return int(model.primary.bits)


def policy_extended_bits(compact_policy: dict[str, Any]) -> int:
    model = compact_policy.get("allocation_model")
    return int(model.extended.bits)


def layout_model_primary_bits(field_layout_model: dict[str, Any]) -> int:
    return int(field_layout_model["primary_bits"])


def layout_model_extended_bits(field_layout_model: dict[str, Any]) -> int:
    return int(field_layout_model["extended_bits"])

def build_field_layout_model(
    candidates: list[Candidate],
    selected_compact: set[str],
    extended_candidates: list[Candidate],
    compact_policy: dict[str, Any],
) -> dict[str, Any]:
    scores: dict[str, int] = {}
    widths: dict[str, int] = {}
    format_counts: dict[tuple[str, ...], int] = {}
    format_weights: dict[tuple[str, ...], int] = {}
    format_examples: dict[tuple[str, ...], list[str]] = {}
    score_model = field_score_model(compact_policy)
    affinity_rules = field_subfield_affinity_rules(compact_policy)
    affinity_scores: dict[tuple[str, str, int], int] = {}
    affinity_examples: dict[tuple[str, str, int], list[str]] = {}
    by_id = {candidate.id: candidate for candidate in candidates}

    layout_sources: list[tuple[Candidate, tuple[Field, ...], str]] = []
    for ident in sorted(selected_compact):
        candidate = by_id[ident]
        layout_sources.append((candidate, candidate.compact_fields, "primary"))
    for candidate in extended_candidates:
        layout_sources.append((candidate, candidate.descriptor_fields, "descriptor"))

    layout_instances: list[tuple[Candidate, tuple[Field, ...], str, list[tuple[str, Field]]]] = []
    for candidate, fields, storage in layout_sources:
        instances = field_instances_for_layout(fields, storage, spilled=False)
        layout_instances.append((candidate, fields, storage, instances))
        for signature, field in instances:
            scores[signature] = scores.get(signature, 0) + field_score(candidate, field.width, signature, score_model)
            widths[signature] = max(widths.get(signature, 0), field.width)

    for candidate, fields, _storage, instances in layout_instances:
        for signature, _field in instances:
            for rule in affinity_rules:
                if signature != rule["container"] or rule["subfield"] not in scores:
                    continue
                width = int(rule["width"])
                subfield = str(rule["subfield"])
                bonus = int(
                    field_score(candidate, width, subfield, score_model)
                    * float(rule["score_multiplier"])
                )
                if bonus <= 0:
                    continue
                scores[subfield] = scores.get(subfield, 0) + bonus
                widths[subfield] = max(widths.get(subfield, 0), width)
                key = (str(rule["container"]), subfield, int(rule["offset"]))
                affinity_scores[key] = affinity_scores.get(key, 0) + bonus
                affinity_examples.setdefault(key, [])
                if len(affinity_examples[key]) < 4:
                    affinity_examples[key].append(profile_candidate_id(candidate, fields))

    ordered = sorted(scores, key=lambda sig: (-scores[sig], -widths[sig], sig))
    explicit_order = explicit_signature_order(compact_policy)
    if explicit_order:
        explicit_rank = {signature: index for index, signature in enumerate(explicit_order)}
        ordered = sorted(
            scores,
            key=lambda sig: (
                explicit_rank.get(sig, explicit_rank.get(sig.split("#", 1)[0], len(explicit_rank) + 1_000)),
                -scores[sig],
                -widths[sig],
                sig,
            ),
        )
    order = {signature: index for index, signature in enumerate(ordered)}
    ranking_model = {
        "order": order,
        "subfield_affinity_relations": affinity_rules,
        "explicit_signature_order": explicit_order,
    }
    lanes, lane_sources = build_field_lanes(layout_instances, ranking_model, compact_policy)
    format_counts = {}
    format_weights = {}
    format_examples = {}
    for candidate, fields, _storage, instances in layout_instances:
        signature_tuple = tuple(signature for signature, _field in ordered_field_instances(instances, ranking_model))
        if not signature_tuple:
            continue
        format_counts[signature_tuple] = format_counts.get(signature_tuple, 0) + 1
        format_weights[signature_tuple] = format_weights.get(signature_tuple, 0) + max(1, candidate.weight)
        format_examples.setdefault(signature_tuple, [])
        if len(format_examples[signature_tuple]) < 4:
            format_examples[signature_tuple].append(profile_candidate_id(candidate, fields))
    return {
        "primary_bits": policy_primary_bits(compact_policy),
        "extended_bits": policy_extended_bits(compact_policy),
        "order": order,
        "scores": scores,
        "widths": widths,
        "lanes": lanes,
        "lane_sources": lane_sources,
        "format_counts": format_counts,
        "format_weights": format_weights,
        "format_examples": format_examples,
        "score_model": score_model,
        "anchor_strategy": field_layout_anchor_strategy(compact_policy),
        "explicit_signature_order": explicit_order,
        "format_similarity": operand_format_similarity_report(
            format_counts,
            format_weights,
            format_examples,
        ),
        "subfield_affinity_relations": affinity_rules,
        "subfield_affinity_scores": affinity_scores,
        "subfield_affinity_examples": affinity_examples,
    }


def field_layout_model_report(model: dict[str, Any]) -> dict[str, Any]:
    order = model.get("order", {})
    scores = model.get("scores", {})
    widths = model.get("widths", {})
    formats = model.get("format_counts", {})
    return {
        "signature_order": [
            {
                "signature": signature,
                "rank": int(rank),
                "width": int(widths.get(signature, 0)),
                "score": int(scores.get(signature, 0)),
            }
            for signature, rank in sorted(order.items(), key=lambda item: int(item[1]))
        ],
        "operand_format_groups": [
            {
                "format": list(fmt),
                "count": count,
                "weight": int(model.get("format_weights", {}).get(fmt, 0)),
                "examples": list(model.get("format_examples", {}).get(fmt, [])),
            }
            for fmt, count in sorted(formats.items(), key=lambda item: (-item[1], item[0]))[:32]
        ],
        "operand_format_similarity": model.get("format_similarity", []),
        "field_score_model": model.get("score_model", {}),
        "anchor_strategy": dict(model.get("anchor_strategy", {})),
        "field_lanes": [
            {
                "storage": storage,
                "signature": signature,
                "low_bit": int(low_bit),
                "source": str(model.get("lane_sources", {}).get(storage, {}).get(signature, "")),
            }
            for storage, lanes in sorted((model.get("lanes", {}) or {}).items())
            for signature, low_bit in sorted(lanes.items(), key=lambda item: (int(item[1]), item[0]))
        ],
        "explicit_signature_order": list(model.get("explicit_signature_order", [])),
        "subfield_affinities": [
            {
                "container": container,
                "subfield": subfield,
                "offset": offset,
                "score": score,
                "examples": list(model.get("subfield_affinity_examples", {}).get((container, subfield, offset), [])),
            }
            for (container, subfield, offset), score in sorted(
                model.get("subfield_affinity_scores", {}).items(),
                key=lambda item: (-int(item[1]), item[0]),
            )
        ],
    }


def explicit_signature_order(compact_policy: dict[str, Any]) -> list[str]:
    policy = compact_policy.get("field_layout", {})
    if not isinstance(policy, dict):
        return []
    raw_order = policy.get("explicit_signature_order", [])
    if not isinstance(raw_order, list):
        return []
    return [str(signature) for signature in raw_order if str(signature)]


def field_score_model(compact_policy: dict[str, Any]) -> dict[str, Any]:
    policy = compact_policy.get("field_layout", {})
    if not isinstance(policy, dict):
        return {}
    raw_model = policy.get("field_score", {})
    if not isinstance(raw_model, dict):
        raw_model = {}
    signature_multipliers = raw_model.get("signature_multipliers", {})
    if not isinstance(signature_multipliers, dict):
        signature_multipliers = {}
    return {
        "formula": str(raw_model.get("formula", "")),
        "default_multiplier": float(raw_model.get("default_multiplier", 1)),
        "signature_multipliers": {
            str(signature): float(multiplier)
            for signature, multiplier in signature_multipliers.items()
        },
    }


def field_score(candidate: Candidate, width: int, signature: str, score_model: dict[str, Any]) -> int:
    formula = str(score_model.get("formula", "candidate_weight_times_field_width"))
    if formula == "candidate_weight":
        base = max(1, candidate.weight)
    elif formula == "field_width":
        base = max(1, width)
    else:
        base = max(1, candidate.weight) * max(1, width)
    multiplier = field_score_multiplier(signature, score_model)
    return int(base * multiplier)


def field_score_multiplier(signature: str, score_model: dict[str, Any]) -> float:
    multipliers = score_model.get("signature_multipliers", {})
    if not isinstance(multipliers, dict):
        multipliers = {}
    if signature in multipliers:
        return float(multipliers[signature])
    base_signature = signature.split("#", 1)[0]
    if base_signature in multipliers:
        return float(multipliers[base_signature])
    return float(score_model.get("default_multiplier", multipliers.get("default", 1)))


def field_layout_anchor_strategy(compact_policy: dict[str, Any]) -> dict[str, Any]:
    policy = compact_policy.get("field_layout", {})
    if not isinstance(policy, dict):
        return {}
    raw_strategy = policy.get("anchor_strategy", {})
    if not isinstance(raw_strategy, dict):
        raw_strategy = {}
    return {
        "format_order": str(raw_strategy.get("format_order", "")),
        "placement": str(raw_strategy.get("placement", "")),
        "fixed_signatures": [
            str(signature)
            for signature in raw_strategy.get("fixed_signatures", [])
            if str(signature)
        ]
    }


def build_field_lanes(
    layout_instances: list[tuple[Candidate, tuple[Field, ...], str, list[tuple[str, Field]]]],
    ranking_model: dict[str, Any],
    compact_policy: dict[str, Any],
) -> tuple[dict[str, dict[str, int]], dict[str, dict[str, str]]]:
    strategy = field_layout_anchor_strategy(compact_policy)
    fixed_signatures = set(strategy.get("fixed_signatures", []))
    lanes: dict[str, dict[str, int]] = {"primary": {}, "descriptor": {}}
    sources: dict[str, dict[str, str]] = {"primary": {}, "descriptor": {}}
    if not fixed_signatures:
        return lanes, sources

    for candidate, fields, storage, instances in sorted(
        layout_instances,
        key=lambda item: field_anchor_sort_key(item, ranking_model, strategy),
    ):
        if storage != "primary":
            continue
        total_bits = policy_primary_bits(compact_policy) if storage == "primary" else policy_extended_bits(compact_policy)
        limit = variable_field_limit(fields, storage, total_bits)
        ordered = [
            (signature, field)
            for signature, field in ordered_field_instances(instances, ranking_model)
            if signature in fixed_signatures
        ]
        if sum(int(field.width) for _signature, field in ordered) > limit:
            continue
        occupied: list[tuple[int, int]] = []
        for signature, field in ordered:
            low = lanes.get(storage, {}).get(signature)
            if low is None:
                continue
            high = int(low) + int(field.width) - 1
            if high >= limit or ranges_overlap(occupied, int(low), high):
                low = first_free_field_low(occupied, int(field.width), limit)
                lanes[storage][signature] = low
                sources[storage][signature] = profile_candidate_id(candidate, fields)
                high = low + int(field.width) - 1
            occupied.append((int(low), high))

        for signature, field in ordered:
            if signature in lanes.get(storage, {}):
                continue
            low = first_free_field_low(occupied, int(field.width), limit)
            lanes[storage][signature] = low
            sources[storage][signature] = profile_candidate_id(candidate, fields)
            occupied.append((low, low + int(field.width) - 1))
    return lanes, sources


def field_anchor_sort_key(
    item: tuple[Candidate, tuple[Field, ...], str, list[tuple[str, Field]]],
    ranking_model: dict[str, Any],
    strategy: dict[str, Any],
) -> tuple[int, int, int, int, str]:
    candidate, fields, storage, instances = item
    fixed_signatures = set(strategy.get("fixed_signatures", []))
    ordered = [
        (signature, field)
        for signature, field in ordered_field_instances(instances, ranking_model)
        if not fixed_signatures or signature in fixed_signatures
    ]
    width = sum(int(field.width) for _signature, field in ordered)
    max_width = max((int(field.width) for _signature, field in ordered), default=0)
    storage_rank = 0 if storage == "primary" else 1
    if strategy.get("format_order") == "score_order":
        first_rank = min(
            (
                field_layout_position_rank(
                    signature,
                    {present for present, _field in ordered},
                    ranking_model.get("order", {}),
                    ranking_model,
                )
                for signature, _field in ordered
            ),
            default=9999,
        )
        return (storage_rank, int(first_rank * 1000), -width, -max(1, candidate.weight), profile_candidate_id(candidate, fields))
    return (storage_rank, -width, -max_width, -max(1, candidate.weight), profile_candidate_id(candidate, fields))


def variable_field_limit(fields: tuple[Field, ...], storage: str, total_bits: int) -> int:
    fixed_high_width = sum(
        int(field.width)
        for field in fields
        if field.storage == storage and field.value is not None and field.placement == "high"
    )
    return max(0, total_bits - fixed_high_width)


def first_free_field_low(occupied: list[tuple[int, int]], width: int, limit: int) -> int:
    bit = 0
    while bit + width <= limit:
        conflict = next(
            ((low, high) for low, high in sorted(occupied) if ranges_overlap([(low, high)], bit, bit + width - 1)),
            None,
        )
        if conflict is None:
            return bit
        bit = int(conflict[1]) + 1
    raise RuntimeError("unable to place semantic field in allocated field lanes")


def ranges_overlap(existing: list[tuple[int, int]], low: int, high: int) -> bool:
    return any(low <= existing_high and high >= existing_low for existing_low, existing_high in existing)


def field_subfield_affinity_rules(compact_policy: dict[str, Any]) -> list[dict[str, Any]]:
    policy = compact_policy.get("field_layout", {})
    if not isinstance(policy, dict):
        return []
    raw_rules = policy.get("subfield_affinities", [])
    if not isinstance(raw_rules, list):
        return []
    rules: list[dict[str, Any]] = []
    for raw_rule in raw_rules:
        if not isinstance(raw_rule, dict):
            continue
        container = str(raw_rule.get("container_signature", ""))
        subfield = str(raw_rule.get("subfield_signature", ""))
        if not container or not subfield:
            continue
        rules.append(
            {
                "name": str(raw_rule.get("name") or f"{container}_contains_{subfield}"),
                "container": container,
                "subfield": subfield,
                "offset": int(raw_rule.get("offset", 0) or 0),
                "width": int(raw_rule.get("width", 0) or 0),
                "score_multiplier": float(raw_rule.get("score_multiplier", 1) or 1),
            }
        )
    return rules


def operand_format_similarity_report(
    format_counts: dict[tuple[str, ...], int],
    format_weights: dict[tuple[str, ...], int],
    format_examples: dict[tuple[str, ...], list[str]],
) -> list[dict[str, Any]]:
    formats = list(format_counts)
    pairs: list[dict[str, Any]] = []
    for left_index, left in enumerate(formats):
        for right in formats[left_index + 1 :]:
            similarity = operand_format_similarity(left, right)
            if similarity <= 0:
                continue
            pairs.append(
                {
                    "left": list(left),
                    "right": list(right),
                    "similarity": round(similarity, 3),
                    "combined_weight": int(
                        min(format_weights.get(left, 0), format_weights.get(right, 0))
                        * similarity
                    ),
                    "left_examples": list(format_examples.get(left, [])),
                    "right_examples": list(format_examples.get(right, [])),
                }
            )
    pairs.sort(key=lambda item: (-float(item["similarity"]), -int(item["combined_weight"]), item["left"], item["right"]))
    return pairs[:32]


def operand_format_similarity(left: tuple[str, ...], right: tuple[str, ...]) -> float:
    left_counts = multiset_counts(left)
    right_counts = multiset_counts(right)
    keys = set(left_counts) | set(right_counts)
    if not keys:
        return 0.0
    overlap = sum(min(left_counts.get(key, 0), right_counts.get(key, 0)) for key in keys)
    total = sum(max(left_counts.get(key, 0), right_counts.get(key, 0)) for key in keys)
    return overlap / total if total else 0.0


def multiset_counts(items: tuple[str, ...]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for item in items:
        counts[item] = counts.get(item, 0) + 1
    return counts


def field_instances_for_layout(
    fields: tuple[Field, ...], storage: str, *, spilled: bool
) -> list[tuple[str, Field]]:
    counts: dict[str, int] = {}
    out: list[tuple[str, Field]] = []
    for field in fields:
        if field.storage != storage or field.value is not None:
            continue
        if field.width <= 0:
            continue
        if storage == "descriptor" and (field.kind == "condition" or spilled):
            continue
        if field.storage == "payload":
            continue
        base = field_base_signature(field)
        counts[base] = counts.get(base, 0) + 1
        signature = base if counts[base] == 1 else f"{base}#{counts[base]}"
        out.append((signature, field))
    return out


def field_base_signature(field: Field) -> str:
    if field.source == "size":
        return f"SIZE{field.width}"
    if field.kind in {"DREG", "AREG", "SREG", "D_or_A"}:
        return f"REG{field.width}"
    if field.kind in {"EA", "IMM_EA"}:
        return f"EA{field.width}"
    if field.kind == "condition":
        return f"COND{field.width}"
    if field.kind in {"small_selector", "selector6"}:
        return f"SEL{field.width}"
    if field.kind == "memory_order":
        return f"ORDER{field.width}"
    return f"{field.kind.upper()}:{field.width}"


def assign_field_positions(
    fields: tuple[Field, ...],
    total_bits: int,
    storage: str,
    field_layout_model: dict[str, Any],
    *,
    spilled: bool = False,
) -> list[dict[str, Any]]:
    fixed_high = [
        field
        for field in fields
        if field.storage == storage and field.value is not None and field.placement == "high"
    ]
    instances = field_instances_for_layout(fields, storage, spilled=spilled)
    ordered_instances = ordered_field_instances(instances, field_layout_model)
    placed = []
    high_cursor = total_bits - 1
    for field in fixed_high:
        high_cursor -= int(field.width)
    variable_limit = high_cursor + 1
    occupied: list[tuple[int, int]] = []
    lanes = (field_layout_model.get("lanes", {}) or {}).get(storage, {})
    present_signatures = {signature for signature, _field in ordered_instances}
    name_counts: dict[str, int] = {}
    for signature, field in ordered_instances:
        count = name_counts.get(field.name, 0) + 1
        name_counts[field.name] = count
        name = duplicate_field_name(field.name, count)
        lane_low = lanes.get(signature) if isinstance(lanes, dict) else None
        if lane_low is not None:
            low = int(lane_low)
            high = low + field.width - 1
            if high >= variable_limit or ranges_overlap(occupied, low, high):
                low = first_free_field_low(occupied, field.width, variable_limit)
        else:
            low = preferred_subfield_low(
                signature,
                field,
                present_signatures,
                occupied,
                variable_limit,
                lanes if isinstance(lanes, dict) else {},
                field_layout_model,
            )
            if low is None:
                low = first_free_field_low(occupied, field.width, variable_limit)
        high = low + field.width - 1
        placed.append(
            {
                **field_dict(field),
                "name": name,
                "low_bit": low,
                "high_bit": high,
                "range": bit_range(high, low),
            }
        )
        occupied.append((low, high))
    high_cursor = total_bits - 1
    for field in fixed_high:
        count = name_counts.get(field.name, 0) + 1
        name_counts[field.name] = count
        name = duplicate_field_name(field.name, count)
        high = high_cursor
        low = high - field.width + 1
        placed.append(
            {
                **field_dict(field),
                "name": name,
                "low_bit": low,
                "high_bit": high,
                "range": bit_range(high, low),
            }
        )
        high_cursor = low - 1
    variable_highs = [int(field["high_bit"]) for field in placed if field.get("value") is None]
    if variable_highs and max(variable_highs) > high_cursor:
        raise RuntimeError("field layout overlaps fixed high semantic fields")
    return placed


def preferred_subfield_low(
    signature: str,
    field: Field,
    present_signatures: set[str],
    occupied: list[tuple[int, int]],
    limit: int,
    lanes: dict[str, int],
    field_layout_model: dict[str, Any],
) -> int | None:
    for relation in field_layout_model.get("subfield_affinity_relations", []):
        container = str(relation.get("container", ""))
        subfield = str(relation.get("subfield", ""))
        if signature != subfield or not container or container in present_signatures:
            continue
        if container not in lanes:
            continue
        offset = int(relation.get("offset", 0) or 0)
        width = int(relation.get("width", field.width) or field.width)
        if int(field.width) > width:
            continue
        low = int(lanes[container]) + offset
        high = low + int(field.width) - 1
        if high < limit and not ranges_overlap(occupied, low, high):
            return low
    return None


def duplicate_field_name(name: str, count: int) -> str:
    if count <= 1:
        return name
    if count == 2 and len(name) == 1 and name.islower():
        return name.upper()
    return f"{name}{count}"


def ordered_field_instances(
    instances: list[tuple[str, Field]],
    field_layout_model: dict[str, Any],
) -> list[tuple[str, Field]]:
    order = field_layout_model.get("order", {})
    present = {signature for signature, _field in instances}
    return sorted(
        instances,
        key=lambda item: (
            field_layout_position_rank(item[0], present, order, field_layout_model),
            item[0],
            item[1].source,
        ),
    )


def field_layout_position_rank(
    signature: str,
    present: set[str],
    order: dict[str, int],
    field_layout_model: dict[str, Any],
) -> float:
    rank = float(order.get(signature, len(order) + 1000))
    for relation in field_layout_model.get("subfield_affinity_relations", []):
        container = str(relation.get("container", ""))
        subfield = str(relation.get("subfield", ""))
        if not container or not subfield:
            continue
        if signature == container and subfield in present:
            rank = min(rank, float(order.get(subfield, rank))) - 0.25
        elif signature == subfield and container in present:
            rank = max(rank, float(order.get(container, rank))) + 0.25
    return rank


def bit_range(high: int, low: int) -> str:
    if high == low:
        return f"[{low}]"
    return f"[{high}:{low}]"


def field_dict(field: Field) -> dict[str, Any]:
    return {
        "name": field.name,
        "kind": field.kind,
        "width": field.width,
        "source": field.source,
        "storage": field.storage,
        **({"value": field.value} if field.value is not None else {}),
        **({"value_label": field.value_label} if field.value_label else {}),
        **({"placement": field.placement} if field.placement else {}),
    }


def layout_text(fields: list[dict[str, Any]], total_bits: int | None = None) -> str:
    if not fields:
        return "none"
    if total_bits is None:
        total_bits = max(int(field["high_bit"]) for field in fields) + 1
    by_low = {int(field["low_bit"]): field for field in fields}
    parts = []
    bit = 0
    while bit < total_bits:
        field = by_low.get(bit)
        if field is not None:
            if field.get("value") is not None:
                label = field.get("value_label", field.get("value"))
                parts.append(f"{field['name']}={label}{field['range']}")
            else:
                parts.append(f"{field['name']}{field['range']}")
            bit = int(field["high_bit"]) + 1
            continue
        low = bit
        while bit + 1 < total_bits and (bit + 1) not in by_low:
            bit += 1
        parts.append(f"op{bit_range(bit, low)}")
        bit += 1
    return " ".join(parts)


def field_layout_variable_mask(fields: list[dict[str, Any]]) -> int:
    mask = 0
    for field in fields:
        if field.get("value") is not None:
            continue
        low = int(field["low_bit"])
        high = int(field["high_bit"])
        mask |= ((1 << (high - low + 1)) - 1) << low
    return mask


def field_layout_span_bits(fields: list[dict[str, Any]]) -> int:
    highs = [int(field["high_bit"]) for field in fields if field.get("value") is None]
    return max(highs) + 1 if highs else 0


def primary_span_bits(candidate: Candidate, field_layout_model: dict[str, Any]) -> int:
    fields = assign_field_positions(candidate.compact_fields, layout_model_primary_bits(field_layout_model), "primary", field_layout_model)
    return field_layout_span_bits(fields)


def primary_span_slots(candidate: Candidate, field_layout_model: dict[str, Any]) -> int:
    bits = primary_span_bits(candidate, field_layout_model)
    return 1 << bits if bits > 0 else 1


def extended_field_layout_text(
    fields: tuple[Field, ...],
    field_layout_model: dict[str, Any],
    opcode_fields: tuple[Field, ...] | None = None,
) -> str:
    parts = []
    if opcode_fields is None:
        opcode_field_set = {
            field
            for field in fields
            if field.storage == "descriptor"
            and field.kind != "condition"
            and field.value is None
        }
    else:
        opcode_field_set = set(opcode_fields)
    opcode_layout_fields = tuple(
        field
        for field in fields
        if field.storage == "descriptor"
        and (field.value is not None or field in opcode_field_set)
    )
    placed = assign_field_positions(opcode_layout_fields, layout_model_extended_bits(field_layout_model), "descriptor", field_layout_model)
    for field in sorted(placed, key=lambda item: item["low_bit"]):
        if field.get("value") is not None:
            label = field.get("value_label", field.get("value"))
            parts.append(f"{field['name']}:{field['kind']}={label}{field['range']}")
        else:
            parts.append(f"{field['name']}:{field['kind']}{field['range']}")
    payload_fields = [field for field in fields if field.storage == "payload"]
    payload_fields.extend(
        field
        for _signature, field in ordered_field_instances(
            field_instances_for_layout(fields, "descriptor", spilled=False),
            field_layout_model,
        )
        if field.kind != "condition" and field.value is None and field not in opcode_field_set
    )
    payload_name_counts: dict[str, int] = {}
    for field in payload_fields:
        count = payload_name_counts.get(field.name, 0) + 1
        payload_name_counts[field.name] = count
        name = duplicate_field_name(field.name, count)
        parts.append(f"{name}:{field.kind}/{field.width}@payload")
    for field in fields:
        if field.kind == "condition":
            parts.append(f"{field.name}:{field.kind}/{field.width}@root")
    return ", ".join(parts) if parts else "none"


def descriptor_layout_text(fields: tuple[Field, ...]) -> str:
    if not fields:
        return "none"
    parts = []
    for field in fields:
        if field.value is not None:
            continue
        if field.width <= 0:
            continue
        if field.kind == "condition":
            storage = "root"
        else:
            storage = "payload" if field.storage == "payload" else "ext"
        parts.append(f"{field.name}:{field.kind}/{field.width}@{storage}")
    return ", ".join(parts)
