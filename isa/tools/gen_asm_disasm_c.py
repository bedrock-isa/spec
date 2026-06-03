#!/usr/bin/env python3
"""Generate C assembler/disassembler tables from allocation output."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any
import sys

sys.dont_write_bytecode = True

from gen_instruction_tables import (  # noqa: E402
    allocation_sort_key,
    field_symbol,
    field_for_operand,
    infer_operand_kind,
    is_condition_mnemonic,
    is_implicit_unencoded_operand,
    line_fields,
    line_syntax_text,
    parse_range,
    root_fields_for_item,
    split_operand,
)
from isa_spec import load_spec  # noqa: E402


FORM_KIND = {
    "compact": "BEDROCK_FORM_COMPACT",
    "compact_alias": "BEDROCK_FORM_COMPACT_ALIAS",
    "extended": "BEDROCK_FORM_EXTENDED",
    "extended_alias": "BEDROCK_FORM_EXTENDED_ALIAS",
}


def cstr(value: Any) -> str:
    return json.dumps("" if value is None else str(value), ensure_ascii=True)


def load_plan(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as fp:
        return json.load(fp)


def allocation_items(plan: dict[str, Any]) -> list[dict[str, Any]]:
    solver = plan.get("solver", plan)
    rows: list[dict[str, Any]] = []
    rows.extend(dict(item, kind="compact") for item in solver.get("primary_allocations", []) if item.get("kind") == "compact")
    rows.extend(dict(item, kind="compact_alias") for item in solver.get("primary_alias_allocations", []))
    rows.extend(dict(item, kind="extended") for item in solver.get("extended_allocations", []))
    rows.extend(dict(item, kind="extended_alias") for item in solver.get("extended_alias_allocations", []))
    return [item for item in rows if item.get("kind") != "extension_root"]


def root_field_list(item: dict[str, Any]) -> list[dict[str, Any]]:
    if item.get("kind") in {"compact", "compact_alias"}:
        return []
    start, end = parse_range(str(item.get("extension_root_payload", "0x000")))
    fields = root_fields_for_item(item, start, end)
    return [dict(field, token=0) for field in fields]


def all_fields(item: dict[str, Any]) -> list[dict[str, Any]]:
    fields = root_field_list(item) + line_fields(item)
    out = []
    seen: set[tuple[int, str, str, int, int]] = set()
    for field in fields:
        token = int(field.get("token", 0))
        low = int(field.get("low_bit", 0))
        width = int(field.get("width", int(field.get("high_bit", low)) - low + 1))
        key = (token, str(field.get("name", "")), str(field.get("source", "")), low, width)
        if key in seen:
            continue
        seen.add(key)
        normalized = dict(field)
        normalized["token"] = token
        normalized["low_bit"] = low
        normalized["width"] = width
        normalized["high_bit"] = low + width - 1
        normalized["symbol"] = field_symbol(normalized)
        out.append(normalized)
    return sorted(out, key=lambda field: (int(field.get("token", 0)), int(field.get("low_bit", 0)), str(field.get("name", ""))))


def exact_primary_values(item: dict[str, Any]) -> list[int]:
    values = item.get("alias_payloads") if item.get("kind") in {"compact_alias", "extended_alias"} else None
    if not values:
        values = item.get("primary_payloads")
    if not values:
        return []
    return sorted({int(str(value), 16) for value in values})


def primary_range(item: dict[str, Any]) -> tuple[int, int]:
    exact = exact_primary_values(item)
    if exact:
        return min(exact), max(exact)
    if item.get("kind") in {"compact", "compact_alias"}:
        return int(str(item["start_payload"]), 16), int(str(item["end_payload"]), 16)
    return parse_range(str(item.get("extension_root_payload", "0x000")))


def extended_range(item: dict[str, Any]) -> tuple[int, int]:
    if item.get("kind") in {"compact", "compact_alias"}:
        return 0, 0
    return parse_range(str(item.get("extended_opcode", "0x0000")))


def required_word_count(item: dict[str, Any], fields: list[dict[str, Any]]) -> int:
    encoded = int(item.get("min_words", 1))
    if item.get("kind") in {"extended", "extended_alias"}:
        encoded = max(encoded, 2)
    for field in fields:
        encoded = max(encoded, int(field.get("token", 0)) + 1)
    return max(1, min(8, encoded))


def decode_sort_key(item: dict[str, Any]) -> tuple[int, int, int, str]:
    primary_start, _primary_end = primary_range(item)
    ext_start, _ext_end = extended_range(item)
    alias_priority = 0 if item.get("kind") in {"compact_alias", "extended_alias"} else 1
    return primary_start, ext_start, alias_priority, str(item.get("id", ""))


def operand_rows(item: dict[str, Any], fields: list[dict[str, Any]], field_base: int) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for operand in item.get("operands", []):
        operand_text = str(operand)
        field = field_for_operand(fields, operand_text)
        if is_implicit_unencoded_operand(operand_text, field):
            continue
        role, declared_kind = split_operand(operand_text)
        kind = infer_operand_kind(operand_text, field)
        if kind == "condition" and is_condition_mnemonic(str(item.get("mnemonic", ""))):
            continue
        if kind == "memory_order":
            continue
        field_index = 0xFFFF
        if field is not None:
            for index, candidate in enumerate(fields):
                if candidate is field:
                    field_index = field_base + index
                    break
                if (
                    str(candidate.get("source", "")) == str(field.get("source", ""))
                    and str(candidate.get("kind", "")) == str(field.get("kind", ""))
                    and int(candidate.get("token", 0)) == int(field.get("token", 0))
                    and int(candidate.get("low_bit", 0)) == int(field.get("low_bit", 0))
                ):
                    field_index = field_base + index
                    break
        rows.append(
            {
                "role": role,
                "declared_kind": declared_kind,
                "kind": kind,
                "field_index": field_index,
            }
        )
    return rows


def syntax_with_field_symbols(item: dict[str, Any], fields: list[dict[str, Any]]) -> str:
    syntax = line_syntax_text(item, fields)
    for operand in item.get("operands", []):
        operand_text = str(operand)
        field = field_for_operand(fields, operand_text)
        if field is None:
            continue
        kind = infer_operand_kind(operand_text, field)
        if kind.lower() == "cr":
            syntax = syntax.replace("<cr>", f"<cr({field_symbol(field)})>", 1)
    return syntax


def form_model(items: list[dict[str, Any]]) -> dict[str, Any]:
    forms = []
    fields = []
    operands = []
    primary_values: list[int] = []

    for item in sorted(items, key=decode_sort_key):
        item_fields = all_fields(item)
        field_base = len(fields)
        operand_base = len(operands)
        value_base = len(primary_values)
        values = exact_primary_values(item)
        primary_values.extend(values)
        item_operands = operand_rows(item, item_fields, field_base)
        fields.extend(item_fields)
        operands.extend(item_operands)

        primary_start, primary_end = primary_range(item)
        ext_start, ext_end = extended_range(item)
        required_words = required_word_count(item, item_fields)
        min_words = max(required_words, max(1, min(8, int(item.get("min_words", 1)))))
        max_words = max(min_words, min(8, int(item.get("max_words", 8))))

        forms.append(
            {
                "id": str(item.get("id", "")),
                "mnemonic": str(item.get("mnemonic", "")),
                "syntax": syntax_with_field_symbols(item, item_fields),
                "kind": FORM_KIND[str(item.get("kind", "compact"))],
                "category": str(item.get("category", "")),
                "group": str(item.get("group", "")),
                "privilege": str(item.get("privilege", "")) or "unprivileged",
                "primary_start": primary_start,
                "primary_end": primary_end,
                "ext_start": ext_start,
                "ext_end": ext_end,
                "min_words": min_words,
                "max_words": max_words,
                "required_words": max(min_words, required_words),
                "field_index": field_base,
                "field_count": len(item_fields),
                "operand_index": operand_base,
                "operand_count": len(item_operands),
                "primary_value_index": value_base,
                "primary_value_count": len(values),
                "alias_of": str(item.get("alias_of", "")),
                "alias_condition": str(item.get("alias_condition", "")),
            }
        )

    return {
        "forms": forms,
        "fields": fields,
        "operands": operands,
        "primary_values": primary_values,
    }


def named_values_from_spec(spec: dict[str, Any]) -> dict[str, list[tuple[str, int]]]:
    conditions: list[tuple[str, int]] = []
    for condition in spec.get("conditions", {}).get("conditions", []):
        value = int(condition.get("value", 0))
        name = str(condition.get("name", ""))
        if name:
            conditions.append((name, value))
        for alias in condition.get("aliases", []) or []:
            alias_text = str(alias)
            if alias_text:
                conditions.append((alias_text, value))

    registers = spec.get("registers", {})
    sreg_names = (
        registers.get("special_register_classes", {})
        .get("S", {})
        .get("registers", [])
    )
    cr_names = (
        registers.get("control_register_classes", {})
        .get("CR", {})
        .get("registers", [])
    )
    return {
        "conditions": [(str(name), index) for name, index in conditions],
        "sregs": [(str(name), index) for index, name in enumerate(sreg_names) if str(name)],
        "crs": [(str(name), index) for index, name in enumerate(cr_names) if str(name)],
        "memory_orders": [
            ("RELAXED", 0),
            ("ACQUIRE", 1),
            ("RELEASE", 2),
            ("ACQREL", 3),
            ("SEQCST", 4),
        ],
    }


TEXT_RUNTIME_C = r'''
#define BEDROCK_TEXT_MAX_OPERANDS 8u
#define BEDROCK_TEXT_MAX_FIELDS 32u
#define BEDROCK_TEXT_OPERAND_CHARS 96u

typedef struct bedrock_text_operand {
    char text[BEDROCK_TEXT_OPERAND_CHARS];
    uint64_t value;
    uint16_t payload[5];
    size_t payload_count;
    int cost;
} bedrock_text_operand;

typedef struct bedrock_text_line {
    char mnemonic[32];
    char size_suffix;
    uint16_t condition;
    uint16_t memory_order;
    int has_condition;
    int has_memory_order;
    size_t operand_count;
    char operands[BEDROCK_TEXT_MAX_OPERANDS][BEDROCK_TEXT_OPERAND_CHARS];
} bedrock_text_line;

static int bedrock_ascii_upper(int ch)
{
    return ch >= 'a' && ch <= 'z' ? ch - ('a' - 'A') : ch;
}

static int bedrock_char_ieq(char lhs, char rhs)
{
    return bedrock_ascii_upper((unsigned char)lhs) == bedrock_ascii_upper((unsigned char)rhs);
}

static int bedrock_streq_ci(const char *lhs, const char *rhs)
{
    while (*lhs != '\0' && *rhs != '\0') {
        if (!bedrock_char_ieq(*lhs, *rhs)) {
            return 0;
        }
        ++lhs;
        ++rhs;
    }
    return *lhs == '\0' && *rhs == '\0';
}

static int bedrock_starts_ci(const char *text, const char *prefix, size_t prefix_len)
{
    size_t index;
    for (index = 0; index < prefix_len; ++index) {
        if (text[index] == '\0' || !bedrock_char_ieq(text[index], prefix[index])) {
            return 0;
        }
    }
    return 1;
}

static void bedrock_trim_copy(char *dst, size_t dst_size, const char *start, const char *end)
{
    size_t len;
    while (start < end && isspace((unsigned char)*start)) {
        ++start;
    }
    while (end > start && isspace((unsigned char)end[-1])) {
        --end;
    }
    len = (size_t)(end - start);
    if (dst_size == 0u) {
        return;
    }
    if (len >= dst_size) {
        len = dst_size - 1u;
    }
    memcpy(dst, start, len);
    dst[len] = '\0';
}

static void bedrock_compact_copy(char *dst, size_t dst_size, const char *src)
{
    size_t out = 0;
    if (dst_size == 0u) {
        return;
    }
    while (*src != '\0' && out + 1u < dst_size) {
        if (!isspace((unsigned char)*src)) {
            dst[out++] = (char)bedrock_ascii_upper((unsigned char)*src);
        }
        ++src;
    }
    dst[out] = '\0';
}

static int bedrock_parse_u64(const char *text, uint64_t *value)
{
    char *end = 0;
    unsigned long long parsed;
    while (isspace((unsigned char)*text)) {
        ++text;
    }
    if (*text == '#') {
        ++text;
    }
    parsed = strtoull(text, &end, 0);
    if (end == text) {
        return 0;
    }
    while (isspace((unsigned char)*end)) {
        ++end;
    }
    if (*end != '\0') {
        return 0;
    }
    *value = (uint64_t)parsed;
    return 1;
}

static int bedrock_parse_i64(const char *text, int64_t *value)
{
    char *end = 0;
    long long parsed;
    while (isspace((unsigned char)*text)) {
        ++text;
    }
    if (*text == '#') {
        ++text;
    }
    parsed = strtoll(text, &end, 0);
    if (end == text) {
        return 0;
    }
    while (isspace((unsigned char)*end)) {
        ++end;
    }
    if (*end != '\0') {
        return 0;
    }
    *value = (int64_t)parsed;
    return 1;
}

static size_t bedrock_words_for_size_suffix(char suffix);

static int bedrock_parse_immediate_payload_text(const char *text, uint64_t *value, size_t *forced_words)
{
    char compact[96];
    size_t len;
    int64_t signed_value;
    uint64_t unsigned_value;
    *forced_words = 0;
    bedrock_compact_copy(compact, sizeof(compact), text);
    len = strlen(compact);
    if (len > 2u && compact[len - 2u] == '.') {
        char suffix = (char)bedrock_ascii_upper((unsigned char)compact[len - 1u]);
        if (suffix == 'W' || suffix == 'L' || suffix == 'Q') {
            *forced_words = bedrock_words_for_size_suffix(suffix);
            compact[len - 2u] = '\0';
        }
    }
    if (compact[0] == '-' || compact[0] == '+') {
        if (!bedrock_parse_i64(compact, &signed_value)) {
            return 0;
        }
        *value = (uint64_t)signed_value;
        return 1;
    }
    if (!bedrock_parse_u64(compact, &unsigned_value)) {
        return 0;
    }
    *value = unsigned_value;
    return 1;
}

static int bedrock_lookup_named(const bedrock_named_value *names, size_t count, const char *text, uint16_t *value)
{
    size_t index;
    for (index = 0; index < count; ++index) {
        if (names[index].name != 0 && bedrock_streq_ci(names[index].name, text)) {
            *value = names[index].value;
            return 1;
        }
    }
    return 0;
}

static const char *bedrock_name_for_value(const bedrock_named_value *names, size_t count, uint16_t value)
{
    size_t index;
    for (index = 0; index < count; ++index) {
        if (names[index].name != 0 && names[index].value == value) {
            return names[index].name;
        }
    }
    return "?";
}

static int bedrock_parse_numbered_register(const char *text, char prefix, unsigned max_index, uint64_t *value)
{
    uint64_t number;
    char digits[16];
    if (!bedrock_char_ieq(text[0], prefix)) {
        return 0;
    }
    if (text[1] == '\0') {
        return 0;
    }
    bedrock_trim_copy(digits, sizeof(digits), text + 1, text + strlen(text));
    if (!bedrock_parse_u64(digits, &number) || number > max_index) {
        return 0;
    }
    *value = number;
    return 1;
}

static int bedrock_parse_dbank_selector(const char *text, uint64_t *value)
{
    char compact[32];
    uint64_t number;
    bedrock_compact_copy(compact, sizeof(compact), text);
    if (bedrock_starts_ci(compact, "DB", 2u)) {
        if (!bedrock_parse_u64(compact + 2, &number) || number > 15u) {
            return 0;
        }
        *value = number;
        return 1;
    }
    if (!bedrock_parse_u64(compact, &number) || number > 15u) {
        return 0;
    }
    *value = number;
    return 1;
}

static void bedrock_payload_from_u64(uint64_t value, uint16_t *payload, size_t words)
{
    size_t index;
    for (index = 0; index < words; ++index) {
        payload[index] = (uint16_t)((value >> (index * 16u)) & 0xffffu);
    }
}

static size_t bedrock_words_for_size_suffix(char suffix)
{
    switch (bedrock_ascii_upper((unsigned char)suffix)) {
    case 'Q':
        return 4;
    case 'L':
        return 2;
    case 'B':
    case 'W':
    default:
        return 1;
    }
}

static size_t bedrock_bits_for_size_suffix(char suffix)
{
    switch (bedrock_ascii_upper((unsigned char)suffix)) {
    case 'B':
        return 8;
    case 'W':
        return 16;
    case 'L':
        return 32;
    case 'Q':
    default:
        return 64;
    }
}

static int bedrock_value_fits_signed_or_unsigned_bits(uint64_t value, unsigned bits)
{
    uint64_t unsigned_max;
    uint64_t signed_min_encoded;
    if (bits >= 64u) {
        return 1;
    }
    unsigned_max = (1ull << bits) - 1ull;
    signed_min_encoded = (~0ull << (bits - 1u));
    return value <= unsigned_max || value >= signed_min_encoded;
}

static int bedrock_choose_compact_immediate_ea(int64_t signed_value, uint64_t unsigned_value, char size_suffix, bedrock_text_operand *out)
{
    size_t operand_bits = bedrock_bits_for_size_suffix(size_suffix);
    if (signed_value >= -32768 && signed_value <= 32767) {
        out->value = 0x32u;
        out->payload_count = 1;
        bedrock_payload_from_u64((uint64_t)signed_value, out->payload, 1);
        return 1;
    }
    if (signed_value >= INT32_MIN && signed_value <= INT32_MAX) {
        out->value = 0x33u;
        out->payload_count = 2;
        bedrock_payload_from_u64((uint64_t)signed_value, out->payload, 2);
        return 1;
    }
    if (operand_bits <= 32u && unsigned_value <= 0xffffffffull) {
        out->value = 0x33u;
        out->payload_count = 2;
        bedrock_payload_from_u64(unsigned_value, out->payload, 2);
        return 1;
    }
    out->value = 0x34u;
    out->payload_count = 4;
    bedrock_payload_from_u64(unsigned_value, out->payload, 4);
    return 1;
}

static int bedrock_parse_forced_immediate_ea(const char *compact, bedrock_text_operand *out)
{
    char number[96];
    size_t len = strlen(compact);
    size_t number_len;
    uint64_t unsigned_value = 0;
    int64_t signed_value = 0;
    uint64_t payload_value = 0;
    size_t words = 0;
    uint64_t code = 0;
    int is_signed_text;
    char suffix;
    if (len < 3u || compact[len - 2u] != '.') {
        return 0;
    }
    suffix = (char)bedrock_ascii_upper((unsigned char)compact[len - 1u]);
    if (suffix != 'W' && suffix != 'L' && suffix != 'Q') {
        return 0;
    }
    number_len = len - 2u;
    if (number_len == 0u || number_len >= sizeof(number)) {
        return 0;
    }
    memcpy(number, compact, number_len);
    number[number_len] = '\0';
    is_signed_text = number[0] == '-' || number[0] == '+';
    if (is_signed_text) {
        if (!bedrock_parse_i64(number, &signed_value)) {
            return 0;
        }
        payload_value = (uint64_t)signed_value;
    } else {
        if (!bedrock_parse_u64(number, &unsigned_value)) {
            return 0;
        }
        payload_value = unsigned_value;
    }
    if (suffix == 'W') {
        if (is_signed_text) {
            if (signed_value < -32768 || signed_value > 32767) {
                return 0;
            }
        } else if (unsigned_value > 0xffffull) {
            return 0;
        }
        code = 0x32u;
        words = 1;
    } else if (suffix == 'L') {
        if (is_signed_text) {
            if (signed_value < INT32_MIN || signed_value > INT32_MAX) {
                return 0;
            }
        } else if (unsigned_value > 0xffffffffull) {
            return 0;
        }
        code = 0x33u;
        words = 2;
    } else {
        code = 0x34u;
        words = 4;
    }
    out->value = code;
    out->payload_count = words;
    bedrock_payload_from_u64(payload_value, out->payload, words);
    return 1;
}

static int bedrock_scale_code(uint64_t scale, uint16_t *code)
{
    switch (scale) {
    case 1: *code = 0; return 1;
    case 2: *code = 1; return 1;
    case 4: *code = 2; return 1;
    case 8: *code = 3; return 1;
    default: return 0;
    }
}

static int bedrock_segment_code(const char *segment, uint16_t *code)
{
    if (segment == 0 || *segment == '\0') {
        return 0;
    }
    if (bedrock_streq_ci(segment, "CS")) {
        *code = 0;
        return 1;
    }
    if (bedrock_streq_ci(segment, "DS")) { *code = 1; return 1; }
    if (bedrock_streq_ci(segment, "SS")) { *code = 2; return 1; }
    if (bedrock_streq_ci(segment, "GS0")) { *code = 3; return 1; }
    if (bedrock_streq_ci(segment, "GS1")) { *code = 4; return 1; }
    if (bedrock_streq_ci(segment, "GS2")) { *code = 5; return 1; }
    if (bedrock_streq_ci(segment, "GS3")) { *code = 6; return 1; }
    if (bedrock_streq_ci(segment, "GS4")) { *code = 7; return 1; }
    return 0;
}

static int bedrock_parse_index_term(char **cursor, uint16_t *index, uint16_t *scale_code, int *signed32_index)
{
    uint64_t reg;
    uint64_t scale;
    char *end;

    if (!bedrock_char_ieq((*cursor)[0], 'D') || !isdigit((unsigned char)(*cursor)[1])) {
        return 0;
    }
    reg = strtoull(*cursor + 1, &end, 10);
    if (end == *cursor + 1 || reg > 7u) {
        return 0;
    }
    *cursor = end;
    *signed32_index = 0;
    if (bedrock_starts_ci(*cursor, ".L", 2u)) {
        *signed32_index = 1;
        *cursor += 2;
    }
    if (**cursor != '*') {
        return 0;
    }
    ++*cursor;
    scale = strtoull(*cursor, &end, 0);
    if (end == *cursor) {
        return 0;
    }
    *cursor = end;
    if (!bedrock_scale_code(scale, scale_code)) {
        return 0;
    }
    *index = (uint16_t)reg;
    return 1;
}

static int bedrock_parse_extended_indexed_ea(char *compact, bedrock_text_operand *out)
{
    char *cursor = compact;
    char *colon;
    uint64_t base_reg = 0;
    uint16_t mode = 0;
    uint16_t segment = 1;
    uint16_t index = 0;
    uint16_t scale = 0;
    uint16_t extra = 0;
    int64_t disp = 0;
    int has_disp = 0;
    int signed32_index = 0;

    colon = strchr(cursor, ':');
    if (colon != 0) {
        *colon = '\0';
        if (!bedrock_segment_code(cursor, &segment)) {
            return 0;
        }
        cursor = colon + 1;
    }

    if (bedrock_char_ieq(cursor[0], 'A') && isdigit((unsigned char)cursor[1])) {
        char *end;
        base_reg = strtoull(cursor + 1, &end, 10);
        if (end == cursor + 1 || base_reg > 7u || *end != '+') {
            return 0;
        }
        cursor = end + 1;
        if (!bedrock_parse_index_term(&cursor, &index, &scale, &signed32_index)) {
            return 0;
        }
        if (*cursor == '+' || *cursor == '-') {
            if (!bedrock_parse_i64(cursor, &disp)) {
                return 0;
            }
            has_disp = 1;
        } else if (*cursor != '\0') {
            return 0;
        }
        if (!has_disp) {
            mode = 0x0u;
        } else if (disp >= -32768 && disp <= 32767) {
            mode = 0x1u;
        } else if (disp >= INT32_MIN && disp <= INT32_MAX) {
            mode = 0x2u;
        } else {
            mode = 0x3u;
        }
        extra = (uint16_t)((base_reg << 5) | ((uint64_t)index << 2) | (uint64_t)scale);
    } else if ((bedrock_starts_ci(cursor, "SP+", 3u) || bedrock_starts_ci(cursor, "PC+", 3u))) {
        int pc_relative = bedrock_char_ieq(cursor[0], 'P');
        segment = 0;
        cursor += 3;
        if (!bedrock_parse_index_term(&cursor, &index, &scale, &signed32_index)) {
            return 0;
        }
        if (*cursor == '+' || *cursor == '-') {
            if (!bedrock_parse_i64(cursor, &disp)) {
                return 0;
            }
        } else if (*cursor == '\0') {
            disp = 0;
        } else {
            return 0;
        }
        if (disp >= -32768 && disp <= 32767) {
            mode = pc_relative ? 0xcu : 0x9u;
        } else if (disp >= INT32_MIN && disp <= INT32_MAX) {
            mode = pc_relative ? 0xdu : 0xau;
        } else {
            mode = pc_relative ? 0xeu : 0xbu;
        }
        extra = (uint16_t)(((uint64_t)index << 2) | (uint64_t)scale);
    } else {
        return 0;
    }

    out->value = signed32_index ? 0x3eu : 0x3fu;
    out->payload[0] = (uint16_t)((mode << 11) | (segment << 8) | extra);
    out->payload_count = 1;
    if (mode == 0x1u || mode == 0x9u || mode == 0xcu) {
        bedrock_payload_from_u64((uint64_t)disp, &out->payload[1], 1);
        out->payload_count = 2;
    } else if (mode == 0x2u || mode == 0xau || mode == 0xdu) {
        bedrock_payload_from_u64((uint64_t)disp, &out->payload[1], 2);
        out->payload_count = 3;
    } else if (mode == 0x3u || mode == 0xbu || mode == 0xeu) {
        bedrock_payload_from_u64((uint64_t)disp, &out->payload[1], 4);
        out->payload_count = 5;
    }
    return 1;
}

static int bedrock_size_value_for_kind(const char *kind, char suffix, uint64_t *value)
{
    char ch = (char)bedrock_ascii_upper((unsigned char)suffix);
    if (ch == '\0') {
        return 0;
    }
    if (strcmp(kind, "BWLQ") == 0) {
        if (ch == 'B') { *value = 0; return 1; }
        if (ch == 'W') { *value = 1; return 1; }
        if (ch == 'L') { *value = 2; return 1; }
        if (ch == 'Q') { *value = 3; return 1; }
        return 0;
    }
    if (strcmp(kind, "LQ") == 0) {
        if (ch == 'L') { *value = 0; return 1; }
        if (ch == 'Q') { *value = 1; return 1; }
        return 0;
    }
    if (strcmp(kind, "WL") == 0) {
        if (ch == 'W') { *value = 0; return 1; }
        if (ch == 'L') { *value = 1; return 1; }
        return 0;
    }
    if (strcmp(kind, "BW") == 0) {
        if (ch == 'B') { *value = 0; return 1; }
        if (ch == 'W') { *value = 1; return 1; }
        return 0;
    }
    if (strcmp(kind, "BWL") == 0 || strcmp(kind, "BWLX") == 0) {
        if (ch == 'B') { *value = 0; return 1; }
        if (ch == 'W') { *value = 1; return 1; }
        if (ch == 'L') { *value = 2; return 1; }
        return 0;
    }
    if (strcmp(kind, "S_D") == 0) {
        if (ch == 'S') { *value = 0; return 1; }
        if (ch == 'D') { *value = 1; return 1; }
        return 0;
    }
    if (strlen(kind) == 1u) {
        if (bedrock_char_ieq(kind[0], ch)) {
            *value = 0;
            return 1;
        }
        return 0;
    }
    return 0;
}

static char bedrock_size_suffix_for_kind(const char *kind, uint64_t value)
{
    if (strcmp(kind, "BWLQ") == 0) {
        return "BWLQ"[value < 4u ? value : 0u];
    }
    if (strcmp(kind, "LQ") == 0) {
        return value == 0u ? 'L' : 'Q';
    }
    if (strcmp(kind, "WL") == 0) {
        return value == 0u ? 'W' : 'L';
    }
    if (strcmp(kind, "BW") == 0) {
        return value == 0u ? 'B' : 'W';
    }
    if (strcmp(kind, "BWL") == 0 || strcmp(kind, "BWLX") == 0) {
        return "BWL"[value < 3u ? value : 0u];
    }
    if (strcmp(kind, "S_D") == 0) {
        return value == 0u ? 'S' : 'D';
    }
    if (strlen(kind) == 1u) {
        return kind[0];
    }
    return '?';
}

static int bedrock_parse_line_text(const char *line, bedrock_text_line *parsed)
{
    const char *cursor;
    const char *mnemonic_start;
    const char *mnemonic_end;
    const char *mnemonic_part_end;
    const char *dot;
    const char *slash;
    memset(parsed, 0, sizeof(*parsed));
    cursor = line;
    while (isspace((unsigned char)*cursor)) {
        ++cursor;
    }
    if (*cursor == '\0') {
        return 0;
    }
    mnemonic_start = cursor;
    while (*cursor != '\0' && !isspace((unsigned char)*cursor)) {
        ++cursor;
    }
    mnemonic_end = cursor;
    mnemonic_part_end = mnemonic_end;
    slash = 0;
    {
        const char *scan;
        for (scan = mnemonic_start; scan < mnemonic_end; ++scan) {
            if (*scan == '/') {
                slash = scan;
            }
        }
    }
    if (slash != 0) {
        char order_name[32];
        uint16_t order_value = 0;
        if ((size_t)(mnemonic_end - slash - 1) >= sizeof(order_name)) {
            return 0;
        }
        bedrock_trim_copy(order_name, sizeof(order_name), slash + 1, mnemonic_end);
        if (!bedrock_lookup_named(bedrock_memory_order_names, bedrock_memory_order_names_count, order_name, &order_value)) {
            return 0;
        }
        parsed->memory_order = order_value;
        parsed->has_memory_order = 1;
        mnemonic_part_end = slash;
    }
    dot = 0;
    {
        const char *scan;
        for (scan = mnemonic_start; scan < mnemonic_part_end; ++scan) {
            if (*scan == '.') {
                dot = scan;
            }
        }
    }
    if (dot != 0 && dot + 2 == mnemonic_part_end) {
        parsed->size_suffix = (char)bedrock_ascii_upper((unsigned char)dot[1]);
        mnemonic_part_end = dot;
    }
    bedrock_trim_copy(parsed->mnemonic, sizeof(parsed->mnemonic), mnemonic_start, mnemonic_part_end);
    while (isspace((unsigned char)*cursor)) {
        ++cursor;
    }
    while (*cursor != '\0') {
        const char *start = cursor;
        int depth = 0;
        if (parsed->operand_count >= BEDROCK_TEXT_MAX_OPERANDS) {
            return 0;
        }
        while (*cursor != '\0') {
            if (*cursor == '[' || *cursor == '{') {
                ++depth;
            } else if (*cursor == ']' || *cursor == '}') {
                --depth;
            } else if (*cursor == ',' && depth == 0) {
                break;
            }
            ++cursor;
        }
        bedrock_trim_copy(parsed->operands[parsed->operand_count], BEDROCK_TEXT_OPERAND_CHARS, start, cursor);
        ++parsed->operand_count;
        if (*cursor == ',') {
            ++cursor;
            while (isspace((unsigned char)*cursor)) {
                ++cursor;
            }
        }
    }
    return 1;
}

static int bedrock_form_mnemonic_matches(const bedrock_form_desc *form, bedrock_text_line *parsed)
{
    size_t len = strlen(form->mnemonic);
    parsed->has_condition = 0;
    parsed->condition = 0;
    if (bedrock_streq_ci(form->mnemonic, parsed->mnemonic)) {
        return 1;
    }
    if (len > 2u && bedrock_char_ieq(form->mnemonic[len - 2u], 'c') && bedrock_char_ieq(form->mnemonic[len - 1u], 'c')) {
        uint16_t condition;
        size_t prefix_len = len - 2u;
        const char *suffix = parsed->mnemonic + prefix_len;
        if (bedrock_starts_ci(parsed->mnemonic, form->mnemonic, prefix_len)
            && *suffix != '\0'
            && bedrock_lookup_named(bedrock_condition_names, bedrock_condition_names_count, suffix, &condition)) {
            parsed->has_condition = 1;
            parsed->condition = condition;
            return 1;
        }
    }
    return 0;
}

static int bedrock_merge_prefix_byte(uint16_t *prefix_word, uint16_t prefix_byte)
{
    uint16_t low = (uint16_t)(*prefix_word & 0x00ffu);
    uint16_t high = (uint16_t)((*prefix_word >> 8) & 0x00ffu);
    if (prefix_byte == 0u || low == prefix_byte || high == prefix_byte) {
        return 1;
    }
    if (low == 0u) {
        *prefix_word = (uint16_t)((*prefix_word & 0xff00u) | prefix_byte);
        return 1;
    }
    if (high == 0u) {
        *prefix_word = (uint16_t)((*prefix_word & 0x00ffu) | (uint16_t)(prefix_byte << 8));
        return 1;
    }
    return 0;
}

static int bedrock_normalize_update_operand(char *operand, uint16_t *prefix_word)
{
    char compact[96];
    char inner[96];
    char *end;
    unsigned long reg;
    uint16_t prefix_byte = 0;
    bedrock_compact_copy(compact, sizeof(compact), operand);
    if (compact[0] != '[' || compact[strlen(compact) - 1u] != ']') {
        return 1;
    }
    bedrock_trim_copy(inner, sizeof(inner), compact + 1, compact + strlen(compact) - 1u);
    if (bedrock_char_ieq(inner[0], 'A') && isdigit((unsigned char)inner[1])) {
        reg = strtoul(inner + 1, &end, 10);
        if (end != inner + 1 && reg <= 7ul && strcmp(end, "++") == 0) {
            prefix_byte = 0x04u;
        } else if (end != inner + 1 && reg <= 7ul && strcmp(end, "--") == 0) {
            prefix_byte = 0x06u;
        } else {
            return 1;
        }
    } else if (inner[0] == '+' && inner[1] == '+' && bedrock_char_ieq(inner[2], 'A') && isdigit((unsigned char)inner[3])) {
        reg = strtoul(inner + 3, &end, 10);
        if (end == inner + 3 || reg > 7ul || *end != '\0') {
            return 1;
        }
        prefix_byte = 0x05u;
    } else if (inner[0] == '-' && inner[1] == '-' && bedrock_char_ieq(inner[2], 'A') && isdigit((unsigned char)inner[3])) {
        reg = strtoul(inner + 3, &end, 10);
        if (end == inner + 3 || reg > 7ul || *end != '\0') {
            return 1;
        }
        prefix_byte = 0x07u;
    } else {
        return 1;
    }
    if (!bedrock_merge_prefix_byte(prefix_word, prefix_byte)) {
        return 0;
    }
    snprintf(operand, BEDROCK_TEXT_OPERAND_CHARS, "[A%lu]", reg);
    return 1;
}

static int bedrock_normalize_update_operands(bedrock_text_line *parsed, uint16_t *prefix_word)
{
    size_t index;
    for (index = 0; index < parsed->operand_count; ++index) {
        if (!bedrock_normalize_update_operand(parsed->operands[index], prefix_word)) {
            return 0;
        }
    }
    return 1;
}

static int bedrock_parse_compact_ea(const char *text, bedrock_text_operand *out, char size_suffix)
{
    char compact[96];
    uint64_t reg;
    int64_t disp;
    char *plus;
    bedrock_compact_copy(compact, sizeof(compact), text);

    if (bedrock_parse_forced_immediate_ea(compact, out)) {
        return 1;
    }
    if (bedrock_parse_numbered_register(compact, 'D', 7, &reg)) {
        out->value = reg;
        out->cost = 1;
        return 1;
    }
    if (bedrock_parse_numbered_register(compact, 'A', 7, &reg)) {
        out->value = 0x08u + reg;
        out->cost = 1;
        return 1;
    }
    if (bedrock_streq_ci(compact, "SP")) {
        out->value = 0x2fu;
        out->cost = 1;
        return 1;
    }
    if (compact[0] != '[') {
        uint64_t imm;
        int64_t signed_imm;
        if ((compact[0] == '-' || compact[0] == '+') && bedrock_parse_i64(compact, &signed_imm)) {
            return bedrock_choose_compact_immediate_ea(signed_imm, (uint64_t)signed_imm, size_suffix, out);
        }
        if (bedrock_parse_u64(compact, &imm)) {
            signed_imm = imm <= 0x7fffffffffffffffull ? (int64_t)imm : INT64_MAX;
            return bedrock_choose_compact_immediate_ea(signed_imm, imm, size_suffix, out);
        }
        return 0;
    }
    if (compact[strlen(compact) - 1u] != ']') {
        return 0;
    }
    compact[strlen(compact) - 1u] = '\0';
    memmove(compact, compact + 1, strlen(compact));

    if (bedrock_parse_extended_indexed_ea(compact, out)) {
        return 1;
    }
    if (bedrock_parse_numbered_register(compact, 'A', 7, &reg)) {
        out->value = 0x10u + reg;
        return 1;
    }
    plus = strchr(compact, '+');
    if (plus != 0) {
        *plus = '\0';
        if (bedrock_parse_numbered_register(compact, 'A', 7, &reg) && bedrock_parse_i64(plus + 1, &disp)) {
            uint64_t udisp = (uint64_t)disp;
            if (disp >= -32768 && disp <= 32767) {
                out->value = 0x18u + reg;
                out->payload_count = 1;
                bedrock_payload_from_u64(udisp, out->payload, 1);
                return 1;
            }
            out->value = 0x20u + reg;
            out->payload_count = 2;
            bedrock_payload_from_u64(udisp, out->payload, 2);
            return 1;
        }
        if (bedrock_streq_ci(compact, "PC") && bedrock_parse_i64(plus + 1, &disp)) {
            uint64_t udisp = (uint64_t)disp;
            if (disp >= -32768 && disp <= 32767) {
                out->value = 0x28u;
                out->payload_count = 1;
                bedrock_payload_from_u64(udisp, out->payload, 1);
                return 1;
            }
            out->value = 0x29u;
            out->payload_count = 2;
            bedrock_payload_from_u64(udisp, out->payload, 2);
            return 1;
        }
        if (bedrock_streq_ci(compact, "SP") && bedrock_parse_i64(plus + 1, &disp)) {
            uint64_t udisp = (uint64_t)disp;
            if (disp >= -32768 && disp <= 32767) {
                out->value = 0x2cu;
                out->payload_count = 1;
                bedrock_payload_from_u64(udisp, out->payload, 1);
                return 1;
            }
            out->value = 0x2du;
            out->payload_count = 2;
            bedrock_payload_from_u64(udisp, out->payload, 2);
            return 1;
        }
    }
    {
        uint64_t absolute;
        if (bedrock_parse_u64(compact, &absolute)) {
            if (absolute <= 0xffffffffull) {
                out->value = 0x30u;
                out->payload_count = 2;
                bedrock_payload_from_u64(absolute, out->payload, 2);
                return 1;
            }
            out->value = 0x31u;
            out->payload_count = 4;
            bedrock_payload_from_u64(absolute, out->payload, 4);
            return 1;
        }
    }
    return 0;
}

static int bedrock_parse_bitmap_register(const char *text, char *kind, unsigned *index)
{
    uint64_t value;
    if (text[0] == '\0' || !isdigit((unsigned char)text[1])) {
        return 0;
    }
    if (!bedrock_char_ieq(text[0], 'D') && !bedrock_char_ieq(text[0], 'A')) {
        return 0;
    }
    if (!bedrock_parse_u64(text + 1, &value) || value > 7u) {
        return 0;
    }
    *kind = (char)bedrock_ascii_upper((unsigned char)text[0]);
    *index = (unsigned)value;
    return 1;
}

static int bedrock_parse_bitmap16(const char *text, uint64_t *value)
{
    char compact[128];
    char token[32];
    char *cursor;
    int braced = 0;
    int closed = 0;
    uint64_t bitmap = 0;
    if (bedrock_parse_u64(text, value)) {
        return *value <= 0xffffu;
    }
    bedrock_compact_copy(compact, sizeof(compact), text);
    cursor = compact;
    if (*cursor == '{') {
        braced = 1;
        ++cursor;
    }
    while (*cursor != '\0') {
        char *start = cursor;
        char *dash;
        char lo_kind, hi_kind;
        unsigned lo_index, hi_index, reg;
        if (*cursor == '}') {
            closed = 1;
            ++cursor;
            break;
        }
        while (*cursor != '\0' && *cursor != ',' && *cursor != '}') {
            ++cursor;
        }
        bedrock_trim_copy(token, sizeof(token), start, cursor);
        if (token[0] == '\0') {
            return 0;
        }
        dash = strchr(token, '-');
        if (dash != 0) {
            *dash = '\0';
            if (!bedrock_parse_bitmap_register(token, &lo_kind, &lo_index)
                || !bedrock_parse_bitmap_register(dash + 1, &hi_kind, &hi_index)
                || lo_kind != hi_kind || lo_index > hi_index) {
                return 0;
            }
            for (reg = lo_index; reg <= hi_index; ++reg) {
                bitmap |= 1ull << (reg + (lo_kind == 'A' ? 8u : 0u));
            }
        } else {
            if (!bedrock_parse_bitmap_register(token, &lo_kind, &lo_index)) {
                return 0;
            }
            bitmap |= 1ull << (lo_index + (lo_kind == 'A' ? 8u : 0u));
        }
        if (*cursor == ',') {
            ++cursor;
        }
    }
    if ((braced && !closed) || (!braced && closed) || *cursor != '\0') {
        return 0;
    }
    *value = bitmap;
    return 1;
}

static int bedrock_parse_operand_for_kind(const bedrock_operand_desc *desc, const char *text, char size_suffix, bedrock_text_operand *out)
{
    uint16_t named;
    memset(out, 0, sizeof(*out));
    bedrock_trim_copy(out->text, sizeof(out->text), text, text + strlen(text));
    if (strcmp(desc->kind, "DREG") == 0) {
        return bedrock_parse_numbered_register(out->text, 'D', 7, &out->value);
    }
    if (strcmp(desc->kind, "DBANK") == 0) {
        return bedrock_parse_dbank_selector(out->text, &out->value);
    }
    if (strcmp(desc->kind, "AREG") == 0) {
        return bedrock_parse_numbered_register(out->text, 'A', 7, &out->value);
    }
    if (strcmp(desc->kind, "SPREG") == 0) {
        out->value = 0;
        return bedrock_streq_ci(out->text, "SP");
    }
    if (strcmp(desc->kind, "FREG") == 0) {
        return bedrock_parse_numbered_register(out->text, 'F', 31, &out->value);
    }
    if (strcmp(desc->kind, "SREG") == 0) {
        if (!bedrock_lookup_named(bedrock_sreg_names, bedrock_sreg_names_count, out->text, &named)) {
            return 0;
        }
        out->value = named;
        return 1;
    }
    if (strcmp(desc->kind, "CR") == 0 || strcmp(desc->kind, "cr") == 0) {
        if (!bedrock_lookup_named(bedrock_cr_names, bedrock_cr_names_count, out->text, &named)) {
            return 0;
        }
        out->value = named;
        return 1;
    }
    if (strcmp(desc->kind, "condition") == 0) {
        if (!bedrock_lookup_named(bedrock_condition_names, bedrock_condition_names_count, out->text, &named)) {
            return 0;
        }
        out->value = named;
        return 1;
    }
    if (strcmp(desc->kind, "memory_order") == 0) {
        if (!bedrock_lookup_named(bedrock_memory_order_names, bedrock_memory_order_names_count, out->text, &named)) {
            return 0;
        }
        out->value = named;
        return 1;
    }
    if (strcmp(desc->kind, "EA") == 0) {
        int ok = bedrock_parse_compact_ea(out->text, out, size_suffix);
        if (ok && strcmp(desc->role, "dst") == 0 && (out->value < 0x10u || out->value == 0x2fu)) {
            out->cost += 3;
        }
        return ok;
    }
    if (strcmp(desc->kind, "IMM_EA") == 0) {
        int ok = bedrock_parse_compact_ea(out->text, out, size_suffix);
        if (!ok) {
            return 0;
        }
        if (out->value == 0x32u || out->value == 0x33u || out->value == 0x34u) {
            out->cost -= 4;
            return 1;
        }
        return 0;
    }
    if (strcmp(desc->kind, "BITMAP16") == 0 || strcmp(desc->kind, "bitmap16") == 0) {
        if (!bedrock_parse_bitmap16(out->text, &out->value)) {
            return 0;
        }
        out->payload_count = 1;
        out->payload[0] = (uint16_t)out->value;
        return 1;
    }
    if (strcmp(desc->kind, "small_selector") == 0) {
        if (bedrock_parse_numbered_register(out->text, 'D', 7, &out->value)) {
            return 1;
        }
        return bedrock_parse_u64(out->text, &out->value);
    }
    if (strcmp(desc->kind, "selector6") == 0 || strcmp(desc->declared_kind, "selector6") == 0) {
        if (!bedrock_parse_u64(out->text, &out->value) || out->value > 63u) {
            return 0;
        }
        return 1;
    }
    if (strstr(desc->kind, "imm") != 0 || strstr(desc->declared_kind, "imm") != 0 || strstr(desc->kind, "asid") != 0) {
        size_t words = bedrock_words_for_size_suffix(size_suffix);
        size_t forced_words = 0;
        if (strstr(desc->kind, "imm16") != 0 || strstr(desc->declared_kind, "imm16") != 0 || strstr(desc->kind, "asid") != 0) {
            words = 1;
        } else if (strstr(desc->kind, "imm32") != 0 || strstr(desc->declared_kind, "imm32") != 0) {
            words = 2;
        } else if (strstr(desc->kind, "imm64") != 0 || strstr(desc->declared_kind, "imm64") != 0) {
            words = 4;
        }
        if (!bedrock_parse_immediate_payload_text(out->text, &out->value, &forced_words)) {
            return 0;
        }
        if (forced_words != 0u) {
            int fixed_width = strstr(desc->kind, "imm16") != 0
                || strstr(desc->declared_kind, "imm16") != 0
                || strstr(desc->kind, "imm32") != 0
                || strstr(desc->declared_kind, "imm32") != 0
                || strstr(desc->kind, "imm64") != 0
                || strstr(desc->declared_kind, "imm64") != 0
                || strstr(desc->kind, "asid") != 0;
            if (fixed_width && forced_words != words) {
                return 0;
            }
            words = forced_words;
        }
        if (words == 1u && !bedrock_value_fits_signed_or_unsigned_bits(out->value, 16u)) {
            return 0;
        }
        if (words == 2u && !bedrock_value_fits_signed_or_unsigned_bits(out->value, 32u)) {
            return 0;
        }
        out->payload_count = words;
        bedrock_payload_from_u64(out->value, out->payload, words);
        return 1;
    }
    return bedrock_parse_u64(out->text, &out->value);
}

static size_t bedrock_payload_start_word(const bedrock_form_desc *form)
{
    size_t index;
    size_t start = bedrock_form_is_extended(form) ? 2u : 1u;
    for (index = 0; index < form->field_count; ++index) {
        const bedrock_field_desc *field = &bedrock_fields[form->field_index + index];
        if ((size_t)field->token + 1u > start) {
            start = (size_t)field->token + 1u;
        }
    }
    return start;
}

static int bedrock_parse_rep_prefix_line(const char *line, uint16_t *prefix_word, const char **inner_line)
{
    const char *cursor = line;
    const char *mnemonic_start;
    const char *mnemonic_end;
    char mnemonic[32];
    char condition_name[32];
    uint16_t condition = 0;
    uint64_t counter = 0;
    while (isspace((unsigned char)*cursor)) {
        ++cursor;
    }
    mnemonic_start = cursor;
    while (*cursor != '\0' && !isspace((unsigned char)*cursor)) {
        ++cursor;
    }
    mnemonic_end = cursor;
    if ((size_t)(mnemonic_end - mnemonic_start) >= sizeof(mnemonic)) {
        return 0;
    }
    bedrock_trim_copy(mnemonic, sizeof(mnemonic), mnemonic_start, mnemonic_end);
    if (bedrock_streq_ci(mnemonic, "REPG") || !bedrock_starts_ci(mnemonic, "REP", 3u)) {
        return 0;
    }
    if (mnemonic[3] == '\0') {
        condition = 0;
    } else {
        bedrock_trim_copy(condition_name, sizeof(condition_name), mnemonic + 3, mnemonic + strlen(mnemonic));
        if (!bedrock_lookup_named(bedrock_condition_names, bedrock_condition_names_count, condition_name, &condition)) {
            return 0;
        }
    }
    while (isspace((unsigned char)*cursor)) {
        ++cursor;
    }
    if (!bedrock_parse_numbered_register(cursor, 'D', 7, &counter)) {
        const char *reg_start = cursor;
        const char *reg_end;
        char reg_text[8];
        while (*cursor != '\0' && *cursor != ',' && !isspace((unsigned char)*cursor)) {
            ++cursor;
        }
        reg_end = cursor;
        bedrock_trim_copy(reg_text, sizeof(reg_text), reg_start, reg_end);
        if (!bedrock_parse_numbered_register(reg_text, 'D', 7, &counter)) {
            return 0;
        }
    } else {
        while (*cursor != '\0' && *cursor != ',' && !isspace((unsigned char)*cursor)) {
            ++cursor;
        }
    }
    while (isspace((unsigned char)*cursor)) {
        ++cursor;
    }
    if (*cursor != ',') {
        return 0;
    }
    ++cursor;
    while (isspace((unsigned char)*cursor)) {
        ++cursor;
    }
    if (*cursor == '\0') {
        return 0;
    }
    *prefix_word = (uint16_t)(0x80u | ((condition & 0x0fu) << 3) | (uint16_t)(counter & 0x07u));
    *inner_line = cursor;
    return 1;
}

static int bedrock_apply_prefix_word(uint16_t prefix_word, uint16_t *out_words, size_t out_word_count, size_t *written_words)
{
    size_t index;
    size_t inner_words;
    size_t total_words;
    if (written_words == 0 || *written_words == 0u) {
        return BEDROCK_ERR_INVALID_ARGUMENT;
    }
    inner_words = *written_words;
    if ((out_words[0] & BEDROCK_WORD0_PREFIX_BIT) != 0u) {
        uint16_t low = (uint16_t)(prefix_word & 0x00ffu);
        uint16_t high = (uint16_t)((prefix_word >> 8) & 0x00ffu);
        if (low != 0u && !bedrock_merge_prefix_byte(&out_words[1], low)) {
            return BEDROCK_ERR_INVALID_ARGUMENT;
        }
        if (high != 0u && !bedrock_merge_prefix_byte(&out_words[1], high)) {
            return BEDROCK_ERR_INVALID_ARGUMENT;
        }
        return BEDROCK_OK;
    }
    total_words = inner_words + 1u;
    if (total_words > out_word_count || total_words > BEDROCK_MAX_INSTRUCTION_WORDS) {
        return BEDROCK_ERR_BUFFER_TOO_SMALL;
    }
    for (index = inner_words; index > 1u; --index) {
        out_words[index] = out_words[index - 1u];
    }
    out_words[1] = prefix_word;
    out_words[0] = (uint16_t)(
        (out_words[0] & (uint16_t)~BEDROCK_WORD0_LENGTH_MASK)
        | BEDROCK_WORD0_PREFIX_BIT
        | (uint16_t)((total_words - 1u) << 12)
    );
    *written_words = total_words;
    return BEDROCK_OK;
}

int bedrock_assemble_line(const char *line, uint16_t *out_words, size_t out_word_count, size_t *written_words, const bedrock_form_desc **matched_form)
{
    bedrock_text_line parsed;
    size_t form_index;
    int best_score = 0x3fffffff;
    const bedrock_form_desc *best_form = 0;
    uint64_t best_fields[BEDROCK_TEXT_MAX_FIELDS];
    bedrock_text_operand best_operands[BEDROCK_TEXT_MAX_OPERANDS];
    uint16_t prefix_word = 0;
    uint16_t operand_prefix_word = 0;
    const char *inner_line = 0;
    if (line != 0 && out_words != 0 && bedrock_parse_rep_prefix_line(line, &prefix_word, &inner_line)) {
        int status = bedrock_assemble_line(inner_line, out_words, out_word_count, written_words, matched_form);
        if (status != BEDROCK_OK) {
            return status;
        }
        return bedrock_apply_prefix_word(prefix_word, out_words, out_word_count, written_words);
    }
    if (line == 0 || out_words == 0 || !bedrock_parse_line_text(line, &parsed)) {
        return BEDROCK_ERR_INVALID_ARGUMENT;
    }
    if (!bedrock_normalize_update_operands(&parsed, &operand_prefix_word)) {
        return BEDROCK_ERR_INVALID_ARGUMENT;
    }
    for (form_index = 0; form_index < bedrock_forms_count; ++form_index) {
        const bedrock_form_desc *form = &bedrock_forms[form_index];
        bedrock_text_line local = parsed;
        bedrock_text_operand parsed_operands[BEDROCK_TEXT_MAX_OPERANDS];
        uint64_t field_values[BEDROCK_TEXT_MAX_FIELDS];
        int score = 0;
        size_t operand_index;
        size_t field_index;
        int ok = 1;
        int form_has_memory_order = 0;
        if (form->field_count > BEDROCK_TEXT_MAX_FIELDS || form->operand_count > BEDROCK_TEXT_MAX_OPERANDS) {
            continue;
        }
        if (!bedrock_form_mnemonic_matches(form, &local) || local.operand_count != form->operand_count) {
            continue;
        }
        for (operand_index = 0; operand_index < form->operand_count; ++operand_index) {
            const bedrock_operand_desc *desc = &bedrock_operands[form->operand_index + operand_index];
            if (!bedrock_parse_operand_for_kind(desc, local.operands[operand_index], local.size_suffix, &parsed_operands[operand_index])) {
                ok = 0;
                break;
            }
            score += parsed_operands[operand_index].cost;
        }
        if (!ok) {
            continue;
        }
        for (field_index = 0; field_index < form->field_count; ++field_index) {
            const bedrock_field_desc *field = &bedrock_fields[form->field_index + field_index];
            int found = 0;
            if (strcmp(field->source, "size") == 0 || strcmp(field->kind, "BWLQ") == 0 || strcmp(field->kind, "LQ") == 0 || strcmp(field->kind, "WL") == 0 || strcmp(field->kind, "BW") == 0 || strcmp(field->kind, "BWL") == 0 || strcmp(field->kind, "BWLX") == 0 || strcmp(field->kind, "S_D") == 0) {
                if (!bedrock_size_value_for_kind(field->kind, local.size_suffix, &field_values[field_index])) {
                    ok = 0;
                    break;
                }
                found = 1;
            } else if (strcmp(field->source, "cc") == 0 || strcmp(field->kind, "condition") == 0) {
                if (!local.has_condition && form->alias_condition[0] != '\0') {
                    uint16_t alias_condition = 0;
                    if (bedrock_lookup_named(bedrock_condition_names, bedrock_condition_names_count, form->alias_condition, &alias_condition)) {
                        local.condition = alias_condition;
                        local.has_condition = 1;
                    }
                }
                field_values[field_index] = local.has_condition ? local.condition : 0;
                found = 1;
            } else if (strcmp(field->kind, "memory_order") == 0) {
                form_has_memory_order = 1;
                if (!local.has_memory_order) {
                    ok = 0;
                    break;
                }
                field_values[field_index] = local.memory_order;
                found = 1;
            } else {
                for (operand_index = 0; operand_index < form->operand_count; ++operand_index) {
                    const bedrock_operand_desc *desc = &bedrock_operands[form->operand_index + operand_index];
                    if (desc->field_index == form->field_index + field_index) {
                        field_values[field_index] = parsed_operands[operand_index].value;
                        found = 1;
                        break;
                    }
                }
            }
            if (!found) {
                ok = 0;
                break;
            }
        }
        if (local.has_memory_order && !form_has_memory_order) {
            ok = 0;
        }
        if (!ok) {
            continue;
        }
        score += (int)form->required_words;
        if (bedrock_form_is_extended(form)) {
            score += 4;
        }
        if (score < best_score) {
            best_score = score;
            best_form = form;
            memcpy(best_fields, field_values, sizeof(uint64_t) * form->field_count);
            memcpy(best_operands, parsed_operands, sizeof(bedrock_text_operand) * form->operand_count);
        }
    }
    if (best_form == 0) {
        return BEDROCK_ERR_NO_MATCH;
    }
    {
        size_t emitted = 0;
        size_t payload_cursor;
        size_t operand_index;
        int status = bedrock_encode_form_words(best_form, best_fields, best_form->field_count, out_words, out_word_count, &emitted);
        if (status != BEDROCK_OK) {
            return status;
        }
        payload_cursor = bedrock_payload_start_word(best_form);
        for (operand_index = 0; operand_index < best_form->operand_count; ++operand_index) {
            const bedrock_operand_desc *desc = &bedrock_operands[best_form->operand_index + operand_index];
            size_t payload_index;
            if (desc->field_index != BEDROCK_NO_FIELD && best_operands[operand_index].payload_count == 0u) {
                continue;
            }
            for (payload_index = 0; payload_index < best_operands[operand_index].payload_count; ++payload_index) {
                if (payload_cursor >= out_word_count || payload_cursor >= BEDROCK_MAX_INSTRUCTION_WORDS) {
                    return BEDROCK_ERR_BUFFER_TOO_SMALL;
                }
                out_words[payload_cursor++] = best_operands[operand_index].payload[payload_index];
            }
        }
        if (payload_cursor > emitted) {
            emitted = payload_cursor;
            out_words[0] = (uint16_t)((out_words[0] & (uint16_t)~BEDROCK_WORD0_LENGTH_MASK) | (uint16_t)((emitted - 1u) << 12));
        }
        if (operand_prefix_word != 0u) {
            status = bedrock_apply_prefix_word(operand_prefix_word, out_words, out_word_count, &emitted);
            if (status != BEDROCK_OK) {
                return status;
            }
        }
        if (written_words != 0) {
            *written_words = emitted;
        }
        if (matched_form != 0) {
            *matched_form = best_form;
        }
    }
    return BEDROCK_OK;
}

static const bedrock_field_desc *bedrock_find_field_by_symbol(const bedrock_form_desc *form, const char *symbol, unsigned occurrence)
{
    size_t index;
    unsigned seen = 0;
    for (index = 0; index < form->field_count; ++index) {
        const bedrock_field_desc *field = &bedrock_fields[form->field_index + index];
        if (strcmp(field->symbol, symbol) == 0) {
            if (seen == occurrence) {
                return field;
            }
            ++seen;
        }
    }
    return 0;
}

static const bedrock_field_desc *bedrock_first_field_by_source_or_kind(const bedrock_form_desc *form, const char *source, const char *kind)
{
    size_t index;
    for (index = 0; index < form->field_count; ++index) {
        const bedrock_field_desc *field = &bedrock_fields[form->field_index + index];
        if ((source != 0 && strcmp(field->source, source) == 0) || (kind != 0 && strcmp(field->kind, kind) == 0)) {
            return field;
        }
    }
    return 0;
}

static int bedrock_append_text(char *out, size_t out_size, size_t *used, const char *text)
{
    size_t len = strlen(text);
    if (*used + len + 1u > out_size) {
        return 0;
    }
    memcpy(out + *used, text, len);
    *used += len;
    out[*used] = '\0';
    return 1;
}

static int bedrock_append_format(char *out, size_t out_size, size_t *used, const char *fmt, unsigned value)
{
    char buf[64];
    int written = snprintf(buf, sizeof(buf), fmt, value);
    if (written < 0 || (size_t)written >= sizeof(buf)) {
        return 0;
    }
    return bedrock_append_text(out, out_size, used, buf);
}

static int bedrock_append_hex64(char *out, size_t out_size, size_t *used, uint64_t value)
{
    char buf[32];
    int written = snprintf(buf, sizeof(buf), "0x%llx", (unsigned long long)value);
    if (written < 0 || (size_t)written >= sizeof(buf)) {
        return 0;
    }
    return bedrock_append_text(out, out_size, used, buf);
}

static int bedrock_append_selector6(char *out, size_t out_size, size_t *used, uint64_t value)
{
    return bedrock_append_format(out, out_size, used, "%u", (unsigned)(value & 0x3fu));
}

static int bedrock_append_bitmap_item(char *out, size_t out_size, size_t *used, int *first, char kind, unsigned start, unsigned end)
{
    char buf[32];
    int written;
    if (!*first && !bedrock_append_text(out, out_size, used, ",")) {
        return 0;
    }
    *first = 0;
    if (start == end) {
        written = snprintf(buf, sizeof(buf), "%c%u", kind, start);
    } else {
        written = snprintf(buf, sizeof(buf), "%c%u-%c%u", kind, start, kind, end);
    }
    if (written < 0 || (size_t)written >= sizeof(buf)) {
        return 0;
    }
    return bedrock_append_text(out, out_size, used, buf);
}

static int bedrock_append_bitmap16(char *out, size_t out_size, size_t *used, uint64_t value)
{
    int first = 1;
    char kind;
    unsigned base;
    if (!bedrock_append_text(out, out_size, used, "{")) {
        return 0;
    }
    for (kind = 'D', base = 0; base <= 8u; kind = 'A', base = 8u) {
        unsigned index = 0;
        while (index < 8u) {
            unsigned start;
            if ((value & (1ull << (base + index))) == 0u) {
                ++index;
                continue;
            }
            start = index;
            while (index + 1u < 8u && (value & (1ull << (base + index + 1u))) != 0u) {
                ++index;
            }
            if (!bedrock_append_bitmap_item(out, out_size, used, &first, kind, start, index)) {
                return 0;
            }
            ++index;
        }
        if (base == 8u) {
            break;
        }
    }
    return bedrock_append_text(out, out_size, used, "}");
}

static uint64_t bedrock_read_payload_words(const uint16_t *words, size_t start, size_t count)
{
    uint64_t value = 0;
    size_t index;
    for (index = 0; index < count && index < 4u; ++index) {
        value |= ((uint64_t)words[start + index]) << (index * 16u);
    }
    return value;
}

static int bedrock_format_ea_value(uint64_t value, char *out, size_t out_size)
{
    if (value < 8u) {
        return snprintf(out, out_size, "D%u", (unsigned)value) > 0;
    }
    if (value < 16u) {
        return snprintf(out, out_size, "A%u", (unsigned)(value - 8u)) > 0;
    }
    if (value >= 0x10u && value <= 0x17u) {
        return snprintf(out, out_size, "[A%u]", (unsigned)(value - 0x10u)) > 0;
    }
    if (value >= 0x18u && value <= 0x1fu) {
        return snprintf(out, out_size, "[A%u + disp16]", (unsigned)(value - 0x18u)) > 0;
    }
    if (value >= 0x20u && value <= 0x27u) {
        return snprintf(out, out_size, "[A%u + disp32]", (unsigned)(value - 0x20u)) > 0;
    }
    if (value == 0x28u) { return snprintf(out, out_size, "[PC + disp16]") > 0; }
    if (value == 0x29u) { return snprintf(out, out_size, "[PC + disp32]") > 0; }
    if (value == 0x2au) { return snprintf(out, out_size, "[PC + disp64]") > 0; }
    if (value == 0x2cu) { return snprintf(out, out_size, "[SP + disp16]") > 0; }
    if (value == 0x2du) { return snprintf(out, out_size, "[SP + disp32]") > 0; }
    if (value == 0x2eu) { return snprintf(out, out_size, "[SP + disp64]") > 0; }
    if (value == 0x2fu) { return snprintf(out, out_size, "SP") > 0; }
    if (value == 0x30u) { return snprintf(out, out_size, "[abs32]") > 0; }
    if (value == 0x31u) { return snprintf(out, out_size, "[abs64]") > 0; }
    if (value == 0x32u) { return snprintf(out, out_size, "imm16") > 0; }
    if (value == 0x33u) { return snprintf(out, out_size, "imm32") > 0; }
    if (value == 0x34u) { return snprintf(out, out_size, "imm64") > 0; }
    if (value == 0x3eu) { return snprintf(out, out_size, "<long-indexed-ea>") > 0; }
    if (value == 0x3fu) { return snprintf(out, out_size, "<extended-ea>") > 0; }
    return snprintf(out, out_size, "<ea:0x%02x>", (unsigned)value) > 0;
}

int bedrock_disassemble_line(const uint16_t *words, size_t word_count, char *out_text, size_t out_text_size, const bedrock_form_desc **matched_form)
{
    const bedrock_form_desc *form;
    const char *cursor;
    size_t used = 0;
    size_t payload_cursor;
    unsigned declared_words;
    unsigned symbol_occurrence[256];
    if (out_text == 0 || out_text_size == 0u) {
        return BEDROCK_ERR_INVALID_ARGUMENT;
    }
    out_text[0] = '\0';
    form = bedrock_decode_form(words, word_count);
    if (form == 0) {
        return BEDROCK_ERR_NO_MATCH;
    }
    memset(symbol_occurrence, 0, sizeof(symbol_occurrence));
    declared_words = bedrock_declared_words(words[0]);
    payload_cursor = bedrock_payload_start_word(form);
    cursor = form->syntax;
    while (*cursor != '\0') {
        if (strncmp(cursor, "<bitmap>", 8) == 0) {
            if (payload_cursor >= declared_words) {
                return BEDROCK_ERR_UNDERSIZED_ENCODING;
            }
            if (!bedrock_append_bitmap16(out_text, out_text_size, &used, words[payload_cursor++])) {
                return BEDROCK_ERR_BUFFER_TOO_SMALL;
            }
            cursor += 8;
            continue;
        }
        if (strncmp(cursor, "imm64", 5) == 0 || strncmp(cursor, "imm32", 5) == 0 || strncmp(cursor, "imm16", 5) == 0 || strncmp(cursor, "imm", 3) == 0) {
            size_t payload_words = 1;
            size_t token_len = 3;
            if (strncmp(cursor, "imm64", 5) == 0) {
                payload_words = 4;
                token_len = 5;
            } else if (strncmp(cursor, "imm32", 5) == 0) {
                payload_words = 2;
                token_len = 5;
            } else if (strncmp(cursor, "imm16", 5) == 0) {
                payload_words = 1;
                token_len = 5;
            } else if (declared_words > payload_cursor) {
                payload_words = declared_words - payload_cursor;
                if (payload_words > 4u) {
                    payload_words = 4u;
                }
            }
            if (payload_cursor + payload_words > declared_words) {
                return BEDROCK_ERR_UNDERSIZED_ENCODING;
            }
            if (!bedrock_append_hex64(out_text, out_text_size, &used, bedrock_read_payload_words(words, payload_cursor, payload_words))) {
                return BEDROCK_ERR_BUFFER_TOO_SMALL;
            }
            payload_cursor += payload_words;
            cursor += token_len;
            continue;
        }
        if (strncmp(cursor, ".X(", 3) == 0) {
            const bedrock_field_desc *field = bedrock_first_field_by_source_or_kind(form, "size", 0);
            if (field != 0) {
                char suffix[3];
                suffix[0] = '.';
                suffix[1] = bedrock_size_suffix_for_kind(field->kind, bedrock_extract_field(words, field));
                suffix[2] = '\0';
                if (!bedrock_append_text(out_text, out_text_size, &used, suffix)) {
                    return BEDROCK_ERR_BUFFER_TOO_SMALL;
                }
                cursor = strchr(cursor, ')');
                if (cursor == 0) {
                    return BEDROCK_ERR_INVALID_ARGUMENT;
                }
                ++cursor;
                continue;
            }
        }
        if (strncmp(cursor, "{condition}", 11) == 0) {
            const bedrock_field_desc *field = bedrock_first_field_by_source_or_kind(form, "cc", "condition");
            uint16_t condition = 0;
            if (field != 0) {
                condition = (uint16_t)bedrock_extract_field(words, field);
            } else if (form->alias_condition[0] != '\0') {
                (void)bedrock_lookup_named(bedrock_condition_names, bedrock_condition_names_count, form->alias_condition, &condition);
            }
            if (!bedrock_append_text(out_text, out_text_size, &used, bedrock_name_for_value(bedrock_condition_names, bedrock_condition_names_count, condition))) {
                return BEDROCK_ERR_BUFFER_TOO_SMALL;
            }
            cursor += 11;
            continue;
        }
        if ((strncmp(cursor, "Dn(", 3) == 0 || strncmp(cursor, "DBn(", 4) == 0 || strncmp(cursor, "An(", 3) == 0 || strncmp(cursor, "Fn(", 3) == 0 || strncmp(cursor, "Sreg(", 5) == 0 || strncmp(cursor, "ORDER(", 6) == 0 || strncmp(cursor, "order(", 6) == 0 || strncmp(cursor, "<ea(", 4) == 0 || strncmp(cursor, "<imm(", 5) == 0 || strncmp(cursor, "<cr(", 4) == 0 || strncmp(cursor, "<count(", 7) == 0 || strncmp(cursor, "<bit_index(", 11) == 0)) {
            const char *open = strchr(cursor, '(');
            const char *close = open != 0 ? strchr(open, ')') : 0;
            char symbol[16];
            const bedrock_field_desc *field;
            uint64_t value;
            unsigned char key;
            if (open == 0 || close == 0 || (size_t)(close - open - 1) >= sizeof(symbol)) {
                return BEDROCK_ERR_INVALID_ARGUMENT;
            }
            bedrock_trim_copy(symbol, sizeof(symbol), open + 1, close);
            key = (unsigned char)symbol[0];
            field = bedrock_find_field_by_symbol(form, symbol, symbol_occurrence[key]++);
            if (field == 0) {
                return BEDROCK_ERR_INVALID_ARGUMENT;
            }
            value = bedrock_extract_field(words, field);
            if (strncmp(cursor, "Dn(", 3) == 0) {
                if (!bedrock_append_format(out_text, out_text_size, &used, "D%u", (unsigned)value)) { return BEDROCK_ERR_BUFFER_TOO_SMALL; }
            } else if (strncmp(cursor, "DBn(", 4) == 0) {
                if (!bedrock_append_format(out_text, out_text_size, &used, "DB%u", (unsigned)value)) { return BEDROCK_ERR_BUFFER_TOO_SMALL; }
            } else if (strncmp(cursor, "An(", 3) == 0) {
                if (!bedrock_append_format(out_text, out_text_size, &used, "A%u", (unsigned)value)) { return BEDROCK_ERR_BUFFER_TOO_SMALL; }
            } else if (strncmp(cursor, "Fn(", 3) == 0) {
                if (!bedrock_append_format(out_text, out_text_size, &used, "F%u", (unsigned)value)) { return BEDROCK_ERR_BUFFER_TOO_SMALL; }
            } else if (strncmp(cursor, "Sreg(", 5) == 0) {
                if (!bedrock_append_text(out_text, out_text_size, &used, bedrock_name_for_value(bedrock_sreg_names, bedrock_sreg_names_count, (uint16_t)value))) { return BEDROCK_ERR_BUFFER_TOO_SMALL; }
            } else if (strncmp(cursor, "<cr(", 4) == 0) {
                if (!bedrock_append_text(out_text, out_text_size, &used, bedrock_name_for_value(bedrock_cr_names, bedrock_cr_names_count, (uint16_t)value))) { return BEDROCK_ERR_BUFFER_TOO_SMALL; }
            } else if (strncmp(cursor, "ORDER(", 6) == 0 || strncmp(cursor, "order(", 6) == 0) {
                if (!bedrock_append_text(out_text, out_text_size, &used, bedrock_name_for_value(bedrock_memory_order_names, bedrock_memory_order_names_count, (uint16_t)value))) { return BEDROCK_ERR_BUFFER_TOO_SMALL; }
            } else if (strcmp(field->kind, "selector6") == 0) {
                if (!bedrock_append_selector6(out_text, out_text_size, &used, value)) { return BEDROCK_ERR_BUFFER_TOO_SMALL; }
            } else if (strcmp(field->kind, "small_selector") == 0) {
                if (!bedrock_append_format(out_text, out_text_size, &used, "%u", (unsigned)value)) { return BEDROCK_ERR_BUFFER_TOO_SMALL; }
            } else {
                char ea_text[64];
                if (!bedrock_format_ea_value(value, ea_text, sizeof(ea_text)) || !bedrock_append_text(out_text, out_text_size, &used, ea_text)) { return BEDROCK_ERR_BUFFER_TOO_SMALL; }
            }
            cursor = close + 1;
            if (*cursor == '>') {
                ++cursor;
            }
            continue;
        }
        {
            char one[2];
            one[0] = *cursor++;
            one[1] = '\0';
            if (!bedrock_append_text(out_text, out_text_size, &used, one)) {
                return BEDROCK_ERR_BUFFER_TOO_SMALL;
            }
        }
    }
    if (matched_form != 0) {
        *matched_form = form;
    }
    return BEDROCK_OK;
}
'''


def render_header() -> str:
    return """/* Generated from build/generated/allocation_plan.json. */
