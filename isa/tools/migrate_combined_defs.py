#!/usr/bin/env python3
"""One-shot, lossless migration from split logical/allocation definitions.

The command is intentionally conservative: ``audit`` never writes, and ``apply``
refuses to write until every old logical form is represented by at least one
encoding or explicitly listed in ``REMOVED_FORM_DISPOSITIONS``.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
import re
import subprocess
from typing import Any

import yaml

from validate_alloc import (
    entry_claims,
    field_widths,
    namespace_patterns,
    parse_range,
)
from defs_schema import decode_encodings, decode_instruction
from encoding_architecture import ENCODING_CLASSES_BY_NAME
from encoding_store import allocation_entry_dict, load_encoding_store


ROOT = Path(__file__).resolve().parents[2]
DEFS_ROOT = ROOT / "isa" / "defs"
ALLOC_ROOT = ROOT / "isa" / "alloc"
LEDGER_PATH = ROOT / "build" / "migration" / "definition-migration-ledger.json"

KIND_TO_TYPE = {
    "size": "size",
    "rn": "Rn",
    "freg": "Fn",
    "ea7": "EA",
    "condition": "condition",
}

# Allocation forms whose operand shape is not present literally in the old
# logical forms. The chosen index supplies only names/access/domain; the actual
# type and size still come from allocation syntax.
FORM_OVERRIDES = {
    "medium.call_ea": 0,
    "medium.call_ea.2": 1,
    "medium.add_q_ea_sp": 1,
    "medium.add_q_ea_sp.2": 1,
    "extrashort.add_q_8_sp": 1,
    "short.add_q_imm8_i_sp": 1,
    "medium.sub_q_ea_sp": 1,
    "medium.sub_q_ea_sp.2": 1,
    "extrashort.sub_q_8_sp": 1,
    "short.sub_q_imm8_i_sp": 1,
    "medium.adc_x_rn_s_rn_d": 0,
    "medium.sbb_x_rn_s_rn_d": 0,
}

# These old logical forms had no concrete allocation and were explicitly
# removed instead of being carried into the integrated definition model.
REMOVED_FORM_DISPOSITIONS: dict[tuple[str, int], str] = {
    ("FCLR", 1): "removed by architecture decision",
    ("ADC", 2): "removed by architecture decision",
    ("ADD", 4): "removed by architecture decision",
    ("AND", 4): "removed by architecture decision",
    ("CALL", 2): "removed by architecture decision",
    ("CMP", 4): "removed by architecture decision",
    ("OR", 4): "removed by architecture decision",
    ("SBB", 2): "removed by architecture decision",
    ("SUB", 4): "removed by architecture decision",
    ("TEST", 4): "removed by architecture decision",
    ("XOR", 4): "removed by architecture decision",
}


@dataclass(frozen=True)
class OldInstruction:
    path: Path
    data: dict[str, Any]

    @property
    def mnemonic(self) -> str:
        return str(self.data["mnemonic"])

    @property
    def forms(self) -> list[dict[str, Any]]:
        return list(self.data.get("forms") or [])


@dataclass(frozen=True)
class OldAllocation:
    path: Path
    cls: str
    payload_bits: int
    namespaces: list[str]
    entry: dict[str, Any]


def load_yaml(path: Path) -> Any:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def instruction_files() -> list[Path]:
    return sorted(DEFS_ROOT.glob("**/instructions/*/instruction.yaml"))


def load_instructions() -> dict[str, OldInstruction]:
    result: dict[str, OldInstruction] = {}
    for path in instruction_files():
        data = load_yaml(path)
        if not isinstance(data, dict) or not data.get("mnemonic"):
            raise ValueError(f"{path}: invalid instruction definition")
        mnemonic = str(data["mnemonic"])
        if mnemonic in result:
            raise ValueError(f"duplicate mnemonic {mnemonic}")
        result[mnemonic] = OldInstruction(path, data)
    return result


def load_allocations() -> tuple[list[dict[str, Any]], list[OldAllocation]]:
    classes: list[dict[str, Any]] = []
    entries: list[OldAllocation] = []
    for path in sorted(
        ALLOC_ROOT.glob("*.yaml"),
        key=lambda item: list(ENCODING_CLASSES_BY_NAME).index(item.stem),
    ):
        data = load_yaml(path)
        if not isinstance(data, dict):
            raise ValueError(f"{path}: expected mapping")
        cls = str(data["class"])
        payload_bits = int(data["payload_bits"])
        namespaces = namespace_patterns(payload_bits, data)
        encoding_class = ENCODING_CLASSES_BY_NAME[cls]
        if payload_bits != encoding_class.payload_bits:
            raise ValueError(
                f"{path}: {cls} payload width {payload_bits} does not match architecture "
                f"width {encoding_class.payload_bits}"
            )
        classes.append(
            {
                "name": cls,
                "instruction_bytes": encoding_class.instruction_bytes,
                "payload_bits": payload_bits,
                "namespace": namespaces,
            }
        )
        for entry in data.get("entries") or []:
            entries.append(OldAllocation(path, cls, payload_bits, namespaces, entry))
    return classes, entries


def allocation_mnemonic(syntax: str) -> str:
    return re.split(r"[./(]", syntax.split()[0])[0]


def split_syntax_operands(syntax: str) -> list[str]:
    if " " not in syntax:
        return []
    return [part.strip() for part in syntax.split(" ", 1)[1].split(",")]


def token_type(token: str) -> str | None:
    token = token.strip()
    if token == "(instruction)":
        return None
    if re.search(r"\bRn(?:\(|$)", token):
        return "Rn"
    if re.search(r"\bFn(?:\(|$)", token):
        return "Fn"
    if "<ea>" in token:
        return "EA"
    if re.search(r"\bSREG(?:\(|$)", token):
        return "SREG"
    if token in {"CS", "SP", "PC"}:
        return token
    for name in ("fp_pair_id", "pair_id", "flags_bitmap", "pt_level"):
        if token.startswith(name + "("):
            return name
    match = re.match(r"<?(imm(?:16s|32s|8s|64|32|16|8|7|6)?)>?", token)
    if match and match.group(0):
        return "imm" if match.group(1) in {"imm", "imm8"} else match.group(1)
    if re.fullmatch(r"(?:0x[0-9a-fA-F]+|\d+)", token):
        return "imm"
    raise ValueError(f"cannot infer operand type from {token!r}")


def token_field(token: str) -> str | None:
    match = re.search(r"\(([A-Za-z])\)\s*$", token)
    return match.group(1) if match else None


def parsed_syntax(syntax: str) -> tuple[str, list[tuple[str, str | None]], list[str]]:
    mnemonic = allocation_mnemonic(syntax)
    head = syntax.split()[0]
    operands: list[tuple[str, str | None]] = []
    if "cc" in mnemonic:
        operands.append(("condition", "c"))
    order = re.search(r"/order\(([A-Za-z])\)", head)
    if order:
        operands.append(("memory_order", order.group(1)))
    for token in split_syntax_operands(syntax):
        typ = token_type(token)
        if typ is not None:
            operands.append((typ, token_field(token)))

    size_match = re.search(r"\(z:([A-Z/]+)\)", syntax)
    if size_match:
        sizes = size_match.group(1).split("/")
    else:
        suffix = re.match(r"[^.]+\.([BWLQSD])(?:\s|$)", syntax)
        sizes = [suffix.group(1)] if suffix else []
    return mnemonic, operands, sizes


def type_score(actual: str, logical: str) -> int:
    if actual == logical:
        return 5
    if (actual == "imm" and logical.startswith("imm")) or (
        logical == "imm" and actual.startswith("imm")
    ):
        return 3
    if {actual, logical} <= {"Rn", "SP"}:
        return 2
    if {actual, logical} <= {"SREG", "CS"}:
        return 2
    if actual == "EA" and logical == "imm":
        return 1
    if actual == "pair_id" and logical == "fp_pair_id":
        return 1
    if actual.startswith("imm") and logical == "fconst_id":
        return 1
    return -100


def logical_types(form: dict[str, Any]) -> list[str]:
    return [str(item["type"]) for item in form.get("operands") or []]


def choose_logical_form(
    instruction: OldInstruction,
    entry_id: str,
    actual_types: list[str],
    actual_sizes: list[str],
) -> int:
    if entry_id in FORM_OVERRIDES:
        return FORM_OVERRIDES[entry_id]
    candidates: list[tuple[int, int]] = []
    for index, form in enumerate(instruction.forms):
        expected = logical_types(form)
        if len(expected) != len(actual_types):
            continue
        scores = [type_score(a, b) for a, b in zip(actual_types, expected)]
        if scores and min(scores) < 0:
            continue
        logical_sizes = [str(item) for item in form.get("sizes") or []]
        if actual_sizes and logical_sizes and not set(actual_sizes) <= set(logical_sizes):
            continue
        candidates.append((sum(scores), index))
    if not candidates:
        raise ValueError(
            f"{entry_id}: no logical form for {actual_types} sizes={actual_sizes}"
        )
    best_score = max(score for score, _index in candidates)
    best = [index for score, index in candidates if score == best_score]
    if len(best) != 1:
        raise ValueError(f"{entry_id}: ambiguous logical forms {best}")
    return best[0]


def effective_actual_type(actual: str, logical: str) -> str:
    if logical in {"fconst_id", "fp_pair_id"}:
        return logical
    return actual


def infer_missing_operand_field(
    typ: str,
    declared_fields: dict[str, Any],
    used_fields: set[str],
) -> str | None:
    expected_kind = {
        "Rn": "rn",
        "Fn": "freg",
        "EA": "ea7",
        "condition": "condition",
        "SREG": "bits",
        "memory_order": "bits",
        "flags_bitmap": "immediate",
        "pt_level": "immediate",
        "pair_id": "immediate",
        "fp_pair_id": "immediate",
        "imm6": "immediate",
        "imm7": "immediate",
        "imm": "immediate",
        "imm8s": "immediate",
    }.get(typ)
    if expected_kind is None:
        return None
    choices = [
        name
        for name, spec in declared_fields.items()
        if name not in used_fields and str(spec.get("kind")) == expected_kind
    ]
    return choices[0] if len(choices) == 1 else None


def explicit_destination_field(entry: dict[str, Any]) -> str:
    fields = entry.get("fields") or {}
    choices = [
        name
        for name, spec in fields.items()
        if str(spec.get("kind")) == "ea7" and int(spec.get("width", 0)) == 7
    ]
    # Preserve the legacy constraint evaluator exactly during migration. It
    # selected a seven-bit ``d`` field first and then ``e``; ``s`` is a source.
    for preferred in ("d", "e"):
        if preferred in choices:
            return preferred
    if len(choices) == 1:
        return choices[0]
    raise ValueError(f"{entry['id']}: destination constraint has EA fields {choices}")


def migrated_constraints(entry: dict[str, Any]) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    for raw in entry.get("constraints") or []:
        constraint = dict(raw)
        if constraint.pop("destination", False):
            constraint["field"] = explicit_destination_field(entry)
            # Keep stable human ordering after replacing destination=true.
            constraint = {
                "field": constraint.pop("field"),
                **constraint,
            }
        result.append(constraint)
    return result


def migrate_entry(
    allocation: OldAllocation,
    instruction: OldInstruction,
) -> tuple[dict[str, Any], int]:
    entry = allocation.entry
    syntax = str(entry.get("text", ""))
    mnemonic, parsed_operands, parsed_sizes = parsed_syntax(syntax)
    if mnemonic != instruction.mnemonic:
        raise ValueError(f"{entry['id']}: parsed mnemonic {mnemonic} != {instruction.mnemonic}")
    logical_index = choose_logical_form(
        instruction,
        str(entry["id"]),
        [typ for typ, _field in parsed_operands],
        parsed_sizes,
    )
    logical = instruction.forms[logical_index]
    logical_operands = list(logical.get("operands") or [])
    if len(logical_operands) != len(parsed_operands):
        raise ValueError(f"{entry['id']}: operand count changed during mapping")

    declared_fields = dict(entry.get("fields") or {})
    used_fields: set[str] = set()
    operands: list[dict[str, Any]] = []
    for (actual_type, field), old_operand in zip(parsed_operands, logical_operands):
        logical_type = str(old_operand["type"])
        typ = effective_actual_type(actual_type, logical_type)
        if field is None:
            field = infer_missing_operand_field(typ, declared_fields, used_fields)
        operand = {
            "name": str(old_operand["name"]),
            "type": typ,
            "access": str(old_operand["access"]),
        }
        if field is not None:
            operand["field"] = field
            used_fields.add(field)
        if "domain" in old_operand:
            operand["domain"] = str(old_operand["domain"])
        operands.append(operand)

    remaining_fields: dict[str, dict[str, Any]] = {}
    actual_widths = field_widths(str(entry["bits"]))
    for name, spec in declared_fields.items():
        old_width = int(spec["width"])
        if actual_widths[name] != old_width:
            raise ValueError(
                f"{entry['id']}: field {name} width changed {old_width}->{actual_widths[name]}"
            )
        if name in used_fields:
            continue
        kind = str(spec["kind"])
        typ = KIND_TO_TYPE.get(kind)
        if typ is None:
            raise ValueError(f"{entry['id']}: unowned field {name} kind={kind}")
        remaining_fields[name] = {"type": typ}
    undeclared_markers = set(actual_widths) - used_fields - set(remaining_fields)
    # One legacy FCLR entry used the conventional ``z`` size selector without
    # repeating its declaration in the allocation field map. Make that latent
    # selector explicit; any other undeclared marker remains a hard failure.
    if undeclared_markers == {"z"}:
        remaining_fields["z"] = {"type": "size"}
    elif undeclared_markers:
        raise ValueError(
            f"{entry['id']}: undeclared bit markers {sorted(undeclared_markers)}"
        )

    sizes = parsed_sizes or [str(item) for item in logical.get("sizes") or []]
    result: dict[str, Any] = {
        "id": str(entry["id"]),
        "class": allocation.cls,
        "bits": str(entry["bits"]),
        "syntax": syntax,
    }
    if operands:
        result["operands"] = operands
    if sizes:
        result["sizes"] = sizes
    if remaining_fields:
        result["fields"] = remaining_fields
    constraints = migrated_constraints(entry)
    if constraints:
        result["constraints"] = constraints
    if entry.get("notes"):
        result["notes"] = list(entry["notes"])
    return result, logical_index


def yaml_leaf_items(value: Any, prefix: str = "") -> list[tuple[str, Any]]:
    if isinstance(value, dict):
        out: list[tuple[str, Any]] = []
        for key, child in value.items():
            child_prefix = f"{prefix}.{key}" if prefix else str(key)
            out.extend(yaml_leaf_items(child, child_prefix))
        return out
    if isinstance(value, list):
        out = []
        for index, child in enumerate(value):
            out.extend(yaml_leaf_items(child, f"{prefix}[{index}]"))
        return out
    return [(prefix, value)]


def value_from_leaf_items(items: list[list[Any]]) -> dict[str, Any]:
    """Reconstruct a mapping from the ledger's complete scalar leaf paths."""
    root: dict[str, Any] = {}
    for leaf_path, value in items:
        tokens: list[str | int] = []
        for name, index in re.findall(r"([^.\[\]]+)|\[(\d+)\]", leaf_path):
            tokens.append(int(index) if index else name)
        current: Any = root
        for position, token in enumerate(tokens):
            final = position == len(tokens) - 1
            next_is_index = not final and isinstance(tokens[position + 1], int)
            if isinstance(token, str):
                if final:
                    current[token] = value
                    continue
                if token not in current:
                    current[token] = [] if next_is_index else {}
                current = current[token]
            else:
                while len(current) <= token:
                    current.append(None)
                if final:
                    current[token] = value
                    continue
                if current[token] is None:
                    current[token] = [] if next_is_index else {}
                current = current[token]
    return root


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def old_claim_digest(allocations: list[OldAllocation]) -> str:
    digest = hashlib.sha256()
    for item in allocations:
        claims, skipped = entry_claims(
            item.path,
            item.payload_bits,
            item.namespaces,
            item.entry,
        )
        digest.update(item.cls.encode())
        digest.update(str(item.entry["id"]).encode())
        for value, claim in claims:
            digest.update(f"{value}:{claim.entry_id}\n".encode())
        for reason, count in sorted(skipped.items()):
            digest.update(f"skip:{reason}:{count}\n".encode())
    return digest.hexdigest()


