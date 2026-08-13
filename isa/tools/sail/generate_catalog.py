#!/usr/bin/env python3
"""Generate the experimental Sail decode and execution metadata."""

from __future__ import annotations

import argparse
from collections import Counter
import json
import os
from pathlib import Path
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[3]
EXPECTED_DISTRIBUTION = {
    "extrashort": 25,
    "short": 37,
    "medium": 125,
    "long": 203,
    "extralong": 32,
}
EXPECTED_SET_DISTRIBUTION = {"base": 141, "fpu": 45, "fpu.transcendental_approx": 19}
CLASS_CONSTRUCTORS = {
    "extrashort": "ExtraShort",
    "short": "Short",
    "medium": "Medium",
    "long": "Long",
    "extralong": "ExtraLong",
}
EXCLUDE_CONSTRUCTORS = {
    "rn_direct": "ExcludeRnDirect",
    "reg_direct": "ExcludeRegDirect",
    "immediate": "ExcludeImmediate",
}
ROUTE_CONSTRUCTORS = {
    "atomics": "RouteAtomics",
    "bounds": "RouteBounds",
    "cache": "RouteCache",
    "control_flow": "RouteControlFlow",
    "core_control": "RouteCoreControl",
    "data_movement": "RouteDataMovement",
    "ea_utility": "RouteEaUtility",
    "fpu": "RouteFpu",
    "fpu_transcendental_approx": "RouteFpuTranscendental",
    "integer_alu": "RouteIntegerAlu",
    "integer_bitfield": "RouteIntegerBitfield",
    "integer_mul_div": "RouteIntegerMulDiv",
    "integer_unary": "RouteIntegerUnary",
    "system_registers": "RouteSystemRegisters",
    "tlb_and_context": "RouteTlbContext",
}
FIELD_KIND_CONSTRUCTORS = {
    "rn": "FieldRn",
    "freg": "FieldFreg",
    "ea7": "FieldEa",
    "condition": "FieldCondition",
    "size": "FieldSize",
    "immediate": "FieldImmediate",
    "bits": "FieldBits",
}
ACCESS_CONSTRUCTORS = {
    "read": "AccessRead",
    "write": "AccessWrite",
    "read_write": "AccessReadWrite",
    "address": "AccessAddress",
}