#ifndef BEDROCK_ASM_DISASM_H
#define BEDROCK_ASM_DISASM_H

#include <stddef.h>
#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

#define BEDROCK_MAX_INSTRUCTION_WORDS 8u
#define BEDROCK_WORD0_PREFIX_BIT 0x8000u
#define BEDROCK_WORD0_LENGTH_MASK 0x7000u
#define BEDROCK_WORD0_PAYLOAD_MASK 0x0fffu
#define BEDROCK_NO_FIELD 0xffffu

typedef enum bedrock_form_kind {
    BEDROCK_FORM_COMPACT = 0,
    BEDROCK_FORM_COMPACT_ALIAS = 1,
    BEDROCK_FORM_EXTENDED = 2,
    BEDROCK_FORM_EXTENDED_ALIAS = 3
} bedrock_form_kind;

typedef enum bedrock_status {
    BEDROCK_OK = 0,
    BEDROCK_ERR_INVALID_ARGUMENT = -1,
    BEDROCK_ERR_BUFFER_TOO_SMALL = -2,
    BEDROCK_ERR_FIELD_VALUE_TOO_LARGE = -3,
    BEDROCK_ERR_UNDERSIZED_ENCODING = -4,
    BEDROCK_ERR_NO_MATCH = -5
} bedrock_status;

