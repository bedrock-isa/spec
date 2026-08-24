#!/usr/bin/env python3
"""Generate the LLVM Bedrock vector MC catalog from normative ISA YAML."""

from __future__ import annotations

import argparse
from functools import cache
from pathlib import Path
import re

import yaml

from defs_schema import parse_assembly_template


ROOT = Path(__file__).resolve().parents[2]
VECTOR = ROOT / "isa/instructions/definitions/extensions/vector"


def _load(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def _range_values(item: object) -> set[int]:
    if isinstance(item, int):
        return {item}
    text = str(item)
    if ".." in text:
        lo, hi = text.split("..", 1)
        return set(range(int(lo, 0), int(hi, 0) + 1))
    return {int(text, 0)}


def _cpp_string(text: str) -> str:
    return '"' + text.replace("\\", "\\\\").replace('"', '\\"') + '"'


def _operand_kind(operand: dict) -> tuple[str, int, bool]:
    operand_type = operand["type"]
    if operand_type == "condition":
        return "Condition", 0, False
    if operand_type == "Rn":
        return "GPR", 0, False
    if operand_type == "Fn":
        return "FPR", 0, False
    if operand_type == "Vn":
        return "Vector", 0, False
    if operand_type == "Pn":
        return "Predicate", 0, False
    if operand_type == "EA":
        return "EA", 0, operand.get("access") != "write"
    if operand_type == "VEA":
        return "VEA", 0, False
    if operand_type == "imm6":
        return "Immediate", 6, False
    match = re.fullmatch(r"imm(8|16|32|64)(s?)", operand_type)
    if match:
        return (
            "TailSigned" if match.group(2) else "TailUnsigned",
            int(match.group(1)),
            False,
        )
    raise ValueError(f"unsupported vector operand type {operand_type!r}")


def _load_forms_and_sizes() -> tuple[list[dict], dict[str, dict[int, str]]]:
    base_sizes = _load(ROOT / "isa/instructions/definitions/sizes.yaml")
    fpu_sizes = _load(
        ROOT / "isa/instructions/definitions/extensions/fpu/sizes.yaml"
    )
    vector_sizes = _load(VECTOR / "sizes.yaml")
    size_values: dict[str, dict[int, str]] = {}
    size_codes = {
        **base_sizes.get("size_codes", {}),
        **fpu_sizes.get("size_codes", {}),
        **vector_sizes.get("size_codes", {}),
    }
    for source in (base_sizes, fpu_sizes, vector_sizes):
        for name, definition in source.get("size_kinds", {}).items():
            size_values[name] = {
                int(entry["value"]): size_codes[entry["code"]]["suffix"][1:].lower()
                for entry in definition.get("values", [])
            }

    forms: list[dict] = []
    for encoding_path in sorted((VECTOR / "instructions").glob("*/encodings.yaml")):
        operation = _load(encoding_path.with_name("operation.yaml"))
        public = operation.get("public_instruction", {})
        aliases = bool(public.get("width_suffix_aliases", False))
        for form in _load(encoding_path).get("forms", []):
            form = dict(form)
            form["width_suffix_aliases"] = aliases
            forms.append(form)
    return forms, size_values


def _allowed_field_values(form: dict, field: str, width: int) -> set[int]:
    allowed = set(range(1 << width))
    for constraint in form.get("constraints", []):
        if constraint.get("field") != field or "allow" not in constraint:
            continue
        allowed = set()
        for item in constraint["allow"]:
            allowed.update(_range_values(item))
    return allowed


def _load_repeat_eligibility() -> list[tuple[str, bool, bool, bool]]:
    entries: list[tuple[str, bool, bool, bool]] = []
    definition_root = ROOT / "isa/instructions/definitions"
    for path in sorted(definition_root.glob("**/operation.yaml")):
        document = _load(path)
        repeat = document["repeat"]
        mnemonic = str(document["public_instruction"]["mnemonic"])
        has_condition = mnemonic.endswith("cc")
        stem = mnemonic[:-2] if has_condition else mnemonic
        kind = repeat["kind"]
        entries.append(
            (stem.lower(), has_condition, kind != "not_eligible", kind == "rep_and_repcc")
        )
    return entries


def _allowed_size_values(
    form: dict, field: str, size_values: dict[str, dict[int, str]]
) -> dict[int, str]:
    kind = form["fields"][field]["type"].split(".", 1)[1]
    values = dict(size_values[kind])
    for constraint in form.get("constraints", []):
        if constraint.get("field") != field or "allow" not in constraint:
            continue
        allowed: set[int] = set()
        for item in constraint["allow"]:
            allowed.update(_range_values(item))
        values = {value: code for value, code in values.items() if value in allowed}
    return values


@cache
def _condition_names() -> dict[int, str]:
    return {
        int(item["value"]): str(item["name"]).lower()
        for item in _load(ROOT / "isa/instructions/definitions/conditions.yaml").get(
            "conditions", []
        )
    }


def _generate() -> str:
    forms, size_values = _load_forms_and_sizes()

    lines = [
        "//===-- BedrockVectorEncoding.inc - generated vector catalog -*- C++ -*-===//",
        "//",
        "// Generated by spec/isa/tools/gen_llvm_vector_catalog.py from the",
        "// normative scalable-vector instruction YAML. Do not edit by hand.",
        "//",
        "//===----------------------------------------------------------------------===//",
        "",
        "#ifndef LLVM_LIB_TARGET_BEDROCK_MCTARGETDESC_BEDROCKVECTORENCODING_INC",
        "#define LLVM_LIB_TARGET_BEDROCK_MCTARGETDESC_BEDROCKVECTORENCODING_INC",
        "",
        "namespace llvm::BedrockMC {",
        "enum class VectorEncodingClass : uint8_t { Long, ExtraLong, Xxlong };",
        "enum class VectorOperandKind : uint8_t {",
        "  None, Condition, GPR, FPR, Vector, Predicate, EA, VEA, Immediate,",
        "  TailSigned, TailUnsigned",
        "};",
        "struct VectorOperandDesc {",
        "  VectorOperandKind Kind;",
        "  char Field;",
        "  uint8_t Width;",
        "  bool AllowImmediateEA;",
        "};",
        "struct VectorEncodingForm {",
        "  const char *Id;",
        "  const char *Mnemonic;",
        "  const char *Pattern;",
        "  const char *Suffixes;",
        "  VectorEncodingClass EncodingClass;",
        "  char SuffixField;",
        "  uint8_t AllowedSuffixMask;",
        "  uint16_t AllowedConditionMask;",
        "  bool HasCondition;",
        "  bool HasWidthOnlyAliases;",
        "  uint8_t OperandCount;",
        "  VectorOperandDesc Operands[6];",
        "  int8_t DistinctOperandA;",
        "  int8_t DistinctOperandB;",
        "};",
        "inline constexpr VectorEncodingForm VectorEncodingForms[] = {",
    ]

    class_names = {"long": "Long", "extralong": "ExtraLong", "xxlong": "Xxlong"}
    for form in forms:
        template = parse_assembly_template(form["syntax"], form["id"])
        has_condition = template.mnemonic.endswith("cc")
        mnemonic = template.mnemonic[:-2] if has_condition else template.mnemonic
        suffix_field = "\\0"
        suffixes = ""
        allowed_mask = 1
        if template.fixed_size_suffix is not None:
            mnemonic += template.fixed_size_suffix
        elif template.selected_size_codes:
            if template.size_field is None:
                raise ValueError(f"{form['id']}: selected suffix has no field")
            suffix_field = template.size_field
            kind = form["fields"][suffix_field]["type"].split(".", 1)[1]
            values = size_values[kind]
            suffix_chars = ["?"] * (max(values) + 1)
            allowed = {
                value
                for value, suffix in values.items()
                if suffix.upper() in template.selected_size_codes
            }
            for value, suffix in values.items():
                if value in allowed:
                    suffix_chars[value] = suffix
            for constraint in form.get("constraints", []):
                if (
                    constraint.get("field") != suffix_field
                    or "allow" not in constraint
                ):
                    continue
                constrained: set[int] = set()
                for item in constraint["allow"]:
                    constrained.update(_range_values(item))
                allowed &= constrained
            suffixes = "".join(suffix_chars)
            allowed_mask = sum(1 << value for value in allowed)

        operands = []
        explicit_index_by_name = {}
        for operand in form.get("operands", []):
            kind, width, allow_immediate = _operand_kind(operand)
            if kind == "EA" and any(
                constraint.get("field") == operand.get("field")
                and constraint.get("exclude") == "immediate"
                for constraint in form.get("constraints", [])
            ):
                allow_immediate = False
            if kind != "Condition":
                explicit_index_by_name[operand["name"]] = len(
                    [entry for entry in operands if entry[0] != "Condition"]
                )
            operands.append(
                (kind, operand.get("field", "\\0"), width, allow_immediate)
            )
        if len(operands) > 6:
            raise ValueError(f"too many operands in {form['id']}")
        distinct_a = distinct_b = -1
        overlaps = form.get("destination_overlap", [])
        if overlaps:
            names = overlaps[0]["operands"]
            distinct_a = explicit_index_by_name[names[0]]
            distinct_b = explicit_index_by_name[names[1]]

        operand_text = []
        for kind, field, width, allow_immediate in operands:
            field_literal = "'\\0'" if field == "\\0" else f"'{field}'"
            operand_text.append(
                "{VectorOperandKind::%s, %s, %d, %s}"
                % (kind, field_literal, width, str(allow_immediate).lower())
            )
        operand_text.extend(
            ["{VectorOperandKind::None, '\\0', 0, false}"]
            * (6 - len(operand_text))
        )
        suffix_literal = "'\\0'" if suffix_field == "\\0" else f"'{suffix_field}'"
        condition_mask = sum(
            1 << value for value in _allowed_field_values(form, "c", 4)
        ) if has_condition else 0xffff
        lines.append(
            "  {%s, %s, %s, %s, VectorEncodingClass::%s, %s, 0x%02x, 0x%04x, %s, %s, %d,"
            % (
                _cpp_string(form["id"]),
                _cpp_string(mnemonic.lower()),
                _cpp_string(form["bits"]),
                _cpp_string(suffixes),
                class_names[form["class"]],
                suffix_literal,
                allowed_mask,
                condition_mask,
                str(has_condition).lower(),
                str(bool(form["width_suffix_aliases"])).lower(),
                len(operands),
            )
        )
        lines.append("   {%s}, %d, %d}," % (", ".join(operand_text), distinct_a, distinct_b))

    lines.extend(
        [
            "};",
            "struct RepeatEligibility {",
            "  const char *Mnemonic;",
            "  bool HasCondition;",
            "  bool AllowsREP;",
            "  bool AllowsREPcc;",
            "};",
            "inline constexpr RepeatEligibility RepeatEligibilityTable[] = {",
        ]
    )
    for mnemonic, has_condition, allows_rep, allows_repcc in _load_repeat_eligibility():
        lines.append(
            "  {%s, %s, %s, %s},"
            % (
                _cpp_string(mnemonic),
                str(has_condition).lower(),
                str(allows_rep).lower(),
                str(allows_repcc).lower(),
            )
        )
    lines.extend(
        [
            "};",
            "} // namespace llvm::BedrockMC",
            "",
            "#endif",
            "",
        ]
    )
    return "\n".join(lines)


def _concrete_assembly(form: dict, size_values: dict[str, dict[int, str]]) -> str:
    template = parse_assembly_template(form["syntax"], form["id"])
    head = template.mnemonic
    if head.endswith("cc"):
        condition = next(
            operand for operand in form["operands"] if operand["type"] == "condition"
        )
        condition_field = condition["field"]
        condition_width = form["bits"].count(condition_field)
        legal_conditions = _allowed_field_values(
            form, condition_field, condition_width
        )
        names = _condition_names()
        selected_condition = min(legal_conditions & names.keys())
        head = head[:-2] + names[selected_condition]
    scale = 1
    if template.fixed_size_suffix is not None:
        head += template.fixed_size_suffix
    elif template.selected_size_codes:
        if template.size_field is None:
            raise ValueError(f"{form['id']}: selected suffix has no field")
        values = _allowed_size_values(form, template.size_field, size_values)
        selected_values = {
            value: suffix
            for value, suffix in values.items()
            if suffix.upper() in template.selected_size_codes
        }
        if not selected_values:
            raise ValueError(f"{form['id']}: no legal public suffix")
        selected = min(selected_values)
        head += "." + selected_values[selected]
        scale = 1 << selected

    encoded_operands = [
        operand
        for operand in form.get("operands", [])
        if operand["type"] not in {"condition", "memory_order"}
    ]
    operand_index = 0
    register_counters = {"Pn": 0, "Vn": 1, "Rn": 1, "Fn": 1}
    register_values: dict[tuple[str, str], int] = {}

    def consume(node: object) -> dict:
        nonlocal operand_index
        if operand_index >= len(encoded_operands):
            raise ValueError(f"{form['id']}: assembly AST has an extra operand {node}")
        operand = encoded_operands[operand_index]
        operand_index += 1
        field = getattr(node, "field", None)
        if field != operand.get("field"):
            raise ValueError(
                f"{form['id']}: assembly AST field {field!r} does not match "
                f"operand {operand['name']!r} field {operand.get('field')!r}"
            )
        return operand

    def concrete_value(node: object) -> str:
        operand = consume(node)
        operand_type = operand["type"]
        if operand_type in register_counters:
            field = operand.get("field")
            key = (operand_type, field or operand["name"])
            if key not in register_values:
                candidate = register_counters[operand_type]
                if field:
                    width = form["bits"].count(field)
                    allowed = _allowed_field_values(form, field, width)
                    candidate = candidate if candidate in allowed else min(allowed)
                register_values[key] = candidate
                register_counters[operand_type] = candidate + 1
            prefix = {"Pn": "p", "Vn": "v", "Rn": "r", "Fn": "f"}[
                operand_type
            ]
            return prefix + str(register_values[key])
        if operand_type in {"EA", "VEA"}:
            return "[r3]"
        if operand_type.startswith("imm"):
            field = operand.get("field")
            if field:
                width = form["bits"].count(field)
                allowed = _allowed_field_values(form, field, width)
                return str(1 if 1 in allowed else min(allowed))
            return "1"
        raise ValueError(
            f"{form['id']}: unsupported concrete operand type {operand_type!r}"
        )

    def render(node: object) -> str:
        kind = getattr(node, "kind")
        if kind == "reference":
            return concrete_value(node)
        if kind == "decimal":
            consume(node)
            return str(getattr(node, "literal"))
        if kind == "scale":
            return str(scale)
        if kind == "operator":
            return f" {getattr(node, 'name')} "
        if kind in {"address", "lane_index"}:
            return "[" + "".join(render(member) for member in node.members) + "]"
        raise ValueError(f"{form['id']}: unsupported assembly AST node {kind!r}")

    args = ", ".join(render(operand) for operand in template.operands)
    if operand_index != len(encoded_operands):
        raise ValueError(
            f"{form['id']}: assembly AST omitted "
            f"{len(encoded_operands) - operand_index} encoded operands"
        )
    return head.lower() if not args else f"{head.lower()} {args.lower()}"


def _generate_mc_test() -> str:
    forms, size_values = _load_forms_and_sizes()
    assembly = [_concrete_assembly(form, size_values) for form in forms]
    lines = [
        "# NOTE: Generated by spec/isa/tools/gen_llvm_vector_catalog.py.",
        "# RUN: llvm-mc -triple=bedrock -mattr=+vector,+fpu -filetype=obj %s -o %t",
        "# RUN: llvm-objdump -d --no-show-raw-insn %t | FileCheck %s",
        "",
    ]
    for index, (form, instruction) in enumerate(zip(forms, assembly)):
        mnemonic, *operands = instruction.split(None, 1)
        directive = "CHECK" if index == 0 else "CHECK-NEXT"
        expected = mnemonic
        if operands:
            expected += "{{[ \\t]+}}" + operands[0]
        lines.extend((f"# {directive}: {expected}", f"# {form['id']}", instruction))

    # Keep alias coverage tied to the same typed public alias declaration that
    # feeds the catalog.  The selected form has the whole B/W/L/Q domain, so
    # the three established width aliases exercise every compatibility map and
    # prove that disassembly returns the canonical public spelling.
    for form, canonical in zip(forms, assembly):
        template = parse_assembly_template(form["syntax"], form["id"])
        if not (
            form["width_suffix_aliases"]
            and {"B", "W", "L", "Q"}.issubset(template.selected_size_codes)
        ):
            continue
        mnemonic, *operands = canonical.split(None, 1)
        if not mnemonic.endswith(".b"):
            continue
        canonical_suffixes = {"h": "w", "s": "l", "d": "q"}
        for alias, canonical_suffix in canonical_suffixes.items():
            alias_mnemonic = mnemonic[:-1] + alias
            expected_mnemonic = mnemonic[:-1] + canonical_suffix
            expected = expected_mnemonic
            if operands:
                expected += "{{[ \\t]+}}" + operands[0]
            lines.extend(
                (
                    f"# CHECK-NEXT: {expected}",
                    f"# {form['id']} public width alias .{alias}",
                    f"{alias_mnemonic} {operands[0]}" if operands else alias_mnemonic,
                )
            )
        break
    else:
        raise ValueError("no full-domain vector form declares public width aliases")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    parser.add_argument("--test-output", type=Path)
    args = parser.parse_args()
    generated = _generate()
    if args.output:
        args.output.write_text(generated, encoding="utf-8")
    else:
        print(generated, end="")
    if args.test_output:
        args.test_output.write_text(_generate_mc_test(), encoding="utf-8")


if __name__ == "__main__":
    main()