def claim_fingerprint(
    path: Path,
    payload_bits: int,
    namespaces: list[str],
    entry: dict[str, Any],
) -> dict[str, Any]:
    claims, skipped = entry_claims(path, payload_bits, namespaces, entry)
    digest = hashlib.sha256()
    for value, claim in claims:
        digest.update(f"{value}:{claim.entry_id}\n".encode())
    for reason, count in sorted(skipped.items()):
        digest.update(f"skip:{reason}:{count}\n".encode())
    return {
        "claims": len(claims),
        "skipped": dict(sorted(skipped.items())),
        "sha256": digest.hexdigest(),
    }


def old_claim_fingerprints(
    allocations: list[OldAllocation],
) -> dict[str, dict[str, Any]]:
    return {
        str(item.entry["id"]): {
            "class": item.cls,
            **claim_fingerprint(
                item.path,
                item.payload_bits,
                item.namespaces,
                item.entry,
            ),
        }
        for item in allocations
    }


def tex_escape(value: str) -> str:
    replacements = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
    return "".join(replacements.get(char, char) for char in value)


def flag_tex(data: dict[str, Any]) -> str:
    lines: list[str] = []
    flags = data.get("flags")
    if isinstance(flags, dict) and flags:
        lines.append(r"\begin{manualflageffects}{FLAGS}")
        for name, effect in flags.items():
            lines.append(
                rf"\manualflageffect{{{tex_escape(str(name))}}}{{{tex_escape(str(effect))}}}"
            )
        lines.append(r"\end{manualflageffects}")
    fp_flags = data.get("may_accrue_fp_flags")
    if isinstance(fp_flags, list) and fp_flags:
        lines.append(r"\begin{manualflageffects}{FFLAGS}")
        for name in fp_flags:
            lines.append(rf"\manualflageffect{{{tex_escape(str(name))}}}{{may accrue}}")
        lines.append(r"\end{manualflageffects}")
    return "\n".join(lines)


