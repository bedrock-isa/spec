#!/usr/bin/env python3
"""Generate the experimental Sail decode and execution metadata."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[3]
ISA_TOOLS = ROOT / "isa" / "tools"
sys.path.insert(0, str(ISA_TOOLS))

import decode_ir
from defs_schema import EXECUTION_ROUTE_CONSTRUCTORS as ROUTE_CONSTRUCTORS
from encoding_architecture import ENCODING_CLASSES_BY_NAME


CLASS_CONSTRUCTORS = {
    "extrashort": "ExtraShort",
    "short": "Short",
    "medium": "Medium",
    "long": "Long",
    "extralong": "ExtraLong",
    "xxlong": "Xxlong",
}
EXCLUDE_CONSTRUCTORS = {
    "immediate": "ExcludeImmediate",
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
INSTRUCTION_SET_CONSTRUCTORS = {
    "base": "BaseSet",
    "fpu": "FpuSet",
    "fpu.transcendental_approx": "FpuTranscendentalSet",
    "vector": "VectorSet",
}
PREDICATE_CONSTRUCTORS = {
    "none": "PredicateNone",
    "write_boolean": "WriteBoolean",
    "temporary": "Temporary",
    "counter_and_condition": "CounterAndCondition",
    "annul_on_false": "AnnulOnFalse",
    "operation_cases": "PredicateNone",  # staging topology probe; final projection uses cases
}


def _load_inputs():
    inputs = decode_ir.load_decode_inputs(ROOT / "isa" / "instructions" / "definitions")
    return inputs.store, inputs.operand_types, inputs.ea_registry, inputs.operations


def _representative_record(located, operand_types) -> list[int]:
    form = located.form
    record = decode_ir.build_representative_record(
        form,
        operand_types,
        ENCODING_CLASSES_BY_NAME[form.encoding_class].opcode_space_bytes,
    )
    if record is None:
        raise ValueError(f"{form.id}: representative exceeds the encodable record length")
    return list(record)


def _list(items: list[str]) -> str:
    return "[|%s|]" % ", ".join(items)


def _strings(items) -> str:
    return _list([json.dumps(str(item)) for item in items])


def _operation(mnemonic: str) -> str:
    return "Op_" + mnemonic


def _instruction_set(path: Path) -> tuple[str, str]:
    name = decode_ir.instruction_set_name(
        ROOT / "isa" / "instructions" / "definitions", path
    )
    return name, INSTRUCTION_SET_CONSTRUCTORS[name]


def _constraint(constraint: decode_ir.ConstraintIR) -> str:
    kind = (
        "AllowRanges"
        if constraint.kind == "allow_ranges"
        else EXCLUDE_CONSTRUCTORS[constraint.kind.removeprefix("exclude_")]
    )
    ranges = [
        "struct { lower = %d, upper = %d }" % (item.lower, item.upper)
        for item in constraint.ranges
    ]
    return (
        "struct { field_positions = %s, kind = %s, ranges = %s, reason = %s }"
        % (
            _list(list(map(str, constraint.positions))),
            kind,
            _list(ranges),
            json.dumps(constraint.reason),
        )
    )


def _fields(items: tuple[decode_ir.FieldIR, ...]) -> list[str]:
    return [
        "struct { symbol = %s, type_name = %s, kind = %s, positions = %s }"
        % (
            json.dumps(item.symbol),
            json.dumps(item.type_name),
            FIELD_KIND_CONSTRUCTORS[item.kind],
            _list(list(map(str, item.positions))),
        )
        for item in items
    ]


def _operands(items: tuple[decode_ir.OperandIR, ...]) -> list[str]:
    out = []
    for item in items:
        source = item.source
        field_symbol = ""
        positions: tuple[int, ...] = ()
        has_fixed_value = False
        fixed_value = 0
        fixed_identity = ""
        if isinstance(
            source,
            (decode_ir.EncodedFieldSourceIR, decode_ir.EffectiveAddressSourceIR),
        ):
            field_symbol = source.field_symbol
            positions = source.positions
        elif isinstance(source, decode_ir.FixedSourceIR):
            has_fixed_value = source.value is not None
            fixed_value = source.value or 0
            fixed_identity = source.identity
        out.append(
            "struct { name = %s, type_name = %s, access = %s, field_symbol = %s, "
            "field_positions = %s, domain = %s, ea_role = %s, ea_width = %s, "
            "ea_profile = %s, has_fixed_value = %s, fixed_value = %d, "
            "fixed_identity = %s, legal_values = %s }"
            % (
                json.dumps(item.name),
                json.dumps(item.type_name),
                ACCESS_CONSTRUCTORS[item.access],
                json.dumps(field_symbol),
                _list(list(map(str, positions))),
                json.dumps(item.domain),
                json.dumps(item.ea_role),
                json.dumps(item.ea_width),
                json.dumps(
                    source.profile
                    if isinstance(source, decode_ir.EffectiveAddressSourceIR)
                    else ""
                ),
                str(has_fixed_value).lower(),
                fixed_value,
                json.dumps(fixed_identity),
                _list([str(value) for value in item.legal_values]),
            )
        )
    return out


def _payloads(form: decode_ir.FormIR) -> list[str]:
    operand_types = {operand.name: operand.type_name for operand in form.operands}
    return [
        "struct { operand_name = %s, type_name = %s, width = %d, signed = %s }"
        % (
            json.dumps(item.operand_name),
            json.dumps(operand_types[item.operand_name]),
            item.width,
            str(item.signed).lower(),
        )
        for item in form.layout
        if isinstance(item, decode_ir.ReadPayloadIR)
    ]


def _exceptions(annotations: decode_ir.AnnotationsIR) -> list[str]:
    return [
        "struct { event = %s, when_text = %s, forms = %s }"
        % (
            json.dumps(item.event),
            json.dumps(item.condition_text),
            _strings(item.forms),
        )
        for item in annotations.exception_conditions
    ]


def _overlaps(items: tuple[decode_ir.DestinationOverlapIR, ...]) -> list[str]:
    return [
        "struct { left = %s, right = %s, rule = %s }"
        % (json.dumps(item.left), json.dumps(item.right), json.dumps(item.rule))
        for item in items
    ]


def _ea_form(form: decode_ir.EaFormIR, profile: str = "") -> str:
    patterns = [
        "struct { width = %d, value = 0x%04X, mask = 0x%04X }"
        % (item.width, item.value, item.mask)
        for item in form.patterns
    ]
    rendered_fields = [
        "struct { symbol = %s, type_name = %s, role = %s, positions = %s }"
        % (
            json.dumps(item.symbol),
            json.dumps(item.type_name),
            json.dumps(item.role),
            _list(list(map(str, item.positions))),
        )
        for item in form.fields
    ]
    return (
        "  struct { name = %s, profile = %s, descriptor_family = %s, descriptor_bytes = %d, "
        "patterns = %s, kind = %s, fields = %s, "
        "segment = %s, payload = %s, payload_width = %d, payload_signed = %s, base = %s, "
        "register_name = %s, descriptor = %s, update_target = %s, update_mode = %s }"
        % (
            json.dumps(form.name),
            json.dumps(profile),
            json.dumps(form.member_of_descriptor_family),
            form.descriptor_bytes,
            _list(patterns),
            json.dumps(form.kind),
            _list(rendered_fields),
            json.dumps(form.segment),
            json.dumps(form.payload_name),
            form.payload_width,
            str(form.payload_signed).lower(),
            json.dumps(form.base),
            json.dumps(form.register_name),
            json.dumps(form.referenced_descriptor_family),
            json.dumps(form.update_target),
            json.dumps(form.update_mode),
        )
    )


def render_operations(operations, cpuid_flags=None) -> str:
    """Render the early, metadata-only operation registry from bundle owners."""
    if cpuid_flags is None:
        cpuid_flags = decode_ir.load_decode_ir().cpuid_flags
    docs = sorted(operations.values(), key=lambda item: item.id)
    lines = ["// Generated by generate_catalog.py. Do not edit.", "", "enum Cpuid_flag ="]
    lines.extend(
        ("  " if index == 0 else "| ") + "CpuidFlag_" + flag.id
        for index, flag in enumerate(cpuid_flags)
    )
    lines.extend(
        [
            "",
            "function cpuid_flag_token(flag : Cpuid_flag) -> string = match flag {",
            *[
                "  CpuidFlag_%s => %s," % (flag.id, json.dumps(flag.token))
                for flag in cpuid_flags
            ],
            "}",
            "",
            "function cpuid_flag_selector_class(flag : Cpuid_flag) -> int = match flag {",
            *[
                "  CpuidFlag_%s => %d," % (flag.id, flag.selector_class)
                for flag in cpuid_flags
            ],
            "}",
            "",
            "function cpuid_flag_leaf(flag : Cpuid_flag) -> int = match flag {",
            *[
                "  CpuidFlag_%s => %d," % (flag.id, flag.leaf)
                for flag in cpuid_flags
            ],
            "}",
            "",
            "function cpuid_flag_index(flag : Cpuid_flag) -> int = match flag {",
            *[
                "  CpuidFlag_%s => %d," % (flag.id, flag.index)
                for flag in cpuid_flags
            ],
            "}",
            "",
            "function cpuid_flag_bit(flag : Cpuid_flag) -> int = match flag {",
            *[
                "  CpuidFlag_%s => %d," % (flag.id, flag.bit)
                for flag in cpuid_flags
            ],
            "}",
            "",
            "enum Semantic_operation =",
        ]
    )
    lines.extend(("  " if index == 0 else "| ") + _operation(doc.id) for index, doc in enumerate(docs))
    lines.extend(["", "function semantic_route(operation : Semantic_operation) -> Semantic_route = match operation {"])
    lines.extend(
        "  %s => %s," % (_operation(doc.id), ROUTE_CONSTRUCTORS[doc.execution_route])
        for doc in docs
    )
    lines.extend(["}", "", "function semantic_mnemonic(operation : Semantic_operation) -> string = match operation {"])
    lines.extend("  %s => %s," % (_operation(doc.id), json.dumps(doc.public_instruction.mnemonic)) for doc in docs)
    lines.extend(["}", "", "function all_semantic_operations() -> list(Semantic_operation) = [|"])
    lines.append("  " + ", ".join(_operation(doc.id) for doc in docs))
    lines.extend(["|]", ""])
    return "\n".join(lines)


def render_operation_entries(operations) -> str:
    """Aggregate operation-local Sail entries and their exhaustive dispatcher."""
    docs = sorted(operations.values(), key=lambda item: item.id)
    lines = ["// Generated by generate_catalog.py from operation bundle semantics. Do not edit.", ""]
    seen_entries: set[str] = set()
    dispatch: list[tuple[str, str]] = []
    for operation in docs:
        if operation.artifacts is None:
            raise ValueError(f"{operation.id}: missing operation artifacts")
        entries = tuple(dict.fromkeys(case.sail_entry for case in operation.cases if case.sail_entry))
        if not entries:
            raise ValueError(f"{operation.id}: missing operation-local Sail entry")
        source = Path(operation.artifacts.bundle_root) / operation.artifacts.semantics.path
        for entry in entries:
            if entry not in seen_entries:
                lines.extend([source.read_text(encoding="utf-8").strip(), ""])
                seen_entries.update(entries)
                break
        dispatch.append((operation.id, entries))
    lines.extend([
        "function execute_operation_entry(instruction : Decoded_instruction, state : Cpu_state)",
        "  -> Execution_result = match instruction.form.operation {",
    ])
    for operation, entries in dispatch:
        fallback = "faulted(state, instruction.form.operation, IllegalInstruction, \"local operation entry rejected its owning form\")"
        for entry in reversed(entries):
            fallback = "match %s(instruction, state) { Some(result) => result, None() => %s }" % (entry, fallback)
        lines.append("  %s => %s," % (_operation(operation), fallback))
    lines.extend(["}", ""])
    return "\n".join(lines)


def _render_catalog_ir(ir: decode_ir.DecodeIR) -> str:
    lines = [
        (
            "// Generated by generate_catalog.py from schema-decoded "
            "isa/instructions/definitions owners."
        ),
        "// Do not edit.",
        "",
        "function primary_form_catalog() -> list(Catalog_entry) = [|",
    ]
    entries = []
    for form in ir.forms:
        control = form.control
        repeat = control.repeat
        flag_effects = [
            f"{item.bank}.{item.flag}={item.effect_text}"
            for item in form.annotations.flag_effects
        ]
        availability_rules = [
            "struct { case_id = %s, selectors = %s, operand_profiles = %s, required_flags = %s }"
            % (
                json.dumps(rule.case_id),
                _list(
                    [
                        "struct { field_symbol = %s, values = %s }"
                        % (
                            json.dumps(selector.field_symbol),
                            _list(list(map(str, selector.encoded_values))),
                        )
                        for selector in rule.selectors
                    ]
                ),
                _list(
                    [
                        "struct { operand_name = %s, type_names = %s }"
                        % (
                            json.dumps(profile.operand_name),
                            _strings(profile.type_names),
                        )
                        for profile in rule.operand_profiles
                    ]
                ),
                _list(
                    ["CpuidFlag_" + flag for flag in rule.required_cpuid_flags]
                ),
            )
            for rule in form.availability_rules
        ]
        common_required = set(form.availability_rules[0].required_cpuid_flags)
        for rule in form.availability_rules[1:]:
            common_required &= set(rule.required_cpuid_flags)
        entries.append(
            "  struct { form_id = %s, mnemonic = %s, operation = %s, route = %s, "
            "instruction_set = %s, instruction_class = %s, family = %s, privilege = %s, "
            "predicate_mode = %s, "
            "has_ea_operand = %s, "
            "repeat_rep = %s, repeat_repcc = %s, "
            "repeat_observed_kind = %s, repeat_observed_operand = %s, flag_effects = %s, "
            "exceptions = %s, encoding_class = %s, allocation_bits = %d, value = 0x%016X, "
            "mask = 0x%016X, constraints = %s, fields = %s, operands = %s, sizes = %s, "
            "appended_payloads = %s, overlaps = %s, availability_rules = %s, "
            "common_required_cpuid_flags = %s }"
            % (
                json.dumps(form.key), json.dumps(form.mnemonic), _operation(form.mnemonic),
                ROUTE_CONSTRUCTORS[control.route],
                INSTRUCTION_SET_CONSTRUCTORS[control.instruction_set],
                json.dumps(control.instruction_class), json.dumps(control.family),
                PRIVILEGE_CONSTRUCTORS[control.privilege],
                PREDICATE_CONSTRUCTORS[control.predicate_mode],
                str(control.has_ea_operand).lower(),
                str(repeat.rep).lower(), str(repeat.repcc).lower(),
                json.dumps(repeat.observed_kind), json.dumps(repeat.observed_operand),
                _strings(flag_effects), _list(_exceptions(form.annotations)),
                CLASS_CONSTRUCTORS[form.opcode_class],
                form.opcode_width, form.opcode_value, form.opcode_mask,
                _list([_constraint(item) for item in form.constraints]),
                _list(_fields(form.fields)), _list(_operands(form.operands)), _strings(form.sizes),
                _list(_payloads(form)), _list(_overlaps(form.overlaps)),
                _list(availability_rules),
                _list(
                    [
                        "CpuidFlag_" + flag
                        for flag in (item.id for item in ir.cpuid_flags)
                        if flag in common_required
                    ]
                ),
            )
        )
    lines.append(",\n".join(entries))
    lines.extend(["|]", "", "function effective_address_catalog() -> list(Ea_form) = [|"])
    ea = ir.effective_addresses
    ea_forms = [
        _ea_form(form, profile.name)
        for profile in ea.profiles
        for form in profile.compact_forms
    ]
    ea_forms.extend(
        _ea_form(form)
        for family in ea.descriptor_families
        for form in family.forms
    )
    lines.append(",\n".join(ea_forms))
    lines.extend(["|]", "", "function representative_form_records() -> list(Representative_record) = [|"])
    records = []
    for form in ir.forms:
        if form.representative_record is None:
            raise ValueError(f"{form.key}: representative exceeds the encodable record length")
        bytes_text = ", ".join(f"0x{byte:02X}" for byte in form.representative_record)
        records.append(
            "  struct { form_id = %s, mnemonic = %s, bytes = [|%s|] }"
            % (json.dumps(form.key), json.dumps(form.mnemonic), bytes_text)
        )
    lines.append(",\n".join(records))
    lines.extend(["|]", ""])
    return "\n".join(lines)


def render_catalog(store, operand_types, ea_registry, operations) -> str:
    """Compatibility adapter that renders only from the canonical Decode IR."""
    return _render_catalog_ir(
        decode_ir.build_decode_ir(store, operand_types, ea_registry, operations)
    )


def render_overlay_project() -> str:
    return """operations {
  requires prelude
  files generated/operations.sail
}

catalog {
  requires prelude, operations, catalog_types
  files generated/catalog.sail
}

operation_entries {
  requires prelude, operations, catalog_types, catalog, decode, fp, core
  files generated/local_operations.sail
}
"""


def render_outputs(build_dir: Path) -> dict[Path, str]:
    inputs = decode_ir.load_decode_inputs(
        ROOT / "isa" / "instructions" / "definitions"
    )
    store, operand_types, ea_registry, operations = (
        inputs.store,
        inputs.operand_types,
        inputs.ea_registry,
        inputs.operations,
    )
    ir = decode_ir.build_decode_ir(
        store,
        operand_types,
        ea_registry,
        operations,
        inputs.cpuid_flags,
        inputs.size_definitions,
    )
    unknown_routes = {form.control.route for form in ir.forms} - ROUTE_CONSTRUCTORS.keys()
    if unknown_routes:
        raise ValueError(f"unrouted instruction families: {sorted(unknown_routes)}")
    return {
        build_dir / "generated" / "operations.sail": render_operations(
            operations, ir.cpuid_flags
        ),
        build_dir / "generated" / "local_operations.sail": render_operation_entries(operations),
        build_dir / "generated" / "catalog.sail": _render_catalog_ir(ir),
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