typedef struct bedrock_field_desc {
    const char *name;
    const char *kind;
    const char *source;
    const char *symbol;
    uint8_t token;
    uint8_t low_bit;
    uint8_t width;
} bedrock_field_desc;

typedef struct bedrock_named_value {
    const char *name;
    uint16_t value;
} bedrock_named_value;

typedef struct bedrock_operand_desc {
    const char *role;
    const char *declared_kind;
    const char *kind;
    uint16_t field_index;
} bedrock_operand_desc;

typedef struct bedrock_form_desc {
    const char *id;
    const char *mnemonic;
    const char *syntax;
    bedrock_form_kind kind;
    const char *category;
    const char *group;
    const char *privilege;
    uint16_t primary_start;
    uint16_t primary_end;
    uint16_t ext_start;
    uint16_t ext_end;
    uint8_t min_words;
    uint8_t max_words;
    uint8_t required_words;
    uint16_t field_index;
    uint16_t field_count;
    uint16_t operand_index;
    uint16_t operand_count;
    uint16_t primary_value_index;
    uint16_t primary_value_count;
    const char *alias_of;
    const char *alias_condition;
} bedrock_form_desc;

extern const bedrock_form_desc bedrock_forms[];
extern const bedrock_field_desc bedrock_fields[];
extern const bedrock_operand_desc bedrock_operands[];
extern const uint16_t bedrock_primary_values[];
extern const bedrock_named_value bedrock_condition_names[];
extern const bedrock_named_value bedrock_sreg_names[];
extern const bedrock_named_value bedrock_cr_names[];
extern const bedrock_named_value bedrock_memory_order_names[];
extern const size_t bedrock_forms_count;
extern const size_t bedrock_fields_count;
extern const size_t bedrock_operands_count;
extern const size_t bedrock_primary_values_count;
extern const size_t bedrock_condition_names_count;
extern const size_t bedrock_sreg_names_count;
extern const size_t bedrock_cr_names_count;
extern const size_t bedrock_memory_order_names_count;