def migrated_instruction(data: dict[str, Any], has_details: bool) -> dict[str, Any]:
    doc = data["doc"]
    old_attributes = data["attributes"]
    attributes: dict[str, Any] = {
        "class": str(doc["instruction_class"]),
        "family": str(doc["instruction_family"]),
        "privilege": str(old_attributes["privilege"]),
    }
    if old_attributes.get("repeat"):
        attributes["repeat"] = list(old_attributes["repeat"])
    result: dict[str, Any] = {
        "mnemonic": str(data["mnemonic"]),
        "title": str(doc["title"]),
        "summary": str(doc["summary"]),
        "description": str(doc["description"]),
        "attributes": attributes,
    }
    if str(data["mnemonic"]) == "REPcc":
        result["additional_assembler_syntax"] = ["REP Rn(r), (instruction)"]
    elif str(data["mnemonic"]) == "REPG":
        result["additional_assembler_syntax"] = [
            "REPGF Rn(r), { (instructions...) }"
        ]
    if has_details:
        result["additional_description"] = "details.tex"
    return result


def dump_yaml(data: Any) -> str:
    return yaml.safe_dump(
        data,
        sort_keys=False,
        allow_unicode=True,
        width=1000,
    )


def build_migration() -> tuple[
    dict[str, OldInstruction],
    list[dict[str, Any]],
    list[OldAllocation],
    dict[str, list[dict[str, Any]]],
    dict[str, set[int]],
    dict[tuple[str, int], list[str]],
]:
    instructions = load_instructions()
    classes, allocations = load_allocations()
    forms_by_mnemonic: dict[str, list[dict[str, Any]]] = defaultdict(list)
    covered: dict[str, set[int]] = defaultdict(set)
    mapped_ids: dict[tuple[str, int], list[str]] = defaultdict(list)
    for allocation in allocations:
        mnemonic = allocation_mnemonic(str(allocation.entry.get("text", "")))
        instruction = instructions.get(mnemonic)
        if instruction is None:
            raise ValueError(f"{allocation.entry['id']}: no instruction {mnemonic}")
        migrated, logical_index = migrate_entry(allocation, instruction)
        forms_by_mnemonic[mnemonic].append(migrated)
        covered[mnemonic].add(logical_index)
        mapped_ids[(mnemonic, logical_index)].append(str(migrated["id"]))
    return instructions, classes, allocations, forms_by_mnemonic, covered, mapped_ids


