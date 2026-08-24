#!/usr/bin/env python3
"""Build the Sail documentation bundle and its semantic authority index."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import subprocess
import sys


sys.dont_write_bytecode = True

TOOLS_ROOT = Path(__file__).resolve().parent
ROOT = TOOLS_ROOT.parents[2]
SAIL_SOURCE_ROOT = ROOT / "isa"
SAIL_PROJECT = SAIL_SOURCE_ROOT / "bedrock.sail_project"
OWNER_SOURCE_PATHS = {
    "operation_entries": (),
    "core": (
        SAIL_SOURCE_ROOT / "execution" / "core" / "types.sail",
        SAIL_SOURCE_ROOT / "execution" / "core" / "state.sail",
        SAIL_SOURCE_ROOT / "execution" / "core" / "predicates.sail",
        SAIL_SOURCE_ROOT / "addressing" / "effective_address" / "evaluation" / "effective_address.sail",
        SAIL_SOURCE_ROOT / "execution" / "core" / "integer_bits.sail",
        SAIL_SOURCE_ROOT / "instructions" / "semantics" / "integer" / "operands.sail",
        SAIL_SOURCE_ROOT / "instructions" / "semantics" / "integer" / "arithmetic.sail",
        SAIL_SOURCE_ROOT / "instructions" / "semantics" / "integer" / "data_control.sail",
        SAIL_SOURCE_ROOT / "instructions" / "semantics" / "integer" / "routing.sail",
        SAIL_SOURCE_ROOT / "system" / "state" / "system.sail",
        SAIL_SOURCE_ROOT / "system" / "state" / "reset.sail",
        SAIL_SOURCE_ROOT / "memory" / "access" / "transactions.sail",
        SAIL_SOURCE_ROOT / "memory" / "cache" / "evaluations.sail",
        SAIL_SOURCE_ROOT / "system" / "state" / "save_restore.sail",
        SAIL_SOURCE_ROOT / "memory" / "cache" / "transactions.sail",
        SAIL_SOURCE_ROOT / "memory" / "translation" / "model" / "translation.sail",
        SAIL_SOURCE_ROOT / "system" / "requests" / "transactions.sail",
        SAIL_SOURCE_ROOT / "addressing" / "effective_address" / "evaluation" / "transactions.sail",
        SAIL_SOURCE_ROOT / "system" / "stack" / "transactions.sail",
        SAIL_SOURCE_ROOT / "instructions" / "semantics" / "control" / "transactions.sail",
        SAIL_SOURCE_ROOT / "system" / "events" / "events.sail",
        SAIL_SOURCE_ROOT / "execution" / "repeat" / "repeat.sail",
        SAIL_SOURCE_ROOT / "instructions" / "semantics" / "control" / "control.sail",
        SAIL_SOURCE_ROOT / "instructions" / "semantics" / "floating_point" / "local_execution.sail",
        SAIL_SOURCE_ROOT / "instructions" / "semantics" / "floating_point" / "transaction_inputs.sail",
        SAIL_SOURCE_ROOT / "instructions" / "semantics" / "floating_point" / "transaction_compute.sail",
        SAIL_SOURCE_ROOT / "instructions" / "semantics" / "vector" / "vector.sail",
        SAIL_SOURCE_ROOT / "instructions" / "semantics" / "floating_point" / "transaction_flow.sail",
        SAIL_SOURCE_ROOT / "execution" / "core" / "dispatch.sail",
        SAIL_SOURCE_ROOT / "execution" / "core" / "resume_values.sail",
        SAIL_SOURCE_ROOT / "execution" / "core" / "resume_restore.sail",
        SAIL_SOURCE_ROOT / "execution" / "core" / "resume_common.sail",
        SAIL_SOURCE_ROOT / "memory" / "access" / "continuation.sail",
        SAIL_SOURCE_ROOT / "execution" / "core" / "resume_control.sail",
        SAIL_SOURCE_ROOT / "execution" / "core" / "resume_system.sail",
        SAIL_SOURCE_ROOT / "execution" / "core" / "resume_repeat.sail",
        SAIL_SOURCE_ROOT / "execution" / "core" / "resume_events.sail",
        SAIL_SOURCE_ROOT / "execution" / "core" / "resume_fp.sail",
        SAIL_SOURCE_ROOT / "execution" / "core" / "resume.sail",
    ),
    "fp": (
        SAIL_SOURCE_ROOT / "instructions" / "semantics" / "floating_point" / "operation_catalog.sail",
        SAIL_SOURCE_ROOT / "instructions" / "semantics" / "floating_point" / "transcendental_contract.sail",
        SAIL_SOURCE_ROOT / "instructions" / "semantics" / "floating_point" / "register_pairs.sail",
        SAIL_SOURCE_ROOT / "instructions" / "semantics" / "floating_point" / "types.sail",
        SAIL_SOURCE_ROOT / "instructions" / "semantics" / "floating_point" / "environment.sail",
        SAIL_SOURCE_ROOT / "instructions" / "semantics" / "floating_point" / "local_operations.sail",
        SAIL_SOURCE_ROOT / "instructions" / "semantics" / "floating_point" / "request_contract.sail",
        SAIL_SOURCE_ROOT / "instructions" / "semantics" / "floating_point" / "response_contract.sail",
        SAIL_SOURCE_ROOT / "instructions" / "semantics" / "floating_point" / "finalize.sail",
    ),
    "postlude": (SAIL_SOURCE_ROOT / "execution" / "core" / "boundary.sail",),
}
OWNER_MODULES = frozenset(OWNER_SOURCE_PATHS)

sys.path.insert(0, str(TOOLS_ROOT))

import generate_catalog


def _function_record(entry: object) -> tuple[list[str], str] | None:
    if not isinstance(entry, dict):
        return None
    function = entry.get("function")
    if not isinstance(function, dict):
        return None
    raw_path = function.get("path", entry.get("path", []))
    path = [str(item) for item in raw_path] if isinstance(raw_path, list) else []
    source = function.get("source", function.get("body", ""))
    return path, source if isinstance(source, str) else ""


def _balanced_block(source: str, opening: int) -> str:
    depth = 0
    quoted = False
    escaped = False
    for index in range(opening, len(source)):
        char = source[index]
        if quoted:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                quoted = False
            continue
        if char == '"':
            quoted = True
        elif char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return source[opening + 1:index]
    raise ValueError("unterminated Sail block in documentation source")


def _split_top_level(text: str) -> list[str]:
    parts = []
    start = 0
    round_depth = square_depth = curly_depth = 0
    quoted = False
    escaped = False
    for index, char in enumerate(text):
        if quoted:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                quoted = False
            continue
        if char == '"':
            quoted = True
        elif char == "(":
            round_depth += 1
        elif char == ")":
            round_depth -= 1
        elif char == "[":
            square_depth += 1
        elif char == "]":
            square_depth -= 1
        elif char == "{":
            curly_depth += 1
        elif char == "}":
            curly_depth -= 1
        elif char == "," and round_depth == square_depth == curly_depth == 0:
            part = text[start:index].strip()
            if part:
                parts.append(part)
            start = index + 1
    tail = text[start:].strip()
    if tail:
        parts.append(tail)
    if any(depth != 0 for depth in (round_depth, square_depth, curly_depth)):
        raise ValueError("unbalanced Sail dispatch arm in documentation source")
    return parts


def _route_dispatch_arms(source: str) -> dict[str, str] | None:
    matches = list(re.finditer(r"\bmatch\s+instruction\.form\.route\s*\{", source))
    if not matches:
        return None
    if len(matches) != 1:
        raise ValueError("ambiguous route dispatch in Sail documentation source")
    block = _balanced_block(source, source.find("{", matches[0].start()))
    arms: dict[str, str] = {}
    for part in _split_top_level(block):
        match = re.match(r"(Route[A-Za-z0-9_]+|_)\s*=>\s*(.*)\Z", part, re.DOTALL)
        if match is None:
            raise ValueError(f"unrecognized Sail route dispatch arm: {part[:80]}")
        label, body = match.groups()
        if label in arms:
            raise ValueError(f"duplicate Sail route dispatch arm: {label}")
        arms[label] = body
    return arms


def _operation_discriminators(source: str) -> set[str]:
    operations = set(re.findall(r"(?m)^\s*(Op_[A-Za-z0-9_]+)\s*=>", source))
    operations.update(re.findall(
        r"\b[A-Za-z_][A-Za-z0-9_.]*operation\s*==\s*(Op_[A-Za-z0-9_]+)\b",
        source,
    ))
    operations.update(re.findall(
        r"\boperation\s*==\s*(Op_[A-Za-z0-9_]+)\b",
        source,
    ))
    return operations


def _owner_function_graph(
    functions: dict[str, object],
) -> tuple[dict[str, str], dict[str, str]]:
    sources: dict[str, str] = {}
    qualified_by_name: dict[str, str] = {}
    for name, entry in functions.items():
        record = _function_record(entry)
        if record is None:
            continue
        path, source = record
        if not path or path[0] not in OWNER_MODULES:
            continue
        plain = str(name)
        qualified = f"{path[0]}.{plain}"
        previous = qualified_by_name.setdefault(plain, qualified)
        if previous != qualified:
            raise ValueError(f"ambiguous Sail owner function: {plain}")
        sources[qualified] = source
    return sources, qualified_by_name


def _known_calls(
    source: str,
    qualified_by_name: dict[str, str],
) -> set[str]:
    return {
        qualified_by_name[name]
        for name in re.findall(r"\b([a-z][A-Za-z0-9_]*)\s*\(", source)
        if name in qualified_by_name
    }


def _catalog_predicate_modes(functions: dict[str, object]) -> dict[str, set[str]]:
    catalog_record = _function_record(functions.get("primary_form_catalog"))
    if catalog_record is None:
        raise ValueError("Sail documentation bundle lacks primary_form_catalog")
    modes: dict[str, set[str]] = {}
    for mnemonic, mode in re.findall(
        r"\boperation\s*=\s*Op_([A-Za-z0-9_]+)\b"
        r"(?:(?!\boperation\s*=).)*?"
        r"\bpredicate_mode\s*=\s*([A-Za-z0-9_]+)\b",
        catalog_record[1],
        re.DOTALL,
    ):
        modes.setdefault(mnemonic, set()).add(mode)
    return modes


def _predicate_dispatch_owners(
    sources: dict[str, str],
    qualified_by_name: dict[str, str],
) -> dict[str, set[str]]:
    owners: dict[str, set[str]] = {}
    dispatch_pattern = re.compile(
        r"\bpredicate_mode\s*==\s*([A-Za-z0-9_]+)\b"
        r"(?:(?!\bthen\b).)*?\bthen\s*\{?\s*"
        r"([A-Za-z_][A-Za-z0-9_]*)\s*\(",
        re.DOTALL,
    )
    for qualified, source in sources.items():
        for mode, callee in dispatch_pattern.findall(source):
            resolved = qualified_by_name.get(callee)
            if resolved is None:
                raise ValueError(f"unresolved Sail predicate dispatcher: {callee}")
            owners.setdefault(mode, set()).update({qualified, resolved})
    return owners


def build_semantic_index(doc_bundle: dict[str, object]) -> dict[str, object]:
    """Derive the operation/form ownership index from a Sail documentation bundle."""
    types = doc_bundle.get("types")
    functions = doc_bundle.get("functions")
    if not isinstance(types, dict) or not isinstance(functions, dict):
        raise ValueError("Sail documentation bundle lacks types or functions")

    store, _, _, documents = generate_catalog._load_inputs()
    expected_mnemonics = set(documents)

    operation_type = types.get("Semantic_operation")
    if not isinstance(operation_type, dict) or not isinstance(operation_type.get("type"), str):
        raise ValueError("Sail documentation bundle lacks Semantic_operation")
    mnemonics = sorted(set(re.findall(r"\bOp_([A-Za-z0-9_]+)\b", operation_type["type"])))
    if set(mnemonics) != expected_mnemonics:
        raise ValueError("Sail operation inventory differs from instruction definitions")

    semantic_route = functions.get("semantic_route")
    route_record = _function_record(semantic_route)
    if route_record is None:
        raise ValueError("Sail documentation bundle lacks semantic_route")
    route_source = route_record[1]
    route_pairs = re.findall(
        r"\bOp_([A-Za-z0-9_]+)\s*=>\s*(Route[A-Za-z0-9_]+)\b",
        route_source,
    )
    routes: dict[str, str] = {}
    for mnemonic, route in route_pairs:
        previous = routes.setdefault(mnemonic, route)
        if previous != route:
            raise ValueError(f"conflicting routes for {mnemonic}: {previous}, {route}")
    if set(routes) != set(mnemonics):
        raise ValueError(f"unexpected Sail route inventory: {len(routes)}")

    owner_sources, qualified_by_name = _owner_function_graph(functions)
    operations_by_route: dict[str, set[str]] = {}
    for mnemonic, route in routes.items():
        operations_by_route.setdefault(route, set()).add(f"Op_{mnemonic}")
    expected_routes = {
        generate_catalog.ROUTE_CONSTRUCTORS[document.execution_route]
        for document in documents.values()
    }
    if set(operations_by_route) != expected_routes:
        raise ValueError("Sail route classes differ from instruction definitions")
    operation_entries: dict[str, tuple[str | None, ...]] = {}
    for document in documents.values():
        entries = tuple(dict.fromkeys(
            qualified_by_name.get(case.sail_entry)
            for case in document.cases
        ))
        operation_entries[document.public_instruction.mnemonic] = entries
    missing_entries = sorted(
        mnemonic for mnemonic, qualified in operation_entries.items()
        if not qualified
        or any(entry is None or not entry.startswith("operation_entries.") for entry in qualified)
    )
    if missing_entries:
        raise ValueError(
            "Sail operation-entry dispatcher is incomplete: "
            + ", ".join(missing_entries)
        )
    route_owners = {
        route: sorted(
            entry
            for mnemonic in mnemonics
            for entry in operation_entries[mnemonic]
            if routes[mnemonic] == route
        )
        for route in sorted(operations_by_route)
    }

    forms_by_mnemonic: dict[str, list[str]] = {mnemonic: [] for mnemonic in mnemonics}
    forms: list[dict[str, str]] = []
    for located in sorted(store.encodings, key=lambda item: item.form.id):
        mnemonic = located.mnemonic
        if mnemonic not in routes:
            raise ValueError(f"encoding form has no Sail operation: {located.form.id}")
        form_id = located.form.id
        forms_by_mnemonic[mnemonic].append(form_id)
        forms.append({
            "form_id": form_id,
            "mnemonic": mnemonic,
            "operation": f"Op_{mnemonic}",
            "route": routes[mnemonic],
        })
    if len({form["form_id"] for form in forms}) != len(forms):
        raise ValueError("duplicate encoding form IDs in semantic index")

    operations = []
    for mnemonic in mnemonics:
        operation = f"Op_{mnemonic}"
        route = routes[mnemonic]
        direct_functions = list(operation_entries[mnemonic])
        owning_route_functions = route_owners[route]
        operations.append({
            "mnemonic": mnemonic,
            "operation": operation,
            "route": route,
            "form_ids": forms_by_mnemonic[mnemonic],
            "direct_functions": direct_functions,
            "route_owner_functions": owning_route_functions,
            "ownership": "direct",
        })

    return {
        "schema_version": 1,
        "operations": operations,
        "forms": forms,
        "routes": [
            {"route": route, "owner_functions": route_owners[route]}
            for route in sorted(route_owners)
        ],
    }


def render_semantic_index(doc_bundle: dict[str, object]) -> str:
    return json.dumps(build_semantic_index(doc_bundle), indent=2, sort_keys=True) + "\n"


def build_docs(raw_build_dir: Path) -> tuple[Path, Path]:
    build_dir = generate_catalog.validate_build_dir(raw_build_dir)
    build_dir.mkdir(parents=True, exist_ok=True)
    generate_catalog.write_outputs(build_dir)

    command = [
        "opam", "exec", "--", "sail",
        "--require-version", "0.20.2",
        "--no-memo-z3",
        "--all-modules",
        "-o", str(build_dir / "sail_doc"),
        "--doc",
        "--doc-format", "asciidoc",
        "--doc-embed", "plain",
        "--doc-compact",
        "--doc-bundle", "bedrock-sail.json",
        str(SAIL_PROJECT),
        str(build_dir / "bedrock-generated.sail_project"),
    ]
    subprocess.run(command, cwd=SAIL_SOURCE_ROOT, check=True)

    sail_output = build_dir / "sail_doc" / "bedrock-sail.json"
    if not sail_output.is_file():
        raise ValueError(f"Sail did not produce its documentation bundle: {sail_output}")
    bundle_output = build_dir / "bedrock-sail.json"
    sail_output.replace(bundle_output)
    try:
        sail_output.parent.rmdir()
    except OSError:
        pass

    with bundle_output.open(encoding="utf-8") as source:
        doc_bundle = json.load(source)
    if not isinstance(doc_bundle, dict):
        raise ValueError("Sail documentation bundle must be a JSON object")
    index_output = build_dir / "semantic-index.json"
    index_output.write_text(render_semantic_index(doc_bundle), encoding="utf-8")
    return bundle_output, index_output


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "build_dir",
        metavar="BUILD_DIR",
        type=Path,
        help="dedicated directory beneath repository build/ or an external temporary directory",
    )
    args = parser.parse_args()
    try:
        bundle, index = build_docs(args.build_dir)
    except (OSError, ValueError, subprocess.CalledProcessError, json.JSONDecodeError) as error:
        print(f"sail documentation build failed: {error}", file=sys.stderr)
        return 1
    print(bundle)
    print(index)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