size_t bedrock_form_count(void);
const bedrock_form_desc *bedrock_form_at(size_t index);
const bedrock_field_desc *bedrock_form_field(const bedrock_form_desc *form, size_t index);
const bedrock_operand_desc *bedrock_form_operand(const bedrock_form_desc *form, size_t index);
const bedrock_form_desc *bedrock_find_form_by_id(const char *id);
const bedrock_form_desc *bedrock_find_first_mnemonic(const char *mnemonic);
const bedrock_form_desc *bedrock_find_form_by_signature(const char *mnemonic, const char *const *operand_kinds, size_t operand_count);
const bedrock_form_desc *bedrock_decode_form(const uint16_t *words, size_t word_count);
int bedrock_assemble_line(const char *line, uint16_t *out_words, size_t out_word_count, size_t *written_words, const bedrock_form_desc **matched_form);
int bedrock_disassemble_line(const uint16_t *words, size_t word_count, char *out_text, size_t out_text_size, const bedrock_form_desc **matched_form);

uint64_t bedrock_extract_field(const uint16_t *words, const bedrock_field_desc *field);
int bedrock_insert_field(uint16_t *words, size_t word_count, const bedrock_field_desc *field, uint64_t value);
int bedrock_encode_form_words(const bedrock_form_desc *form, const uint64_t *field_values, size_t field_value_count, uint16_t *out_words, size_t out_word_count, size_t *written_words);