def constraint_accepts_ea_subset(
    form: dict[str, Any], field: str | None, logical_type: str
) -> bool:
    if field is None:
        return False
    forbidden = {"rn_direct", "reg_direct"} if logical_type == "Rn" else {"immediate"}
    required = set(range(0x00, 0x10)) if logical_type == "Rn" else set(range(0x6C, 0x70))
    for constraint in form.get("constraints") or []:
        if constraint.get("field") != field:
            continue
        if constraint.get("exclude") in forbidden:
            return False
        if "allow" in constraint:
            allowed: set[int] = set()
            for item in constraint.get("allow") or []:
                lo, hi = parse_range(item)
                allowed.update(range(lo, hi + 1))
            if not required <= allowed:
                return False
    return True


def form_subsumes_logical(
    encoding: dict[str, Any], logical: dict[str, Any]
) -> bool:
    actual_operands = list(encoding.get("operands") or [])
    logical_operands = list(logical.get("operands") or [])
    if len(actual_operands) != len(logical_operands):
        return False
    for actual, old in zip(actual_operands, logical_operands):
        if actual.get("access") != old.get("access"):
            return False
        if actual.get("domain") != old.get("domain"):
            return False
        actual_type = str(actual.get("type"))
        logical_type = str(old.get("type"))
        if actual_type == logical_type:
            continue
        if actual_type != "EA" or logical_type not in {"Rn", "imm", "imm64"}:
            return False
        if not constraint_accepts_ea_subset(
            encoding, actual.get("field"), logical_type
        ):
            return False
    return True


