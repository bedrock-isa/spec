#!/usr/bin/env python3
"""Generate the LLVM Bedrock vector MC catalog from normative ISA YAML."""

from __future__ import annotations

import argparse
from pathlib import Path
import re

import yaml


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


def _has_width_only_aliases(mnemonic: str, suffixes: str) -> bool:
    base_mnemonic = mnemonic.split(".", 1)[0]
    fixed_width = mnemonic.removeprefix(base_mnemonic) in {".L", ".Q"}
    if not fixed_width and (
        not suffixes or not all(code in "bwlq?" for code in suffixes)
    ):
        return False
    return (
        base_mnemonic.startswith("P")
        or base_mnemonic in {
            "VLCNT", "VLCADD", "VGATHER1", "VSCATTER1",
            "PLOOP", "VMOV", "VMOVZ",
        }
        or any(
            word in base_mnemonic
            for word in ("PERM", "SLIDE", "SLICE", "ZIP", "TRN")
        )
    )


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
        forms.extend(_load(encoding_path).get("forms", []))
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
    for path in sorted(definition_root.glob("**/instruction.yaml")):
        document = _load(path)
        repeat = document.get("repeat")
        if not repeat:
            continue
        mnemonic = str(document["mnemonic"])
        has_condition = mnemonic.endswith("cc")
        stem = mnemonic[:-2] if has_condition else mnemonic
        contexts = set(repeat.get("contexts", []))
        entries.append(
            (stem.lower(), has_condition, "REP" in contexts, "REPcc" in contexts)
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
        mnemonic_template = form["syntax"].split(None, 1)[0]
        head, dot, suffix_template = mnemonic_template.partition(".")
        has_condition = head.endswith("cc")
        mnemonic = head[:-2] if has_condition else head
        suffix_field = "\\0"
        suffixes = ""
        allowed_mask = 1
        if dot:
            match = re.fullmatch(r"([A-Z0-9_]+)\(([a-z])\)", suffix_template)
            if not match:
                if not re.fullmatch(r"[A-Z]+", suffix_template):
                    raise ValueError(
                        f"unsupported vector suffix template {suffix_template!r}"
                    )
                mnemonic += "." + suffix_template
            else:
                kind, suffix_field = match.groups()
                values = size_values[kind]
                suffix_chars = ["?"] * (max(values) + 1)
                for value, suffix in values.items():
                    suffix_chars[value] = suffix
                suffixes = "".join(suffix_chars)
                allowed = set(values)
                for constraint in form.get("constraints", []):
                    if (
                        constraint.get("field") != suffix_field
                        or "allow" not in constraint
                    ):
                        continue
                    allowed = set()
                    for item in constraint["allow"]:
                        allowed.update(_range_values(item))
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
                str(_has_width_only_aliases(mnemonic, suffixes)).lower(),
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
    syntax = form["syntax"]
    head, *rest = syntax.split(None, 1)
    if "cc" in head:
        head = head.replace("cc", "eq")
    suffix_match = re.search(r"\.([A-Z0-9_]+)\(([a-z])\)$", head)
    scale = 1
    if suffix_match:
        field = suffix_match.group(2)
        values = _allowed_size_values(form, field, size_values)
        selected = min(values)
        head = head[: suffix_match.start()] + "." + values[selected]
        scale = 1 << selected

    if not rest:
        return head.lower()
    field_numbers = {
        "p": 0, "q": 1, "h": 2,
        "v": 1, "w": 2, "y": 3, "x": 1,
        "r": 1, "s": 4, "u": 3, "b": 3, "i": 2,
    }
    def render_operand(match: re.Match[str]) -> str:
        kind, field = match.groups()
        if kind == "imm6":
            return "1"
        prefix = {"Pn": "p", "Vn": "v", "Rn": "r", "Fn": "f"}[kind]
        return prefix + str(field_numbers[field])

    args = re.sub(
        r"(Pn|Vn|Rn|Fn|imm6)\(([a-z])\)",
        render_operand,
        rest[0],
    )
    args = re.sub(r"<ea>\(e\)", "[r3]", args)
    args = re.sub(r"<(?:imm|disp)(?:8|16|32|64)s?>", "1", args)
    args = args.replace("<scale>", str(scale))
    return f"{head.lower()} {args.lower()}"


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
