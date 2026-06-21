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
    set_active_spec,
    split_operand,
)
from isa_spec import load_spec  # noqa: E402
from spec_model.encoding import (
    bitmap_operand_ranges,
    condition_named_values,
    compact_ea_values_by_name,
    control_register_named_values,
    ea_segment_named_values,
    named_values as spec_named_values,
    prefix_value,
    size_codes,
    size_kind_entries,
    size_kinds,
    special_register_named_values,
)
from template_utils import load_tool_template, render_tool_template  # noqa: E402


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
    return {
        "conditions": condition_named_values(spec),
        "sregs": special_register_named_values(spec, "S"),
        "crs": control_register_named_values(spec, "CR"),
        "ea_segments": ea_segment_named_values(spec),
        "memory_orders": spec_named_values(spec, "memory_order"),
    }


TEXT_RUNTIME_C = load_tool_template("bedrock_text_runtime.c")
CORE_HELPERS_C = load_tool_template("bedrock_asm_disasm_core.c")


def render_header() -> str:
    return load_tool_template("bedrock_asm_disasm.h")


def render_source(model: dict[str, Any], header_name: str, named_values: dict[str, list[tuple[str, int]]]) -> str:
    forms = model["forms"]
    fields = model["fields"]
    operands = model["operands"]
    primary_values = model["primary_values"]
    lines: list[str] = []

    lines.append("typedef struct bedrock_size_code_desc { char code; char suffix; uint8_t bytes; } bedrock_size_code_desc;")
    lines.append("typedef struct bedrock_size_kind_value_desc { const char *kind; uint16_t value; char code; } bedrock_size_kind_value_desc;")
    lines.append("typedef struct bedrock_bitmap_range_desc { const char *kind; uint8_t low_bit; uint8_t high_bit; char reg_prefix; } bedrock_bitmap_range_desc;")
    lines.append("")

    for prefix_name in ("POSTINC", "PREINC", "POSTDEC", "PREDEC"):
        lines.append(f"#define BEDROCK_PREFIX_{prefix_name} 0x{prefix_value(model['spec'], prefix_name):02x}u")
    for ea_name, ea_value in sorted(compact_ea_values_by_name(model["spec"]).items()):
        lines.append(f"#define BEDROCK_EA_{ea_name} 0x{ea_value:02x}u")
    lines.append("")

    lines.append("const bedrock_size_code_desc bedrock_size_codes[] = {")
    for code, body in size_codes(model["spec"]).items():
        suffix = str(body.get("suffix", ".?"))
        lines.append(f"    {{'{code}', '{suffix[-1]}', {int(body.get('bytes', 0))}u}},")
    lines.append("};")
    lines.append("")

    lines.append("const bedrock_size_kind_value_desc bedrock_size_kind_values[] = {")
    for kind in sorted(size_kinds(model["spec"])):
        for item in size_kind_entries(model["spec"], kind):
            lines.append(f"    {{{cstr(kind)}, {int(item.get('value', 0))}u, '{str(item.get('code'))[0]}'}},")
    lines.append("};")
    lines.append("")

    lines.append("const bedrock_bitmap_range_desc bedrock_bitmap_ranges[] = {")
    bitmap_operands = (
        model["spec"]
        .get("instructions", {})
        .get("operand_schema", {})
        .get("bitmap_operands", {})
    )
    bitmap_names = sorted(bitmap_operands) if isinstance(bitmap_operands, dict) else ["bitmap16"]
    for bitmap_name in bitmap_names:
        for item in bitmap_operand_ranges(model["spec"], bitmap_name):
            bits = item.get("bits", [])
            reg_class = str(item.get("register_class"))
            lines.append(f"    {{{cstr(bitmap_name)}, {int(bits[0])}u, {int(bits[1])}u, '{reg_class[0]}'}},")
    lines.append("};")
    lines.append("")

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
        ("bedrock_ea_segment_names", named_values["ea_segments"]),
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
            "const size_t bedrock_ea_segment_names_count = sizeof(bedrock_ea_segment_names) / sizeof(bedrock_ea_segment_names[0]);",
            "const size_t bedrock_memory_order_names_count = sizeof(bedrock_memory_order_names) / sizeof(bedrock_memory_order_names[0]);",
            "const size_t bedrock_size_codes_count = sizeof(bedrock_size_codes) / sizeof(bedrock_size_codes[0]);",
            "const size_t bedrock_size_kind_values_count = sizeof(bedrock_size_kind_values) / sizeof(bedrock_size_kind_values[0]);",
            "const size_t bedrock_bitmap_ranges_count = sizeof(bedrock_bitmap_ranges) / sizeof(bedrock_bitmap_ranges[0]);",
        ]
    )
    return render_tool_template(
        "bedrock_asm_disasm.c",
        {
            "HEADER_NAME": header_name,
            "FORM_METADATA": "\n".join(lines),
            "CORE_HELPERS": CORE_HELPERS_C.rstrip("\n"),
            "TEXT_RUNTIME": TEXT_RUNTIME_C.rstrip("\n"),
        },
    )


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
    set_active_spec(spec)
    model = form_model(allocation_items(load_plan(allocation)))
    model["spec"] = spec
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