def automatic_subsumption(
    logical: dict[str, Any], encodings: list[dict[str, Any]]
) -> list[str]:
    logical_sizes = set(str(item) for item in logical.get("sizes") or [])
    compatible = [form for form in encodings if form_subsumes_logical(form, logical)]
    if not compatible:
        return []
    if logical_sizes:
        covered_sizes = {
            str(size) for form in compatible for size in form.get("sizes") or []
        }
        if not logical_sizes <= covered_sizes:
            return []
    return [str(form["id"]) for form in compatible]


def uncovered_forms(
    instructions: dict[str, OldInstruction],
    covered: dict[str, set[int]],
    forms_by_mnemonic: dict[str, list[dict[str, Any]]],
) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for mnemonic, instruction in instructions.items():
        for index, form in enumerate(instruction.forms):
            if index in covered[mnemonic]:
                continue
            subsuming = automatic_subsumption(
                form, forms_by_mnemonic.get(mnemonic, [])
            )
            reason = (
                "subsumed by " + ", ".join(subsuming)
                if subsuming
                else REMOVED_FORM_DISPOSITIONS.get((mnemonic, index))
            )
            out.append(
                {
                    "mnemonic": mnemonic,
                    "index": index,
                    "form": form,
                    "disposition": reason,
                }
            )
    return out