#ifdef __cplusplus
}
#endif

#endif
"""


def render_source(model: dict[str, Any], header_name: str, named_values: dict[str, list[tuple[str, int]]]) -> str:
    forms = model["forms"]
    fields = model["fields"]
    operands = model["operands"]
    primary_values = model["primary_values"]
    lines: list[str] = [
        "/* Generated from build/generated/allocation_plan.json. */",
        f'#include "{header_name}"',
        "",
        "#include <ctype.h>",
        "#include <limits.h>",
        "#include <stdio.h>",
        "#include <stdlib.h>",
        "#include <string.h>",
        "",
    ]

    lines.append("const bedrock_field_desc bedrock_fields[] = {")
    if fields:
        for field in fields:
            lines.append(
                "    {"
                f"{cstr(field.get('name', ''))}, "
                f"{cstr(field.get('kind', ''))}, "
                f"{cstr(field.get('source', ''))}, "
                f"{cstr(field.get('symbol', ''))}, "
                f"{int(field.get('token', 0))}u, "
                f"{int(field.get('low_bit', 0))}u, "
                f"{int(field.get('width', 0))}u"
                "},"
            )
    else:
        lines.append("    {0},")
    lines.append("};")
    lines.append("")

    lines.append("const bedrock_operand_desc bedrock_operands[] = {")
    if operands:
        for operand in operands:
            lines.append(
                "    {"
                f"{cstr(operand['role'])}, "
                f"{cstr(operand['declared_kind'])}, "
                f"{cstr(operand['kind'])}, "
                f"{int(operand['field_index'])}u"
                "},"
            )
    else:
        lines.append("    {0},")
    lines.append("};")
    lines.append("")

    lines.append("const uint16_t bedrock_primary_values[] = {")
    if primary_values:
        for value in primary_values:
            lines.append(f"    0x{value:03x}u,")
    else:
        lines.append("    0u,")
    lines.append("};")
    lines.append("")

    for array_name, values in (
        ("bedrock_condition_names", named_values["conditions"]),
        ("bedrock_sreg_names", named_values["sregs"]),
        ("bedrock_cr_names", named_values["crs"]),
        ("bedrock_memory_order_names", named_values["memory_orders"]),
    ):
        lines.append(f"const bedrock_named_value {array_name}[] = {{")
        if values:
            for name, value in values:
                lines.append(f"    {{{cstr(name)}, {value}u}},")
        else:
            lines.append("    {0},")
        lines.append("};")
        lines.append("")

    lines.append("const bedrock_form_desc bedrock_forms[] = {")
    for form in forms:
        lines.append(
            "    {"
            f"{cstr(form['id'])}, "
            f"{cstr(form['mnemonic'])}, "
            f"{cstr(form['syntax'])}, "
            f"{form['kind']}, "
            f"{cstr(form['category'])}, "
            f"{cstr(form['group'])}, "
            f"{cstr(form['privilege'])}, "
            f"0x{form['primary_start']:03x}u, "
            f"0x{form['primary_end']:03x}u, "
            f"0x{form['ext_start']:04x}u, "
            f"0x{form['ext_end']:04x}u, "
            f"{form['min_words']}u, "
            f"{form['max_words']}u, "
            f"{form['required_words']}u, "
            f"{form['field_index']}u, "
            f"{form['field_count']}u, "
            f"{form['operand_index']}u, "
            f"{form['operand_count']}u, "
            f"{form['primary_value_index']}u, "
            f"{form['primary_value_count']}u, "
            f"{cstr(form['alias_of'])}, "
            f"{cstr(form['alias_condition'])}"
            "},"
        )
    lines.append("};")
    lines.append("")

    lines.extend(
        [
            "const size_t bedrock_forms_count = sizeof(bedrock_forms) / sizeof(bedrock_forms[0]);",
            "const size_t bedrock_fields_count = sizeof(bedrock_fields) / sizeof(bedrock_fields[0]);",
            "const size_t bedrock_operands_count = sizeof(bedrock_operands) / sizeof(bedrock_operands[0]);",
            "const size_t bedrock_primary_values_count = sizeof(bedrock_primary_values) / sizeof(bedrock_primary_values[0]);",
            "const size_t bedrock_condition_names_count = sizeof(bedrock_condition_names) / sizeof(bedrock_condition_names[0]);",
            "const size_t bedrock_sreg_names_count = sizeof(bedrock_sreg_names) / sizeof(bedrock_sreg_names[0]);",
            "const size_t bedrock_cr_names_count = sizeof(bedrock_cr_names) / sizeof(bedrock_cr_names[0]);",
            "const size_t bedrock_memory_order_names_count = sizeof(bedrock_memory_order_names) / sizeof(bedrock_memory_order_names[0]);",
            "",
            "static uint16_t bedrock_word0_payload(uint16_t word0)",
            "{",
            "    return (uint16_t)(word0 & BEDROCK_WORD0_PAYLOAD_MASK);",
            "}",
            "",
            "static unsigned bedrock_declared_words(uint16_t word0)",
            "{",
            "    return (unsigned)(((word0 & BEDROCK_WORD0_LENGTH_MASK) >> 12) + 1u);",
            "}",
            "",
            "static int bedrock_primary_matches(const bedrock_form_desc *form, uint16_t payload)",
            "{",
            "    if (form->primary_value_count != 0u) {",
            "        size_t index;",
            "        for (index = 0; index < form->primary_value_count; ++index) {",
            "            if (bedrock_primary_values[form->primary_value_index + index] == payload) {",
            "                return 1;",
            "            }",
            "        }",
            "        return 0;",
            "    }",
            "    return payload >= form->primary_start && payload <= form->primary_end;",
            "}",
            "",
            "static int bedrock_form_is_extended(const bedrock_form_desc *form)",
            "{",
            "    return form->kind == BEDROCK_FORM_EXTENDED || form->kind == BEDROCK_FORM_EXTENDED_ALIAS;",
            "}",
            "",
            "size_t bedrock_form_count(void)",
            "{",
            "    return bedrock_forms_count;",
            "}",
            "",
            "const bedrock_form_desc *bedrock_form_at(size_t index)",
            "{",
            "    return index < bedrock_forms_count ? &bedrock_forms[index] : 0;",
            "}",
            "",
            "const bedrock_field_desc *bedrock_form_field(const bedrock_form_desc *form, size_t index)",
            "{",
            "    if (form == 0 || index >= form->field_count) {",
            "        return 0;",
            "    }",
            "    return &bedrock_fields[form->field_index + index];",
            "}",
            "",
            "const bedrock_operand_desc *bedrock_form_operand(const bedrock_form_desc *form, size_t index)",
            "{",
            "    if (form == 0 || index >= form->operand_count) {",
            "        return 0;",
            "    }",
            "    return &bedrock_operands[form->operand_index + index];",
            "}",
            "",
            "const bedrock_form_desc *bedrock_find_form_by_id(const char *id)",
            "{",
            "    size_t index;",
            "    if (id == 0) {",
            "        return 0;",
            "    }",
            "    for (index = 0; index < bedrock_forms_count; ++index) {",
            "        if (strcmp(bedrock_forms[index].id, id) == 0) {",
            "            return &bedrock_forms[index];",
            "        }",
            "    }",
            "    return 0;",
            "}",
            "",
            "const bedrock_form_desc *bedrock_find_first_mnemonic(const char *mnemonic)",
            "{",
            "    size_t index;",
            "    if (mnemonic == 0) {",
            "        return 0;",
            "    }",
            "    for (index = 0; index < bedrock_forms_count; ++index) {",
            "        if (strcmp(bedrock_forms[index].mnemonic, mnemonic) == 0) {",
            "            return &bedrock_forms[index];",
            "        }",
            "    }",
            "    return 0;",
            "}",
            "",
            "const bedrock_form_desc *bedrock_find_form_by_signature(const char *mnemonic, const char *const *operand_kinds, size_t operand_count)",
            "{",
            "    size_t index;",
            "    if (mnemonic == 0 || (operand_count != 0u && operand_kinds == 0)) {",
            "        return 0;",
            "    }",
            "    for (index = 0; index < bedrock_forms_count; ++index) {",
            "        const bedrock_form_desc *form = &bedrock_forms[index];",
            "        size_t operand_index;",
            "        int matches = 1;",
            "        if (strcmp(form->mnemonic, mnemonic) != 0 || form->operand_count != operand_count) {",
            "            continue;",
            "        }",
            "        for (operand_index = 0; operand_index < operand_count; ++operand_index) {",
            "            const bedrock_operand_desc *operand = &bedrock_operands[form->operand_index + operand_index];",
            "            if (operand_kinds[operand_index] == 0 || strcmp(operand->kind, operand_kinds[operand_index]) != 0) {",
            "                matches = 0;",
            "                break;",
            "            }",
            "        }",
            "        if (matches) {",
            "            return form;",
            "        }",
            "    }",
            "    return 0;",
            "}",
            "",
            "const bedrock_form_desc *bedrock_decode_form(const uint16_t *words, size_t word_count)",
            "{",
            "    uint16_t payload;",
            "    unsigned declared_words;",
            "    size_t index;",
            "    if (words == 0 || word_count == 0u) {",
            "        return 0;",
            "    }",
            "    declared_words = bedrock_declared_words(words[0]);",
            "    if (word_count < declared_words) {",
            "        return 0;",
            "    }",
            "    payload = bedrock_word0_payload(words[0]);",
            "    for (index = 0; index < bedrock_forms_count; ++index) {",
            "        const bedrock_form_desc *form = &bedrock_forms[index];",
            "        if (declared_words < form->required_words || declared_words > form->max_words) {",
            "            continue;",
            "        }",
            "        if (!bedrock_primary_matches(form, payload)) {",
            "            continue;",
            "        }",
            "        if (bedrock_form_is_extended(form)) {",
            "            if (declared_words < 2u || words[1] < form->ext_start || words[1] > form->ext_end) {",
            "                continue;",
            "            }",
            "        }",
            "        {",
            "            size_t field_index;",
            "            int fields_valid = 1;",
            "            for (field_index = 0; field_index < form->field_count; ++field_index) {",
            "                const bedrock_field_desc *field = &bedrock_fields[form->field_index + field_index];",
            "                if (strcmp(field->kind, \"memory_order\") == 0 && bedrock_extract_field(words, field) > 4u) {",
            "                    fields_valid = 0;",
            "                    break;",
            "                }",
            "            }",
            "            if (!fields_valid) {",
            "                continue;",
            "            }",
            "        }",
            "        return form;",
            "    }",
            "    return 0;",
            "}",
            "",
            "uint64_t bedrock_extract_field(const uint16_t *words, const bedrock_field_desc *field)",
            "{",
            "    uint64_t mask;",
            "    uint16_t word;",
            "    if (words == 0 || field == 0 || field->width == 0u) {",
            "        return 0;",
            "    }",
            "    word = words[field->token];",
            "    mask = field->width >= 16u ? 0xffffu : ((1ull << field->width) - 1ull);",
            "    return ((uint64_t)word >> field->low_bit) & mask;",
            "}",
            "",
            "int bedrock_insert_field(uint16_t *words, size_t word_count, const bedrock_field_desc *field, uint64_t value)",
            "{",
            "    uint64_t mask;",
            "    uint16_t shifted_mask;",
            "    if (words == 0 || field == 0 || field->width == 0u) {",
            "        return BEDROCK_ERR_INVALID_ARGUMENT;",
            "    }",
            "    if ((size_t)field->token >= word_count) {",
            "        return BEDROCK_ERR_BUFFER_TOO_SMALL;",
            "    }",
            "    mask = field->width >= 16u ? 0xffffu : ((1ull << field->width) - 1ull);",
            "    if ((value & ~mask) != 0ull) {",
            "        return BEDROCK_ERR_FIELD_VALUE_TOO_LARGE;",
            "    }",
            "    shifted_mask = (uint16_t)(mask << field->low_bit);",
            "    words[field->token] = (uint16_t)((words[field->token] & (uint16_t)~shifted_mask) | (uint16_t)((value & mask) << field->low_bit));",
            "    return BEDROCK_OK;",
            "}",
            "",
            "int bedrock_encode_form_words(const bedrock_form_desc *form, const uint64_t *field_values, size_t field_value_count, uint16_t *out_words, size_t out_word_count, size_t *written_words)",
            "{",
            "    size_t index;",
            "    size_t required;",
            "    if (form == 0 || out_words == 0) {",
            "        return BEDROCK_ERR_INVALID_ARGUMENT;",
            "    }",
            "    required = form->required_words;",
            "    if (required == 0u || required > BEDROCK_MAX_INSTRUCTION_WORDS) {",
            "        return BEDROCK_ERR_INVALID_ARGUMENT;",
            "    }",
            "    if (out_word_count < required) {",
            "        return BEDROCK_ERR_BUFFER_TOO_SMALL;",
            "    }",
            "    if (form->field_count != 0u && field_values == 0) {",
            "        return BEDROCK_ERR_INVALID_ARGUMENT;",
            "    }",
            "    if (field_value_count < form->field_count) {",
            "        return BEDROCK_ERR_INVALID_ARGUMENT;",
            "    }",
            "    for (index = 0; index < required; ++index) {",
            "        out_words[index] = 0;",
            "    }",
            "    out_words[0] = (uint16_t)((((uint16_t)(required - 1u)) << 12) | (form->primary_start & BEDROCK_WORD0_PAYLOAD_MASK));",
            "    if (bedrock_form_is_extended(form)) {",
            "        out_words[1] = form->ext_start;",
            "    }",
            "    for (index = 0; index < form->field_count; ++index) {",
            "        int status = bedrock_insert_field(out_words, required, &bedrock_fields[form->field_index + index], field_values[index]);",
            "        if (status != BEDROCK_OK) {",
            "            return status;",
            "        }",
            "    }",
            "    if (!bedrock_primary_matches(form, bedrock_word0_payload(out_words[0]))) {",
            "        return BEDROCK_ERR_INVALID_ARGUMENT;",
            "    }",
            "    if (written_words != 0) {",
            "        *written_words = required;",
            "    }",
            "    return BEDROCK_OK;",
            "}",
            "",
        ]
    )
    lines.append(TEXT_RUNTIME_C)
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("spec_dir", nargs="?", default="isa/spec")
    parser.add_argument("--allocation", default="build/generated/allocation_plan.json")
    parser.add_argument("--header", default="build/generated/bedrock_asm_disasm.h")
    parser.add_argument("--source", default="build/generated/bedrock_asm_disasm.c")
    args = parser.parse_args(argv)

    allocation = Path(args.allocation)
    header = Path(args.header)
    source = Path(args.source)
    spec = load_spec(args.spec_dir)
    model = form_model(allocation_items(load_plan(allocation)))
    named_values = named_values_from_spec(spec)

    header.parent.mkdir(parents=True, exist_ok=True)
    source.parent.mkdir(parents=True, exist_ok=True)
    header.write_text(render_header(), encoding="utf-8")
    source.write_text(render_source(model, header.name, named_values), encoding="utf-8")
    print(f"wrote {header}")
    print(f"wrote {source}")
    print(f"forms: {len(model['forms'])}, fields: {len(model['fields'])}, operands: {len(model['operands'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