def _is_within(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def validate_build_dir(raw_build_dir: Path) -> Path:
    """Resolve and validate a dedicated repository-build or external-temp path."""
    build_dir = raw_build_dir.expanduser().resolve()
    repository_build = (ROOT / "build").resolve()
    if _is_within(build_dir, repository_build):
        return build_dir

    temp_roots = {
        Path(tempfile.gettempdir()).resolve(),
        Path("/private/tmp").resolve(),
        Path("/tmp").resolve(),
        Path("/var/tmp").resolve(),
    }
    external_temp = not _is_within(build_dir, ROOT) and any(
        build_dir != temp_root and _is_within(build_dir, temp_root)
        for temp_root in temp_roots
    )
    if external_temp:
        return build_dir

    raise ValueError(
        f"refusing generated-catalog build directory outside {repository_build} "
        f"or an external temporary directory: {build_dir}"
    )
PRIVILEGE_CONSTRUCTORS = {
    "unprivileged": "UserPrivilege",
    "supervisor": "SupervisorPrivilege",
    "any": "AnyPrivilege",
}


def _load_inputs():
    sys.path.insert(0, str(ROOT / "isa" / "tools"))
    from defs_loader import load_operand_types, load_yaml
    from defs_schema import decode_ea_registry, decode_instruction
    from encoding_store import load_encoding_store

    previous = Path.cwd()
    try:
        os.chdir(ROOT)
        store = load_encoding_store(Path("isa/defs"))
        operand_types = load_operand_types(Path("isa/defs"))
        ea_path = Path("isa/defs/ea.yaml")
        ea_registry = decode_ea_registry(ea_path, load_yaml(ea_path))
        documents = {}
        for located in store.encodings:
            path = located.path.with_name("instruction.yaml")
            documents[located.mnemonic] = decode_instruction(path, load_yaml(path))
        return store, operand_types, ea_registry, documents
    finally:
        os.chdir(previous)


def _range(value: int | str) -> tuple[int, int]:
    if isinstance(value, int):
        return value, value
    text = value.replace("_", "")
    if ".." in text:
        lower, upper = text.split("..", 1)
        return int(lower, 0), int(upper, 0)
    parsed = int(text, 0)
    return parsed, parsed


def _bits(pattern: str) -> tuple[int, int]:
    value = 0
    mask = 0
    for char in pattern:
        value <<= 1
        mask <<= 1
        if char in "01":
            mask |= 1
            value |= int(char)
    return value, mask


def _set_field(pattern: str, payload: int, symbol: str, field_value: int) -> int:
    positions = _positions(pattern, symbol)
    for bit_index, position in enumerate(reversed(positions)):
        bit = (field_value >> bit_index) & 1
        payload = (payload | (1 << position)) if bit else (payload & ~(1 << position))
    return payload


def _representative_payload(form) -> int:
    value, _ = _bits(form.bits)
    for constraint in form.constraints:
        selected = _range(constraint.allow[0])[0] if constraint.allow else 0x10
        value = _set_field(form.bits, value, constraint.field, selected)
    return value


def _representative_record(located, operand_types) -> list[int]:
    form = located.form
    payload = _representative_payload(form)
    opcode_bytes = {"extrashort": 1, "short": 2, "medium": 3, "long": 4, "extralong": 5}[form.encoding_class]
    appended = sum(item["field_width"] for item in (
        operand_types[operand.type]
        for operand in form.operands
        if operand.field is None and not (operand.type == "imm" and "<" not in form.syntax)
    )) // 8
    total = opcode_bytes + appended
    if form.encoding_class == "extrashort":
        record = [payload]
    elif form.encoding_class == "short":
        full = (0b10 << 14) | payload
        record = [(full >> 8) & 0xFF, full & 0xFF]
    else:
        if total > 18:
            raise ValueError(f"{form.id}: representative requires {total} bytes")
        header = 0b11000000 | ((total - 3) << 2) | ((payload >> ((opcode_bytes - 1) * 8)) & 0x3)
        record = [header]
        record.extend((payload >> shift) & 0xFF for shift in range((opcode_bytes - 2) * 8, -1, -8))
    record.extend([0] * appended)
    return record


def _positions(pattern: str, symbol: str) -> list[int]:
    return [len(pattern) - index - 1 for index, char in enumerate(pattern) if char == symbol]


def _list(items: list[str]) -> str:
    return "[|%s|]" % ", ".join(items)


def _strings(items) -> str:
    return _list([json.dumps(str(item)) for item in items])


def _operation(mnemonic: str) -> str:
    return "Op_" + mnemonic


def _instruction_set(path: Path) -> tuple[str, str]:
    text = path.as_posix()
    if "/extensions/fpu/extensions/transcendental_approx/" in text:
        return "fpu.transcendental_approx", "FpuTranscendentalSet"
    if "/extensions/fpu/" in text:
        return "fpu", "FpuSet"
    return "base", "BaseSet"


def _constraint(pattern: str, constraint) -> str:
    positions = _positions(pattern, constraint.field)
    if constraint.allow:
        kind = "AllowRanges"
        ranges = [
            "struct { lower = %d, upper = %d }" % _range(item)
            for item in constraint.allow
        ]
    else:
        kind = EXCLUDE_CONSTRUCTORS[constraint.exclude]
        ranges = []
    return (
        "struct { field_positions = %s, kind = %s, ranges = %s, reason = %s }"
        % (_list(list(map(str, positions))), kind, _list(ranges), json.dumps(constraint.reason or ""))
    )


def _fields(form, registry) -> list[str]:
    declarations = {}
    for operand in form.operands:
        if operand.field is not None:
            declarations[operand.field] = operand.type
    for symbol, field in form.fields.items():
        declarations[symbol] = field.type
    out = []
    for symbol in sorted(declarations):
        type_name = declarations[symbol]
        spec = registry.types[type_name]
        out.append(
            "struct { symbol = %s, type_name = %s, kind = %s, positions = %s }"
            % (
                json.dumps(symbol),
                json.dumps(type_name),
                FIELD_KIND_CONSTRUCTORS[spec.allocation_kind],
                _list(list(map(str, _positions(form.bits, symbol)))),
            )
        )
    return out


def _operand_legal_values(raw) -> list[int]:
    return [int(item["value"], 0) if isinstance(item["value"], str) else int(item["value"])
            for item in raw.get("values", [])]


def _predicate_mode(mnemonic: str, form) -> str:
    if mnemonic == "SETcc":
        return "WriteBoolean"
    if mnemonic in {"CMPJcc", "TESTJcc"}:
        return "Temporary"
    if mnemonic in {"DJcc", "IJcc", "REPcc"}:
        return "CounterAndCondition"
    if any(operand.type == "condition" for operand in form.operands):
        return "AnnulOnFalse"
    return "PredicateNone"


def _operands(form, operand_types) -> list[str]:
    from defs_schema import parse_assembly_template

    template = parse_assembly_template(form.syntax, form.id)
    decimal_literals = [item.literal for item in template.operands if item.kind == "decimal"]
    out = []
    for operand in form.operands:
        raw = operand_types[operand.type]
        fixed_value = 0
        has_fixed_value = False
        if operand.field is None and operand.type == "imm" and decimal_literals:
            fixed_value = int(decimal_literals.pop(0))
            has_fixed_value = True
        positions = _positions(form.bits, operand.field) if operand.field else []
        out.append(
            "struct { name = %s, type_name = %s, access = %s, field_symbol = %s, "
            "field_positions = %s, domain = %s, ea_role = %s, ea_width = %s, "
            "has_fixed_value = %s, fixed_value = %d, fixed_identity = %s, legal_values = %s }"
            % (
                json.dumps(operand.name),
                json.dumps(operand.type),
                ACCESS_CONSTRUCTORS[operand.access],
                json.dumps(operand.field or ""),
                _list(list(map(str, positions))),
                json.dumps(operand.domain or ""),
                json.dumps(operand.ea_role or ""),
                json.dumps(operand.ea_width or ""),
                str(has_fixed_value).lower(),
                fixed_value,
                json.dumps(raw.get("register", "")),
                _list([str(value) for value in _operand_legal_values(raw)]),
            )
        )
    return out


def _payloads(form, operand_types) -> list[str]:
    out = []
    for operand in form.operands:
        if operand.field is not None:
            continue
        raw = operand_types[operand.type]
        width = int(raw["field_width"])
        if width == 0 or (operand.type == "imm" and "<" not in form.syntax):
            continue
        out.append(
            "struct { operand_name = %s, type_name = %s, width = %d, signed = %s }"
            % (
                json.dumps(operand.name),
                json.dumps(operand.type),
                width,
                str(bool(raw.get("signed", False))).lower(),
            )
        )
    return out


def _exceptions(document) -> list[str]:
    return [
        "struct { event = %s, when_text = %s, forms = %s }"
        % (json.dumps(item.event), json.dumps(item.when), _strings(item.forms))
        for item in document.exceptions
    ]


def _overlaps(form) -> list[str]:
    return [
        "struct { left = %s, right = %s, rule = %s }"
        % (json.dumps(item.operands[0]), json.dumps(item.operands[1]), json.dumps(item.rule))
        for item in form.destination_overlap
    ]


def _ea_form(form, ext0: bool, payloads) -> str:
    joined = "".join(form.pattern)
    patterns = []
    offset = len(joined)
    for pattern in form.pattern:
        offset -= len(pattern)
        value, mask = _bits(pattern)
        patterns.append(
            "struct { width = %d, value = 0x%04X, mask = 0x%04X }"
            % (len(pattern), value, mask)
        )
    fields = []
    for symbol, field in sorted(form.fields.items()):
        fields.append(
            "struct { symbol = %s, type_name = %s, role = %s, positions = %s }"
            % (
                json.dumps(symbol),
                json.dumps(field.type),
                json.dumps(field.role),
                _list(list(map(str, _positions(joined, symbol)))),
            )
        )
    payload = payloads.get(form.payload) if form.payload else None
    return (
        "  struct { name = %s, ext0 = %s, patterns = %s, kind = %s, fields = %s, "
        "segment = %s, payload = %s, payload_width = %d, payload_signed = %s, base = %s, "
        "register_name = %s, descriptor = %s, update_target = %s, update_mode = %s }"
        % (
            json.dumps(form.name),
            str(ext0).lower(),
            _list(patterns),
            json.dumps(form.kind or "memory" if ext0 else form.kind or ""),
            _list(fields),
            json.dumps(form.segment or ""),
            json.dumps(form.payload or ""),
            payload.field_width if payload else 0,
            str(payload.signed if payload else False).lower(),
            json.dumps(form.base or ""),
            json.dumps(form.register or ""),
            json.dumps(form.descriptor or ""),
            json.dumps(form.update.target if form.update else ""),
            json.dumps(form.update.mode if form.update else ""),
        )
    )


def render_operations(documents) -> str:
    docs = sorted(documents.values(), key=lambda item: item.mnemonic)
    lines = ["// Generated by generate_catalog.py. Do not edit.", "", "enum Semantic_operation ="]
    lines.extend(("  " if index == 0 else "| ") + _operation(doc.mnemonic) for index, doc in enumerate(docs))
    lines.extend(["", "function semantic_route(operation : Semantic_operation) -> Semantic_route = match operation {"])
    lines.extend(
        "  %s => %s," % (_operation(doc.mnemonic), ROUTE_CONSTRUCTORS[doc.attributes.family])
        for doc in docs
    )
    lines.extend(["}", "", "function semantic_mnemonic(operation : Semantic_operation) -> string = match operation {"])
    lines.extend("  %s => %s," % (_operation(doc.mnemonic), json.dumps(doc.mnemonic)) for doc in docs)
    lines.extend(["}", "", "function all_semantic_operations() -> list(Semantic_operation) = [|"])
    lines.append("  " + ", ".join(_operation(doc.mnemonic) for doc in docs))
    lines.extend(["|]", ""])
    return "\n".join(lines)


def render_catalog(store, operand_types, ea_registry, documents) -> str:
    lines = [
        "// Generated by generate_catalog.py from schema-decoded isa/defs owners.",
        "// Do not edit.",
        "",
        "function primary_form_catalog() -> list(Catalog_entry) = [|",
    ]
    entries = []
    for located in sorted(store.encodings, key=lambda item: item.form.id):
        form = located.form
        document = documents[located.mnemonic]
        set_name, set_constructor = _instruction_set(located.path)
        value, mask = _bits(form.bits)
        contexts = set(document.repeat.contexts if document.repeat else ())
        observed_kind = document.repeat.observed.kind if document.repeat and document.repeat.observed else ""
        observed_operand = document.repeat.observed.operand or "" if document.repeat and document.repeat.observed else ""
        flag_effects = [
            f"{bank}.{flag}={effect}"
            for bank, effects in document.flag_effects.items()
            for flag, effect in effects.items()
        ]
        entries.append(
            "  struct { form_id = %s, mnemonic = %s, operation = %s, route = %s, "
            "instruction_set = %s, instruction_class = %s, family = %s, privilege = %s, "
            "predicate_mode = %s, "
            "has_ea_operand = %s, "
            "repeat_rep = %s, repeat_repcc = %s, repeat_repg = %s, "
            "repeat_observed_kind = %s, repeat_observed_operand = %s, flag_effects = %s, "
            "exceptions = %s, encoding_class = %s, payload_width = %d, value = 0x%016X, "
            "mask = 0x%016X, constraints = %s, fields = %s, operands = %s, sizes = %s, "
            "appended_payloads = %s, overlaps = %s }"
            % (
                json.dumps(form.id), json.dumps(located.mnemonic), _operation(located.mnemonic),
                ROUTE_CONSTRUCTORS[document.attributes.family], set_constructor,
                json.dumps(document.attributes.instruction_class), json.dumps(document.attributes.family),
                PRIVILEGE_CONSTRUCTORS[document.attributes.privilege],
                _predicate_mode(located.mnemonic, form),
                str(any(operand.type == "EA" for operand in form.operands)).lower(),
                str("REP" in contexts).lower(), str("REPcc" in contexts).lower(), str("REPG" in contexts).lower(),
                json.dumps(observed_kind), json.dumps(observed_operand),
                _strings(flag_effects), _list(_exceptions(document)), CLASS_CONSTRUCTORS[form.encoding_class],
                len(form.bits), value, mask, _list([_constraint(form.bits, item) for item in form.constraints]),
                _list(_fields(form, store.field_types)), _list(_operands(form, operand_types)), _strings(form.sizes),
                _list(_payloads(form, operand_types)), _list(_overlaps(form)),
            )
        )
    lines.append(",\n".join(entries))
    lines.extend(["|]", "", "function effective_address_catalog() -> list(Ea_form) = [|"])
    ea_forms = [_ea_form(form, False, ea_registry.payloads) for form in ea_registry.compact_forms]
    ea_forms.extend(_ea_form(form, True, ea_registry.payloads) for form in ea_registry.ext0_forms)
    lines.append(",\n".join(ea_forms))
    lines.extend(["|]", "", "function representative_form_records() -> list(Representative_record) = [|"])
    records = []
    for located in sorted(store.encodings, key=lambda item: item.form.id):
        bytes_text = ", ".join(f"0x{byte:02X}" for byte in _representative_record(located, operand_types))
        records.append(
            "  struct { form_id = %s, mnemonic = %s, bytes = [|%s|] }"
            % (json.dumps(located.form.id), json.dumps(located.mnemonic), bytes_text)
        )
    lines.append(",\n".join(records))
    lines.extend(["|]", ""])
    return "\n".join(lines)


def render_overlay_project() -> str:
    return """operations {
  requires prelude
  files generated/operations.sail
}

catalog {
  requires prelude, operations, catalog_types
  files generated/catalog.sail
}
"""


def render_outputs(build_dir: Path) -> dict[Path, str]:
    store, operand_types, ea_registry, documents = _load_inputs()
    distribution = Counter(item.form.encoding_class for item in store.encodings)
    set_distribution = Counter(_instruction_set(item.path)[0] for item in {x.mnemonic: x for x in store.encodings}.values())
    if len(store.encodings) != 422 or dict(distribution) != EXPECTED_DISTRIBUTION:
        raise ValueError(f"unexpected form inventory: {len(store.encodings)} {dict(distribution)}")
    if len(documents) != 205 or dict(set_distribution) != EXPECTED_SET_DISTRIBUTION:
        raise ValueError(f"unexpected mnemonic inventory: {len(documents)} {dict(set_distribution)}")
    unknown_routes = {doc.attributes.family for doc in documents.values()} - ROUTE_CONSTRUCTORS.keys()
    if unknown_routes:
        raise ValueError(f"unrouted instruction families: {sorted(unknown_routes)}")
    return {
        build_dir / "generated" / "operations.sail": render_operations(documents),
        build_dir / "generated" / "catalog.sail": render_catalog(
            store, operand_types, ea_registry, documents
        ),
        build_dir / "bedrock-generated.sail_project": render_overlay_project(),
    }


def write_outputs(build_dir: Path) -> None:
    for path, text in render_outputs(build_dir).items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")


def check_outputs(build_dir: Path) -> bool:
    return all(
        path.exists() and path.read_text(encoding="utf-8") == expected
        for path, expected in render_outputs(build_dir).items()
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "build_dir",
        metavar="BUILD_DIR",
        type=Path,
        help="dedicated directory beneath repository build/ or an external temporary directory",
    )
    parser.add_argument("--check", action="store_true", help="fail if build output is stale")
    args = parser.parse_args()
    try:
        build_dir = validate_build_dir(args.build_dir)
    except ValueError as error:
        print(f"catalog generation failed: {error}", file=sys.stderr)
        return 1
    outputs = render_outputs(build_dir)
    if args.check:
        stale = [
            path
            for path, expected in outputs.items()
            if not path.exists() or path.read_text(encoding="utf-8") != expected
        ]
        for path in stale:
            print(f"stale generated output: {path}", file=sys.stderr)
        return int(bool(stale))
    write_outputs(build_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