def migration_coverage(
    instructions: dict[str, OldInstruction],
    allocations: list[OldAllocation],
    forms_by_mnemonic: dict[str, list[dict[str, Any]]],
    mapped_ids: dict[tuple[str, int], list[str]],
) -> dict[str, dict[str, Any]]:
    """Give every old YAML leaf an explicit owner or transformation proof."""
    coverage: dict[str, dict[str, Any]] = {}
    direct_instruction_paths = {
        "mnemonic": "mnemonic",
        "doc.title": "title",
        "doc.summary": "summary",
        "doc.description": "description",
        "doc.instruction_class": "attributes.class",
        "doc.instruction_family": "attributes.family",
        "attributes.privilege": "attributes.privilege",
    }
    for mnemonic, instruction in instructions.items():
        source = str(instruction.path.relative_to(ROOT))
        new_path = source
        for leaf_path, value in yaml_leaf_items(instruction.data):
            key = f"{source}#{leaf_path}"
            if leaf_path in direct_instruction_paths:
                coverage[key] = {
                    "owner": f"{new_path}#{direct_instruction_paths[leaf_path]}",
                    "proof": "equal",
                }
                continue
            repeat = re.fullmatch(r"attributes\.repeat\[(\d+)\]", leaf_path)
            if repeat:
                coverage[key] = {
                    "owner": f"{new_path}#attributes.repeat[{repeat.group(1)}]",
                    "proof": "equal",
                }
                continue
            form = re.match(r"forms\[(\d+)\](?:\.(.*))?$", leaf_path)
            if form:
                index = int(form.group(1))
                owners = list(mapped_ids.get((mnemonic, index), []))
                if not owners:
                    owners = automatic_subsumption(
                        instruction.forms[index], forms_by_mnemonic.get(mnemonic, [])
                    )
                disposition = REMOVED_FORM_DISPOSITIONS.get((mnemonic, index))
                coverage[key] = {
                    "owner": [f"encoding:{owner}" for owner in owners]
                    or f"architecture-decision:removed-logical-form[{mnemonic}:{index}]",
                    "proof": "projected" if owners else disposition,
                }
                continue
            if leaf_path.startswith("flags.") or leaf_path.startswith("may_accrue_fp_flags["):
                coverage[key] = {
                    "owner": f"{instruction.path.with_name('details.tex').relative_to(ROOT)}",
                    "proof": "verbatim TeX table cell",
                }
                continue
            raise ValueError(f"{source}: no migration rule for leaf {leaf_path}={value!r}")

    for allocation in allocations:
        source = f"{allocation.path.relative_to(ROOT)}#{allocation.entry['id']}"
        form_id = str(allocation.entry["id"])
        mnemonic = allocation_mnemonic(str(allocation.entry.get("text", "")))
        target = next(
            form
            for form in forms_by_mnemonic[mnemonic]
            if str(form["id"]) == form_id
        )
        target_path = instructions[mnemonic].path.with_name("encodings.yaml").relative_to(ROOT)
        for leaf_path, value in yaml_leaf_items(allocation.entry):
            key = f"{source}#{leaf_path}"
            proof = "equal"
            target_leaf = leaf_path
            if leaf_path == "text":
                target_leaf = "syntax"
            elif re.fullmatch(r"fields\.[^.]+\.width", leaf_path):
                target_leaf = "bits"
                proof = "derived marker width"
            elif re.fullmatch(r"fields\.[^.]+\.kind", leaf_path):
                target_leaf = "operands/fields type"
                proof = "kind-to-type translation with equal width"
            elif re.fullmatch(r"constraints\[\d+\]\.destination", leaf_path):
                target_leaf = "constraints.field"
                proof = "legacy destination-field resolution"
            coverage[key] = {
                "owner": f"{target_path}#forms[id={form_id}].{target_leaf}",
                "proof": proof,
            }
    return coverage


def write_ledger(
    instructions: dict[str, OldInstruction],
    classes: list[dict[str, Any]],
    allocations: list[OldAllocation],
    forms_by_mnemonic: dict[str, list[dict[str, Any]]],
    covered: dict[str, set[int]],
    mapped_ids: dict[tuple[str, int], list[str]],
) -> dict[str, Any]:
    tex_files = sorted(DEFS_ROOT.glob("**/*.tex"))
    ledger = {
        "instruction_count": len(instructions),
        "logical_form_count": sum(len(item.forms) for item in instructions.values()),
        "logical_operand_count": sum(
            len(form.get("operands") or [])
            for item in instructions.values()
            for form in item.forms
        ),
        "encoding_count": len(allocations),
        "encoding_class_count": len(classes),
        "old_claim_digest": old_claim_digest(allocations),
        "old_claim_fingerprints": old_claim_fingerprints(allocations),
        "instruction_leaves": {
            str(item.path.relative_to(ROOT)): yaml_leaf_items(item.data)
            for item in instructions.values()
        },
        "allocation_leaves": {
            f"{item.path.relative_to(ROOT)}#{item.entry['id']}": yaml_leaf_items(item.entry)
            for item in allocations
        },
        "tex_sha256": {
            str(path.relative_to(ROOT)): sha256_text(path.read_text(encoding="utf-8"))
            for path in tex_files
        },
        "new_encoding_counts": {
            mnemonic: len(forms) for mnemonic, forms in forms_by_mnemonic.items()
        },
        "uncovered_logical_forms": uncovered_forms(
            instructions, covered, forms_by_mnemonic
        ),
        "leaf_coverage": migration_coverage(
            instructions, allocations, forms_by_mnemonic, mapped_ids
        ),
    }
    expected_leaf_count = sum(
        len(yaml_leaf_items(item.data)) for item in instructions.values()
    ) + sum(len(yaml_leaf_items(item.entry)) for item in allocations)
    if len(ledger["leaf_coverage"]) != expected_leaf_count:
        raise ValueError(
            f"ledger covers {len(ledger['leaf_coverage'])}/{expected_leaf_count} YAML leaves"
        )
    LEDGER_PATH.parent.mkdir(parents=True, exist_ok=True)
    LEDGER_PATH.write_text(json.dumps(ledger, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return ledger


def apply_migration(
    instructions: dict[str, OldInstruction],
    forms_by_mnemonic: dict[str, list[dict[str, Any]]],
    ledger: dict[str, Any],
) -> None:
    old_tex_bodies = {
        mnemonic: instruction.path.with_name("details.tex").read_text(encoding="utf-8")
        for mnemonic, instruction in instructions.items()
        if instruction.path.with_name("details.tex").is_file()
    }
    for mnemonic, instruction in instructions.items():
        details_path = instruction.path.with_name("details.tex")
        old_details = details_path.read_text(encoding="utf-8") if details_path.exists() else ""
        flags = flag_tex(instruction.data)
        has_details = bool(old_details or flags)
        if flags:
            body = flags + ("\n\n" + old_details if old_details else "\n")
            details_path.write_text(body, encoding="utf-8")
        instruction.path.write_text(
            dump_yaml(migrated_instruction(instruction.data, has_details)),
            encoding="utf-8",
        )
        instruction.path.with_name("encodings.yaml").write_text(
            dump_yaml({"forms": forms_by_mnemonic[mnemonic]}),
            encoding="utf-8",
        )
    verify_migration(instructions, ledger, old_tex_bodies)
    for path in sorted(ALLOC_ROOT.glob("*.yaml")):
        path.unlink()


def verify_migration(
    instructions: dict[str, OldInstruction],
    ledger: dict[str, Any],
    old_tex_bodies: dict[str, str],
) -> None:
    form_count = 0
    for mnemonic, old in instructions.items():
        instruction = decode_instruction(old.path, load_yaml(old.path))
        if instruction.mnemonic != mnemonic:
            raise ValueError(f"{old.path}: mnemonic changed during migration")
        encodings_path = old.path.with_name("encodings.yaml")
        encodings = decode_encodings(encodings_path, load_yaml(encodings_path))
        form_count += len(encodings.forms)
        old_tex = old_tex_bodies.get(mnemonic)
        if old_tex is not None:
            new_tex = old.path.with_name("details.tex").read_text(encoding="utf-8")
            if old_tex not in new_tex:
                raise ValueError(f"{old.path}: existing details.tex body was not preserved")
        flags_tex = flag_tex(old.data)
        if flags_tex:
            new_tex = old.path.with_name("details.tex").read_text(encoding="utf-8")
            if flags_tex not in new_tex:
                raise ValueError(f"{old.path}: flag table text was not preserved")

    if len(instructions) != int(ledger["instruction_count"]):
        raise ValueError("instruction count changed during migration")
    if form_count != int(ledger["encoding_count"]):
        raise ValueError(
            f"encoding count changed during migration: {form_count} != {ledger['encoding_count']}"
        )
    if any(not item.get("proof") for item in ledger["leaf_coverage"].values()):
        raise ValueError("migration ledger has leaves without an ownership proof")

    store = load_encoding_store(DEFS_ROOT)
    new_fingerprints: dict[str, dict[str, Any]] = {}
    classes_by_name = store.classes_by_name
    for located in store.encodings:
        encoding_class = classes_by_name[located.form.encoding_class]
        raw = allocation_entry_dict(located)
        new_fingerprints[located.form.id] = {
            "class": encoding_class.name,
            **claim_fingerprint(
                located.path,
                encoding_class.payload_bits,
                list(encoding_class.namespace),
                raw,
            ),
        }
    if new_fingerprints != ledger["old_claim_fingerprints"]:
        changed = sorted(
            set(new_fingerprints) ^ set(ledger["old_claim_fingerprints"])
            | {
                form_id
                for form_id in new_fingerprints.keys() & ledger["old_claim_fingerprints"].keys()
                if new_fingerprints[form_id] != ledger["old_claim_fingerprints"][form_id]
            }
        )
        raise ValueError(f"opcode claims changed during migration: {changed[:20]}")


def restore_old_sources_from_ledger() -> None:
    if not LEDGER_PATH.is_file():
        raise ValueError(f"missing migration ledger: {LEDGER_PATH}")
    ledger = json.loads(LEDGER_PATH.read_text(encoding="utf-8"))
    tex_hashes = ledger.get("tex_sha256") or {}
    for relative, leaves in (ledger.get("instruction_leaves") or {}).items():
        path = ROOT / relative
        try:
            original_yaml = subprocess.run(
                ["git", "show", f"HEAD:{relative}"],
                cwd=ROOT,
                check=True,
                stdout=subprocess.PIPE,
            ).stdout.decode("utf-8")
        except (subprocess.CalledProcessError, UnicodeDecodeError) as exc:
            raise ValueError(f"cannot read original source for {relative} from Git") from exc
        old_data = yaml.safe_load(original_yaml)
        if yaml_leaf_items(old_data) != [(str(key), value) for key, value in leaves]:
            raise ValueError(f"{relative}: Git source differs from migration ledger")
        details_path = path.with_name("details.tex")
        details_relative = str(details_path.relative_to(ROOT))
        expected_hash = tex_hashes.get(details_relative)
        if expected_hash is not None:
            original_tex = subprocess.run(
                ["git", "show", f"HEAD:{details_relative}"],
                cwd=ROOT,
                check=True,
                stdout=subprocess.PIPE,
            ).stdout.decode("utf-8")
            actual = sha256_text(original_tex)
            if actual != expected_hash:
                raise ValueError(f"{details_path}: failed to restore original TeX body")
            details_path.write_text(original_tex, encoding="utf-8")
        elif details_path.exists():
            # A flag-only details file was created by the failed migration.
            details_path.unlink()
        path.write_text(original_yaml, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("audit", "apply", "restore-old"))
    args = parser.parse_args()

    if args.command == "restore-old":
        restore_old_sources_from_ledger()
        print("restored old instruction sources from migration ledger")
        return 0

    (
        instructions,
        classes,
        allocations,
        forms_by_mnemonic,
        covered,
        mapped_ids,
    ) = build_migration()
    ledger = write_ledger(
        instructions,
        classes,
        allocations,
        forms_by_mnemonic,
        covered,
        mapped_ids,
    )
    uncovered = ledger["uncovered_logical_forms"]
    undecided = [item for item in uncovered if not item["disposition"]]
    print(f"instructions:     {ledger['instruction_count']}")
    print(f"logical forms:    {ledger['logical_form_count']}")
    print(f"logical operands: {ledger['logical_operand_count']}")
    print(f"encodings:        {ledger['encoding_count']}")
    print(f"uncovered forms:  {len(uncovered)} ({len(undecided)} undecided)")
    print(f"ledger:           {LEDGER_PATH.relative_to(ROOT)}")
    for item in undecided:
        print(
            f"  {item['mnemonic']}[{item['index']}]: "
            f"{item['form'].get('operands', [])} sizes={item['form'].get('sizes', [])}"
        )
    if args.command == "apply":
        if undecided:
            raise SystemExit("refusing migration: uncovered logical forms need dispositions")
        apply_migration(instructions, forms_by_mnemonic, ledger)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
